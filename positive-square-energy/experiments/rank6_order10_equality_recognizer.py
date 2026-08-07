#!/usr/bin/env python3
"""Exact atomic equality recognizer for all 125457 order-ten residual rows.

The recognizer is deliberately narrower than an equality-classification theorem:
it proves membership in the signed-five-cycle or tetrahedron-plus-apex atomic
faces and labels every other residual ``other``.  Every recognized Gram, cost,
and canonical/+2 frontier relation is checked with rational arithmetic.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
CENSUS_PATH = HERE / "rank6_order10_cubic_frontier_census.py"
STREAM_PATH = HERE / "rank6_order10_cubic_exact_rational.py"
OUTPUT = HERE / "rank6_order10_equality_recognizer.json"
SCHEMA = "rank-six-order-ten-atomic-equality-recognizer-v1"
ORDER = 10
PATH_COUNT = 15
BUDGET = Fraction(5)
F = Fraction
SOURCE_SHA256 = {
    CENSUS_PATH: "536981d000d417b7edaa94461ad3bfa6540c1f400e560c244eec585cae0000de",
    STREAM_PATH: "31c5744aa6ade7ebeebf87f2559325304665ac4966915e3f23284f19aa2c58a7",
}
ARTIFACT_SHA256 = "4344461fd13b0056f719fa6f56963095c9596ff81bdd0e4e0e962dbc0bc7ac74"
EXPECTED_GEOMETRIES = {
    "signed-five-cycle": 8,
    "tetrahedron-plus-apex": 15,
    "other": 125434,
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def lock_sources():
    for path, expected in SOURCE_SHA256.items():
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected,
                f"source digest changed: {path.name}")


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def reject_constant(value):
    raise ValueError(f"nonstandard JSON constant: {value}")


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
    require(len(gram) == ORDER and all(len(row) == ORDER for row in gram), "bad Gram order")
    require(all(gram[i][i] == 1 for i in range(ORDER)), "Gram diagonal changed")
    require(all(gram[i][j] == gram[j][i] for i in range(ORDER) for j in range(ORDER)),
            "Gram is not symmetric")
    for width in range(1, ORDER + 1):
        for indices in itertools.combinations(range(ORDER), width):
            minor = [[gram[i][j] for j in indices] for i in indices]
            require(determinant(minor) >= 0, "Gram is not positive semidefinite")


def signed_components(edges, parities):
    adjacency = [[] for _ in range(ORDER)]
    for (u, v), parity in zip(edges, parities):
        relation = -1 if parity else 1
        adjacency[u].append((v, relation))
        adjacency[v].append((u, relation))
    classes = [-1] * ORDER
    signs = [0] * ORDER
    count = 0
    for root in range(ORDER):
        if classes[root] >= 0:
            continue
        classes[root], signs[root] = count, 1
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbor, relation in adjacency[vertex]:
                expected = signs[vertex] * relation
                if classes[neighbor] < 0:
                    classes[neighbor], signs[neighbor] = count, expected
                    stack.append(neighbor)
                else:
                    require(classes[neighbor] == count and signs[neighbor] == expected,
                            "inconsistent signed contraction")
        count += 1
    return tuple(classes), tuple(signs), count


def tetra_apex_structures(census, source):
    number, _, support, multiplicities, _, _, _, _ = source
    values = {census.PAIRS[index]: value for index, value in zip(support, multiplicities)}
    singles = tuple(edge for edge, value in values.items() if value == 1)
    structures = []
    for contractions in itertools.combinations(singles, ORDER - 5):
        classes, _, count = signed_components(contractions, (0,) * len(contractions))
        if count != 5:
            continue
        quotient = {}
        for edge, multiplicity in values.items():
            if edge in contractions:
                continue
            key = tuple(sorted((classes[edge[0]], classes[edge[1]])))
            if key[0] == key[1] or key in quotient:
                break
            quotient[key] = multiplicity, edge
        else:
            if sorted(value[0] for value in quotient.values()) != [1] * 6 + [2] * 2:
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
            structures.append({
                "kernel": number,
                "contractions": tuple(sorted(contractions)),
                "mixed": tuple(sorted(quotient[key][1] for key in doubled)),
                "tetra": tuple(sorted(quotient[key][1] for key in tetra_pairs)),
            })
    unique = {tuple((key, value) for key, value in sorted(row.items())): row
              for row in structures}
    return tuple(unique.values())


def solve_switches(edges, products):
    adjacency = {}
    for (left, right), product in zip(edges, products):
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
                if neighbor in switches and switches[neighbor] != expected:
                    return None
                if neighbor not in switches:
                    switches[neighbor] = expected
                    stack.append(neighbor)
    return switches


def tetra_apex_gram(structure, row_by_edge):
    contractions = structure["contractions"]
    classes, signs, count = signed_components(
        contractions, tuple(row_by_edge[edge] for edge in contractions))
    require(count == 5, "tetrahedron-plus-apex quotient width changed")
    tetra_edges = structure["tetra"]
    switches = solve_switches(tuple((classes[u], classes[v]) for u, v in tetra_edges),
                               tuple(signs[u] * signs[v] for u, v in tetra_edges))
    if switches is None:
        return None
    mixed = structure["mixed"]
    apex = next(iter(set(classes[mixed[0][i]] for i in (0, 1)) &
                     set(classes[mixed[1][i]] for i in (0, 1))))
    tetra = tuple(vertex for vertex in range(5) if vertex != apex)
    base = [[F(int(i == j)) for j in range(5)] for i in range(5)]
    for left, right in itertools.combinations(tetra, 2):
        base[left][right] = base[right][left] = F(-switches[left] * switches[right], 3)
    prescribed = {}
    for u, v in mixed:
        other = classes[v] if classes[u] == apex else classes[u]
        prescribed[other] = F(-signs[u] * signs[v], 2)
    missing = tuple(vertex for vertex in tetra if vertex not in prescribed)
    require(len(missing) == 2, "apex prescribed-correlation count changed")
    fill = -sum(prescribed.values(), F()) / len(missing)
    prescribed.update((vertex, fill) for vertex in missing)
    for vertex, value in prescribed.items():
        base[apex][vertex] = base[vertex][apex] = value
    return [[signs[i] * signs[j] * base[classes[i]][classes[j]]
             for j in range(ORDER)] for i in range(ORDER)]


def recognize_tetra_apex(census, source, structures):
    _, _, support, multiplicities, row, _, _, _ = source
    row_by_edge = {census.PAIRS[index]: odd for index, odd in zip(support, row)}
    multiplicity_by_edge = {census.PAIRS[index]: value
                            for index, value in zip(support, multiplicities)}
    recognized = []
    for structure in structures:
        if any(row_by_edge[edge] != 1 for edge in structure["tetra"]):
            continue
        if any(multiplicity_by_edge[edge] != 2 or row_by_edge[edge] != 1
               for edge in structure["mixed"]):
            continue
        gram = tetra_apex_gram(structure, row_by_edge)
        if gram is None:
            continue
        try:
            audit_atomic_geometry(census, source, gram, set(structure["contractions"]),
                                  set(structure["mixed"]), set(structure["tetra"]))
        except RuntimeError:
            continue
        recognized.append((structure, gram))
    return tuple(recognized)


def path_cost(correlation, length):
    transformed = correlation if length % 2 == 0 else -correlation
    if transformed == 1:
        return F(0)
    if length == 1:
        return (1 - transformed) / (1 + transformed)
    require(length == 2 and transformed == F(-1, 2), "unsupported exact path atom")
    return F(2, 3)


def audit_atomic_geometry(census, source, gram, contractions, mixed, tetra):
    audit_psd(gram)
    _, _, _, _, _, _, _, _ = source
    stream = load_stream()
    paths = stream.path_ledger(census, source)
    total = F()
    zero = []
    for _, _, u, v, length in paths:
        edge = tuple(sorted((u, v)))
        correlation = gram[u][v]
        transformed = correlation if length % 2 == 0 else -correlation
        if edge in contractions:
            require(transformed == 1, "contraction has nonzero cost")
        elif edge in mixed:
            require(correlation == F(-1, 2) and length in (1, 2),
                    "mixed-pair atom changed")
        else:
            require(edge in tetra and correlation == F(-1, 3) and length == 1,
                    "tetrahedral atom changed")
        total += path_cost(correlation, length)
        zero.append(transformed == 1)
    require(total == BUDGET, "atomic canonical cost changed")
    require(sum(zero) == ORDER - 5, "zero-cost contraction count changed")
    return tuple(zero)


_STREAM = None


def load_stream():
    global _STREAM
    if _STREAM is None:
        _STREAM = load_module(STREAM_PATH, "rank6_order10_stream")
    return _STREAM


def edge_name(edge):
    return f"{edge[0]}{edge[1]}"


def target_ledger(census, source, gram, contractions, mixed, tetra):
    zero = audit_atomic_geometry(census, source, gram, contractions, mixed, tetra)
    paths = load_stream().path_ledger(census, source)
    targets = [{"frontier": None, "relation": "eq", "cost": [5, 1]}]
    for index, (path, is_zero) in enumerate(zip(paths, zero)):
        targets.append({
            "frontier": index,
            "edge": edge_name(tuple(sorted(path[2:4]))),
            "occurrence": path[1],
            "canonical_length": path[4],
            "canonical_local_cost_zero": is_zero,
            "relation": "eq" if is_zero else "lt",
        })
    require(sum(row["relation"] == "eq" for row in targets) == ORDER - 4,
            "frontier equality count changed")
    return targets


def derive(progress=False):
    lock_sources()
    census = load_module(CENSUS_PATH, "rank6_order10_census")
    stream = load_stream()
    residuals = stream.residual_rows(census, progress=False)
    require(len(residuals) == 125457, "residual universe changed")
    by_kernel = {}
    for source in residuals:
        number = source[0]
        if number not in by_kernel:
            by_kernel[number] = tetra_apex_structures(census, source)
    records = []
    counts = {"signed-five-cycle": 0, "tetrahedron-plus-apex": 0, "other": 0}
    for source_index, source in enumerate(residuals):
        number, code, support, multiplicities, row, _, _, cycle = source
        geometry = None
        gram = None
        contractions = mixed = tetra = set()
        if cycle:
            singles, doubles = census.five_cycle_support(ORDER, code)
            row_by_edge = {census.PAIRS[index]: odd for index, odd in zip(support, row)}
            gram = census.cycle_gram(ORDER, singles, doubles,
                                     tuple(row_by_edge[edge] for edge in singles))
            geometry = "signed-five-cycle"
            contractions, mixed = set(singles), set(doubles)
        else:
            matches = recognize_tetra_apex(census, source, by_kernel[number])
            require(len(matches) <= 1, "row has multiple tetrahedron-plus-apex structures")
            if matches:
                structure, gram = matches[0]
                geometry = "tetrahedron-plus-apex"
                contractions = set(structure["contractions"])
                mixed = set(structure["mixed"])
                tetra = set(structure["tetra"])
        if geometry is None:
            counts["other"] += 1
        else:
            targets = target_ledger(census, source, gram, contractions, mixed, tetra)
            records.append({
                "source_index": source_index,
                "kernel": number,
                "row": list(row),
                "geometry": geometry,
                "contractions": [edge_name(edge) for edge in sorted(contractions)],
                "canonical_cost": [5, 1],
                "targets": targets,
            })
            counts[geometry] += 1
        if progress and (source_index + 1) % 10000 == 0:
            print(f"[{source_index + 1}/125457] recognized={len(records)}", flush=True)
    equality = sum(target["relation"] == "eq" for record in records
                   for target in record["targets"])
    strict = sum(target["relation"] == "lt" for record in records
                 for target in record["targets"])
    return {
        "schema": SCHEMA,
        "full_theorem": False,
        "scope": "exact recognition of known atomic equality geometries over every order-ten cubic residual orbit",
        "residual_total": len(residuals),
        "geometry_counts": counts,
        "recognized_row_total": len(records),
        "frontier_target_total": len(residuals) * (PATH_COUNT + 1),
        "recognized_target_total": len(records) * (PATH_COUNT + 1),
        "exact_cost_five_target_total": equality,
        "strict_by_lengthening_target_total": strict,
        "other_target_total": counts["other"] * (PATH_COUNT + 1),
        "records": records,
    }


def exact_int(value, label):
    require(type(value) is int and value >= 0, f"bad {label}")


def verify(payload):
    require(type(payload) is dict and payload.get("schema") == SCHEMA, "schema changed")
    require(payload.get("full_theorem") is False, "recognizer was theorem-promoted")
    for key in ("residual_total", "recognized_row_total", "frontier_target_total",
                "recognized_target_total", "exact_cost_five_target_total",
                "strict_by_lengthening_target_total", "other_target_total"):
        exact_int(payload[key], key)
    require(payload["residual_total"] == 125457, "residual total changed")
    counts = payload["geometry_counts"]
    require(type(counts) is dict and set(counts) ==
            {"signed-five-cycle", "tetrahedron-plus-apex", "other"}, "geometry ledger changed")
    require(all(type(value) is int and value >= 0 for value in counts.values()),
            "bad geometry count")
    require(sum(counts.values()) == payload["residual_total"], "geometry partition changed")
    require(counts == EXPECTED_GEOMETRIES, "pinned geometry partition changed")
    records = payload["records"]
    require(type(records) is list and len(records) == payload["recognized_row_total"],
            "record total changed")
    require(payload["recognized_row_total"] == counts["signed-five-cycle"] +
            counts["tetrahedron-plus-apex"], "recognized geometry sum changed")
    require(payload["frontier_target_total"] == 16 * payload["residual_total"] and
            payload["recognized_target_total"] == 16 * payload["recognized_row_total"] and
            payload["other_target_total"] == 16 * counts["other"], "frontier totals changed")
    require(payload["exact_cost_five_target_total"] == 6 * payload["recognized_row_total"] and
            payload["strict_by_lengthening_target_total"] == 10 * payload["recognized_row_total"],
            "atomic frontier partition changed")
    seen = set()
    for record in records:
        require(type(record) is dict and set(record) == {"source_index", "kernel", "row",
                "geometry", "contractions", "canonical_cost", "targets"}, "record fields changed")
        exact_int(record["source_index"], "source index")
        require(record["source_index"] not in seen, "duplicate source index")
        seen.add(record["source_index"])
        require(record["geometry"] in ("signed-five-cycle", "tetrahedron-plus-apex"),
                "unknown geometry")
        require(record["canonical_cost"] == [5, 1] and len(record["contractions"]) == 5,
                "record cost or contractions changed")
        require(type(record["targets"]) is list and len(record["targets"]) == 16,
                "record frontier width changed")


def report(payload, digest):
    counts = payload["geometry_counts"]
    return "\n".join((
        f"residuals={payload['residual_total']} signed_cycle={counts['signed-five-cycle']} "
        f"simplex_apex={counts['tetrahedron-plus-apex']} other={counts['other']}",
        f"recognized_targets={payload['recognized_target_total']} "
        f"equality_frontiers={payload['exact_cost_five_target_total']} "
        f"strict_frontiers={payload['strict_by_lengthening_target_total']}",
        f"artifact_sha256={digest}",
        "scope=EXACT_ATOMIC_RECOGNIZER full_theorem=false",
    )) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--emit", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.verify is None:
        payload = derive(args.progress)
        verify(payload)
        require(args.output.parent.is_dir(), "output parent is missing")
        raw = canonical_bytes(payload)
        require(hashlib.sha256(raw).hexdigest() == ARTIFACT_SHA256,
                "regenerated artifact digest changed")
        temporary = args.output.with_name(args.output.name + ".tmp")
        temporary.write_bytes(raw)
        temporary.replace(args.output)
    else:
        raw = args.verify.read_bytes()
        payload = json.loads(raw.decode("ascii"), parse_constant=reject_constant)
        require(raw == canonical_bytes(payload), "artifact is not canonical JSON")
        verify(payload)
        require(hashlib.sha256(raw).hexdigest() == ARTIFACT_SHA256,
                "artifact digest changed")
        regenerated = derive(args.progress)
        require(canonical_bytes(regenerated) == raw,
                "artifact differs from exact regenerated recognizer")
    output = report(payload, hashlib.sha256(raw).hexdigest())
    if sys.flags.optimize == 0 and not args.emit:
        completed = subprocess.run([sys.executable, "-O", __file__, "--verify",
                                    str(args.output), "--emit"], check=False,
                                   capture_output=True, text=True)
        require(completed.returncode == 0 and completed.stderr == "", "optimized audit failed")
        require(completed.stdout == output, "normal and optimized outputs differ")
    sys.stdout.write(output)


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
