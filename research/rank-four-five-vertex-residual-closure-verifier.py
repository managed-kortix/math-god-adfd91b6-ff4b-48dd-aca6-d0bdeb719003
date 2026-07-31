#!/usr/bin/env python3
"""Fail-closed exact audit closing the eight five-vertex residual rows."""

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "rank-four-five-vertex-residual-frontiers.json"
KERNEL9_VERIFIER = HERE / "kernel9-row01111-all-length-verifier.py"
EXPECTED_SHA256 = "dcd008fd27a813927def289f785caa506ddf14a8d6b0635bf7a196f8e58a5242"
PAIRS = tuple(combinations(range(5), 2))
KERNELS = {
    9: (0, 0, 1, 2, 1, 0, 2, 2, 0, 0),
    10: (0, 0, 1, 2, 1, 1, 1, 1, 1, 0),
    11: (0, 0, 1, 2, 1, 1, 1, 2, 0, 0),
}
KERNEL9_ROWS = (
    (0, 0, 0, 1, 1, 0, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 0, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 0, 1, 2, 0, 0),
    (0, 0, 1, 1, 1, 0, 2, 1, 0, 0),
)
FRONTIER_ROWS = (
    (9, KERNEL9_ROWS[2]),
    (9, KERNEL9_ROWS[3]),
    (10, (0, 0, 0, 1, 1, 1, 1, 1, 1, 0)),
    (10, (0, 0, 1, 0, 1, 1, 1, 1, 1, 0)),
    (11, (0, 0, 1, 1, 0, 0, 1, 1, 0, 0)),
    (11, (0, 0, 1, 1, 1, 1, 1, 1, 0, 0)),
)
PARTIAL_FRONTIER_ROW = (9, KERNEL9_ROWS[1])
PARTIAL_FRONTIER_COORDINATES = (1, 2, 4, 5, 6, 7)
INVOLUTION = (1, 0, 3, 2, 4)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class Qsqrt3:
    __slots__ = ("rational", "radical")

    def __init__(self, rational=0, radical=0):
        self.rational = Fraction(rational)
        self.radical = Fraction(radical)

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Qsqrt3) else Qsqrt3(value)

    def __eq__(self, other):
        try:
            other = self.coerce(other)
        except (TypeError, ValueError):
            return NotImplemented
        return (self.rational == other.rational
                and self.radical == other.radical)

    def __add__(self, other):
        other = self.coerce(other)
        return Qsqrt3(self.rational + other.rational,
                      self.radical + other.radical)

    __radd__ = __add__

    def __neg__(self):
        return Qsqrt3(-self.rational, -self.radical)

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return Qsqrt3(
            self.rational * other.rational + 3 * self.radical * other.radical,
            self.rational * other.radical + self.radical * other.rational)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        norm = other.rational * other.rational - 3 * other.radical * other.radical
        require(norm != 0, "division by zero in Q(sqrt(3))")
        return self * Qsqrt3(other.rational / norm, -other.radical / norm)


def qs3(rational=0, radical=0):
    return Qsqrt3(rational, radical)


KERNEL9_ROW11111_CERTIFICATE = {
    "row": KERNEL9_ROWS[1],
    "vectors": (
        (qs3(1), qs3()),
        (qs3(Fraction(-1, 2)), qs3(0, Fraction(1, 2))),
        (qs3(Fraction(1, 2)), qs3(0, Fraction(-1, 2))),
        (qs3(-1), qs3()),
        (qs3(Fraction(-1, 2)), qs3(0, Fraction(-1, 2))),
    ),
    "singletons": ((0, 3), (1, 2)),
    "bundles": ((0, 4, 2), (1, 4, 3), (2, 3, 4)),
}


def load_kernel9_module():
    require(KERNEL9_VERIFIER.is_file(), "missing kernel-9 verifier")
    spec = importlib.util.spec_from_file_location("kernel9_all_length", KERNEL9_VERIFIER)
    require(spec is not None and spec.loader is not None,
            "could not load kernel-9 verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def relabel(values, permutation):
    lookup = dict(zip(PAIRS, values))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in PAIRS)


def unit(parameter):
    denominator = 1 + parameter * parameter
    return ((1 - parameter * parameter) / denominator,
            2 * parameter / denominator)


def negate(vector):
    return -vector[0], -vector[1]


def step_cost(left, right):
    dot = sum(x * y for x, y in zip(left, right))
    require(dot != -1, "antipodal transformed step")
    return (1 - dot) / (1 + dot)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def parity_correlation(correlation, odd):
    return -correlation if odd else correlation


