#!/usr/bin/env python3
"""Fail-closed manifest and segmented exact auditor for R7G1 search packs."""

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
STREAM_PATH = HERE / "rank7_order7_exact_rational.py"
CENSUS_PATH = HERE / "rank7_order7_residual_census.json.xz"
CENSUS_ENGINE_PATH = HERE / "rank7_order7_residual_census.py"
RECOGNIZER_PATH = HERE / "rank7_order7_symbolic_atom_recognizer.py"
RATIONAL_BASE_PATH = HERE / "rank6_order10_cubic_exact_rational.py"
COARSE_ENGINE_PATH = HERE / "rank7_parity_coarse_digest_census.py"
KERNEL_SOURCE_PATH = ROOT / "research" / "fixtures" / "rank-seven-kernel-frontier-census.json"
DEFAULT_MANIFEST = HERE / "rank7_order7_search_manifest.json"
SCHEMA = "rank-seven-order-seven-r7g1-search-pack-manifest-v1"
CHUNK_TRANSCRIPT_SCHEMA = "rank-seven-order-seven-exact-chunk-replay-v1"
AGGREGATE_SCHEMA = "rank-seven-order-seven-segmented-replay-index-v1"
RESIDUAL_TOTAL = 40964
FRONTIER_TOTAL = 14
MODE_FIELDS = {"shared", "template", "fallback", "unresolved", "structural", "atom",
               "balanced"}
DIRECT_SPECTRAL_KEYS = frozenset({(28385, None), (28385, 10)})


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def load_canonical(path, label):
    raw = path.read_bytes()
    payload = strict_json(raw, label)
    require(raw == canonical_bytes(payload), f"{label} is not canonical JSON")
    return payload, raw


def digest_string(value, label):
    require(type(value) is str and len(value) == 64 and
            all(character in "0123456789abcdef" for character in value), f"bad {label}")


def exact_nonnegative_int(value, label):
    require(type(value) is int and value >= 0, f"bad {label}")


def dependency_digests():
    return {name: sha256(path.read_bytes()) for name, path in {
        "census": CENSUS_PATH,
        "census_engine": CENSUS_ENGINE_PATH,
        "coarse_engine": COARSE_ENGINE_PATH,
        "kernel_source": KERNEL_SOURCE_PATH,
        "rational_base": RATIONAL_BASE_PATH,
        "symbolic_recognizer": RECOGNIZER_PATH,
        "witness_stream": STREAM_PATH,
    }.items()}


def auditor_sha256():
    return sha256(Path(__file__).resolve().read_bytes())


def manifest_sha256(manifest):
    return sha256(canonical_bytes(manifest))


def target_frontier(target):
    require(type(target) is int and 0 <= target < FRONTIER_TOTAL, "bad target index")
    return None if target == 0 else target - 1


def load_scope(name):
    stream = load_module(name, STREAM_PATH)
    census = stream.load_census_module()
    residuals = stream.residual_rows(census)
    require(stream.MAGIC == b"R7G1" and stream.ORDER == 7 and stream.PATH_COUNT == 13 and
            len(residuals) == RESIDUAL_TOTAL, "R7G1 stream scope changed")
    return stream, census, residuals


