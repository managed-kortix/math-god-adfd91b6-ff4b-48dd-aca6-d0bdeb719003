#!/usr/bin/env python3
"""Fail-closed manifest and exact auditor for R9G1 search packs."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PIPELINE_PATH = HERE / "rank6_order9_sparse_witness.py"
BASE_PATH = HERE / "rank6_order8_sparse_pipeline.py"
ENGINE_PATH = ROOT / "pentacyclic" / "research" / "order7-dim7-rational-gram-experiment.py"
RECOGNIZER_PATH = HERE / "rank6_order9_symbolic_recognizers.py"
CLASSIFIER_PATH = HERE / "rank6_orders8_10_atom_ledger_search.py"
CLASSIFICATION_PATH = HERE / "rank6_orders8_10_atom_ledger_classification.json"
KERNEL_PATH = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
DEFAULT_MANIFEST = HERE / "rank6_order9_search_manifest.json"
SCHEMA = "rank-six-order-nine-r9g-search-pack-manifest-v1"
CHUNK_RECEIPT_SCHEMA = "rank-six-order-nine-exact-chunk-proof-receipt-v2"
AGGREGATE_RECEIPT_SCHEMA = "rank-six-order-nine-segmented-proof-aggregate-v2"
FRONTIER_TOTAL = 15
RECORD_MODE_FIELDS = {"shared", "template", "individual", "unresolved"}
EXPECTED_SYMBOLIC_REPORT = {
    "classification_sha256": "cc20f4c684ef269297cd7c1d2bc888508fdc31f16cc26e8cb1c2e86792052059",
    "decomposition_total": 82,
    "exact_target_total": 388,
    "geometry_row_counts": {
        "coupled-triangle-tetrahedron": 14,
        "signed-five-cycle": 10,
        "tetrahedron-plus-apex": 56,
    },
    "recognized_row_total": 80,
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def auditor_sha256():
    return sha256(Path(__file__).resolve().read_bytes())


def strict_json(raw, label):
    def object_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise RuntimeError(f"nonstandard constant in {label}: {value}")

    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=object_pairs,
                          parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label} is not strict ASCII JSON") from error


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_pipeline(name):
    wrapper = load_module(name, PIPELINE_PATH)
    pipeline = wrapper.base
    require(pipeline.MAGIC == b"R9G1" and pipeline.ORDER == 9 and pipeline.PATH_COUNT == 14,
            "witness pipeline configuration changed")
    return pipeline


def exact_nonnegative_int(value, label):
    require(type(value) is int and value >= 0, f"bad {label}")


def digest_string(value, label):
    require(type(value) is str and len(value) == 64 and
            all(character in "0123456789abcdef" for character in value), f"bad {label}")


def dependency_digests():
    paths = {
        "atom_classification": CLASSIFICATION_PATH,
        "atom_classifier": CLASSIFIER_PATH,
        "kernel_source": KERNEL_PATH,
        "rational_engine": ENGINE_PATH,
        "sparse_base": BASE_PATH,
        "symbolic_recognizer": RECOGNIZER_PATH,
        "witness_pipeline": PIPELINE_PATH,
    }
    return {name: sha256(path.read_bytes()) for name, path in paths.items()}


def target_frontier(target):
    return None if target == 0 else target - 1


def key_digest(residuals, stop):
    digest = hashlib.sha256()
    for source_index, source in enumerate(residuals[:stop]):
        number, _, _, row, _, _, _ = source
        for target in range(FRONTIER_TOTAL):
            digest.update(canonical_bytes(
                [source_index, number, list(row), target_frontier(target)]))
    return digest.hexdigest()


def symbolic_ownership(pipeline):
    recognizer = load_module("rank6_order9_symbolic_for_pack_audit", RECOGNIZER_PATH)
    report, keys = recognizer.derive(pipeline)
    require(report == EXPECTED_SYMBOLIC_REPORT, "symbolic ownership report changed")
    require(type(keys) is frozenset and len(keys) == report["exact_target_total"],
            "symbolic ownership key set changed")
    ordered = sorted(keys, key=lambda key: (key[0], -1 if key[1] is None else key[1]))
    require(all(type(key) is tuple and len(key) == 2 and type(key[0]) is int and
                key[0] >= 0 and (key[1] is None or type(key[1]) is int and
                                 0 <= key[1] < FRONTIER_TOTAL - 1)
                for key in ordered), "bad symbolic ownership key")
    digest = hashlib.sha256()
    for source_index, frontier in ordered:
        digest.update(canonical_bytes([source_index, frontier]))
    return keys, report, digest.hexdigest()


def load_manifest(path):
    raw = path.read_bytes()
    payload = strict_json(raw, "manifest")
    require(raw == canonical_bytes(payload), "manifest is not canonical JSON")
    require(type(payload) is dict and set(payload) == {
        "schema", "source_sha256", "symbolic_sha256", "dependency_sha256",
        "residual_total", "frontiers_per_residual", "chunks",
        "covered_residual_range", "covered_target_total", "covered_key_stream_sha256",
    }, "manifest fields changed")
    require(payload["schema"] == SCHEMA, "manifest schema changed")
    for field in ("source_sha256", "symbolic_sha256", "covered_key_stream_sha256"):
        digest_string(payload[field], f"manifest {field}")
    for field in ("residual_total", "frontiers_per_residual", "covered_target_total"):
        exact_nonnegative_int(payload[field], f"manifest {field}")
    require(type(payload["dependency_sha256"]) is dict and
            all(type(key) is str for key in payload["dependency_sha256"]),
            "bad manifest dependency digest map")
    for key, value in payload["dependency_sha256"].items():
        digest_string(value, f"dependency {key}")
    covered_range = payload["covered_residual_range"]
    require(type(covered_range) is list and len(covered_range) == 2 and
            all(type(value) is int and value >= 0 for value in covered_range),
            "bad manifest covered range")
    return payload


def manifest_sha256(manifest):
    return sha256(canonical_bytes(manifest))


def read_chunks(manifest_path, manifest, pipeline, residuals, chunk_index=None,
                consume=None):
    chunks = manifest["chunks"]
    require(type(chunks) is list and chunks, "manifest has no chunks")
    expected_start = 0
    decoded = []
    root = manifest_path.parent.resolve()
    for index, chunk in enumerate(chunks):
        require(type(chunk) is dict and set(chunk) == {
            "path", "residual_range", "compressed_bytes", "compressed_sha256",
            "raw_bytes", "raw_sha256",
        }, f"bad chunk {index} manifest record")
        require(type(chunk["path"]) is str and chunk["path"], f"bad chunk {index} path")
        residual_range = chunk["residual_range"]
        require(type(residual_range) is list and len(residual_range) == 2,
                f"bad chunk {index} range")
        start, stop = residual_range
        require(type(start) is int and type(stop) is int and
                start == expected_start < stop <= len(residuals),
                f"chunk {index} range is not the next ordered interval")
        for field in ("compressed_bytes", "raw_bytes"):
            exact_nonnegative_int(chunk[field], f"chunk {index} {field}")
        for field in ("compressed_sha256", "raw_sha256"):
            digest_string(chunk[field], f"chunk {index} {field}")
        path = (manifest_path.parent / chunk["path"]).resolve()
        try:
            path.relative_to(root)
        except ValueError as error:
            raise RuntimeError(f"chunk {index} escapes the manifest directory") from error
        stored = path.read_bytes()
        require(len(stored) == chunk["compressed_bytes"] and
                sha256(stored) == chunk["compressed_sha256"],
                f"chunk {index} compressed artifact changed")
        expected_start = stop
        if chunk_index is not None and index != chunk_index:
            continue
        try:
            raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
        except lzma.LZMAError as error:
            raise RuntimeError(f"chunk {index} is not a valid XZ stream") from error
        require(len(raw) == chunk["raw_bytes"] and sha256(raw) == chunk["raw_sha256"],
                f"chunk {index} raw stream changed")
        actual_start, attempts, records = pipeline.decode_search(raw, residuals)
        require(actual_start == start and attempts == stop - start and
                len(records) == attempts, f"chunk {index} embedded range changed")
        if consume is None:
            decoded.append((start, records))
        else:
            consume(start, records)
    return expected_start, decoded


def exact_certificates(pipeline, residuals, decoded, symbolic_keys):
    engine = pipeline.load_engine()
    certified = set()
    unresolved = set()
    symbolic_exact = set()
    modes = {"shared": 0, "template": 0, "individual": 0, "unresolved": 0}
    for start, records in decoded:
        for local, record in enumerate(records):
            source_index = start + local
            mode = record[0]
            if mode == pipeline.MODE_SHARED:
                modes["shared"] += 1
            elif mode == pipeline.MODE_TEMPLATE:
                modes["template"] += 1
            elif mode == pipeline.MODE_INDIVIDUAL:
                modes["individual"] += 1
            else:
                require(mode == pipeline.MODE_UNRESOLVED, "unknown decoded mode")
                modes["unresolved"] += 1
            costs = pipeline.verify_record(engine, residuals[source_index], record)
            require(type(costs) is tuple and len(costs) == FRONTIER_TOTAL,
                    "record audit did not return every target")
            for target, cost in enumerate(costs):
                key = (source_index, target_frontier(target))
                if cost is None:
                    unresolved.add(key)
                else:
                    certified.add(key)
                    if key in symbolic_keys:
                        symbolic_exact.add(key)
    unexpected = unresolved - symbolic_keys
    require(not unexpected, f"unrecognized unresolved targets: {len(unexpected)}")
    return certified, unresolved, symbolic_exact, modes


def audit(manifest_path, exact=True, chunk_index=None):
    manifest = load_manifest(manifest_path)
    dependencies = dependency_digests()
    require(manifest["dependency_sha256"] == dependencies,
            "transitive dependency digest changed")
    pipeline = load_pipeline("rank6_order9_for_pack_audit")
    require(manifest["source_sha256"] == pipeline.SOURCE_SHA256 ==
            dependencies["kernel_source"], "kernel source ownership changed")
    census_payload, residuals = pipeline.census(collect_residuals=True)
    require(manifest["residual_total"] == len(residuals) ==
            census_payload["coarse_residual_total"], "regenerated residual census changed")
    require(manifest["frontiers_per_residual"] == FRONTIER_TOTAL ==
            census_payload["frontiers_per_residual"], "manifest frontier width changed")
    symbolic_keys, symbolic_report, symbolic_sha256 = symbolic_ownership(pipeline)
    require(all(source_index < len(residuals) for source_index, _ in symbolic_keys),
            "symbolic source index exceeds regenerated census")
    require(manifest["symbolic_sha256"] == symbolic_sha256,
            "symbolic ownership stream digest changed")
    chunks = manifest["chunks"]
    if chunk_index is not None:
        require(type(chunk_index) is int and 0 <= chunk_index < len(chunks),
                "chunk index is out of range")
    totals = None
    if chunk_index is None:
        totals = ({
            "numerical": 0,
            "unresolved": 0,
            "symbolic_exact": set(),
            "symbolic_certified": set(),
            "modes": {"shared": 0, "template": 0, "individual": 0, "unresolved": 0},
        } if exact else {})

        def consume(start, records):
            if not exact:
                return
            numerical, unresolved, symbolic_exact, modes = exact_certificates(
                pipeline, residuals, [(start, records)], symbolic_keys)
            stop = start + len(records)
            expected = {key for key in symbolic_keys if start <= key[0] < stop}
            symbolic_certified = unresolved & expected
            require(len(numerical) + len(symbolic_certified) ==
                    len(records) * FRONTIER_TOTAL,
                    "chunk exact ownership is incomplete")
            require(expected <= symbolic_exact | symbolic_certified,
                    "symbolically owned target lacks an exact certificate")
            totals["numerical"] += len(numerical)
            totals["unresolved"] += len(unresolved)
            totals["symbolic_exact"].update(symbolic_exact)
            totals["symbolic_certified"].update(symbolic_certified)
            for mode, count in modes.items():
                totals["modes"][mode] += count

        manifest_covered, decoded = read_chunks(
            manifest_path, manifest, pipeline, residuals, consume=consume)
    else:
        manifest_covered, decoded = read_chunks(
            manifest_path, manifest, pipeline, residuals, chunk_index)
    require(manifest["covered_residual_range"] == [0, manifest_covered] and
            manifest["covered_target_total"] == manifest_covered * FRONTIER_TOTAL,
            "manifest coverage totals changed")
    require(manifest["covered_key_stream_sha256"] == key_digest(residuals, manifest_covered),
            "covered ordered target key stream digest changed")

    if chunk_index is None:
        covered_start, covered_stop = 0, manifest_covered
        replay_scope = "full-manifest"
    else:
        covered_start, covered_stop = chunks[chunk_index]["residual_range"]
        replay_scope = "single-chunk"
    covered = covered_stop - covered_start

    expected_symbolic = {
        key for key in symbolic_keys if covered_start <= key[0] < covered_stop
    }
    if exact and totals is not None:
        numerical_count = totals["numerical"]
        unresolved_count = totals["unresolved"]
        symbolic_exact = totals["symbolic_exact"]
        symbolic_certified = totals["symbolic_certified"]
        certified_count = numerical_count + len(symbolic_certified)
        modes = totals["modes"]
        require(expected_symbolic <= symbolic_exact | symbolic_certified,
                "symbolically owned target lacks an exact certificate")
    elif exact:
        numerical, unresolved, symbolic_exact, modes = exact_certificates(
            pipeline, residuals, decoded, symbolic_keys)
        symbolic_certified = unresolved & expected_symbolic
        certified = numerical | symbolic_certified
        require(expected_symbolic <= symbolic_exact | symbolic_certified,
                "symbolically owned target lacks an exact certificate")
        numerical_count = len(numerical)
        unresolved_count = len(unresolved)
        certified_count = len(certified)
    else:
        numerical = unresolved = symbolic_exact = symbolic_certified = certified = set()
        numerical_count = unresolved_count = certified_count = 0
        modes = {"shared": 0, "template": 0, "individual": 0, "unresolved": 0}
    replay_complete = exact and certified_count == covered * FRONTIER_TOTAL
    complete = replay_complete and (chunk_index is not None or manifest_covered == len(residuals))
    report = {
        "status": "complete" if complete else "incomplete",
        "replay_scope": replay_scope,
        "theorem_gate_eligible": bool(
            complete and chunk_index is None and manifest_covered == len(residuals)),
        "census": {
            "kernel_interval": census_payload["kernel_interval"],
            "kernel_total": census_payload["kernel_total"],
            "physical_total": census_payload["physical_total"],
            "parity_orbit_total": census_payload["parity_orbit_total"],
            "coarse_certified_total": census_payload["coarse_certified_total"],
            "coarse_residual_total": census_payload["coarse_residual_total"],
            "frontier_target_total": census_payload["frontier_target_total"],
        },
        "covered_residual_range": [covered_start, covered_stop],
        "manifest_covered_residual_range": [0, manifest_covered],
        "residual_total": len(residuals),
        "missing_residual_total": len(residuals) - manifest_covered,
        "covered_target_total": covered * FRONTIER_TOTAL,
        "missing_target_total": (len(residuals) - manifest_covered) * FRONTIER_TOTAL,
        "exact_certified_target_total": certified_count,
        "uncertified_target_total": covered * FRONTIER_TOTAL - certified_count,
        "unresolved_target_total": unresolved_count,
        "symbolic_owned_target_total": len(expected_symbolic),
        "symbolic_numerically_certified_target_total": len(symbolic_exact),
        "symbolic_only_certified_target_total": len(symbolic_certified),
        "disjoint_rational_owner_target_total": numerical_count,
        "disjoint_symbolic_owner_target_total": len(symbolic_certified),
        "symbolic_decomposition_total": symbolic_report["decomposition_total"],
        "symbolic_geometry_row_counts": symbolic_report["geometry_row_counts"],
        "record_modes": modes,
        "exact_audit": exact,
    }
    return report, complete


def chunk_receipt_payload(manifest_path, chunk_index, report):
    manifest = load_manifest(manifest_path)
    require(type(chunk_index) is int and 0 <= chunk_index < len(manifest["chunks"]),
            "chunk index is out of range")
    chunk = manifest["chunks"][chunk_index]
    start, stop = chunk["residual_range"]
    validate_chunk_report(report, start, stop, manifest)
    return {
        "schema": CHUNK_RECEIPT_SCHEMA,
        "receipt_kind": "independent-exact-replay",
        "theorem_evidence": True,
        "auditor_sha256": auditor_sha256(),
        "manifest_sha256": manifest_sha256(manifest),
        "dependency_sha256": manifest["dependency_sha256"],
        "covered_key_stream_sha256": manifest["covered_key_stream_sha256"],
        "chunk_index": chunk_index,
        "chunk": chunk,
        "report": report,
        "notice": "repository execution evidence from one exact replay; digests bind inputs and bytes but are not proof that execution occurred",
    }


def validate_chunk_report(report, start, stop, manifest):
    require(type(report) is dict, "chunk report is not an object")
    require(report.get("status") == "complete" and report.get("exact_audit") is True and
            report.get("replay_scope") == "single-chunk" and
            report.get("theorem_gate_eligible") is False,
            "chunk report is not an independent exact replay")
    width = stop - start
    require(report.get("covered_residual_range") == [start, stop] and
            report.get("manifest_covered_residual_range") ==
            manifest["covered_residual_range"] and
            report.get("residual_total") == manifest["residual_total"] and
            report.get("covered_target_total") == width * FRONTIER_TOTAL,
            "chunk report coverage changed")
    require(report.get("missing_residual_total") ==
            manifest["residual_total"] - manifest["covered_residual_range"][1] and
            report.get("missing_target_total") ==
            (manifest["residual_total"] - manifest["covered_residual_range"][1]) *
            FRONTIER_TOTAL, "chunk report manifest bookkeeping changed")
    certified = report.get("exact_certified_target_total")
    rational = report.get("disjoint_rational_owner_target_total")
    symbolic = report.get("disjoint_symbolic_owner_target_total")
    require(type(certified) is int and certified == width * FRONTIER_TOTAL and
            report.get("uncertified_target_total") == 0 and
            type(rational) is int and type(symbolic) is int and
            rational + symbolic == certified,
            "chunk report ownership totals changed")
    modes = report.get("record_modes")
    require(type(modes) is dict and set(modes) == RECORD_MODE_FIELDS and
            all(type(value) is int and value >= 0 for value in modes.values()) and
            sum(modes.values()) == width, "chunk report mode totals changed")


def load_receipt(path, label):
    raw = path.read_bytes()
    payload = strict_json(raw, label)
    require(raw == canonical_bytes(payload), f"{label} is not canonical JSON")
    return raw, payload


def authenticate_chunk_receipt(manifest_path, receipt_path, authenticated=None):
    """Validate a replay receipt; its digests identify bytes, not execution."""
    manifest = load_manifest(manifest_path) if authenticated is None else authenticated
    raw, receipt = load_receipt(receipt_path, "exact chunk replay receipt")
    require(type(receipt) is dict and set(receipt) == {
        "schema", "receipt_kind", "theorem_evidence", "auditor_sha256",
        "manifest_sha256", "dependency_sha256", "covered_key_stream_sha256",
        "chunk_index", "chunk", "report", "notice",
    }, "chunk receipt fields changed")
    require(receipt["schema"] == CHUNK_RECEIPT_SCHEMA and
            receipt["receipt_kind"] == "independent-exact-replay" and
            receipt["theorem_evidence"] is True,
            "chunk receipt overstates its evidentiary role")
    require(receipt["auditor_sha256"] == auditor_sha256(), "receipted auditor changed")
    require(receipt["manifest_sha256"] == manifest_sha256(manifest),
            "receipted manifest changed")
    require(receipt["dependency_sha256"] == manifest["dependency_sha256"],
            "receipted dependencies changed")
    require(receipt["covered_key_stream_sha256"] == manifest["covered_key_stream_sha256"],
            "receipted target key stream changed")
    index = receipt["chunk_index"]
    require(type(index) is int and 0 <= index < len(manifest["chunks"]),
            "receipted chunk index is out of range")
    require(receipt["chunk"] == manifest["chunks"][index], "receipted chunk changed")
    start, stop = receipt["chunk"]["residual_range"]
    validate_chunk_report(receipt["report"], start, stop, manifest)
    return raw, receipt


def build_receipt_aggregate(manifest_path, receipt_paths, aggregate_path):
    manifest = load_manifest(manifest_path)
    aggregate_root = aggregate_path.parent.resolve()
    records = []
    reports = []
    seen = set()
    for path in receipt_paths:
        raw, receipt = authenticate_chunk_receipt(manifest_path, path, manifest)
        index = receipt["chunk_index"]
        require(index not in seen, f"duplicate chunk receipt: {index}")
        seen.add(index)
        resolved = path.resolve()
        try:
            relative = resolved.relative_to(aggregate_root).as_posix()
        except ValueError as error:
            raise RuntimeError("chunk receipt is outside the aggregate directory") from error
        records.append({
            "chunk_index": index,
            "path": relative,
            "receipt_sha256": sha256(raw),
        })
        reports.append(receipt["report"])
    require(seen == set(range(len(manifest["chunks"]))),
            "aggregate requires exactly one receipt for every manifest chunk")
    records.sort(key=lambda record: record["chunk_index"])
    covered_targets = sum(report["covered_target_total"] for report in reports)
    certified_targets = sum(report["exact_certified_target_total"] for report in reports)
    require(covered_targets == certified_targets == manifest["covered_target_total"],
            "aggregate target bookkeeping changed")
    return {
        "schema": AGGREGATE_RECEIPT_SCHEMA,
        "status": "proof-complete",
        "receipt_kind": "segmented-independent-exact-replays",
        "theorem_evidence": True,
        "auditor_sha256": auditor_sha256(),
        "manifest_sha256": manifest_sha256(manifest),
        "dependency_sha256": manifest["dependency_sha256"],
        "covered_key_stream_sha256": manifest["covered_key_stream_sha256"],
        "chunks": records,
        "bookkeeping": {
            "covered_residual_range": manifest["covered_residual_range"],
            "covered_target_total": covered_targets,
            "exact_certified_target_total_recorded": certified_targets,
            "chunk_receipt_total": len(records),
        },
        "notice": "accepted repository proof artifact under the segmented replay policy; digests bind identities and are not execution proof",
    }


def authenticate_receipt_aggregate(manifest_path, aggregate_path):
    manifest = load_manifest(manifest_path)
    raw, aggregate = load_receipt(aggregate_path, "segmented exact replay aggregate")
    require(type(aggregate) is dict and set(aggregate) == {
        "schema", "status", "receipt_kind", "theorem_evidence", "auditor_sha256",
        "manifest_sha256", "dependency_sha256", "covered_key_stream_sha256",
        "chunks", "bookkeeping", "notice",
    }, "segmented aggregate fields changed")
    require(aggregate["schema"] == AGGREGATE_RECEIPT_SCHEMA and
            aggregate["status"] == "proof-complete" and
            aggregate["receipt_kind"] == "segmented-independent-exact-replays" and
            aggregate["theorem_evidence"] is True,
            "aggregate overstates or weakens its evidentiary role")
    require(aggregate["auditor_sha256"] == auditor_sha256(),
            "aggregate auditor changed")
    require(aggregate["manifest_sha256"] == manifest_sha256(manifest),
            "aggregate manifest changed")
    require(aggregate["dependency_sha256"] == manifest["dependency_sha256"] and
            aggregate["covered_key_stream_sha256"] ==
            manifest["covered_key_stream_sha256"],
            "aggregate transitive inputs changed")
    records = aggregate["chunks"]
    require(type(records) is list and len(records) == len(manifest["chunks"]),
            "aggregate chunk count changed")
    root = aggregate_path.parent.resolve()
    receipt_paths = []
    for expected_index, record in enumerate(records):
        require(type(record) is dict and set(record) == {
            "chunk_index", "path", "receipt_sha256",
        }, "aggregate chunk record fields changed")
        require(record["chunk_index"] == expected_index and
                type(record["path"]) is str and record["path"],
                "aggregate chunk order or path changed")
        path = (aggregate_path.parent / record["path"]).resolve()
        try:
            path.relative_to(root)
        except ValueError as error:
            raise RuntimeError("aggregate receipt path escapes its directory") from error
        receipt_raw, receipt = authenticate_chunk_receipt(manifest_path, path, manifest)
        require(receipt["chunk_index"] == expected_index and
                sha256(receipt_raw) == record["receipt_sha256"],
                "aggregate receipt identity changed")
        receipt_paths.append(path)
    bookkeeping = aggregate["bookkeeping"]
    require(bookkeeping == {
        "covered_residual_range": manifest["covered_residual_range"],
        "covered_target_total": manifest["covered_target_total"],
        "exact_certified_target_total_recorded": manifest["covered_target_total"],
        "chunk_receipt_total": len(manifest["chunks"]),
    }, "aggregate exact coverage bookkeeping changed")
    return raw, aggregate, tuple(receipt_paths)


def build_manifest(output, paths):
    require(output.parent.is_dir(), "manifest output parent does not exist")
    resolved = tuple(path.resolve() for path in paths)
    require(len(set(resolved)) == len(resolved), "duplicate pack path")
    pipeline = load_pipeline("rank6_order9_for_manifest")
    census_payload, residuals = pipeline.census(collect_residuals=True)
    require(len(residuals) == census_payload["coarse_residual_total"],
            "regenerated residual census changed")
    _, _, symbolic_sha256 = symbolic_ownership(pipeline)
    chunks = []
    for path in paths:
        stored = path.read_bytes()
        try:
            raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
        except lzma.LZMAError as error:
            raise RuntimeError(f"{path.name} is not a valid XZ stream") from error
        start, attempts, records = pipeline.decode_search(raw, residuals)
        require(attempts == len(records), f"{path.name} record count changed")
        chunks.append((start, start + attempts, path, stored, raw))
    chunks.sort(key=lambda item: item[0])
    require(chunks, "no packs supplied")
    expected_start = 0
    records = []
    for index, (start, stop, path, stored, raw) in enumerate(chunks):
        require(start == expected_start < stop, f"pack {index} leaves a gap or overlaps")
        try:
            relative = path.resolve().relative_to(output.parent.resolve()).as_posix()
        except ValueError as error:
            raise RuntimeError("pack is outside the manifest directory") from error
        records.append({
            "path": relative,
            "residual_range": [start, stop],
            "compressed_bytes": len(stored),
            "compressed_sha256": sha256(stored),
            "raw_bytes": len(raw),
            "raw_sha256": sha256(raw),
        })
        expected_start = stop
    payload = {
        "schema": SCHEMA,
        "source_sha256": pipeline.SOURCE_SHA256,
        "symbolic_sha256": symbolic_sha256,
        "dependency_sha256": dependency_digests(),
        "residual_total": len(residuals),
        "frontiers_per_residual": FRONTIER_TOTAL,
        "chunks": records,
        "covered_residual_range": [0, expected_start],
        "covered_target_total": expected_start * FRONTIER_TOTAL,
        "covered_key_stream_sha256": key_digest(residuals, expected_start),
    }
    output.write_bytes(canonical_bytes(payload))
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--digest-only", action="store_true",
                        help="check dependencies, ranges, bytes, keys, and symbolic ownership")
    parser.add_argument("--build-manifest", nargs="+", type=Path, metavar="PACK")
    parser.add_argument("--chunk-index", type=int,
                        help="exactly replay one manifest chunk independently")
    parser.add_argument("--write-chunk-receipt", type=Path, metavar="PATH",
                        help="write repository evidence for one independent exact replay")
    parser.add_argument("--aggregate-receipts", nargs="+", type=Path, metavar="PATH",
                        help="combine one validated exact-replay receipt per manifest chunk")
    parser.add_argument("--write-aggregate", type=Path, metavar="PATH")
    args = parser.parse_args()
    if args.build_manifest is not None:
        require(not args.digest_only and args.chunk_index is None and
                args.write_chunk_receipt is None and args.aggregate_receipts is None and
                args.write_aggregate is None,
                "manifest build mode cannot be combined with replay or receipt modes")
        payload = build_manifest(args.manifest, args.build_manifest)
        print(f"manifest_sha256={sha256(canonical_bytes(payload))} "
              f"covered_residual_range=0..{payload['covered_residual_range'][1]}")
        return
    if args.aggregate_receipts is not None:
        require(args.write_aggregate is not None,
                "--aggregate-receipts requires --write-aggregate")
        require(args.chunk_index is None and args.write_chunk_receipt is None and
                not args.digest_only,
                "aggregate mode cannot be combined with replay modes")
        require(args.write_aggregate.parent.is_dir(), "aggregate output parent does not exist")
        payload = build_receipt_aggregate(
            args.manifest, args.aggregate_receipts, args.write_aggregate)
        args.write_aggregate.write_bytes(canonical_bytes(payload))
        sys.stdout.write(canonical_bytes(payload).decode("ascii"))
        return
    require(args.write_aggregate is None, "--write-aggregate requires --aggregate-receipts")
    require((args.chunk_index is None) == (args.write_chunk_receipt is None),
            "--chunk-index and --write-chunk-receipt must be used together")
    require(not (args.digest_only and args.write_chunk_receipt is not None),
            "--digest-only cannot write an exact replay receipt")
    report, complete = audit(args.manifest, not args.digest_only, args.chunk_index)
    if args.write_chunk_receipt is not None:
        require(complete, "cannot receipt an incomplete chunk replay")
        require(args.write_chunk_receipt.parent.is_dir(),
                "chunk receipt output parent does not exist")
        payload = chunk_receipt_payload(args.manifest, args.chunk_index, report)
        args.write_chunk_receipt.write_bytes(canonical_bytes(payload))
    sys.stdout.write(canonical_bytes(report).decode("ascii"))
    if not complete:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except (IndexError, KeyError, OSError, OverflowError, TypeError, ValueError,
            ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
