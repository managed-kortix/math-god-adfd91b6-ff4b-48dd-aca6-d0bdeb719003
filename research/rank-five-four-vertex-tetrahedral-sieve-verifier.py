#!/usr/bin/env python3
"""Exact fail-closed census and coarse tetrahedral sieve for rank five."""

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
KERNEL_FIXTURE = HERE / "fixtures" / "rank-five-kernels.json"
FIXTURE = HERE / "fixtures" / "rank-five-four-vertex-tetrahedral-sieve.json"
KERNEL_FIXTURE_SHA256 = "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884"
EXPECTED_SHA256 = "0b8ded3f4dbe0b8de916c085393c5f470bbaf8961deddf4305396e15f1d45588"
PAIRS = tuple(combinations(range(4), 2))
PAIR_NAMES = tuple(f"{u}{v}" for u, v in PAIRS)
EXPECTED_PHYSICAL = (108, 108, 108, 64, 96, 81, 96, 72, 128, 144, 144, 72, 60)
EXPECTED_AUTOMORPHISMS = (2, 2, 1, 4, 1, 8, 1, 2, 4, 2, 8, 1, 2)
EXPECTED_ORBITS = (63, 63, 108, 30, 96, 21, 96, 48, 56, 84, 39, 72, 45)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def load_json(path):
    try:
        raw = path.read_bytes()
        value = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot load fixture {path}: {error}") from error
    require(isinstance(value, dict), f"fixture root is not an object: {path}")
    return value, raw


@lru_cache(maxsize=1)
def kernels():
    payload, raw = load_json(KERNEL_FIXTURE)
    require(hashlib.sha256(raw).hexdigest() == KERNEL_FIXTURE_SHA256,
            "rank-five kernel source digest changed")
    rows = tuple(tuple(record["code"]) for record in payload.get("kernels", ())
                 if record.get("n") == 4)
    require(len(rows) == 13, "rank-five four-vertex kernel count changed")
    return rows


def relabel(row, permutation):
    require(len(row) == 6, "row width changed")
    require(tuple(sorted(permutation)) == tuple(range(4)), "invalid permutation")
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in PAIRS)


def automorphisms(kernel):
    return tuple(permutation for permutation in permutations(range(4))
                 if relabel(kernel, permutation) == kernel)


def canonical_row(row, group):
    return min(relabel(row, permutation) for permutation in group)


def coarse_cost(kernel, row, coloring):
    """Rational upper bound for the regular-tetrahedron Gram certificate."""
    total = Fraction(0)
    for multiplicity, odd, (u, v) in zip(kernel, row, PAIRS):
        require(0 <= odd <= multiplicity, "invalid physical odd count")
        if coloring[u] == coloring[v]:
            if odd:
                return None
            continue
        # Tetrahedral correlation is -1/3.  One odd path may be direct and
        # costs 1/2.  Further odd paths have length at least three and cost
        # <1/6; even paths have length at least two and cost <3/5.
        if odd:
            total += Fraction(1, 2) + (odd - 1) * Fraction(1, 6)
        total += (multiplicity - odd) * Fraction(3, 5)
    return total


def minimum_record(kernel_number, kernel, row, orbit_size):
    candidates = []
    for coloring in product(range(4), repeat=4):
        cost = coarse_cost(kernel, row, coloring)
        if cost is not None:
            candidates.append((cost, coloring))
    require(candidates, "physical row has no admissible tetrahedral coloring")
    bound, witness = min(candidates)
    certified = bound <= 4
    return {
        "kernel": kernel_number,
        "row": list(row),
        "orbit_size": orbit_size,
        "minimum_rational_upper": [bound.numerator, bound.denominator],
        "first_coloring": list(witness),
        "certified": certified,
    }


@lru_cache(maxsize=1)
def regenerate_payload():
    ledgers = []
    records = []
    for offset, kernel in enumerate(kernels()):
        group = automorphisms(kernel)
        orbit_sizes = {}
        for row in product(*(range(value + 1) for value in kernel)):
            representative = canonical_row(row, group)
            orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
        kernel_records = [minimum_record(offset + 4, kernel, row, orbit_sizes[row])
                          for row in sorted(orbit_sizes)]
        records.extend(kernel_records)
        ledgers.append({
            "kernel": offset + 4,
            "code": list(kernel),
            "physical_rows": sum(orbit_sizes.values()),
            "automorphisms": len(group),
            "orbits": len(orbit_sizes),
            "certified": sum(record["certified"] for record in kernel_records),
            "residual": sum(not record["certified"] for record in kernel_records),
        })
    residual_keys = [[record["kernel"], record["row"]]
                     for record in records if not record["certified"]]
    return {
        "schema": "rank-five-four-vertex-tetrahedral-sieve-v1",
        "source_kernel_fixture_sha256": KERNEL_FIXTURE_SHA256,
        "pair_order": list(PAIR_NAMES),
        "budget": [4, 1],
        "color_gram": {"colors": 4, "diagonal": [1, 1], "off_diagonal": [-1, 3]},
        "coarse_costs": {
            "first_odd": [1, 2],
            "additional_odd_strict_upper": [1, 6],
            "even_strict_upper": [3, 5],
        },
        "kernels": ledgers,
        "physical_total": sum(row["physical_rows"] for row in ledgers),
        "orbit_total": len(records),
        "certified_total": sum(record["certified"] for record in records),
        "residual_total": len(residual_keys),
        "residual_keys": residual_keys,
        "full_theorem": False,
        "theorem_status": "residual_open",
        "records": records,
    }


