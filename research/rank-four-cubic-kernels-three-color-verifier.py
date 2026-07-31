#!/usr/bin/env python3
"""Fail-closed physical-row and exact three-color sieve for kernels 13-15,17."""

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "rank-four-cubic-kernels-three-color-sieve.json"
PAIRS = tuple(combinations(range(6), 2))
PAIR_NAMES = tuple(f"{u}{v}" for u, v in PAIRS)
KERNELS = {
    13: (0, 0, 0, 1, 2, 0, 1, 1, 1, 2, 1, 0, 0, 0, 0),
    14: (0, 0, 0, 1, 2, 0, 1, 2, 0, 2, 0, 1, 0, 0, 0),
    15: (0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0),
    17: (0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0),
}
EXPECTED_PHYSICAL = (288, 216, 384, 512)
EXPECTED_AUTOMORPHISMS = (4, 6, 4, 12)
EXPECTED_ORBITS = (102, 56, 144, 74)
EXPECTED_CERTIFIED = 359
EXPECTED_RESIDUAL = 17
EXPECTED_SHA256 = "531dfd4fc75703e01a57e5c030a374d7e563a566679d0b1618c5e4c9837997ed"
ROOT_LEFT = Fraction(93, 1000)
ROOT_RIGHT = Fraction(94, 1000)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def polynomial(value):
    return value ** 3 - 27 * value ** 2 + 99 * value - 9


def root_interval():
    require(polynomial(ROOT_LEFT) < 0 < polynomial(ROOT_RIGHT),
            "algebraic root is not bracketed")
    require(3 * ROOT_RIGHT ** 2 - 54 * ROOT_RIGHT + 99 > 0,
            "algebraic root uniqueness check failed")
    return ROOT_LEFT, ROOT_RIGHT


def sign_algebraic(rational, coefficient):
    """Return the exact sign of rational + coefficient*a."""
    rational = Fraction(rational)
    coefficient = int(coefficient)
    if coefficient == 0:
        return (rational > 0) - (rational < 0)
    left, right = root_interval()
    for _ in range(256):
        low = rational + coefficient * (left if coefficient > 0 else right)
        high = rational + coefficient * (right if coefficient > 0 else left)
        if low > 0:
            return 1
        if high < 0:
            return -1
        middle = (left + right) / 2
        value = polynomial(middle)
        if value < 0:
            left = middle
        elif value > 0:
            right = middle
        else:
            require(rational + coefficient * middle == 0,
                    "unexpected rational algebraic root")
            return 0
    raise RuntimeError("algebraic comparison did not separate")


def compare_cost(left, right):
    return sign_algebraic(left[0] - right[0], left[1] - right[1])


def relabel(row, permutation):
    require(len(row) == len(PAIRS), "row width changed")
    require(tuple(sorted(permutation)) == tuple(range(6)), "invalid permutation")
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in PAIRS)


def automorphisms(kernel):
    return tuple(permutation for permutation in permutations(range(6))
                 if relabel(kernel, permutation) == kernel)


def canonical_row(row, group):
    return min(relabel(row, permutation) for permutation in group)


def orbit_members(row, group):
    return tuple(sorted({relabel(row, permutation) for permutation in group}))


def bundle_record(kernel, row):
    result = []
    for edge, multiplicity, odd in zip(PAIR_NAMES, kernel, row):
        require(0 <= odd <= multiplicity, "invalid physical odd count")
        if multiplicity:
            result.append({"edge": edge, "multiplicity": multiplicity,
                           "odd": odd, "even": multiplicity - odd})
        else:
            require(odd == 0, "nonedge has odd incidence")
    return result


def bundle_cost(multiplicity, odd):
    table = {
        (1, 0): (Fraction(2, 3), 0),
        (1, 1): (Fraction(1, 3), 0),
        (2, 0): (Fraction(4, 3), 0),
        (2, 1): (Fraction(1), 0),
        (2, 2): (Fraction(1, 3), 1),
    }
    require((multiplicity, odd) in table, "unsupported bundle state")
    return table[multiplicity, odd]