def audit_kernel9_row11111(certificate=None):
    certificate = (KERNEL9_ROW11111_CERTIFICATE if certificate is None
                   else certificate)
    require(set(certificate) == {"row", "vectors", "singletons", "bundles"},
            "kernel-9 row 11111 certificate schema changed")
    require(certificate["row"] == KERNEL9_ROWS[1],
            "kernel-9 row 11111 changed")
    require(certificate["vectors"] == KERNEL9_ROW11111_CERTIFICATE["vectors"],
            "kernel-9 row 11111 canonical angles changed")
    require(certificate["singletons"] == ((0, 3), (1, 2)),
            "kernel-9 row 11111 singleton ledger changed")
    require(certificate["bundles"] == ((0, 4, 2), (1, 4, 3), (2, 3, 4)),
            "kernel-9 row 11111 bundle ledger changed")

    vectors = certificate["vectors"]
    require(len(vectors) == 5 and all(dot(vector, vector) == 1
                                      for vector in vectors),
            "kernel-9 row 11111 vectors are not unit planar vectors")
    paths = path_ledger(KERNELS[9], certificate["row"])
    require(tuple(path[4] for path in paths) == (1, 1, 2, 1, 1, 2, 1, 2),
            "kernel-9 row 11111 canonical path lengths changed")

    singleton_total = qs3()
    for left, right in certificate["singletons"]:
        correlation = dot(vectors[left], vectors[right])
        require(correlation == -1, "singleton correlation is not -1")
        transformed = parity_correlation(correlation, odd=True)
        require(transformed == 1,
                "arbitrary odd singleton parity relation failed")
        singleton_total += (1 - transformed) / (1 + transformed)
    require(singleton_total == 0, "singleton costs are not zero")

    bundle_costs = []
    for left, right, midpoint in certificate["bundles"]:
        correlation = dot(vectors[left], vectors[right])
        require(correlation == Fraction(-1, 2),
                "bundle correlation is not -1/2")
        odd_cost = step_cost(vectors[left], negate(vectors[right]))
        even_cost = (step_cost(vectors[left], vectors[midpoint])
                     + step_cost(vectors[midpoint], vectors[right]))
        require(odd_cost == Fraction(1, 3), "bundle odd-path cost is not 1/3")
        require(even_cost == Fraction(2, 3), "bundle even-path cost is not 2/3")
        bundle_costs.append(odd_cost + even_cost)
    require(bundle_costs == [1, 1, 1], "bundle costs are not exactly one")
    total = singleton_total + sum(bundle_costs, qs3())
    require(total == 3, "kernel-9 row 11111 canonical total is not three")
    return total


def path_ledger(kernel, row):
    paths = []
    for edge, ((u, v), multiplicity, odd) in enumerate(zip(PAIRS, kernel, row)):
        require(0 <= odd <= multiplicity, "invalid physical row")
        lengths = [1] * odd + [2] * (multiplicity - odd)
        if multiplicity == odd == 2:
            lengths = [1, 3]
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(lengths))
    return tuple(paths)


def exact_cost(paths, branches, internals):
    require(len(branches) == 5 and branches[0] == 0, "bad branch ledger")
    require(len(paths) == len(internals), "bad internal ledger")
    vectors = tuple(unit(value) for value in branches)
    total = Fraction(0)
    for (_, _, u, v, length), parameters in zip(paths, internals):
        require(len(parameters) == length - 1, "bad internal path width")
        chain = [vectors[u], *(unit(value) for value in parameters)]
        chain.append(vectors[v] if length % 2 == 0 else negate(vectors[v]))
        total += sum(step_cost(left, right)
                     for left, right in zip(chain, chain[1:]))
    return total


def expected_keys():
    keys = [(PARTIAL_FRONTIER_ROW[0], PARTIAL_FRONTIER_ROW[1], coordinate)
            for coordinate in PARTIAL_FRONTIER_COORDINATES]
    keys.extend((kernel, row, coordinate)
                for kernel, row in FRONTIER_ROWS
                for coordinate in (None, *range(8)))
    return tuple(keys)


def load_fixture():
    require(FIXTURE.is_file(), f"missing fixture: {FIXTURE}")
    raw = FIXTURE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256,
            "frontier fixture digest changed")
    value = json.loads(raw.decode("ascii"))
    require(isinstance(value, dict), "fixture root is not an object")
    return value


def audit(payload=None, expected_digest=EXPECTED_SHA256):
    fixture = load_fixture() if payload is None else payload
    require(expected_digest == EXPECTED_SHA256, "digest policy was mutated")
    require(fixture.get("schema") == "rank-four-five-vertex-residual-frontiers-v1",
            "fixture schema changed")
    require(fixture.get("pair_order") == [f"{u}{v}" for u, v in PAIRS],
            "pair order changed")
    records = fixture.get("records")
    require(isinstance(records, list) and len(records) == 60,
            "frontier record count changed")
    keys = []
    for record in records:
        require(set(record) == {"kernel", "row", "frontier_coordinate", "lengths",
                                "branches", "internals", "cost"},
                "frontier record schema changed")
        kernel_number = record["kernel"]
        row = tuple(record["row"])
        coordinate = record["frontier_coordinate"]
        key = (kernel_number, row, coordinate)
        keys.append(key)
        require((kernel_number, row) in FRONTIER_ROWS
                or ((kernel_number, row) == PARTIAL_FRONTIER_ROW
                    and coordinate in PARTIAL_FRONTIER_COORDINATES),
                "foreign frontier row")
        paths = list(path_ledger(KERNELS[kernel_number], row))
        if coordinate is not None:
            require(type(coordinate) is int and 0 <= coordinate < len(paths),
                    "invalid frontier coordinate")
            path = paths[coordinate]
            paths[coordinate] = (*path[:-1], path[-1] + 2)
        require(record["lengths"] == [path[4] for path in paths],
                "frontier length vector changed")
        branches = tuple(Fraction(value) for value in record["branches"])
        internals = tuple(tuple(Fraction(value) for value in path)
                          for path in record["internals"])
        actual = exact_cost(tuple(paths), branches, internals)
        expected = Fraction(*record["cost"])
        require(actual == expected, "independent exact Fraction cost mismatch")
        require(actual < 3, "frontier certificate exceeds strict DNN budget")
    require(tuple(keys) == expected_keys(), "frontier keys are not exact and ordered")
    require(len(set(keys)) == 60, "duplicate frontier key")

    serial = json.dumps(fixture, sort_keys=True, separators=(",", ":")) + "\n"
    digest = hashlib.sha256(serial.encode("ascii")).hexdigest()
    require(digest == expected_digest, "canonical fixture digest changed")
    return digest