def audit(payload=None, expected_digest=EXPECTED_SHA256):
    if payload is None:
        fixture, raw = load_json(FIXTURE)
        require(raw == canonical_bytes(fixture), "sieve fixture is not canonical JSON")
    else:
        fixture = payload
    generated = regenerate_payload()
    require(fixture == generated, "sieve fixture differs from exact regeneration")
    require(tuple(row["physical_rows"] for row in fixture["kernels"]) == EXPECTED_PHYSICAL,
            "physical-row ledger changed")
    require(tuple(row["automorphisms"] for row in fixture["kernels"]) == EXPECTED_AUTOMORPHISMS,
            "automorphism ledger changed")
    require(tuple(row["orbits"] for row in fixture["kernels"]) == EXPECTED_ORBITS,
            "orbit ledger changed")
    require(fixture["physical_total"] == 1281, "physical total changed")
    require(fixture["orbit_total"] == 821, "orbit total changed")
    require(fixture["certified_total"] == 808, "certified total changed")
    require(fixture["residual_total"] == 13, "residual total changed")
    require(sum(record["orbit_size"] for record in fixture["records"]) == 1281,
            "orbit sizes do not partition the physical census")
    keys = [(record["kernel"], tuple(record["row"])) for record in fixture["records"]]
    require(len(keys) == len(set(keys)) == 821, "orbit keys are not unique and exhaustive")
    require(fixture["full_theorem"] is False and fixture["theorem_status"] == "residual_open",
            "open residual was promoted to a full theorem")
    digest = hashlib.sha256(canonical_bytes(fixture)).hexdigest()
    require(expected_digest == EXPECTED_SHA256, "digest policy was mutated")
    require(digest == expected_digest, "sieve fixture digest changed")
    return digest


def expect_rejected(action, label):
    try:
        action()
    except (IndexError, KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    baseline = regenerate_payload()
    mutations = []

    def add(label, mutate):
        candidate = deepcopy(baseline)
        mutate(candidate)
        mutations.append((label, candidate))

    add("deleted orbit", lambda value: value["records"].pop())
    add("changed orbit size", lambda value: value["records"][0].__setitem__("orbit_size", 99))
    add("forged cost", lambda value: value["records"][-1]
        .__setitem__("minimum_rational_upper", [0, 1]))
    add("changed coloring", lambda value: value["records"][0]["first_coloring"].__setitem__(0, 3))
    add("lost residual", lambda value: value["residual_keys"].pop())
    add("promoted theorem", lambda value: value.__setitem__("full_theorem", True))
    add("closed status", lambda value: value.__setitem__("theorem_status", "proved"))
    add("changed budget", lambda value: value.__setitem__("budget", [5, 1]))
    for label, candidate in mutations:
        expect_rejected(lambda candidate=candidate: audit(candidate), label)
    expect_rejected(lambda: audit(baseline, "0" * 64), "digest mutation")
    return len(mutations) + 1


def report(digest, mutations):
    return "\n".join((
        "rank-five four-vertex exact census and tetrahedral sieve: audit passed",
        "physical_rows_by_kernel: " + ",".join(map(str, EXPECTED_PHYSICAL)) + " (total 1281)",
        "automorphism_orbits_by_kernel: " + ",".join(map(str, EXPECTED_ORBITS)) + " (total 821)",
        "sieve_partition: 808 certified + 13 residual",
        "budget: 4; Gram: regular tetrahedron; arithmetic: Fraction upper bounds",
        "full_theorem: false (residual_open)",
        f"fixture_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


def optimized_output():
    completed = subprocess.run([sys.executable, "-O", str(Path(__file__).resolve()), "--emit"],
                               check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O verifier failed")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-fixture", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    if args.write_fixture:
        require(FIXTURE.parent.is_dir(), "fixture directory is missing")
        FIXTURE.write_bytes(canonical_bytes(regenerate_payload()))
        print(hashlib.sha256(FIXTURE.read_bytes()).hexdigest())
        return 0
    digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 9, "hostile mutation count changed")
    output = report(digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
