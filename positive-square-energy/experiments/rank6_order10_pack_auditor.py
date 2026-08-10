#!/usr/bin/env python3
"""Fail-closed manifest and exact auditor for R10G1 search packs."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STREAM_PATH = HERE / "rank6_order10_cubic_exact_rational.py"
CENSUS_PATH = HERE / "rank6_order10_cubic_frontier_census.py"
RECOGNIZER_PATH = HERE / "rank6_order10_equality_recognizer.py"
RECOGNIZER_FIXTURE_PATH = HERE / "rank6_order10_equality_recognizer.json"
LEDGER_PATH = HERE / "rank6_orders8_10_atom_ledger_search.py"
LEDGER_FIXTURE_PATH = HERE / "rank6_orders8_10_atom_ledger_classification.json"
KERNEL_PATH = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
DEFAULT_MANIFEST = HERE / "rank6_order10_search_manifest.json"
SCHEMA = "rank-six-order-ten-r10g-search-pack-manifest-v1"
CHUNK_TRANSCRIPT_SCHEMA = "rank-six-order-ten-exact-chunk-audit-v1"
AGGREGATE_SCHEMA = "rank-six-order-ten-chunk-audit-aggregate-v1"
FRONTIER_TOTAL = 16
PROFILES = ((1, (3, 4)), (2, (4,)), (5, ()))
EXPECTED_PROFILE_DECOMPOSITIONS = {(1, (3, 4)): 18, (2, (4,)): 152, (5, ()): 8}
EXPECTED_LEDGER_SCOPE = {
    "orders": [8, 9, 10],
    "source": "canonical coarse residual parity-orbit representatives",
    "atoms": "regular simplexes K_m for 2<=m<=5 and mixed odd/even doubled pairs",
    "cost": 5,
    "overlaps": "physical occurrences disjoint; quotient supports may overlap",
    "contractions": "every unused odd singleton and every non-odd singleton is signed-contracted",
}
EXPECTED_LEDGER_COUNTS = {
    "8": [
        {"mixed": 1, "simplex_widths": [3, 4], "decompositions": 4},
        {"mixed": 2, "simplex_widths": [4], "decompositions": 185},
        {"mixed": 5, "simplex_widths": [], "decompositions": 12},
    ],
    "9": [
        {"mixed": 1, "simplex_widths": [3, 4], "decompositions": 16},
        {"mixed": 2, "simplex_widths": [4], "decompositions": 249},
        {"mixed": 5, "simplex_widths": [], "decompositions": 10},
    ],
    "10": [
        {"mixed": 1, "simplex_widths": [3, 4], "decompositions": 18},
        {"mixed": 2, "simplex_widths": [4], "decompositions": 152},
        {"mixed": 5, "simplex_widths": [], "decompositions": 8},
    ],
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def stream_line(payload):
    return canonical_bytes(payload)


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
        raise RuntimeError(f"{label} is not canonical ASCII JSON") from error


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dependency_digests():
    paths = {
        "census": CENSUS_PATH,
        "equality_recognizer": RECOGNIZER_PATH,
        "equality_recognizer_fixture": RECOGNIZER_FIXTURE_PATH,
        "kernel_source": KERNEL_PATH,
        "symbolic_ledger": LEDGER_PATH,
        "symbolic_ledger_fixture": LEDGER_FIXTURE_PATH,
        "witness_stream": STREAM_PATH,
    }
    return {name: sha256(path.read_bytes()) for name, path in paths.items()}


def exact_nonnegative_int(value, label):
    require(type(value) is int and value >= 0, f"bad {label}")


def load_canonical_fixture(path, label):
    raw = path.read_bytes()
    payload = strict_json(raw, label)
    require(raw == canonical_bytes(payload), f"{label} is not canonical JSON")
    return payload, raw


def profile_of(record):
    profile = record["profile"]
    require(type(profile) is dict and set(profile) == {"mixed", "simplex_widths"},
            "symbolic profile fields changed")
    exact_nonnegative_int(profile["mixed"], "symbolic mixed count")
    widths = profile["simplex_widths"]
    require(type(widths) is list and all(type(value) is int for value in widths),
            "bad symbolic simplex widths")
    return profile["mixed"], tuple(widths)


def symbolic_owners(stream, census, residuals):
    stream.PAIRS = census.PAIRS
    recognizer_payload, _ = load_canonical_fixture(
        RECOGNIZER_FIXTURE_PATH, "equality recognizer fixture")
    recognizer = load_module("rank6_order10_recognizer_for_pack_audit", RECOGNIZER_PATH)
    recognizer.verify(recognizer_payload)

    payload, raw = load_canonical_fixture(LEDGER_FIXTURE_PATH, "symbolic ledger fixture")
    require(type(payload) is dict and set(payload) ==
            {"schema", "scope", "counts", "decompositions"},
            "symbolic ledger top-level fields changed")
    require(payload["schema"] == "rank6-orders8-10-exact-atom-ledger-classification-v1",
            "symbolic ledger schema changed")
    require(canonical_bytes(payload["scope"]) == canonical_bytes(EXPECTED_LEDGER_SCOPE),
            "symbolic ledger scope changed")
    require(canonical_bytes(payload["counts"]) == canonical_bytes(EXPECTED_LEDGER_COUNTS),
            "symbolic ledger counts changed")
    require(type(payload["decompositions"]) is list, "bad symbolic decomposition list")
    ledger = load_module("rank6_order10_ledger_for_pack_audit", LEDGER_PATH)
    ledger.audit_atom_model()

    records = [record for record in payload["decompositions"]
               if type(record) is dict and record.get("order") == 10]
    require(len(records) == sum(EXPECTED_PROFILE_DECOMPOSITIONS.values()),
            "order-ten symbolic decomposition total changed")
    expected_records = []
    for source_index, source in enumerate(residuals):
        expected_records.extend(ledger.result_record(10, source_index, result)
                                for result in ledger.classify(stream, source))
    require(canonical_bytes(records) == canonical_bytes(expected_records),
            "symbolic ledger differs from exact regenerated order-ten classification")

    decomposition_counts = {profile: 0 for profile in PROFILES}
    owner_profiles = {}
    owner_rows = {profile: set() for profile in PROFILES}
    for record in records:
        require(set(record) == {"order", "source_index", "kernel", "row", "profile",
                                "mixed", "simplexes", "contractions", "classes", "signs",
                                "prescribed"}, "symbolic decomposition fields changed")
        profile = profile_of(record)
        require(profile in decomposition_counts, f"unknown symbolic equality profile: {profile}")
        decomposition_counts[profile] += 1
        source_index = record["source_index"]
        exact_nonnegative_int(source_index, "symbolic source index")
        require(source_index < len(residuals), "symbolic source index out of range")
        source = residuals[source_index]
        require(record["kernel"] == source[0] and record["row"] == list(source[4]),
                "symbolic source key changed")
        owner_rows[profile].add(source_index)
        keys = {(source_index, None)}
        contractions = {(tuple(edge), odd) for edge, odd in record["contractions"]}
        expected_contractions = 4 if profile == (1, (3, 4)) else 5
        require(len(contractions) == expected_contractions,
                "symbolic contraction count changed")
        for frontier, path in enumerate(stream.path_ledger(census, source)):
            _, _, u, v, length = path
            if ((u, v), bool(length & 1)) in contractions:
                keys.add((source_index, frontier))
        require(len(keys) == expected_contractions + 1,
                "symbolic equality frontier width changed")
        for key in keys:
            owner_profiles.setdefault(key, set()).add(profile)

    require(decomposition_counts == EXPECTED_PROFILE_DECOMPOSITIONS,
            "three-profile symbolic decomposition ledger changed")
    recognizer_owners = {
        (record["source_index"], target["frontier"])
        for record in recognizer_payload["records"] for target in record["targets"]
        if target["relation"] == "eq"
    }
    require(recognizer_owners <= set(owner_profiles),
            "recognizer equality ownership is absent from the symbolic ledger")
    for record in recognizer_payload["records"]:
        profile = ((5, ()) if record["geometry"] == "signed-five-cycle"
                   else (2, (4,)))
        for target in record["targets"]:
            if target["relation"] == "eq":
                require(profile in owner_profiles[(record["source_index"], target["frontier"])],
                        "recognizer equality profile ownership changed")
    require(set().union(*owner_profiles.values()) == set(PROFILES),
            "not all three symbolic equality profiles are represented")
    return owner_profiles, owner_rows, decomposition_counts, sha256(raw)


def target_frontier(target):
    return None if target == 0 else target - 1


def key_digest(residuals, stop):
    return key_range_digest(residuals, 0, stop)


def key_range_digest(residuals, start, stop):
    digest = hashlib.sha256()
    for source_index in range(start, stop):
        source = residuals[source_index]
        number, _, _, _, row, _, _, _ = source
        for target in range(FRONTIER_TOTAL):
            digest.update(stream_line(
                [source_index, number, list(row), target_frontier(target)]))
    return digest.hexdigest()


def load_manifest(path):
    payload, _ = load_canonical_fixture(path, "manifest")
    require(type(payload) is dict and set(payload) == {
        "schema", "source_sha256", "symbolic_sha256", "dependency_sha256",
        "residual_total", "frontiers_per_residual", "chunks",
        "covered_residual_range", "covered_target_total", "covered_key_stream_sha256",
    }, "manifest fields changed")
    require(payload["schema"] == SCHEMA, "manifest schema changed")
    for field in ("residual_total", "frontiers_per_residual", "covered_target_total"):
        exact_nonnegative_int(payload[field], f"manifest {field}")
    require(type(payload["covered_residual_range"]) is list and
            len(payload["covered_residual_range"]) == 2 and
            all(type(value) is int and value >= 0
                for value in payload["covered_residual_range"]),
            "bad manifest covered range")
    require(all(type(payload[field]) is str and len(payload[field]) == 64 and
                all(character in "0123456789abcdef" for character in payload[field])
                for field in ("source_sha256", "symbolic_sha256",
                              "covered_key_stream_sha256")),
            "bad manifest digest")
    require(type(payload["dependency_sha256"]) is dict and
            set(payload["dependency_sha256"]) == {
                "census", "equality_recognizer", "equality_recognizer_fixture",
                "kernel_source", "symbolic_ledger", "symbolic_ledger_fixture",
                "witness_stream",
            } and
            all(type(value) is str and len(value) == 64 and
                all(character in "0123456789abcdef" for character in value)
                for value in payload["dependency_sha256"].values()),
            "bad manifest dependency digest map")
    require(type(payload["chunks"]) is list, "bad manifest chunk list")
    return payload


def auditor_sha256():
    return sha256(Path(__file__).resolve().read_bytes())


def manifest_sha256(manifest):
    return sha256(canonical_bytes(manifest))


def resolve_chunk_path(manifest_path, chunk, index):
    root = manifest_path.parent.resolve()
    path = (manifest_path.parent / chunk["path"]).resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise RuntimeError(f"chunk {index} escapes the manifest directory") from error
    require(path.is_file(), f"missing chunk {index}")
    return path


def read_chunks(manifest_path, manifest, stream, census, residuals, chunk_index=None,
                consume=None):
    chunks = manifest["chunks"]
    require(type(chunks) is list and chunks, "manifest has no chunks")
    expected_start = 0
    decoded = []
    seen_paths = set()
    if chunk_index is not None:
        require(type(chunk_index) is int and 0 <= chunk_index < len(chunks),
                "chunk index is out of range")
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
        require(all(type(chunk[field]) is str and len(chunk[field]) == 64 and
                    all(character in "0123456789abcdef" for character in chunk[field])
                    for field in ("compressed_sha256", "raw_sha256")),
                f"bad chunk {index} digest")
        path = resolve_chunk_path(manifest_path, chunk, index)
        require(path not in seen_paths, f"chunk {index} repeats a pack path")
        seen_paths.add(path)
        expected_start = stop
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
        actual_start, records = stream.decode_pack(census, raw, residuals)
        require(actual_start == start and len(records) == stop - start,
                f"chunk {index} embedded range changed")
        if consume is None:
            decoded.append((start, records))
        else:
            consume(start, records)
            del records, raw, stored
    return expected_start, decoded


def certified_targets(stream, census, residuals, decoded, exact):
    certified = set()
    modes = {"shared": 0, "template": 0, "fallback": 0, "unresolved": 0}
    for start, records in decoded:
        for local, record in enumerate(records):
            source_index = start + local
            mode, payload = record
            if exact:
                stream.verify_record(census, residuals[source_index], record)
            if mode == stream.MODE_SHARED:
                modes["shared"] += 1
                targets = range(FRONTIER_TOTAL)
            elif mode == stream.MODE_TEMPLATE:
                modes["template"] += 1
                targets = range(FRONTIER_TOTAL)
            elif mode == stream.MODE_FALLBACK:
                modes["fallback"] += 1
                targets = (target for target, witness in enumerate(payload) if witness is not None)
            else:
                require(mode == stream.MODE_UNRESOLVED, "unknown decoded mode")
                modes["unresolved"] += 1
                targets = ()
            certified.update((source_index, target_frontier(target)) for target in targets)
    return certified, modes


def ownership_digest(start, stop, numerical, symbolic):
    require(numerical.isdisjoint(symbolic), "target ownership overlaps")
    digest = hashlib.sha256()
    for source_index in range(start, stop):
        for target in range(FRONTIER_TOTAL):
            key = (source_index, target_frontier(target))
            owner = "rational" if key in numerical else "symbolic" if key in symbolic else "none"
            digest.update(stream_line([source_index, key[1], owner]))
    return digest.hexdigest()


def accumulate_chunk(stream, census, residuals, start, records, owners, exact,
                     ownership_stream):
    counts = {
        "numerical": 0,
        "unresolved": 0,
        "symbolic_exact": 0,
        "symbolic_certified": 0,
    }
    modes = {"shared": 0, "template": 0, "fallback": 0, "unresolved": 0}
    symbolic_seen = set()
    for local, record in enumerate(records):
        source_index = start + local
        mode, payload = record
        if exact:
            stream.verify_record(census, residuals[source_index], record)
        if mode == stream.MODE_SHARED:
            modes["shared"] += 1
            numerical_targets = None
        elif mode == stream.MODE_TEMPLATE:
            modes["template"] += 1
            numerical_targets = None
        elif mode == stream.MODE_FALLBACK:
            modes["fallback"] += 1
            numerical_targets = {target for target, witness in enumerate(payload)
                                 if witness is not None}
        else:
            require(mode == stream.MODE_UNRESOLVED, "unknown decoded mode")
            modes["unresolved"] += 1
            numerical_targets = set()
        if not exact:
            continue
        for target in range(FRONTIER_TOTAL):
            key = (source_index, target_frontier(target))
            numerical = numerical_targets is None or target in numerical_targets
            symbolic = key in owners
            if symbolic:
                symbolic_seen.add(key)
            if numerical:
                counts["numerical"] += 1
                if symbolic:
                    counts["symbolic_exact"] += 1
                owner = "rational"
            else:
                counts["unresolved"] += 1
                require(symbolic, "unrecognized unresolved target")
                counts["symbolic_certified"] += 1
                owner = "symbolic"
            ownership_stream.update(stream_line([source_index, key[1], owner]))
    if exact:
        stop = start + len(records)
        expected_symbolic = {
            key for key in owners if start <= key[0] < stop
        }
        require(symbolic_seen == expected_symbolic,
                "symbolically owned target lacks an exact certificate")
        require(counts["numerical"] + counts["symbolic_certified"] ==
                len(records) * FRONTIER_TOTAL,
                "chunk exact ownership is incomplete")
    return counts, modes


def audit(manifest_path, exact=True, chunk_index=None):
    manifest = load_manifest(manifest_path)
    dependencies = dependency_digests()
    require(manifest["dependency_sha256"] == dependencies,
            "transitive dependency digest changed")
    census = load_module("rank6_order10_census_for_pack_audit", CENSUS_PATH)
    stream = load_module("rank6_order10_stream_for_pack_audit", STREAM_PATH)
    require(census.ORDER == 10 and census.RANK == 6 and census.PATH_COUNT == 15 and
            census.EXPECTED_TOTALS == (1508832, 497572, 372115, 125457,
                                       2007312, 8, 128),
            "order-ten census contract changed")
    require(stream.MAGIC == b"R10G1" and stream.ORDER == 10 and
            stream.PATH_COUNT == 15 and stream.BUDGET == 5,
            "witness stream configuration changed")
    require(manifest["source_sha256"] == census.SOURCE_SHA256 ==
            dependencies["kernel_source"], "kernel source ownership changed")
    residuals = stream.residual_rows(census)
    require(manifest["residual_total"] == len(residuals), "residual total changed")
    require(manifest["frontiers_per_residual"] == FRONTIER_TOTAL,
            "manifest frontier width changed")
    owners, owner_rows, decomposition_counts, symbolic_sha256 = symbolic_owners(
        stream, census, residuals)
    require(manifest["symbolic_sha256"] == symbolic_sha256,
            "manifest points to another symbolic ownership fixture")
    totals = {
        "numerical": 0,
        "unresolved": 0,
        "symbolic_exact": 0,
        "symbolic_certified": 0,
    }
    modes = {"shared": 0, "template": 0, "fallback": 0, "unresolved": 0}
    ownership_stream = hashlib.sha256()

    def consume(start, records):
        counts, chunk_modes = accumulate_chunk(
            stream, census, residuals, start, records, owners, exact, ownership_stream)
        for field, count in counts.items():
            totals[field] += count
        for mode, count in chunk_modes.items():
            modes[mode] += count

    manifest_covered, decoded = read_chunks(
        manifest_path, manifest, stream, census, residuals, chunk_index, consume)
    require(not decoded, "streaming chunk audit retained decoded records")
    require(manifest["covered_residual_range"] == [0, manifest_covered] and
            manifest["covered_target_total"] == manifest_covered * FRONTIER_TOTAL,
            "manifest coverage totals changed")
    require(manifest["covered_key_stream_sha256"] == key_digest(residuals, manifest_covered),
            "covered ordered key stream digest changed")
    if chunk_index is None:
        covered_start, covered_stop = 0, manifest_covered
    else:
        covered_start, covered_stop = manifest["chunks"][chunk_index]["residual_range"]
    expected_owned = {key for key in owners if covered_start <= key[0] < covered_stop}
    if exact:
        numerical_count = totals["numerical"]
        unresolved_count = totals["unresolved"]
        symbolic_exact_count = totals["symbolic_exact"]
        symbolic_certified_count = totals["symbolic_certified"]
        certified_count = numerical_count + symbolic_certified_count
        require(symbolic_exact_count + symbolic_certified_count == len(expected_owned),
                "symbolic ownership total changed")
    else:
        numerical_count = unresolved_count = symbolic_exact_count = 0
        symbolic_certified_count = certified_count = 0
    profile_report = {}
    for profile in PROFILES:
        label = f"mixed-{profile[0]}_simplex-{'-'.join(map(str, profile[1])) or 'none'}"
        keys = {key for key, profiles in owners.items() if profile in profiles and
                covered_start <= key[0] < covered_stop}
        profile_report[label] = {
            "decompositions": decomposition_counts[profile],
            "rows_in_coverage": sum(covered_start <= row < covered_stop
                                    for row in owner_rows[profile]),
            "owned_targets_in_coverage": len(keys),
        }
    covered_target_total = (covered_stop - covered_start) * FRONTIER_TOTAL
    scope_complete = exact and certified_count == covered_target_total
    complete = exact and scope_complete and (chunk_index is not None or
                                               covered_stop == len(residuals))
    ownership_sha256 = ownership_stream.hexdigest() if exact else None
    return {
        "status": "complete" if complete else "incomplete",
        "census": {
            "kernel_interval": [1133, 1198],
            "kernel_total": 66,
            "physical_total": 1508832,
            "parity_orbit_total": 497572,
            "coarse_certified_total": 372115,
            "coarse_residual_total": len(residuals),
            "frontier_target_total": len(residuals) * FRONTIER_TOTAL,
        },
        "covered_residual_range": [covered_start, covered_stop],
        "manifest_covered_residual_range": [0, manifest_covered],
        "residual_total": len(residuals),
        "missing_residual_total": len(residuals) - manifest_covered,
        "covered_target_total": covered_target_total,
        "manifest_covered_target_total": manifest_covered * FRONTIER_TOTAL,
        "missing_target_total": (len(residuals) - manifest_covered) * FRONTIER_TOTAL,
        "exact_certified_target_total": certified_count,
        "uncertified_target_total": covered_target_total - certified_count,
        "unresolved_target_total": unresolved_count,
        "symbolic_owned_target_total": len(expected_owned),
        "symbolic_numerically_certified_target_total": symbolic_exact_count,
        "symbolic_only_certified_target_total": symbolic_certified_count,
        "disjoint_rational_owner_target_total": numerical_count,
        "disjoint_symbolic_owner_target_total": symbolic_certified_count,
        "symbolic_decomposition_total": sum(decomposition_counts.values()),
        "symbolic_profiles": profile_report,
        "record_modes": modes,
        "covered_key_stream_sha256": key_range_digest(
            residuals, covered_start, covered_stop),
        "ownership_stream_sha256": ownership_sha256,
        "exact_audit": exact,
    }, complete


def chunk_transcript_payload(manifest_path, chunk_index, report):
    manifest = load_manifest(manifest_path)
    require(manifest["dependency_sha256"] == dependency_digests(),
            "transitive dependency digest changed")
    require(type(chunk_index) is int and 0 <= chunk_index < len(manifest["chunks"]),
            "chunk index is out of range")
    chunk = manifest["chunks"][chunk_index]
    start, stop = chunk["residual_range"]
    require(report.get("status") == "complete" and report.get("exact_audit") is True,
            "cannot checkpoint an incomplete chunk audit")
    require(report.get("covered_residual_range") == [start, stop] and
            report.get("covered_target_total") == (stop - start) * FRONTIER_TOTAL,
            "chunk report covers another interval")
    require(report.get("exact_certified_target_total") ==
            report.get("covered_target_total") and
            report.get("uncertified_target_total") == 0,
            "chunk report does not own every target")
    return {
        "schema": CHUNK_TRANSCRIPT_SCHEMA,
        "proof_semantics": "checkpoint_only_no_proof_without_exact_replay",
        "auditor_sha256": auditor_sha256(),
        "manifest_sha256": manifest_sha256(manifest),
        "dependency_sha256": manifest["dependency_sha256"],
        "manifest_covered_key_stream_sha256": manifest["covered_key_stream_sha256"],
        "chunk_index": chunk_index,
        "chunk_path": chunk["path"],
        "chunk_residual_range": chunk["residual_range"],
        "chunk_key_stream_sha256": report["covered_key_stream_sha256"],
        "chunk_compressed_sha256": chunk["compressed_sha256"],
        "chunk_raw_sha256": chunk["raw_sha256"],
        "ownership_stream_sha256": report["ownership_stream_sha256"],
        "report": report,
    }


def load_transcript(path):
    raw = path.read_bytes()
    payload = strict_json(raw, "chunk audit transcript")
    require(raw == canonical_bytes(payload), "chunk audit transcript is not canonical JSON")
    return raw, payload


def validate_chunk_report(report, manifest, chunk):
    require(type(report) is dict, "chunk report is not an object")
    start, stop = chunk["residual_range"]
    require(report.get("status") == "complete" and report.get("exact_audit") is True,
            "chunk checkpoint does not claim a complete exact replay")
    require(report.get("covered_residual_range") == [start, stop] and
            report.get("manifest_covered_residual_range") ==
            manifest["covered_residual_range"] and
            report.get("residual_total") == manifest["residual_total"] and
            report.get("covered_target_total") == (stop - start) * FRONTIER_TOTAL and
            report.get("manifest_covered_target_total") == manifest["covered_target_total"],
            "chunk checkpoint range binding changed")
    require(report.get("exact_certified_target_total") ==
            report.get("covered_target_total") and
            report.get("uncertified_target_total") == 0,
            "chunk checkpoint ownership is not exhaustive")
    require(report.get("disjoint_rational_owner_target_total") +
            report.get("disjoint_symbolic_owner_target_total") ==
            report.get("exact_certified_target_total"),
            "chunk checkpoint ownership is not disjoint")
    for field in ("covered_key_stream_sha256", "ownership_stream_sha256"):
        value = report.get(field)
        require(type(value) is str and len(value) == 64 and
                all(character in "0123456789abcdef" for character in value),
                f"bad chunk report {field}")


def authenticate_chunk_transcript(manifest_path, transcript_path, manifest=None):
    """Authenticate a checkpoint claim; this performs no exact witness replay."""
    if manifest is None:
        manifest = load_manifest(manifest_path)
    raw, transcript = load_transcript(transcript_path)
    require(type(transcript) is dict and set(transcript) == {
        "schema", "proof_semantics", "auditor_sha256", "manifest_sha256",
        "dependency_sha256", "manifest_covered_key_stream_sha256", "chunk_index",
        "chunk_path", "chunk_residual_range", "chunk_key_stream_sha256",
        "chunk_compressed_sha256", "chunk_raw_sha256", "ownership_stream_sha256",
        "report",
    }, "chunk transcript fields changed")
    require(transcript["schema"] == CHUNK_TRANSCRIPT_SCHEMA,
            "chunk transcript schema changed")
    require(transcript["proof_semantics"] ==
            "checkpoint_only_no_proof_without_exact_replay",
            "chunk transcript proof semantics changed")
    require(transcript["auditor_sha256"] == auditor_sha256(), "checkpoint auditor changed")
    require(transcript["manifest_sha256"] == manifest_sha256(manifest),
            "checkpoint manifest changed")
    require(transcript["dependency_sha256"] == manifest["dependency_sha256"] ==
            dependency_digests(), "checkpoint dependencies changed")
    require(transcript["manifest_covered_key_stream_sha256"] ==
            manifest["covered_key_stream_sha256"], "checkpoint manifest key stream changed")
    index = transcript["chunk_index"]
    require(type(index) is int and 0 <= index < len(manifest["chunks"]),
            "checkpoint chunk index is out of range")
    chunk = manifest["chunks"][index]
    require(transcript["chunk_path"] == chunk["path"] and
            transcript["chunk_residual_range"] == chunk["residual_range"] and
            transcript["chunk_compressed_sha256"] == chunk["compressed_sha256"] and
            transcript["chunk_raw_sha256"] == chunk["raw_sha256"],
            "checkpoint chunk path, range, or bytes changed")
    path = resolve_chunk_path(manifest_path, chunk, index)
    stored = path.read_bytes()
    require(len(stored) == chunk["compressed_bytes"] and
            sha256(stored) == chunk["compressed_sha256"],
            f"chunk {index} compressed artifact changed")
    report = transcript["report"]
    validate_chunk_report(report, manifest, chunk)
    require(transcript["chunk_key_stream_sha256"] == report["covered_key_stream_sha256"] and
            transcript["ownership_stream_sha256"] == report["ownership_stream_sha256"],
            "checkpoint key or ownership binding changed")
    return raw, transcript


def build_aggregate(manifest_path, transcript_paths):
    """Index authenticated checkpoints; aggregation itself performs no exact replay."""
    manifest = load_manifest(manifest_path)
    require(manifest["dependency_sha256"] == dependency_digests(),
            "transitive dependency digest changed")
    records = []
    reports = []
    seen = set()
    for path in transcript_paths:
        raw, transcript = authenticate_chunk_transcript(manifest_path, path, manifest)
        index = transcript["chunk_index"]
        require(index not in seen, f"duplicate chunk transcript: {index}")
        seen.add(index)
        records.append({
            "chunk_index": index,
            "path": transcript["chunk_path"],
            "residual_range": transcript["chunk_residual_range"],
            "key_stream_sha256": transcript["chunk_key_stream_sha256"],
            "ownership_stream_sha256": transcript["ownership_stream_sha256"],
            "transcript_sha256": sha256(raw),
        })
        reports.append(transcript["report"])
    require(seen == set(range(len(manifest["chunks"]))),
            "aggregate requires exactly one checkpoint for every manifest chunk")
    records.sort(key=lambda record: record["chunk_index"])
    require([record["residual_range"] for record in records] ==
            [chunk["residual_range"] for chunk in manifest["chunks"]],
            "aggregate chunk ranges changed")
    total_targets = sum(report["covered_target_total"] for report in reports)
    rational = sum(report["disjoint_rational_owner_target_total"] for report in reports)
    symbolic = sum(report["disjoint_symbolic_owner_target_total"] for report in reports)
    require(total_targets == manifest["covered_target_total"] == rational + symbolic,
            "aggregate ownership or target total changed")
    return {
        "schema": AGGREGATE_SCHEMA,
        "proof_semantics": "checkpoint_index_only_no_proof_without_exact_replay",
        "exact_proof": False,
        "auditor_sha256": auditor_sha256(),
        "manifest_sha256": manifest_sha256(manifest),
        "dependency_sha256": manifest["dependency_sha256"],
        "covered_residual_range": manifest["covered_residual_range"],
        "covered_target_total": total_targets,
        "manifest_covered_key_stream_sha256": manifest["covered_key_stream_sha256"],
        "disjoint_rational_owner_target_total": rational,
        "disjoint_symbolic_owner_target_total": symbolic,
        "chunks": records,
    }


def build_manifest(output, paths):
    require(output.parent.is_dir(), "manifest output parent does not exist")
    resolved = tuple(path.resolve() for path in paths)
    require(len(set(resolved)) == len(resolved), "duplicate pack path")
    census = load_module("rank6_order10_census_for_manifest", CENSUS_PATH)
    stream = load_module("rank6_order10_stream_for_manifest", STREAM_PATH)
    residuals = stream.residual_rows(census)
    _, _, _, symbolic_sha256 = symbolic_owners(stream, census, residuals)
    chunks = []
    for path in paths:
        stored = path.read_bytes()
        try:
            raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
        except lzma.LZMAError as error:
            raise RuntimeError(f"{path.name} is not a valid XZ stream") from error
        start, records = stream.decode_pack(census, raw, residuals)
        chunks.append((start, start + len(records), path, stored, raw))
    chunks.sort(key=lambda item: item[0])
    require(chunks, "no packs supplied")
    records = []
    expected_start = 0
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
        "source_sha256": census.SOURCE_SHA256,
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
                        help="check dependency, range, byte, key, and symbolic digests only")
    parser.add_argument("--build-manifest", nargs="+", type=Path, metavar="PACK")
    parser.add_argument("--chunk-index", type=int,
                        help="exactly replay one manifest chunk independently")
    parser.add_argument("--write-chunk-transcript", type=Path, metavar="PATH",
                        help="write a no-proof checkpoint for an exact chunk replay")
    parser.add_argument("--aggregate-transcripts", nargs="+", type=Path, metavar="PATH",
                        help="index one authenticated checkpoint per manifest chunk")
    parser.add_argument("--write-aggregate", type=Path, metavar="PATH")
    parser.add_argument("--emit", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.build_manifest is not None:
        require(not args.digest_only, "--digest-only cannot build a manifest")
        payload = build_manifest(args.manifest, args.build_manifest)
        print(f"manifest_sha256={sha256(canonical_bytes(payload))} "
              f"covered_residual_range=0..{payload['covered_residual_range'][1]}")
        return
    require(not (args.digest_only and args.write_chunk_transcript),
            "--digest-only cannot write an exact checkpoint")
    if args.aggregate_transcripts is not None:
        require(args.write_aggregate is not None,
                "--aggregate-transcripts requires --write-aggregate")
        require(args.chunk_index is None and args.write_chunk_transcript is None and
                not args.digest_only, "aggregate mode cannot be combined with replay modes")
        require(args.write_aggregate.parent.is_dir(), "aggregate output parent does not exist")
        payload = build_aggregate(args.manifest, args.aggregate_transcripts)
        args.write_aggregate.write_bytes(canonical_bytes(payload))
        sys.stdout.write(canonical_bytes(payload).decode("ascii"))
        return
    require((args.chunk_index is None) == (args.write_chunk_transcript is None),
            "--chunk-index and --write-chunk-transcript must be used together")
    require(args.write_aggregate is None, "--write-aggregate requires --aggregate-transcripts")
    report, complete = audit(args.manifest, not args.digest_only, args.chunk_index)
    if args.write_chunk_transcript is not None:
        require(complete, "cannot checkpoint an incomplete chunk audit")
        require(args.write_chunk_transcript.parent.is_dir(),
                "chunk transcript output parent does not exist")
        payload = chunk_transcript_payload(args.manifest, args.chunk_index, report)
        args.write_chunk_transcript.write_bytes(canonical_bytes(payload))
    output = canonical_bytes(report).decode("ascii")
    if sys.flags.optimize == 0 and not args.emit:
        command = [sys.executable, "-O", __file__, "--manifest", str(args.manifest), "--emit"]
        if args.digest_only:
            command.append("--digest-only")
        if args.chunk_index is not None:
            command.extend(("--chunk-index", str(args.chunk_index),
                            "--write-chunk-transcript", str(args.write_chunk_transcript)))
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        expected_returncode = 0 if complete else 1
        require(completed.returncode == expected_returncode and completed.stderr == "",
                "optimized audit failed")
        require(completed.stdout == output, "normal and optimized outputs differ")
    sys.stdout.write(output)
    if not complete:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