def coloring_cost(kernel, row, coloring):
    rational = Fraction(0)
    coefficient = 0
    for (u, v), multiplicity, odd in zip(PAIRS, kernel, row):
        if not multiplicity:
            require(odd == 0, "nonedge has odd incidence")
            continue
        if coloring[u] == coloring[v]:
            if odd:
                return None
            continue
        term_rational, term_coefficient = bundle_cost(multiplicity, odd)
        rational += term_rational
        coefficient += term_coefficient
    return rational, coefficient


def minimum_cost(kernel, row):
    best = None
    witnesses = []
    for coloring in product(range(3), repeat=6):
        cost = coloring_cost(kernel, row, coloring)
        if cost is None:
            continue
        relation = -1 if best is None else compare_cost(cost, best)
        if relation < 0:
            best = cost
            witnesses = [coloring]
        elif relation == 0:
            witnesses.append(coloring)
    require(best is not None, "row has no admissible three-coloring")
    return best, min(witnesses)


def regenerate_payload():
    ledgers = []
    records = []
    for number, kernel in KERNELS.items():
        group = automorphisms(kernel)
        physical = tuple(product(*(range(m + 1) for m in kernel)))
        representatives = tuple(sorted({canonical_row(row, group) for row in physical}))
        ledgers.append({
            "kernel": number,
            "code": list(kernel),
            "physical_rows": len(physical),
            "automorphisms": len(group),
            "orbits": len(representatives),
        })
        for row in representatives:
            best, witness = minimum_cost(kernel, row)
            records.append({
                "kernel": number,
                "row": list(row),
                "bundles": bundle_record(kernel, row),
                "automorphism_orbit": [list(member)
                                       for member in orbit_members(row, group)],
                "minimum_cost": [best[0].numerator, best[0].denominator, best[1]],
                "first_witness": list(witness),
                "sieve_residual": compare_cost(best, (Fraction(3), 0)) > 0,
            })
    residual_keys = [[record["kernel"], record["row"]]
                     for record in records if record["sieve_residual"]]
    return {
        "schema": "rank-four-cubic-kernels-three-color-sieve-v1",
        "scope": "finite physical-row/orbit fixture and equilateral three-color sieve only",
        "pair_order": list(PAIR_NAMES),
        "algebraic_parameter": {
            "symbol": "a",
            "definition": "3*tan(pi/18)^2",
            "minimal_polynomial": [1, -27, 99, -9],
            "isolating_interval": [[93, 1000], [94, 1000]],
        },
        "kernels": ledgers,
        "physical_row_total": sum(item["physical_rows"] for item in ledgers),
        "orbit_total": len(records),
        "certified_total": sum(not record["sieve_residual"] for record in records),
        "residual_total": len(residual_keys),
        "residual_keys": residual_keys,
        "records": records,
    }


