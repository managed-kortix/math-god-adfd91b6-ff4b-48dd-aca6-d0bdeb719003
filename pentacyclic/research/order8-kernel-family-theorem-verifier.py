#!/usr/bin/env python3
"""Fail-closed verifier for the complete order-eight rank-five theorem."""

from __future__ import annotations

import argparse
import copy
import gc
import hashlib
import itertools
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KERNEL_SOURCE = ROOT / "research" / "fixtures" / "rank-five-kernels.json"
CENSUS_SOURCE = HERE / "order8-cubic-tetra-census.json"
CHUNK_SOURCES = tuple(HERE / f"order8-chunk{index}.json" for index in range(4))
FIXTURE = HERE / "order8-kernel-family-theorem.json"
EXPECTED_DIGESTS = {
    "kernels": "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884",
    "census": "096a3ec3213bdf02f322a33790c84b206cd65b9a665220dbd76067de25947488",
    "chunk0": "2b4f2ccdb91c4cb6e8f27da94f99afec24d36c0fd0fc0175683ee9e97cd901f3",
    "chunk1": "4714d80c3e3b5161add1f915378af0a9541181b210bafd64ce531678c6bb0929",
    "chunk2": "291beab34f3d3d3649042eea2ce55c76657aa460d59ace71615fa133b6a2b81a",
    "chunk3": "09e0d6f38b19177b54f7579d14bc05dfc37bfb6f1c5308d870106698130feccf",
    "fixture": "f1c08641de224194d871197454d7056eb0884c8972c535dd8daa5abd08a37a6f",
}
EXPECTED = {
    "kernels": 16, "physical": 46736, "orbits": 11188,
    "tetra": 7705, "residual": 3483, "targets": 45279,
    "rational": 45249, "symbolic": 30,
}
CHUNK_STARTS = (0, 871, 1742, 2613)
CHUNK_RESIDUALS = (871, 871, 871, 870)
CHUNK_TARGETS = (11323, 11323, 11323, 11310)
PAIRS = tuple(itertools.combinations(range(8), 2))
FRONTIERS = (None, *range(12))
SYMBOLIC_FRONTIERS = (None, 0, 5, 6, 11)
SINGLE_CODE_COORDINATES = (0, 16, 19, 24)
HALF = Fraction(1, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def raw_locked(path, digest, label):
    require(path.is_file(), f"missing {label}")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == digest, f"{label} digest changed")
    try:
        return json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"invalid ASCII JSON in {label}") from error


def digest_locked(path, digest, label):
    require(path.is_file(), f"missing {label}")
    actual = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            actual.update(block)
    require(actual.hexdigest() == digest, f"{label} digest changed")


def stream_chunk(path, digest, label, consume):
    """Decode one record at a time and return the small top-level metadata."""
    digest_locked(path, digest, label)
    marker = '"records":['
    decoder = json.JSONDecoder()
    try:
        with path.open("r", encoding="ascii", newline="") as source:
            prefix = ""
            while marker not in prefix:
                block = source.read(65536)
                require(block != "", f"{label} has no records array")
                prefix += block
                require(len(prefix) <= 131072, f"oversized {label} header")
            before, buffer = prefix.split(marker, 1)
            count = 0
            while True:
                buffer = buffer.lstrip()
                while not buffer:
                    block = source.read(65536)
                    require(block != "", f"truncated {label} records")
                    buffer += block
                    buffer = buffer.lstrip()
                if buffer[0] == "]":
                    suffix = buffer[1:] + source.read()
                    metadata = json.loads(before + '"records":[]' + suffix)
                    require(metadata.get("records") == [], f"bad {label} records envelope")
                    metadata.pop("records")
                    return metadata, count
                while True:
                    try:
                        record, end = decoder.raw_decode(buffer)
                        break
                    except json.JSONDecodeError as error:
                        block = source.read(65536)
                        if block == "":
                            raise RuntimeError(f"invalid JSON record in {label}") from error
                        buffer += block
                require(isinstance(record, dict), f"non-object record in {label}")
                consume(record)
                count += 1
                if count % 128 == 0:
                    gc.collect()
                buffer = buffer[end:].lstrip()
                while not buffer:
                    block = source.read(65536)
                    require(block != "", f"truncated {label} records")
                    buffer += block
                    buffer = buffer.lstrip()
                require(buffer[0] in ",]", f"bad record separator in {label}")
                if buffer[0] == ",":
                    buffer = buffer[1:]
    except UnicodeDecodeError as error:
        raise RuntimeError(f"invalid ASCII JSON in {label}") from error


