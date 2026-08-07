#!/usr/bin/env python3
"""Verify the exact order-eight symbolic equality-template fixture."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
PIPELINE = HERE / "rank6_order8_sparse_pipeline.py"
FIXTURE = HERE / "rank6_order8_symbolic_templates.json"
F = Fraction
SCHEMA = "rank-six-order-eight-symbolic-templates-v1"
EXPECTED_GEOMETRY_COUNTS = {
    "signed-five-cycle": 12,
    "tetrahedron-plus-apex": 52,
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pipeline():
    spec = importlib.util.spec_from_file_location("rank6_order8_sparse", PIPELINE)
    require(spec is not None and spec.loader is not None, "cannot load sparse census")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    require(all(len(row) == order for row in gram), "nonsquare Gram")
    require(all(gram[i][i] == 1 for i in range(order)), "nonunit Gram diagonal")
    require(all(gram[i][j] == gram[j][i] for i in range(order) for j in range(order)),
            "nonsymmetric Gram")
    for width in range(1, order + 1):
        for indices in itertools.combinations(range(order), width):
            minor = [[gram[i][j] for j in indices] for i in indices]
            require(determinant(minor) >= 0, "indefinite symbolic Gram")


def edge_name(edge):
    return f"{edge[0]}{edge[1]}"


def pair(value):
    return [value.numerator, value.denominator]


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def signed_components(order, contraction_edges, contraction_parities):
    adjacency = [[] for _ in range(order)]
    for (u, v), parity in zip(contraction_edges, contraction_parities):
        relation = -1 if parity else 1
        adjacency[u].append((v, relation))
        adjacency[v].append((u, relation))
    classes = [None] * order
    signs = [None] * order
    count = 0
    for root in range(order):
        if classes[root] is not None:
            continue
        classes[root], signs[root] = count, 1
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbor, relation in adjacency[vertex]:
                expected = signs[vertex] * relation
                if classes[neighbor] is None:
                    classes[neighbor], signs[neighbor] = count, expected
                    stack.append(neighbor)
                else:
                    require(classes[neighbor] == count and signs[neighbor] == expected,
                            "inconsistent signed contraction")
        count += 1
    return tuple(classes), tuple(signs), count


def tetra_apex_structures(pipeline, source):
    number, _, support, multiplicities, _ = source
    values = {pipeline.PAIRS[index]: multiplicity
              for index, multiplicity in zip(support, multiplicities)}
    singleton_edges = tuple(edge for edge, multiplicity in values.items() if multiplicity == 1)
    for contractions in itertools.combinations(singleton_edges, 3):
        classes, _, count = signed_components(pipeline.ORDER, contractions, (0, 0, 0))
        if count != 5:
            continue
        quotient = {}
        valid = True
        for edge, multiplicity in values.items():
            if edge in contractions:
                continue
            left, right = classes[edge[0]], classes[edge[1]]
            if left == right:
                valid = False
                break
            key = tuple(sorted((left, right)))
            if key in quotient:
                valid = False
                break
            quotient[key] = (multiplicity, edge)
        if not valid or sorted(value[0] for value in quotient.values()) != [1] * 6 + [2] * 2:
            continue
        doubled = tuple(key for key, value in quotient.items() if value[0] == 2)
        common = set(doubled[0]) & set(doubled[1])
        if len(common) != 1:
            continue
        apex = next(iter(common))
        tetra = tuple(vertex for vertex in range(5) if vertex != apex)
        tetra_pairs = set(itertools.combinations(tetra, 2))
        if {key for key, value in quotient.items() if value[0] == 1} != tetra_pairs:
            continue
        yield {
            "kernel": number,
            "contractions": tuple(sorted(contractions)),
            "mixed": tuple(sorted(quotient[key][1] for key in doubled)),
            "tetra_support": tuple(sorted(quotient[key][1] for key in tetra_pairs)),
        }


def solve_switches(edges, required_products):
    adjacency = {}
    for (left, right), product in zip(edges, required_products):
        adjacency.setdefault(left, []).append((right, product))
        adjacency.setdefault(right, []).append((left, product))
    switches = {}
    for root in adjacency:
        if root in switches:
            continue
        switches[root] = 1
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbor, product in adjacency[vertex]:
                expected = switches[vertex] * product
                if neighbor in switches:
                    if switches[neighbor] != expected:
                        return None
                else:
                    switches[neighbor] = expected
                    stack.append(neighbor)
    return switches


def tetra_apex_gram(pipeline, structure, row_by_edge):
    contractions = structure["contractions"]
    contraction_parities = tuple(row_by_edge[edge] for edge in contractions)
    classes, signs, count = signed_components(pipeline.ORDER, contractions,
                                               contraction_parities)
    require(count == 5, "tetra-apex quotient width changed")
    tetra_edges = structure["tetra_support"]
    products = tuple(signs[u] * signs[v] for u, v in tetra_edges)
    switches = solve_switches(tuple((classes[u], classes[v]) for u, v in tetra_edges), products)
    if switches is None:
        return None
    mixed = structure["mixed"]
    apex_class = next(iter(set(classes[mixed[0][i]] for i in (0, 1)) &
                           set(classes[mixed[1][i]] for i in (0, 1))))
    tetra_classes = tuple(vertex for vertex in range(5) if vertex != apex_class)
    base = [[F(int(i == j)) for j in range(5)] for i in range(5)]
    for left, right in itertools.combinations(tetra_classes, 2):
        base[left][right] = base[right][left] = F(-switches[left] * switches[right], 3)
    prescribed = {}
    for u, v in mixed:
        other = classes[v] if classes[u] == apex_class else classes[u]
        prescribed[other] = F(-signs[u] * signs[v], 2)
    missing = [vertex for vertex in tetra_classes if vertex not in prescribed]
    require(len(missing) == 2, "tetra-apex missing-correlation count changed")
    switched_sum = sum((switches[vertex] * value for vertex, value in prescribed.items()), F())
    switched_fill = -switched_sum / len(missing)
    prescribed.update((vertex, switches[vertex] * switched_fill) for vertex in missing)
    for vertex, value in prescribed.items():
        base[apex_class][vertex] = base[vertex][apex_class] = value
    gram = [[signs[i] * signs[j] * base[classes[i]][classes[j]]
             for j in range(pipeline.ORDER)] for i in range(pipeline.ORDER)]
    return gram


def path_cost(correlation, parity):
    require(parity in (0, 1), "symbolic row is not singleton parity")
    transformed = correlation if parity == 0 else -correlation
    if transformed == 1:
        return F(0)
    if parity == 1:
        return (1 - transformed) / (1 + transformed)
    require(transformed == F(-1, 2), "unsupported symbolic even endpoint")
    return F(2, 3)


def recognize_tetra_apex_row(pipeline, structure, support, multiplicities, row):
    row_by_edge = {pipeline.PAIRS[index]: odd for index, odd in zip(support, row)}
    multiplicity_by_edge = {pipeline.PAIRS[index]: value
                            for index, value in zip(support, multiplicities)}
    if any(row_by_edge[edge] != 1 for edge in structure["tetra_support"]):
        return None
    if any(multiplicity_by_edge[edge] != 2 or row_by_edge[edge] != 1
           for edge in structure["mixed"]):
        return None
    gram = tetra_apex_gram(pipeline, structure, row_by_edge)
    if gram is None:
        return None
    try:
        audit_psd(gram)
        total = F()
        for edge, multiplicity in multiplicity_by_edge.items():
            correlation = gram[edge[0]][edge[1]]
            odd = row_by_edge[edge]
            if multiplicity == 1:
                total += path_cost(correlation, odd)
            else:
                require(multiplicity == 2 and odd == 1 and correlation == F(-1, 2),
                        "mixed bundle geometry changed")
                total += F(1, 3) + F(2, 3)
        require(total == pipeline.BUDGET, "tetra-apex budget is not exact")
    except RuntimeError:
        return None
    return gram


def signed_cycle_gram(pipeline, source):
    number, support, multiplicities, row, _, _, cycle = source
    require(cycle, "row is not a signed-cycle template")
    singles, doubles = pipeline.SIGNED_CYCLE_SUPPORTS[number]
    contractions = tuple(sorted(tuple(map(int, edge)) for edge in singles))
    row_by_edge = {pipeline.PAIRS[index]: odd for index, odd in zip(support, row)}
    classes, signs, count = signed_components(
        pipeline.ORDER, contractions, tuple(row_by_edge[edge] for edge in contractions))
    require(count == 5, "signed-cycle quotient width changed")
    gram = [[F() for _ in range(pipeline.ORDER)] for _ in range(pipeline.ORDER)]
    for u in range(pipeline.ORDER):
        for v in range(pipeline.ORDER):
            if classes[u] == classes[v]:
                gram[u][v] = F(signs[u] * signs[v])
    for raw_edge in doubles:
        u, v = map(int, raw_edge)
        require(classes[u] != classes[v], "doubled cycle support contracted")
        for left in range(pipeline.ORDER):
            if classes[left] != classes[u]:
                continue
            for right in range(pipeline.ORDER):
                if classes[right] == classes[v]:
                    gram[left][right] = gram[right][left] = F(-signs[left] * signs[right], 2)
    audit_psd(gram)
    return gram, contractions


def path_ledger(pipeline, support, multiplicities, row):
    paths = []
    for index, multiplicity, odd in zip(support, multiplicities, row):
        edge = pipeline.PAIRS[index]
        occurrence = 0
        if odd:
            paths.append((edge, occurrence, 1))
            occurrence += 1
            for _ in range(odd - 1):
                paths.append((edge, occurrence, 3))
                occurrence += 1
        for _ in range(multiplicity - odd):
            paths.append((edge, occurrence, 2))
            occurrence += 1
    require(len(paths) == pipeline.PATH_COUNT, "symbolic path ledger width changed")
    return tuple(paths)


def classify_targets(pipeline, source, gram, contractions):
    _, support, multiplicities, row, _, _, _ = source
    contraction_set = set(contractions)
    paths = path_ledger(pipeline, support, multiplicities, row)
    zero_cost = []
    for edge, _, length in paths:
        correlation = gram[edge[0]][edge[1]]
        transformed = correlation if length % 2 == 0 else -correlation
        if edge in contraction_set:
            require(length in (1, 2) and correlation in (F(-1), F(1)),
                    "contraction path is not zero-cost")
            require(transformed == 1,
                    "contraction parity does not match its Gram entry")
        else:
            require(transformed != 1, "noncontraction symbolic path has zero cost")
        zero_cost.append(transformed == 1)
    targets = [{"frontier": None, "relation": "eq", "cost": pair(pipeline.BUDGET)}]
    for coordinate, ((edge, occurrence, length), is_zero) in enumerate(zip(paths, zero_cost)):
        relation = "eq" if is_zero else "lt"
        targets.append({
            "frontier": coordinate,
            "edge": edge_name(edge),
            "occurrence": occurrence,
            "canonical_length": length,
            "canonical_local_cost_zero": is_zero,
            "relation": relation,
        })
    require(sum(target["relation"] == "eq" for target in targets) == 4,
            "equality frontier is not canonical plus three contractions")
    return targets


def derive_payload(pipeline):
    structures = []
    for source in pipeline.source_kernels():
        structures.extend(tetra_apex_structures(pipeline, source))
    by_kernel = {}
    for structure in structures:
        by_kernel.setdefault(structure["kernel"], []).append(structure)

    _, residuals = pipeline.census(collect_residuals=True)
    records = []
    for source_index, source in enumerate(residuals):
        number, support, multiplicities, row, _, _, cycle = source
        geometry = gram = contractions = None
        if cycle:
            geometry = "signed-five-cycle"
            gram, contractions = signed_cycle_gram(pipeline, source)
        else:
            for structure in by_kernel.get(number, ()):
                candidate = recognize_tetra_apex_row(
                    pipeline, structure, support, multiplicities, row)
                if candidate is not None:
                    require(gram is None, "equality row has multiple symbolic structures")
                    geometry = "tetrahedron-plus-apex"
                    gram = candidate
                    contractions = structure["contractions"]
        if gram is None:
            continue
        targets = classify_targets(pipeline, source, gram, contractions)
        records.append({
            "source_index": source_index,
            "kernel": number,
            "row": list(row),
            "geometry": geometry,
            "contractions": [edge_name(edge) for edge in contractions],
            "targets": targets,
        })
    equality = sum(target["relation"] == "eq" for record in records
                   for target in record["targets"])
    strict = sum(target["relation"] == "lt" for record in records
                 for target in record["targets"])
    geometry_counts = {geometry: sum(record["geometry"] == geometry for record in records)
                       for geometry in EXPECTED_GEOMETRY_COUNTS}
    require(geometry_counts == EXPECTED_GEOMETRY_COUNTS and
            len(records) == 64 and equality == 256 and strict == 640,
            "symbolic packet totals changed")
    return {
        "schema": SCHEMA,
        "full_theorem": False,
        "scope": "64 symbolic equality rows and their canonical plus 13 coordinate frontiers",
        "strictness_lemma": "lengthening a positive-cost path by two strictly lowers its DNN energy; a zero-cost contraction remains zero",
        "row_total": len(records),
        "geometry_counts": geometry_counts,
        "target_total": equality + strict,
        "exact_cost_five_total": equality,
        "strict_dnn_total": strict,
        "records": records,
    }


def load_fixture():
    raw = FIXTURE.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), "symbolic fixture is not canonical JSON")
    return raw, payload


def verify_payload(payload, derived):
    require(type(payload) is dict and payload == derived,
            "symbolic fixture differs from exact derivation")
    require(set(payload) == {"schema", "full_theorem", "scope", "strictness_lemma",
                             "row_total", "geometry_counts", "target_total",
                             "exact_cost_five_total", "strict_dnn_total", "records"},
            "symbolic fixture fields changed")
    require(payload["schema"] == SCHEMA and payload["full_theorem"] is False,
            "symbolic fixture schema changed")
    require(payload["geometry_counts"] == EXPECTED_GEOMETRY_COUNTS,
            "symbolic geometry partition changed")
    require(payload["row_total"] == len(payload["records"]) == 64 and
            payload["target_total"] == 14 * payload["row_total"] and
            payload["exact_cost_five_total"] == 4 * payload["row_total"] and
            payload["strict_dnn_total"] == 10 * payload["row_total"],
            "symbolic target totals changed")


def null_keys(payload):
    return {(record["source_index"], target["frontier"])
            for record in payload["records"] for target in record["targets"]
            if target["relation"] == "eq"}


def compare_null_set(path, expected):
    payload = json.loads(path.read_text(encoding="ascii"))
    rows = payload["null_targets"] if type(payload) is dict else payload
    require(type(rows) is list, "null set must be a list or a null_targets envelope")
    actual = set()
    for row in rows:
        require(type(row) is dict and set(row) == {"source_index", "frontier"},
                "bad null target record")
        key = (row["source_index"], row["frontier"])
        require(type(key[0]) is int and (key[1] is None or type(key[1]) is int),
                "bad null target key")
        require(key not in actual, "duplicate null target")
        actual.add(key)
    missing, unexpected = expected - actual, actual - expected
    require(not missing and not unexpected,
            f"final null set differs: missing={len(missing)} unexpected={len(unexpected)}")


def write_null_set(path, expected):
    payload = {"null_targets": [
        {"source_index": source_index, "frontier": frontier}
        for source_index, frontier in sorted(
            expected, key=lambda item: (item[0], -1 if item[1] is None else item[1]))
    ]}
    path.write_bytes(canonical_bytes(payload))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-rows", action="store_true")
    parser.add_argument("--write-fixture", action="store_true")
    parser.add_argument("--write-null-set", type=Path)
    parser.add_argument("--compare-null-set", type=Path)
    args = parser.parse_args()
    pipeline = load_pipeline()
    derived = derive_payload(pipeline)
    if args.write_fixture:
        FIXTURE.write_bytes(canonical_bytes(derived))
    raw, fixture = load_fixture()
    verify_payload(fixture, derived)
    expected = null_keys(fixture)
    if args.write_null_set is not None:
        write_null_set(args.write_null_set, expected)
    if args.compare_null_set is not None:
        compare_null_set(args.compare_null_set, expected)
    if args.list_rows:
        for record in fixture["records"]:
            print(f"source={record['source_index']} K{record['kernel']} "
                  f"geometry={record['geometry']} row={tuple(record['row'])} "
                  f"contractions={','.join(record['contractions'])}")
    counts = fixture["geometry_counts"]
    print(f"rows={fixture['row_total']} signed_cycle={counts['signed-five-cycle']} "
          f"tetra_apex={counts['tetrahedron-plus-apex']} targets={fixture['target_total']} "
          f"exact_cost5={fixture['exact_cost_five_total']} "
          f"strict_dnn={fixture['strict_dnn_total']}")
    print(f"fixture_sha256={hashlib.sha256(raw).hexdigest()} "
          f"null_set_match={str(args.compare_null_set is not None).lower()} full_theorem=false")


if __name__ == "__main__":
    main()
