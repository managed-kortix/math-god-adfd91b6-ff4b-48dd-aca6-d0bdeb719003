#!/usr/bin/env python3
"""Exact fail-closed audit of the 13 rank-five four-vertex frontiers."""

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
SIEVE_VERIFIER = HERE / "rank-five-four-vertex-tetrahedral-sieve-verifier.py"
SIEVE_FIXTURE = HERE / "fixtures" / "rank-five-four-vertex-tetrahedral-sieve.json"
FIXTURE = HERE / "fixtures" / "rank-five-four-vertex-residual-frontiers.json"
SIEVE_SHA256 = "0b8ded3f4dbe0b8de916c085393c5f470bbaf8961deddf4305396e15f1d45588"
EXPECTED_SHA256 = "09a7b38b1e9f5e18aaddc1f9e0114b8490151f2062d3f51100c52eb314eb56d2"
PAIRS = tuple(combinations(range(4), 2))
EXPECTED_STRICT = 116
EXPECTED_EQUALITY = 1
EXPECTED_TARGETS = 117


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
def sieve_module():
    spec = spec_from_file_location("rank_five_four_vertex_sieve", SIEVE_VERIFIER)
    require(spec is not None and spec.loader is not None, "cannot load sieve verifier")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fraction_pair(value):
    return [value.numerator, value.denominator]


def parse_fraction(value, label):
    require(isinstance(value, list) and len(value) == 2, f"bad fraction: {label}")
    require(all(type(entry) is int for entry in value), f"noninteger fraction: {label}")
    require(value[1] > 0, f"nonpositive denominator: {label}")
    result = Fraction(*value)
    require(fraction_pair(result) == value, f"noncanonical fraction: {label}")
    return result


def determinant(matrix):
    size = len(matrix)
    if size == 0:
        return Fraction(1)
    total = Fraction(0)
    for column, value in enumerate(matrix[0]):
        minor = tuple(tuple(row[j] for j in range(size) if j != column)
                      for row in matrix[1:])
        total += (-1 if column % 2 else 1) * value * determinant(minor)
    return total


def require_psd(matrix):
    size = len(matrix)
    require(size and all(len(row) == size for row in matrix), "Gram matrix is not square")
    require(all(matrix[i][j] == matrix[j][i] for i in range(size) for j in range(size)),
            "Gram matrix is not symmetric")
    for mask in range(1, 1 << size):
        indices = tuple(index for index in range(size) if mask >> index & 1)
        minor = tuple(tuple(matrix[i][j] for j in indices) for i in indices)
        require(determinant(minor) >= 0, "negative principal Gram minor")


def unit(parameter):
    square = sum(value * value for value in parameter)
    denominator = 1 + square
    return ((1 - square) / denominator,) + tuple(2 * value / denominator
                                                  for value in parameter)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def step_cost(left, right):
    correlation = dot(left, right)
    require(correlation != -1, "antipodal transformed step")
    return (1 - correlation) / (1 + correlation)


def path_ledger(kernel, row, coordinate=None):
    paths = []
    for edge, ((u, v), multiplicity, odd) in enumerate(zip(PAIRS, kernel, row)):
        require(0 <= odd <= multiplicity, "bad physical row")
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(lengths))
    require(len(paths) == 8, "rank-five four-vertex path count changed")
    if coordinate is not None:
        require(type(coordinate) is int and 0 <= coordinate < 8, "bad frontier coordinate")
        edge, occurrence, u, v, length = paths[coordinate]
        paths[coordinate] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def exact_cost(paths, branch_parameters, internal_parameters):
    require(len(branch_parameters) == 4 and branch_parameters[0] == (0, 0, 0),
            "branch parameter ledger changed")
    require(len(internal_parameters) == len(paths), "internal path ledger changed")
    branches = tuple(unit(value) for value in branch_parameters)
    total = Fraction(0)
    for (_, _, u, v, length), parameters in zip(paths, internal_parameters):
        require(len(parameters) == length - 1, "internal path width changed")
        chain = [branches[u], *(unit(value) for value in parameters)]
        endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
        chain.append(endpoint)
        total += sum(step_cost(left, right) for left, right in zip(chain, chain[1:]))
    return total


def residual_source():
    fixture, raw = load_json(SIEVE_FIXTURE)
    require(hashlib.sha256(raw).hexdigest() == SIEVE_SHA256, "sieve fixture digest changed")
    sieve_module().audit()
    kernels = {record["kernel"]: tuple(record["code"]) for record in fixture["kernels"]}
    residuals = tuple((record["kernel"], tuple(record["row"]))
                      for record in fixture["records"] if not record["certified"])
    require(len(residuals) == 13, "source residual count changed")
    return kernels, residuals


def parse_parameter_rows(record):
    branches = tuple(tuple(parse_fraction(value, "branch") for value in row)
                     for row in record["branches"])
    internals = tuple(tuple(tuple(parse_fraction(value, "internal") for value in row)
                            for row in path)
                      for path in record["internals"])
    return branches, internals


def audit_strict_record(record, kernels, residuals):
    key = record["kernel"], tuple(record["row"])
    require(key in residuals, "strict record is not a source residual")
    coordinate = record["frontier_coordinate"]
    paths = path_ledger(kernels[key[0]], key[1], coordinate)
    require(record["lengths"] == [path[4] for path in paths], "strict length vector changed")
    branches, internals = parse_parameter_rows(record)
    cost = exact_cost(paths, branches, internals)
    require(cost == parse_fraction(record["cost"], "cost"), "stored exact cost changed")
    require(cost < 4, "strict certificate is not strict")
    vectors = tuple(unit(value) for value in branches)
    gram = tuple(tuple(dot(left, right) for right in vectors) for left in vectors)
    require_psd(gram)
    return key, coordinate