def canonical_json(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def fraction(value, label):
    require(isinstance(value, list) and len(value) == 2, f"bad {label} fraction")
    require(all(isinstance(x, int) and not isinstance(x, bool) for x in value),
            f"noninteger {label} fraction")
    require(value[1] > 0, f"nonpositive {label} denominator")
    result = Fraction(value[0], value[1])
    require([result.numerator, result.denominator] == value, f"uncanonical {label} fraction")
    return result


def dot(left, right):
    require(len(left) == len(right), "vector dimensions differ")
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def rational_unit(parameters):
    square = dot(parameters, parameters)
    denominator = 1 + square
    return ((1 - square) / denominator,) + tuple(2 * x / denominator for x in parameters)


def step_cost(left, right):
    correlation = dot(left, right)
    require(correlation != -1, "antipodal path step")
    return (1 - correlation) / (1 + correlation)


def canonical_lengths(multiplicity, odd):
    require(isinstance(multiplicity, int) and isinstance(odd, int) and
            0 <= odd <= multiplicity, "invalid physical incidence")
    return (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)


def path_ledger(kernel, row, frontier):
    paths = []
    for edge, ((u, v), multiplicity, odd) in enumerate(zip(PAIRS, kernel, row)):
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)))
    require(len(paths) == 12, "rank-five order-eight path count changed")
    if frontier is not None:
        require(isinstance(frontier, int) and not isinstance(frontier, bool) and
                0 <= frontier < 12, "invalid frontier coordinate")
        edge, occurrence, u, v, length = paths[frontier]
        paths[frontier] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def key(record):
    return record["kernel"], tuple(record["row"]), record["frontier"]


def determinant(matrix):
    work = [list(row) for row in matrix]
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


def audit_psd(matrix, label):
    size = len(matrix)
    require(size and all(len(row) == size for row in matrix), f"bad {label} size")
    require(all(matrix[i][j] == matrix[j][i] for i in range(size) for j in range(size)),
            f"asymmetric {label}")
    require(all(matrix[i][i] == 1 for i in range(size)), f"bad {label} diagonal")
    for width in range(1, size + 1):
        for indices in itertools.combinations(range(size), width):
            minor = tuple(tuple(matrix[i][j] for j in indices) for i in indices)
            require(determinant(minor) >= 0, f"non-PSD {label}")


def cycle_gram(signs):
    s01, s26, s35, s47 = signs
    matrix = [[Fraction(int(i == j)) for j in range(4)] for i in range(4)]
    for u, v, value in ((0, 1, -HALF), (1, 2, -s26 * HALF),
                        (2, 3, -s35 * HALF), (3, 0, -s01 * s47 * HALF)):
        matrix[u][v] = matrix[v][u] = value
    return tuple(tuple(row) for row in matrix)


def branch_gram(signs):
    s01, s26, s35, s47 = signs
    base = cycle_gram(signs)
    assignment = ((0, 1), (0, s01), (1, 1), (2, 1),
                  (3, 1), (2, s35), (1, s26), (3, s47))
    return tuple(tuple(Fraction(si * sj) * base[i][j] for j, sj in assignment)
                 for i, si in assignment)


def encoded_matrix(matrix):
    return [[[x.numerator, x.denominator] for x in row] for row in matrix]


def parse_matrix(raw, size, label):
    matrix = tuple(tuple(fraction(x, label) for x in row) for row in raw)
    require(len(matrix) == size and all(len(row) == size for row in matrix),
            f"bad {label} order")
    return matrix


def closure_record(source):
    signs = tuple(1 if source["row"][edge] == 0 else -1
                  for edge in SINGLE_CODE_COORDINATES)
    return {
        "kernel": source["kernel"], "row": source["row"],
        "frontier": source["frontier"], "lengths": source["lengths"],
        "method": "exact_signed_cycle_support_gram",
        "single_edge_order": ["01", "26", "35", "47"],
        "single_signs": list(signs),
        "base_cycle_order": ["01", "26", "35", "47"],
        "base_gram": encoded_matrix(cycle_gram(signs)),
        "branch_gram": encoded_matrix(branch_gram(signs)),
        "cost": [4, 1],
    }


def build_fixture(unresolved):
    require(len(unresolved) == EXPECTED["symbolic"], "unresolved source partition changed")
    return {
        "schema": "rank-five-order-eight-kernel-family-theorem-v1",
        "theorem_scope": "all 16 order-eight kernels and all physical parity families",
        "source_digests": {name: EXPECTED_DIGESTS[name]
                           for name in ("kernels", "census", "chunk0", "chunk1", "chunk2", "chunk3")},
        "counts": EXPECTED,
        "frontier_policy": "canonical plus all twelve one-path length-plus-two frontiers",
        "closure_records": [closure_record(record) for record in unresolved],
    }


