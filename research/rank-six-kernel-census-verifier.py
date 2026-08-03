#!/usr/bin/env python3
"""Exact fail-closed census of loopless no-cut-vertex rank-six kernels."""

import json
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
EXPECTED_DIGEST = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
EXPECTED_COUNTS = (1, 4, 26, 84, 216, 314, 325, 162, 66)
EXPECTED_DEGREE_COUNTS = {
    "7,7": 1,
    "7,6,3": 1,
    "7,5,4": 1,
    "6,6,4": 1,
    "6,5,5": 1,
    "7,5,3,3": 2,
    "7,4,4,3": 2,
    "6,6,3,3": 4,
    "6,5,4,3": 7,
    "6,4,4,4": 2,
    "5,5,5,3": 2,
    "5,5,4,4": 7,
    "7,4,3,3,3": 4,
    "6,5,3,3,3": 11,
    "6,4,4,3,3": 18,
    "5,5,4,3,3": 26,
    "5,4,4,4,3": 20,
    "4,4,4,4,4": 5,
    "7,3,3,3,3,3": 2,
    "6,4,3,3,3,3": 29,
    "5,5,3,3,3,3": 34,
    "5,4,4,3,3,3": 101,
    "4,4,4,4,3,3": 50,
    "6,3,3,3,3,3,3": 15,
    "5,4,3,3,3,3,3": 134,
    "4,4,4,3,3,3,3": 165,
    "5,3,3,3,3,3,3,3": 55,
    "4,4,3,3,3,3,3,3": 270,
    "4,3,3,3,3,3,3,3,3": 162,
    "3,3,3,3,3,3,3,3,3,3": 66,
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(maxsize=None)
def pairs(n):
    return tuple(combinations(range(n), 2))


def degrees(n, code):
    if len(code) != n * (n - 1) // 2:
        raise ValueError("multiplicity code has wrong length")
    result = [0] * n
    for value, (u, v) in zip(code, pairs(n)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("multiplicity is not a nonnegative integer")
        result[u] += value
        result[v] += value
    return tuple(result)


def matrix_of(n, code):
    matrix = [[0] * n for _ in range(n)]
    for value, (u, v) in zip(code, pairs(n)):
        matrix[u][v] = matrix[v][u] = value
    return matrix


def connected_after_deleting(n, code, deleted):
    remaining = [vertex for vertex in range(n) if vertex != deleted]
    if len(remaining) <= 1:
        return True
    adjacency = [set() for _ in range(n)]
    for value, (u, v) in zip(code, pairs(n)):
        if value and u != deleted and v != deleted:
            adjacency[u].add(v)
            adjacency[v].add(u)
    seen = {remaining[0]}
    stack = [remaining[0]]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    return len(seen) == len(remaining)


def is_kernel(n, code):
    try:
        degree_row = degrees(n, code)
    except (TypeError, ValueError):
        return False
    return (
        isinstance(n, int)
        and not isinstance(n, bool)
        and 2 <= n <= 10
        and sum(code) == n + 5
        and min(degree_row) >= 3
        and all(connected_after_deleting(n, code, vertex) for vertex in range(n))
    )


def relabel(n, code, permutation):
    if tuple(sorted(permutation)) != tuple(range(n)):
        raise ValueError("invalid vertex permutation")
    matrix = matrix_of(n, code)
    return tuple(matrix[permutation[u]][permutation[v]] for u, v in pairs(n))


def refine_partition(matrix, partition):
    while True:
        refined = []
        changed = False
        for cell in partition:
            groups = {}
            for vertex in cell:
                signature = tuple(
                    tuple(sorted(matrix[vertex][other] for other in target))
                    for target in partition
                )
                groups.setdefault(signature, []).append(vertex)
            if len(groups) > 1:
                changed = True
            refined.extend(tuple(groups[key]) for key in sorted(groups))
        partition = tuple(refined)
        if not changed:
            return partition


def canonical_code(n, code):
    """Exact individualization-refinement canonical form."""
    matrix = matrix_of(n, code)
    degree_row = degrees(n, code)
    initial = tuple(
        tuple(vertex for vertex, value in enumerate(degree_row) if value == degree)
        for degree in sorted(set(degree_row))
    )
    best = None
    seen = set()

    def visit(partition):
        nonlocal best
        partition = refine_partition(matrix, partition)
        state = tuple(tuple(sorted(cell)) for cell in partition)
        if state in seen:
            return
        seen.add(state)
        if all(len(cell) == 1 for cell in partition):
            candidate = relabel(n, code, tuple(cell[0] for cell in partition))
            if best is None or candidate < best:
                best = candidate
            return
        index = next(index for index, cell in enumerate(partition) if len(cell) > 1)
        cell = partition[index]
        for vertex in cell:
            remainder = tuple(other for other in cell if other != vertex)
            visit(partition[:index] + ((vertex,), remainder) + partition[index + 1 :])

    visit(initial)
    require(best is not None, "canonicalization produced no labelling")
    return best


def excess_partitions(total, length, ceiling=None):
    if length == 0:
        if total == 0:
            yield ()
        return
    maximum = min(total - length + 1, total if ceiling is None else ceiling)
    for first in range(maximum, 0, -1):
        yield from (
            (first,) + rest
            for rest in excess_partitions(total - first, length - 1, first)
        )


def incidence_solutions(degree_row):
    n = len(degree_row)
    matrix = [[0] * n for _ in range(n)]

    def visit(vertex, target, residual):
        if vertex == n - 1:
            if residual[vertex] == 0:
                yield tuple(matrix[u][v] for u, v in pairs(n))
            return
        if target == n:
            if residual[vertex] == 0 and sum(residual[vertex + 1 :]) % 2 == 0:
                yield from visit(vertex + 1, vertex + 2, residual)
            return
        maximum = min(residual[vertex], residual[target])
        for value in range(maximum + 1):
            matrix[vertex][target] = matrix[target][vertex] = value
            updated = list(residual)
            updated[vertex] -= value
            updated[target] -= value
            yield from visit(vertex, target + 1, tuple(updated))
        matrix[vertex][target] = matrix[target][vertex] = 0

    yield from visit(0, 1, tuple(degree_row))


def multiplicity_compositions(total, slots, prefix=()):
    if slots == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from multiplicity_compositions(total - value, slots - 1, prefix + (value,))


def fixed_root_cubic_multigraphs(n):
    """Cover every cubic class using the three possible support rows at vertex zero."""
    def complete(matrix, residual):
        try:
            vertex = next(index for index, value in enumerate(residual) if value)
        except StopIteration:
            code = tuple(matrix[u][v] for u, v in pairs(n))
            if all(connected_after_deleting(n, code, deleted) for deleted in range(n)):
                yield code
            return
        available = [other for other in range(vertex + 1, n) if residual[other]]
        if not available:
            return
        for row in multiplicity_compositions(residual[vertex], len(available)):
            updated = list(residual)
            updated[vertex] = 0
            for neighbor, value in zip(available, row):
                matrix[vertex][neighbor] = matrix[neighbor][vertex] = value
                updated[neighbor] -= value
            if all(value >= 0 for value in updated):
                yield from complete(matrix, tuple(updated))
            for neighbor in available:
                matrix[vertex][neighbor] = matrix[neighbor][vertex] = 0

    for root_row in ((3,), (2, 1), (1, 1, 1)):
        matrix = [[0] * n for _ in range(n)]
        residual = [3] * n
        residual[0] = 0
        for neighbor, value in enumerate(root_row, 1):
            matrix[0][neighbor] = matrix[neighbor][0] = value
            residual[neighbor] -= value
        yield from complete(matrix, tuple(residual))


def fixed_root_degree_multigraphs(degree_row):
    """Generate every class with vertex zero fixed inside its degree class."""
    n = len(degree_row)

    def complete(matrix, residual):
        try:
            vertex = next(index for index, value in enumerate(residual) if value)
        except StopIteration:
            yield tuple(matrix[u][v] for u, v in pairs(n))
            return
        available = [other for other in range(vertex + 1, n) if residual[other]]
        if not available:
            return
        for row in multiplicity_compositions(residual[vertex], len(available)):
            updated = list(residual)
            updated[vertex] = 0
            for neighbor, value in zip(available, row):
                matrix[vertex][neighbor] = matrix[neighbor][vertex] = value
                updated[neighbor] -= value
            if all(value >= 0 for value in updated):
                yield from complete(matrix, tuple(updated))
            for neighbor in available:
                matrix[vertex][neighbor] = matrix[neighbor][vertex] = 0

    for root_row in multiplicity_compositions(degree_row[0], n - 1):
        if any(
            root_row[left] < root_row[right]
            for left in range(n - 1)
            for right in range(left + 1, n - 1)
            if degree_row[left + 1] == degree_row[right + 1]
        ):
            continue
        residual = list(degree_row)
        residual[0] = 0
        if any(value > residual[index] for index, value in enumerate(root_row, 1)):
            continue
        matrix = [[0] * n for _ in range(n)]
        for neighbor, value in enumerate(root_row, 1):
            matrix[0][neighbor] = matrix[neighbor][0] = value
            residual[neighbor] -= value
        yield from complete(matrix, tuple(residual))


def top_order_cubic_multigraphs():
    """Generate order-ten cubic kernels by exact two-edge expansion from rank five."""
    bases = set()
    for code in fixed_root_cubic_multigraphs(8):
        if all(connected_after_deleting(8, code, vertex) for vertex in range(8)):
            bases.add(canonical_code(8, code))
    require(len(bases) == 16, "rank-five cubic base census changed")
    old_pairs = pairs(8)
    new_index = {edge: index for index, edge in enumerate(pairs(10))}
    for base in bases:
        support = [index for index, value in enumerate(base) if value]
        for left_position, left in enumerate(support):
            for right in support[left_position:]:
                code = [0] * len(pairs(10))
                for index, value in enumerate(base):
                    code[new_index[old_pairs[index]]] = value
                a, b = old_pairs[left]
                c, d = old_pairs[right]
                if left != right:
                    code[new_index[(a, b)]] -= 1
                    code[new_index[(c, d)]] -= 1
                    for edge in ((a, 8), (b, 8), (c, 9), (d, 9), (8, 9)):
                        code[new_index[edge]] += 1
                elif base[left] >= 2:
                    code[new_index[(a, b)]] -= 2
                    for edge in ((a, 8), (b, 8), (a, 9), (b, 9), (8, 9)):
                        code[new_index[edge]] += 1
                else:
                    code[new_index[(a, b)]] -= 1
                    for edge in ((a, 8), (8, 9), (8, 9), (b, 9)):
                        code[new_index[edge]] += 1
                yield tuple(code)


@lru_cache(maxsize=None)
def census():
    classes = []
    incidence_counts = []
    degree_counts = {}
    for n in range(2, 11):
        candidates = set()
        incidence_count = 0
        if n == 10:
            source = top_order_cubic_multigraphs()
        elif n >= 8:
            source = (
                code
                for excesses in excess_partitions(10, n)
                for degree_row in (tuple(value + 2 for value in excesses),)
                if degree_row[0] <= sum(degree_row[1:])
                for code in fixed_root_degree_multigraphs(degree_row)
            )
        else:
            source = (
                code
                for excesses in excess_partitions(10, n)
                for degree_row in (tuple(value + 2 for value in excesses),)
                if degree_row[0] <= sum(degree_row[1:])
                for code in incidence_solutions(degree_row)
            )
        for code in source:
            incidence_count += 1
            if all(connected_after_deleting(n, code, vertex) for vertex in range(n)):
                candidates.add(canonical_code(n, code))
        classes.extend((n, code) for code in sorted(candidates))
        incidence_counts.append(incidence_count)
    classes = tuple(classes)
    for n, code in classes:
        key = ",".join(map(str, sorted(degrees(n, code), reverse=True)))
        degree_counts[key] = degree_counts.get(key, 0) + 1
    return classes, tuple(incidence_counts), degree_counts


def fixture_payload(kernels):
    return {
        "schema": "rank-six-loopless-no-cut-kernels-v1",
        "beta": 6,
        "minimum_degree": 3,
        "orders": [2, 10],
        "encoding": "lexicographic upper-triangle multiplicities",
        "kernels": [{"n": n, "code": list(code)} for n, code in kernels],
    }


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def load_fixture(path=FIXTURE):
    try:
        raw = path.read_bytes()
        payload = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot read canonical fixture: {error}") from error
    require(raw == canonical_bytes(payload), "fixture is not in canonical JSON form")
    require(set(payload) == {"schema", "beta", "minimum_degree", "orders", "encoding", "kernels"},
            "fixture fields changed")
    require(payload["schema"] == "rank-six-loopless-no-cut-kernels-v1", "fixture schema changed")
    require(payload["beta"] == 6, "fixture rank changed")
    require(payload["minimum_degree"] == 3, "fixture degree policy changed")
    require(payload["orders"] == [2, 10], "fixture order range changed")
    require(payload["encoding"] == "lexicographic upper-triangle multiplicities", "fixture encoding changed")
    rows = payload["kernels"]
    require(isinstance(rows, list), "fixture kernel list is malformed")
    require(all(isinstance(row, dict) and set(row) == {"n", "code"} for row in rows),
            "fixture row fields changed")
    return tuple((row["n"], tuple(row["code"])) for row in rows), raw


def audit(path=FIXTURE, expected_digest=EXPECTED_DIGEST, expected_counts=EXPECTED_COUNTS,
          expected_degree_counts=EXPECTED_DEGREE_COUNTS):
    fixture, raw = load_fixture(path)
    require(sha256(raw).hexdigest() == expected_digest, "fixture SHA-256 changed")
    require(len(fixture) == sum(expected_counts), "fixture kernel total changed")
    require(fixture == tuple(sorted(fixture)), "fixture is not sorted")
    require(len(set(fixture)) == len(fixture), "fixture contains duplicates")
    for n, code in fixture:
        require(is_kernel(n, code), "fixture contains a non-kernel")
        require(code == canonical_code(n, code), "fixture contains a noncanonical code")
    generated, incidence_counts, degree_counts = census()
    counts = tuple(sum(n == order for n, _ in generated) for order in range(2, 11))
    require(counts == expected_counts, "counts by order changed")
    require(degree_counts == expected_degree_counts, "degree-multiset counts changed")
    require(generated == fixture, "independently regenerated list differs from fixture")
    return generated, incidence_counts, degree_counts, sha256(raw).hexdigest()


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    payload = fixture_payload(load_fixture()[0])
    mutations = []

    def add(label, mutate):
        candidate = deepcopy(payload)
        mutate(candidate)
        mutations.append((label, canonical_bytes(candidate)))

    add("deleted row", lambda value: value["kernels"].pop())
    add("duplicated row", lambda value: value["kernels"].append(deepcopy(value["kernels"][-1])))
    add("changed multiplicity", lambda value: value["kernels"][1]["code"].__setitem__(0, 2))
    add("reordered rows", lambda value: value["kernels"].__setitem__(slice(0, 2), reversed(value["kernels"][:2])))
    add("rank policy", lambda value: value.__setitem__("beta", 5))
    add("degree policy", lambda value: value.__setitem__("minimum_degree", 2))
    add("order policy", lambda value: value.__setitem__("orders", [2, 9]))
    add("extra field", lambda value: value.__setitem__("note", "unsafe"))
    mutations.append(("noncanonical JSON", json.dumps(payload, indent=2).encode("ascii")))

    import tempfile
    for label, raw in mutations:
        with tempfile.NamedTemporaryFile() as handle:
            handle.write(raw)
            handle.flush()
            expect_rejected(lambda name=handle.name: audit(Path(name)), label)
    return len(mutations)


def main():
    kernels, incidence_counts, degree_counts, digest = audit()
    mutations = hostile_self_checks()
    counts = tuple(sum(n == order for n, _ in kernels) for order in range(2, 11))
    print("rank-six kernel census: exact audit passed")
    print(f"canonical_counts_n2_to_n10: {','.join(map(str, counts))} (total {len(kernels)})")
    print(f"incidence_solutions_n2_to_n10: {','.join(map(str, incidence_counts))}")
    print(f"degree_multisets: {len(degree_counts)}")
    print(f"canonical_fixture_sha256: {digest}")
    print(f"rejected_hostile_mutations: {mutations}")


if __name__ == "__main__":
    main()
