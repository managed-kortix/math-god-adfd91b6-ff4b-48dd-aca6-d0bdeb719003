#!/usr/bin/env python3
"""Compute the exact precedence-aware order-eight lane union."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import lzma
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "rank7_order8_exact_rational.py"
SCALAR_PATH = HERE / "rank7_order8_parametric_gram_ansatz.py"
TYPED_PATH = HERE / "rank7_order8_typed_diagonal_gram_lane.py"
CACHE_PATH = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
OUTPUT_PATH = HERE / "rank7_order8_lane_union.json.xz"
LEDGER_PATH = HERE / "rank7_order8_combined_owner_ledger.json"
INDICES_PATH = HERE / "rank7_order8_combined_owner_indices.json.xz"
PAYLOAD_REPORT_PATH = HERE / "rank7_order8_payload_free_lane_coverage.json"
SCALAR_REPORT_PATH = HERE / "rank7_order8_parametric_gram_ansatz_coverage.json"
TYPED_REPORT_PATH = HERE / "rank7_order8_typed_diagonal_gram_coverage.json"
TYPED_RECEIPTS_PATH = HERE / "rank7_order8_typed_diagonal_receipts"
SCHEDULER_RESULTS_PATH = HERE / "rank7_order8_scheduler" / "results"
PAYLOAD_FREE_TOTAL = 605
COMMITTED_STOP = 29000
TARGETS_PER_ROW = 15
BASELINE_PACK_SHA256 = "2f3773dc99c930f9aeacff1e3566e037eb6d7d106d866e81a829c1b53797a2ee"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def scalar_owner(scalar, engine, census, source, candidates, values):
    costs = scalar.numerical_costs(engine, census, source, values)
    for position in np.argsort(costs):
        if costs[position] > 6.0 + 1e-10:
            break
        if scalar.exact_cost(engine, census, source, candidates[int(position)]) <= 6:
            return True
    return False


def intervals(indices):
    if not indices:
        return []
    output = []
    start = previous = indices[0]
    for value in indices[1:]:
        if value != previous + 1:
            output.append([start, previous + 1])
            start = value
        previous = value
    output.append([start, previous + 1])
    return output


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


def read_canonical(path):
    raw = path.read_bytes()
    payload = strict_json(raw, path.name)
    require(raw == canonical_bytes(payload), f"noncanonical artifact: {path.name}")
    return payload, hashlib.sha256(raw).hexdigest()


def verify_committed(engine, census, residuals):
    paths = sorted(HERE.glob("rank7_order8_chunk_*.r7o8g.xz"))
    covered = []
    artifacts = []
    cursor = 0
    for path in paths:
        stored = path.read_bytes()
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
        start, records = engine.base.exact_decode_pack(census, raw, residuals)
        if start >= COMMITTED_STOP:
            continue
        require(start == cursor and start + len(records) <= COMMITTED_STOP,
                "committed packs leave a gap, overlap, or exceed the requested range")
        require(all(mode == engine.base.MODE_SHARED for mode, _ in records),
                "committed range contains a non-shared record")
        xz_sha256 = hashlib.sha256(stored).hexdigest()
        if start == 0:
            require(start + len(records) == 5000 and xz_sha256 == BASELINE_PACK_SHA256,
                    "baseline pack is not the authenticated committed artifact")
            authentication = {"kind": "pinned-baseline-sha256"}
        else:
            manifest_path = SCHEDULER_RESULTS_PATH / f"shard-{start:06d}_{start + len(records):06d}.json"
            manifest = strict_json(manifest_path.read_bytes(), manifest_path.name)
            require(manifest.get("schema") == "rank-seven-order-eight-shard-result-v1" and
                    manifest.get("status") == "completed" and
                    manifest.get("exact_audit") is True and
                    manifest.get("range") == [start, start + len(records)] and
                    manifest.get("rows") == len(records) and
                    manifest.get("output") == path.name and
                    manifest.get("output_sha256") == xz_sha256,
                    f"scheduler result does not authenticate {path.name}")
            authentication = {"kind": "scheduler-result", "path": manifest_path.name,
                              "sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest()}
        covered.extend(range(start, start + len(records)))
        artifacts.append({"path": path.name, "row_range": [start, start + len(records)],
                           "raw_sha256": hashlib.sha256(raw).hexdigest(),
                           "xz_sha256": xz_sha256, "authentication": authentication})
        cursor += len(records)
    require(cursor == COMMITTED_STOP, f"committed packs do not cover [0,{COMMITTED_STOP})")
    return frozenset(covered), artifacts


def typed_receipt_status():
    paths = sorted(TYPED_RECEIPTS_PATH.glob("receipt-*.json")) if TYPED_RECEIPTS_PATH.is_dir() else []
    return {
        "status": "theorem-evidence" if paths else "candidate-exact-search-acceptance",
        "segmented_receipts_present": bool(paths),
        "segmented_receipt_count": len(paths),
        "theorem_evidence_count": None if paths else 0,
        "candidate_count_note": "typed ownership is candidate accounting until a gap-free full receipt partition is independently merged",
    }


def write_canonical(path, payload, compressed=False):
    raw = canonical_bytes(payload)
    stored = lzma.compress(raw, format=lzma.FORMAT_XZ, preset=6) if compressed else raw
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(stored)
    temporary.replace(path)
    return hashlib.sha256(raw).hexdigest(), hashlib.sha256(stored).hexdigest()


def read_canonical_xz(path, label):
    stored = path.read_bytes()
    try:
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
    except lzma.LZMAError as error:
        raise RuntimeError(f"cannot decompress {label}") from error
    payload = strict_json(raw, label)
    require(raw == canonical_bytes(payload), f"noncanonical {label}")
    return payload, hashlib.sha256(raw).hexdigest(), hashlib.sha256(stored).hexdigest()


def audit_outputs(engine, census, residuals, output_path, ledger_path, indices_path):
    report, report_raw, report_xz = read_canonical_xz(output_path, "union report")
    indices, indices_raw, indices_xz = read_canonical_xz(indices_path, "owner indices")
    ledger, ledger_digest = read_canonical(ledger_path)
    require(report.get("schema") == "rank-seven-order-eight-lane-union-v1" and
            indices.get("schema") == "rank-seven-order-eight-combined-owner-indices-v1" and
            ledger.get("schema") == "rank-seven-order-eight-combined-owner-ledger-v1",
            "wrong output schema")
    require(report.get("source_stream_sha256") == census.SOURCE_SHA256 ==
            indices.get("source_stream_sha256") == ledger.get("source_stream_sha256"),
            "output source stream changed")
    require(report.get("precedence") == indices.get("precedence") ==
            ledger.get("owner_precedence") ==
            ["payload-free", "direct-rational", "scalar-sos", "typed-diagonal"],
            "strict precedence changed")
    linked_indices = report.get("combined_indices", {})
    require(linked_indices == {"path": indices_path.name, "raw_sha256": indices_raw,
                               "xz_sha256": indices_xz}, "report/index link changed")
    require(ledger.get("combined_indices") == linked_indices and
            ledger.get("union_report") == {"path": output_path.name,
                                            "raw_sha256": report_raw,
                                            "xz_sha256": report_xz},
            "ledger artifact links changed")
    groups = indices.get("exclusive_stream_indices", {})
    require(set(groups) == {"direct-rational", "scalar-sos", "typed-diagonal", "remaining"},
            "exclusive index groups changed")
    sets = {}
    for name, values in groups.items():
        require(isinstance(values, list) and values == sorted(values) and
                len(values) == len(set(values)) and
                all(type(value) is int and 0 <= value < len(residuals) for value in values),
                f"malformed {name} indices")
        sets[name] = frozenset(values)
    require(sum(len(values) for values in sets.values()) == len(set().union(*sets.values())) ==
            len(residuals), "exclusive indices do not partition the rational-search stream")
    require(len(sets["direct-rational"]) == COMMITTED_STOP and
            sets["direct-rational"] == frozenset(range(COMMITTED_STOP)),
            "committed rational index range changed")
    require(groups["remaining"] == report.get("remaining_stream_indices") and
            report.get("remaining_count") == len(groups["remaining"]) and
            indices.get("remaining_source_indices") == report.get("remaining_source_indices") ==
            [residuals[index][1] for index in groups["remaining"]],
            "remaining index accounting changed")
    exclusive = ledger.get("exclusive_owner_row_counts", {})
    require(exclusive == report.get("precedence_exclusive_counts") and
            exclusive == {"payload-free": PAYLOAD_FREE_TOTAL,
                          "direct-rational": len(sets["direct-rational"]),
                          "scalar-sos": len(sets["scalar-sos"]),
                          "typed-diagonal": len(sets["typed-diagonal"])},
            "exclusive owner counts changed")
    owned = sum(exclusive.values())
    require(ledger.get("combined_owned_residual_total") == owned and
            ledger.get("remaining_residual_total") == len(sets["remaining"]) and
            owned + len(sets["remaining"]) == len(residuals) + PAYLOAD_FREE_TOTAL and
            ledger.get("remaining_target_total") == len(sets["remaining"]) * TARGETS_PER_ROW,
            "ledger partition arithmetic changed")
    rational_set, rational_artifacts = verify_committed(engine, census, residuals)
    require(rational_set == sets["direct-rational"] and
            rational_artifacts == report.get("direct_rational_artifacts") ==
            ledger.get("direct_rational_artifacts"), "committed artifact authentication changed")
    for name, path in (("payload-free-report", PAYLOAD_REPORT_PATH),
                       ("scalar-sos-report", SCALAR_REPORT_PATH),
                       ("typed-diagonal-report", TYPED_REPORT_PATH)):
        _, digest = read_canonical(path)
        require(ledger.get("authenticated_inputs", {}).get(name) == digest,
                f"authenticated input changed: {name}")
    typed_evidence = ledger.get("evidence_accounting", {}).get("typed-diagonal", {})
    require(typed_evidence.get("status") == "candidate-exact-search-acceptance" and
            typed_evidence.get("segmented_receipts_present") is False and
            ledger.get("accounting_status") == "candidate-union-not-typed-theorem-evidence",
            "typed candidate/theorem-evidence boundary changed")
    return {"ledger_sha256": ledger_digest, "remaining_count": len(sets["remaining"]),
            "remaining_target_count": len(sets["remaining"]) * TARGETS_PER_ROW}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--ledger", type=Path, default=LEDGER_PATH)
    parser.add_argument("--indices", type=Path, default=INDICES_PATH)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    require(args.workers > 0, "workers must be positive")

    engine = load("rank7_order8_union_engine", ENGINE_PATH)
    scalar = load("rank7_order8_union_scalar", SCALAR_PATH)
    typed = load("rank7_order8_union_typed", TYPED_PATH)
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=CACHE_PATH)
    if args.audit:
        result = audit_outputs(engine, census, residuals, args.output, args.ledger, args.indices)
        print(json.dumps(result, sort_keys=True, indent=2))
        return

    candidates = scalar.coefficients(32, 4)
    values = np.asarray([float(value) for value in candidates])
    ratios = typed.rationals(8, 4, include_zero=True)
    scales = (Fraction(1, 2), Fraction(2, 3), Fraction(1), Fraction(3, 2), Fraction(2))
    parameter_grid = tuple((float(scale), float(scale * ratio), scale, scale * ratio)
                           for scale in scales for ratio in ratios)
    typed._WORKER_CONTEXT = engine, census, residuals, ratios, parameter_grid, 3
    if args.workers == 1:
        results = map(typed.worker_search, range(len(residuals)))
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=args.workers)
        results = executor.map(typed.worker_search, range(len(residuals)), chunksize=64)

    scalar_indices = []
    typed_indices = []
    for index, (source, result) in enumerate(zip(residuals, results, strict=True)):
        if scalar_owner(scalar, engine, census, source, candidates, values):
            scalar_indices.append(index)
        cost = result[0]
        if cost is not None and cost <= 6:
            typed_indices.append(index)
        if args.progress and (index + 1) % 25000 == 0:
            print(f"rows={index + 1} scalar={len(scalar_indices)} typed={len(typed_indices)}",
                  flush=True)
    if executor is not None:
        executor.shutdown()

    scalar_set = frozenset(scalar_indices)
    typed_set = frozenset(typed_indices)
    rational_set, rational_artifacts = verify_committed(engine, census, residuals)
    universe = frozenset(range(len(residuals)))
    structural_union = scalar_set | typed_set
    full_union = structural_union | rational_set
    remaining = sorted(universe - full_union)
    structural_remaining = sorted(universe - structural_union)
    source_remaining = [residuals[index][1] for index in remaining]

    atoms = {
        "scalar_only": len(scalar_set - typed_set - rational_set),
        "typed_only": len(typed_set - scalar_set - rational_set),
        "rational_only": len(rational_set - scalar_set - typed_set),
        "scalar_typed_only": len((scalar_set & typed_set) - rational_set),
        "scalar_rational_only": len((scalar_set & rational_set) - typed_set),
        "typed_rational_only": len((typed_set & rational_set) - scalar_set),
        "scalar_typed_rational": len(scalar_set & typed_set & rational_set),
    }
    report = {
        "schema": "rank-seven-order-eight-lane-union-v1",
        "source_stream_sha256": census.SOURCE_SHA256,
        "precedence": ["payload-free", "direct-rational", "scalar-sos", "typed-diagonal"],
        "universe": {
            "coarse_residual_total": len(residuals) + PAYLOAD_FREE_TOTAL,
            "rational_search_total": len(residuals),
            "payload_free_total": PAYLOAD_FREE_TOTAL,
        },
        "raw_lane_counts": {
            "payload-free": PAYLOAD_FREE_TOTAL,
            "scalar-sos": len(scalar_set),
            "typed-diagonal": len(typed_set),
            "direct-rational": len(rational_set),
        },
        "pairwise_overlap_counts": {
            "payload-free+scalar-sos": 0,
            "payload-free+typed-diagonal": 0,
            "payload-free+direct-rational": 0,
            "scalar-sos+typed-diagonal": len(scalar_set & typed_set),
            "scalar-sos+direct-rational": len(scalar_set & rational_set),
            "typed-diagonal+direct-rational": len(typed_set & rational_set),
        },
        "venn_atoms_within_rational_search": atoms,
        "precedence_exclusive_counts": {
            "payload-free": PAYLOAD_FREE_TOTAL,
            "direct-rational": len(rational_set),
            "scalar-sos": len(scalar_set - rational_set),
            "typed-diagonal": len(typed_set - scalar_set - rational_set),
        },
        "structural_union_count": PAYLOAD_FREE_TOTAL + len(structural_union),
        "structural_residual_count": len(structural_remaining),
        "full_union_count": PAYLOAD_FREE_TOTAL + len(full_union),
        "remaining_count": len(remaining),
        "structural_residual_stream_indices": structural_remaining,
        "remaining_stream_indices": remaining,
        "remaining_stream_intervals": intervals(remaining),
        "remaining_source_indices": source_remaining,
        "remaining_stream_indices_sha256": hashlib.sha256(canonical_bytes(remaining)).hexdigest(),
        "remaining_source_indices_sha256": hashlib.sha256(canonical_bytes(source_remaining)).hexdigest(),
        "evidence_accounting": {
            "payload-free": {"status": "theorem-evidence", "rows": PAYLOAD_FREE_TOTAL},
            "direct-rational": {"status": "theorem-evidence", "rows": len(rational_set),
                                "committed_half_open_range": [0, COMMITTED_STOP]},
            "scalar-sos": {"status": "theorem-evidence", "rows": len(scalar_set)},
            "typed-diagonal": {**typed_receipt_status(), "candidate_rows": len(typed_set)},
        },
    }
    report["direct_rational_artifacts"] = rational_artifacts
    indices = {
        "schema": "rank-seven-order-eight-combined-owner-indices-v1",
        "source_stream_sha256": census.SOURCE_SHA256,
        "precedence": report["precedence"],
        "stream_index_scope": "authenticated 492812-row payload-free complement",
        "exclusive_stream_indices": {
            "direct-rational": sorted(rational_set),
            "scalar-sos": sorted(scalar_set - rational_set),
            "typed-diagonal": sorted(typed_set - scalar_set - rational_set),
            "remaining": remaining,
        },
        "remaining_source_indices": source_remaining,
    }
    indices_raw_sha256, indices_xz_sha256 = write_canonical(args.indices, indices, True)
    report["combined_indices"] = {"path": args.indices.name,
                                  "raw_sha256": indices_raw_sha256,
                                  "xz_sha256": indices_xz_sha256}
    raw_sha256, xz_sha256 = write_canonical(args.output, report, True)

    payload_report, payload_digest = read_canonical(PAYLOAD_REPORT_PATH)
    scalar_report, scalar_digest = read_canonical(SCALAR_REPORT_PATH)
    typed_report, typed_digest = read_canonical(TYPED_REPORT_PATH)
    require(payload_report["recognized_residual_total"] == PAYLOAD_FREE_TOTAL and
            scalar_report["covered_residual_total"] == len(scalar_set) and
            typed_report["covered_residual_total"] == len(typed_set),
            "recomputed lane count differs from authenticated report")
    exclusive = report["precedence_exclusive_counts"]
    owned = sum(exclusive.values())
    ledger = {
        "schema": "rank-seven-order-eight-combined-owner-ledger-v1",
        "full_theorem": False,
        "accounting_status": "candidate-union-not-typed-theorem-evidence",
        "source_stream_sha256": census.SOURCE_SHA256,
        "coarse_residual_total": len(residuals) + PAYLOAD_FREE_TOTAL,
        "targets_per_residual": TARGETS_PER_ROW,
        "owner_precedence": report["precedence"],
        "exclusive_owner_row_counts": exclusive,
        "exclusive_owner_target_counts": {key: value * TARGETS_PER_ROW
                                           for key, value in exclusive.items()},
        "combined_owned_residual_total": owned,
        "combined_owned_target_total": owned * TARGETS_PER_ROW,
        "remaining_residual_total": len(remaining),
        "remaining_target_total": len(remaining) * TARGETS_PER_ROW,
        "partition_identity": f"{len(residuals) + PAYLOAD_FREE_TOTAL} = " +
                              " + ".join(str(exclusive[key]) for key in report["precedence"]) +
                              f" + {len(remaining)}",
        "authenticated_inputs": {
            "payload-free-report": payload_digest,
            "scalar-sos-report": scalar_digest,
            "typed-diagonal-report": typed_digest,
        },
        "direct_rational_artifacts": rational_artifacts,
        "combined_indices": report["combined_indices"],
        "union_report": {"path": args.output.name, "raw_sha256": raw_sha256,
                         "xz_sha256": xz_sha256},
        "theorem_contract": {
            "direct-rational": "every pack is canonical and every exact witness is replayed",
            "structural": "scalar and typed formulas are recomputed with exact acceptance",
            "precedence": "payload-free, then direct rational, then scalar SOS, then typed diagonal",
            "partition": "exclusive indices and remainder partition the authenticated stream",
        },
        "evidence_accounting": report["evidence_accounting"],
    }
    ledger_sha256, _ = write_canonical(args.ledger, ledger)
    print(json.dumps({key: report[key] for key in (
        "raw_lane_counts", "pairwise_overlap_counts", "venn_atoms_within_rational_search",
        "precedence_exclusive_counts", "structural_union_count", "structural_residual_count",
        "full_union_count", "remaining_count")}, sort_keys=True, indent=2))
    print(f"raw_sha256={raw_sha256}")
    print(f"xz_sha256={xz_sha256}")
    print(f"indices_raw_sha256={indices_raw_sha256}")
    print(f"indices_xz_sha256={indices_xz_sha256}")
    print(f"ledger_sha256={ledger_sha256}")


if __name__ == "__main__":
    main()
