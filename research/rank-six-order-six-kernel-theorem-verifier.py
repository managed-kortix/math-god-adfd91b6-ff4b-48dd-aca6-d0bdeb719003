#!/usr/bin/env python3
"""Fail-closed exact verifier for the order-six rank-six kernel theorem."""

from __future__ import annotations

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
FIXTURE = HERE / "fixtures" / "rank-six-order-six-theorem.json"
CENSUS = ROOT / "positive-square-energy" / "experiments" / "rank6_order6_coarse_census.json"
KERNEL_SOURCE = HERE / "fixtures" / "rank-six-kernels.json"
FIXTURE_SHA256 = "c7883de1eff39c057e58630904e3ab15e9b88565b468e06f5d5692d08cd3ae4d"
CENSUS_SHA256 = "4cc2b699284fb1adac9ecf6f6fbedf5414af2a3d267d1c064413f8a8c8b3edce"
KERNEL_SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
PAIRS = tuple(itertools.combinations(range(6), 2))
FRONTIERS = (None, *range(11))
BUDGET = Fraction(5)


def q(value):
    return Fraction(value)


def matrix(rows):
    return tuple(tuple(q(value) for value in row) for row in rows)


GRAMS = {
    "K253-even": matrix((
        (1, "-1/3", "-1/3", "-1/2", 1, "-1/3"),
        ("-1/3", 1, "-1/3", "1/10", "-1/3", "-1/3"),
        ("-1/3", "-1/3", 1, "9/10", "-1/3", "-1/3"),
        ("-1/2", "1/10", "9/10", 1, "-1/2", "-1/2"),
        (1, "-1/3", "-1/3", "-1/2", 1, "-1/3"),
        ("-1/3", "-1/3", "-1/3", "-1/2", "-1/3", 1),
    )),
    "K253-odd": matrix((
        (1, "1/3", "1/3", "-1/2", -1, "1/3"),
        ("1/3", 1, "-1/3", 0, "-1/3", "-1/3"),
        ("1/3", "-1/3", 1, 0, "-1/3", "-1/3"),
        ("-1/2", 0, 0, 1, "1/2", "-1/2"),
        (-1, "-1/3", "-1/3", "1/2", 1, "-1/3"),
        ("1/3", "-1/3", "-1/3", "-1/2", "-1/3", 1),
    )),
    "K300-even": matrix((
        (1, 1, "1/2", "1/2", "-1/2", "-1/2"),
        (1, 1, "1/2", "1/2", "-1/2", "-1/2"),
        ("1/2", "1/2", 1, "-1/3", "-1/3", "-1/3"),
        ("1/2", "1/2", "-1/3", 1, "-1/3", "-1/3"),
        ("-1/2", "-1/2", "-1/3", "-1/3", 1, "-1/3"),
        ("-1/2", "-1/2", "-1/3", "-1/3", "-1/3", 1),
    )),
    "K300-odd": matrix((
        (1, -1, 0, 0, "1/2", "-1/2"),
        (-1, 1, 0, 0, "-1/2", "1/2"),
        (0, 0, 1, "-1/3", "-1/3", "-1/3"),
        (0, 0, "-1/3", 1, "-1/3", "-1/3"),
        ("1/2", "-1/2", "-1/3", "-1/3", 1, "-1/3"),
        ("-1/2", "1/2", "-1/3", "-1/3", "-1/3", 1),
    )),
    "K302-even": matrix((
        (1, 1, "-1/2", "-1/2", "-1/2", "-1/2"),
        (1, 1, "-1/2", "-1/2", "-1/2", "-1/2"),
        ("-1/2", "-1/2", 1, "-1/2", 1, "-1/2"),
        ("-1/2", "-1/2", "-1/2", 1, "-1/2", 1),
        ("-1/2", "-1/2", 1, "-1/2", 1, "-1/2"),
        ("-1/2", "-1/2", "-1/2", 1, "-1/2", 1),
    )),
    "K302-odd": matrix((
        (1, -1, "-1/2", "-1/2", "1/2", "-1/2"),
        (-1, 1, "1/2", "1/2", "-1/2", "1/2"),
        ("-1/2", "1/2", 1, "-1/2", 0, "-1/2"),
        ("-1/2", "1/2", "-1/2", 1, "-1/2", 1),
        ("1/2", "-1/2", 0, "-1/2", 1, "-1/2"),
        ("-1/2", "1/2", "-1/2", 1, "-1/2", 1),
    )),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def locked_json(path, digest, label):
    require(path.is_file(), f"missing {label}")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == digest, f"{label} digest changed")
    return json.loads(raw.decode("ascii"))