def audit_sources(kernels, census):
    order_eight = tuple(tuple(record["code"]) for record in kernels["kernels"]
                        if record["n"] == 8)
    require(len(order_eight) == EXPECTED["kernels"], "order-eight kernel source changed")
    checks = (("kernel_total", "kernels"), ("physical_total", "physical"),
              ("orbit_total", "orbits"), ("tetra_certified_total", "tetra"),
              ("tetra_residual_total", "residual"), ("frontier_target_total", "targets"))
    require(all(census[field] == EXPECTED[name] for field, name in checks),
            "order-eight census counts changed")
    require(census["frontiers_per_residual"] == 13 and
            census["row118_cycle_equality_residual_total"] == 1 and
            census["full_theorem"] is False, "census status changed")
    require(tuple(tuple(row["code"]) for row in census["kernels"]) == order_eight,
            "census kernel selection differs from source")
    return {row["kernel"]: tuple(row["code"]) for row in census["kernels"]}


def audit_chunk_metadata(chunk, index, record_total):
    require(chunk["source_census_sha256"] == EXPECTED_DIGESTS["census"],
            f"chunk {index} points to another census")
    require(chunk["selected_residual_start"] == CHUNK_STARTS[index] and
            chunk["selected_residual_total"] == CHUNK_RESIDUALS[index] and
            chunk["target_total"] == CHUNK_TARGETS[index], f"chunk {index} slice changed")
    require(chunk["source_residual_total"] == EXPECTED["residual"] and
            chunk["source_frontier_total"] == EXPECTED["targets"] and
            chunk["frontiers_per_residual"] == 13, f"chunk {index} source census changed")
    require(chunk["full_theorem"] is False and chunk["complete_source_cover"] is False and
            chunk["experiment_fixture_frozen"] is True, f"chunk {index} status changed")
    require(record_total == CHUNK_TARGETS[index], f"chunk {index} width changed")


def audit_rational(source, kernel):
    require(source["exact_dnn_le_4"] is True and source["witness"] is not None,
            "rational target lacks source witness")
    witness = source["witness"]
    branch_parameters = tuple(tuple(fraction(x, "branch") for x in row)
                              for row in witness["branches"])
    require(len(branch_parameters) == 8 and all(len(row) == 7 for row in branch_parameters),
            "branch stereographic dimensions changed")
    branches = tuple(rational_unit(row) for row in branch_parameters)
    paths = path_ledger(kernel, tuple(source["row"]), source["frontier"])
    require(source["lengths"] == [path[4] for path in paths], "rational lengths changed")
    require(len(witness["internals"]) == 12, "rational internal ledger changed")
    total = Fraction(0)
    for (_, _, u, v, length), raw_internal in zip(paths, witness["internals"]):
        parameters = tuple(tuple(fraction(x, "internal") for x in row)
                           for row in raw_internal)
        require(len(parameters) == length - 1 and all(len(row) == 7 for row in parameters),
                "internal stereographic dimensions changed")
        chain = [branches[u], *(rational_unit(row) for row in parameters)]
        chain.append(branches[v] if length % 2 == 0 else tuple(-x for x in branches[v]))
        total += sum((step_cost(left, right) for left, right in zip(chain, chain[1:])),
                     Fraction(0))
    require(total == fraction(witness["cost"], "cost") and total < 4,
            "strict rational cost changed")


