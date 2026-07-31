#!/usr/bin/env python3
"""Fail-closed exact three-color sieve for five-vertex rank-four kernels."""

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
FIXTURE = HERE / "fixtures" / "rank-four-five-vertex-three-color-sieve.json"
ORBIT_FIXTURE = HERE / "fixtures" / "rank-four-five-vertex-orbits.json"
PAIRS = tuple(combinations(range(5), 2))
PAIR_NAMES = tuple(f"{u}{v}" for u, v in PAIRS)
KERNELS = (
    (0, 0, 1, 2, 1, 0, 2, 2, 0, 0),
    (0, 0, 1, 2, 1, 1, 1, 1, 1, 0),
    (0, 0, 1, 2, 1, 1, 1, 2, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 0, 1, 1),
)
EXPECTED_PHYSICAL = (108, 192, 144, 256)
EXPECTED_AUTOMORPHISMS = (2, 2, 1, 8)
EXPECTED_ORBITS = (63, 120, 144, 51)
EXPECTED_OLD_ORBIT_SHA256 = "d43a7c9e1e50a3381043a0c6c5b4ed019c5c858264f0f5b572c5a28a326c8245"
EXPECTED_SHA256 = "cca0916cba1071a06f44e3e09712f3fc2d0b95709f3f8976ef1573059e450875"
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
    # P'(x)=3x^2-54x+99 is positive throughout [0,1].
    require(3 * ROOT_RIGHT ** 2 - 54 * ROOT_RIGHT + 99 > 0,
            "root uniqueness derivative check failed")
    return ROOT_LEFT, ROOT_RIGHT


def sign_algebraic(rational, coefficient):
    """Sign of rational + coefficient*a for the isolated root a."""
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
        if low == high == 0:
            return 0
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
    require(tuple(sorted(permutation)) == tuple(range(5)), "invalid permutation")
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in PAIRS)


def automorphisms(kernel):
    return tuple(permutation for permutation in permutations(range(5))
                 if relabel(kernel, permutation) == kernel)


def canonical_row(kernel, row):
    return min(relabel(row, permutation) for permutation in automorphisms(kernel))


def all_rows():
    ledgers = []
    records = []
    for index, kernel in enumerate(KERNELS):
        physical = tuple(product(*(range(m + 1) for m in kernel)))
        representatives = tuple(sorted({canonical_row(kernel, row) for row in physical}))
        ledgers.append({
            "kernel": index + 9,
            "code": list(kernel),
            "physical_rows": len(physical),
            "automorphisms": len(automorphisms(kernel)),
            "orbits": len(representatives),
        })
        records.extend((index + 9, kernel, row) for row in representatives)
    return ledgers, records


def bundle_cost(multiplicity, odd):
    """Canonical bichromatic cost as p+q*a; a=3*tan(pi/18)^2."""
    table = {
        (1, 0): (Fraction(2, 3), 0),
        (1, 1): (Fraction(1, 3), 0),
        (2, 0): (Fraction(4, 3), 0),
        (2, 1): (Fraction(1), 0),
        # Two odd paths cannot both be direct in a simple subdivision.  Their
        # worst physical lengths are therefore one and three, not one and one.
        (2, 2): (Fraction(1, 3), 1),
    }
    require((multiplicity, odd) in table, "unsupported physical bundle state")
    return table[multiplicity, odd]


def coloring_cost(kernel, row, coloring):
    rational = Fraction(0)
    coefficient = 0
    for (u, v), multiplicity, odd in zip(PAIRS, kernel, row):
        require(0 <= odd <= multiplicity, "invalid physical odd count")
        if multiplicity == 0:
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


def minimum_record(kernel_number, kernel, row, old_residuals):
    best = None
    witnesses = []
    for coloring in product(range(3), repeat=5):
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
    witness = min(witnesses)
    residual = compare_cost(best, (Fraction(3), 0)) > 0
    return {
        "kernel": kernel_number,
        "row": list(row),
        "minimum_cost": [best[0].numerator, best[0].denominator, best[1]],
        "first_witness": list(witness),
        "sieve_residual": residual,
        "in_old_96": (kernel_number, row) in old_residuals,
    }


def load_json(path):
    require(path.is_file(), f"missing fixture: {path}")
    with path.open("r", encoding="ascii") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"fixture root is not an object: {path}")
    return value


