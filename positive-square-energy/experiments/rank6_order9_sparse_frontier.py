#!/usr/bin/env python3
"""Exact sparse order-nine/rank-six frontier census and structural recognizers.

This is a finite experiment, not a theorem artifact. All tetrahedral decisions
use integer arithmetic scaled by 30. The output keeps per-kernel counts and
ordered stream commitments, but does not materialize residual or frontier rows.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
OUTPUT = HERE / "rank6_order9_sparse_frontier.json"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
SCHEMA = "rank-six-order-nine-sparse-frontier-experiment-v1"
ORDER = 9
RANK = 6
PATH_COUNT = ORDER + RANK - 1
BUDGET_SCALED = 30 * (RANK - 1)
PAIRS = tuple(itertools.combinations(range(ORDER), 2))
PAIR_INDEX = {edge: index for index, edge in enumerate(PAIRS)}
EXPECTED = {
    "physical_total": 1726000,
    "parity_orbit_total": 1108126,
    "tetrahedral_certified_total": 921831,
    "tetrahedral_residual_total": 186295,
    "frontier_target_total": 2794425,
    "signed_cycle_structure_total": 1,
    "equality_template_orbit_total": 10,
    "equality_template_target_total": 150,
    "search_target_after_templates": 2794275,
    "digests": {
        "kernel_stream_sha256": "8a805c3272e75f365eb2b4ddff995882a39054e20e9ef213daed659705355620",
        "residual_stream_sha256": "2a6f0c88d8c03116096e583235bec1688a64ee5c4af0e2f61114be73b5e31807",
        "frontier_key_stream_sha256": "8e4398963209a30141a4c2bbb1c3d4b2a722251fba2096674f20057a148698c2",
        "equality_template_stream_sha256": "19f06d56a4c0d76cfd4243a534eee0d0c9dd01a5c39449edab85d40b8c6fcefc",
    },
}
EXPECTED_JSON_SHA256 = "6db83c893bc865c215ee29cdc9ad05e076ffab3e122e5fe6c51a0b25ef657712"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def stream_line(payload):
    return canonical_bytes(payload)


def reject_constant(value):
    raise ValueError(f"nonstandard JSON constant: {value}")


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "rank-six fixture changed")
    payload = json.loads(raw.decode("ascii"), parse_constant=reject_constant)
    rows = []
    for number, record in enumerate(payload["kernels"], 1):
        if record["n"] != ORDER:
            continue
        dense = tuple(record["code"])
        require(len(dense) == len(PAIRS) and sum(dense) == PATH_COUNT,
                "order-nine kernel encoding changed")
        support = tuple(index for index, value in enumerate(dense) if value)
        multiplicities = tuple(dense[index] for index in support)
        degrees = [0] * ORDER
        for index, value in zip(support, multiplicities):
            u, v = PAIRS[index]
            degrees[u] += value
            degrees[v] += value
        require(sorted(degrees, reverse=True) == [4] + [3] * 8,
                "order-nine kernel is not near-cubic with excess one")
        rows.append((number, dense, support, multiplicities, tuple(degrees)))
    require(len(rows) == 162 and rows[0][0] == 971 and rows[-1][0] == 1132,
            "order-nine kernel interval changed")
    return tuple(rows)


def degree_class_permutations(degrees):
    classes = tuple(tuple(i for i, value in enumerate(degrees) if value == degree)
                    for degree in sorted(set(degrees), reverse=True))
    for images in itertools.product(*(itertools.permutations(cell) for cell in classes)):
        permutation = list(range(ORDER))
        for cell, image in zip(classes, images):
            for source, target in zip(cell, image):
                permutation[source] = target
        yield tuple(permutation)


def automorphism_actions(dense, support, degrees):
    sparse_index = {dense_index: index for index, dense_index in enumerate(support)}
    actions = []
    for permutation in degree_class_permutations(degrees):
        action = tuple(PAIR_INDEX[tuple(sorted((permutation[u], permutation[v])))]
                       for u, v in PAIRS)
        if tuple(dense[index] for index in action) == dense:
            actions.append(tuple(sparse_index[action[index]] for index in support))
    require(actions, "kernel has no identity automorphism")
    return tuple(actions)


def restricted_growth_strings(prefix=(0,)):
    if len(prefix) == ORDER:
        yield prefix
        return
    for color in range(min(3, max(prefix) + 1) + 1):
        yield from restricted_growth_strings(prefix + (color,))


COLORINGS = tuple(restricted_growth_strings())


def crossing_masks(support):
    edges = tuple(PAIRS[index] for index in support)
    masks = set()
    for colors in COLORINGS:
        mask = 0
        for bit, (u, v) in enumerate(edges):
            if colors[u] != colors[v]:
                mask |= 1 << bit
        masks.add(mask)
    return masks


def superset_crossing_costs(multiplicities, masks):
    width = len(multiplicities)
    infinity = 10 ** 9
    best = [infinity] * (1 << width)
    weights = tuple(18 * value for value in multiplicities)
    for mask in masks:
        best[mask] = min(best[mask], sum(weight for bit, weight in enumerate(weights)
                                         if mask & (1 << bit)))
    for bit in range(width):
        flag = 1 << bit
        for mask in range(1 << width):
            if not mask & flag and best[mask | flag] < best[mask]:
                best[mask] = best[mask | flag]
    require(best[0] == 0, "constant coloring disappeared")
    return tuple(best)


def mixed_radix_decode(code, radices):
    row = []
    for radix in radices:
        row.append(code % radix)
        code //= radix
    return tuple(row)


def mixed_radix_encode(row, radices):
    code = 0
    scale = 1
    for value, radix in zip(row, radices):
        code += scale * value
        scale *= radix
    return code


def coarse_cost(row, multiplicities, best_crossing):
    mandatory = 0
    adjustment = 0
    for bit, odd in enumerate(row):
        if odd:
            mandatory |= 1 << bit
            adjustment += 10 - 13 * odd
    return best_crossing[mandatory] + adjustment


def signed_cycle_structure(support, multiplicities):
    if sorted(multiplicities) != [1] * 4 + [2] * 5:
        return None
    singles = tuple(PAIRS[index] for index, value in zip(support, multiplicities) if value == 1)
    doubles = tuple(PAIRS[index] for index, value in zip(support, multiplicities) if value == 2)
    parent = list(range(ORDER))

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for u, v in singles:
        left, right = root(u), root(v)
        if left == right:
            return None
        parent[right] = left
    classes = {}
    labels = []
    for vertex in range(ORDER):
        labels.append(classes.setdefault(root(vertex), len(classes)))
    if len(classes) != 5:
        return None
    quotient = []
    degrees = [0] * 5
    for u, v in doubles:
        edge = tuple(sorted((labels[u], labels[v])))
        if edge[0] == edge[1] or edge in quotient:
            return None
        quotient.append(edge)
        degrees[edge[0]] += 1
        degrees[edge[1]] += 1
    if sorted(degrees) != [2] * 5:
        return None
    return {"singles": tuple(sorted(singles)), "doubles": tuple(sorted(doubles))}


def equality_row(row, multiplicities, structure):
    if structure is None:
        return False
    return all(odd == 1 for odd, value in zip(row, multiplicities) if value == 2)


def determinant(matrix):
    work = [list(row) for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return Fraction()
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


def audit_signed_cycle_structure(structure):
    require(structure is not None, "missing signed-cycle structure")
    singles = structure["singles"]
    doubles = structure["doubles"]
    for parities in itertools.product((0, 1), repeat=len(singles)):
        parent = list(range(ORDER))
        signs = [1] * ORDER
        for (u, v), parity in zip(singles, parities):
            require(parent[v] == v, "singleton structure is not an oriented forest")
            parent[v] = parent[u]
            signs[v] = signs[u] * (-1 if parity else 1)
        require(len(set(parent)) == 5, "signed quotient width changed")
        gram = [[Fraction() for _ in range(ORDER)] for _ in range(ORDER)]
        for u in range(ORDER):
            for v in range(ORDER):
                if parent[u] == parent[v]:
                    gram[u][v] = Fraction(signs[u] * signs[v])
        for u, v in doubles:
            value = Fraction(-signs[u] * signs[v], 2)
            for left in range(ORDER):
                if parent[left] != parent[u]:
                    continue
                for right in range(ORDER):
                    if parent[right] == parent[v]:
                        gram[left][right] = gram[right][left] = signs[left] * signs[right] * value
        require(all(gram[i][i] == 1 for i in range(ORDER)), "signed Gram diagonal changed")
        for (u, v), parity in zip(singles, parities):
            transformed = -gram[u][v] if parity else gram[u][v]
            require(transformed == 1, "signed singleton contraction cost changed")
        for u, v in doubles:
            require(abs(gram[u][v]) == Fraction(1, 2),
                    "signed doubled correlation changed")
        for width in range(1, ORDER + 1):
            for indices in itertools.combinations(range(ORDER), width):
                minor = [[gram[i][j] for j in indices] for i in indices]
                require(determinant(minor) >= 0, "signed-cycle Gram is not PSD")
        require(5 * (Fraction(1, 3) + Fraction(2, 3)) == 5,
                "signed-cycle equality cost changed")
        require(2 * (1 - Fraction(1)) == 0, "free equality extension changed")


def kernel_census(source, residual_digest, frontier_digest, equality_digest):
    number, dense, support, multiplicities, degrees = source
    actions = automorphism_actions(dense, support, degrees)
    best_crossing = superset_crossing_costs(multiplicities, crossing_masks(support))
    radices = tuple(value + 1 for value in multiplicities)
    physical = math.prod(radices)
    seen = bytearray(physical)
    structure = signed_cycle_structure(support, multiplicities)
    orbits = residuals = equality_orbits = 0
    orbit_histogram = {}
    for code in range(physical):
        if seen[code]:
            continue
        row = mixed_radix_decode(code, radices)
        orbit = {mixed_radix_encode(tuple(row[index] for index in action), radices)
                 for action in actions}
        for image in orbit:
            seen[image] = 1
        orbit_size = len(orbit)
        orbits += 1
        orbit_histogram[orbit_size] = orbit_histogram.get(orbit_size, 0) + 1
        cost = coarse_cost(row, multiplicities, best_crossing)
        if cost <= BUDGET_SCALED:
            continue
        residuals += 1
        residual_digest.update(stream_line([number, list(row), orbit_size, cost]))
        source_index = residual_digest.count - 1
        for frontier in (None, *range(PATH_COUNT)):
            frontier_digest.update(stream_line([source_index, number, list(row), frontier]))
        if equality_row(row, multiplicities, structure):
            equality_orbits += 1
            equality_digest.update(stream_line([source_index, number, list(row), orbit_size]))
    return {
        "kernel": number,
        "support_edges": len(support),
        "parallel_excess": PATH_COUNT - len(support),
        "automorphisms": len(actions),
        "physical_rows": physical,
        "parity_orbits": orbits,
        "tetrahedral_certified": orbits - residuals,
        "tetrahedral_residuals": residuals,
        "signed_cycle_structure": structure is not None,
        "equality_template_orbits": equality_orbits,
        "orbit_size_histogram": {str(key): orbit_histogram[key]
                                 for key in sorted(orbit_histogram)},
    }, structure


class CountingDigest:
    def __init__(self):
        self.digest = hashlib.sha256()
        self.count = 0

    def update(self, raw):
        self.digest.update(raw)
        self.count += 1

    def hexdigest(self):
        return self.digest.hexdigest()


def regenerate(progress=False):
    sources = source_kernels()
    kernel_digest = CountingDigest()
    residual_digest = CountingDigest()
    frontier_digest = CountingDigest()
    equality_digest = CountingDigest()
    ledgers = []
    structures = []
    for index, source in enumerate(sources, 1):
        number, dense, _, _, _ = source
        kernel_digest.update(stream_line([number, list(dense)]))
        ledger, structure = kernel_census(source, residual_digest, frontier_digest,
                                          equality_digest)
        ledgers.append(ledger)
        if structure is not None:
            audit_signed_cycle_structure(structure)
            structures.append({"kernel": number,
                               "singles": [f"{u}{v}" for u, v in structure["singles"]],
                               "doubles": [f"{u}{v}" for u, v in structure["doubles"]]})
        if progress:
            print(f"[{index}/162] K{number} orbits={ledger['parity_orbits']} "
                  f"residuals={ledger['tetrahedral_residuals']}", flush=True)
    residual_total = sum(row["tetrahedral_residuals"] for row in ledgers)
    equality_total = sum(row["equality_template_orbits"] for row in ledgers)
    require(residual_digest.count == residual_total, "residual stream count changed")
    require(frontier_digest.count == (PATH_COUNT + 1) * residual_total,
            "frontier stream count changed")
    require(equality_digest.count == equality_total, "equality stream count changed")
    return {
        "schema": SCHEMA,
        "status": "census_complete_certificates_open",
        "full_theorem": False,
        "rank": RANK,
        "order": ORDER,
        "degree_partition": [4] + [3] * 8,
        "degree_excess": 1,
        "kernel_interval": [971, 1132],
        "kernel_total": len(ledgers),
        "path_count": PATH_COUNT,
        "frontiers_per_residual": PATH_COUNT + 1,
        "frontier_policy": "canonical plus every one-coordinate length-plus-two target",
        "source_sha256": SOURCE_SHA256,
        "physical_total": sum(row["physical_rows"] for row in ledgers),
        "parity_orbit_total": sum(row["parity_orbits"] for row in ledgers),
        "tetrahedral_certified_total": sum(row["tetrahedral_certified"] for row in ledgers),
        "tetrahedral_residual_total": residual_total,
        "frontier_target_total": (PATH_COUNT + 1) * residual_total,
        "signed_cycle_structure_total": len(structures),
        "equality_template_orbit_total": equality_total,
        "equality_template_target_total": (PATH_COUNT + 1) * equality_total,
        "search_target_after_templates": (PATH_COUNT + 1) * (residual_total - equality_total),
        "representation": "support census with committed residual/frontier streams",
        "digests": {
            "kernel_stream_sha256": kernel_digest.hexdigest(),
            "residual_stream_sha256": residual_digest.hexdigest(),
            "frontier_key_stream_sha256": frontier_digest.hexdigest(),
            "equality_template_stream_sha256": equality_digest.hexdigest(),
        },
        "signed_cycle_structures": structures,
        "kernels": ledgers,
    }


def exact_int(value, label, minimum=0):
    require(type(value) is int and value >= minimum, f"bad {label}")


def verify(payload, pin=True):
    require(type(payload) is dict, "payload is not an object")
    require(payload["schema"] == SCHEMA and payload["status"] ==
            "census_complete_certificates_open", "schema or status changed")
    require(payload["full_theorem"] is False, "experiment was theorem-promoted")
    require((payload["rank"], payload["order"], payload["degree_partition"],
             payload["degree_excess"], payload["kernel_interval"], payload["kernel_total"],
             payload["path_count"]) == (6, 9, [4] + [3] * 8, 1, [971, 1132], 162, 14),
            "scope changed")
    require(payload["source_sha256"] == SOURCE_SHA256, "source digest changed")
    require(payload["frontiers_per_residual"] == 15 and payload["frontier_policy"] ==
            "canonical plus every one-coordinate length-plus-two target", "frontier changed")
    for key in ("physical_total", "parity_orbit_total", "tetrahedral_certified_total",
                "tetrahedral_residual_total", "frontier_target_total",
                "signed_cycle_structure_total", "equality_template_orbit_total",
                "equality_template_target_total", "search_target_after_templates"):
        exact_int(payload[key], key)
    require(payload["tetrahedral_certified_total"] + payload["tetrahedral_residual_total"] ==
            payload["parity_orbit_total"], "tetrahedral partition changed")
    require(payload["frontier_target_total"] == 15 * payload["tetrahedral_residual_total"],
            "frontier total changed")
    require(payload["equality_template_target_total"] ==
            15 * payload["equality_template_orbit_total"], "template total changed")
    require(type(payload["kernels"]) is list and len(payload["kernels"]) == 162,
            "kernel ledger changed")
    require([row["kernel"] for row in payload["kernels"]] == list(range(971, 1133)),
            "kernel ordering changed")
    require(sum(row["physical_rows"] for row in payload["kernels"]) ==
            payload["physical_total"], "physical ledger sum changed")
    require(sum(row["parity_orbits"] for row in payload["kernels"]) ==
            payload["parity_orbit_total"], "orbit ledger sum changed")
    require(sum(row["tetrahedral_certified"] for row in payload["kernels"]) ==
            payload["tetrahedral_certified_total"], "certified ledger sum changed")
    require(sum(row["tetrahedral_residuals"] for row in payload["kernels"]) ==
            payload["tetrahedral_residual_total"], "residual ledger sum changed")
    require(sum(row["equality_template_orbits"] for row in payload["kernels"]) ==
            payload["equality_template_orbit_total"], "equality ledger sum changed")
    require(payload["signed_cycle_structures"] == [{
        "kernel": 971,
        "singles": ["07", "16", "25", "34"],
        "doubles": ["08", "18", "27", "36", "45"],
    }], "signed structural recognizer changed")
    if pin:
        actual = {key: payload[key] for key in EXPECTED if key != "digests"}
        require(actual == {key: value for key, value in EXPECTED.items() if key != "digests"},
                "pinned exact totals changed")
        require(payload["digests"] == EXPECTED["digests"], "pinned stream digest changed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    if args.verify is None:
        payload = regenerate(args.progress)
        verify(payload)
        require(args.output.parent.is_dir(), "output parent is missing")
        raw = canonical_bytes(payload)
        require(hashlib.sha256(raw).hexdigest() == EXPECTED_JSON_SHA256,
                "canonical frontier artifact changed")
        temporary = args.output.with_name(args.output.name + ".tmp")
        temporary.write_bytes(raw)
        temporary.replace(args.output)
    else:
        raw = args.verify.read_bytes()
        payload = json.loads(raw.decode("ascii"), parse_constant=reject_constant)
        require(raw == canonical_bytes(payload), "frontier JSON is not canonical")
        require(hashlib.sha256(raw).hexdigest() == EXPECTED_JSON_SHA256,
                "canonical frontier artifact changed")
        verify(payload)
    print(f"kernels={payload['kernel_total']} physical={payload['physical_total']} "
          f"orbits={payload['parity_orbit_total']}")
    print(f"tetrahedral_certified={payload['tetrahedral_certified_total']} "
          f"residuals={payload['tetrahedral_residual_total']} "
          f"frontier_targets={payload['frontier_target_total']}")
    print(f"signed_structures={payload['signed_cycle_structure_total']} "
          f"equality_orbits={payload['equality_template_orbit_total']} "
          f"search_targets={payload['search_target_after_templates']}")
    print(f"json_sha256={hashlib.sha256(raw).hexdigest()}")
    print("scope=EXACT_FRONTIER_EXPERIMENT full_theorem=false")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