def determinant(values):
    work = [list(row) for row in values]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result *= value
        for row in range(column + 1, len(work)):
            scale = work[row][column] / value
            for index in range(column, len(work)):
                work[row][index] -= scale * work[column][index]
    return result


def audit_psd(gram, label):
    require(len(gram) == 6 and all(len(row) == 6 for row in gram), f"bad {label} order")
    require(all(gram[i][i] == 1 for i in range(6)), f"bad {label} diagonal")
    require(all(gram[i][j] == gram[j][i] for i in range(6) for j in range(6)),
            f"asymmetric {label}")
    for width in range(1, 7):
        for indices in itertools.combinations(range(6), width):
            minor = tuple(tuple(gram[i][j] for j in indices) for i in indices)
            require(determinant(minor) >= 0, f"non-PSD {label}")


def fraction(value, label):
    require(isinstance(value, list) and len(value) == 2, f"bad {label}")
    result = Fraction(*value)
    require(value == [result.numerator, result.denominator], f"uncanonical {label}")
    return result


def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def unit(parameters):
    square = dot(parameters, parameters)
    return ((1 - square) / (1 + square),) + tuple(2 * x / (1 + square) for x in parameters)


def step_cost(left, right):
    correlation = dot(left, right)
    require(correlation != -1, "antipodal path step")
    return (1 - correlation) / (1 + correlation)


def canonical_lengths(multiplicity, odd):
    require(0 <= odd <= multiplicity, "invalid physical row")
    return (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)


def path_ledger(kernel, row, frontier=None):
    paths = []
    for edge, ((u, v), multiplicity, odd) in enumerate(zip(PAIRS, kernel, row)):
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)))
    require(len(paths) == 11, "path count changed")
    if frontier is not None:
        require(type(frontier) is int and 0 <= frontier < 11, "invalid frontier")
        paths[frontier] = (*paths[frontier][:-1], paths[frontier][-1] + 2)
    return tuple(paths)


def audit_rational(record, kernel):
    witness = record.get("witness")
    require(record.get("exact_dnn_le_5") is True and isinstance(witness, dict),
            "missing rational witness")
    branches = tuple(unit(tuple(fraction(x, "branch parameter") for x in row))
                     for row in witness["branches"])
    require(len(branches) == 6 and all(len(row) == 6 for row in branches),
            "branch dimensions changed")
    paths = path_ledger(kernel, tuple(record["row"]), record["frontier"])
    require(record["lengths"] == [path[4] for path in paths], "rational lengths changed")
    require(len(witness["internals"]) == 11, "internal ledger changed")
    total = Fraction(0)
    for (_, _, u, v, length), raw in zip(paths, witness["internals"]):
        parameters = tuple(tuple(fraction(x, "internal parameter") for x in row) for row in raw)
        require(len(parameters) == length - 1, "wrong internal path width")
        chain = [branches[u], *(unit(row) for row in parameters)]
        chain.append(branches[v] if length % 2 == 0 else tuple(-x for x in branches[v]))
        total += sum((step_cost(left, right) for left, right in zip(chain, chain[1:])),
                     Fraction(0))
    require(total == fraction(witness["cost"], "stored cost"), "rational cost changed")
    require(total <= BUDGET, "rational witness exceeds five")


def row_tuple(text):
    require(isinstance(text, str) and len(text) == 15 and set(text) <= {"0", "1", "2"},
            "bad encoded row")
    return tuple(int(value) for value in text)


def path_symbolic_cost(correlation, length):
    transformed = correlation if length % 2 == 0 else -correlation
    if transformed == 1:
        return Fraction(0)
    if length == 1:
        return (1 - transformed) / (1 + transformed)
    if length == 2 and transformed == Fraction(-1, 2):
        midpoint_gram = ((Fraction(1), Fraction(1, 2), Fraction(-1, 2)),
                         (Fraction(1, 2), Fraction(1), Fraction(1, 2)),
                         (Fraction(-1, 2), Fraction(1, 2), Fraction(1)))
        require(determinant(midpoint_gram) >= 0, "invalid equality midpoint")
        return Fraction(2, 3)
    raise RuntimeError("equality template contains an unrealized path")


