#!/usr/bin/env python3
"""Fail-closed manifest and exact auditor for R10G1 search packs."""

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
STREAM_PATH = HERE / "rank6_order10_cubic_exact_rational.py"
CENSUS_PATH = HERE / "rank6_order10_cubic_frontier_census.py"
RECOGNIZER_PATH = HERE / "rank6_order10_equality_recognizer.py"
RECOGNIZER_FIXTURE_PATH = HERE / "rank6_order10_equality_recognizer.json"
LEDGER_PATH = HERE / "rank6_orders8_10_atom_ledger_search.py"
LEDGER_FIXTURE_PATH = HERE / "rank6_orders8_10_atom_ledger_classification.json"
KERNEL_PATH = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
DEFAULT_MANIFEST = HERE / "rank6_order10_search_manifest.json"
SCHEMA = "rank-six-order-ten-r10g-search-pack-manifest-v1"
FRONTIER_TOTAL = 16
PROFILES = ((1, (3, 4)), (2, (4,)), (5, ()))
EXPECTED_PROFILE_DECOMPOSITIONS = {(1, (3, 4)): 18, (2, (4,)): 152, (5, ()): 8}


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
    require(records == expected_records,
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
    digest = hashlib.sha256()
    for source_index, source in enumerate(residuals[:stop]):
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
    require(type(payload["dependency_sha256"]) is dict,
            "bad manifest dependency digest map")
    return payload


def read_chunks(manifest_path, manifest, stream, census, residuals):
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
        require(all(type(chunk[field]) is str and len(chunk[field]) == 64 and
                    all(character in "0123456789abcdef" for character in chunk[field])
                    for field in ("compressed_sha256", "raw_sha256")),
                f"bad chunk {index} digest")
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
        actual_start, records = stream.decode_pack(census, raw, residuals)
        require(actual_start == start and len(records) == stop - start,
                f"chunk {index} embedded range changed")
        decoded.append((start, records))
        expected_start = stop
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


def audit(manifest_path, exact=True):
    manifest = load_manifest(manifest_path)
    dependencies = dependency_digests()
    require(manifest["dependency_sha256"] == dependencies,
            "transitive dependency digest changed")
    census = load_module("rank6_order10_census_for_pack_audit", CENSUS_PATH)
    stream = load_module("rank6_order10_stream_for_pack_audit", STREAM_PATH)
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
    covered, decoded = read_chunks(manifest_path, manifest, stream, census, residuals)
    require(manifest["covered_residual_range"] == [0, covered] and
            manifest["covered_target_total"] == covered * FRONTIER_TOTAL,
            "manifest coverage totals changed")
    require(manifest["covered_key_stream_sha256"] == key_digest(residuals, covered),
            "covered ordered key stream digest changed")
    decoded_certificates, modes = certified_targets(stream, census, residuals, decoded, exact)
    certified = decoded_certificates if exact else set()
    expected_owned = {key for key in owners if key[0] < covered}
    missing_owned = expected_owned - certified if exact else set()
    require(not missing_owned, f"symbolic equality targets lack exact certificates: {len(missing_owned)}")
    profile_report = {}
    for profile in PROFILES:
        label = f"mixed-{profile[0]}_simplex-{'-'.join(map(str, profile[1])) or 'none'}"
        keys = {key for key, profiles in owners.items() if profile in profiles and key[0] < covered}
        profile_report[label] = {
            "decompositions": decomposition_counts[profile],
            "rows_in_coverage": len(owner_rows[profile] & set(range(covered))),
            "owned_targets_in_coverage": len(keys),
        }
    complete = exact and covered == len(residuals) and len(certified) == len(residuals) * FRONTIER_TOTAL
    return {
        "status": "complete" if complete else "incomplete",
        "covered_residual_range": [0, covered],
        "residual_total": len(residuals),
        "covered_target_total": covered * FRONTIER_TOTAL,
        "exact_certified_target_total": len(certified),
        "uncertified_target_total": (covered * FRONTIER_TOTAL - len(certified)
                                     if exact else covered * FRONTIER_TOTAL),
        "symbolic_owned_target_total": len(expected_owned),
        "symbolic_missing_exact_target_total": len(missing_owned),
        "symbolic_profiles": profile_report,
        "record_modes": modes,
        "exact_audit": exact,
    }, complete


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
    except (KeyError, OSError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
