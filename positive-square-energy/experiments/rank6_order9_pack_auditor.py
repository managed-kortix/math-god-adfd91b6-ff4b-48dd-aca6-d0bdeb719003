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
FRONTIER_TOTAL = 15
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


def read_chunks(manifest_path, manifest, pipeline, residuals):
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
        try:
            raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
        except lzma.LZMAError as error:
            raise RuntimeError(f"chunk {index} is not a valid XZ stream") from error
        require(len(raw) == chunk["raw_bytes"] and sha256(raw) == chunk["raw_sha256"],
                f"chunk {index} raw stream changed")
        actual_start, attempts, records = pipeline.decode_search(raw, residuals)
        require(actual_start == start and attempts == stop - start and
                len(records) == attempts, f"chunk {index} embedded range changed")
        decoded.append((start, records))
        expected_start = stop
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


def audit(manifest_path, exact=True):
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
    covered, decoded = read_chunks(manifest_path, manifest, pipeline, residuals)
    require(manifest["covered_residual_range"] == [0, covered] and
            manifest["covered_target_total"] == covered * FRONTIER_TOTAL,
            "manifest coverage totals changed")
    require(manifest["covered_key_stream_sha256"] == key_digest(residuals, covered),
            "covered ordered target key stream digest changed")

    expected_symbolic = {key for key in symbolic_keys if key[0] < covered}
    if exact:
        numerical, unresolved, symbolic_exact, modes = exact_certificates(
            pipeline, residuals, decoded, symbolic_keys)
        symbolic_certified = unresolved & expected_symbolic
        certified = numerical | symbolic_certified
        require(expected_symbolic <= symbolic_exact | symbolic_certified,
                "symbolically owned target lacks an exact certificate")
    else:
        numerical = unresolved = symbolic_exact = symbolic_certified = certified = set()
        modes = {"shared": 0, "template": 0, "individual": 0, "unresolved": 0}
    complete = exact and covered == len(residuals) and len(certified) == covered * FRONTIER_TOTAL
    report = {
        "status": "complete" if complete else "incomplete",
        "census": {
            "kernel_interval": census_payload["kernel_interval"],
            "kernel_total": census_payload["kernel_total"],
            "physical_total": census_payload["physical_total"],
            "parity_orbit_total": census_payload["parity_orbit_total"],
            "coarse_certified_total": census_payload["coarse_certified_total"],
            "coarse_residual_total": census_payload["coarse_residual_total"],
            "frontier_target_total": census_payload["frontier_target_total"],
        },
        "covered_residual_range": [0, covered],
        "residual_total": len(residuals),
        "missing_residual_total": len(residuals) - covered,
        "covered_target_total": covered * FRONTIER_TOTAL,
        "missing_target_total": (len(residuals) - covered) * FRONTIER_TOTAL,
        "exact_certified_target_total": len(certified),
        "uncertified_target_total": covered * FRONTIER_TOTAL - len(certified),
        "unresolved_target_total": len(unresolved),
        "symbolic_owned_target_total": len(expected_symbolic),
        "symbolic_numerically_certified_target_total": len(symbolic_exact),
        "symbolic_only_certified_target_total": len(symbolic_certified),
        "disjoint_rational_owner_target_total": len(numerical),
        "disjoint_symbolic_owner_target_total": len(symbolic_certified),
        "symbolic_decomposition_total": symbolic_report["decomposition_total"],
        "symbolic_geometry_row_counts": symbolic_report["geometry_row_counts"],
        "record_modes": modes,
        "exact_audit": exact,
    }
    return report, complete


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
    args = parser.parse_args()
    if args.build_manifest is not None:
        require(not args.digest_only, "--digest-only cannot build a manifest")
        payload = build_manifest(args.manifest, args.build_manifest)
        print(f"manifest_sha256={sha256(canonical_bytes(payload))} "
              f"covered_residual_range=0..{payload['covered_residual_range'][1]}")
        return
    report, complete = audit(args.manifest, not args.digest_only)
    sys.stdout.write(canonical_bytes(report).decode("ascii"))
    if not complete:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except (IndexError, KeyError, OSError, OverflowError, TypeError, ValueError,
            ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
