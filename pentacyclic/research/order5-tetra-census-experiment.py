#!/usr/bin/env python3
"""Exact, fail-closed order-five rank-five tetrahedral census experiment.

This experiment deliberately does not freeze Gram certificates.  It reconstructs
the finite source and records the exact residual target set needed by a later
certificate search.  In particular, the exceptional all-odd simple
complete-minus-one-edge target is excluded only from the requested 207-target
search ledger; no claim is made for it.
"""

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "research" / "fixtures" / "rank-five-kernels.json"
EXPECTED_SOURCE_SHA256 = "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884"
ARTIFACT = HERE / "order5-tetra-census.json"
PAIRS = tuple(itertools.combinations(range(5), 2))
EXPECTED_KERNELS = 24
EXPECTED_PHYSICAL = 6282
EXPECTED_ORBITS = 4238
EXPECTED_RESIDUALS = 208
EXPECTED_SEARCH_TARGETS = 207
PATHS_PER_KERNEL = 9
EXPECTED_ALL_LENGTH_TARGETS = 2070
EXCLUDED_KERNEL = (0, 1, 1, 1, 1, 1, 1, 1, 1, 1)
EXCLUDED_ROW = EXCLUDED_KERNEL


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def relabel(row, permutation):
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in PAIRS)


def automorphisms(kernel):
    return tuple(permutation for permutation in itertools.permutations(range(5))
                 if relabel(kernel, permutation) == kernel)


def tetra_cost(kernel, row, coloring):
    total = Fraction(0)
    for (u, v), multiplicity, odd in zip(PAIRS, kernel, row):
        require(0 <= odd <= multiplicity, "invalid physical row")
        if coloring[u] == coloring[v]:
            if odd:
                return None
            continue
        if odd:
            total += Fraction(1, 2)
        total += Fraction(max(0, odd - 1), 6)
        total += Fraction(3 * (multiplicity - odd), 5)
    return total


def minimum_tetra_cost(kernel, row):
    costs = (tetra_cost(kernel, row, coloring)
             for coloring in itertools.product(range(4), repeat=5))
    admissible = tuple(cost for cost in costs if cost is not None)
    require(admissible, "physical row has no admissible tetrahedral coloring")
    return min(admissible)


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256,
            "rank-five source fixture digest changed")
    payload = json.loads(raw.decode("ascii"))
    kernels = tuple(tuple(record["code"]) for record in payload["kernels"]
                    if record["n"] == 5)
    require(len(kernels) == EXPECTED_KERNELS, "order-five kernel count changed")
    return kernels


def regenerate():
    ledgers = []
    residuals = []
    for kernel_number, kernel in enumerate(source_kernels(), 17):
        group = automorphisms(kernel)
        physical = tuple(itertools.product(*(range(value + 1) for value in kernel)))
        representatives = tuple(sorted({min(relabel(row, permutation)
                                            for permutation in group)
                                        for row in physical}))
        local_residuals = []
        for row in representatives:
            cost = minimum_tetra_cost(kernel, row)
            if cost > 4:
                record = {
                    "kernel": kernel_number,
                    "row": list(row),
                    "minimum_tetra_upper_bound": [cost.numerator, cost.denominator],
                }
                residuals.append(record)
                local_residuals.append(record)
        ledgers.append({
            "kernel": kernel_number,
            "code": list(kernel),
            "physical_rows": len(physical),
            "automorphisms": len(group),
            "orbits": len(representatives),
            "residuals": len(local_residuals),
        })
    excluded = [record for record in residuals
                if tuple(ledgers[record["kernel"] - 17]["code"]) == EXCLUDED_KERNEL
                and tuple(record["row"]) == EXCLUDED_ROW]
    search_targets = [record for record in residuals if record not in excluded]
    return {
        "schema": "rank-five-order-five-tetra-census-experiment-v1",
        "status": "census_complete_certificates_not_frozen",
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "pair_order": [f"{u}{v}" for u, v in PAIRS],
        "kernel_total": len(ledgers),
        "physical_total": sum(row["physical_rows"] for row in ledgers),
        "orbit_total": sum(row["orbits"] for row in ledgers),
        "residual_total": len(residuals),
        "excluded_target_total": len(excluded),
        "search_target_total": len(search_targets),
        "all_length_frontier_target_total": len(search_targets) * (1 + PATHS_PER_KERNEL),
        "frontier_policy": "canonical plus every one-coordinate length-plus-two target",
        "certificate_fixture_frozen": False,
        "kernels": ledgers,
        "residuals": residuals,
        "excluded_target_keys": [[record["kernel"], record["row"]]
                                 for record in excluded],
        "search_target_keys": [[record["kernel"], record["row"]]
                               for record in search_targets],
    }


def serialize(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"


def audit():
    generated = regenerate()
    require(generated["kernel_total"] == EXPECTED_KERNELS, "kernel total changed")
    require(generated["physical_total"] == EXPECTED_PHYSICAL, "physical total changed")
    require(generated["orbit_total"] == EXPECTED_ORBITS, "orbit total changed")
    require(generated["residual_total"] == EXPECTED_RESIDUALS, "residual total changed")
    require(generated["excluded_target_total"] == 1, "excluded target is not unique")
    require(generated["search_target_total"] == EXPECTED_SEARCH_TARGETS,
            "non-excluded search target total changed")
    require(generated["all_length_frontier_target_total"] == EXPECTED_ALL_LENGTH_TARGETS,
            "all-length frontier target total changed")
    require(not generated["certificate_fixture_frozen"],
            "incomplete experiment attempted certificate freeze")
    require(ARTIFACT.is_file(), "missing generated census artifact")
    stored = json.loads(ARTIFACT.read_text(encoding="ascii"))
    require(stored == generated, "stored artifact differs from exact regeneration")
    return generated


def main():
    generated = audit()
    print("order-five rank-five tetra census: exact audit passed")
    print(f"kernels={generated['kernel_total']} physical={generated['physical_total']} "
          f"orbits={generated['orbit_total']}")
    print(f"tetra_residuals={generated['residual_total']} "
          f"non_excluded_search_targets={generated['search_target_total']}")
    print(f"all_length_canonical_plus_coordinate_frontiers="
          f"{generated['all_length_frontier_target_total']}")
    print("certificate_freeze=false")


if __name__ == "__main__":
    main()
