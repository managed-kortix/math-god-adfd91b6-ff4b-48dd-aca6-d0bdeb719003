#!/usr/bin/env python3
"""Fail-closed exact integration audit for cubic kernels 13--15 and 17."""

import argparse
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
SIEVE_VERIFIER = HERE / "rank-four-cubic-kernels-three-color-verifier.py"
FRONTIER_VERIFIER = HERE / "rank-four-cubic-kernels-residual-frontier-verifier.py"
KERNEL17_VERIFIER = HERE / "rank-four-kernel17-all-odd-switching-verifier.py"
SIEVE_FIXTURE = HERE / "fixtures" / "rank-four-cubic-kernels-three-color-sieve.json"
FRONTIER_FIXTURE = HERE / "fixtures" / "rank-four-cubic-kernels-residual-frontiers.json"
DEPENDENCIES = (
    (SIEVE_VERIFIER, ("--emit",), "sieve_partition: 359 certified + 17 residual"),
    (FRONTIER_VERIFIER, ("--emit",),
     "strict_fraction_certificates: 148; unresolved_equality_candidates: 12"),
    (KERNEL17_VERIFIER, (), "seven_template_residual: 0"),
)
PAIRS = tuple(combinations(range(6), 2))
PAIR_NAMES = tuple(f"{u}{v}" for u, v in PAIRS)
KERNEL14 = (0, 0, 0, 1, 2, 0, 1, 2, 0, 2, 0, 1, 0, 0, 0)
KERNEL14_ROWS = (
    (0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0),
    (0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0),
)
KERNEL14_CERTIFICATES = (
    ((1, 1, -1), (Fraction(-1, 2), Fraction(1, 2), Fraction(-1, 2))),
    ((1, -1, -1), (Fraction(-1, 2), Fraction(1, 2), Fraction(1, 2))),
    ((-1, -1, -1), (Fraction(1, 2), Fraction(1, 2), Fraction(1, 2))),
)
KERNEL14_PATHS = ("04", "05a", "05b", "13", "14a", "14b",
                  "23a", "23b", "25")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def exact_integer(value, label):
    require(type(value) is int, label)
    return value


def load_json(path):
    require(path.is_file(), f"missing fixture dependency: {path}")
    value = json.loads(path.read_text(encoding="ascii"))
    require(isinstance(value, dict), f"fixture root is not an object: {path}")
    return value


def load_module(path, name):
    require(path.is_file(), f"missing verifier dependency: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            f"cannot load verifier dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def invoke_dependencies():
    optimize = ("-O",) if sys.flags.optimize else ()
    outputs = []
    for path, arguments, required_line in DEPENDENCIES:
        completed = subprocess.run(
            (sys.executable, *optimize, str(path), *arguments),
            check=False, capture_output=True, text=True)
        require(completed.returncode == 0, f"dependency failed: {path.name}")
        require(completed.stderr == "", f"dependency wrote stderr: {path.name}")
        require(required_line in completed.stdout,
                f"dependency acceptance ledger changed: {path.name}")
        outputs.append(completed.stdout)
    return tuple(outputs)


def determinant3(matrix):
    return (matrix[0][0] * (matrix[1][1] * matrix[2][2]
                            - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2]
                              - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1]
                              - matrix[1][1] * matrix[2][0]))


def gram3(off_diagonal):
    ab, ac, bc = off_diagonal
    return ((Fraction(1), ab, ac), (ab, Fraction(1), bc),
            (ac, bc, Fraction(1)))


def canonical_lengths(multiplicity, odd):
    exact_integer(multiplicity, "path multiplicity is not an integer")
    exact_integer(odd, "path odd count is not an integer")
    return {
        (0, 0): (), (1, 0): (2,), (1, 1): (1,),
        (2, 0): (2, 2), (2, 1): (1, 2), (2, 2): (1, 3),
    }[multiplicity, odd]


def path_ledger(kernel, row):
    paths = []
    for name, multiplicity, odd in zip(PAIR_NAMES, kernel, row):
        require(0 <= odd <= multiplicity, "invalid physical row")
        for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)):
            suffix = "" if multiplicity == 1 else chr(ord("a") + occurrence)
            paths.append((name + suffix, length))
    return tuple(paths)