def audit_equalities(fixture, kernels):
    expected = {
        (253, "001001011011011", (None, 2), "K253-even"),
        (253, "001101011011011", (None, 2), "K253-odd"),
        (300, "000010010111111", (None, 0), "K300-even"),
        (300, "100010010111111", (None, 0), "K300-odd"),
        (302, "000010010101100", (None, 0), "K302-even"),
        (302, "100010010101100", (None, 0), "K302-odd"),
    }
    actual = {(item["kernel"], item["row"], tuple(item["frontiers"]), item["gram"])
              for item in fixture["equality_rows"]}
    require(actual == expected and len(fixture["equality_rows"]) == 6,
            "equality-row ledger changed")
    keys = set()
    for number, text, frontiers, name in sorted(expected):
        gram = GRAMS[name]
        audit_psd(gram, name)
        row = row_tuple(text)
        for frontier in frontiers:
            paths = path_ledger(kernels[number], row, frontier)
            total = sum((path_symbolic_cost(gram[u][v], length)
                         for _, _, u, v, length in paths), Fraction(0))
            require(total == BUDGET, f"{name} cost is not five")
            keys.add((number, row, frontier))
        special = frontiers[1]
        _, _, u, v, length = path_ledger(kernels[number], row, special)[special]
        transformed = gram[u][v] if length % 2 == 0 else -gram[u][v]
        require(transformed == 1, f"{name} special path is not zero-cost at all lengths")
    require(len(keys) == 12, "equality target count changed")
    return keys


def audit_structural(fixture, kernels):
    item = fixture["structural"]
    require(item == {"kernel": 223, "row": "001111011011111", "frontier": None,
                     "k4_vertices": [0, 3, 4, 5], "tree_vertices": [1, 2]},
            "K223 structural ledger changed")
    row = row_tuple(item["row"])
    paths = path_ledger(kernels[223], row)
    require(all(path[4] == 1 for path in paths), "K223 core is not all-unit")
    edges = {tuple(sorted((u, v))) for _, _, u, v, _ in paths}
    k4 = set(item["k4_vertices"])
    tree = set(item["tree_vertices"])
    require(k4.isdisjoint(tree) and k4 | tree == set(range(6)), "K223 partition changed")
    require({tuple(sorted(edge)) for edge in itertools.combinations(k4, 2)} <= edges,
            "K223 retained side is not an actual K4")
    require(tuple(sorted(tree)) in edges, "K223 deleted side is not a nonempty tree")
    # Every rooted attachment follows its unique branch owner. The two induced
    # parts are disjoint and exhaustive; cross edges do not affect induced
    # superadditivity. Attached K4 credit >2 plus nonempty-tree credit -1 is >0.
    return (223, row, None)