def symbolic_owner_dictionary(stream, census, residuals):
    """Regenerate all 20 symbolic rows and their exact, non-full target sets."""
    recognizer = load_module("rank7_order7_atoms_for_pack_audit", RECOGNIZER_PATH)
    dictionary = []
    exact_keys = set()
    for source_index, source in enumerate(residuals):
        records = recognizer.recognize(stream.source_edges(census, source), source[4])
        owners = [record for record in records if record["status"] == "exact-equality-owner"]
        if not owners:
            continue
        frontiers = {frontier for record in owners for frontier in record["equality_frontiers"]}
        targets = sorted(0 if frontier is None else frontier + 1 for frontier in frontiers)
        require(targets and len(targets) < FRONTIER_TOTAL, "symbolic owner target width changed")
        require(all(0 <= target < FRONTIER_TOTAL for target in targets),
                "symbolic owner target exceeds R7G1 frontier")
        entry = {
            "source_index": source_index,
            "global_kernel": source[0],
            "order_kernel": stream.census_payload()["residuals"][source_index]["order_kernel"],
            "row": list(source[4]),
            "targets": targets,
            "frontiers": [target_frontier(target) for target in targets],
            "geometries": sorted({record["geometry"] for record in owners}),
        }
        dictionary.append(entry)
        exact_keys.update((source_index, target_frontier(target)) for target in targets)
    require(len(dictionary) == 20 and len({entry["source_index"] for entry in dictionary}) == 20,
            "symbolic owner dictionary does not contain exactly 20 rows")
    require(sum(len(entry["targets"]) for entry in dictionary) == len(exact_keys),
            "symbolic owner target set overlaps itself")
    dictionary_raw = canonical_bytes(dictionary)
    key_raw = b"".join(canonical_bytes([source_index, frontier])
                       for source_index, frontier in sorted(
                           exact_keys, key=lambda key: (key[0], -1 if key[1] is None else key[1])))
    return tuple(dictionary), frozenset(exact_keys), sha256(dictionary_raw), sha256(key_raw)


def symbolic_target_records(keys):
    return [{"source_index": source_index, "frontier": frontier}
            for source_index, frontier in sorted(
                keys, key=lambda key: (key[0], -1 if key[1] is None else key[1]))]


def polynomial_add(left, right):
    width = max(len(left), len(right))
    return tuple((left[index] if index < len(left) else 0) +
                 (right[index] if index < len(right) else 0) for index in range(width))


def polynomial_multiply(left, right):
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return tuple(result)


def determinant_polynomial(matrix):
    """Return det(xI-A), low coefficient first, by exact permutation expansion."""
    import itertools

    width = len(matrix)
    total = (0,)
    for permutation in itertools.permutations(range(width)):
        inversions = sum(permutation[i] > permutation[j] for i in range(width)
                         for j in range(i + 1, width))
        term = (1 if inversions % 2 == 0 else -1,)
        for row, column in enumerate(permutation):
            entry = (-matrix[row][column], 1) if row == column else (-matrix[row][column],)
            term = polynomial_multiply(term, entry)
        total = polynomial_add(total, term)
    return total


def target_adjacency(stream, census, source, frontier):
    paths = stream.base.path_ledger(census, source, frontier)
    order = stream.ORDER + sum(length - 1 for _, _, _, _, length in paths)
    adjacency = [[0] * order for _ in range(order)]
    next_vertex = stream.ORDER
    for _, _, u, v, length in paths:
        chain = [u, *range(next_vertex, next_vertex + length - 1), v]
        next_vertex += length - 1
        for left, right in zip(chain, chain[1:]):
            require(adjacency[left][right] == 0, "structural target is not simple")
            adjacency[left][right] = adjacency[right][left] = 1
    require(next_vertex == order, "structural target order changed")
    return adjacency


