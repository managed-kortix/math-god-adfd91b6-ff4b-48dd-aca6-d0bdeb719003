#!/usr/bin/env python3
"""Fail-closed census of loopless no-cut-vertex rank-five kernels."""

import json
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "research" / "fixtures" / "rank-five-kernels.json"
EXPECTED_DIGEST = "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884"
EXPECTED_COUNTS = (1, 3, 13, 24, 38, 23, 16)
EXPECTED_DEGREE_COUNTS = {
    "6,6": 1,
    "6,5,3": 1,
    "5,5,4": 1,
    "6,4,4": 1,
    "5,5,3,3": 4,
    "5,4,4,3": 4,
    "4,4,4,4": 3,
    "6,4,3,3": 2,
    "5,4,3,3,3": 11,
    "4,4,4,3,3": 11,
    "6,3,3,3,3": 2,
    "5,3,3,3,3,3": 7,
    "4,4,3,3,3,3": 31,
    "4,3,3,3,3,3,3": 23,
    "3,3,3,3,3,3,3,3": 16,
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
    for multiplicity, (u, v) in zip(code, pairs(n)):
        if not isinstance(multiplicity, int) or isinstance(multiplicity, bool) or multiplicity < 0:
            raise ValueError("multiplicity is not a nonnegative integer")
        result[u] += multiplicity
        result[v] += multiplicity
    return tuple(result)


def connected_after_deleting(n, code, deleted):
    remaining = [vertex for vertex in range(n) if vertex != deleted]
    if len(remaining) <= 1:
        return True
    adjacency = [set() for _ in range(n)]
    for multiplicity, (u, v) in zip(code, pairs(n)):
        if multiplicity and u != deleted and v != deleted:
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
        and 2 <= n <= 8
        and sum(code) == n + 4
        and min(degree_row) >= 3
        and all(connected_after_deleting(n, code, deleted) for deleted in range(n))
    )


def relabel(n, code, permutation):
    if tuple(sorted(permutation)) != tuple(range(n)):
        raise ValueError("invalid vertex permutation")
    matrix = [[0] * n for _ in range(n)]
    for value, (u, v) in zip(code, pairs(n)):
        matrix[u][v] = matrix[v][u] = value
    return tuple(matrix[permutation[u]][permutation[v]] for u, v in pairs(n))


@lru_cache(maxsize=None)
def all_permutations(n):
    return tuple(permutations(range(n)))


def canonical_code(n, code):
    return min(relabel(n, code, permutation) for permutation in all_permutations(n))


def degree_preserving_canonical_code(n, code):
    """Canonicalize a degree-sorted code using only equal-degree permutations."""
    degree_row = degrees(n, code)
    groups = []
    for degree in sorted(set(degree_row), reverse=True):
        groups.append(tuple(vertex for vertex, value in enumerate(degree_row) if value == degree))
    candidates = [list(range(n))]
    for group in groups:
        expanded = []
        for candidate in candidates:
            for image in permutations(group):
                updated = candidate.copy()
                for target, source in zip(group, image):
                    updated[target] = source
                expanded.append(updated)
        candidates = expanded
    return min(relabel(n, code, tuple(permutation)) for permutation in candidates)


def support_signature(n, code):
    adjacency = [set() for _ in range(n)]
    for value, (u, v) in zip(code, pairs(n)):
        if value:
            adjacency[u].add(v)
            adjacency[v].add(u)
    vertex_signatures = []
    for vertex in range(n):
        distances = [-1] * n
        distances[vertex] = 0
        queue = [vertex]
        for current in queue:
            for neighbor in adjacency[current]:
                if distances[neighbor] < 0:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        vertex_signatures.append((len(adjacency[vertex]), tuple(sorted(distances))))
    return tuple(sorted(vertex_signatures))


def canonicalize_candidates(n, candidates):
    """Collapse isomorphism classes after cheap invariant bucketing."""
    buckets = {}
    for code in candidates:
        key = (tuple(sorted(degrees(n, code), reverse=True)), support_signature(n, code))
        buckets.setdefault(key, []).append(code)
    result = set()
    for bucket in buckets.values():
        result.update(canonical_code(n, code) for code in bucket)
    return result


def degree_aware_canonical_code(n, code):
    """Full canonical code, enumerating only degree-compatible labellings."""
    degree_row = degrees(n, code)
    choices = []
    for degree in sorted(set(degree_row)):
        group = tuple(vertex for vertex, value in enumerate(degree_row) if value == degree)
        choices.append(tuple(permutations(group)))
    candidates = [()]
    for group_choices in choices:
        candidates = [prefix + group for prefix in candidates for group in group_choices]
    return min(relabel(n, code, candidate) for candidate in candidates)


def excess_partitions(total, length, ceiling=None):
    """Nonincreasing positive partitions; these drive, but do not list, kernels."""
    if length == 0:
        if total == 0:
            yield ()
        return
    maximum = min(total - length + 1, total if ceiling is None else ceiling)
    for first in range(maximum, 0, -1):
        for rest in excess_partitions(total - first, length - 1, first):
            yield (first,) + rest


def incidence_solutions(degree_row):
    """Solve the loopless incidence equations recursively, independently of the fixture."""
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

    yield from visit(0, 1, tuple(degree_row))


def support_graphs(n):
    """All labelled 2-connected simple supports, generated by edge subsets."""
    edge_pairs = pairs(n)
    for mask in range(1 << len(edge_pairs)):
        edge_count = mask.bit_count()
        if edge_count < n or edge_count > n + 4:
            continue
        code = tuple((mask >> index) & 1 for index in range(len(edge_pairs)))
        if min(degrees(n, code)) < 2:
            continue
        if all(connected_after_deleting(n, code, deleted) for deleted in range(n)):
            yield code