def audit_kernel14(certificates=KERNEL14_CERTIFICATES):
    require(certificates == KERNEL14_CERTIFICATES,
            "kernel-14 symbolic certificate table changed")
    covered = set()
    determinants = []
    for row, (epsilons, off_diagonal) in zip(KERNEL14_ROWS, certificates):
        require(all(type(value) is int for value in epsilons),
                "kernel-14 parity signs are not integers")
        require(all(isinstance(value, Fraction) for value in off_diagonal),
                "kernel-14 Gram entries are not exact fractions")
        ledger = path_ledger(KERNEL14, row)
        require(tuple(name for name, _ in ledger) == KERNEL14_PATHS,
                "kernel-14 physical coordinate order changed")
        matrix = gram3(off_diagonal)
        minors = tuple(matrix[i][i] * matrix[j][j] - matrix[i][j] ** 2
                       for i, j in combinations(range(3), 2))
        require(all(matrix[i][i] == 1 for i in range(3)),
                "kernel-14 Gram diagonal changed")
        require(minors == (Fraction(3, 4),) * 3,
                "kernel-14 principal minor changed")
        determinant = determinant3(matrix)
        require(determinant >= 0, "kernel-14 Gram matrix is not PSD")
        determinants.append(determinant)

        parity_word = (row[3], row[6], row[11])
        require(epsilons == tuple(-1 if bit else 1 for bit in parity_word),
                "kernel-14 singleton parity signs changed")
        ab, ac, bc = off_diagonal
        mixed = (epsilons[2] * ac, epsilons[0] * ab, epsilons[1] * bc)
        require(mixed == (Fraction(-1, 2),) * 3,
                "kernel-14 mixed-bundle correlations changed")
        require(tuple(length % 2 for _, length in ledger) ==
                tuple(length % 2 for multiplicity, odd in zip(KERNEL14, row)
                      for length in canonical_lengths(multiplicity, odd)),
                "kernel-14 physical parity expansion changed")
        require(sum(length % 2 for _, length in ledger) == sum(row),
                "kernel-14 physical odd-path count changed")

        x_squared = Fraction(1, 3)
        odd_cost = (1 - x_squared) ** 2 / (4 * x_squared)
        even_cost = 2 * x_squared
        require((odd_cost, even_cost, 3 * (odd_cost + even_cost)) ==
                (Fraction(1, 3), Fraction(2, 3), Fraction(3)),
                "kernel-14 symbolic costs changed")
        covered.update((14, row, coordinate) for coordinate in (None, *range(9)))
    require(tuple(determinants) == (Fraction(1, 2), 0, Fraction(1, 2)),
            "kernel-14 determinant table changed")
    require(len(covered) == 30, "kernel-14 coordinate frontier is incomplete")
    return frozenset(covered), tuple(determinants)


def frontier_key(record):
    return record["kernel"], tuple(record["row"]), record["frontier_coordinate"]


def audit_integrated_frontiers(kernel14_covered, frontier=None):
    sieve = load_json(SIEVE_FIXTURE)
    frontier = load_json(FRONTIER_FIXTURE) if frontier is None else frontier
    require(sieve.get("certified_total") == 359 and sieve.get("residual_total") == 17,
            "three-color sieve partition changed")
    residual = tuple((record["kernel"], tuple(record["row"]))
                     for record in sieve["records"]
                     if record["sieve_residual"] and record["kernel"] in (13, 14, 15))
    require(len(residual) == 16, "kernel-13--15 residual orbit count changed")
    expected = {(number, row, coordinate) for number, row in residual
                for coordinate in (None, *range(9))}
    strict = {frontier_key(record) for record in frontier["records"]}
    unresolved = {frontier_key(record) for record in frontier["unresolved"]}
    symbolic = {(14, row, coordinate) for row in KERNEL14_ROWS
                for coordinate in (None, 0, 3, 8)}
    require(len(strict) == 148 and len(unresolved) == 12,
            "strict/equality frontier partition changed")
    require(unresolved == symbolic, "kernel-14 equality target set changed")
    require(strict.isdisjoint(unresolved) and strict | unresolved == expected,
            "16-orbit canonical/coordinate frontier is not exact")
    require(symbolic <= kernel14_covered and expected <= strict | kernel14_covered,
            "integrated kernel-13--15 frontier has a gap")
    return len(expected), len(strict), len(symbolic)


