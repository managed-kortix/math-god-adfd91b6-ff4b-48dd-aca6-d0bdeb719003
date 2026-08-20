#!/usr/bin/env python3
"""Replace the 296 finite packet/spectral owners by exact all-length DNN owners."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "rank7_order8_exact_rational.py"
BASE_LEDGER_PATH = HERE / "rank7_order8_combined_owner_ledger.json"
TYPED_ACCOUNTING_PATH = HERE / "rank7_order8_combined_owner_accounting.json"
INDICES_PATH = HERE / "rank7_order8_combined_owner_indices.json.xz"
FINITE_OWNERS_PATH = HERE / "rank7_order8_packet_spectral_owners.json.xz"
REMAINDER_PATH = HERE / "rank7_order8_after_packet_spectral_remainder.jsonl.xz"
CACHE_PATH = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
OWNER_PATH = HERE / "rank7_order8_theorem_dnn_owners.json.xz"
LEDGER_PATH = HERE / "rank7_order8_theorem_eligible_combined_ledger.json"
OWNER_SCHEMA = "rank-seven-order-eight-theorem-dnn-owners-v1"
LEDGER_SCHEMA = "rank-seven-order-eight-theorem-eligible-combined-ledger-v1"
EXPECTED_INPUT_REMAINDER = 84152
EXPECTED_RESCUE = 296
EXPECTED_REMAINDER = 83856
TARGETS_PER_ROW = 15
DENOMINATORS = (256, 1024, 4096, 16384, 65536)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def strict_json(raw, label):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(
                              RuntimeError(f"nonstandard constant in {label}: {value}")))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {label}") from error


def read_canonical(path, compressed=False):
    stored = path.read_bytes()
    try:
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ) if compressed else stored
    except lzma.LZMAError as error:
        raise RuntimeError(f"cannot decompress {path.name}") from error
    payload = strict_json(raw, path.name)
    require(raw == canonical_bytes(payload), f"noncanonical artifact: {path.name}")
    return payload, hashlib.sha256(raw).hexdigest(), hashlib.sha256(stored).hexdigest()


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def write_canonical(path, payload, compressed=False):
    raw = canonical_bytes(payload)
    stored = lzma.compress(raw, format=lzma.FORMAT_XZ, preset=6) if compressed else raw
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(stored)
    temporary.replace(path)
    return {"path": path.name, "raw_sha256": hashlib.sha256(raw).hexdigest(),
            "artifact_sha256": hashlib.sha256(stored).hexdigest(), "bytes": len(stored)}


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order8_boundary_engine", ENGINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load order-eight engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def integer_rows(rows, denominator):
    result = []
    for row in rows:
        values = []
        for value in row:
            require(denominator % value.denominator == 0, "non-shared parameter denominator")
            values.append(value.numerator * (denominator // value.denominator))
        result.append(values)
    return result


def encode_witness(witness):
    denominator, branches, canonical, extended = witness
    return {
        "denominator": denominator,
        "branches": integer_rows(branches, denominator),
        "canonical": [integer_rows(path, denominator) for path in canonical],
        "extended": [integer_rows(path, denominator) for path in extended],
    }


def decode_witness(payload):
    denominator = payload["denominator"]
    require(type(denominator) is int and denominator in DENOMINATORS,
            "unexpected witness denominator")

    def rows(values):
        return tuple(tuple(Fraction(value, denominator) for value in row) for row in values)

    return (denominator, rows(payload["branches"]),
            tuple(rows(path) for path in payload["canonical"]),
            tuple(rows(path) for path in payload["extended"]))


def authenticated_scope():
    base, base_raw, _ = read_canonical(BASE_LEDGER_PATH)
    typed, typed_raw, _ = read_canonical(TYPED_ACCOUNTING_PATH)
    indices, indices_raw, indices_xz = read_canonical(INDICES_PATH, True)
    finite, finite_raw, finite_xz = read_canonical(FINITE_OWNERS_PATH, True)
    require(base.get("remaining_residual_total") == EXPECTED_INPUT_REMAINDER,
            "base remainder changed")
    require(base.get("combined_indices") == {
        "path": INDICES_PATH.name, "raw_sha256": indices_raw, "xz_sha256": indices_xz,
    }, "base ledger/index link changed")
    require(typed.get("combined_owned_residual_total") == 403317 and
            typed.get("remaining_residual_total") == 90100,
            "typed theorem replay accounting changed")
    owners = finite.get("owners")
    require(finite.get("schema") == "rank-seven-order-eight-packet-spectral-owners-v2" and
            isinstance(owners, list) and len(owners) == EXPECTED_RESCUE,
            "finite owner scope changed")
    rescue = [item["stream_index"] for item in owners]
    require(rescue == sorted(set(rescue)), "finite owner indices are not canonical")
    remaining = indices["exclusive_stream_indices"]["remaining"]
    require(len(remaining) == EXPECTED_INPUT_REMAINDER and set(rescue) <= set(remaining),
            "finite owners escaped the authenticated remainder")
    return base, indices, owners, rescue, {
        "base_combined_ledger": {"path": BASE_LEDGER_PATH.name, "raw_sha256": base_raw},
        "typed_segmented_accounting": {"path": TYPED_ACCOUNTING_PATH.name,
                                        "raw_sha256": typed_raw},
        "combined_owner_indices": {"path": INDICES_PATH.name, "raw_sha256": indices_raw,
                                     "artifact_sha256": indices_xz},
        "finite_owner_classification": {"path": FINITE_OWNERS_PATH.name,
                                         "raw_sha256": finite_raw,
                                         "artifact_sha256": finite_xz},
    }


def verify_remainder(expected_stream_indices):
    digest = hashlib.sha256()
    seen = []
    try:
        with lzma.open(REMAINDER_PATH, "rb") as stream:
            for raw in stream:
                record = strict_json(raw, REMAINDER_PATH.name)
                require(raw == canonical_bytes(record) and isinstance(record, list) and
                        len(record) == 6, "malformed updated remainder record")
                seen.append(record[0])
                digest.update(raw)
    except lzma.LZMAError as error:
        raise RuntimeError("cannot decompress updated remainder") from error
    require(seen == expected_stream_indices and len(seen) == EXPECTED_REMAINDER,
            "updated remainder is not the exact rescued complement")
    return {"path": REMAINDER_PATH.name, "record_total": len(seen),
            "raw_sha256": digest.hexdigest(), "artifact_sha256": file_sha256(REMAINDER_PATH)}


def make_owner_payload(engine, census, residuals, finite_owners, progress):
    class Arguments:
        symbolic_fast_lane = False
        seed = 1729
        restarts = 2
        iterations = 300
        fallback_restarts = 2
        fallback_iterations = 420

    records = []
    for position, finite in enumerate(finite_owners, 1):
        index = finite["stream_index"]
        source = residuals[index]
        record, _, shared, _ = engine.base.search_record(
            Arguments, census, source, index, DENOMINATORS)
        require(record[0] == engine.base.MODE_SHARED and shared is not None,
                f"no shared rational DNN witness for stream index {index}")
        engine.base.verify_shared(census, source, shared)
        records.append({
            "stream_index": index,
            "source_index": source[1],
            "global_kernel": source[0],
            "displaced_finite_lane": finite["lane"],
            "witness": encode_witness(shared),
        })
        if progress and position % 25 == 0:
            print(f"rescued={position}/{EXPECTED_RESCUE}", flush=True)
    return {
        "schema": OWNER_SCHEMA,
        "source_stream_sha256": census.SOURCE_SHA256,
        "owner_method": "shared exact rational correlation Gram",
        "theorem_contract": {
            "canonical": "the exact path-chain cost is at most six",
            "coordinate_frontiers": "the same branch Gram has exact cost at most six after each one-path length-plus-two move",
            "all_length_lift": "start from a dominated canonical or coordinate frontier and retain its branch Gram; fixed-parity path cost is nonincreasing",
            "rooted_tree_lift": "one-vertex DNN additivity assigns every rooted-tree edge its tree Gram",
        },
        "owner_total": len(records),
        "target_total": len(records) * TARGETS_PER_ROW,
        "owners": records,
    }


def verify_owner_payload(engine, census, residuals, payload, rescue):
    require(payload.get("schema") == OWNER_SCHEMA and
            payload.get("source_stream_sha256") == census.SOURCE_SHA256 and
            payload.get("owner_total") == EXPECTED_RESCUE and
            payload.get("target_total") == EXPECTED_RESCUE * TARGETS_PER_ROW,
            "wrong DNN owner artifact scope")
    records = payload.get("owners")
    require(isinstance(records, list) and
            [record.get("stream_index") for record in records] == rescue,
            "DNN owner index set changed")
    for record in records:
        index = record["stream_index"]
        source = residuals[index]
        require((record["source_index"], record["global_kernel"]) == (source[1], source[0]) and
                record["displaced_finite_lane"] in
                ("induced-packet", "direct-spectral-rayleigh"),
                "DNN owner identity changed")
        engine.base.verify_shared(census, source, decode_witness(record["witness"]))


def ledger_payload(base, inputs, owner_artifact, remainder_artifact):
    prior = base["exclusive_owner_row_counts"]
    counts = {key: prior[key] for key in base["owner_precedence"]}
    counts["shared-rational-gram-rescue"] = EXPECTED_RESCUE
    owned = sum(counts.values())
    require(owned + EXPECTED_REMAINDER == base["coarse_residual_total"],
            "theorem ledger partition arithmetic failed")
    return {
        "schema": LEDGER_SCHEMA,
        "full_theorem": False,
        "accounting_status": "theorem-eligible-exact-owner-union",
        "scope": "rank-seven order-eight canonical-plus-coordinate reduction",
        "source_stream_sha256": base["source_stream_sha256"],
        "coarse_residual_total": base["coarse_residual_total"],
        "targets_per_residual": TARGETS_PER_ROW,
        "owner_precedence": [*base["owner_precedence"], "shared-rational-gram-rescue"],
        "exclusive_owner_row_counts": counts,
        "exclusive_owner_target_counts": {key: value * TARGETS_PER_ROW
                                           for key, value in counts.items()},
        "combined_owned_residual_total": owned,
        "combined_owned_target_total": owned * TARGETS_PER_ROW,
        "remaining_residual_total": EXPECTED_REMAINDER,
        "remaining_target_total": EXPECTED_REMAINDER * TARGETS_PER_ROW,
        "partition_identity": (f"{base['coarse_residual_total']} = " +
                               " + ".join(str(counts[key]) for key in
                                          [*base["owner_precedence"],
                                           "shared-rational-gram-rescue"]) +
                               f" + {EXPECTED_REMAINDER}"),
        "boundary_closure": {
            "input_theorem_eligible_remainder": EXPECTED_INPUT_REMAINDER,
            "finite_packet_spectral_candidate_remainder": EXPECTED_REMAINDER,
            "rescued_owner_total": EXPECTED_RESCUE,
            "result": "all finite packet/spectral owners are replaced by exact shared-Gram DNN frontier owners",
        },
        "authenticated_inputs": inputs,
        "rescue_owner_artifact": owner_artifact,
        "exact_remainder_stream": remainder_artifact,
        "theorem_contract": {
            "existing_lanes": "payload-free, direct-rational, scalar SOS, and typed-diagonal certificates have exact theorem replay evidence",
            "rescue_lane": "every stored shared rational Gram is replayed on the canonical target and all fourteen coordinate frontiers",
            "subdivision": "canonical-plus-coordinate reduction and fixed-parity path monotonicity give every same-parity realization",
            "rooted_trees": "DNN one-vertex additivity gives arbitrary rooted-tree attachments",
        },
    }


def run(audit, progress):
    base, indices, finite_owners, rescue, inputs = authenticated_scope()
    expected_remainder = sorted(set(indices["exclusive_stream_indices"]["remaining"]) - set(rescue))
    remainder_artifact = verify_remainder(expected_remainder)
    engine = load_engine()
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=CACHE_PATH)
    if audit:
        owners, owner_raw, owner_xz = read_canonical(OWNER_PATH, True)
        verify_owner_payload(engine, census, residuals, owners, rescue)
        owner_artifact = {"path": OWNER_PATH.name, "raw_sha256": owner_raw,
                          "artifact_sha256": owner_xz, "bytes": OWNER_PATH.stat().st_size}
        expected_ledger = ledger_payload(base, inputs, owner_artifact, remainder_artifact)
        actual, _, _ = read_canonical(LEDGER_PATH)
        require(actual == expected_ledger, "theorem-eligible ledger differs from exact audit")
        return expected_ledger
    owners = make_owner_payload(engine, census, residuals, finite_owners, progress)
    verify_owner_payload(engine, census, residuals, owners, rescue)
    owner_artifact = write_canonical(OWNER_PATH, owners, True)
    ledger = ledger_payload(base, inputs, owner_artifact, remainder_artifact)
    write_canonical(LEDGER_PATH, ledger)
    return ledger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    report = run(args.audit, args.progress)
    print(json.dumps({
        "owned": report["combined_owned_residual_total"],
        "rescued": report["boundary_closure"]["rescued_owner_total"],
        "remaining": report["remaining_residual_total"],
        "ledger_sha256": hashlib.sha256(canonical_bytes(report)).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, RuntimeError, TypeError, ValueError, ZeroDivisionError) as error:
        raise SystemExit(f"rank-seven order-eight theorem boundary closure: FAIL CLOSED: {error}")