def audit_symbolic(record, source, kernel):
    require(record["kernel"] == 118 and record["frontier"] in SYMBOLIC_FRONTIERS,
            "symbolic key left the K118 signed-cycle frontier")
    require(source["exact_dnn_le_4"] is False and source["witness"] is None,
            "symbolic key was not a raw obstruction")
    paths = path_ledger(kernel, tuple(record["row"]), record["frontier"])
    require(record["lengths"] == source["lengths"] == [path[4] for path in paths],
            "symbolic path ledger changed")
    signs = tuple(record["single_signs"])
    require(record["single_edge_order"] == ["01", "26", "35", "47"] and
            record["base_cycle_order"] == ["01", "26", "35", "47"],
            "cycle-support orders changed")
    require(signs == tuple(1 if record["row"][edge] == 0 else -1
                           for edge in SINGLE_CODE_COORDINATES), "sign transport changed")
    base = parse_matrix(record["base_gram"], 4, "base Gram")
    gram = parse_matrix(record["branch_gram"], 8, "branch Gram")
    require(base == cycle_gram(signs) and gram == branch_gram(signs),
            "stored signed-cycle Gram changed")
    audit_psd(base, "base Gram")
    audit_psd(gram, "branch Gram")

    total = Fraction(0)
    singles = {0, 5, 6, 11}
    for index, (_, _, u, v, length) in enumerate(paths):
        transformed = gram[u][v] if length % 2 == 0 else -gram[u][v]
        if index in singles:
            require(transformed == 1, "single support path is not zero-cost")
            path_cost = Fraction(0)
        elif length & 1:
            require(length == 1 and transformed == HALF, "odd doubled path changed")
            path_cost = Fraction(1, 3)
        else:
            require(length == 2 and transformed == -HALF, "even doubled path changed")
            midpoint = ((Fraction(1), HALF, -HALF),
                        (HALF, Fraction(1), HALF),
                        (-HALF, HALF, Fraction(1)))
            audit_psd(midpoint, f"path {index} midpoint Gram")
            path_cost = Fraction(2, 3)
        total += path_cost
    require(total == 4 and record["cost"] == [4, 1], "symbolic equality cost changed")


def audit_fixture_shape(fixture, kernels_by_number):
    expected = build_fixture([{
        "kernel": record["kernel"], "row": record["row"],
        "frontier": record["frontier"], "lengths": record["lengths"],
    } for record in fixture["closure_records"]])
    require(fixture == expected, "theorem fixture metadata or closure changed")
    closures = fixture["closure_records"]
    targets = [key(record) for record in closures]
    require(len(targets) == EXPECTED["symbolic"] and len(set(targets)) == len(targets),
            "symbolic closure count or uniqueness changed")
    rows = {(target[0], target[1]) for target in targets}
    require(len(rows) == 6 and all(target[0] == 118 for target in targets) and
            all({(*base, frontier) for frontier in SYMBOLIC_FRONTIERS} <= set(targets)
                for base in rows), "symbolic closure support changed")
    for record in closures:
        source = {"exact_dnn_le_4": False, "witness": None, "lengths": record["lengths"]}
        audit_symbolic(record, source, kernels_by_number[record["kernel"]])


def audit_fixture(fixture, census, kernels_by_number):
    audit_fixture_shape(fixture, kernels_by_number)
    closures = {}
    for record in fixture["closure_records"]:
        require(key(record) not in closures, "duplicate symbolic closure key")
        closures[key(record)] = record
    methods = {"strict_rational_path_vectors": 0, "exact_signed_cycle_support_gram": 0}
    missing = set()
    unresolved = []
    exact_metadata = unresolved_metadata = 0
    frontier_index = {frontier: index for index, frontier in enumerate(FRONTIERS)}

    for chunk_index, path in enumerate(CHUNK_SOURCES):
        residuals = census["residuals"][CHUNK_STARTS[chunk_index]:
                                       CHUNK_STARTS[chunk_index] + CHUNK_RESIDUALS[chunk_index]]
        residual_index = {(row["kernel"], tuple(row["row"])): index
                          for index, row in enumerate(residuals)}
        require(len(residual_index) == len(residuals), f"duplicate census row in chunk {chunk_index}")
        seen = bytearray(CHUNK_TARGETS[chunk_index])

        def consume(source):
            target = key(source)
            base = target[:2]
            require(base in residual_index and target[2] in frontier_index,
                    f"chunk {chunk_index} has an extra key")
            position = residual_index[base] * len(FRONTIERS) + frontier_index[target[2]]
            require(not seen[position], "duplicate raw result key")
            seen[position] = 1
            kernel = kernels_by_number[source["kernel"]]
            if source["exact_dnn_le_4"]:
                audit_rational(source, kernel)
                methods["strict_rational_path_vectors"] += 1
            else:
                require(target in closures, "raw obstruction lacks symbolic closure")
                audit_symbolic(closures[target], source, kernel)
                methods["exact_signed_cycle_support_gram"] += 1
                missing.add(target)
                unresolved.append(source)

        metadata, record_total = stream_chunk(
            path, EXPECTED_DIGESTS[f"chunk{chunk_index}"], f"result chunk {chunk_index}", consume)
        audit_chunk_metadata(metadata, chunk_index, record_total)
        require(all(seen), f"chunk {chunk_index} keys have omissions")
        exact_metadata += metadata["exact_certificate_total"]
        unresolved_metadata += metadata["finite_unresolved_total"]

    require(exact_metadata == EXPECTED["rational"] and
            unresolved_metadata == EXPECTED["symbolic"], "chunk certificate partition changed")
    require(methods == {"strict_rational_path_vectors": EXPECTED["rational"],
                        "exact_signed_cycle_support_gram": EXPECTED["symbolic"]},
            "verified certificate partition changed")
    require(set(closures) == missing, "symbolic keys differ from raw missing keys")
    require(fixture == build_fixture(unresolved), "fixture differs from streamed reconstruction")
    rows = {(target[0], target[1]) for target in missing}
    require(len(rows) == 6 and {target[2] for target in missing} == set(SYMBOLIC_FRONTIERS),
            "symbolic six-row/five-frontier support changed")
    require(all(sum(target[2] == frontier for target in missing) == 6
                for frontier in SYMBOLIC_FRONTIERS), "symbolic frontier multiplicity changed")
    return methods, missing