def direct_spectral_owner_dictionary(stream, census, residuals):
    """Verify the two non-DNN targets by exact characteristic-polynomial factors.

    These certificates concern the two finite target graphs only.  They do not
    assert the all-length/rooted-tree lift required by the single-block theorem.
    """
    source_index = 28385
    source = residuals[source_index]
    require(source[0] == 2763 and tuple(source[4]) == (1,) * 13,
            "K2763 direct-spectral source changed")
    specifications = {
        None: ((1, 2, 1), (-3, 0, 1), (-2, -7, -2, 1),
               "two-positive-factors: sqrt(3)^2=3 and cubic root >2"),
        10: ((1, 2, 1), (-1, -4, 0, 1), (10, 3, -8, -2, 1),
             "quartic root >3"),
    }
    dictionary = []
    for frontier, (linear, first, second, argument) in specifications.items():
        adjacency = target_adjacency(stream, census, source, frontier)
        expected = polynomial_multiply(polynomial_multiply(linear, first), second)
        require(determinant_polynomial(adjacency) == expected,
                "K2763 characteristic polynomial changed")
        if frontier is None:
            require(sum(coefficient * 2 ** power for power, coefficient in enumerate(first)) > 0
                    and sum(coefficient * 2 ** power for power, coefficient in enumerate(second)) < 0,
                    "K2763 canonical root signs changed")
        else:
            require(sum(coefficient * 3 ** power for power, coefficient in enumerate(second)) < 0,
                    "K2763 frontier root sign changed")
        dictionary.append({
            "source_index": source_index,
            "global_kernel": source[0],
            "order_kernel": stream.census_payload()["residuals"][source_index]["order_kernel"],
            "row": list(source[4]),
            "frontier": frontier,
            "target_order": len(adjacency),
            "characteristic_factors": [list(linear), list(first), list(second)],
            "argument": argument,
            "all_length_rooted_tree_lift": False,
        })
    require(frozenset((entry["source_index"], entry["frontier"])
                      for entry in dictionary) == DIRECT_SPECTRAL_KEYS,
            "direct-spectral target set changed")
    raw = canonical_bytes(dictionary)
    return tuple(dictionary), DIRECT_SPECTRAL_KEYS, sha256(raw)


def key_range_digest(residuals, start, stop):
    digest = hashlib.sha256()
    for source_index in range(start, stop):
        source = residuals[source_index]
        for target in range(FRONTIER_TOTAL):
            digest.update(canonical_bytes(
                [source_index, source[0], list(source[4]), target_frontier(target)]))
    return digest.hexdigest()


def load_manifest(path):
    payload, _ = load_canonical(path, "R7G1 manifest")
    require(type(payload) is dict and set(payload) == {
        "schema", "source_sha256", "dependency_sha256",
        "symbolic_owner_dictionary_sha256", "symbolic_exact_target_set_sha256",
        "symbolic_owners", "symbolic_exact_targets",
        "symbolic_owner_row_total", "symbolic_exact_target_total", "residual_total",
        "frontiers_per_residual", "chunks", "covered_residual_range",
        "covered_target_total", "covered_key_stream_sha256",
    }, "manifest fields changed")
    require(payload["schema"] == SCHEMA, "manifest schema changed")
    for field in ("source_sha256", "symbolic_owner_dictionary_sha256",
                  "symbolic_exact_target_set_sha256", "covered_key_stream_sha256"):
        digest_string(payload[field], f"manifest {field}")
    require(type(payload["dependency_sha256"]) is dict and
            set(payload["dependency_sha256"]) == set(dependency_digests()),
            "manifest dependency fields changed")
    for name, value in payload["dependency_sha256"].items():
        digest_string(value, f"dependency {name}")
    for field in ("symbolic_owner_row_total", "symbolic_exact_target_total", "residual_total",
                  "frontiers_per_residual", "covered_target_total"):
        exact_nonnegative_int(payload[field], f"manifest {field}")
    require(type(payload["chunks"]) is list and payload["chunks"], "manifest has no chunks")
    require(type(payload["symbolic_owners"]) is list and
            type(payload["symbolic_exact_targets"]) is list,
            "manifest symbolic owner materialization changed")
    return payload


def resolve_chunk_path(manifest_path, chunk, index):
    root = manifest_path.parent.resolve()
    path = (manifest_path.parent / chunk["path"]).resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise RuntimeError(f"chunk {index} escapes the manifest directory") from error
    require(path.is_file(), f"missing chunk {index}")
    return path


