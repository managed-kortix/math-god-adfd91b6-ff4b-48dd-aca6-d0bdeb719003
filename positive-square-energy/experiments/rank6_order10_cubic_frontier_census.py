#!/usr/bin/env python3
"""Exact cubic order-ten rank-six parity-orbit and tetrahedral census.

This is an experimental frontier reduction, not a theorem verifier.  It uses
only integer arithmetic for the DNN tetrahedral sieve and rational arithmetic
for the signed-five-cycle templates.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
OUTPUT = HERE / "rank6_order10_cubic_frontier_census.json"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
SCHEMA = "rank-six-order-ten-cubic-frontier-census-experiment-v1"
ORDER = 10
RANK = 6
PATH_COUNT = ORDER + RANK - 1
BUDGET_SCALED = 30 * (RANK - 1)
PAIRS = tuple(itertools.combinations(range(ORDER), 2))
PAIR_INDEX = {edge: index for index, edge in enumerate(PAIRS)}
EXPECTED_CYCLE_KERNELS = {9: (971,), 10: (1133,)}
EXPECTED_TOTALS = (1508832, 497572, 372115, 125457, 2007312, 8, 128)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def source_rows(order):
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "kernel fixture changed")
    payload = json.loads(raw.decode("ascii"))
    rows = tuple((number, tuple(record["code"]))
                 for number, record in enumerate(payload["kernels"], 1)
                 if record["n"] == order)
    return rows


def dense_adjacency(order, code):
    matrix = [[0] * order for _ in range(order)]
    for value, (u, v) in zip(code, itertools.combinations(range(order), 2)):
        matrix[u][v] = matrix[v][u] = value
    return matrix


def automorphisms(code):
    adjacency = dense_adjacency(ORDER, code)
    signatures = [tuple(sorted(row, reverse=True)) for row in adjacency]
    candidates = [tuple(v for v in range(ORDER) if signatures[v] == signatures[u])
                  for u in range(ORDER)]
    image = [-1] * ORDER
    used = [False] * ORDER
    result = []

    def visit():
        if all(value >= 0 for value in image):
            result.append(tuple(image))
            return
        choices = []
        for u in range(ORDER):
            if image[u] >= 0:
                continue
            allowed = [v for v in candidates[u] if not used[v] and
                       all(image[w] < 0 or adjacency[u][w] == adjacency[v][image[w]]
                           for w in range(ORDER))]
            if not allowed:
                return
            choices.append((len(allowed), u, allowed))
        _, u, allowed = min(choices)
        for v in allowed:
            image[u] = v
            used[v] = True
            visit()
            used[v] = False
            image[u] = -1

    visit()
    require(result and tuple(range(ORDER)) in result, "automorphism search lost identity")
    return tuple(result)


def support_data(code):
    support = tuple(index for index, value in enumerate(code) if value)
    multiplicities = tuple(code[index] for index in support)
    return support, multiplicities


def support_actions(support, permutations):
    sparse_index = {dense: sparse for sparse, dense in enumerate(support)}
    actions = []
    for permutation in permutations:
        action = []
        for dense in support:
            u, v = PAIRS[dense]
            image = PAIR_INDEX[tuple(sorted((permutation[u], permutation[v])))]
            require(image in sparse_index, "automorphism moved a support edge off support")
            action.append(sparse_index[image])
        actions.append(tuple(action))
    return tuple(actions)


def restricted_growth_strings(width, prefix=(0,)):
    if len(prefix) == width:
        yield prefix
        return
    for color in range(min(3, max(prefix) + 1) + 1):
        yield from restricted_growth_strings(width, prefix + (color,))


COLORINGS = tuple(restricted_growth_strings(ORDER))


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
    weights = [18 * value for value in multiplicities]
    for mask in masks:
        value = sum(weight for bit, weight in enumerate(weights) if mask & (1 << bit))
        best[mask] = min(best[mask], value)
    for bit in range(width):
        flag = 1 << bit
        for mask in range(1 << width):
            if not mask & flag and best[mask | flag] < best[mask]:
                best[mask] = best[mask | flag]
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
        code += value * scale
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


def five_cycle_support(order, code):
    pairs = tuple(itertools.combinations(range(order), 2))
    singles = tuple(edge for edge, value in zip(pairs, code) if value == 1)
    doubles = tuple(edge for edge, value in zip(pairs, code) if value == 2)
    if any(value not in (0, 1, 2) for value in code) or len(doubles) != 5:
        return None
    parent = list(range(order))

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for u, v in singles:
        u, v = root(u), root(v)
        if u == v:
            return None
        parent[v] = u
    classes = {root(vertex) for vertex in range(order)}
    if len(classes) != 5:
        return None
    degrees = {vertex: 0 for vertex in classes}
    for u, v in doubles:
        u, v = root(u), root(v)
        if u == v:
            return None
        degrees[u] += 1
        degrees[v] += 1
    return (singles, doubles) if all(value == 2 for value in degrees.values()) else None


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


def cycle_gram(order, singles, doubles, bits):
    adjacency = [[] for _ in range(order)]
    for (u, v), odd in zip(singles, bits):
        relation = -1 if odd else 1
        adjacency[u].append((v, relation))
        adjacency[v].append((u, relation))
    classes = [-1] * order
    signs = [0] * order
    class_count = 0
    for root in range(order):
        if classes[root] >= 0:
            continue
        classes[root], signs[root] = class_count, 1
        stack = [root]
        while stack:
            u = stack.pop()
            for v, relation in adjacency[u]:
                expected = signs[u] * relation
                if classes[v] < 0:
                    classes[v], signs[v] = class_count, expected
                    stack.append(v)
                else:
                    require(classes[v] == class_count and signs[v] == expected,
                            "inconsistent signed contraction")
        class_count += 1
    require(class_count == 5, "signed quotient width changed")
    quotient = [[Fraction(int(i == j)) for j in range(5)] for i in range(5)]
    for u, v in doubles:
        left, right = classes[u], classes[v]
        quotient[left][right] = quotient[right][left] = Fraction(-signs[u] * signs[v], 2)
    return [[signs[u] * signs[v] * quotient[classes[u]][classes[v]]
             for v in range(order)] for u in range(order)]


def audit_psd(gram):
    order = len(gram)
    require(all(gram[i][i] == 1 for i in range(order)), "Gram diagonal changed")
    for width in range(1, order + 1):
        for indices in itertools.combinations(range(order), width):
            minor = [[gram[u][v] for v in indices] for u in indices]
            require(determinant(minor) >= 0, "signed-cycle Gram is not PSD")


def cycle_candidate_audit():
    result = {}
    for order in (9, 10):
        candidates = {number: five_cycle_support(order, code)
                      for number, code in source_rows(order) if five_cycle_support(order, code)}
        require(tuple(candidates) == EXPECTED_CYCLE_KERNELS[order],
                f"order-{order} five-cycle candidates changed")
        for number, (singles, doubles) in candidates.items():
            for bits in itertools.product((0, 1), repeat=len(singles)):
                gram = cycle_gram(order, singles, doubles, bits)
                audit_psd(gram)
                for edge, odd in zip(singles, bits):
                    transformed = -gram[edge[0]][edge[1]] if odd else gram[edge[0]][edge[1]]
                    require(transformed == 1, "singleton contraction has nonzero cost")
                require(sum((Fraction(1, 3) + Fraction(2, 3) for _ in doubles), Fraction()) == 5,
                        "signed-cycle cost changed")
        result[order] = candidates
    return result


def candidate_row(support, multiplicities, row, specification):
    singles, doubles = specification
    values = {PAIRS[index]: (value, odd)
              for index, value, odd in zip(support, multiplicities, row)}
    return (all(values[edge][0] == 1 for edge in singles)
            and all(values[edge] == (2, 1) for edge in doubles))


def census_kernel(source, cycle_specification):
    number, code = source
    support, multiplicities = support_data(code)
    require(sum(multiplicities) == PATH_COUNT, "path count changed")
    degrees = [0] * ORDER
    for index, value in zip(support, multiplicities):
        u, v = PAIRS[index]
        degrees[u] += value
        degrees[v] += value
    require(degrees == [3] * ORDER, "order-ten kernel is not cubic")
    permutations = automorphisms(code)
    actions = support_actions(support, permutations)
    radices = tuple(value + 1 for value in multiplicities)
    physical = 1
    for radix in radices:
        physical *= radix
    seen = bytearray(physical)
    best_crossing = superset_crossing_costs(multiplicities, crossing_masks(support))
    orbit_count = certified = residual = equality = equality_residual = 0
    orbit_histogram = {}
    residual_digest = hashlib.sha256()
    for encoded in range(physical):
        if seen[encoded]:
            continue
        row = mixed_radix_decode(encoded, radices)
        orbit = {mixed_radix_encode(
            tuple(row[source] for source in action), radices) for action in actions}
        for image in orbit:
            seen[image] = 1
        representative = min(orbit)
        representative_row = mixed_radix_decode(representative, radices)
        orbit_count += 1
        orbit_histogram[len(orbit)] = orbit_histogram.get(len(orbit), 0) + 1
        cost = coarse_cost(representative_row, multiplicities, best_crossing)
        is_equality = (cycle_specification is not None and
                       candidate_row(support, multiplicities, representative_row,
                                     cycle_specification))
        equality += is_equality
        if cost <= BUDGET_SCALED:
            certified += 1
        else:
            residual += 1
            equality_residual += is_equality
            residual_digest.update(canonical_bytes(
                [number, list(representative_row), len(orbit), cost]))
    require(sum(seen) == physical, "orbit traversal missed physical rows")
    return {
        "kernel": number,
        "code": list(code),
        "support_edges": len(support),
        "parallel_excess": PATH_COUNT - len(support),
        "automorphisms": len(permutations),
        "physical_rows": physical,
        "parity_orbits": orbit_count,
        "tetrahedral_certified": certified,
        "tetrahedral_residuals": residual,
        "signed_cycle_template_orbits": equality,
        "signed_cycle_residual_orbits": equality_residual,
        "orbit_size_histogram": {str(key): orbit_histogram[key]
                                 for key in sorted(orbit_histogram)},
        "residual_stream_sha256": residual_digest.hexdigest(),
    }


def regenerate(progress=False):
    rows = source_rows(ORDER)
    require(len(rows) == 66 and rows[0][0] == 1133 and rows[-1][0] == 1198,
            "order-ten kernel interval changed")
    cycle_candidates = cycle_candidate_audit()
    ledgers = []
    for index, source in enumerate(rows, 1):
        ledger = census_kernel(source, cycle_candidates[10].get(source[0]))
        ledgers.append(ledger)
        if progress:
            print(f"[{index}/66] K{source[0]} orbits={ledger['parity_orbits']} "
                  f"residuals={ledger['tetrahedral_residuals']}", flush=True)
    residuals = sum(row["tetrahedral_residuals"] for row in ledgers)
    equality = sum(row["signed_cycle_template_orbits"] for row in ledgers)
    payload = {
        "schema": SCHEMA,
        "status": "census_complete_certificates_open",
        "full_theorem": False,
        "rank": RANK,
        "order": ORDER,
        "kernel_interval": [1133, 1198],
        "kernel_total": len(ledgers),
        "path_count": PATH_COUNT,
        "frontiers_per_residual": PATH_COUNT + 1,
        "source_sha256": SOURCE_SHA256,
        "physical_total": sum(row["physical_rows"] for row in ledgers),
        "parity_orbit_total": sum(row["parity_orbits"] for row in ledgers),
        "tetrahedral_certified_total": sum(row["tetrahedral_certified"] for row in ledgers),
        "tetrahedral_residual_total": residuals,
        "frontier_target_total": (PATH_COUNT + 1) * residuals,
        "signed_cycle_candidates": {"order9": [971], "order10": [1133]},
        "signed_cycle_template_orbit_total": equality,
        "signed_cycle_residual_orbit_total": sum(
            row["signed_cycle_residual_orbits"] for row in ledgers),
        "signed_cycle_template_target_total": (PATH_COUNT + 1) * equality,
        "strategy": "cubic support, sparse parity orbits, integer DNN tetra sieve, exact signed-C5 templates, then rational residual frontiers",
        "kernels": ledgers,
    }
    return payload


def verify(payload):
    require(payload["schema"] == SCHEMA, "schema changed")
    require(payload["status"] == "census_complete_certificates_open" and
            payload["full_theorem"] is False, "open census was theorem-promoted")
    require((payload["rank"], payload["order"], payload["kernel_interval"],
             payload["kernel_total"], payload["path_count"],
             payload["frontiers_per_residual"]) == (6, 10, [1133, 1198], 66, 15, 16),
            "scope changed")
    require(payload["source_sha256"] == SOURCE_SHA256, "source digest changed")
    require(payload["tetrahedral_certified_total"] + payload["tetrahedral_residual_total"]
            == payload["parity_orbit_total"], "tetrahedral partition changed")
    require(payload["frontier_target_total"] == 16 * payload["tetrahedral_residual_total"],
            "frontier count changed")
    require(payload["signed_cycle_candidates"] == {"order9": [971], "order10": [1133]},
            "signed-cycle lineage changed")
    require((payload["physical_total"], payload["parity_orbit_total"],
             payload["tetrahedral_certified_total"], payload["tetrahedral_residual_total"],
             payload["frontier_target_total"], payload["signed_cycle_template_orbit_total"],
             payload["signed_cycle_template_target_total"]) == EXPECTED_TOTALS,
            "exact frontier totals changed")
    require(payload["signed_cycle_residual_orbit_total"] == 8,
            "signed-cycle residual partition changed")
    require(tuple((row["kernel"], tuple(row["code"])) for row in payload["kernels"])
            == source_rows(ORDER), "kernel ledger changed")


def report(payload):
    return "\n".join((
        f"kernels={payload['kernel_total']} physical={payload['physical_total']} "
        f"orbits={payload['parity_orbit_total']}",
        f"tetrahedral_certified={payload['tetrahedral_certified_total']} "
        f"residuals={payload['tetrahedral_residual_total']} "
        f"frontier_targets={payload['frontier_target_total']}",
        f"signed_cycle_candidates=K971,K1133 order10_template_orbits="
        f"{payload['signed_cycle_template_orbit_total']} "
        f"order10_template_targets={payload['signed_cycle_template_target_total']}",
        "scope=EXACT_CENSUS_AND_STRATEGY_ONLY full_theorem=false",
    )) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--emit", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.verify is None:
        payload = regenerate(args.progress)
        verify(payload)
        require(args.output.parent.is_dir(), "output parent is missing")
        args.output.write_bytes(canonical_bytes(payload))
    else:
        raw = args.verify.read_bytes()
        payload = json.loads(raw.decode("ascii"))
        require(raw == canonical_bytes(payload), "census JSON is not canonical")
        verify(payload)
    output = report(payload)
    if sys.flags.optimize == 0 and not args.emit:
        completed = subprocess.run(
            [sys.executable, "-O", __file__, "--verify", str(args.output), "--emit"],
            check=False, capture_output=True, text=True)
        require(completed.returncode == 0 and completed.stderr == "", "optimized audit failed")
        require(completed.stdout == output, "normal and optimized outputs differ")
    sys.stdout.write(output)


if __name__ == "__main__":
    main()