def hostile_mutations(fixture, kernels_by_number):
    attacks = []

    def add(name, mutate):
        candidate = copy.deepcopy(fixture)
        mutate(candidate)
        attacks.append((name, candidate))

    add("delete closure", lambda x: x["closure_records"].pop())
    add("duplicate closure", lambda x: x["closure_records"].append(copy.deepcopy(x["closure_records"][0])))
    add("forge rational count", lambda x: x["counts"].__setitem__("rational", 45250))
    add("change parity row", lambda x: x["closure_records"][0]["row"].__setitem__(0, 1))
    add("change frontier", lambda x: x["closure_records"][0].__setitem__("frontier", 1))
    add("change sign", lambda x: x["closure_records"][0]["single_signs"].__setitem__(0, -1))
    add("change base Gram", lambda x: x["closure_records"][0]["base_gram"][0].__setitem__(1, [0, 1]))
    add("change branch Gram", lambda x: x["closure_records"][0]["branch_gram"][0].__setitem__(1, [0, 1]))
    add("change path cost", lambda x: x["closure_records"][0].__setitem__("cost", [3, 1]))
    add("change chunk lock", lambda x: x["source_digests"].__setitem__("chunk3", "0" * 64))
    for name, candidate in attacks:
        try:
            audit_fixture_shape(candidate, kernels_by_number)
        except (RuntimeError, KeyError, IndexError, TypeError, ZeroDivisionError):
            continue
        raise RuntimeError(f"hostile mutation accepted: {name}")
    return len(attacks)


def load_sources(check_fixture=True):
    kernels = raw_locked(KERNEL_SOURCE, EXPECTED_DIGESTS["kernels"], "kernel fixture")
    census = raw_locked(CENSUS_SOURCE, EXPECTED_DIGESTS["census"], "tetra census")
    fixture = None
    if check_fixture:
        fixture = raw_locked(FIXTURE, EXPECTED_DIGESTS["fixture"], "theorem fixture")
    return kernels, census, fixture


def regenerate():
    kernels, census, _ = load_sources(False)
    kernels_by_number = audit_sources(kernels, census)
    fixture = raw_locked(FIXTURE, EXPECTED_DIGESTS["fixture"], "theorem fixture")
    audit_fixture(fixture, census, kernels_by_number)
    FIXTURE.write_bytes(canonical_json(fixture))
    print(hashlib.sha256(FIXTURE.read_bytes()).hexdigest())


def report(methods, missing, attacks):
    return "\n".join((
        "order-eight rank-five kernel-family theorem: exact audit passed",
        "kernels=16 physical=46736 orbits=11188 tetra_certified=7705 residual=3483",
        f"all_length_targets=45279 rational={methods['strict_rational_path_vectors']} "
        f"symbolic_K118={methods['exact_signed_cycle_support_gram']}",
        "exact_missing_keys=K118:30 parity_rows=6 frontiers=canonical,0,5,6,11",
        "attachments=arbitrary_rooted_trees conclusion=s+(G)>=|V(G)|",
        f"hostile_mutations_rejected={attacks} verified_missing={len(missing)}",
    )) + "\n"


def optimized_output():
    completed = subprocess.run([sys.executable, "-O", str(Path(__file__).resolve()), "--emit"],
                               check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O theorem verifier failed")
    require(completed.stderr == "", "python -O theorem verifier wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--regenerate", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    require(not (args.regenerate and args.emit), "incompatible arguments")
    if args.regenerate:
        regenerate()
        return
    kernels, census, fixture = load_sources()
    kernels_by_number = audit_sources(kernels, census)
    methods, missing = audit_fixture(fixture, census, kernels_by_number)
    attacks = hostile_mutations(fixture, kernels_by_number)
    output = report(methods, missing, attacks)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)


if __name__ == "__main__":
    main()