def audit_kernel9_reuse():
    module = load_kernel9_module()
    require(set(module.CERTIFICATES) == {"Oa", "Ea", "O23", "E23"},
            "kernel-9 accepted frontier classes changed")
    for name, (lengths, branches, internals, expected) in module.CERTIFICATES.items():
        actual = module.cost(lengths, branches, internals)
        require(actual == expected and actual < 3,
                f"kernel-9 reused certificate failed: {name}")

    kernel = KERNELS[9]
    require(relabel(kernel, INVOLUTION) == kernel,
            "stated kernel-9 map is not an automorphism")
    require(relabel(KERNEL9_ROWS[1], INVOLUTION) == KERNEL9_ROWS[1],
            "self-invariant kernel-9 parity row changed")
    require(relabel(KERNEL9_ROWS[0], INVOLUTION)
            == (0, 0, 1, 1, 0, 0, 1, 1, 0, 0),
            "kernel-9 involution image changed")
    require(len(set(KERNEL9_ROWS)) == 4, "kernel-9 parity ledger is not four rows")
    return len(module.CERTIFICATES)


def expect_rejected(action, label):
    try:
        action()
    except (IndexError, KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    baseline = load_fixture()
    mutations = []

    def add(label, mutate):
        candidate = deepcopy(baseline)
        mutate(candidate)
        mutations.append((label, candidate))

    add("deleted certificate", lambda value: value["records"].pop())
    add("changed branch", lambda value: value["records"][0]["branches"].__setitem__(1, "1"))
    add("changed internal", lambda value: value["records"][0]["internals"][2].__setitem__(0, "1"))
    add("forged cost", lambda value: value["records"][0]["cost"].__setitem__(0, 1))
    add("changed length", lambda value: value["records"][0]["lengths"].__setitem__(0, 4))
    add("duplicate coordinate", lambda value: value["records"][1].__setitem__(
        "frontier_coordinate", None))
    add("foreign row", lambda value: value["records"][0]["row"].__setitem__(2, 0))
    add("changed pair order", lambda value: value["pair_order"].reverse())
    for label, candidate in mutations:
        expect_rejected(lambda candidate=candidate: audit(candidate), label)
    expect_rejected(lambda: audit(baseline, "0" * 64), "digest mutation")
    angle_mutation = deepcopy(KERNEL9_ROW11111_CERTIFICATE)
    vectors = list(angle_mutation["vectors"])
    vectors[4] = vectors[3]
    angle_mutation["vectors"] = tuple(vectors)
    expect_rejected(lambda: audit_kernel9_row11111(angle_mutation),
                    "changed row 11111 canonical angle")
    return len(mutations) + 2


def report(digest, reused, row11111_total, mutations):
    return "\n".join((
        "five-vertex rank-four residual closure: exact audit passed",
        "residual_rows: 8 (kernel 9: 4, kernel 10: 2, kernel 11: 2)",
        f"kernel9_reused_frontier_classes: {reused}",
        "kernel9_parity_variants: 4 explicit; involution fixes row 11111",
        "kernel9_row11111: exact Q(sqrt(3)) planar certificate; "
        f"singleton_costs=0; bundle_costs=1,1,1; total={row11111_total.rational}",
        "kernel9_row11111_singletons: correlation=-1; arbitrary odd parity cost=0",
        "kernel9_row11111_bundles: correlation=-1/2; costs=1/3+2/3=1",
        "frozen_frontiers: 6 canonical + 54 one-coordinate-plus-two",
        "cost_backend: fractions.Fraction; strict_budget: cost < 3",
        "coverage: fixed-parity coordinatewise upward monotonicity",
        f"fixture_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


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
    digest = audit()
    reused = audit_kernel9_reuse()
    row11111_total = audit_kernel9_row11111()
    mutations = hostile_self_checks()
    require(mutations == 10, "hostile mutation count changed")
    output = report(digest, reused, row11111_total, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