def validate_chunk_record(chunk, index, expected_start, residual_total):
    require(type(chunk) is dict and set(chunk) == {
        "path", "residual_range", "compressed_bytes", "compressed_sha256", "raw_bytes",
        "raw_sha256", "key_stream_sha256",
    }, f"bad chunk {index} manifest record")
    require(type(chunk["path"]) is str and chunk["path"], f"bad chunk {index} path")
    residual_range = chunk["residual_range"]
    require(type(residual_range) is list and len(residual_range) == 2,
            f"bad chunk {index} range")
    start, stop = residual_range
    require(type(start) is int and type(stop) is int and
            start == expected_start < stop <= residual_total,
            f"chunk {index} range is not the next ordered interval")
    for field in ("compressed_bytes", "raw_bytes"):
        exact_nonnegative_int(chunk[field], f"chunk {index} {field}")
    for field in ("compressed_sha256", "raw_sha256", "key_stream_sha256"):
        digest_string(chunk[field], f"chunk {index} {field}")
    return start, stop


def read_chunks(manifest_path, manifest, stream, census, residuals, chunk_index, consume):
    if chunk_index is not None:
        require(type(chunk_index) is int and 0 <= chunk_index < len(manifest["chunks"]),
                "chunk index is out of range")
    cursor = 0
    seen_paths = set()
    for index, chunk in enumerate(manifest["chunks"]):
        start, stop = validate_chunk_record(chunk, index, cursor, len(residuals))
        require(chunk["key_stream_sha256"] == key_range_digest(residuals, start, stop),
                f"chunk {index} target key stream changed")
        path = resolve_chunk_path(manifest_path, chunk, index)
        require(path not in seen_paths, f"chunk {index} repeats a pack path")
        seen_paths.add(path)
        cursor = stop
        if chunk_index is not None and index != chunk_index:
            continue
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
        actual_start, records = stream.base.decode_pack(census, raw, residuals)
        require(raw == stream.base.encode_pack(census, actual_start, records),
                f"chunk {index} has noncanonical R7G1 bytes")
        require(actual_start == start and len(records) == stop - start,
                f"chunk {index} embedded range changed")
        consume(start, records)
    return cursor


def numerical_targets(stream, mode, payload):
    if mode in (stream.base.MODE_SHARED, stream.base.MODE_TEMPLATE,
                stream.base.MODE_STRUCTURAL, stream.base.MODE_BALANCED):
        return set(range(FRONTIER_TOTAL))
    if mode == stream.base.MODE_FALLBACK:
        return {target for target, witness in enumerate(payload) if witness is not None}
    require(mode in (stream.base.MODE_UNRESOLVED, stream.base.MODE_ATOM),
            "unknown R7G1 record mode")
    return set()