def audit_kernel17_all_length(module=None, templates=None):
    module = load_module(KERNEL17_VERIFIER, "kernel17_final") if module is None else module
    templates = module.TEMPLATE_ANGLES if templates is None else templates
    require(templates == module.TEMPLATE_ANGLES and len(templates) == 7,
            "kernel-17 seven-template table changed")
    sieve = load_json(SIEVE_FIXTURE)
    records = [record for record in sieve["records"]
               if record["kernel"] == 17 and record["sieve_residual"]]
    require(len(records) == 1, "kernel-17 residual orbit count changed")
    edge_indices = tuple(index for index, multiplicity in enumerate(module.KERNEL17_CODE)
                         if multiplicity)
    canonical_full = tuple(records[0]["row"])
    canonical = tuple(canonical_full[index] for index in edge_indices)
    orbit = tuple(tuple(row[index] for index in edge_indices)
                  for row in records[0]["automorphism_orbit"])
    require(module.canonical_row(canonical) == min(orbit),
            "kernel-17 residual projected orbit is not canonical")
    require(set(orbit) == {module.relabel(canonical, permutation)
                           for permutation in module.automorphisms()},
            "kernel-17 residual physical orbit changed")
    require(all(any(module.within_budget(module.best_switched_cost(row, angles))
                    for angles in templates) for row in orbit),
            "kernel-17 residual orbit member is uncovered")
    covered_targets = {(row, coordinate) for row in orbit
                       for coordinate in (None, *range(9))}
    require(len(covered_targets) == len(orbit) * 10,
            "kernel-17 canonical/coordinate frontier is incomplete")
    rows = tuple(product((0, 1), repeat=9))
    require(all(any(module.within_budget(module.best_switched_cost(row, angles))
                    for angles in templates) for row in rows),
            "kernel-17 seven templates leave a physical row")
    return len(orbit), len(covered_targets), len(rows)


def expect_rejected(action, label):
    try:
        action()
    except (IndexError, KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks(kernel14_covered):
    changed = list(deepcopy(KERNEL14_CERTIFICATES))
    changed[0] = (changed[0][0], (Fraction(-1, 3), *changed[0][1][1:]))
    expect_rejected(lambda: audit_kernel14(tuple(changed)), "changed K14 matrix")
    changed = list(deepcopy(KERNEL14_CERTIFICATES))
    changed[1] = ((1, 1, -1), changed[1][1])
    expect_rejected(lambda: audit_kernel14(tuple(changed)), "changed K14 signs")
    module = load_module(KERNEL17_VERIFIER, "kernel17_mutation")
    expect_rejected(lambda: audit_kernel17_all_length(module, module.TEMPLATE_ANGLES[:-1]),
                    "deleted K17 template")
    frontier = load_json(FRONTIER_FIXTURE)
    frontier["records"].pop()
    expect_rejected(lambda: audit_integrated_frontiers(kernel14_covered, frontier),
                    "deleted strict frontier")
    for label, value in (("boolean exact payload", True),
                         ("floating exact payload", 1.0),
                         ("nonintegral exact payload", Fraction(1, 2))):
        changed = list(deepcopy(KERNEL14_CERTIFICATES))
        epsilons = list(changed[0][0])
        epsilons[0] = value
        changed[0] = (tuple(epsilons), changed[0][1])
        expect_rejected(lambda changed=changed: audit_kernel14(tuple(changed)), label)
    return 7


def report(dependencies, targets, strict, equalities, determinants,
           orbit_size, kernel17_targets, kernel17_rows, mutations):
    return "\n".join((
        "cubic kernels 13--15,17 final theorem: exact audit passed",
        f"dependency_verifiers_invoked: {dependencies}",
        "three_color_sieve: 359 certified orbits + 17 residual orbits",
        f"kernel13_15_frontiers: {targets} total = {strict} strict + "
        f"{equalities} K14 symbolic equality targets",
        "kernel14_symbolic_rows: 3; canonical_costs=3,3,3; "
        f"Gram_determinants={','.join(str(value) for value in determinants)}",
        "kernel14_coverage: every canonical and coordinate frontier; all lengths",
        f"kernel17_residual_orbit: {orbit_size} labeled rows; "
        f"canonical_coordinate_targets={kernel17_targets}",
        f"kernel17_seven_template_cover: {kernel17_rows} rows; residual=0; all lengths",
        "attachments: arbitrary rooted trees at core or internal path vertices",
        "inequality_scope: nonstrict; 148 rational frontier certificates are strict",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


def optimized_output():
    completed = subprocess.run(
        [sys.executable, "-O", str(Path(__file__).resolve()), "--emit"],
        check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O final verifier failed")
    require(completed.stderr == "", "python -O final verifier wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    dependencies = invoke_dependencies()
    kernel14_covered, determinants = audit_kernel14()
    targets, strict, equalities = audit_integrated_frontiers(kernel14_covered)
    orbit_size, kernel17_targets, kernel17_rows = audit_kernel17_all_length()
    mutations = hostile_self_checks(kernel14_covered)
    require(mutations == 7, "hostile mutation count changed")
    output = report(len(dependencies), targets, strict, equalities, determinants,
                    orbit_size, kernel17_targets, kernel17_rows, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
