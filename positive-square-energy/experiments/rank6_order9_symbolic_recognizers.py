#!/usr/bin/env python3
"""Regenerate and exactly audit all order-nine cost-five atom geometries."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
CLASSIFIER_PATH = HERE / "rank6_orders8_10_atom_ledger_search.py"
CLASSIFICATION_PATH = HERE / "rank6_orders8_10_atom_ledger_classification.json"
F = Fraction
EXPECTED_CLASSIFIER_PROFILES = {(5, ()): 10, (2, (4,)): 249, (1, (3, 4)): 16}
EXPECTED_EXACT_PROFILES = {(5, ()): 10, (2, (4,)): 56, (1, (3, 4)): 16}
GEOMETRIES = {
    (5, ()): "signed-five-cycle",
    (2, (4,)): "tetrahedron-plus-apex",
    (1, (3, 4)): "coupled-triangle-tetrahedron",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def strict_json(raw, label):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(
                              ValueError(f"nonstandard constant {value}")))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"{label} is not strict ASCII JSON") from error


def determinant(matrix):
    work = [list(row) for row in matrix]
    result = F(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result *= value
        for row in range(column + 1, len(work)):
            scale = work[row][column] / value
            for index in range(column + 1, len(work)):
                work[row][index] -= scale * work[column][index]
    return result


def audit_psd(gram):
    order = len(gram)
    require(all(len(row) == order for row in gram), "nonsquare symbolic Gram")
    require(all(gram[i][i] == 1 for i in range(order)), "nonunit symbolic Gram")
    require(all(gram[i][j] == gram[j][i] for i in range(order) for j in range(order)),
            "nonsymmetric symbolic Gram")
    for width in range(1, order + 1):
        for indices in itertools.combinations(range(order), width):
            require(determinant([[gram[i][j] for j in indices] for i in indices]) >= 0,
                    "indefinite symbolic Gram")


def solve_switches(edges):
    adjacency = {}
    for (left, right), switch in edges:
        adjacency.setdefault(left, []).append((right, switch))
        adjacency.setdefault(right, []).append((left, switch))
    values = {}
    for root in adjacency:
        if root in values:
            continue
        values[root] = 1
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbor, product in adjacency[vertex]:
                expected = values[vertex] * product
                if neighbor in values:
                    require(values[neighbor] == expected, "inconsistent simplex switching")
                else:
                    values[neighbor] = expected
                    stack.append(neighbor)
    return values


def quotient_gram(result):
    _, _, mixed, atoms, _, classes, _, prescribed = result
    width = max(classes) + 1
    gram = [[F(int(i == j)) for j in range(width)] for i in range(width)]
    for (u, v), value in prescribed:
        gram[u][v] = gram[v][u] = value
    profile = (len(mixed), tuple(sorted(atom_width for atom_width, _ in atoms)))
    if profile == (5, ()):
        pass
    elif profile == (2, (4,)):
        tetra_edges = next(edges for atom_width, edges in atoms if atom_width == 4)
        tetra = set(itertools.chain.from_iterable(edge for edge, _ in tetra_edges))
        apex = next(iter(set(mixed[0][0]) & set(mixed[1][0])))
        require(apex not in tetra and len(tetra) == 4, "bad tetrahedron-plus-apex support")
        switches = solve_switches(tuple((edge, -3 * gram[edge[0]][edge[1]])
                                         for edge, _ in tetra_edges))
        known = {v if u == apex else u: gram[u][v] for (u, v), _ in mixed}
        require(len(known) == 2 and set(known) < tetra, "bad apex mixed-pair support")
        missing = tetra - set(known)
        fill = -sum((switches[v] * value for v, value in known.items()), F()) / len(missing)
        for vertex in missing:
            gram[apex][vertex] = gram[vertex][apex] = switches[vertex] * fill
    elif profile == (1, (3, 4)):
        blocks = {atom_width: set(itertools.chain.from_iterable(edge for edge, _ in edges))
                  for atom_width, edges in atoms}
        shared = blocks[3] & blocks[4]
        require(len(shared) == 1 and set(mixed[0][0]) <= blocks[3],
                "bad coupled triangle/tetrahedron support")
        cut = next(iter(shared))
        for left in blocks[3] - {cut}:
            for right in blocks[4] - {cut}:
                gram[left][right] = gram[right][left] = gram[left][cut] * gram[cut][right]
    else:
        raise RuntimeError(f"unknown symbolic profile {profile}")
    audit_psd(gram)
    return gram, profile


def audit_ledger(pipeline, source, result):
    _, support, multiplicities, row, _, _, _ = source
    _, stored_row, _, _, contractions, classes, signs, _ = result
    require(tuple(row) == stored_row, "classifier row differs from census")
    quotient, profile = quotient_gram(result)
    gram = [[F(signs[i] * signs[j]) * quotient[classes[i]][classes[j]]
             for j in range(pipeline.ORDER)] for i in range(pipeline.ORDER)]
    audit_psd(gram)
    contraction_set = set(contractions)
    total = F()
    zero_coordinates = []
    coordinate = 0
    for index, multiplicity, odd in zip(support, multiplicities, row):
        edge = pipeline.PAIRS[index]
        correlation = gram[edge[0]][edge[1]]
        occurrence_lengths = ([1] + [3] * (odd - 1) if odd else []) + [2] * (multiplicity - odd)
        for length in occurrence_lengths:
            transformed = correlation if length % 2 == 0 else -correlation
            require(transformed > -1, "symbolic path has singular endpoint correlation")
            if transformed == 1:
                cost = F()
            elif length == 1:
                cost = (1 - transformed) / (1 + transformed)
            else:
                require(length == 2 and transformed == F(-1, 2),
                        "unsupported positive-cost symbolic path")
                cost = F(2, 3)
            total += cost
            if cost == 0:
                require((edge, bool(length % 2)) in contraction_set,
                        "unclassified zero-cost symbolic path")
                zero_coordinates.append(coordinate)
            coordinate += 1
    require(coordinate == pipeline.PATH_COUNT and total == pipeline.BUDGET,
            "symbolic physical ledger does not have exact cost five")
    require(len(zero_coordinates) == len(contractions), "contraction target count changed")
    return profile, (None, *zero_coordinates)


def derive(pipeline):
    classifier = load_module("rank6_order9_atom_classifier", CLASSIFIER_PATH)
    classifier.audit_atom_model()
    raw = CLASSIFICATION_PATH.read_bytes()
    fixture = strict_json(raw, "atom classification")
    require(raw == canonical_bytes(fixture), "atom classification is not canonical JSON")
    require(fixture.get("schema") == "rank6-orders8-10-exact-atom-ledger-classification-v1",
            "atom classification schema changed")
    expected_records = [record for record in fixture.get("decompositions", ())
                        if record.get("order") == pipeline.ORDER]
    classifier_profiles = {}
    for record in expected_records:
        key = (record["profile"]["mixed"], tuple(record["profile"]["simplex_widths"]))
        classifier_profiles[key] = classifier_profiles.get(key, 0) + 1
    require(classifier_profiles == EXPECTED_CLASSIFIER_PROFILES,
            f"classifier profile counts changed: {classifier_profiles}")

    _, residual_rows = pipeline.census(collect_residuals=True)
    records = []
    null_keys = set()
    profile_counts = {}
    regenerated = []
    for source_index, source in enumerate(residual_rows):
        for result in classifier.classify(pipeline, source):
            regenerated.append(classifier.result_record(pipeline.ORDER, source_index, result))
            try:
                profile, frontiers = audit_ledger(pipeline, source, result)
            except RuntimeError:
                continue
            profile_counts[profile] = profile_counts.get(profile, 0) + 1
            record = classifier.result_record(pipeline.ORDER, source_index, result)
            records.append(record)
            for frontier in frontiers:
                null_keys.add((source_index, frontier))
    require(regenerated == expected_records,
            "order-nine atom classification differs from regeneration")
    require(profile_counts == EXPECTED_EXACT_PROFILES,
            f"exact symbolic profile counts changed: {profile_counts}")
    geometry_rows = {name: set() for name in GEOMETRIES.values()}
    for record in records:
        key = (record["profile"]["mixed"], tuple(record["profile"]["simplex_widths"]))
        geometry_rows[GEOMETRIES[key]].add(record["source_index"])
    return {
        "classification_sha256": hashlib.sha256(raw).hexdigest(),
        "decomposition_total": len(records),
        "recognized_row_total": len({record["source_index"] for record in records}),
        "geometry_row_counts": {name: len(rows) for name, rows in geometry_rows.items()},
        "exact_target_total": len(null_keys),
    }, frozenset(null_keys)


if __name__ == "__main__":
    pipeline = load_module("rank6_order9_for_symbolic_audit",
                           HERE / "rank6_order9_sparse_witness.py")
    report, keys = derive(pipeline)
    print(canonical_bytes({**report, "null_key_total": len(keys)}).decode("ascii"), end="")
