#!/usr/bin/env python3
"""Exact fail-closed census for the sixteen order-eight cubic kernels.

This is an experimental artifact only. It reconstructs every physical parity
row, quotients by the exact kernel automorphism group, and applies the regular
tetrahedron sieve using integer arithmetic.
"""

import argparse
import hashlib
import itertools
import json
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "research" / "fixtures" / "rank-five-kernels.json"
EXPECTED_SOURCE_SHA256 = "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884"
ARTIFACT = HERE / "order8-cubic-tetra-census.json"
VERTICES = 8
PAIRS = tuple(itertools.combinations(range(VERTICES), 2))
EXPECTED_KERNELS = 16
PATHS_PER_KERNEL = 12
ROW118 = 118


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256,
            "rank-five source fixture digest changed")
    payload = json.loads(raw.decode("ascii"))
    records = tuple((number, tuple(record["code"]))
                    for number, record in enumerate(payload["kernels"], 1)
                    if record["n"] == VERTICES)
    require(len(records) == EXPECTED_KERNELS, "order-eight kernel count changed")
    require(records[-1][0] == ROW118, "row 118 is no longer the final cubic kernel")
    return records


def edge_data(kernel):
    edges = tuple(pair for pair, multiplicity in zip(PAIRS, kernel) if multiplicity)
    require(sum(kernel) == PATHS_PER_KERNEL, "order-eight path count changed")
    degrees = [0] * VERTICES
    for (u, v), multiplicity in zip(PAIRS, kernel):
        degrees[u] += multiplicity
        degrees[v] += multiplicity
    require(degrees == [3] * VERTICES, "order-eight kernel is not cubic")
    return edges


def relabel(row, permutation):
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))] for u, v in PAIRS)


def automorphisms(kernel):
    group = []
    for permutation in itertools.permutations(range(VERTICES)):
        if relabel(kernel, permutation) == kernel:
            group.append(permutation)
    return tuple(group)


def crossing_masks(edges):
    masks = set()
    # Vertex zero has color zero. This retains one representative of every
    # coloring under global color permutation and permits at most four colors.
    for suffix in itertools.product(range(4), repeat=VERTICES - 1):
        colors = (0,) + suffix
        mask = sum(1 << index for index, (u, v) in enumerate(edges)
                   if colors[u] != colors[v])
        masks.add(mask)
    return masks


def tetra_cost(kernel, row, edges, crossing):
    total = 0
    support_index = {pair: index for index, pair in enumerate(edges)}
    for pair, multiplicity, odd in zip(PAIRS, kernel, row):
        if not multiplicity:
            continue
        if not crossing & (1 << support_index[pair]):
            if odd:
                return None
            continue
        # Common denominator 30 for 1/2, 1/6, and 3/5.
        if odd:
            total += 15 + 5 * (odd - 1)
        total += 18 * (multiplicity - odd)
    return total


def minimum_tetra_numerator(kernel, row, edges, crossings):
    costs = (tetra_cost(kernel, row, edges, crossing) for crossing in crossings)
    return min(cost for cost in costs if cost is not None)


def fraction_pair(numerator, denominator=30):
    divisor = gcd(numerator, denominator)
    return [numerator // divisor, denominator // divisor]


def row118_cycle_equality_row(kernel):
    return tuple(1 if multiplicity else 0 for multiplicity in kernel)


def regenerate():
    ledgers = []
    residuals = []
    for number, kernel in source_kernels():
        edges = edge_data(kernel)
        group = automorphisms(kernel)
        crossings = crossing_masks(edges)
        orbit_sizes = {}
        for row in itertools.product(*(range(value + 1) for value in kernel)):
            representative = min(relabel(row, permutation) for permutation in group)
            orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
        local = []
        for row in sorted(orbit_sizes):
            numerator = minimum_tetra_numerator(kernel, row, edges, crossings)
            if numerator > 120:
                record = {
                    "kernel": number,
                    "row": list(row),
                    "orbit_size": orbit_sizes[row],
                    "minimum_tetra_upper_bound": fraction_pair(numerator),
                    "row118_cycle_equality": (number == ROW118
                                              and row == row118_cycle_equality_row(kernel)),
                }
                residuals.append(record)
                local.append(record)
        ledgers.append({
            "kernel": number,
            "code": list(kernel),
            "edge_order": [f"{u}{v}" for u, v in edges],
            "automorphisms": len(group),
            "physical_rows": sum(orbit_sizes.values()),
            "orbits": len(orbit_sizes),
            "tetra_certified": len(orbit_sizes) - len(local),
            "tetra_residuals": len(local),
        })
    equality = [record for record in residuals if record["row118_cycle_equality"]]
    require(len(equality) == 1, "row 118 cycle equality residual is not unique")
    return {
        "schema": "rank-five-order-eight-cubic-tetra-census-experiment-v1",
        "status": "experimental_census_complete_certificates_open",
        "full_theorem": False,
        "experiment_fixture_frozen": True,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "kernel_total": len(ledgers),
        "paths_per_kernel": PATHS_PER_KERNEL,
        "physical_total": sum(row["physical_rows"] for row in ledgers),
        "orbit_total": sum(row["orbits"] for row in ledgers),
        "tetra_certified_total": sum(row["tetra_certified"] for row in ledgers),
        "tetra_residual_total": len(residuals),
        "frontiers_per_residual": 1 + PATHS_PER_KERNEL,
        "frontier_target_total": len(residuals) * (1 + PATHS_PER_KERNEL),
        "frontier_policy": "canonical plus every one-coordinate length-plus-two target",
        "row118_cycle_equality_residual_total": len(equality),
        "kernels": ledgers,
        "residuals": residuals,
    }


def audit():
    generated = regenerate()
    require(generated["kernel_total"] == EXPECTED_KERNELS, "kernel total changed")
    require(generated["physical_total"] == sum(
        __import__("math").prod(value + 1 for value in kernel)
        for _, kernel in source_kernels()), "physical total changed")
    require(generated["full_theorem"] is False, "experiment was theorem-promoted")
    require(generated["experiment_fixture_frozen"] is True, "experiment is not frozen")
    require(ARTIFACT.is_file(), "missing generated census artifact")
    raw = ARTIFACT.read_bytes()
    require(raw == canonical_bytes(generated), "stored census is not exact regeneration")
    return generated, hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-fixture", action="store_true")
    args = parser.parse_args()
    if args.write_fixture:
        ARTIFACT.write_bytes(canonical_bytes(regenerate()))
    generated, digest = audit()
    print("order-eight cubic tetra census: exact audit passed")
    print(f"kernels={generated['kernel_total']} physical={generated['physical_total']} "
          f"orbits={generated['orbit_total']}")
    print(f"tetra_certified={generated['tetra_certified_total']} "
          f"tetra_residuals={generated['tetra_residual_total']}")
    print(f"canonical_plus_12_frontiers={generated['frontier_target_total']} "
          "row118_cycle_equality=1")
    print("experiment_fixture_frozen=true full_theorem=false")
    print(f"fixture_sha256={digest}")


if __name__ == "__main__":
    main()
