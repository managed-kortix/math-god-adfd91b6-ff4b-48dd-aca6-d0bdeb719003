#!/usr/bin/env python3
"""Analyze order-eight packs as a dictionary of reusable branch-Gram templates.

The cover computed here is numerical evidence, not an exact certificate.  A
certificate verifier must replace the floating path-cost evaluation by outward
rational intervals (or exact rational waypoint costs).  Pack decoding and Gram
reconstruction do use the existing authenticated rational witnesses.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
PIPELINE_PATH = HERE / "rank6_order8_sparse_pipeline.py"
DEFAULT_PACKS = HERE / "rank6_order8_search_ckpt"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pipeline():
    spec = importlib.util.spec_from_file_location("rank6_order8_cover_pipeline", PIPELINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load sparse pipeline")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rational_unit_float(parameters):
    values = tuple(float(value) for value in parameters)
    square = sum(value * value for value in values)
    denominator = 1.0 + square
    return ((1.0 - square) / denominator,) + tuple(
        2.0 * value / denominator for value in values)


def gram_from_parameters(parameters):
    vectors = tuple(rational_unit_float(row) for row in parameters)
    return tuple(tuple(sum(x * y for x, y in zip(left, right))
                       for right in vectors) for left in vectors)


def path_cost(correlation, length):
    sign = -1.0 if length & 1 else 1.0
    transformed = max(-1.0, min(1.0, sign * correlation))
    if transformed >= 1.0:
        return 0.0
    angle = math.acos(transformed)
    tangent = math.tan(angle / (2.0 * length))
    return length * tangent * tangent


def row_cost(pipeline, source, gram):
    _, support, multiplicities, row, _, _, _ = source
    total = 0.0
    for dense_index, multiplicity, odd in zip(support, multiplicities, row):
        left, right = pipeline.PAIRS[dense_index]
        correlation = gram[left][right]
        if odd:
            total += path_cost(correlation, 1)
            total += (odd - 1) * path_cost(correlation, 3)
        total += (multiplicity - odd) * path_cost(correlation, 2)
    return total


def rounded_signature(gram, digits):
    return tuple(round(gram[left][right], digits)
                 for left in range(len(gram)) for right in range(left + 1, len(gram)))


def greedy_kernel_cover(pipeline, rows, grams, margin):
    """Return a greedy cover using only templates originating on this kernel."""
    if not rows:
        return (), ()
    pair_indices = sorted({dense_index for source in rows for dense_index in source[1]})
    pair_column = {dense_index: column for column, dense_index in enumerate(pair_indices)}
    correlations = np.asarray([
        [gram[pipeline.PAIRS[index][0]][pipeline.PAIRS[index][1]] for index in pair_indices]
        for gram in grams
    ], dtype=np.float64)
    costs = np.zeros((len(rows), len(grams)), dtype=np.float64)
    for row_index, source in enumerate(rows):
        _, support, multiplicities, parity, _, _, _ = source
        for dense_index, multiplicity, odd in zip(support, multiplicities, parity):
            values = correlations[:, pair_column[dense_index]]
            if odd:
                transformed = np.clip(-values, -1.0, 1.0)
                costs[row_index] += np.tan(np.arccos(transformed) / 2.0) ** 2
                if odd > 1:
                    tangent = np.tan(np.arccos(transformed) / 6.0)
                    costs[row_index] += (odd - 1) * 3.0 * tangent ** 2
            if multiplicity > odd:
                transformed = np.clip(values, -1.0, 1.0)
                tangent = np.tan(np.arccos(transformed) / 4.0)
                costs[row_index] += (multiplicity - odd) * 2.0 * tangent ** 2
    covers = costs <= float(pipeline.BUDGET) - margin
    uncovered = np.ones(len(rows), dtype=bool)
    selected = []
    while np.any(uncovered):
        gains = np.count_nonzero(covers[uncovered], axis=0)
        best = int(np.argmax(gains))
        if gains[best] == 0:
            break
        selected.append(best)
        uncovered &= ~covers[:, best]
    return tuple(selected), tuple(np.flatnonzero(uncovered).tolist())


def canonical_json(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packs", nargs="*", type=Path)
    parser.add_argument("--margin", type=float, default=1e-9,
                        help="numerical slack required below five")
    parser.add_argument("--round-digits", default="2,3,4,6")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    require(args.margin >= 0.0, "negative cover margin")

    pipeline = load_pipeline()
    _, residual_rows = pipeline.census(collect_residuals=True)
    paths = args.packs or sorted(DEFAULT_PACKS.glob("*.r8g.xz"))
    require(paths, "no search packs found")

    records = []
    ranges = []
    raw_digest = hashlib.sha256()
    compressed_bytes = 0
    raw_bytes = 0
    for path in paths:
        stored = path.read_bytes()
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
        compressed_bytes += len(stored)
        raw_bytes += len(raw)
        start, attempts, decoded = pipeline.decode_search(raw, residual_rows)
        ranges.append((start, start + attempts, path.name))
        raw_digest.update(hashlib.sha256(raw).digest())
        records.extend((start + local, record) for local, record in enumerate(decoded))
    records.sort(key=lambda item: item[0])
    require(len({index for index, _ in records}) == len(records), "overlapping packs")

    mode_counts = Counter()
    denominator_counts = Counter()
    grams_by_kernel = defaultdict(list)
    rows_by_kernel = defaultdict(list)
    exact_payload_hashes = set()
    exact_branch_parameter_hashes = set()
    signatures = defaultdict(set)
    digits = tuple(int(value) for value in args.round_digits.split(","))
    strict_costs = []
    for source_index, record in records:
        source = residual_rows[source_index]
        mode, payload = record
        mode_counts[mode] += 1
        rows_by_kernel[source[0]].append(source)
        if mode != pipeline.MODE_SHARED:
            continue
        denominator, branch_parameters, canonical, extended = payload
        denominator_counts[denominator] += 1
        payload_key = repr((denominator, branch_parameters, canonical, extended)).encode("ascii")
        exact_payload_hashes.add(hashlib.sha256(payload_key).digest())
        branch_key = repr(branch_parameters).encode("ascii")
        exact_branch_parameter_hashes.add(hashlib.sha256(branch_key).digest())
        gram = gram_from_parameters(branch_parameters)
        grams_by_kernel[source[0]].append(gram)
        cost = row_cost(pipeline, source, gram)
        strict_costs.append(cost)
        for width in digits:
            signatures[width].add(rounded_signature(gram, width))

    cover_selected = 0
    cover_uncovered = 0
    cover_kernel_counts = {}
    for kernel, rows in rows_by_kernel.items():
        grams = grams_by_kernel[kernel]
        if not grams:
            cover_uncovered += len(rows)
            continue
        selected, uncovered = greedy_kernel_cover(pipeline, rows, grams, args.margin)
        cover_selected += len(selected)
        cover_uncovered += len(uncovered)
        cover_kernel_counts[str(kernel)] = len(selected)

    mode_names = {
        pipeline.MODE_UNRESOLVED: "unresolved",
        pipeline.MODE_SHARED: "shared",
        pipeline.MODE_TEMPLATE: "symbolic_template",
        pipeline.MODE_INDIVIDUAL: "individual",
    }
    payload = {
        "schema": "rank-six-order-eight-template-cover-analysis-v1",
        "rigorous_certificate": False,
        "reason_nonrigorous": "greedy coverage uses binary64 transcendental path costs",
        "pack_ranges": [list(value) for value in ranges],
        "pack_raw_digest_of_digests_sha256": raw_digest.hexdigest(),
        "covered_residual_total": len(records),
        "covered_target_total": len(records) * (pipeline.PATH_COUNT + 1),
        "compressed_pack_bytes": compressed_bytes,
        "raw_pack_bytes": raw_bytes,
        "mode_counts": {mode_names[key]: mode_counts[key] for key in sorted(mode_counts)},
        "shared_denominators": {str(key): denominator_counts[key]
                                for key in sorted(denominator_counts)},
        "unique_exact_shared_payloads": len(exact_payload_hashes),
        "unique_exact_branch_parameter_arrays": len(exact_branch_parameter_hashes),
        "unique_rounded_branch_gram_signatures": {str(key): len(signatures[key])
                                                   for key in digits},
        "represented_kernel_total": len(rows_by_kernel),
        "shared_template_kernel_total": len(grams_by_kernel),
        "own_kernel_greedy_cover": {
            "required_margin": args.margin,
            "selected_template_total": cover_selected,
            "uncovered_residual_total": cover_uncovered,
            "selected_by_kernel": cover_kernel_counts,
        },
        "source_template_cost": {
            "minimum": min(strict_costs) if strict_costs else None,
            "maximum": max(strict_costs) if strict_costs else None,
            "at_least_five": sum(value >= float(pipeline.BUDGET) for value in strict_costs),
        },
    }
    rendered = canonical_json(payload)
    if args.output is not None:
        require(args.output.parent.is_dir(), "output parent does not exist")
        args.output.write_text(rendered, encoding="ascii")
    print(rendered, end="")


if __name__ == "__main__":
    main()
