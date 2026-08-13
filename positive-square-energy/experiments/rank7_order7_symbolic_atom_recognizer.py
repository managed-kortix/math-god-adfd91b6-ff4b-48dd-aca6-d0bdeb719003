#!/usr/bin/env python3
"""Recognize exact cost-six mixed-pair/simplex geometries on thirteen paths."""

from __future__ import annotations

import argparse
import itertools
import json
import lzma
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_CENSUS = HERE / "rank7_order7_residual_census.json.xz"
F = Fraction
BUDGET = 6
ORDER = 7
PATH_COUNT = 13
SIMPLEX_COST = {3: 1, 4: 3, 5: 6}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def signed_quotient(order, contractions):
    adjacency = [[] for _ in range(order)]
    for (u, v), odd in contractions:
        relation = -1 if odd else 1
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
                elif classes[neighbor] != count or signs[neighbor] != expected:
                    return None
        count += 1
    return tuple(classes), tuple(signs), count


def simplex_profiles(cost):
    result = []

    def visit(width, remaining, chosen):
        if width == 6:
            if remaining == 0:
                result.append(tuple(chosen))
            return
        value = SIMPLEX_COST[width]
        for count in range(remaining // value + 1):
            visit(width + 1, remaining - count * value, chosen + [width] * count)

    visit(3, cost, [])
    return tuple(result)


def atom_partitions(active, target_cost):
    """Partition indexed quotient edges into complete simplex supports."""
    all_indices = frozenset(range(len(active)))
    vertices = sorted(set(itertools.chain.from_iterable(edge for edge, _ in active)))
    atoms = []
    for width, cost in SIMPLEX_COST.items():
        if cost > target_cost:
            continue
        for vertices_in_atom in itertools.combinations(vertices, width):
            choices = [tuple(index for index, (edge, _) in enumerate(active) if edge == pair)
                       for pair in itertools.combinations(vertices_in_atom, 2)]
            if not choices or not all(choices):
                continue
            for indices in itertools.product(*choices):
                if len(set(indices)) == len(indices):
                    atoms.append((frozenset(indices), width, cost, tuple(vertices_in_atom)))

    def visit(remaining, chosen, cost):
        if not remaining:
            if cost == target_cost:
                yield tuple(chosen)
            return
        if cost >= target_cost:
            return
        first = min(remaining)
        for indices, width, value, vertices_in_atom in atoms:
            if first in indices and indices <= remaining and cost + value <= target_cost:
                yield from visit(remaining - indices,
                                 chosen + [(width, indices, vertices_in_atom)], cost + value)

    yield from visit(all_indices, [], 0)


def compatible_prescriptions(mixed, atoms, active):
    prescribed = {}

    def assign(edge, value):
        if edge in prescribed and prescribed[edge] != value:
            return False
        prescribed[edge] = value
        return True

    for edge, switch in mixed:
        if not assign(edge, F(-switch, 2)):
            return None
    for width, indices, _ in atoms:
        for index in indices:
            edge, switch = active[index]
            if not assign(edge, F(-switch, width - 1)):
                return None
    return tuple(sorted(prescribed.items()))


def has_running_intersection(scopes):
    """Decide hypergraph acyclicity exactly by testing all atom join trees."""
    count = len(scopes)
    if count <= 1:
        return True
    links = tuple(itertools.combinations(range(count), 2))
    for chosen in itertools.combinations(links, count - 1):
        adjacency = [[] for _ in scopes]
        for left, right in chosen:
            adjacency[left].append(right)
            adjacency[right].append(left)
        seen = {0}
        stack = [0]
        while stack:
            stack.extend(vertex for vertex in adjacency[stack.pop()] if vertex not in seen
                         and not seen.add(vertex))
        if len(seen) != count:
            continue
        valid = True
        for vertex in set().union(*scopes):
            containing = {index for index, scope in enumerate(scopes) if vertex in scope}
            reached = {next(iter(containing))}
            stack = list(reached)
            while stack:
                current = stack.pop()
                for neighbor in adjacency[current]:
                    if neighbor in containing and neighbor not in reached:
                        reached.add(neighbor)
                        stack.append(neighbor)
            if reached != containing:
                valid = False
                break
        if valid:
            return True
    return False


def mixed_path_cycle_completion(scopes, mixed_count, atom_count):
    """Recognize the PSD `I-S/2` completion for signed paths and cycles."""
    if atom_count or mixed_count != len(scopes):
        return False
    adjacency = {}
    for scope in scopes:
        require(len(scope) == 2, "mixed atom does not have two endpoints")
        left, right = tuple(scope)
        adjacency.setdefault(left, []).append(right)
        adjacency.setdefault(right, []).append(left)
    return bool(adjacency) and all(len(neighbors) <= 2 for neighbors in adjacency.values())


def geometry_name(mixed_count, widths, scopes):
    if widths == (5,) and mixed_count == 0:
        return "regular-simplex-K5"
    if not widths:
        return "six-mixed-pairs"
    intersections = [set(scopes[i]) & set(scopes[j])
                     for i, j in itertools.combinations(range(len(scopes)), 2)]
    coupled = any(len(value) >= 2 for value in intersections)
    profile = "+".join([*(f"K{width}" for width in widths),
                        *([f"{mixed_count}M"] if mixed_count else [])])
    return ("coupled-" if coupled else "assembly-") + profile


def path_ledger(edges, row):
    paths = []
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row)):
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge_index, occurrence, (u, v), length)
                     for occurrence, length in enumerate(lengths))
    require(len(paths) == PATH_COUNT, "row does not have thirteen physical paths")
    return tuple(paths)