def audit(manifest_path, exact=True, chunk_index=None):
    manifest = load_manifest(manifest_path)
    dependencies = dependency_digests()
    require(manifest["dependency_sha256"] == dependencies,
            "transitive dependency digest changed")
    stream, census, residuals = load_scope("rank7_order7_for_pack_audit")
    require(manifest["source_sha256"] == census.SOURCE_SHA256 and
            manifest["residual_total"] == len(residuals) == RESIDUAL_TOTAL and
            manifest["frontiers_per_residual"] == FRONTIER_TOTAL,
            "manifest census scope changed")
    dictionary, symbolic_keys, dictionary_sha256, target_set_sha256 = (
        symbolic_owner_dictionary(stream, census, residuals))
    structural_dictionary, structural_keys, structural_dictionary_sha256 = (
        direct_spectral_owner_dictionary(stream, census, residuals))
    require(symbolic_keys.isdisjoint(structural_keys), "symbolic owner lanes overlap")
    require(manifest["symbolic_owner_dictionary_sha256"] == dictionary_sha256 and
            manifest["symbolic_exact_target_set_sha256"] == target_set_sha256 and
            manifest["symbolic_owners"] == list(dictionary) and
            manifest["symbolic_exact_targets"] == symbolic_target_records(symbolic_keys) and
            manifest["symbolic_owner_row_total"] == len(dictionary) == 20 and
            manifest["symbolic_exact_target_total"] == len(symbolic_keys),
            "manifest symbolic owner dictionary changed")

    totals = {"rational": 0, "symbolic": 0, "structural": 0, "unresolved": 0,
              "symbolic_numerical": 0, "structural_numerical": 0}
    modes = {field: 0 for field in MODE_FIELDS}
    ownership = hashlib.sha256()

    def consume(start, records):
        labels = {
            stream.base.MODE_SHARED: "shared", stream.base.MODE_TEMPLATE: "template",
            stream.base.MODE_FALLBACK: "fallback", stream.base.MODE_UNRESOLVED: "unresolved",
            stream.base.MODE_STRUCTURAL: "structural", stream.base.MODE_ATOM: "atom",
            stream.base.MODE_BALANCED: "balanced",
        }
        for local, record in enumerate(records):
            source_index = start + local
            mode, payload = record
            require(mode in labels, "unknown decoded R7G1 mode")
            modes[labels[mode]] += 1
            if exact:
                stream.base.verify_record(census, residuals[source_index], record)
            rational = numerical_targets(stream, mode, payload)
            for target in range(FRONTIER_TOTAL):
                key = (source_index, target_frontier(target))
                if target in rational:
                    totals["rational"] += 1
                    if key in symbolic_keys:
                        totals["symbolic_numerical"] += 1
                    if key in structural_keys:
                        totals["structural_numerical"] += 1
                    owner = "rational"
                elif key in symbolic_keys:
                    totals["symbolic"] += 1
                    owner = "symbolic"
                elif key in structural_keys:
                    totals["structural"] += 1
                    owner = "structural"
                else:
                    totals["unresolved"] += 1
                    owner = "none"
                if exact:
                    ownership.update(canonical_bytes([source_index, key[1], owner]))

    manifest_covered = read_chunks(
        manifest_path, manifest, stream, census, residuals, chunk_index, consume)
    require(manifest["covered_residual_range"] == [0, manifest_covered] and
            manifest["covered_target_total"] == manifest_covered * FRONTIER_TOTAL and
            manifest["covered_key_stream_sha256"] == key_range_digest(
                residuals, 0, manifest_covered), "manifest coverage bookkeeping changed")
    if chunk_index is None:
        start, stop = 0, manifest_covered
        replay_scope = "full-manifest"
    else:
        start, stop = manifest["chunks"][chunk_index]["residual_range"]
        replay_scope = "single-chunk"
    covered_targets = (stop - start) * FRONTIER_TOTAL
    certified = (totals["rational"] + totals["symbolic"] + totals["structural"]
                 if exact else 0)
    scope_complete = exact and certified == covered_targets and totals["unresolved"] == 0
    complete = scope_complete and (chunk_index is not None or manifest_covered == len(residuals))
    report = {
        "status": "complete" if complete else "incomplete",
        "replay_scope": replay_scope,
        "finite_target_gate_eligible": bool(
            complete and chunk_index is None and stop == len(residuals)),
        "theorem_gate_eligible": False,
        "theorem_gate_blocker": "two direct-spectral owners lack all-length/rooted-tree lifts",
        "exact_audit": exact,
        "covered_residual_range": [start, stop],
        "manifest_covered_residual_range": [0, manifest_covered],
        "residual_total": len(residuals),
        "missing_residual_total": len(residuals) - manifest_covered,
        "covered_target_total": covered_targets,
        "manifest_covered_target_total": manifest_covered * FRONTIER_TOTAL,
        "missing_target_total": (len(residuals) - manifest_covered) * FRONTIER_TOTAL,
        "exact_certified_target_total": certified,
        "uncertified_target_total": covered_targets - certified,
        "disjoint_rational_owner_target_total": totals["rational"] if exact else 0,
        "disjoint_symbolic_owner_target_total": totals["symbolic"] if exact else 0,
        "disjoint_structural_owner_target_total": totals["structural"] if exact else 0,
        "symbolic_numerically_certified_target_total": (
            totals["symbolic_numerical"] if exact else 0),
        "symbolic_owner_row_total": len(dictionary),
        "symbolic_exact_target_total": len(symbolic_keys),
        "symbolic_owner_rows_in_coverage": sum(
            start <= entry["source_index"] < stop for entry in dictionary),
        "symbolic_exact_targets_in_coverage": sum(
            start <= key[0] < stop for key in symbolic_keys),
        "symbolic_owner_dictionary_sha256": dictionary_sha256,
        "symbolic_exact_target_set_sha256": target_set_sha256,
        "direct_spectral_owner_target_total": len(structural_keys),
        "direct_spectral_targets_in_coverage": sum(
            start <= key[0] < stop for key in structural_keys),
        "direct_spectral_numerically_certified_target_total": (
            totals["structural_numerical"] if exact else 0),
        "direct_spectral_owner_dictionary_sha256": structural_dictionary_sha256,
        "direct_spectral_owners": list(structural_dictionary),
        "covered_key_stream_sha256": key_range_digest(residuals, start, stop),
        "ownership_stream_sha256": ownership.hexdigest() if exact else None,
        "record_modes": modes,
    }
    return report, complete