def old_residual_keys():
    raw = ORBIT_FIXTURE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_OLD_ORBIT_SHA256,
            "the 96-row source fixture digest changed")
    fixture = load_json(ORBIT_FIXTURE)
    require(fixture.get("residual_total") == 96, "source residual count changed")
    keys = frozenset((record["kernel"], tuple(record["row"]))
                     for record in fixture.get("residuals", ()))
    require(len(keys) == 96, "source residual keys are not unique and exact")
    return keys


def regenerate_payload():
    old_residuals = old_residual_keys()
    ledgers, rows = all_rows()
    records = [minimum_record(number, kernel, row, old_residuals)
               for number, kernel, row in rows]
    residual_keys = [[record["kernel"], record["row"]]
                     for record in records if record["sieve_residual"]]
    intersection_keys = [[record["kernel"], record["row"]]
                         for record in records
                         if record["sieve_residual"] and record["in_old_96"]]
    return {
        "schema": "rank-four-five-vertex-three-color-sieve-v1",
        "pair_order": list(PAIR_NAMES),
        "algebraic_parameter": {
            "symbol": "a",
            "definition": "3*tan(pi/18)^2",
            "minimal_polynomial": [1, -27, 99, -9],
            "isolating_interval": [[93, 1000], [94, 1000]],
        },
        "source_orbit_fixture_sha256": EXPECTED_OLD_ORBIT_SHA256,
        "kernels": ledgers,
        "orbit_total": len(records),
        "certified_total": sum(not record["sieve_residual"] for record in records),
        "residual_total": len(residual_keys),
        "old_96_intersection_total": len(intersection_keys),
        "residual_keys": residual_keys,
        "old_96_intersection_keys": intersection_keys,
        "records": records,
    }


def serialize(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"


def audit(payload=None, expected_digest=EXPECTED_SHA256):
    fixture = load_json(FIXTURE) if payload is None else payload
    generated = regenerate_payload()
    require(fixture == generated, "sieve fixture differs from exact regeneration")
    require(tuple(row["physical_rows"] for row in fixture["kernels"])
            == EXPECTED_PHYSICAL, "physical-row ledger changed")
    require(tuple(row["automorphisms"] for row in fixture["kernels"])
            == EXPECTED_AUTOMORPHISMS, "automorphism ledger changed")
    require(tuple(row["orbits"] for row in fixture["kernels"])
            == EXPECTED_ORBITS, "orbit ledger changed")
    require(fixture["orbit_total"] == 378, "orbit total changed")
    require(fixture["certified_total"] == 370, "certified total changed")
    require(fixture["residual_total"] == 8, "residual total changed")
    require(fixture["old_96_intersection_total"] == 2,
            "old-96 intersection total changed")
    keys = [(record["kernel"], tuple(record["row"])) for record in fixture["records"]]
    require(len(keys) == len(set(keys)) == 378, "record keys are not exhaustive")
    digest = hashlib.sha256(serialize(fixture).encode("ascii")).hexdigest()
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

    add("deleted record", lambda value: value["records"].pop())
    add("changed odd-odd cost", lambda value: value["records"][0]
        .__setitem__("minimum_cost", [2, 3, 0]))
    add("changed witness", lambda value: value["records"][0]
        ["first_witness"].__setitem__(0, 2))
    add("promoted residual", lambda value: value["records"][0]
        .__setitem__("sieve_residual", True))
    add("lost residual key", lambda value: value["residual_keys"].pop())
    add("forged intersection", lambda value: value["old_96_intersection_keys"].append([9, [0] * 10]))
    add("changed polynomial", lambda value: value["algebraic_parameter"]
        ["minimal_polynomial"].__setitem__(1, -26))
    add("changed pair order", lambda value: value["pair_order"].reverse())
    for label, candidate in mutations:
        expect_rejected(lambda candidate=candidate: audit(candidate), label)
    expect_rejected(lambda: audit(baseline, "0" * 64), "digest mutation")
    return len(mutations) + 1


def optimized_output():
    command = [sys.executable, "-O", str(Path(__file__).resolve()), "--emit"]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O verifier failed")
    return completed.stdout


def report(digest, mutations):
    return "\n".join((
        "five-vertex exact coarse three-color DNN sieve: audit passed",
        "physical_rows_by_kernel: 108,192,144,256 (total 700)",
        "automorphism_orbits_by_kernel: 63,120,144,51 (total 378)",
        "sieve_partition: 370 certified + 8 residual",
        "old_96_intersection: 2",
        "odd_odd_bundle_cost: 1/3+a, a=3*tan(pi/18)^2",
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
    require(mutations == 9, "hostile mutation count changed")
    output = report(digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