def audit(payload=None, mutation_mode=False):
    fixture = locked_json(FIXTURE, FIXTURE_SHA256, "theorem fixture") if payload is None else payload
    require(fixture["schema"] == "rank-six-order-six-kernel-theorem-v1", "schema changed")
    require(fixture["pair_order"] == [f"{u}{v}" for u, v in PAIRS], "pair order changed")
    require((fixture["rank"], fixture["order"], fixture["kernel_interval"],
             fixture["kernel_total"], fixture["path_count"])
            == (6, 6, [116, 331], 216, 11), "scope changed")
    require((fixture["physical_total"], fixture["orbit_total"],
             fixture["coarse_certified_total"], fixture["residual_total"])
            == (207358, 150734, 148130, 2604), "census totals changed")
    require((fixture["frontiers_per_residual"], fixture["target_total"],
             fixture["rational_total"], fixture["equality_total"],
             fixture["structural_total"]) == (12, 31248, 31235, 12, 1),
            "closure totals changed")

    census = locked_json(CENSUS, CENSUS_SHA256, "coarse census")
    source = locked_json(KERNEL_SOURCE, KERNEL_SOURCE_SHA256, "kernel source")
    source_kernels = {index: tuple(record["code"])
                      for index, record in enumerate(source["kernels"], 1)
                      if record["n"] == 6}
    kernels = {record["kernel"]: tuple(record["code"]) for record in census["kernels"]}
    require(kernels == source_kernels and set(kernels) == set(range(116, 332)),
            "exact kernel set changed")
    require((census["kernel_total"], census["physical_total"], census["orbit_total"],
             census["coarse_certified_total"], census["coarse_residual_total"],
             census["frontier_target_total"])
            == (216, 207358, 150734, 148130, 2604, 31248), "census mismatch")
    residual_keys = [(record["kernel"], tuple(record["row"])) for record in census["residuals"]]
    require(len(residual_keys) == len(set(residual_keys)) == 2604, "residual key set changed")
    expected = {(number, row, frontier) for number, row in residual_keys for frontier in FRONTIERS}

    records = {}
    source_coverage = []
    for descriptor in fixture["sources"]:
        path = ROOT / descriptor["file"]
        chunk = locked_json(path, descriptor["sha256"], path.name)
        start, count = descriptor["start"], descriptor["residuals"]
        require((chunk["selected_residual_start"], chunk["selected_residual_total"],
                 chunk["target_total"]) == (start, count, descriptor["targets"]),
                "chunk extent changed")
        require(chunk["selected_frontiers"] == list(FRONTIERS), "chunk frontiers changed")
        require(chunk["source_census_sha256"] == CENSUS_SHA256, "chunk census changed")
        source_coverage.extend(range(start, start + count))
        for record in chunk["records"]:
            key = (record["kernel"], tuple(record["row"]), record["frontier"])
            require(key not in records, "duplicate target key")
            require(record["source_index"] < len(residual_keys)
                    and key[:2] == residual_keys[record["source_index"]],
                    "source index/key mismatch")
            records[key] = record
    require(source_coverage == list(range(2604)), "chunk source coverage changed")
    require(set(records) == expected and len(records) == 31248, "frontier key universe changed")

    unresolved = {key for key, record in records.items() if not record["exact_dnn_le_5"]}
    equality = audit_equalities(fixture, kernels)
    structural = audit_structural(fixture, kernels)
    require(unresolved == equality | {structural} and len(unresolved) == 13,
            "13-target residual set changed")
    rational = expected - unresolved
    require(len(rational) == 31235, "rational target count changed")
    if not mutation_mode:
        for key in sorted(rational, key=lambda item: (item[0], item[1], -1 if item[2] is None else item[2])):
            audit_rational(records[key], kernels[key[0]])
    return fixture


def expect_rejected(candidate, label):
    try:
        audit(candidate, mutation_mode=True)
    except (IndexError, KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks(fixture):
    mutations = []

    def add(label, change):
        candidate = deepcopy(fixture)
        change(candidate)
        mutations.append((label, candidate))

    add("kernel count", lambda value: value.__setitem__("kernel_total", 215))
    add("pair order", lambda value: value["pair_order"].reverse())
    add("rational count", lambda value: value.__setitem__("rational_total", 31234))
    add("deleted source", lambda value: value["sources"].pop())
    add("source range", lambda value: value["sources"][1].__setitem__("start", 26))
    add("source digest", lambda value: value["sources"][0].__setitem__("sha256", "0" * 64))
    add("equality row", lambda value: value["equality_rows"][0].__setitem__("row", "0" * 15))
    add("equality frontier", lambda value: value["equality_rows"][0]["frontiers"].pop())
    add("equality gram", lambda value: value["equality_rows"][0].__setitem__("gram", "K300-even"))
    add("structural K4", lambda value: value["structural"]["k4_vertices"].pop())
    add("structural row", lambda value: value["structural"].__setitem__("row", "0" * 15))
    for label, candidate in mutations:
        expect_rejected(candidate, label)
    return len(mutations)


def report(mutations):
    return "\n".join((
        "rank-six order-six kernel theorem: exact audit passed",
        "kernels=216 physical=207358 orbits=150734 coarse=148130 residuals=2604",
        "frontier_targets=31248 rational=31235 equality=12 structural_K223=1",
        "equality_rows=K253:4 K300:4 K302:4; each exact cost=5",
        "coverage=canonical plus 11 coordinate frontiers; all same-parity lengths",
        "attachments=arbitrary finite rooted trees by owner-exact induced partitions",
        f"rejected_hostile_mutations={mutations}",
        "conclusion=s+(G)>=|V(G)|",
    )) + "\n"


def main():
    fixture = audit()
    mutations = hostile_self_checks(fixture)
    require(mutations == 11, "hostile mutation count changed")
    output = report(mutations)
    if sys.flags.optimize == 0 and "--emit" not in sys.argv:
        completed = subprocess.run((sys.executable, "-O", __file__, "--emit"),
                                   check=False, capture_output=True, text=True)
        require(completed.returncode == 0 and completed.stderr == "",
                "optimized verifier failed")
        require(completed.stdout == output, "normal and optimized outputs differ")
    sys.stdout.write(output)


if __name__ == "__main__":
    main()
