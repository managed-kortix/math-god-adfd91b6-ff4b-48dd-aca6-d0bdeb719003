#!/usr/bin/env python3
"""Exact fail-closed order-seven rank-five tetrahedral census experiment.

The artifact is experimental only. It freezes the complete finite source and
the residual canonical-plus-coordinate ledger, but makes no theorem claim.
"""

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "research" / "fixtures" / "rank-five-kernels.json"
EXPECTED_SOURCE_SHA256 = "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884"
ARTIFACT = HERE / "order7-tetra-census.json"
PAIRS = tuple(itertools.combinations(range(7), 2))
EXPECTED_KERNELS = 23
EXPECTED_PHYSICAL = 31112
EXPECTED_ORBITS = 18026
EXPECTED_RESIDUALS = 3720
PATHS_PER_KERNEL = 11
EXPECTED_FRONTIERS = EXPECTED_RESIDUALS * (1 + PATHS_PER_KERNEL)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def relabel(row, permutation):
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))] for u, v in PAIRS)


def automorphisms(kernel):
    return tuple(permutation for permutation in itertools.permutations(range(7))
                 if relabel(kernel, permutation) == kernel)


def color_patterns(prefix=(0,)):
    if len(prefix) == 7:
        yield prefix
        return
    for color in range(min(3, max(prefix) + 1) + 1):
        yield from color_patterns(prefix + (color,))


COLORINGS = tuple(color_patterns())


def tetra_cost(kernel, row, coloring):
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


def minimum_tetra_cost(kernel, row):
    costs = (tetra_cost(kernel, row, coloring) for coloring in COLORINGS)
    return min(cost for cost in costs if cost is not None)


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256,
            "rank-five source fixture digest changed")
    payload = json.loads(raw.decode("ascii"))
    kernels = tuple(tuple(record["code"]) for record in payload["kernels"]
                    if record["n"] == 7)
    require(len(kernels) == EXPECTED_KERNELS, "order-seven kernel count changed")
    return kernels


def regenerate():
    ledgers = []
    residuals = []
    for kernel_number, kernel in enumerate(source_kernels(), 80):
        require(sum(kernel) == PATHS_PER_KERNEL, "order-seven path count changed")
        group = automorphisms(kernel)
        orbit_sizes = {}
        for row in itertools.product(*(range(value + 1) for value in kernel)):
            representative = min(relabel(row, permutation) for permutation in group)
            orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
        local_residuals = []
        for row in sorted(orbit_sizes):
            cost = minimum_tetra_cost(kernel, row)
            if cost > 4:
                record = {
                    "kernel": kernel_number,
                    "row": list(row),
                    "orbit_size": orbit_sizes[row],
                    "minimum_tetra_upper_bound": [cost.numerator, cost.denominator],
                }
                residuals.append(record)
                local_residuals.append(record)
        ledgers.append({
            "kernel": kernel_number,
            "code": list(kernel),
            "physical_rows": sum(orbit_sizes.values()),
            "automorphisms": len(group),
            "orbits": len(orbit_sizes),
            "tetra_certified": len(orbit_sizes) - len(local_residuals),
            "tetra_residuals": len(local_residuals),
        })
    return {
        "schema": "rank-five-order-seven-tetra-census-experiment-v1",
        "status": "census_complete_certificates_open",
        "full_theorem": False,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "pair_order": [f"{u}{v}" for u, v in PAIRS],
        "kernel_total": len(ledgers),
        "physical_total": sum(record["physical_rows"] for record in ledgers),
        "orbit_total": sum(record["orbits"] for record in ledgers),
        "tetra_certified_total": sum(record["tetra_certified"] for record in ledgers),
        "tetra_residual_total": len(residuals),
        "paths_per_kernel": PATHS_PER_KERNEL,
        "frontiers_per_residual": 1 + PATHS_PER_KERNEL,
        "frontier_target_total": len(residuals) * (1 + PATHS_PER_KERNEL),
        "frontier_policy": "canonical plus every one-coordinate length-plus-two target",
        "certificate_fixture_frozen": False,
        "kernels": ledgers,
        "residuals": residuals,
    }


def audit():
    generated = regenerate()
    require(generated["kernel_total"] == EXPECTED_KERNELS, "kernel total changed")
    require(generated["physical_total"] == EXPECTED_PHYSICAL, "physical total changed")
    require(generated["orbit_total"] == EXPECTED_ORBITS, "orbit total changed")
    require(generated["tetra_residual_total"] == EXPECTED_RESIDUALS, "residual total changed")
    require(generated["tetra_certified_total"] == EXPECTED_ORBITS - EXPECTED_RESIDUALS,
            "tetra partition changed")
    require(generated["frontier_target_total"] == EXPECTED_FRONTIERS,
            "canonical-plus-coordinate frontier total changed")
    require(generated["full_theorem"] is False and not generated["certificate_fixture_frozen"],
            "incomplete experiment was promoted")
    require(ARTIFACT.is_file(), "missing generated census artifact")
    raw = ARTIFACT.read_bytes()
    require(raw == canonical_bytes(generated), "stored census is not exact canonical regeneration")
    return generated, hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-fixture", action="store_true")
    args = parser.parse_args()
    if args.write_fixture:
        generated = regenerate()
        require(ARTIFACT.parent.is_dir(), "artifact parent is missing")
        ARTIFACT.write_bytes(canonical_bytes(generated))
    generated, digest = audit()
    print("order-seven rank-five tetra census: exact audit passed")
    print(f"kernels={generated['kernel_total']} physical={generated['physical_total']} "
          f"orbits={generated['orbit_total']}")
    print(f"tetra_certified={generated['tetra_certified_total']} "
          f"tetra_residuals={generated['tetra_residual_total']}")
    print(f"canonical_plus_coordinate_frontiers={generated['frontier_target_total']}")
    print("full_theorem=false certificate_fixture_frozen=false")
    print(f"fixture_sha256={digest}")


if __name__ == "__main__":
    main()
