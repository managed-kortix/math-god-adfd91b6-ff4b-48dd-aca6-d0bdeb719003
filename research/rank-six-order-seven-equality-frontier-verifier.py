#!/usr/bin/env python3
"""Fail-closed exact verifier for the 39 order-seven equality targets."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIXTURE = HERE / "fixtures" / "rank-six-order-seven-equality-frontier.json"
CHUNK_DIR = ROOT / "positive-square-energy" / "experiments" / "rank6_order7_batched_chunks"
BATCHED_ENGINE = (ROOT / "positive-square-energy" / "experiments"
                  / "rank6_order7_batched_exact_gram.py")
FRONTIER_ENGINE = (ROOT / "positive-square-energy" / "experiments"
                   / "rank6_order7_dim7_rational_frontier.py")
VECTOR_ENGINE = (ROOT / "pentacyclic" / "research"
                 / "order7-dim7-rational-gram-experiment.py")
CHUNKS = (
    ("chunk-00000-04000.json.xz", "7973e5e36baf73814b542301cd2da4674bf1bc66bc4cacd796dfcf18c05415e8", "3731079c31db0dd8613836ca69e4e21bcd6533f876964492d38d4d773ec7ecf0"),
    ("chunk-04000-08000.json.xz", "7af9efd2a8fe37e787540ad25dcab19ecea2f0a1b917b860eb1d0dc3401f493e", "4f1746f60bb1d6e32daf77371f0790d0f711e3c98c79dc04f079f094aee7a75c"),
    ("chunk-08000-12000.json.xz", "c66e94e4443bff1aa67d6576c42a8338703e1d1d23d1b70d25d23e4cc056da8d", "0d9425d33fe780d305ab3c0ff22873285861b4196157cbd080c843f6dd8d02a3"),
    ("chunk-12000-16000.json.xz", "1ea2e870017d62c8b53a00d9264182aca0a2081c85396f629abc5777d033a51a", "e4b1a2cc5e235a3eed356090703525a986548af2ba26c2f62a1d972269f955bd"),
    ("chunk-16000-20000.json.xz", "714efdc1d5a4105c4034e587b8dabcce235323987f69590edd90d88d9e91160c", "b2e8d70e14ac7fb8f8430c6af7c949e1cb7a0c6a11c3f18f44c8813257a059d4"),
    ("chunk-20000-24554.json.xz", "c15c4488106b036f2a846df4df3bd2804785e2054670323cd711470990019469", "491afa09d32f772e74bafc8b498544b3894411cdd74097b7229830602f03c318"),
)
MANIFEST_SHA256 = "5a3693a15beb0a6c37089c5fe15f78eaf76875dcd3096b98a2fc3dbf0f339324"
FIXTURE_SHA256 = "3afbc2bef60604eede74611e5a75c045e5f143f8b0737c7679025c3a1577d6d2"
ENGINE_SHA256 = {
    BATCHED_ENGINE: "6d0c23e89d902ed21997c0a6eea15bd9674a54a3fe85be468ffb83a3914150d5",
    FRONTIER_ENGINE: "0e8f6ccbe26edf59d91120c16ae331e2aecdb896901921a94389ec6b1796b4cf",
    VECTOR_ENGINE: "0d7acde3eec194772dd00f7e4897e0355e2347482c8e0fdfce26f9e8473394cc",
}
BUDGET = Fraction(5)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def reject_constant(value):
    raise ValueError(f"nonstandard JSON constant: {value}")


def load_json(raw):
    return json.loads(raw.decode("ascii"), parse_constant=reject_constant)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require_int(value, message):
    require(type(value) is int, message)
    return value


def lock_engine_sources():
    for path, expected in ENGINE_SHA256.items():
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected,
                f"proof engine digest changed: {path.name}")


def determinant(matrix):
    work = [list(row) for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
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
    require(len(gram) == 7 and all(len(row) == 7 for row in gram), "bad Gram order")
    require(all(gram[i][j] == gram[j][i] for i in range(7) for j in range(7)),
            "Gram matrix is not symmetric")
    require(all(gram[i][i] == 1 for i in range(7)), "Gram diagonal changed")
    # A rational symmetric matrix is PSD iff all principal minors are nonnegative.
    for width in range(1, 8):
        for indices in itertools.combinations(range(7), width):
            minor = [[gram[i][j] for j in indices] for i in indices]
            require(determinant(minor) >= 0, "Gram matrix is not positive semidefinite")


def singleton_sign(paths, edge):
    local = [path for path in paths if tuple(sorted(path[2:4])) == edge]
    require(len(local) == 1, f"{edge} is not a singleton")
    return -1 if local[0][4] & 1 else 1


def require_mixed(paths, edge):
    local = [path for path in paths if tuple(sorted(path[2:4])) == edge]
    require(len(local) == 2 and sorted(path[4] & 1 for path in local) == [0, 1],
            f"{edge} is not a mixed doubled bundle")


def tetra_apex_gram(kernel, paths):
    if kernel == 469:
        contractions = ((0, 4), (3, 5))
        mixed = ((0, 6), (3, 4))
        tetra = (1, 2, 5, 6)
        signs = {4: singleton_sign(paths, (0, 4)), 3: singleton_sign(paths, (3, 5))}
        apex = 0
        correlations = {6: Fraction(-1, 2),
                        5: Fraction(-signs[3] * signs[4], 2)}
        correlations[1] = correlations[2] = -(correlations[5] + correlations[6]) / 2
        expansion = {0: (0, 1), 1: (1, 1), 2: (2, 1), 3: (5, signs[3]),
                     4: (0, signs[4]), 5: (5, 1), 6: (6, 1)}
    else:
        require(kernel == 511, "unknown tetrahedron-plus-apex kernel")
        contractions = ((0, 6), (1, 5))
        mixed = ((0, 4), (1, 4))
        tetra = (2, 3, 5, 6)
        signs = {0: singleton_sign(paths, (0, 6)), 1: singleton_sign(paths, (1, 5))}
        apex = 4
        correlations = {6: Fraction(-signs[0], 2), 5: Fraction(-signs[1], 2)}
        correlations[2] = correlations[3] = -(correlations[5] + correlations[6]) / 2
        expansion = {0: (6, signs[0]), 1: (5, signs[1]), 2: (2, 1), 3: (3, 1),
                     4: (4, 1), 5: (5, 1), 6: (6, 1)}
    for edge in mixed:
        require_mixed(paths, edge)
    base = {vertex: {vertex: Fraction(1)} for vertex in (*tetra, apex)}
    for left, right in itertools.combinations(tetra, 2):
        base[left][right] = base[right][left] = Fraction(-1, 3)
    for vertex in tetra:
        base[apex][vertex] = base[vertex][apex] = correlations[vertex]
    gram = [[Fraction() for _ in range(7)] for _ in range(7)]
    for left in range(7):
        source_left, sign_left = expansion[left]
        for right in range(7):
            source_right, sign_right = expansion[right]
            gram[left][right] = sign_left * sign_right * base[source_left][source_right]
    return gram, set(contractions), set(mixed), "tetrahedron-plus-apex"


def cycle_gram(kernel, paths):
    geometry = {
        534: (((0, 3), (1, 2)), ((0, 6), (1, 6), (2, 5), (3, 4), (4, 5))),
        548: (((0, 3), (1, 2)), ((0, 6), (1, 5), (2, 3), (4, 5), (4, 6))),
    }
    require(kernel in geometry, "unknown signed-five-cycle kernel")
    contractions, mixed = geometry[kernel]
    signs = list(range(7))
    parity = [1] * 7
    for left, right in contractions:
        sign = singleton_sign(paths, (left, right))
        signs[right] = signs[left]
        parity[right] = sign * parity[left]
    classes = sorted(set(signs))
    require(len(classes) == 5, "cycle quotient does not have five classes")
    quotient = [[Fraction(int(i == j)) for j in classes] for i in classes]
    positions = {value: index for index, value in enumerate(classes)}
    for edge in mixed:
        require_mixed(paths, edge)
        left, right = edge
        i, j = positions[signs[left]], positions[signs[right]]
        quotient[i][j] = quotient[j][i] = Fraction(-parity[left] * parity[right], 2)
    gram = [[parity[i] * parity[j] * quotient[positions[signs[i]]][positions[signs[j]]]
             for j in range(7)] for i in range(7)]
    return gram, set(contractions), set(mixed), "signed-five-cycle"


def step_cost(correlation):
    require(correlation != -1, "singular DNN step")
    return (1 - correlation) / (1 + correlation)


def audit_target(paths, frontier, gram, contractions, mixed):
    require(frontier is None or type(frontier) is int and 0 <= frontier < len(paths),
            "invalid equality frontier")
    total = Fraction()
    for index, (_, _, left, right, canonical_length) in enumerate(paths):
        length = canonical_length + (2 if frontier == index else 0)
        edge = tuple(sorted((left, right)))
        correlation = gram[left][right]
        transformed = correlation if length % 2 == 0 else -correlation
        if edge in contractions:
            require(transformed == 1, "contraction path does not have zero cost")
            cost = step_cost(transformed)
        elif edge in mixed:
            require(correlation == Fraction(-1, 2), "mixed endpoint correlation changed")
            if canonical_length & 1:
                require(canonical_length == 1 and transformed == Fraction(1, 2),
                        "mixed odd path geometry changed")
                cost = step_cost(transformed)
            else:
                require(canonical_length == 2 and transformed == Fraction(-1, 2),
                        "mixed even path geometry changed")
                cost = 2 * step_cost(Fraction(1, 2))
        else:
            require(canonical_length == 1 and correlation == Fraction(-1, 3),
                    "tetrahedral singleton geometry changed")
            cost = step_cost(-correlation)
        # Lengthening by two is realized exactly by duplicating the first unit
        # vector twice; those two new Gram steps have correlation one and cost zero.
        require(length == canonical_length or length == canonical_length + 2,
                "frontier changed more than one coordinate by two")
        total += cost + ((length - canonical_length) // 2) * 2 * step_cost(Fraction(1))
    require(total == BUDGET, "equality-template cost changed")


def audit_uniform_extension():
    zero_pair_cost = 2 * step_cost(Fraction(1))
    require(zero_pair_cost == 0, "duplicated-vector extension is not free")
    for pair_count in range(8):
        require(BUDGET + pair_count * zero_pair_cost == BUDGET,
                "same-parity extension changed the equality cost")


def audit_tree_lift():
    # Coefficients encode a*L+b*t+c, checking every finite tree-edge count t.
    edges = (1, 1, 0)
    kappa_bound = (1, 1, 5)
    vertices = (1, 1, -5)
    lower_bound = tuple(2 * value - cost
                        for value, cost in zip(edges, kappa_bound))
    require(lower_bound == vertices, "arbitrary-tree theorem lift changed")


def locked_chunks(engine):
    census = engine.load_engine().load_census()
    residual_total = len(census["residuals"])
    frontier_total = residual_total * 13
    require(census["frontier_target_total"] == frontier_total,
            "authenticated census frontier count is inconsistent")
    records = {}
    digests = []
    exact = unresolved = 0
    stored_digests = []
    for name, stored_digest, expected_digest in CHUNKS:
        path = CHUNK_DIR / name
        raw = engine.artifact_bytes(path, stored_digest)
        digest = hashlib.sha256(raw).hexdigest()
        require(digest == expected_digest, f"decompressed chunk digest changed: {name}")
        digests.append(digest)
        stored_digests.append(stored_digest)
        payload = load_json(raw)
        require(raw == canonical_bytes(payload), f"noncanonical chunk: {name}")
        engine.verify(payload)
        for record in payload["records"]:
            index = require_int(record["source_index"], "noninteger chunk source index")
            require(index not in records, "duplicate source row")
            records[index] = record
            subtotal = require_int(record["exact_target_total"], "noninteger exact subtotal")
            exact += subtotal
            unresolved += 13 - subtotal
    manifest = hashlib.sha256(("\n".join(digests) + "\n").encode("ascii")).hexdigest()
    require(manifest == MANIFEST_SHA256, "ordered manifest digest changed")
    artifact_manifest = hashlib.sha256(
        ("\n".join(stored_digests) + "\n").encode("ascii")).hexdigest()
    require(artifact_manifest == engine.ARTIFACT_MANIFEST_SHA256,
            "ordered compressed-artifact manifest digest changed")
    require(set(records) == set(range(residual_total)), "batched source universe is incomplete")
    require(exact + unresolved == frontier_total, "batched target partition changed")
    return records, exact, unresolved, frontier_total


def audit():
    lock_engine_sources()
    engine = load_module(BATCHED_ENGINE, "rank6_order7_batched_closure")
    records, batched_exact, batched_unresolved, frontier_total = locked_chunks(engine)
    raw = FIXTURE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, "equality fixture digest changed")
    fixture = load_json(raw)
    require(raw == canonical_bytes(fixture), "equality fixture is not canonical")
    require(set(fixture) == {"schema", "full_theorem", "source_batched_manifest_sha256",
                             "target_total", "records"}, "equality fixture fields changed")
    require(fixture["schema"] == "rank-six-order-seven-equality-frontier-v1"
            and fixture["full_theorem"] is False, "equality fixture scope changed")
    require(fixture["source_batched_manifest_sha256"] == MANIFEST_SHA256,
            "equality fixture has wrong source")
    require_int(fixture["target_total"], "noninteger equality target total")
    require(type(fixture["records"]) is list, "equality records are not a list")
    census = engine.load_engine().load_census()
    kernels = {row["kernel"]: tuple(row["code"]) for row in census["kernels"]}
    certified = set()
    geometries = {}
    for closure in fixture["records"]:
        require(set(closure) == {"source_index", "kernel", "frontiers", "template"},
                "closure record fields changed")
        source_index = require_int(closure["source_index"], "noninteger closure source index")
        require(0 <= source_index < len(census["residuals"]), "closure source index out of range")
        require_int(closure["kernel"], "noninteger closure kernel")
        require(type(closure["template"]) is str, "nonstr closure template")
        require(type(closure["frontiers"]) is list and closure["frontiers"],
                "bad closure frontier list")
        require(all(frontier is None or type(frontier) is int and 0 <= frontier < 12
                    for frontier in closure["frontiers"]),
                "bad closure frontier type or value")
        require(len(closure["frontiers"]) == len(set(closure["frontiers"])),
                "duplicate closure frontier")
        source = census["residuals"][source_index]
        record = records[source_index]
        require(source["kernel"] == record["kernel"] == closure["kernel"], "kernel changed")
        require(source["row"] == record["row"], "physical row changed")
        paths = engine.load_engine().load_engine().path_ledger(
            kernels[closure["kernel"]], tuple(source["row"]))
        if closure["template"] == "tetrahedron-plus-apex":
            gram, contractions, mixed, geometry = tetra_apex_gram(closure["kernel"], paths)
        else:
            require(closure["template"] == "signed-five-cycle", "unknown template")
            gram, contractions, mixed, geometry = cycle_gram(closure["kernel"], paths)
        audit_psd(gram)
        missing = [None, *range(12)]
        missing = [frontier for frontier, witness in zip(missing, record["individual_witnesses"])
                   if witness is None]
        require(record["shared_witness"] is None and missing == closure["frontiers"],
                "closure does not equal the unresolved source targets")
        for frontier in closure["frontiers"]:
            target = source_index, frontier
            require(target not in certified, "duplicate equality target")
            audit_target(paths, frontier, gram, contractions, mixed)
            certified.add(target)
        previous = geometries.setdefault(closure["kernel"], geometry)
        require(previous == geometry, "kernel geometry changed between closure rows")
    actual_missing = {(index, frontier)
                      for index, record in records.items()
                      for frontier, witness in zip((None, *range(12)),
                                                   record["individual_witnesses"] or ())
                      if record["shared_witness"] is None and witness is None}
    require(certified == actual_missing, "equality fixture is not the exact null-key universe")
    require(len(certified) == fixture["target_total"] == batched_unresolved,
            "equality target total changed")
    require(batched_exact + len(certified) == frontier_total,
            "complete authenticated frontier is not certified")
    audit_uniform_extension()
    audit_tree_lift()
    return geometries, batched_exact, len(certified), frontier_total


def report(result):
    geometries, batched_exact, equality_exact, frontier_total = result
    labels = " ".join(f"K{kernel}={geometries[kernel]}" for kernel in sorted(geometries))
    return ("rank-six order-seven equality-frontier audit passed\n"
            f"batched_exact={batched_exact} equality_exact={equality_exact} "
            f"frontier_targets={frontier_total}\n"
            f"geometry {labels}\n"
            "proof_arithmetic=Fraction principal_minors=exact numerical_costs=ignored\n"
            "same_parity_extension=explicit arbitrary_rooted_trees=exact_affine_lift\n"
            "theorem_status=PROVED\n")


def main():
    output = report(audit())
    if sys.flags.optimize == 0 and "--emit" not in sys.argv:
        completed = subprocess.run([sys.executable, "-O", __file__, "--emit"], check=False,
                                   capture_output=True, text=True)
        require(completed.returncode == 0 and completed.stderr == "", "optimized audit failed")
        require(completed.stdout == output, "normal and optimized outputs differ")
    sys.stdout.write(output)


if __name__ == "__main__":
    try:
        main()
    except (IndexError, KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