def audit_equality(record, kernels, residuals):
    key = record["kernel"], tuple(record["row"])
    require(key in residuals and key[0] == 9, "symbolic equality is not kernel 9")
    require(record["frontier_coordinate"] is None, "equality is not canonical")
    paths = path_ledger(kernels[key[0]], key[1])
    require(record["lengths"] == [path[4] for path in paths] == [1, 2] * 4,
            "kernel-9 equality lengths changed")
    gram = tuple(tuple(parse_fraction(value, "equality Gram") for value in row)
                 for row in record["gram"])
    expected = (
        (Fraction(1), Fraction(1), Fraction(-1, 2), Fraction(-1, 2)),
        (Fraction(1), Fraction(1), Fraction(-1, 2), Fraction(-1, 2)),
        (Fraction(-1, 2), Fraction(-1, 2), Fraction(1), Fraction(1)),
        (Fraction(-1, 2), Fraction(-1, 2), Fraction(1), Fraction(1)),
    )
    require(gram == expected, "kernel-9 symbolic Gram changed")
    require_psd(gram)
    require(determinant(gram) == 0, "kernel-9 equality Gram determinant changed")
    require(record.get("symbolic_parameter") == "theta=2*pi/3",
            "kernel-9 symbolic field changed")
    require(record.get("cost_identity") == "4*((1/3)+(2/3))=4",
            "kernel-9 symbolic cost identity changed")
    odd_cost = (1 + Fraction(-1, 2)) / (1 - Fraction(-1, 2))
    # A length-two path at endpoint angle 2*pi/3 has two transformed steps
    # of angle pi/3, each with tangent-square cost 1/3.
    even_cost = 2 * Fraction(1, 3)
    require(4 * (odd_cost + even_cost) == 4,
            "kernel-9 symbolic total is not equality four")
    return key, None


def audit(payload=None, expected_digest=EXPECTED_SHA256):
    if payload is None:
        fixture, raw = load_json(FIXTURE)
        require(raw == canonical_bytes(fixture), "frontier fixture is not canonical JSON")
    else:
        fixture = payload
    require(fixture.get("schema") == "rank-five-four-vertex-residual-frontiers-v1",
            "frontier schema changed")
    require(fixture.get("source_sieve_sha256") == SIEVE_SHA256, "source digest field changed")
    kernels, residuals = residual_source()
    strict = fixture.get("strict_records")
    equalities = fixture.get("symbolic_equalities")
    require(isinstance(strict, list) and len(strict) == EXPECTED_STRICT,
            "strict record count changed")
    require(isinstance(equalities, list) and len(equalities) == EXPECTED_EQUALITY,
            "equality record count changed")
    keys = [audit_strict_record(record, kernels, residuals) for record in strict]
    keys += [audit_equality(record, kernels, residuals) for record in equalities]
    expected = {(key, coordinate) for key in residuals for coordinate in (None, *range(8))}
    require(len(keys) == len(set(keys)) == EXPECTED_TARGETS and set(keys) == expected,
            "selected canonical-plus-coordinate frontier covering set is not exact")
    require(fixture.get("target_total") == EXPECTED_TARGETS, "target total changed")
    require(fixture.get("strict_total") == EXPECTED_STRICT, "strict total changed")
    require(fixture.get("equality_total") == EXPECTED_EQUALITY, "equality total changed")
    digest = hashlib.sha256(canonical_bytes(fixture)).hexdigest()
    require(expected_digest == EXPECTED_SHA256, "digest policy was mutated")
    require(digest == expected_digest, "frontier fixture digest changed")
    return digest


def expect_rejected(action, label):
    try:
        action()
    except (IndexError, KeyError, RuntimeError, TypeError, ValueError, ZeroDivisionError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    baseline, _ = load_json(FIXTURE)
    mutations = []

    def add(label, mutate):
        candidate = deepcopy(baseline)
        mutate(candidate)
        mutations.append((label, candidate))

    add("deleted target", lambda value: value["strict_records"].pop())
    add("forged strict cost", lambda value: value["strict_records"][0].__setitem__("cost", [0, 1]))
    add("changed coordinate", lambda value: value["strict_records"][0].__setitem__("frontier_coordinate", 7))
    add("changed path length", lambda value: value["strict_records"][0]["lengths"].__setitem__(0, 99))
    add("changed branch", lambda value: value["strict_records"][0]["branches"].__setitem__(1, [1, 7]))
    add("changed internal", lambda value: value["strict_records"][0]["internals"][2][0].__setitem__(0, [1, 7]))
    add("noncanonical fraction", lambda value: value["strict_records"][0].__setitem__("cost", [2, 2]))
    add("changed equality Gram", lambda value: value["symbolic_equalities"][0]["gram"][0].__setitem__(1, [-1, 3]))
    add("promoted count", lambda value: value.__setitem__("strict_total", 117))
    for label, candidate in mutations:
        expect_rejected(lambda candidate=candidate: audit(candidate), label)
    expect_rejected(lambda: audit(baseline, "0" * 64), "digest mutation")
    return len(mutations) + 1


def report(digest, mutations):
    return "\n".join((
        "rank-five four-vertex residual frontier: audit passed",
        "source_census: 1281 physical rows / 821 automorphism orbits",
        "source_sieve: 808 certified + 13 residual",
        "frontier_covering_set: selected 13 canonical + 104 coordinate-plus-two = 117",
        "certificates: 116 strict rational path-vector + 1 kernel-9 symbolic equality",
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
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 10, "hostile mutation count changed")
    output = report(digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