def serialize(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"


def load_fixture():
    require(FIXTURE.is_file(), f"missing fixture: {FIXTURE}")
    with FIXTURE.open("r", encoding="ascii") as handle:
        fixture = json.load(handle)
    require(isinstance(fixture, dict), "fixture root is not an object")
    return fixture


def audit(payload=None, expected_digest=EXPECTED_SHA256, generated=None):
    fixture = load_fixture() if payload is None else payload
    if generated is None:
        generated = regenerate_payload()
    require(fixture == generated, "fixture differs from exact regeneration")
    require(tuple(item["physical_rows"] for item in fixture["kernels"])
            == EXPECTED_PHYSICAL, "physical-row ledger changed")
    require(tuple(item["automorphisms"] for item in fixture["kernels"])
            == EXPECTED_AUTOMORPHISMS, "automorphism ledger changed")
    require(tuple(item["orbits"] for item in fixture["kernels"])
            == EXPECTED_ORBITS, "orbit ledger changed")
    require(fixture["orbit_total"] == sum(EXPECTED_ORBITS), "orbit total changed")
    require(fixture["certified_total"] == EXPECTED_CERTIFIED,
            "certified total changed")
    require(fixture["residual_total"] == EXPECTED_RESIDUAL,
            "residual total changed")

    seen = set()
    covered = 0
    for record in fixture["records"]:
        require(set(record) == {"kernel", "row", "bundles", "automorphism_orbit",
                                "minimum_cost", "first_witness", "sieve_residual"},
                "record schema changed")
        kernel = KERNELS[record["kernel"]]
        group = automorphisms(kernel)
        row = tuple(record["row"])
        require(row == canonical_row(row, group), "record row is not canonical")
        require(record["bundles"] == bundle_record(kernel, row),
                "bundle reconstruction changed")
        members = orbit_members(row, group)
        require(record["automorphism_orbit"] == [list(member) for member in members],
                "automorphism orbit changed")
        require((record["kernel"], row) not in seen, "duplicate orbit record")
        seen.add((record["kernel"], row))
        covered += len(members)
    require(covered == fixture["physical_row_total"],
            "orbits do not cover every physical row exactly once")
    require(len(seen) == fixture["orbit_total"], "orbit records are not unique")

    digest = hashlib.sha256(serialize(fixture).encode("ascii")).hexdigest()
    require(expected_digest == EXPECTED_SHA256, "digest policy was mutated")
    require(digest == expected_digest, "fixture digest changed")
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
    add("duplicated orbit", lambda value: value["records"].append(
        deepcopy(value["records"][-1])))
    add("noncanonical row", lambda value: value["records"][-1]["row"].reverse())
    add("changed bundle count", lambda value: value["records"][0]["bundles"][0]
        .__setitem__("odd", 1))
    add("lost orbit member", lambda value: value["records"][-1]
        ["automorphism_orbit"].pop())
    add("changed exact minimum", lambda value: value["records"][0]
        .__setitem__("minimum_cost", [1, 3, 0]))
    add("changed witness", lambda value: value["records"][0]
        ["first_witness"].__setitem__(0, 1))
    add("changed residual key", lambda value: value["residual_keys"].pop())
    add("changed polynomial", lambda value: value["algebraic_parameter"]
        ["minimal_polynomial"].__setitem__(1, -26))
    add("changed pair order", lambda value: value["pair_order"].reverse())
    for label, candidate in mutations:
        expect_rejected(lambda candidate=candidate: audit(candidate, generated=baseline), label)
    expect_rejected(lambda: audit(baseline, "0" * 64, baseline), "digest mutation")
    return len(mutations) + 1


def optimized_output():
    command = [sys.executable, "-O", str(Path(__file__).resolve()), "--emit"]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O verifier failed")
    return completed.stdout


def report(digest, mutations):
    fixture = load_fixture()
    physical = ",".join(str(item["physical_rows"]) for item in fixture["kernels"])
    groups = ",".join(str(item["automorphisms"]) for item in fixture["kernels"])
    orbits = ",".join(str(item["orbits"]) for item in fixture["kernels"])
    return "\n".join((
        "cubic kernels 13-15,17 physical-row/orbit sieve: audit passed",
        f"physical_rows_by_kernel: {physical} (total {fixture['physical_row_total']})",
        f"automorphism_orders_by_kernel: {groups}",
        f"automorphism_orbits_by_kernel: {orbits} (total {fixture['orbit_total']})",
        f"sieve_partition: {fixture['certified_total']} certified + {fixture['residual_total']} residual",
        f"fixture_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-fixture", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    if args.write_fixture:
        require(FIXTURE.parent.is_dir(), "fixture directory is missing")
        FIXTURE.write_text(serialize(regenerate_payload()), encoding="ascii")
        print(hashlib.sha256(FIXTURE.read_bytes()).hexdigest())
        return 0
    digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 11, "hostile mutation count changed")
    output = report(digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