def cubic_graphs(n):
    """Generate labelled simple cubic graphs by recursive neighbor pairing."""
    matrix = [[0] * n for _ in range(n)]

    def visit(residual):
        try:
            vertex = next(index for index, value in enumerate(residual) if value)
        except StopIteration:
            code = tuple(matrix[u][v] for u, v in pairs(n))
            if all(connected_after_deleting(n, code, deleted) for deleted in range(n)):
                yield code
            return
        available = [other for other in range(vertex + 1, n) if residual[other] and not matrix[vertex][other]]
        demand = residual[vertex]
        for neighbors in combinations(available, demand):
            updated = list(residual)
            updated[vertex] = 0
            for neighbor in neighbors:
                matrix[vertex][neighbor] = matrix[neighbor][vertex] = 1
                updated[neighbor] -= 1
            if all(value >= 0 for value in updated):
                yield from visit(tuple(updated))
            for neighbor in neighbors:
                matrix[vertex][neighbor] = matrix[neighbor][vertex] = 0

    yield from visit((3,) * n)


def fixed_root_cubic_multigraphs(n):
    """Generate cubic multigraphs using the three possible multiplicity rows at 0."""
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


def canonical_cubic_code(n, code):
    """Canonicalize by fixing the first image's three neighbors, then the rest."""
    adjacency = [set() for _ in range(n)]
    for value, (u, v) in zip(code, pairs(n)):
        if value:
            adjacency[u].add(v)
            adjacency[v].add(u)
    candidates = []
    for root in range(n):
        for first_neighbors in permutations(adjacency[root]):
            prefix = (root,) + first_neighbors
            remaining = set(range(n)) - set(prefix)
            candidates.extend(relabel(n, code, prefix + suffix) for suffix in permutations(remaining))
    return min(candidates)


def multiplicity_compositions(extra, slots, prefix=()):
    if slots == 1:
        yield prefix + (extra,)
        return
    for value in range(extra + 1):
        yield from multiplicity_compositions(extra - value, slots - 1, prefix + (value,))


def expand_support(n, support):
    support_indices = [index for index, value in enumerate(support) if value]
    extra = n + 4 - len(support_indices)
    for additions in multiplicity_compositions(extra, len(support_indices)):
        code = list(support)
        for index, addition in zip(support_indices, additions):
            code[index] += addition
        code = tuple(code)
        if min(degrees(n, code)) >= 3:
            yield code


@lru_cache(maxsize=None)
def census():
    classes = set()
    degree_counts = {}
    incidence_counts = []
    for n in range(2, 9):
        incidence_count = 0
        candidates = set()
        if n == 8:
            source = fixed_root_cubic_multigraphs(n)
        else:
            source = (
                code
                for excesses in excess_partitions(8, n)
                for degree_row in (tuple(value + 2 for value in excesses),)
                if degree_row[0] <= sum(degree_row[1:])
                for code in incidence_solutions(degree_row)
            )
        for code in source:
            incidence_count += 1
            if not all(connected_after_deleting(n, code, deleted) for deleted in range(n)):
                continue
            candidates.add(canonical_cubic_code(n, code) if n == 8 else degree_aware_canonical_code(n, code))
        classes.update((n, code) for code in candidates)
        incidence_counts.append(incidence_count)
    ordered = tuple(sorted(classes))
    for n, code in ordered:
        key = ",".join(map(str, sorted(degrees(n, code), reverse=True)))
        degree_counts[key] = degree_counts.get(key, 0) + 1
    return ordered, tuple(incidence_counts), degree_counts


def fixture_payload(kernels):
    return {
        "schema": "rank-five-loopless-no-cut-kernels-v1",
        "beta": 5,
        "minimum_degree": 3,
        "orders": [2, 8],
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
    require(payload["schema"] == "rank-five-loopless-no-cut-kernels-v1", "fixture schema changed")
    require(payload["beta"] == 5, "fixture rank changed")
    require(payload["minimum_degree"] == 3, "fixture degree policy changed")
    require(payload["orders"] == [2, 8], "fixture order range changed")
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
    require(len(fixture) == 118, "fixture does not contain exactly 118 kernels")
    require(fixture == tuple(sorted(fixture)), "fixture is not sorted")
    require(len(set(fixture)) == len(fixture), "fixture contains duplicates")
    for n, code in fixture:
        require(is_kernel(n, code), "fixture contains a non-kernel")
        canonicalizer = canonical_cubic_code if n == 8 else degree_aware_canonical_code
        require(code == canonicalizer(n, code), "fixture contains a noncanonical code")
    generated, incidence_counts, degree_counts = census()
    counts = tuple(sum(n == order for n, _ in generated) for order in range(2, 9))
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
    add("rank policy", lambda value: value.__setitem__("beta", 4))
    add("degree policy", lambda value: value.__setitem__("minimum_degree", 2))
    add("order policy", lambda value: value.__setitem__("orders", [2, 7]))
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
    counts = tuple(sum(n == order for n, _ in kernels) for order in range(2, 9))
    print("rank-five kernel census: exact audit passed")
    print(f"canonical_counts_n2_to_n8: {','.join(map(str, counts))} (total {len(kernels)})")
    print(f"incidence_solutions_n2_to_n8: {','.join(map(str, incidence_counts))}")
    print(f"degree_multisets: {len(degree_counts)}")
    print(f"canonical_fixture_sha256: {digest}")
    print(f"rejected_hostile_mutations: {mutations}")


if __name__ == "__main__":
    main()
