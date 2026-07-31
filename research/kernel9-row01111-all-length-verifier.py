#!/usr/bin/env python3
"""Fail-closed exact audit for the four kernel-9 q=01111 frontiers."""

import argparse
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def q(text):
    return Fraction(text)


def unit(parameter):
    denominator = 1 + parameter * parameter
    return ((1 - parameter * parameter) / denominator,
            2 * parameter / denominator)


def negate(vector):
    return tuple(-entry for entry in vector)


def step_cost(left, right):
    dot = sum(x * y for x, y in zip(left, right))
    require(dot != -1, "antipodal transformed step")
    return (1 - dot) / (1 + dot)


def cost(lengths, branches, internals):
    endpoints = ((0, 3), (0, 4), (0, 4), (1, 2),
                 (1, 4), (1, 4), (2, 3), (2, 3))
    require(len(lengths) == len(internals) == len(endpoints), "bad path ledger")
    vectors = tuple(unit(q(value)) for value in branches)
    total = Fraction(0)
    for length, (left_index, right_index), parameters in zip(
            lengths, endpoints, internals):
        require(len(parameters) == length - 1, "bad internal ledger")
        chain = [vectors[left_index]]
        chain.extend(unit(q(value)) for value in parameters)
        endpoint = vectors[right_index]
        chain.append(negate(endpoint) if length % 2 else endpoint)
        total += sum(step_cost(left, right)
                     for left, right in zip(chain, chain[1:]))
    return total


CERTIFICATES = {
    "Oa": (
        (2, 3, 2, 1, 1, 2, 1, 2),
        ("0", "1/2", "-2", "0", "-3/4"),
        (("0",), ("3/8", "3/4"), ("-3/8",), (), (),
         ("-1/8",), (), ("-5/8",)),
        Fraction(274636609, 106750224),
    ),
    "Ea": (
        (2, 1, 4, 1, 1, 2, 1, 2),
        ("0", "-35/128", "363/128", "5/32", "-449/128"),
        (("5/64",), (), ("-43/128", "-97/128", "-187/128"), (), (),
         ("-127/128",), (), ("53/64",)),
        Fraction(
            2455762417234397771632703751839480116390241219369499364904459306592428429364885494167,
            961994787065419545265007148397320162556673426780741122018796796569502796106728243200),
    ),
    "O23": (
        (2, 1, 2, 1, 1, 2, 3, 2),
        ("0", "-13/8", "5/8", "0", "7/4"),
        (("0",), (), ("5/8",), (), (), ("-381/4",),
         ("5/4", "21/8"), ("1/4",)),
        Fraction(
            169397265426892375078896116727548029,
            66498943294333381292657717152262400),
    ),
    "E23": (
        (2, 1, 2, 1, 1, 2, 1, 4),
        ("0", "0", "-31/4", "-1/8", "-13/8"),
        (("-1/8",), (), ("-5/8",), (), (), ("-1/2",), (),
         ("-2", "-1", "-1/2")),
        Fraction(24574309112220291047807, 9464079288722234391072),
    ),
}


def audit(certificates=None):
    certificates = CERTIFICATES if certificates is None else certificates
    require(set(certificates) == {"Oa", "Ea", "O23", "E23"},
            "frontier class mismatch")
    costs = []
    for name in ("Oa", "Ea", "O23", "E23"):
        lengths, branches, internals, expected = certificates[name]
        actual = cost(lengths, branches, internals)
        require(actual == expected, f"{name}: exact fixture mismatch")
        require(actual < 3, f"{name}: DNN budget failure")
        costs.append((name, actual))
    return tuple(costs)


def expect_rejected(action, label):
    try:
        action()
    except (IndexError, KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = []

    def add(label, mutate):
        candidate = deepcopy(CERTIFICATES)
        mutate(candidate)
        mutations.append((label, candidate))

    add("deleted variant", lambda value: value.pop("Oa"))
    add("changed length", lambda value: value.__setitem__(
        "Oa", ((4, *value["Oa"][0][1:]), *value["Oa"][1:])))
    add("changed branch", lambda value: value.__setitem__(
        "Ea", (value["Ea"][0], ("1", *value["Ea"][1][1:]), *value["Ea"][2:])))
    add("changed internal", lambda value: value.__setitem__(
        "O23", (value["O23"][0], value["O23"][1],
                (("1",), *value["O23"][2][1:]), value["O23"][3])))
    add("forged cost", lambda value: value.__setitem__(
        "E23", (*value["E23"][:3], Fraction(1))))
    for label, candidate in mutations:
        expect_rejected(lambda candidate=candidate: audit(candidate), label)
    return len(mutations)


def report(costs, mutations):
    lines = [f"{name}: exact_cost={actual} < 3" for name, actual in costs]
    lines.extend((
        "frontier_variants=4: Oa,Ea,O23,E23",
        "coverage=fixed-physical-parity coordinatewise upward monotonicity",
        "residual=structural singleton family",
        f"rejected_hostile_mutations: {mutations}",
    ))
    return "\n".join(lines) + "\n"


def optimized_output():
    completed = subprocess.run(
        [sys.executable, "-O", str(Path(__file__).resolve()), "--emit"],
        check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O verifier failed")
    require(completed.stderr == "", "python -O verifier wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    output = report(audit(), hostile_self_checks())
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
