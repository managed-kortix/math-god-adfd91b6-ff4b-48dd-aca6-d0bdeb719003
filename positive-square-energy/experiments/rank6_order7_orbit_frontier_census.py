#!/usr/bin/env python3
"""Exact orbit and coarse-frontier census for order-seven rank-six kernels.

The artifact produced here is an experimental source, not a theorem fixture.
All arithmetic used for acceptance is integral (costs are scaled by 30).
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import multiprocessing
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
OUTPUT = HERE / "rank6_order7_orbit_frontier_census.json"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
ORDER = 7
RANK = 6
PATH_COUNT = ORDER + RANK - 1
BUDGET_SCALED = 30 * (RANK - 1)
PAIRS = tuple(itertools.combinations(range(ORDER), 2))
PAIR_INDEX = {edge: index for index, edge in enumerate(PAIRS)}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def relabel_action(permutation):
    return tuple(PAIR_INDEX[tuple(sorted((permutation[u], permutation[v])))] for u, v in PAIRS)


PERMUTATION_ACTIONS = tuple(relabel_action(p) for p in itertools.permutations(range(ORDER)))


def apply_action(row, action):
    return tuple(row[index] for index in action)


def automorphism_actions(kernel):
    return tuple(action for action in PERMUTATION_ACTIONS
                 if apply_action(kernel, action) == kernel)


def color_patterns(prefix=(0,)):
    if len(prefix) == ORDER:
        yield prefix
        return
    for color in range(min(3, max(prefix) + 1) + 1):
        yield from color_patterns(prefix + (color,))


def difference_mask(coloring):
    return tuple(coloring[u] != coloring[v] for u, v in PAIRS)


COLOR_MASKS = tuple(difference_mask(coloring) for coloring in color_patterns())


def coarse_cost_scaled(kernel, row, mask):
    total = 0
    for multiplicity, odd, different in zip(kernel, row, mask):
        if not different:
            if odd:
                return None
            continue
        if odd:
            total += 10 + 5 * odd
        total += 18 * (multiplicity - odd)
        if total > BUDGET_SCALED:
            return total
    return total


def minimum_coarse_cost_scaled(kernel, row):
    best = None
    for mask in COLOR_MASKS:
        value = coarse_cost_scaled(kernel, row, mask)
        if value is not None and (best is None or value < best):
            best = value
            if best <= BUDGET_SCALED:
                return best
    require(best is not None, "physical row has no admissible coloring")
    return best


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "rank-six fixture changed")
    payload = json.loads(raw.decode("ascii"))
    records = tuple((index, tuple(record["code"]))
                    for index, record in enumerate(payload["kernels"], 1)
                    if record["n"] == ORDER)
    require(len(records) == 314, "order-seven rank-six kernel count changed")
    require(records[0][0] == 332 and records[-1][0] == 645, "kernel interval changed")
    require(all(sum(kernel) == PATH_COUNT for _, kernel in records), "path count changed")
    return records


def census_kernel(item):
    kernel_number, kernel = item
    group = automorphism_actions(kernel)
    orbit_sizes = {}
    for row in itertools.product(*(range(value + 1) for value in kernel)):
        representative = min(apply_action(row, action) for action in group)
        orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
    residuals = []
    for row in sorted(orbit_sizes):
        cost = minimum_coarse_cost_scaled(kernel, row)
        if cost > BUDGET_SCALED:
            residuals.append({
                "kernel": kernel_number,
                "row": list(row),
                "orbit_size": orbit_sizes[row],
                "minimum_coarse_upper_bound_scaled_30": cost,
            })
    ledger = {
        "kernel": kernel_number,
        "code": list(kernel),
        "physical_rows": sum(orbit_sizes.values()),
        "automorphisms": len(group),
        "orbits": len(orbit_sizes),
        "coarse_certified": len(orbit_sizes) - len(residuals),
        "coarse_residuals": len(residuals),
    }
    return ledger, residuals


def regenerate(jobs=1, progress=False):
    sources = source_kernels()
    pool = None
    if jobs == 1:
        results = map(census_kernel, sources)
    else:
        pool = multiprocessing.Pool(jobs)
        results = pool.imap(census_kernel, sources)
    ledgers, residuals = [], []
    try:
        for index, (ledger, local) in enumerate(results, 1):
            ledgers.append(ledger)
            residuals.extend(local)
            if progress:
                print(f"[{index}/314] K{ledger['kernel']} orbits={ledger['orbits']} "
                      f"residuals={len(local)}", flush=True)
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    return {
        "schema": "rank-six-order-seven-orbit-frontier-census-experiment-v1",
        "status": "census_complete_certificates_open",
        "full_theorem": False,
        "rank": RANK,
        "order": ORDER,
        "budget": [RANK - 1, 1],
        "cost_scale": 30,
        "source_sha256": SOURCE_SHA256,
        "pair_order": [f"{u}{v}" for u, v in PAIRS],
        "kernel_interval": [332, 645],
        "kernel_total": len(ledgers),
        "path_count": PATH_COUNT,
        "physical_total": sum(row["physical_rows"] for row in ledgers),
        "orbit_total": sum(row["orbits"] for row in ledgers),
        "coarse_certified_total": sum(row["coarse_certified"] for row in ledgers),
        "coarse_residual_total": len(residuals),
        "frontiers_per_residual": 1 + PATH_COUNT,
        "frontier_target_total": len(residuals) * (1 + PATH_COUNT),
        "frontier_policy": "canonical plus every one-coordinate length-plus-two target",
        "certificate_fixture_frozen": False,
        "kernels": ledgers,
        "residuals": residuals,
    }


def verify(payload):
    require(payload["schema"] == "rank-six-order-seven-orbit-frontier-census-experiment-v1",
            "schema changed")
    require(payload["full_theorem"] is False and not payload["certificate_fixture_frozen"],
            "open experiment was theorem-promoted")
    require((payload["rank"], payload["order"], payload["kernel_interval"],
             payload["kernel_total"], payload["path_count"], payload["budget"],
             payload["cost_scale"]) == (6, 7, [332, 645], 314, 12, [5, 1], 30),
            "scope changed")
    require(payload["pair_order"] == [f"{u}{v}" for u, v in PAIRS], "pair order changed")
    require(payload["coarse_certified_total"] + payload["coarse_residual_total"]
            == payload["orbit_total"], "coarse partition changed")
    require(payload["frontiers_per_residual"] == 13 and payload["frontier_target_total"]
            == 13 * payload["coarse_residual_total"], "frontier count changed")
    require(tuple((row["kernel"], tuple(row["code"])) for row in payload["kernels"])
            == source_kernels(), "kernel selection changed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    require(args.jobs >= 1, "jobs must be positive")
    if args.verify is None:
        payload = regenerate(args.jobs, args.progress)
        verify(payload)
        require(args.output.parent.is_dir(), "output parent is missing")
        args.output.write_bytes(canonical_bytes(payload))
    else:
        raw = args.verify.read_bytes()
        payload = json.loads(raw.decode("ascii"))
        require(raw == canonical_bytes(payload), "census JSON is not canonical")
        verify(payload)
    print(f"kernels={payload['kernel_total']} physical={payload['physical_total']} "
          f"orbits={payload['orbit_total']}")
    print(f"coarse_certified={payload['coarse_certified_total']} "
          f"residuals={payload['coarse_residual_total']} "
          f"frontier_targets={payload['frontier_target_total']}")
    print("full_theorem=false")


if __name__ == "__main__":
    main()