def build_manifest(output, paths):
    require(output.parent.is_dir(), "manifest output parent does not exist")
    require(paths, "no R7G1 packs supplied")
    resolved = tuple(path.resolve() for path in paths)
    require(len(set(resolved)) == len(resolved), "duplicate pack path")
    stream, census, residuals = load_scope("rank7_order7_for_manifest")
    dictionary, symbolic_keys, dictionary_sha256, target_set_sha256 = (
        symbolic_owner_dictionary(stream, census, residuals))
    chunks = []
    for path in paths:
        stored = path.read_bytes()
        try:
            raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
        except lzma.LZMAError as error:
            raise RuntimeError(f"{path.name} is not a valid XZ stream") from error
        start, records = stream.base.decode_pack(census, raw, residuals)
        require(raw == stream.base.encode_pack(census, start, records),
                f"{path.name} is not canonical R7G1")
        chunks.append((start, start + len(records), path, stored, raw))
    chunks.sort(key=lambda item: item[0])
    records = []
    cursor = 0
    for index, (start, stop, path, stored, raw) in enumerate(chunks):
        require(start == cursor < stop, f"pack {index} leaves a gap or overlaps")
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
            "key_stream_sha256": key_range_digest(residuals, start, stop),
        })
        cursor = stop
    payload = {
        "schema": SCHEMA,
        "source_sha256": census.SOURCE_SHA256,
        "dependency_sha256": dependency_digests(),
        "symbolic_owner_dictionary_sha256": dictionary_sha256,
        "symbolic_exact_target_set_sha256": target_set_sha256,
        "symbolic_owners": list(dictionary),
        "symbolic_exact_targets": symbolic_target_records(symbolic_keys),
        "symbolic_owner_row_total": len(dictionary),
        "symbolic_exact_target_total": len(symbolic_keys),
        "residual_total": len(residuals),
        "frontiers_per_residual": FRONTIER_TOTAL,
        "chunks": records,
        "covered_residual_range": [0, cursor],
        "covered_target_total": cursor * FRONTIER_TOTAL,
        "covered_key_stream_sha256": key_range_digest(residuals, 0, cursor),
    }
    output.write_bytes(canonical_bytes(payload))
    return payload


