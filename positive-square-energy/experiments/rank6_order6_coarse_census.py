#!/usr/bin/env python3
"""Exact coarse-orbit census for the 216 order-six rank-six kernels.

This is an experimental, fail-closed source for a later rational Gram search.
It makes no theorem claim.
"""

import argparse
import hashlib
import itertools
import json
import multiprocessing
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
OUTPUT = HERE / "rank6_order6_coarse_census.json"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
ORDER = 6
RANK = 6
PATHS = ORDER + RANK - 1
BUDGET = Fraction(RANK - 1)
PAIRS = tuple(itertools.combinations(range(ORDER), 2))
COLORINGS = tuple((0,) + suffix for suffix in itertools.product(range(4), repeat=ORDER - 1))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def relabel(row, permutation):
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))] for u, v in PAIRS)


def automorphisms(kernel):
    return tuple(permutation for permutation in itertools.permutations(range(ORDER))
                 if relabel(kernel, permutation) == kernel)


def coarse_cost(kernel, row, coloring):
    total = Fraction(0)
    for (u, v), multiplicity, odd in zip(PAIRS, kernel, row):
        require(0 <= odd <= multiplicity, "invalid physical row")
        if coloring[u] == coloring[v]:
            if odd:
                return None
            continue
        if odd:
            total += Fraction(1, 2) + Fraction(max(0, odd - 1), 6)
        total += Fraction(3 * (multiplicity - odd), 5)
    return total


def minimum_coarse_cost(kernel, row):
    values = (coarse_cost(kernel, row, coloring) for coloring in COLORINGS)
    return min(value for value in values if value is not None)


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "rank-six fixture changed")
    payload = json.loads(raw.decode("ascii"))
    records = tuple((index, tuple(record["code"]))
                    for index, record in enumerate(payload["kernels"], 1)
                    if record["n"] == ORDER)
    require(len(records) == 216, "order-six rank-six kernel count changed")
    require(all(sum(kernel) == PATHS for _, kernel in records), "path count changed")
    return records


def census_kernel(item):
    kernel_number, kernel = item
    group = automorphisms(kernel)
    orbit_sizes = {}
    for row in itertools.product(*(range(value + 1) for value in kernel)):
        representative = min(relabel(row, permutation) for permutation in group)
        orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
    local_residuals = []
    for row in sorted(orbit_sizes):
        cost = minimum_coarse_cost(kernel, row)
        if cost > BUDGET:
            local_residuals.append({
                "kernel": kernel_number,
                "row": list(row),
                "orbit_size": orbit_sizes[row],
                "minimum_coarse_upper_bound": [cost.numerator, cost.denominator],
            })
    ledger = {
        "kernel": kernel_number,
        "code": list(kernel),
        "physical_rows": sum(orbit_sizes.values()),
        "automorphisms": len(group),
        "orbits": len(orbit_sizes),
        "coarse_certified": len(orbit_sizes) - len(local_residuals),
        "coarse_residuals": len(local_residuals),
    }
    return ledger, local_residuals


def regenerate(progress=False, jobs=1):
    sources = source_kernels()
    if jobs == 1:
        results = map(census_kernel, sources)
    else:
        pool = multiprocessing.Pool(jobs)
        results = pool.imap(census_kernel, sources)
    ledgers, residuals = [], []
    try:
        for local_index, (ledger, local_residuals) in enumerate(results, 1):
            ledgers.append(ledger)
            residuals.extend(local_residuals)
            if progress:
                print(f"[{local_index}/216] K{ledger['kernel']} orbits={ledger['orbits']} "
                      f"residuals={len(local_residuals)}", flush=True)
    finally:
        if jobs != 1:
            pool.close()
            pool.join()
    return {
        "schema": "rank-six-order-six-coarse-census-experiment-v1",
        "status": "census_complete_certificates_open",
        "full_theorem": False,
        "rank": RANK,
        "order": ORDER,
        "budget": [BUDGET.numerator, BUDGET.denominator],
        "source_sha256": SOURCE_SHA256,
        "pair_order": [f"{u}{v}" for u, v in PAIRS],
        "kernel_total": len(ledgers),
        "path_count": PATHS,
        "physical_total": sum(record["physical_rows"] for record in ledgers),
        "orbit_total": sum(record["orbits"] for record in ledgers),
        "coarse_certified_total": sum(record["coarse_certified"] for record in ledgers),
        "coarse_residual_total": len(residuals),
        "frontiers_per_residual": 1 + PATHS,
        "frontier_target_total": len(residuals) * (1 + PATHS),
        "frontier_policy": "canonical plus every one-coordinate length-plus-two target",
        "certificate_fixture_frozen": False,
        "kernels": ledgers,
        "residuals": residuals,
    }


def verify(payload):
    require(payload["full_theorem"] is False, "experiment was theorem-promoted")
    require(payload["kernel_total"] == 216 and payload["path_count"] == 11,
            "scope changed")
    require(payload["coarse_certified_total"] + payload["coarse_residual_total"]
            == payload["orbit_total"], "coarse partition changed")
    require(payload["frontier_target_total"]
            == 12 * payload["coarse_residual_total"], "frontier count changed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        payload = json.loads(args.verify.read_text(encoding="ascii"))
        verify(payload)
    else:
        require(args.jobs >= 1, "jobs must be positive")
        payload = regenerate(args.progress, args.jobs)
        verify(payload)
        require(args.output.parent.is_dir(), "output parent is missing")
        args.output.write_bytes(canonical_bytes(payload))
    print(f"kernels={payload['kernel_total']} physical={payload['physical_total']} "
          f"orbits={payload['orbit_total']}")
    print(f"coarse_certified={payload['coarse_certified_total']} "
          f"coarse_residuals={payload['coarse_residual_total']} "
          f"frontier_targets={payload['frontier_target_total']}")
    print("full_theorem=false")


if __name__ == "__main__":
    main()
