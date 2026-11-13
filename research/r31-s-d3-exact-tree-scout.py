#!/usr/bin/env python3
"""Independent bounded scout for the open R31-S:D3 spectral packet.

The theorem target is sigma(G)=s^+(G)-|V(G)|>3 for a diamond
Theta(1,2,2), three legally incident triangular blocks, and arbitrary rooted
trees.  This program does *not* prove the unbounded theorem.  It independently
regenerates the 14 one-side incidence records and supports two deliberately
separate modes:

* ``--mode numeric`` ranks a complete bounded attachment census with NumPy.
  Those values are scouting data only and are never accepted as a conclusion.
* ``--mode exact`` recomputes integer characteristic polynomials and uses only
  ``fractions.Fraction`` Sturm isolation (with multiplicities) to certify every
  graph in the requested bounded census, or a supplied numeric low tail.
* ``--mode stars`` exactly stress-tests a reproducible large pendant-star
  family after removing its known zero-eigenvalue factors.

A rooted attachment at a core vertex is an unlabeled rooted tree with its root
identified with that vertex.  Bounding ``--extra`` by B means that the sum of
non-root attachment vertices over all ten core vertices is at most B.  A union
of several branches at one core vertex is represented by their single rooted
union, so this is the natural exhaustive bounded model.

No SymPy, NetworkX, PARI, or floating point is used in exact mode.  The exact
characteristic polynomial is accelerated by the coalescence identity

  phi_G = sum_{S subset A} phi_(H-S) prod_(v in S) c_v prod_(v in A-S) d_v,

where d_v=phi_(T_v-r_v) and c_v=phi_(T_v)-x d_v.  Core minors are independently
computed by integer Newton identities.  Exact mode also checks selected full
adjacency characteristic polynomials directly against the coalescence result.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Iterator


Record = tuple
Tree = tuple["Tree", ...]
Graph = tuple[int, frozenset[tuple[int, int]]]
Poly = list[int]  # coefficients in descending order


class ScoutError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ScoutError(message)


def add_edge(edges: set[tuple[int, int]], left: int, right: int) -> None:
    require(left != right, "loop requested")
    edges.add(tuple(sorted((left, right))))


def records() -> tuple[Record, ...]:
    """Regenerate the 14 one-side records without importing the old verifier."""
    owners = ("A", "B", "x")
    direct = {
        ("direct3", roots)
        for roots in itertools.combinations_with_replacement(owners, 3)
        if "x" in roots
    }
    chain_direct = {
        ("chain2+direct", upstream, direct_root)
        for upstream in owners
        for direct_root in owners
        if "x" in (upstream, direct_root)
    }
    fork = {("fork", "x", occupancy) for occupancy in ("same", "split")}
    chain = {("chain3", "x")}
    result = tuple(sorted(direct | chain_direct | fork | chain, key=repr))
    require(len(result) == 14, "one-side record count changed")
    require(Counter(row[0] for row in result) == Counter({
        "direct3": 6,
        "chain2+direct": 5,
        "fork": 2,
        "chain3": 1,
    }), "one-side shape census changed")
    return result


def bare_named_graph(record: Record) -> tuple[tuple[str, ...], frozenset[tuple[int, int]]]:
    """Realize D=Theta(1,2,2) and the three triangular block incidences.

    The sorted name order is part of the attachment certificate: an assignment
    such as ``8:(()())`` is otherwise not independently interpretable.
    """
    names = {"A", "B", "x", "z"}
    named_edges = {
        tuple(sorted(edge))
        for edge in (("A", "B"), ("A", "x"), ("B", "x"),
                     ("A", "z"), ("B", "z"))
    }

    def triangle(root: str, label: str) -> tuple[str, str]:
        left, right = f"{label}a", f"{label}b"
        names.update((left, right))
        named_edges.update(tuple(sorted(edge)) for edge in
                           ((root, left), (left, right), (right, root)))
        return left, right

    kind = record[0]
    if kind == "direct3":
        for index, root in enumerate(record[1], 1):
            triangle(root, f"T{index}")
    elif kind == "chain2+direct":
        fresh = triangle(record[1], "T1")[0]
        triangle(fresh, "T2")
        triangle(record[2], "T3")
    elif kind == "fork":
        fresh = triangle(record[1], "T1")
        roots = (fresh[0], fresh[0]) if record[2] == "same" else fresh
        triangle(roots[0], "T2")
        triangle(roots[1], "T3")
    elif kind == "chain3":
        fresh = triangle(record[1], "T1")[0]
        fresh = triangle(fresh, "T2")[0]
        triangle(fresh, "T3")
    else:
        raise ScoutError(f"unknown record kind: {kind}")

    order = tuple(sorted(names))
    index = {name: place for place, name in enumerate(order)}
    edges = frozenset(tuple(sorted((index[left], index[right])))
                      for left, right in named_edges)
    require(len(order) == 10 and len(edges) == 14, "bare rank/order changed")
    return order, edges


def bare_graph(record: Record) -> Graph:
    order, edges = bare_named_graph(record)
    return len(order), edges


def core_vertex_order(record: Record) -> tuple[str, ...]:
    return bare_named_graph(record)[0]


def tree_code_text(tree: Tree) -> str:
    return "(" + "".join(tree_code_text(child) for child in tree) + ")"


def tree_size(tree: Tree) -> int:
    return 1 + sum(tree_size(child) for child in tree)


def rooted_trees(max_extra: int) -> tuple[tuple[Tree, ...], ...]:
    """All unlabeled non-plane rooted trees through max_extra+1 vertices."""
    by_size: list[set[Tree]] = [set() for _ in range(max_extra + 2)]
    by_size[1].add(())
    for target_size in range(2, max_extra + 2):
        catalog = sorted(
            (tree for size in range(1, target_size) for tree in by_size[size]),
            key=lambda tree: (tree_size(tree), tree_code_text(tree)),
        )
        weights = [tree_size(tree) for tree in catalog]
        generated: set[Tree] = set()

        def choose(start: int, remaining: int, children: list[Tree]) -> None:
            if remaining == 0:
                generated.add(tuple(children))
                return
            for position in range(start, len(catalog)):
                weight = weights[position]
                if weight > remaining:
                    break
                children.append(catalog[position])
                choose(position, remaining - weight, children)
                children.pop()

        choose(0, target_size - 1, [])
        by_size[target_size] = generated
    expected = (1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842)
    for size, level in enumerate(by_size[1:], 1):
        if size <= len(expected):
            require(len(level) == expected[size - 1],
                    f"rooted-tree count changed at order {size}")
    return tuple(tuple(sorted(level, key=tree_code_text)) for level in by_size)


def attachment_assignments(core_order: int, max_extra: int,
                           trees: tuple[tuple[Tree, ...], ...]) -> Iterator[tuple[Tree, ...]]:
    """All labelled-site rooted-tree assignments with total extra <= max_extra."""
    options = tuple((tree, tree_size(tree) - 1)
                    for size in range(1, max_extra + 2)
                    for tree in trees[size])
    trivial = ()
    current: list[Tree] = [trivial] * core_order

    def recurse(site: int, remaining: int) -> Iterator[tuple[Tree, ...]]:
        if site == core_order:
            yield tuple(current)
            return
        for tree, extra in options:
            if extra > remaining:
                continue
            current[site] = tree
            yield from recurse(site + 1, remaining - extra)
        current[site] = trivial

    yield from recurse(0, max_extra)


def assignment_text(assignment: tuple[Tree, ...]) -> str:
    return ";".join(f"{site}:{tree_code_text(tree)}"
                    for site, tree in enumerate(assignment) if tree)


def parse_assignment(text: str, order: int,
                     tree_lookup: dict[str, Tree]) -> tuple[Tree, ...]:
    assignment: list[Tree] = [()] * order
    if not text:
        return tuple(assignment)
    for field in text.split(";"):
        site_text, code = field.split(":", 1)
        site = int(site_text)
        require(0 <= site < order, "attachment site outside core")
        require(code in tree_lookup, f"unknown rooted-tree code: {code}")
        require(assignment[site] == (), "duplicate attachment site")
        assignment[site] = tree_lookup[code]
    return tuple(assignment)


def materialize(graph: Graph, assignment: tuple[Tree, ...]) -> Graph:
    n, old_edges = graph
    require(len(assignment) == n, "attachment assignment has wrong core order")
    edges = set(old_edges)

    def append_children(parent: int, children: Tree) -> None:
        nonlocal n
        for child in children:
            vertex = n
            n += 1
            add_edge(edges, parent, vertex)
            append_children(vertex, child)

    for root, tree in enumerate(assignment):
        append_children(root, tree)
    return n, frozenset(edges)


def matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    n = len(left)
    return [[sum(left[i][k] * right[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]


def characteristic_polynomial(graph: Graph) -> Poly:
    """Integer det(xI-A), via traces and Newton identities."""
    n, edges = graph
    if n == 0:
        return [1]
    adjacency = [[0] * n for _ in range(n)]
    for left, right in edges:
        adjacency[left][right] = adjacency[right][left] = 1
    power = [row[:] for row in adjacency]
    traces: list[int] = []
    for exponent in range(1, n + 1):
        traces.append(sum(power[index][index] for index in range(n)))
        if exponent != n:
            power = matmul(power, adjacency)
    coefficients = [1]
    for k in range(1, n + 1):
        numerator = sum(coefficients[k - i] * traces[i - 1]
                        for i in range(1, k + 1))
        require(numerator % k == 0, "Newton identity produced a fraction")
        coefficients.append(-numerator // k)
    return coefficients


def induced_subgraph(graph: Graph, deleted: frozenset[int]) -> Graph:
    n, edges = graph
    keep = [vertex for vertex in range(n) if vertex not in deleted]
    image = {vertex: place for place, vertex in enumerate(keep)}
    new_edges = frozenset((image[left], image[right]) for left, right in edges
                          if left not in deleted and right not in deleted)
    return len(keep), new_edges


def trim_int(poly: Iterable[int]) -> Poly:
    result = list(poly)
    while len(result) > 1 and result[0] == 0:
        result.pop(0)
    return result or [0]


def poly_add(left: Poly, right: Poly) -> Poly:
    length = max(len(left), len(right))
    a = [0] * (length - len(left)) + left
    b = [0] * (length - len(right)) + right
    return trim_int(x + y for x, y in zip(a, b))


def poly_sub(left: Poly, right: Poly) -> Poly:
    length = max(len(left), len(right))
    a = [0] * (length - len(left)) + left
    b = [0] * (length - len(right)) + right
    return trim_int(x - y for x, y in zip(a, b))


def poly_mul(left: Poly, right: Poly) -> Poly:
    if left == [0] or right == [0]:
        return [0]
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim_int(result)


def x_times(poly: Poly) -> Poly:
    return list(poly) + [0]


def tree_polynomials(tree: Tree, cache: dict[Tree, tuple[Poly, Poly, Poly]]) -> tuple[Poly, Poly, Poly]:
    """Return (phi_T, phi_(T-root), correction=phi_T-x*phi_(T-root))."""
    if tree in cache:
        return cache[tree]
    if not tree:
        result = ([1, 0], [1], [0])
        cache[tree] = result
        return result
    # Root deletion is the disjoint union of the child rooted trees.
    denominator = [1]
    child_data = []
    for child in tree:
        data = tree_polynomials(child, cache)
        child_data.append(data)
        denominator = poly_mul(denominator, data[0])
    # Tree matching recurrence at the root.
    numerator = x_times(denominator)
    for index, (_, child_denominator, _) in enumerate(child_data):
        term = child_denominator
        for other, (child_numerator, _, _) in enumerate(child_data):
            if other != index:
                term = poly_mul(term, child_numerator)
        numerator = poly_sub(numerator, term)
    correction = poly_sub(numerator, x_times(denominator))
    result = (numerator, denominator, correction)
    cache[tree] = result
    return result


class CoreMinorPolynomials:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.cache: dict[int, Poly] = {}

    def get(self, deleted_mask: int) -> Poly:
        if deleted_mask not in self.cache:
            deleted = frozenset(index for index in range(self.graph[0])
                                if deleted_mask & (1 << index))
            self.cache[deleted_mask] = characteristic_polynomial(
                induced_subgraph(self.graph, deleted))
        return self.cache[deleted_mask]


def coalesced_characteristic(core: Graph, assignment: tuple[Tree, ...],
                             minors: CoreMinorPolynomials,
                             tree_cache: dict[Tree, tuple[Poly, Poly, Poly]]) -> Poly:
    active = [(site, tree_polynomials(tree, tree_cache))
              for site, tree in enumerate(assignment) if tree]
    result = [0]
    # Expand the commuting coalescence operators.  With at most B active sites
    # this has at most 2^B terms, independent of total core order.
    for selected_bits in range(1 << len(active)):
        mask = 0
        factor = [1]
        for position, (site, (_, denominator, correction)) in enumerate(active):
            if selected_bits & (1 << position):
                mask |= 1 << site
                factor = poly_mul(factor, correction)
            else:
                factor = poly_mul(factor, denominator)
        result = poly_add(result, poly_mul(factor, minors.get(mask)))
    expected_degree = core[0] + sum(tree_size(tree) - 1 for tree in assignment)
    require(len(result) == expected_degree + 1 and result[0] == 1,
            "coalesced characteristic polynomial has wrong degree/leading term")
    return result


# Fraction-polynomial and Sturm routines.  These are intentionally local rather
# than imported from the pre-existing rooted-cactus experiment.
def qtrim(poly: Iterable[Fraction | int]) -> list[Fraction]:
    result = [Fraction(value) for value in poly]
    while len(result) > 1 and result[0] == 0:
        result.pop(0)
    return result or [Fraction(0)]


def derivative(poly: list[Fraction]) -> list[Fraction]:
    degree = len(poly) - 1
    if degree <= 0:
        return [Fraction(0)]
    return qtrim(poly[index] * (degree - index) for index in range(degree))


def qdivmod(dividend: list[Fraction], divisor: list[Fraction]) -> tuple[list[Fraction], list[Fraction]]:
    dividend = qtrim(dividend)
    divisor = qtrim(divisor)
    if divisor == [0]:
        raise ZeroDivisionError
    quotient = [Fraction(0)] * max(1, len(dividend) - len(divisor) + 1)
    while dividend != [0] and len(dividend) >= len(divisor):
        shift = len(dividend) - len(divisor)
        factor = dividend[0] / divisor[0]
        quotient[len(quotient) - shift - 1] = factor
        subtractor = [factor * value for value in divisor] + [Fraction(0)] * shift
        dividend = qtrim(left - right for left, right in zip(dividend, subtractor))
    return qtrim(quotient), qtrim(dividend)


def monic(poly: Iterable[Fraction | int]) -> list[Fraction]:
    result = qtrim(poly)
    if result == [0]:
        return result
    return [value / result[0] for value in result]


def qgcd(left: Iterable[Fraction | int], right: Iterable[Fraction | int]) -> list[Fraction]:
    a, b = qtrim(left), qtrim(right)
    while b != [0]:
        _, remainder = qdivmod(a, b)
        a, b = b, remainder
    return monic(a)


def squarefree_layers(poly: Poly) -> list[tuple[list[Fraction], int]]:
    current = monic(poly)
    repeated = qgcd(current, derivative(current))
    remaining, remainder = qdivmod(current, repeated)
    require(remainder == [0], "nonexact initial squarefree quotient")
    layers: list[tuple[list[Fraction], int]] = []
    multiplicity = 1
    while len(remaining) > 1:
        shared = qgcd(remaining, repeated)
        factor, remainder = qdivmod(remaining, shared)
        require(remainder == [0], "nonexact squarefree layer")
        factor = monic(factor)
        if len(factor) > 1:
            layers.append((factor, multiplicity))
        remaining = shared
        repeated, remainder = qdivmod(repeated, shared)
        require(remainder == [0], "nonexact repeated-factor quotient")
        multiplicity += 1
    return layers


def sturm_sequence(poly: list[Fraction]) -> list[list[Fraction]]:
    sequence = [qtrim(poly), derivative(qtrim(poly))]
    while sequence[-1] != [0]:
        _, remainder = qdivmod(sequence[-2], sequence[-1])
        if remainder == [0]:
            break
        sequence.append([-value for value in remainder])
    return sequence


def evaluate(poly: list[Fraction], point: Fraction) -> Fraction:
    value = Fraction(0)
    for coefficient in poly:
        value = value * point + coefficient
    return value


def variations(sequence: list[list[Fraction]], point: Fraction) -> int:
    signs = []
    for poly in sequence:
        value = evaluate(poly, point)
        if value:
            signs.append(value > 0)
    return sum(signs[index] != signs[index - 1]
               for index in range(1, len(signs)))


def root_count(sequence: list[list[Fraction]], left: Fraction, right: Fraction) -> int:
    return variations(sequence, left) - variations(sequence, right)


def isolate_positive_squarefree(poly: list[Fraction], bits: int) -> list[tuple[Fraction, Fraction]]:
    # Remove a zero root so the open positive ray has a clean endpoint.
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    if len(poly) == 1:
        return []
    sequence = sturm_sequence(poly)
    bound_q = 1 + max(abs(coefficient / poly[0]) for coefficient in poly[1:])
    bound = Fraction((bound_q.numerator + bound_q.denominator - 1) // bound_q.denominator)
    total = root_count(sequence, Fraction(0), bound)
    intervals: list[tuple[Fraction, Fraction]] = []
    stack = [(Fraction(0), bound, total)]
    target = Fraction(1, 1 << bits)
    while stack:
        left, right, count = stack.pop()
        if count == 0:
            continue
        if count == 1 and right - left <= target:
            intervals.append((left, right))
            continue
        middle = (left + right) / 2
        left_count = root_count(sequence, left, middle)
        stack.append((middle, right, count - left_count))
        stack.append((left, middle, left_count))
    return sorted(intervals)


def isolate_positive_roots(poly: Poly, bits: int) -> list[tuple[Fraction, Fraction, int]]:
    roots = []
    for factor, multiplicity in squarefree_layers(poly):
        roots.extend((left, right, multiplicity)
                     for left, right in isolate_positive_squarefree(factor, bits))
    return sorted(roots)


def exact_surplus_interval(poly: Poly, order: int, bits: int) -> tuple[Fraction, Fraction, list[tuple[Fraction, Fraction, int]]]:
    roots = isolate_positive_roots(poly, bits)
    lower = sum(multiplicity * left * left for left, _, multiplicity in roots) - order
    upper = sum(multiplicity * right * right for _, right, multiplicity in roots) - order
    return lower, upper, roots


def rational_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def polynomial_digest(poly: Poly) -> str:
    raw = ",".join(map(str, poly)).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def record_text(record: Record) -> str:
    return repr(record)


def assignment_extra(assignment: tuple[Tree, ...]) -> int:
    return sum(tree_size(tree) - 1 for tree in assignment)


def expected_assignment_count(core_order: int, max_extra: int,
                              trees: tuple[tuple[Tree, ...], ...]) -> int:
    # Coefficient sum through B of (sum_t a_t z^(t-1))^core_order.
    polynomial = [1] + [0] * max_extra
    choices = [len(trees[extra + 1]) for extra in range(max_extra + 1)]
    for _ in range(core_order):
        product = [0] * (max_extra + 1)
        for i, left in enumerate(polynomial):
            for j, right in enumerate(choices):
                if i + j <= max_extra:
                    product[i + j] += left * right
        polynomial = product
    return sum(polynomial)


def numeric_surplus(graph: Graph) -> float:
    # Imported only inside numeric mode: exact mode therefore has no accidental
    # floating-point dependency.
    import numpy as np

    n, edges = graph
    adjacency = np.zeros((n, n), dtype=float)
    for left, right in edges:
        adjacency[left, right] = adjacency[right, left] = 1.0
    eigenvalues = np.linalg.eigvalsh(adjacency)
    return float(np.dot(eigenvalues[eigenvalues > 0.0],
                        eigenvalues[eigenvalues > 0.0]) - n)


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def numeric_mode(args: argparse.Namespace) -> dict:
    rows = records()
    trees = rooted_trees(args.extra)
    expected_per_record = expected_assignment_count(10, args.extra, trees)
    keep: list[tuple[float, str, str, int]] = []
    tested = 0
    minimum_by_extra: dict[int, tuple[float, str, str]] = {}
    for record in rows:
        core = bare_graph(record)
        assignments = attachment_assignments(core[0], args.extra, trees)
        local_count = 0
        for assignment in assignments:
            graph = materialize(core, assignment)
            surplus = numeric_surplus(graph)
            text = assignment_text(assignment)
            extra = assignment_extra(assignment)
            item = (surplus, record_text(record), text, graph[0])
            keep.append(item)
            keep.sort(key=lambda row: (row[0], row[1], row[2]))
            del keep[args.keep:]
            old = minimum_by_extra.get(extra)
            if old is None or (surplus, record_text(record), text) < old:
                minimum_by_extra[extra] = (surplus, record_text(record), text)
            local_count += 1
            tested += 1
        require(local_count == expected_per_record,
                f"attachment count changed for {record}: {local_count}")
    payload = {
        "schema": "r31-s-d3-bounded-tree-numeric-scout-v1",
        "status": "NUMERIC_SCOUT_ONLY_NOT_PROOF",
        "scope": {
            "one_side_records": len(rows),
            "maximum_total_extra_vertices": args.extra,
            "core_vertices": 10,
            "labelled_site_assignments_per_record": expected_per_record,
            "tested_graphs": tested,
        },
        "rooted_tree_counts_by_order": {
            str(size): len(trees[size]) for size in range(1, len(trees))
        },
        "minimum_by_exact_extra_count": [
            {
                "extra": extra,
                "numeric_surplus": format(row[0], ".17g"),
                "record": row[1],
                "assignment": row[2],
            }
            for extra, row in sorted(minimum_by_extra.items())
        ],
        "low_tail": [
            {
                "numeric_surplus": format(surplus, ".17g"),
                "record": record,
                "assignment": assignment,
                "order": order,
            }
            for surplus, record, assignment, order in keep
        ],
    }
    return payload


def resolve_record(text: str, rows: tuple[Record, ...]) -> Record:
    matches = [record for record in rows if repr(record) == text]
    require(len(matches) == 1, f"record not uniquely recognized: {text}")
    return matches[0]


def exact_certificate(record: Record, assignment: tuple[Tree, ...], bits: int,
                      direct_check: bool,
                      minor_cache: dict[Record, CoreMinorPolynomials],
                      tree_cache: dict[Tree, tuple[Poly, Poly, Poly]]) -> tuple[dict, Fraction, Fraction]:
    core = bare_graph(record)
    minors = minor_cache.setdefault(record, CoreMinorPolynomials(core))
    polynomial = coalesced_characteristic(core, assignment, minors, tree_cache)
    graph = materialize(core, assignment)
    if direct_check:
        require(characteristic_polynomial(graph) == polynomial,
                "direct and coalesced characteristic polynomials differ")
    lower, upper, roots = exact_surplus_interval(polynomial, graph[0], bits)
    certificate = {
        "record": record_text(record),
        "core_vertex_order": list(core_vertex_order(record)),
        "assignment": assignment_text(assignment),
        "order": graph[0],
        "size": len(graph[1]),
        "characteristic_polynomial_desc": polynomial,
        "characteristic_polynomial_sha256": polynomial_digest(polynomial),
        "positive_root_intervals": [
            [rational_text(left), rational_text(right), multiplicity]
            for left, right, multiplicity in roots
        ],
        "surplus_interval": [rational_text(lower), rational_text(upper)],
        "threshold_margin_interval": [rational_text(lower - 3), rational_text(upper - 3)],
        "direct_charpoly_crosscheck": direct_check,
    }
    return certificate, lower, upper


def load_tail(path: Path, rows: tuple[Record, ...], lookup: dict[str, Tree]) -> list[tuple[Record, tuple[Tree, ...]]]:
    payload = json.loads(path.read_text(encoding="ascii"))
    require(payload.get("status") == "NUMERIC_SCOUT_ONLY_NOT_PROOF",
            "input is not a numeric scout artifact")
    result = []
    for row in payload["low_tail"]:
        record = resolve_record(row["record"], rows)
        assignment = parse_assignment(row["assignment"], 10, lookup)
        result.append((record, assignment))
    return result


def exact_mode(args: argparse.Namespace) -> dict:
    rows = records()
    trees = rooted_trees(args.extra)
    lookup = {tree_code_text(tree): tree
              for size in range(1, len(trees)) for tree in trees[size]}
    minor_cache: dict[Record, CoreMinorPolynomials] = {}
    tree_cache: dict[Tree, tuple[Poly, Poly, Poly]] = {}
    candidates: list[tuple[Record, tuple[Tree, ...]]] = []
    scope_kind: str
    expected_per_record = expected_assignment_count(10, args.extra, trees)
    if args.tail_input:
        candidates = load_tail(Path(args.tail_input), rows, lookup)
        scope_kind = "numeric-low-tail-only"
    else:
        for record in rows:
            candidates.extend((record, assignment)
                              for assignment in attachment_assignments(10, args.extra, trees))
        require(len(candidates) == len(rows) * expected_per_record,
                "complete exact census count changed")
        scope_kind = "complete-bounded-census"

    # Many labelled attachment assignments are cospectral.  Compute every
    # integer characteristic polynomial first, then run Sturm once per exact
    # (polynomial, order) class.  This is a lossless exact quotient, not a
    # numerical heuristic.  A representative and its multiplicity are kept so
    # the finite census remains auditable.
    classes: dict[tuple[tuple[int, ...], int], dict] = {}
    direct_checks = 0
    for index, (record, assignment) in enumerate(candidates):
        core = bare_graph(record)
        minors = minor_cache.setdefault(record, CoreMinorPolynomials(core))
        polynomial = coalesced_characteristic(core, assignment, minors, tree_cache)
        order = core[0] + assignment_extra(assignment)
        direct_check = index < args.direct_checks
        if direct_check:
            require(characteristic_polynomial(materialize(core, assignment)) == polynomial,
                    "direct and coalesced characteristic polynomials differ")
            direct_checks += 1
        key = (tuple(polynomial), order)
        if key not in classes:
            classes[key] = {
                "polynomial": polynomial,
                "order": order,
                "record": record,
                "assignment": assignment,
                "multiplicity": 0,
                "direct_charpoly_crosscheck": False,
            }
        classes[key]["multiplicity"] += 1
        classes[key]["direct_charpoly_crosscheck"] |= direct_check

    minimum: tuple[Fraction, Fraction, dict] | None = None
    unresolved = []
    counterexamples = []
    certificates = []
    for row in classes.values():
        polynomial = row["polynomial"]
        lower, upper, roots = exact_surplus_interval(polynomial, row["order"], args.bits)
        certificate = {
            "record": record_text(row["record"]),
            "core_vertex_order": list(core_vertex_order(row["record"])),
            "assignment": assignment_text(row["assignment"]),
            "cospectral_multiplicity": row["multiplicity"],
            "order": row["order"],
            "size": row["order"] + 4,  # every scoped graph has rank five
            "characteristic_polynomial_desc": polynomial,
            "characteristic_polynomial_sha256": polynomial_digest(polynomial),
            "positive_root_intervals": [
                [rational_text(left), rational_text(right), multiplicity]
                for left, right, multiplicity in roots
            ],
            "surplus_interval": [rational_text(lower), rational_text(upper)],
            "threshold_margin_interval": [rational_text(lower - 3), rational_text(upper - 3)],
            "direct_charpoly_crosscheck": row["direct_charpoly_crosscheck"],
        }
        if minimum is None or (lower, upper, certificate["record"], certificate["assignment"]) < (
                minimum[0], minimum[1], minimum[2]["record"], minimum[2]["assignment"]):
            minimum = (lower, upper, certificate)
        if upper <= 3:
            counterexamples.append(certificate)
        elif lower <= 3:
            unresolved.append(certificate)
        if args.keep_certificates:
            certificates.append((lower, certificate))
            certificates.sort(key=lambda item: (item[0], item[1]["record"], item[1]["assignment"]))
            del certificates[args.keep_certificates:]

    require(minimum is not None, "empty exact candidate set")
    require(sum(row["multiplicity"] for row in classes.values()) == len(candidates),
            "cospectral quotient lost a graph")
    status = ("CERTIFIED_COUNTEREXAMPLE_IN_SCOPED_CENSUS" if counterexamples else
              "UNRESOLVED_AT_REQUESTED_PRECISION" if unresolved else
              "CERTIFIED_POSITIVE_ON_SCOPED_FINITE_CENSUS")
    payload = {
        "schema": "r31-s-d3-bounded-tree-exact-scout-v2",
        "status": status,
        "scope_kind": scope_kind,
        "unbounded_theorem_status": "NOT_PROVED_BY_FINITE_CENSUS",
        "arithmetic": "integer characteristic polynomials; exact cospectral quotient; Fraction Sturm isolation; squarefree multiplicity layers",
        "scope": {
            "one_side_records": len(rows),
            "maximum_total_extra_vertices": args.extra,
            "core_vertices": 10,
            "labelled_site_assignments_per_record": expected_per_record,
            "tested_graphs": len(candidates),
            "distinct_characteristic_polynomial_order_classes": len(classes),
            "sturm_bits": args.bits,
        },
        "rooted_tree_counts_by_order": {
            str(size): len(trees[size]) for size in range(1, len(trees))
        },
        "direct_charpoly_crosschecks": direct_checks,
        "counterexample_class_count": len(counterexamples),
        "unresolved_class_count": len(unresolved),
        "minimum_by_certified_lower_endpoint": minimum[2],
        "low_certificates": [certificate for _, certificate in certificates],
        "counterexamples": counterexamples,
        "unresolved": unresolved,
    }
    return payload


def stars_mode(args: argparse.Namespace) -> dict:
    record = ("direct3", ("x", "x", "x"))
    core = bare_graph(record)
    minors = CoreMinorPolynomials(core)
    tree_cache: dict[Tree, tuple[Poly, Poly, Poly]] = {}
    requested = [int(field) for field in args.star_k.split(",") if field]
    require(requested and all(k >= 1 for k in requested),
            "--star-k must be a nonempty comma-separated list of positive integers")
    require(len(set(requested)) == len(requested), "duplicate --star-k value")
    rows = []
    for k in requested:
        assignment = tuple(tuple(() for _ in range(k)) for _ in range(core[0]))
        polynomial = coalesced_characteristic(core, assignment, minors, tree_cache)
        reduced = list(polynomial)
        zero_multiplicity = 0
        while len(reduced) > 1 and reduced[-1] == 0:
            reduced.pop()
            zero_multiplicity += 1
        require(zero_multiplicity >= core[0] * (k - 1),
                "pendant-star zero eigenspace unexpectedly small")
        order = core[0] * (k + 1)
        lower, upper, roots = exact_surplus_interval(reduced, order, args.bits)
        rows.append({
            "leaves_per_site": k,
            "order": order,
            "zero_multiplicity_removed": zero_multiplicity,
            "reduced_characteristic_polynomial_desc": reduced,
            "reduced_characteristic_polynomial_sha256": polynomial_digest(reduced),
            "positive_root_intervals": [
                [rational_text(left), rational_text(right), multiplicity]
                for left, right, multiplicity in roots
            ],
            "surplus_interval": [rational_text(lower), rational_text(upper)],
            "threshold_margin_interval": [rational_text(lower - 3),
                                          rational_text(upper - 3)],
        })
    status = ("CERTIFIED_POSITIVE_ON_LISTED_FAMILY_MEMBERS"
              if all(Fraction(row["threshold_margin_interval"][0]) > 0
                     for row in rows)
              else "NONPOSITIVE_OR_UNRESOLVED_LISTED_FAMILY_MEMBER")
    return {
        "schema": "r31-s-d3-equal-star-exact-scout-v1",
        "status": status,
        "unbounded_theorem_status": "NOT_PROVED_BY_FINITE_FAMILY_SAMPLE",
        "record": record_text(record),
        "core_vertex_order": list(core_vertex_order(record)),
        "family": "attach k pendant leaves at each of all ten core vertices",
        "arithmetic": "integer characteristic polynomial; exact zero-factor removal; Fraction Sturm isolation",
        "sturm_bits": args.bits,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("numeric", "exact", "stars"), required=True)
    parser.add_argument("--extra", type=int, default=0,
                        help="maximum total non-root attachment vertices")
    parser.add_argument("--bits", type=int, default=24,
                        help="dyadic Sturm interval precision in exact mode")
    parser.add_argument("--keep", type=int, default=20,
                        help="numeric low-tail size")
    parser.add_argument("--keep-certificates", type=int, default=20)
    parser.add_argument("--direct-checks", type=int, default=14,
                        help="number of exact rows recomputed from full adjacency")
    parser.add_argument("--tail-input",
                        help="exact-certify only the low tail of a numeric JSON artifact")
    parser.add_argument("--star-k", default="10,20,50,100",
                        help="comma-separated leaves-per-site values for --mode stars")
    parser.add_argument("--print-records", action="store_true",
                        help="print the independently regenerated 14 records as JSON and exit")
    parser.add_argument("--output")
    args = parser.parse_args()
    require(args.extra >= 0, "--extra must be nonnegative")
    require(args.bits >= 4, "--bits is too small")
    require(args.keep >= 1 and args.keep_certificates >= 0,
            "invalid tail size")
    require(args.direct_checks >= 0, "negative direct-check count")
    if args.print_records:
        payload = {
            "schema": "r31-s-d3-one-side-records-v1",
            "record_count": len(records()),
            "records": [record_text(record) for record in records()],
        }
    else:
        payload = (numeric_mode(args) if args.mode == "numeric" else
                   exact_mode(args) if args.mode == "exact" else
                   stars_mode(args))
    raw = canonical_json(payload)
    if args.output:
        Path(args.output).write_bytes(raw)
    else:
        sys.stdout.buffer.write(raw)


if __name__ == "__main__":
    main()