def validate_chunk_report(report, manifest, chunk):
    start, stop = chunk["residual_range"]
    width = stop - start
    require(type(report) is dict and report.get("status") == "complete" and
            report.get("replay_scope") == "single-chunk" and
            report.get("theorem_gate_eligible") is False and
            report.get("finite_target_gate_eligible") is False and
            report.get("exact_audit") is True, "chunk transcript is not an exact replay")
    require(report.get("covered_residual_range") == [start, stop] and
            report.get("manifest_covered_residual_range") ==
            manifest["covered_residual_range"] and
            report.get("covered_target_total") == width * FRONTIER_TOTAL and
            report.get("exact_certified_target_total") == width * FRONTIER_TOTAL and
            report.get("uncertified_target_total") == 0,
            "chunk transcript coverage changed")
    require(report.get("disjoint_rational_owner_target_total") +
            report.get("disjoint_symbolic_owner_target_total") +
            report.get("disjoint_structural_owner_target_total") == width * FRONTIER_TOTAL,
            "chunk transcript ownership is not exact and disjoint")
    modes = report.get("record_modes")
    require(type(modes) is dict and set(modes) == MODE_FIELDS and
            all(type(value) is int and value >= 0 for value in modes.values()) and
            sum(modes.values()) == width, "chunk transcript mode totals changed")
    for field in ("covered_key_stream_sha256", "ownership_stream_sha256"):
        digest_string(report.get(field), f"chunk report {field}")


def chunk_transcript_payload(manifest_path, chunk_index, report):
    manifest = load_manifest(manifest_path)
    require(type(chunk_index) is int and 0 <= chunk_index < len(manifest["chunks"]),
            "chunk index is out of range")
    chunk = manifest["chunks"][chunk_index]
    validate_chunk_report(report, manifest, chunk)
    return {
        "schema": CHUNK_TRANSCRIPT_SCHEMA,
        "proof_semantics": "checkpoint_only_no_claim_without_aggregate_authentication",
        "full_theorem": False,
        "auditor_sha256": auditor_sha256(),
        "manifest_sha256": manifest_sha256(manifest),
        "dependency_sha256": manifest["dependency_sha256"],
        "chunk_index": chunk_index,
        "chunk": chunk,
        "report": report,
    }


def load_transcript(path):
    return load_canonical(path, "R7G1 exact chunk transcript")


def authenticate_chunk_transcript(manifest_path, transcript_path, manifest=None):
    manifest = load_manifest(manifest_path) if manifest is None else manifest
    transcript, raw = load_transcript(transcript_path)
    require(type(transcript) is dict and set(transcript) == {
        "schema", "proof_semantics", "full_theorem", "auditor_sha256", "manifest_sha256",
        "dependency_sha256", "chunk_index", "chunk", "report",
    }, "chunk transcript fields changed")
    require(transcript["schema"] == CHUNK_TRANSCRIPT_SCHEMA and
            transcript["proof_semantics"] ==
            "checkpoint_only_no_claim_without_aggregate_authentication" and
            transcript["full_theorem"] is False, "chunk transcript semantics changed")
    require(transcript["auditor_sha256"] == auditor_sha256() and
            transcript["manifest_sha256"] == manifest_sha256(manifest) and
            transcript["dependency_sha256"] == manifest["dependency_sha256"] ==
            dependency_digests(), "chunk transcript transitive identity changed")
    index = transcript["chunk_index"]
    require(type(index) is int and 0 <= index < len(manifest["chunks"]),
            "transcript chunk index is out of range")
    require(transcript["chunk"] == manifest["chunks"][index], "transcript chunk changed")
    validate_chunk_report(transcript["report"], manifest, transcript["chunk"])
    return raw, transcript