def recognize(edges, row):
    """Return all exact support decompositions and their equality-owner status."""
    require(len(edges) == len(row), "edge/row width mismatch")
    mandatory_contractions = []
    optional_active = []
    mixed_original = []
    for (u, v, multiplicity), odd in zip(edges, row):
        require(0 <= odd <= multiplicity, "nonphysical parity row")
        edge = (u, v)
        if (multiplicity, odd) == (2, 1):
            mixed_original.append(edge)
        elif (multiplicity, odd) == (1, 1):
            optional_active.append(edge)
        elif odd in (0, multiplicity):
            mandatory_contractions.append((edge, odd > 0))
        else:
            return ()
    remaining = BUDGET - len(mixed_original)
    if remaining < 0:
        return ()
    required_active_counts = {sum(width * (width - 1) // 2 for width in profile)
                              for profile in simplex_profiles(remaining)}
    results = []
    for kept_count in sorted(required_active_counts):
        for kept_indices in itertools.combinations(range(len(optional_active)), kept_count):
            kept = set(kept_indices)
            contractions = mandatory_contractions + [
                (edge, True) for index, edge in enumerate(optional_active) if index not in kept
            ]
            quotient = signed_quotient(ORDER, contractions)
            if quotient is None:
                continue
            classes, signs, _ = quotient
            active = []
            mixed = []
            valid = True
            for index in kept_indices:
                u, v = optional_active[index]
                edge = tuple(sorted((classes[u], classes[v])))
                if edge[0] == edge[1]:
                    valid = False
                    break
                active.append((edge, signs[u] * signs[v]))
            for u, v in mixed_original:
                edge = tuple(sorted((classes[u], classes[v])))
                if edge[0] == edge[1]:
                    valid = False
                    break
                mixed.append((edge, signs[u] * signs[v]))
            if not valid:
                continue
            for atoms in atom_partitions(tuple(active), remaining):
                prescriptions = compatible_prescriptions(tuple(mixed), atoms, tuple(active))
                if prescriptions is None:
                    continue
                widths = tuple(sorted(width for width, _, _ in atoms))
                scopes = tuple(frozenset(edge) for edge, _ in mixed) + tuple(
                    frozenset(vertices) for _, _, vertices in atoms)
                owner = (has_running_intersection(scopes) or
                         mixed_path_cycle_completion(scopes, len(mixed), len(atoms)))
                zero_support = {(edge, odd) for edge, odd in contractions}
                zero_coordinates = tuple(index for index, (_, _, edge, length) in enumerate(
                    path_ledger(edges, row)) if (edge, bool(length % 2)) in zero_support)
                results.append({
                    "geometry": geometry_name(len(mixed), widths, scopes),
                    "profile": {"mixed": len(mixed), "simplex_widths": list(widths)},
                    "status": "exact-equality-owner" if owner else "coupled-psd-open",
                    "equality_frontiers": [None, *zero_coordinates] if owner else [],
                    "contractions": [[list(edge), odd] for edge, odd in contractions],
                    "prescribed": [[list(edge), [value.numerator, value.denominator]]
                                   for edge, value in prescriptions],
                })
    unique = {json.dumps(record, sort_keys=True, separators=(",", ":")): record
              for record in results}
    return tuple(unique[key] for key in sorted(unique))


def load_census(path):
    stored = path.read_bytes()
    raw = lzma.decompress(stored) if path.suffix == ".xz" else stored
    payload = json.loads(raw.decode("ascii"))
    require(payload.get("schema") == "rank-seven-order-seven-exact-residual-census-v1",
            "wrong order-seven census")
    return payload


def scan_census(payload, limit=None):
    kernels = {record["order_kernel"]: tuple(map(tuple, record["edges"]))
               for record in payload["kernels"]}
    geometry_rows = Counter()
    status_decompositions = Counter()
    recognized = 0
    owner_rows = 0
    for source in payload["residuals"][:limit]:
        records = recognize(kernels[source["order_kernel"]], tuple(source["row"]))
        if records:
            recognized += 1
        owners = [record for record in records if record["status"] == "exact-equality-owner"]
        if owners:
            owner_rows += 1
            geometry_rows.update({record["geometry"] for record in owners})
        status_decompositions.update(record["status"] for record in records)
    return {
        "schema": "rank-seven-order-seven-symbolic-atom-scan-v1",
        "scanned_residual_total": min(len(payload["residuals"]), limit or len(payload["residuals"])),
        "recognized_candidate_row_total": recognized,
        "exact_owner_row_total": owner_rows,
        "geometry_owner_row_counts": dict(sorted(geometry_rows.items())),
        "decomposition_status_counts": dict(sorted(status_decompositions.items())),
        "full_theorem": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, default=DEFAULT_CENSUS)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--generic", help='JSON object with "edges" and "row"')
    args = parser.parse_args()
    require(args.limit is None or args.limit >= 0, "negative scan limit")
    if args.generic is not None:
        raw = json.loads(args.generic)
        require(type(raw) is dict and set(raw) == {"edges", "row"}, "bad generic row object")
        edges = tuple(tuple(value) for value in raw["edges"])
        require(all(len(edge) == 3 and all(type(value) is int for value in edge)
                    for edge in edges), "bad generic sparse edges")
        row = tuple(raw["row"])
        require(all(type(value) is int for value in row), "bad generic row")
        report = {"records": recognize(edges, row), "full_theorem": False}
    else:
        report = scan_census(load_census(args.census), args.limit)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
