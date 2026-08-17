#!/usr/bin/env python3
"""Segmented exact verifier for the rank-seven/order-eight typed Gram lane.

Each segment reruns the deterministic finite search, then independently checks
the proposed rational formula, its PSD decomposition, and all fifteen frontier
costs.  Canonical receipts carry a compact ownership bitmap.  The merge command
requires a gap-free partition of the complete authenticated residual stream and
produces the theorem-owner and combined order-eight accounting ledger.
"""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANE_PATH = HERE / "rank7_order8_typed_diagonal_gram_lane.py"
PAYLOAD_REPORT = HERE / "rank7_order8_payload_free_lane_coverage.json"
TYPED_REPORT = HERE / "rank7_order8_typed_diagonal_gram_coverage.json"
DEFAULT_RECEIPTS = HERE / "rank7_order8_typed_diagonal_receipts"
DEFAULT_LEDGER = HERE / "rank7_order8_combined_owner_accounting.json"
DEFAULT_CACHE = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
RECEIPT_SCHEMA = "rank-seven-order-eight-typed-diagonal-segment-receipt-v1"
LEDGER_SCHEMA = "rank-seven-order-eight-combined-owner-accounting-v1"
EXPECTED_ROWS = 492812
EXPECTED_TYPED_OWNERS = 402712
EXPECTED_COARSE_ROWS = 493417
TARGETS_PER_ROW = 15
ORDER = 8
F = Fraction
_WORKER_CONTEXT = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_lane():
    spec = importlib.util.spec_from_file_location("rank7_order8_segmented_lane", LANE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load typed Gram lane")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


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


def pair(value):
    return [value.numerator, value.denominator]


def bitmap_encode(values):
    raw = bytearray((len(values) + 7) // 8)
    for index, value in enumerate(values):
        if value:
            raw[index // 8] |= 1 << (index % 8)
    return base64.b64encode(raw).decode("ascii")


def bitmap_decode(encoded, count):
    try:
        raw = base64.b64decode(encoded.encode("ascii"), validate=True)
    except (UnicodeEncodeError, ValueError) as error:
        raise RuntimeError("invalid receipt ownership bitmap") from error
    require(len(raw) == (count + 7) // 8, "wrong receipt ownership bitmap length")
    if count % 8:
        require(raw[-1] >> (count % 8) == 0, "nonzero receipt bitmap padding")
    return tuple(bool(raw[index // 8] & (1 << (index % 8))) for index in range(count))


def exact_certificate(lane, engine, census, source, result):
    """Check a search result without trusting the lane's cost implementation."""
    claimed_cost, _, claimed_normalizer, type_keys, type_ids, parameters = result
    require(len(parameters) == len(set(type_keys)), "parameter/type count mismatch")
    signed = [[0] * ORDER for _ in range(ORDER)]
    for dense, multiplicity, odd in zip(source[2], source[3], source[4], strict=True):
        u, v = census.PAIRS[dense]
        signed[u][v] = signed[v][u] = multiplicity - 2 * odd
    d0 = [parameters[int(type_ids[u])][0] for u in range(ORDER)]
    d1 = [parameters[int(type_ids[u])][1] for u in range(ORDER)]
    x = [[(d0[u] if u == v else F()) + d1[u] * signed[u][v]
          for v in range(ORDER)] for u in range(ORDER)]
    square = [[sum(x[u][w] * x[v][w] for w in range(ORDER))
               for v in range(ORDER)] for u in range(ORDER)]
    normalizer = max(square[u][u] for u in range(ORDER))
    require(normalizer > 0 and normalizer == claimed_normalizer, "normalizer mismatch")
    completion = [1 - square[u][u] / normalizer for u in range(ORDER)]
    require(all(value >= 0 for value in completion), "negative diagonal PSD completion")
    gram = [[square[u][v] / normalizer +
             (completion[u] if u == v else F()) for v in range(ORDER)]
            for u in range(ORDER)]
    require(all(gram[u][u] == 1 for u in range(ORDER)), "Gram diagonal is not one")
    require(all(gram[u][v] == gram[v][u]
                for u in range(ORDER) for v in range(ORDER)), "Gram is not symmetric")
    paths = tuple(engine.base.path_ledger(census, source))
    local = []
    for _, _, u, v, length in paths:
        transformed = -gram[u][v] if length & 1 else gram[u][v]
        require(-1 <= transformed <= 1, "Gram correlation escaped [-1,1]")
        if transformed == -1:
            require(claimed_cost is None, "lane missed an infinite exact path cost")
            return False, None, None
        local.append((1 - transformed) / (length * (1 + transformed)))
    base = sum(local, F())
    targets = [base]
    for old, (_, _, u, v, length) in zip(local, paths, strict=True):
        transformed = -gram[u][v] if length & 1 else gram[u][v]
        replacement = (1 - transformed) / ((length + 2) * (1 + transformed))
        targets.append(base - old + replacement)
    require(len(targets) == TARGETS_PER_ROW and all(value <= base for value in targets),
            "frontier monotonicity failed")
    require(claimed_cost == base, "lane and independent exact costs disagree")
    return base <= engine.BUDGET, base, max(targets)


def worker(index):
    lane, engine, census, residuals, ratios, grid, passes = _WORKER_CONTEXT
    result = lane.search_row(engine, census, residuals[index], ratios, grid, passes)
    accepted, cost, worst = exact_certificate(lane, engine, census, residuals[index], result)
    parameters = result[5]
    classification = canonical_bytes([
        index, residuals[index][1], accepted, None if cost is None else pair(cost),
        [[pair(left), pair(right)] for left, right in parameters],
    ])
    return accepted, cost, worst, classification


def verify_segment(lane, engine, census, residuals, start, stop, workers, passes,
                   max_denominator, maximum, progress=False):
    global _WORKER_CONTEXT
    require(0 <= start < stop <= len(residuals), "bad half-open segment")
    ratios = lane.rationals(max_denominator, maximum, include_zero=True)
    scales = (F(1, 2), F(2, 3), F(1), F(3, 2), F(2))
    grid = tuple((float(scale), float(scale * ratio), scale, scale * ratio)
                 for scale in scales for ratio in ratios)
    _WORKER_CONTEXT = lane, engine, census, residuals, ratios, grid, passes
    indices = range(start, stop)
    executor = None
    if workers == 1:
        results = map(worker, indices)
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker, indices, chunksize=64)
    owners = []
    classification = hashlib.sha256()
    coverage = hashlib.sha256()
    try:
        for offset, result in enumerate(results):
            index = start + offset
            accepted, cost, worst, raw = result
            owners.append(accepted)
            classification.update(raw)
            coverage.update(canonical_bytes([index, residuals[index][1], accepted]))
            if progress and (offset + 1) % 5000 == 0:
                print(f"segment={start}:{stop} rows={offset + 1} owners={sum(owners)}",
                      flush=True)
    finally:
        if executor is not None:
            executor.shutdown()
    bitmap = bitmap_encode(owners)
    return {
        "schema": RECEIPT_SCHEMA,
        "source_stream_sha256": census.SOURCE_SHA256,
        "row_range": [start, stop],
        "row_total": stop - start,
        "first_source_index": residuals[start][1],
        "last_source_index": residuals[stop - 1][1],
        "search": {"maximum_denominator": max_denominator, "maximum": maximum,
                   "coordinate_passes": passes, "d0_scales": [pair(value) for value in scales]},
        "verified": {
            "rational_feature_formula_rows": stop - start,
            "exact_psd_decomposition_rows": stop - start,
            "exact_frontier_cost_total": (stop - start) * TARGETS_PER_ROW,
        },
        "typed_owner_total": sum(owners),
        "unowned_total": len(owners) - sum(owners),
        "ownership_bitmap_base64": bitmap,
        "ownership_bitmap_sha256": hashlib.sha256(base64.b64decode(bitmap)).hexdigest(),
        "coverage_stream_sha256": coverage.hexdigest(),
        "full_classification_segment_sha256": classification.hexdigest(),
        "proof_contract": {
            "gram": "XX^T/M plus diag(1-diag(XX^T)/M)",
            "psd": "exact rational Gram factor plus exact nonnegative diagonal completion",
            "costs": "canonical and fourteen length-plus-two targets checked with Fraction",
        },
    }


def validate_receipt(receipt, census, residuals):
    require(receipt.get("schema") == RECEIPT_SCHEMA and
            receipt.get("source_stream_sha256") == census.SOURCE_SHA256,
            "wrong segment receipt scope")
    start, stop = receipt["row_range"]
    count = stop - start
    require(0 <= start < stop <= len(residuals) and receipt["row_total"] == count,
            "bad receipt range arithmetic")
    require((receipt["first_source_index"], receipt["last_source_index"]) ==
            (residuals[start][1], residuals[stop - 1][1]), "receipt source endpoints changed")
    values = bitmap_decode(receipt["ownership_bitmap_base64"], count)
    bitmap_raw = base64.b64decode(receipt["ownership_bitmap_base64"])
    require(hashlib.sha256(bitmap_raw).hexdigest() == receipt["ownership_bitmap_sha256"],
            "receipt bitmap digest changed")
    require(sum(values) == receipt["typed_owner_total"] and
            count - sum(values) == receipt["unowned_total"], "receipt owner arithmetic changed")
    verified = receipt["verified"]
    require(verified == {"rational_feature_formula_rows": count,
                         "exact_psd_decomposition_rows": count,
                         "exact_frontier_cost_total": count * TARGETS_PER_ROW},
            "receipt exact-verification ledger changed")
    digest = hashlib.sha256()
    for offset, accepted in enumerate(values):
        index = start + offset
        digest.update(canonical_bytes([index, residuals[index][1], accepted]))
    require(digest.hexdigest() == receipt["coverage_stream_sha256"],
            "receipt coverage digest changed")
    return start, stop, values


def read_canonical(path, label):
    raw = path.read_bytes()
    payload = strict_json(raw, label)
    require(raw == canonical_bytes(payload), f"noncanonical {label}")
    return payload, hashlib.sha256(raw).hexdigest()


def merge_receipts(census, residuals, receipt_paths, payload_path, typed_path):
    records = []
    for path in receipt_paths:
        payload, digest = read_canonical(path, path.name)
        start, stop, values = validate_receipt(payload, census, residuals)
        records.append((start, stop, values, path.name, digest))
    records.sort()
    require(records and records[0][0] == 0 and records[-1][1] == len(residuals) and
            all(left[1] == right[0] for left, right in zip(records, records[1:])),
            "receipts do not partition the complete residual stream")
    coverage = hashlib.sha256()
    typed_total = 0
    for start, _, values, _, _ in records:
        for offset, accepted in enumerate(values):
            index = start + offset
            coverage.update(canonical_bytes([index, residuals[index][1], accepted]))
            typed_total += accepted
    payload, payload_digest = read_canonical(payload_path, "payload-free coverage report")
    typed, typed_digest = read_canonical(typed_path, "typed-diagonal coverage report")
    payload_owned = payload["recognized_residual_total"]
    require(payload["scanned_residual_total"] == EXPECTED_COARSE_ROWS and
            payload["rational_search_residual_total"] == len(residuals),
            "payload-free partition changed")
    require(typed["source_stream_sha256"] == census.SOURCE_SHA256 and
            typed["scanned_residual_total"] == len(residuals) and
            typed["covered_residual_total"] == typed_total == EXPECTED_TYPED_OWNERS,
            "typed owner count differs from committed full scan")
    combined = payload_owned + typed_total
    remainder = EXPECTED_COARSE_ROWS - combined
    return {
        "schema": LEDGER_SCHEMA,
        "full_theorem": False,
        "scope": "complete disjoint owner accounting for rank-seven order eight",
        "source_stream_sha256": census.SOURCE_SHA256,
        "coarse_residual_total": EXPECTED_COARSE_ROWS,
        "targets_per_residual": TARGETS_PER_ROW,
        "owner_precedence": ["payload-free", "typed-diagonal-rational-gram"],
        "exclusive_owner_row_counts": {
            "payload-free": payload_owned,
            "typed-diagonal-rational-gram": typed_total,
        },
        "exclusive_owner_target_counts": {
            "payload-free": payload_owned * TARGETS_PER_ROW,
            "typed-diagonal-rational-gram": typed_total * TARGETS_PER_ROW,
        },
        "combined_owned_residual_total": combined,
        "combined_owned_target_total": combined * TARGETS_PER_ROW,
        "remaining_residual_total": remainder,
        "remaining_target_total": remainder * TARGETS_PER_ROW,
        "typed_coverage_stream_sha256": coverage.hexdigest(),
        "segment_receipts": [
            {"row_range": [start, stop], "path": name, "sha256": digest,
             "typed_owner_total": sum(values)}
            for start, stop, values, name, digest in records
        ],
        "payload_free_report_sha256": payload_digest,
        "typed_full_scan_report_sha256": typed_digest,
        "theorem_contract": {
            "coverage": "gap-free receipts partition all 492812 rational-search rows",
            "formula": "every receipt row independently verifies the exact typed formula and PSD split",
            "cost": "all 15 exact Fraction frontier costs are checked per row",
            "disjointness": "the rational-search stream is the exact complement of payload-free owners",
        },
    }


def write_canonical(path, payload):
    require(path.parent.is_dir(), f"output parent does not exist: {path.parent}")
    raw = canonical_bytes(payload)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(raw)
    temporary.replace(path)
    return hashlib.sha256(raw).hexdigest()


def load_scope(cache_path=None):
    lane = load_lane()
    engine = lane.load_engine()
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=cache_path)
    require(len(residuals) == EXPECTED_ROWS, "typed residual stream size changed")
    return lane, engine, census, residuals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--census-cache", type=Path, default=DEFAULT_CACHE)
    subparsers = parser.add_subparsers(dest="command", required=True)
    verify = subparsers.add_parser("verify-segment")
    verify.add_argument("--start", type=int, required=True)
    verify.add_argument("--stop", type=int, required=True)
    verify.add_argument("--output", type=Path, required=True)
    verify.add_argument("--workers", type=int, default=1)
    verify.add_argument("--passes", type=int, default=3)
    verify.add_argument("--max-denominator", type=int, default=8)
    verify.add_argument("--maximum", type=int, default=4)
    verify.add_argument("--progress", action="store_true")
    verify_all = subparsers.add_parser("verify-all")
    verify_all.add_argument("--output-dir", type=Path, default=DEFAULT_RECEIPTS)
    verify_all.add_argument("--chunk-rows", type=int, default=25000)
    verify_all.add_argument("--workers", type=int, default=1)
    verify_all.add_argument("--passes", type=int, default=3)
    verify_all.add_argument("--max-denominator", type=int, default=8)
    verify_all.add_argument("--maximum", type=int, default=4)
    verify_all.add_argument("--progress", action="store_true")
    audit = subparsers.add_parser("audit-receipt")
    audit.add_argument("receipt", type=Path)
    audit.add_argument("--workers", type=int, default=1)
    audit.add_argument("--progress", action="store_true")
    merge = subparsers.add_parser("merge")
    merge.add_argument("receipts", nargs="+", type=Path)
    merge.add_argument("--payload-report", type=Path, default=PAYLOAD_REPORT)
    merge.add_argument("--typed-report", type=Path, default=TYPED_REPORT)
    merge.add_argument("--output", type=Path, default=DEFAULT_LEDGER)
    args = parser.parse_args()
    lane, engine, census, residuals = load_scope(args.census_cache)
    if args.command == "verify-segment":
        require(args.workers > 0 and args.passes > 0 and args.max_denominator > 0 and
                args.maximum > 0, "bad verifier search parameters")
        receipt = verify_segment(lane, engine, census, residuals, args.start, args.stop,
                                 args.workers, args.passes, args.max_denominator,
                                 args.maximum, args.progress)
        digest = write_canonical(args.output, receipt)
        print(f"receipt={args.output} rows={receipt['row_total']} "
              f"owners={receipt['typed_owner_total']} sha256={digest}")
        return
    if args.command == "verify-all":
        require(args.output_dir.is_dir(), "receipt output directory does not exist")
        require(args.chunk_rows > 0 and args.workers > 0 and args.passes > 0 and
                args.max_denominator > 0 and args.maximum > 0, "bad verifier parameters")
        paths = []
        for start in range(0, len(residuals), args.chunk_rows):
            stop = min(start + args.chunk_rows, len(residuals))
            path = args.output_dir / f"receipt-{start:06d}-{stop:06d}.json"
            if path.is_file():
                stored, _ = read_canonical(path, path.name)
                validate_receipt(stored, census, residuals)
                require(stored["row_range"] == [start, stop] and stored["search"] == {
                    "maximum_denominator": args.max_denominator, "maximum": args.maximum,
                    "coordinate_passes": args.passes,
                    "d0_scales": [[1, 2], [2, 3], [1, 1], [3, 2], [2, 1]],
                }, "existing receipt has incompatible search parameters")
                print(f"receipt={path} status=reused", flush=True)
            else:
                receipt = verify_segment(lane, engine, census, residuals, start, stop,
                                         args.workers, args.passes, args.max_denominator,
                                         args.maximum, args.progress)
                digest = write_canonical(path, receipt)
                print(f"receipt={path} owners={receipt['typed_owner_total']} "
                      f"sha256={digest}", flush=True)
            paths.append(path)
        ledger = merge_receipts(census, residuals, paths, PAYLOAD_REPORT, TYPED_REPORT)
        digest = write_canonical(DEFAULT_LEDGER, ledger)
        print(f"ledger={DEFAULT_LEDGER} owned={ledger['combined_owned_residual_total']} "
              f"remaining={ledger['remaining_residual_total']} sha256={digest}")
        return
    if args.command == "audit-receipt":
        stored, stored_digest = read_canonical(args.receipt, args.receipt.name)
        start, stop = stored["row_range"]
        search = stored["search"]
        regenerated = verify_segment(lane, engine, census, residuals, start, stop,
                                     args.workers, search["coordinate_passes"],
                                     search["maximum_denominator"], search["maximum"],
                                     args.progress)
        require(canonical_bytes(regenerated) == canonical_bytes(stored),
                "receipt does not reproduce byte-for-byte")
        print(f"audit=passed rows={stop - start} sha256={stored_digest}")
        return
    ledger = merge_receipts(census, residuals, args.receipts, args.payload_report,
                            args.typed_report)
    digest = write_canonical(args.output, ledger)
    print(f"ledger={args.output} owned={ledger['combined_owned_residual_total']} "
          f"remaining={ledger['remaining_residual_total']} sha256={digest}")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