def build_aggregate(manifest_path, transcript_paths, aggregate_path):
    manifest = load_manifest(manifest_path)
    require(manifest["covered_residual_range"] == [0, manifest["residual_total"]],
            "segmented aggregate requires a full residual manifest")
    root = aggregate_path.parent.resolve()
    records = []
    seen = set()
    rational = symbolic = structural = targets = 0
    for path in transcript_paths:
        raw, transcript = authenticate_chunk_transcript(manifest_path, path, manifest)
        index = transcript["chunk_index"]
        require(index not in seen, f"duplicate chunk transcript: {index}")
        seen.add(index)
        try:
            relative = path.resolve().relative_to(root).as_posix()
        except ValueError as error:
            raise RuntimeError("chunk transcript is outside aggregate directory") from error
        report = transcript["report"]
        targets += report["covered_target_total"]
        rational += report["disjoint_rational_owner_target_total"]
        symbolic += report["disjoint_symbolic_owner_target_total"]
        structural += report["disjoint_structural_owner_target_total"]
        records.append({"chunk_index": index, "path": relative, "transcript_sha256": sha256(raw)})
    require(seen == set(range(len(manifest["chunks"]))),
            "aggregate requires one transcript for every manifest chunk")
    records.sort(key=lambda record: record["chunk_index"])
    require(targets == rational + symbolic + structural == manifest["covered_target_total"],
            "aggregate exact ownership bookkeeping changed")
    return {
        "schema": AGGREGATE_SCHEMA,
        "status": "segmented-replay-complete",
        "proof_semantics": "authenticated_exact_replay_index_no_standalone_theorem_claim",
        "full_theorem": False,
        "auditor_sha256": auditor_sha256(),
        "manifest_sha256": manifest_sha256(manifest),
        "dependency_sha256": manifest["dependency_sha256"],
        "covered_residual_range": manifest["covered_residual_range"],
        "covered_target_total": targets,
        "disjoint_rational_owner_target_total": rational,
        "disjoint_symbolic_owner_target_total": symbolic,
        "disjoint_structural_owner_target_total": structural,
        "chunks": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--build-manifest", nargs="+", type=Path, metavar="PACK")
    parser.add_argument("--digest-only", action="store_true")
    parser.add_argument("--chunk-index", type=int)
    parser.add_argument("--write-chunk-transcript", type=Path, metavar="PATH")
    parser.add_argument("--aggregate-transcripts", nargs="+", type=Path, metavar="PATH")
    parser.add_argument("--write-aggregate", type=Path, metavar="PATH")
    parser.add_argument("--print-symbolic-dictionary", action="store_true")
    args = parser.parse_args()
    if args.print_symbolic_dictionary:
        stream, census, residuals = load_scope("rank7_order7_for_dictionary")
        dictionary, keys, dictionary_digest, key_digest = symbolic_owner_dictionary(
            stream, census, residuals)
        sys.stdout.write(canonical_bytes({
            "rows": dictionary, "row_total": len(dictionary), "exact_target_total": len(keys),
            "dictionary_sha256": dictionary_digest, "exact_target_set_sha256": key_digest,
            "full_theorem": False,
        }).decode("ascii"))
        return
    if args.build_manifest is not None:
        payload = build_manifest(args.manifest, args.build_manifest)
        print(f"manifest_sha256={manifest_sha256(payload)} "
              f"covered_residual_range=0..{payload['covered_residual_range'][1]}")
        return
    if args.aggregate_transcripts is not None:
        require(args.write_aggregate is not None and args.write_aggregate.parent.is_dir(),
                "aggregate mode requires an output in an existing directory")
        payload = build_aggregate(
            args.manifest, args.aggregate_transcripts, args.write_aggregate)
        args.write_aggregate.write_bytes(canonical_bytes(payload))
        sys.stdout.write(canonical_bytes(payload).decode("ascii"))
        return
    require(args.write_aggregate is None, "--write-aggregate requires --aggregate-transcripts")
    require((args.chunk_index is None) == (args.write_chunk_transcript is None),
            "--chunk-index and --write-chunk-transcript must be used together")
    require(not (args.digest_only and args.write_chunk_transcript is not None),
            "digest-only mode cannot write an exact replay transcript")
    report, complete = audit(args.manifest, not args.digest_only, args.chunk_index)
    if args.write_chunk_transcript is not None:
        require(complete and args.write_chunk_transcript.parent.is_dir(),
                "cannot write transcript for an incomplete replay")
        args.write_chunk_transcript.write_bytes(canonical_bytes(
            chunk_transcript_payload(args.manifest, args.chunk_index, report)))
    sys.stdout.write(canonical_bytes(report).decode("ascii"))
    if not complete:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except (IndexError, KeyError, OSError, OverflowError, TypeError, ValueError,
            ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
