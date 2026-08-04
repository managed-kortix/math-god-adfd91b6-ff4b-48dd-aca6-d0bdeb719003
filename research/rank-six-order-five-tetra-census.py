#!/usr/bin/env python3
"""Exact fail-closed tetrahedral census for order-five rank-six kernels."""

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "fixtures" / "rank-six-kernels.json"
FIXTURE = HERE / "fixtures" / "rank-six-order-five-tetra-census.json"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
PAIRS = tuple(itertools.combinations(range(5), 2))
BUDGET = Fraction(5)


def set_partition_colorings():
    rows = []
    def extend(prefix):
        if len(prefix) == 5:
            rows.append(tuple(prefix))
            return
        for color in range(min(4, max(prefix) + 2)):
            extend(prefix + [color])
    extend([0])
    return tuple(rows)


COLORINGS = set_partition_colorings()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def relabel(row, permutation):
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))] for u, v in PAIRS)


def automorphisms(kernel):
    return tuple(p for p in itertools.permutations(range(5)) if relabel(kernel, p) == kernel)


def tetra_cost(kernel, row, coloring):
    total = Fraction(0)
    for multiplicity, odd, (u, v) in zip(kernel, row, PAIRS):
        require(0 <= odd <= multiplicity, "invalid physical row")
        if coloring[u] == coloring[v]:
            if odd:
                return None
            continue
        if odd:
            total += Fraction(1, 2) + (odd - 1) * Fraction(1, 6)
        total += (multiplicity - odd) * Fraction(3, 5)
    return total


def minimum_cost(kernel, row):
    candidates = []
    for coloring in COLORINGS:
        cost = tetra_cost(kernel, row, coloring)
        if cost is not None:
            candidates.append((cost, coloring))
    return min(candidates) if candidates else None


def source_kernels(expected_digest=SOURCE_SHA256):
    raw = SOURCE.read_bytes()
    require(expected_digest == SOURCE_SHA256, "source digest policy changed")
    require(hashlib.sha256(raw).hexdigest() == expected_digest, "rank-six source changed")
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), "rank-six source is not canonical JSON")
    rows = tuple(tuple(record["code"]) for record in payload["kernels"] if record["n"] == 5)
    require(len(rows) == 84, "order-five rank-six kernel count changed")
    return rows


def regenerate():
    ledgers = []
    records = []
    for number, kernel in enumerate(source_kernels(), 32):
        group = automorphisms(kernel)
        orbit_sizes = {}
        for row in itertools.product(*(range(value + 1) for value in kernel)):
            representative = min(relabel(row, p) for p in group)
            orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
        local = []
        for row in sorted(orbit_sizes):
            minimum = minimum_cost(kernel, row)
            cost, coloring = minimum if minimum is not None else (None, None)
            record = {
                "kernel": number,
                "row": list(row),
                "orbit_size": orbit_sizes[row],
                "minimum_rational_upper": ([cost.numerator, cost.denominator]
                                             if cost is not None else None),
                "first_coloring": list(coloring) if coloring is not None else None,
                "certified": cost is not None and cost <= BUDGET,
            }
            records.append(record)
            local.append(record)
        ledgers.append({
            "kernel": number,
            "code": list(kernel),
            "physical_rows": sum(orbit_sizes.values()),
            "automorphisms": len(group),
            "orbits": len(orbit_sizes),
            "certified": sum(record["certified"] for record in local),
            "residual": sum(not record["certified"] for record in local),
        })
    residual_keys = [[record["kernel"], record["row"]]
                     for record in records if not record["certified"]]
    return {
        "schema": "rank-six-order-five-tetra-census-v1",
        "status": "exact_census_residual_open",
        "source_sha256": SOURCE_SHA256,
        "pair_order": [f"{u}{v}" for u, v in PAIRS],
        "budget": [5, 1],
        "gram": {"colors": 4, "diagonal": [1, 1], "off_diagonal": [-1, 3]},
        "frontier_policy": "canonical plus every one-coordinate length-plus-two target",
        "kernels": ledgers,
        "kernel_total": len(ledgers),
        "physical_total": sum(row["physical_rows"] for row in ledgers),
        "orbit_total": len(records),
        "certified_total": sum(record["certified"] for record in records),
        "residual_total": len(residual_keys),
        "frontiers_per_residual": 11,
        "frontier_target_total": 11 * len(residual_keys),
        "residual_keys": residual_keys,
        "full_theorem": not residual_keys,
        "records": records,
    }


def load_fixture():
    raw = FIXTURE.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), "census fixture is not canonical JSON")
    return payload, raw


def audit(payload=None):
    fixture, raw = load_fixture() if payload is None else (payload, canonical_bytes(payload))
    generated = regenerate()
    require(fixture == generated, "census fixture differs from exact regeneration")
    require(fixture["kernel_total"] == 84, "kernel total changed")
    require(sum(row["orbit_size"] for row in fixture["records"]) == fixture["physical_total"],
            "orbits do not partition physical rows")
    require(fixture["certified_total"] + fixture["residual_total"] == fixture["orbit_total"],
            "sieve partition changed")
    require(fixture["frontier_target_total"] == 11 * fixture["residual_total"],
            "frontier ledger changed")
    require(fixture["full_theorem"] == (fixture["residual_total"] == 0),
            "theorem status is inconsistent")
    return fixture, hashlib.sha256(raw).hexdigest()


def expect_rejected(action, label):
    try:
        action()
    except (KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


def hostile_checks():
    baseline = regenerate()
    mutations = []
    def add(label, mutation):
        value = deepcopy(baseline)
        mutation(value)
        mutations.append((label, value))
    add("deleted orbit", lambda x: x["records"].pop())
    add("forged count", lambda x: x.__setitem__("physical_total", 0))
    add("forged cost", lambda x: x["records"][-1].__setitem__("minimum_rational_upper", [0, 1]))
    add("lost residual", lambda x: x["residual_keys"].pop() if x["residual_keys"] else x.__setitem__("residual_total", 1))
    add("promoted theorem", lambda x: x.__setitem__("full_theorem", True))
    for label, value in mutations:
        expect_rejected(lambda value=value: audit(value), label)
    expect_rejected(lambda: source_kernels("0" * 64), "source digest")
    return len(mutations) + 1


def report(payload, digest, mutations):
    return "\n".join((
        "rank-six order-five tetrahedral census: exact audit passed",
        f"kernels={payload['kernel_total']} physical={payload['physical_total']} orbits={payload['orbit_total']}",
        f"tetra_certified={payload['certified_total']} residual={payload['residual_total']}",
        f"canonical_plus_frontier_targets={payload['frontier_target_total']}",
        f"full_theorem={str(payload['full_theorem']).lower()}",
        f"fixture_sha256={digest}",
        f"rejected_hostile_mutations={mutations}",
    )) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-fixture", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    if args.write_fixture:
        require(FIXTURE.parent.is_dir(), "fixture directory missing")
        FIXTURE.write_bytes(canonical_bytes(regenerate()))
        print(hashlib.sha256(FIXTURE.read_bytes()).hexdigest())
        return
    payload, digest = audit()
    mutations = hostile_checks()
    output = report(payload, digest, mutations)
    if sys.flags.optimize == 0 and not args.emit:
        completed = subprocess.run([sys.executable, "-O", __file__, "--emit"],
                                   check=False, capture_output=True, text=True)
        require(completed.returncode == 0 and completed.stdout == output,
                "normal and optimized verifier output differ")
    sys.stdout.write(output)


if __name__ == "__main__":
    main()
