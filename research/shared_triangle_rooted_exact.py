#!/usr/bin/env python3
"""Exact experiments for rooted triangular cactus packets.

The script uses integer characteristic polynomials, multiplicity-aware rational
Sturm intervals, and symbolic rooted transfer ratios.  It deliberately
contains no floating point arithmetic.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


def add_edge(edges, u, v):
    if u == v:
        raise ValueError("loops are not supported")
    edges.add(tuple(sorted((u, v))))


def add_cycle(edges, vertices):
    for i, u in enumerate(vertices):
        add_edge(edges, u, vertices[(i + 1) % len(vertices)])


def bouquet(triangles, pentagons=0):
    edges = set()
    next_vertex = 1
    for length, count in ((3, triangles), (5, pentagons)):
        for _ in range(count):
            private = list(range(next_vertex, next_vertex + length - 1))
            next_vertex += length - 1
            add_cycle(edges, [0] + private)
    return next_vertex, edges, 0


def triangle_chain(triangles):
    edges = set()
    add_cycle(edges, [0, 1, 2])
    next_vertex = 3
    boundary = 1
    for _ in range(1, triangles):
        new = [next_vertex, next_vertex + 1]
        next_vertex += 2
        add_cycle(edges, [boundary] + new)
        boundary = new[0]
    return next_vertex, edges, boundary


def central_three_petals():
    edges = set()
    add_cycle(edges, [0, 1, 2])
    next_vertex = 3
    for center in range(3):
        add_cycle(edges, [center, next_vertex, next_vertex + 1])
        next_vertex += 2
    return next_vertex, edges, 0


ROOTED_TREES = {
    "point": (1, (), 0),
    "edge-end": (2, ((0, 1),), 0),
    "path3-end": (3, ((0, 1), (1, 2)), 0),
    "path3-middle": (3, ((0, 1), (0, 2)), 0),
    "path4-end": (4, ((0, 1), (1, 2), (2, 3)), 0),
    "path4-inner": (4, ((0, 1), (1, 2), (1, 3)), 0),
    "claw-center": (4, ((0, 1), (0, 2), (0, 3)), 0),
    "claw-leaf": (4, ((0, 1), (1, 2), (1, 3)), 0),
}


def attach_rooted_tree(graph, at, tree_name):
    n, edges, boundary = graph
    tn, tree_edges, root = ROOTED_TREES[tree_name]
    image = {root: at}
    for vertex in range(tn):
        if vertex != root:
            image[vertex] = n
            n += 1
    edges = set(edges)
    for u, v in tree_edges:
        add_edge(edges, image[u], image[v])
    return n, edges, boundary


def add_petal(graph, at, length):
    n, edges, boundary = graph
    vertices = [at] + list(range(n, n + length - 1))
    edges = set(edges)
    add_cycle(edges, vertices)
    return n + length - 1, edges, boundary


def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def characteristic_polynomial(n, edges):
    """Return det(xI-A), coefficients in descending order."""
    adjacency = [[0] * n for _ in range(n)]
    for u, v in edges:
        adjacency[u][v] = adjacency[v][u] = 1
    power = [row[:] for row in adjacency]
    traces = []
    for exponent in range(1, n + 1):
        traces.append(sum(power[i][i] for i in range(n)))
        if exponent != n:
            power = matmul(power, adjacency)
    coefficients = [1]
    for k in range(1, n + 1):
        numerator = sum(coefficients[k - i] * traces[i - 1] for i in range(1, k + 1))
        if numerator % k:
            raise ArithmeticError("nonintegral Newton coefficient")
        coefficients.append(-numerator // k)
    return coefficients


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[0] == 0:
        poly.pop(0)
    return poly


def derivative(poly):
    degree = len(poly) - 1
    return trim([poly[i] * (degree - i) for i in range(degree)]) or [Fraction(0)]


def poly_divmod(a, b):
    a = [Fraction(x) for x in trim(a)]
    b = [Fraction(x) for x in trim(b)]
    if b == [0]:
        raise ZeroDivisionError
    quotient = [Fraction(0)] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and a != [0]:
        shift = len(a) - len(b)
        factor = a[0] / b[0]
        quotient[len(quotient) - shift - 1] = factor
        subtractor = [factor * value for value in b] + [Fraction(0)] * shift
        a = trim([x - y for x, y in zip(a, subtractor)])
    return trim(quotient), trim(a)


def monic(poly):
    poly = [Fraction(x) for x in trim(poly)]
    if poly == [0]:
        return poly
    return [x / poly[0] for x in poly]


def poly_gcd(a, b):
    a = [Fraction(x) for x in trim(a)]
    b = [Fraction(x) for x in trim(b)]
    while b != [0]:
        _, remainder = poly_divmod(a, b)
        a, b = b, remainder
    return monic(a)


def squarefree_layers(poly):
    """Return (factor, multiplicity) layers for a characteristic polynomial."""
    current = monic(poly)
    repeated = poly_gcd(current, derivative(current))
    remaining, remainder = poly_divmod(current, repeated)
    if remainder != [0]:
        raise ArithmeticError("nonexact squarefree quotient")
    layers = []
    multiplicity = 1
    while len(remaining) > 1:
        shared = poly_gcd(remaining, repeated)
        factor, remainder = poly_divmod(remaining, shared)
        if remainder != [0]:
            raise ArithmeticError("nonexact squarefree quotient")
        factor = monic(factor)
        if len(factor) > 1:
            layers.append((factor, multiplicity))
        remaining = shared
        repeated, remainder = poly_divmod(repeated, shared)
        if remainder != [0]:
            raise ArithmeticError("nonexact repeated-factor quotient")
        multiplicity += 1
    return layers


def sturm_sequence(poly):
    sequence = [[Fraction(x) for x in trim(poly)], derivative(poly)]
    while sequence[-1] != [0]:
        _, remainder = poly_divmod(sequence[-2], sequence[-1])
        if remainder == [0]:
            break
        sequence.append([-value for value in remainder])
    return sequence


def evaluate(poly, x):
    value = Fraction(0)
    for coefficient in poly:
        value = value * x + coefficient
    return value


def variations(sequence, x):
    signs = []
    for poly in sequence:
        value = evaluate(poly, x)
        if value:
            signs.append(value > 0)
    return sum(signs[i] != signs[i - 1] for i in range(1, len(signs)))


def root_count(sequence, left, right):
    return variations(sequence, left) - variations(sequence, right)


def rational_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def isolate_positive_roots(poly, bits=36):
    # Zero eigenvalues are not positive roots.  Removing their common x-power
    # also prevents endpoint zeros from degenerating the Sturm variations.
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    if len(poly) == 1:
        return []
    sequence = sturm_sequence(poly)
    bound = 1 + max(abs(Fraction(c, poly[0])) for c in poly[1:])
    bound = Fraction((bound.numerator + bound.denominator - 1) // bound.denominator)
    intervals = []
    stack = [(Fraction(0), bound, root_count(sequence, Fraction(0), bound))]
    target = Fraction(1, 1 << bits)
    while stack:
        left, right, count = stack.pop()
        if not count:
            continue
        if count == 1 and right - left <= target:
            intervals.append((left, right))
            continue
        middle = (left + right) / 2
        left_count = root_count(sequence, left, middle)
        stack.append((middle, right, count - left_count))
        stack.append((left, middle, left_count))
    return sorted(intervals)


def isolate_positive_roots_with_multiplicity(poly, bits=36):
    roots = []
    for factor, multiplicity in squarefree_layers(poly):
        for left, right in isolate_positive_roots(factor, bits):
            roots.append((left, right, multiplicity))
    return sorted(roots)


def surplus_certificate(graph, bits=36):
    n, edges, _ = graph
    poly = characteristic_polynomial(n, edges)
    intervals = isolate_positive_roots_with_multiplicity(poly, bits)
    lower = sum(multiplicity * left * left for left, _, multiplicity in intervals) - n
    upper = sum(multiplicity * right * right for _, right, multiplicity in intervals) - n
    return {
        "vertices": n,
        "edges": len(edges),
        "characteristic_polynomial_desc": poly,
        "positive_root_intervals": [
            {
                "interval": [rational_text(left), rational_text(right)],
                "multiplicity": multiplicity,
            }
            for left, right, multiplicity in intervals
        ],
        "surplus_interval": [rational_text(lower), rational_text(upper)],
        "surplus_sign": "positive" if lower > 0 else "negative" if upper < 0 else "unresolved",
    }


def delete_vertex_graph(n, edges, vertex):
    keep = [v for v in range(n) if v != vertex]
    relabel = {v: i for i, v in enumerate(keep)}
    new_edges = {(relabel[u], relabel[v]) for u, v in edges if u != vertex and v != vertex}
    return n - 1, new_edges


def polynomial_text(coefficients):
    degree = len(coefficients) - 1
    terms = []
    for i, coefficient in enumerate(coefficients):
        power = degree - i
        if coefficient == 0:
            continue
        sign = "-" if coefficient < 0 else "+"
        magnitude = abs(coefficient)
        body = "" if magnitude == 1 and power else str(magnitude)
        if power:
            body += "x" + (f"^{power}" if power != 1 else "")
        terms.append((sign, body))
    if not terms:
        return "0"
    first_sign, first_body = terms[0]
    text = ("-" if first_sign == "-" else "") + first_body
    return text + "".join(f" {sign} {body}" for sign, body in terms[1:])


def divides(dividend, divisor):
    quotient, remainder = poly_divmod(dividend, divisor)
    if remainder != [0]:
        raise AssertionError(f"{divisor} does not divide characteristic polynomial")
    return [int(value) if value.denominator == 1 else rational_text(value) for value in quotient]


def rooted_transfer(tree_name):
    n, tree_edges, root = ROOTED_TREES[tree_name]
    numerator = characteristic_polynomial(n, set(tree_edges))
    dn, dedges = delete_vertex_graph(n, set(tree_edges), root)
    denominator = characteristic_polynomial(dn, dedges)
    # The diagonal correction in phi(G) + a_T phi(G-v) is phi_T/phi_(T-r)-x.
    shifted = denominator + [0]
    if len(shifted) < len(numerator):
        shifted = [0] * (len(numerator) - len(shifted)) + shifted
    correction = [a - b for a, b in zip(numerator, shifted)]
    return {
        "tree_phi": polynomial_text(numerator),
        "root_deleted_phi": polynomial_text(denominator),
        "correction_ratio": f"({polynomial_text(trim(correction))})/({polynomial_text(denominator)})",
    }


def experiment(bits):
    records = {}
    base_graphs = {
        "T4-central-three-petals": central_three_petals(),
        "T4-common-cut": bouquet(4),
        "T5-chain": triangle_chain(5),
        "T5-common-cut": bouquet(5),
        "T7-common-cut": bouquet(7),
    }
    for name, graph in base_graphs.items():
        records[name] = surplus_certificate(graph, bits)
    expected_central = [1, 0, -12, -8, 42, 48, -36, -72, -27, 0]
    assert records["T4-central-three-petals"]["characteristic_polynomial_desc"] == expected_central
    quotient = expected_central
    central_factors = []
    for label, factor in (("x", [1, 0]), ("x-3", [1, -3]), ("x^2-3", [1, 0, -3])):
        quotient = divides(quotient, factor)
        central_factors.append(label)
    assert quotient == [1, 3, 0, -8, -9, -3]
    records["T4-central-three-petals"]["exact_factorization"] = (
        "x*(x-3)*(x^2-3)^2*(x+1)^3"
    )
    records["T4-central-three-petals"]["exact_surplus"] = "6"

    attachment_records = {}
    for base_name in ("T4-central-three-petals", "T4-common-cut", "T5-chain"):
        graph = base_graphs[base_name]
        at = graph[2]
        for tree_name in ROOTED_TREES:
            name = f"{base_name}+{tree_name}@boundary"
            attachment_records[name] = surplus_certificate(attach_rooted_tree(graph, at, tree_name), bits)

    comparisons = {}
    for base_name in ("T4-central-three-petals", "T4-common-cut", "T5-chain", "T7-common-cut"):
        graph = base_graphs[base_name]
        at = graph[2]
        base = surplus_certificate(graph, bits)
        triangle = surplus_certificate(add_petal(graph, at, 3), bits)
        pentagon = surplus_certificate(add_petal(graph, at, 5), bits)
        comparisons[base_name] = {"base": base, "plus_triangle": triangle, "plus_pentagon": pentagon}

    false_conjectures = []
    # Exact interval subtraction: if U(new)-L(old)<c then delta<c is certified.
    for base_name, row in comparisons.items():
        old_lower = Fraction(row["base"]["surplus_interval"][0])
        old_upper = Fraction(row["base"]["surplus_interval"][1])
        for kind in ("plus_triangle", "plus_pentagon"):
            new_lower = Fraction(row[kind]["surplus_interval"][0])
            new_upper = Fraction(row[kind]["surplus_interval"][1])
            delta = (new_lower - old_upper, new_upper - old_lower)
            row[kind]["surplus_increment_interval"] = [rational_text(delta[0]), rational_text(delta[1])]
            if kind == "plus_triangle" and delta[1] < 1:
                false_conjectures.append({
                    "conjecture": "a boundary triangle raises surplus by at least one",
                    "counterexample": base_name,
                    "certified_increment_upper": rational_text(delta[1]),
                })
            if kind == "plus_pentagon" and delta[1] < 0:
                false_conjectures.append({
                    "conjecture": "a hostile boundary pentagon never lowers surplus",
                    "counterexample": base_name,
                    "certified_increment_upper": rational_text(delta[1]),
                })
        triangle_upper = Fraction(row["plus_triangle"]["surplus_increment_interval"][1])
        pentagon_lower = Fraction(row["plus_pentagon"]["surplus_increment_interval"][0])
        if pentagon_lower > triangle_upper:
            false_conjectures.append({
                "conjecture": "at a fixed boundary, a hostile pentagon adds no more surplus than a triangle",
                "counterexample": base_name,
                "triangle_increment_upper": rational_text(triangle_upper),
                "pentagon_increment_lower": rational_text(pentagon_lower),
            })

    return {
        "arithmetic": "integers and fractions.Fraction only; multiplicity-aware Sturm isolation",
        "root_interval_bits": bits,
        "rooted_transfer_identity": "phi_(G vee T)=phi_(T-r)*(phi_G+(phi_T/phi_(T-r)-x)*phi_(G-v))",
        "rooted_tree_transfers": {name: rooted_transfer(name) for name in ROOTED_TREES},
        "base_packets": records,
        "tree_attachment_samples": attachment_records,
        "hostile_pentagon_comparisons": comparisons,
        "false_conjecture_certificates": false_conjectures,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", type=int, default=36)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = experiment(args.bits)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="ascii") as handle:
            handle.write(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
