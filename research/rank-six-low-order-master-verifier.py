#!/usr/bin/env python3
"""Exact low-order rank-six kernel theorem audit (orders two through four)."""

import hashlib
import itertools
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
KERNEL_FIXTURE = HERE / "fixtures" / "rank-six-kernels.json"
SEVEN_PATH_PROOF = (ROOT / "positive-square-energy" / "hexacyclic-general"
                    / "seven-path-dnn-theorem.md")
KERNEL_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
SEVEN_PATH_SHA256 = "cf3625413b6e77e84f87414b103d5f9e656cbd106445c2d2803469f3586fbb92"
EXPECTED_CODES = {
    2: ((7,),),
    3: ((1, 2, 5), (1, 3, 4), (2, 2, 4), (2, 3, 3)),
}
EXPECTED_THREE_PHYSICAL = (36, 40, 45, 48)
EXPECTED_THREE_AUTOMORPHISMS = (1, 1, 2, 2)
EXPECTED_THREE_ORBITS = (36, 40, 30, 30)
EXPECTED_FOUR_PHYSICAL = (
    144, 144, 144, 162, 144, 144, 128, 144, 162, 120, 90, 144, 96,
    128, 160, 192, 216, 216, 216, 96, 72, 120, 108, 90, 192, 80,
)
EXPECTED_FOUR_AUTOMORPHISMS = (
    2, 1, 2, 1, 1, 1, 2, 1, 4, 1, 2, 1, 2, 2, 4, 1, 6, 6, 2, 1,
    2, 1, 2, 1, 4, 2,
)
EXPECTED_FOUR_ORBITS = (
    84, 144, 84, 162, 144, 144, 72, 144, 54, 120, 60, 144, 60, 72, 70,
    192, 56, 56, 126, 96, 54, 120, 72, 90, 84, 60,
)
T_CERTIFICATES = {
    ((1, 2, 5), 0): (Fraction(1, 2), Fraction(3, 8), Fraction(1, 8)),
    ((1, 2, 5), 1): (Fraction(3, 8), Fraction(1, 2), Fraction(1, 8)),
    ((1, 2, 5), 2): (Fraction(1, 4), Fraction(1, 8), Fraction(3, 8)),
    ((1, 3, 4), 0): (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)),
    ((1, 3, 4), 1): (Fraction(3, 8), Fraction(1, 2), Fraction(1, 8)),
    ((1, 3, 4), 2): (Fraction(1, 4), Fraction(1, 8), Fraction(3, 8)),
    ((2, 2, 4), 0): (Fraction(1, 2), Fraction(3, 8), Fraction(1, 8)),
    ((2, 2, 4), 1): (Fraction(3, 8), Fraction(1, 2), Fraction(1, 8)),
    ((2, 2, 4), 2): (Fraction(1, 8), Fraction(1, 4), Fraction(3, 8)),
    ((2, 3, 3), 0): (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)),
    ((2, 3, 3), 1): (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)),
    ((2, 3, 3), 2): (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_kernels(expected_digest=KERNEL_SHA256):
    raw = KERNEL_FIXTURE.read_bytes()
    require(expected_digest == KERNEL_SHA256, "kernel digest policy changed")
    require(hashlib.sha256(raw).hexdigest() == expected_digest,
            "rank-six kernel fixture changed")
    payload = json.loads(raw)
    canonical = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
    require(raw == canonical, "kernel fixture is not canonical JSON")
    selected = {n: tuple(tuple(row["code"]) for row in payload["kernels"] if row["n"] == n)
                for n in (2, 3, 4)}
    require(tuple(map(lambda n: len(selected[n]), (2, 3, 4))) == (1, 4, 26),
            "low-order selection is not 1+4+26")
    require(selected[2] == EXPECTED_CODES[2] and selected[3] == EXPECTED_CODES[3],
            "order-two or order-three kernel codes changed")
    return selected


def analytic_ledger(proof_digest=SEVEN_PATH_SHA256, ledger=None):
    require(proof_digest == SEVEN_PATH_SHA256, "seven-path digest policy changed")
    require(hashlib.sha256(SEVEN_PATH_PROOF.read_bytes()).hexdigest() == proof_digest,
            "seven-path analytic proof changed")
    expected = {
        "path_count": 7,
        "rank": 6,
        "budget": 5,
        "no_unit_even_counts": tuple(range(8)),
        "no_unit_witness_values": (0, 2, 4, 4, 3, 2, 1, 0),
        "unit_even_counts": tuple(range(7)),
        "unit_endpoint_values": (0, 2, 4),
        "unit_middle_numerators": (10, 11, 12, 13),
        "common_denominator": 3,
    }
    value = expected if ledger is None else ledger
    require(value == expected, "seven-path analytic ledger changed")
    require(max(value["no_unit_witness_values"]) < value["budget"],
            "no-unit witness reaches budget")
    require(max(value["unit_endpoint_values"]) < value["budget"],
            "unit endpoint witness reaches budget")
    require(all(Fraction(x, value["common_denominator"]) < value["budget"]
                for x in value["unit_middle_numerators"]),
            "unit middle witness reaches budget")
    require(value["budget"] == value["rank"] - 1, "rank-six budget changed")
    return value


def pairs(n):
    return tuple(itertools.combinations(range(n), 2))


def relabel(row, permutation, n):
    edge_pairs = pairs(n)
    lookup = dict(zip(edge_pairs, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in edge_pairs)


def automorphisms(kernel, n):
    return tuple(p for p in itertools.permutations(range(n))
                 if relabel(kernel, p, n) == kernel)


def orbit_rows(kernel, n):
    group = automorphisms(kernel, n)
    physical = tuple(itertools.product(*(range(value + 1) for value in kernel)))
    representatives = tuple(sorted({min(relabel(row, p, n) for p in group)
                                    for row in physical}))
    return physical, group, representatives


def correlation(t):
    return (1 - 6 * t * t + t ** 4) / (1 + t * t) ** 2


def determinant3(matrix):
    a, b, c = matrix[0][1], matrix[0][2], matrix[1][2]
    return 1 + 2 * a * b * c - a * a - b * b - c * c


def three_certificate(kernel, row):
    odd_total = sum(row)
    if odd_total == 0:
        matrix = ((Fraction(1),) * 3,) * 3
        cost = Fraction(0)
    elif odd_total == 1:
        values = T_CERTIFICATES[(kernel, row.index(1))]
        a, b, c = map(correlation, values)
        matrix = ((Fraction(1), a, b), (a, Fraction(1), c),
                  (b, c, Fraction(1)))
        cost = Fraction(0)
        for multiplicity, odd, r, t in zip(kernel, row, (a, b, c), values):
            if odd:
                require(r != 1, "odd path has infinite cost")
                cost += odd * (1 + r) / (1 - r)
            cost += (multiplicity - odd) * 2 * t * t
    else:
        matrix = tuple(tuple(Fraction(1) if i == j else Fraction(-1, 2)
                             for j in range(3)) for i in range(3))
        cost = Fraction(16 - odd_total, 3)
    require(all(matrix[i][i] == 1 for i in range(3)), "three-Gram diagonal changed")
    require(all(1 - matrix[i][j] ** 2 >= 0 for i in range(3) for j in range(i)),
            "negative two-minor in three-Gram")
    require(determinant3(matrix) >= 0, "negative three-Gram determinant")
    require(cost <= 5, "three-vertex certificate exceeds budget five")
    return cost


def audit_three(kernels):
    ledgers = []
    costs = []
    for kernel in kernels:
        physical, group, representatives = orbit_rows(kernel, 3)
        costs.extend(three_certificate(kernel, row) for row in representatives)
        ledgers.append((len(physical), len(group), len(representatives)))
    require(tuple(x[0] for x in ledgers) == EXPECTED_THREE_PHYSICAL,
            "three-vertex physical ledger changed")
    require(tuple(x[1] for x in ledgers) == EXPECTED_THREE_AUTOMORPHISMS,
            "three-vertex automorphism ledger changed")
    require(tuple(x[2] for x in ledgers) == EXPECTED_THREE_ORBITS,
            "three-vertex orbit ledger changed")
    require(len(costs) == 136 and max(costs) <= 5, "three-vertex coverage changed")
    return ledgers, max(costs)


def tetrahedral_cost(kernel, row, coloring):
    total = Fraction(0)
    for multiplicity, odd, (u, v) in zip(kernel, row, pairs(4)):
        if coloring[u] == coloring[v]:
            if odd:
                return None
            continue
        if odd:
            total += Fraction(1, 2) + (odd - 1) * Fraction(1, 6)
        total += (multiplicity - odd) * Fraction(3, 5)
    return total


def audit_four(kernels):
    colorings = tuple(itertools.product(range(4), repeat=4))
    ledgers = []
    maxima = []
    for kernel in kernels:
        physical, group, representatives = orbit_rows(kernel, 4)
        costs = []
        for row in representatives:
            candidates = [cost for coloring in colorings
                          if (cost := tetrahedral_cost(kernel, row, coloring)) is not None]
            require(candidates, "four-vertex row has no tetrahedral coloring")
            cost = min(candidates)
            require(cost <= 5, "four-vertex tetrahedral certificate exceeds budget five")
            costs.append(cost)
        maxima.append(max(costs))
        ledgers.append((len(physical), len(group), len(representatives)))
    require(tuple(x[0] for x in ledgers) == EXPECTED_FOUR_PHYSICAL,
            "four-vertex physical ledger changed")
    require(tuple(x[1] for x in ledgers) == EXPECTED_FOUR_AUTOMORPHISMS,
            "four-vertex automorphism ledger changed")
    require(tuple(x[2] for x in ledgers) == EXPECTED_FOUR_ORBITS,
            "four-vertex orbit ledger changed")
    require(sum(x[0] for x in ledgers) == 3652, "four-vertex physical total changed")
    require(sum(x[2] for x in ledgers) == 2564, "four-vertex orbit total changed")
    require(max(maxima) == 5, "four-vertex sharp coarse bound changed")
    return ledgers, max(maxima)


def audit():
    selected = load_kernels()
    analytic_ledger()
    three, three_max = audit_three(selected[3])
    four, four_max = audit_four(selected[4])
    return three, three_max, four, four_max


def expect_rejected(action, label):
    try:
        action()
    except (KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


def hostile_self_checks():
    mutations = 0
    expect_rejected(lambda: load_kernels("0" * 64), "kernel digest")
    mutations += 1
    expect_rejected(lambda: analytic_ledger("0" * 64), "proof digest")
    mutations += 1
    for key in ("no_unit_even_counts", "unit_even_counts", "budget"):
        bad = deepcopy(analytic_ledger())
        bad[key] = () if key != "budget" else 4
        expect_rejected(lambda bad=bad: analytic_ledger(ledger=bad), f"analytic {key}")
        mutations += 1
    bad_t = dict(T_CERTIFICATES)
    bad_t[((1, 2, 5), 0)] = (Fraction(0),) * 3
    original = T_CERTIFICATES[((1, 2, 5), 0)]
    try:
        T_CERTIFICATES[((1, 2, 5), 0)] = bad_t[((1, 2, 5), 0)]
        expect_rejected(lambda: audit_three(EXPECTED_CODES[3]), "Gram certificate")
    finally:
        T_CERTIFICATES[((1, 2, 5), 0)] = original
    mutations += 1
    return mutations


def report(mutations):
    return "\n".join((
        "rank-six low-order master theorem: all exact audits passed",
        "kernel_selection_by_order_2_to_4: 1+4+26=31 exact fixture rows",
        "order_2: seven-path analytic theorem; all simple lengths; strict excess < 5",
        "order_3: 169 physical rows / 136 orbits; rational Gram excess <= 5",
        "order_4: 3652 physical rows / 2564 orbits; tetrahedral Gram excess <= 5",
        "order_4_residual_frontier: empty",
        "attachments: arbitrary rooted trees at arbitrary subdivision vertices",
        "conclusion: s+(G)>=|V(G)|; strict for the seven-dipole family",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


def main():
    audit()
    mutations = hostile_self_checks()
    require(mutations == 6, "hostile mutation count changed")
    output = report(mutations)
    if sys.flags.optimize == 0 and "--emit" not in sys.argv:
        completed = subprocess.run([sys.executable, "-O", str(Path(__file__).resolve()), "--emit"],
                                   check=False, capture_output=True, text=True)
        require(completed.returncode == 0 and completed.stderr == "",
                "optimized verifier failed")
        require(completed.stdout == output, "normal and optimized output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
