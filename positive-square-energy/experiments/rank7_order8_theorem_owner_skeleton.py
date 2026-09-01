#!/usr/bin/env python3
"""Assemble the global order-eight theorem-owner ledger and exact remainder."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_LEDGER = HERE / "rank7_order8_theorem_eligible_combined_ledger.json"
BASE_REMAINDER = HERE / "rank7_order8_after_packet_spectral_remainder.jsonl.xz"
PACKET_REPORT = HERE / "rank7_order8_induced_packet_gram_family.json"
PACKET_OWNERS = HERE / "rank7_order8_induced_packet_gram_family_owners.jsonl.xz"
ENGINE_PATH = HERE / "rank7_order8_exact_rational.py"
CACHE_PATH = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
SKELETON_PATH = HERE / "rank7_order8_theorem_owner_skeleton.json"
LEDGER_PATH = HERE / "rank7_order8_global_theorem_eligible_ledger.json"
REMAINDER_PATH = HERE / "rank7_order8_global_theorem_remainder.jsonl.xz"
STRUCTURAL_LANES = (
    ("structural-cycle-gram", "rank7_order8_structural_cycle_gram_lane.json",
     "rank7_order8_structural_cycle_gram_owners.jsonl.xz", 112),
    ("next-structural-cycle-gram", "rank7_order8_next_structural_cycle_gram_lane.json",
     "rank7_order8_next_structural_cycle_gram_owners.jsonl.xz", 97),
    ("third-structural-cycle-gram", "rank7_order8_third_structural_cycle_gram_lane.json",
     "rank7_order8_third_structural_cycle_gram_owners.jsonl.xz", 36),
)
SCHEMA = "rank-seven-order-eight-global-theorem-ledger-v1"
SKELETON_SCHEMA = "rank-seven-order-eight-theorem-owner-skeleton-v1"
BASE_REMAINDER_TOTAL = 83856
PACKET_TOTAL = 2928
DOWNSTREAM_TOTAL = 3173
FINAL_REMAINDER_TOTAL = 80683
TARGETS_PER_ROW = 15


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


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def read_json(path):
    raw = path.read_bytes()
    payload = strict_json(raw, path.name)
    return payload, hashlib.sha256(raw).hexdigest()


def read_jsonl(path):
    records = []
    digest = hashlib.sha256()
    with lzma.open(path, "rb") as stream:
        for raw in stream:
            record = strict_json(raw, path.name)
            require(raw == canonical_bytes(record), f"noncanonical record in {path.name}")
            records.append((record, raw))
            digest.update(raw)
    return records, digest.hexdigest(), file_sha256(path)


def write_json(path, payload):
    raw = canonical_bytes(payload)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(raw)
    temporary.replace(path)
    return hashlib.sha256(raw).hexdigest()


def write_remainder(records):
    digest = hashlib.sha256()
    temporary = REMAINDER_PATH.with_name(REMAINDER_PATH.name + ".tmp")
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as stream:
        for _, raw in records:
            stream.write(raw)
            digest.update(raw)
    temporary.replace(REMAINDER_PATH)
    return {
        "path": REMAINDER_PATH.name,
        "record_total": len(records),
        "raw_sha256": digest.hexdigest(),
        "artifact_sha256": file_sha256(REMAINDER_PATH),
    }


def verify_existing_remainder(records, expected):
    actual, raw_sha256, artifact_sha256 = read_jsonl(REMAINDER_PATH)
    require([raw for _, raw in actual] == [raw for _, raw in records],
            "global remainder is not the exact owner complement")
    observed = {"path": REMAINDER_PATH.name, "record_total": len(actual),
                "raw_sha256": raw_sha256, "artifact_sha256": artifact_sha256}
    require(observed == expected, "global remainder aggregate changed")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_packet_replay(records):
    engine = load_module("rank7_order8_global_engine", ENGINE_PATH)
    packet = load_module("rank7_order8_packet_family", HERE /
                         "rank7_order8_induced_packet_gram_family.py")
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=CACHE_PATH)
    for owner, _ in records:
        index = owner["stream_index"]
        source = residuals[index]
        require((owner["source_index"], owner["global_kernel"]) ==
                (source[1], source[0]), "packet owner escaped the authenticated stream")
        engine.base.verify_shared(census, source,
                                  packet.source.decode_witness(owner["witness"])
                                  if hasattr(packet.source, "decode_witness") else
                                  decode_packet_witness(owner["witness"]))


def decode_packet_witness(payload):
    from fractions import Fraction

    denominator = payload["denominator"]

    def rows(values):
        return tuple(tuple(Fraction(value, denominator) for value in row)
                     for row in values)

    return (denominator, rows(payload["branches"]),
            tuple(rows(path) for path in payload["canonical"]),
            tuple(rows(path) for path in payload["extended"]))


def lane_artifact(name, report_name, owner_name, expected_total):
    report_path = HERE / report_name
    owner_path = HERE / owner_name
    report, report_sha256 = read_json(report_path)
    owners, raw_sha256, artifact_sha256 = read_jsonl(owner_path)
    require(report["owned_orbit_total"] == expected_total and
            report["owner_stream"] == {
                "path": owner_name, "record_total": expected_total,
                "raw_sha256": raw_sha256, "artifact_sha256": artifact_sha256,
            }, f"{name} owner stream changed")
    lift = report.get("theorem_lift", {})
    require(all(key in lift for key in ("all_length", "rooted_trees")),
            f"{name} lacks all-length/tree lift evidence")
    indices = [owner[0][0] for owner, _ in owners]
    require(len(indices) == len(set(indices)) == expected_total,
            f"{name} owner indices are not unique")
    return indices, {
        "lane": name,
        "owner_total": expected_total,
        "report": {"path": report_name, "raw_sha256": report_sha256},
        "owner_stream": {"path": owner_name, "record_total": expected_total,
                         "raw_sha256": raw_sha256,
                         "artifact_sha256": artifact_sha256},
        "lift_audit": {
            "all_length": "authenticated exact Gram acceptance and fixed-parity path-cost monotonicity",
            "rooted_trees": "DNN one-vertex additivity",
            "status": "theorem-eligible",
        },
    }


def build(audit=False, replay_packet=True):
    base, base_sha256 = read_json(BASE_LEDGER)
    base_rows, base_raw, base_xz = read_jsonl(BASE_REMAINDER)
    require(base["remaining_residual_total"] == BASE_REMAINDER_TOTAL and
            base["exact_remainder_stream"] == {
                "path": BASE_REMAINDER.name, "record_total": BASE_REMAINDER_TOTAL,
                "raw_sha256": base_raw, "artifact_sha256": base_xz,
            }, "base theorem remainder changed")
    base_indices = [record[0] for record, _ in base_rows]
    require(len(base_indices) == len(set(base_indices)) == BASE_REMAINDER_TOTAL,
            "base remainder indices are not unique")
    base_set = set(base_indices)

    lanes = []
    downstream_sets = []
    for lane in STRUCTURAL_LANES:
        indices, artifact = lane_artifact(*lane)
        downstream_sets.append(set(indices))
        lanes.append(artifact)

    packet_report, packet_report_sha256 = read_json(PACKET_REPORT)
    packet_records, packet_raw, packet_xz = read_jsonl(PACKET_OWNERS)
    packet_indices = [owner["stream_index"] for owner, _ in packet_records]
    require(packet_report["full_theorem"] is True and
            packet_report["owned_orbit_total"] == PACKET_TOTAL and
            packet_report["remaining_target_family_total"] == 0 and
            packet_report["owner_stream"] == {
                "path": PACKET_OWNERS.name, "record_total": PACKET_TOTAL,
                "raw_sha256": packet_raw, "artifact_sha256": packet_xz,
            } and len(packet_indices) == len(set(packet_indices)) == PACKET_TOTAL,
            "standalone induced-packet closure changed")
    if replay_packet:
        exact_packet_replay(packet_records)
    packet_set = set(packet_indices)
    downstream_sets.append(packet_set)
    lanes.append({
        "lane": "induced-packet-shared-rational-gram",
        "owner_total": PACKET_TOTAL,
        "report": {"path": PACKET_REPORT.name, "raw_sha256": packet_report_sha256},
        "owner_stream": {"path": PACKET_OWNERS.name, "record_total": PACKET_TOTAL,
                         "raw_sha256": packet_raw, "artifact_sha256": packet_xz},
        "lift_audit": {
            "canonical_and_frontiers": "all 2928 witnesses replay exactly on the canonical target and fourteen coordinate frontiers",
            "all_length": "the retained branch Gram has nonnegative path terms decreasing under L -> L+2",
            "rooted_trees": "DNN one-vertex additivity assigns arbitrary rooted-tree attachments their tree Gram",
            "status": "theorem-eligible",
        },
    })

    union = set()
    intersections = {}
    for lane, indices in zip(lanes, downstream_sets, strict=True):
        name = lane["lane"]
        intersections[name] = len(union & indices)
        require(not union & indices, f"owner lane overlap at {name}")
        require(indices <= base_set, f"owner lane escaped base theorem remainder: {name}")
        union.update(indices)
    require(len(union) == DOWNSTREAM_TOTAL, "downstream owner union changed")
    final_rows = [(record, raw) for record, raw in base_rows if record[0] not in union]
    require(len(final_rows) == FINAL_REMAINDER_TOTAL,
            "global remainder arithmetic failed")

    owner_digest = hashlib.sha256()
    for index in sorted(union):
        owner_digest.update(canonical_bytes(index))
    skeleton = {
        "schema": SKELETON_SCHEMA,
        "scope": "theorem-owner lanes applied after the 83856-row boundary closure",
        "base_remainder_total": BASE_REMAINDER_TOTAL,
        "lanes": lanes,
        "exclusive_owner_total": DOWNSTREAM_TOTAL,
        "exclusive_owner_index_sha256": owner_digest.hexdigest(),
        "disjointness_audit": {
            "all_owner_indices_lie_in_base_remainder": True,
            "precedence_intersection_counts": intersections,
            "pairwise_disjoint": True,
        },
        "lift_audit": {
            "canonical_plus_coordinate_frontiers": "authenticated exact replay",
            "all_length": "fixed-parity path terms are nonnegative and weakly decrease with length",
            "rooted_trees": "DNN one-vertex additivity",
            "status": "all listed owners are theorem-eligible",
        },
        "remaining_residual_total": FINAL_REMAINDER_TOTAL,
    }
    if audit:
        actual_skeleton, _ = read_json(SKELETON_PATH)
        require(actual_skeleton == skeleton, "theorem-owner skeleton changed")
        actual_ledger, _ = read_json(LEDGER_PATH)
        remainder_artifact = actual_ledger["exact_remainder_stream"]
        verify_existing_remainder(final_rows, remainder_artifact)
    else:
        write_json(SKELETON_PATH, skeleton)
        remainder_artifact = write_remainder(final_rows)

    counts = dict(base["exclusive_owner_row_counts"])
    for lane in lanes:
        counts[lane["lane"]] = lane["owner_total"]
    owned = sum(counts.values())
    require(owned == 412734 and owned + FINAL_REMAINDER_TOTAL ==
            base["coarse_residual_total"], "global ledger partition failed")
    ledger = {
        "schema": SCHEMA,
        "full_theorem": False,
        "accounting_status": "global-theorem-eligible-exact-owner-union",
        "scope": base["scope"],
        "source_stream_sha256": base["source_stream_sha256"],
        "coarse_residual_total": base["coarse_residual_total"],
        "targets_per_residual": TARGETS_PER_ROW,
        "base_ledger": {"path": BASE_LEDGER.name, "raw_sha256": base_sha256,
                        "owned_residual_total": base["combined_owned_residual_total"],
                        "remaining_residual_total": BASE_REMAINDER_TOTAL},
        "theorem_owner_skeleton": {"path": SKELETON_PATH.name,
                                   "raw_sha256": hashlib.sha256(
                                       canonical_bytes(skeleton)).hexdigest()},
        "owner_precedence": [*base["owner_precedence"],
                             *(lane["lane"] for lane in lanes)],
        "exclusive_owner_row_counts": counts,
        "exclusive_owner_target_counts": {key: value * TARGETS_PER_ROW
                                           for key, value in counts.items()},
        "combined_owned_residual_total": owned,
        "combined_owned_target_total": owned * TARGETS_PER_ROW,
        "remaining_residual_total": FINAL_REMAINDER_TOTAL,
        "remaining_target_total": FINAL_REMAINDER_TOTAL * TARGETS_PER_ROW,
        "partition_identity": f"{base['coarse_residual_total']} = {owned} + {FINAL_REMAINDER_TOTAL}",
        "new_closure": {
            "standalone_induced_packet_owner_total": PACKET_TOTAL,
            "prior_structural_owner_total": DOWNSTREAM_TOTAL - PACKET_TOTAL,
            "new_global_owner_total": DOWNSTREAM_TOTAL,
            "input_remainder_total": BASE_REMAINDER_TOTAL,
            "exact_new_remainder_total": FINAL_REMAINDER_TOTAL,
        },
        "exact_remainder_stream": remainder_artifact,
        "theorem_contract": skeleton["lift_audit"],
        "claim_boundary": "the listed exact owners and their all-length/rooted-tree lifts are owned; the exact 80683-row complement remains open",
    }
    if audit:
        actual_ledger, _ = read_json(LEDGER_PATH)
        require(actual_ledger == ledger, "global theorem ledger changed")
    else:
        write_json(LEDGER_PATH, ledger)
    return ledger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--skip-packet-replay", action="store_true")
    args = parser.parse_args()
    ledger = build(args.audit, not args.skip_packet_replay)
    print(json.dumps({"owned": ledger["combined_owned_residual_total"],
                      "new_closure": ledger["new_closure"]["standalone_induced_packet_owner_total"],
                      "remaining": ledger["remaining_residual_total"],
                      "ledger_sha256": hashlib.sha256(canonical_bytes(ledger)).hexdigest()},
                     sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            ZeroDivisionError, lzma.LZMAError) as error:
        raise SystemExit(f"rank-seven order-eight theorem-owner skeleton: FAIL CLOSED: {error}")
