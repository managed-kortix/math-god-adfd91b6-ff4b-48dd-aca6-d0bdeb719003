#!/usr/bin/env python3
"""Exact Sturm certificates for the eight short-base theta gates.

No floating-point value participates in a proof.  The displayed decimals are
computed only after all adjacency, characteristic-polynomial, Sturm-count,
and rational square-sum assertions have passed.  Each exceptional gate also
gets a weighted-endpoint certificate for every automorphism orbit of roots.
"""

import sympy as sp


x = sp.symbols("x")
TARGET_SURPLUS = sp.Rational(4, 5)
ISOLATION_WIDTH = sp.Rational(1, 10_000)

# Expanded polynomials are kept independently of the graph constructor.  This
# catches path-length, shared-endpoint, and vertex-count convention errors.
CASES = (
    ("236", (2, 3, 6), "safe", "x**10-11*x**8+41*x**6-2*x**5-60*x**4+8*x**3+27*x**2-8*x"),
    ("237", (2, 3, 7), "safe", "x**11-12*x**9+51*x**7-2*x**6-92*x**5+10*x**4+65*x**3-14*x**2-14*x+4"),
    ("143", (1, 4, 3), "safe", "x**7-8*x**5+15*x**3-2*x**2-5*x"),
    ("145", (1, 4, 5), "safe", "x**9-10*x**7+32*x**5-2*x**4-39*x**3+6*x**2+15*x-4"),
    ("148", (1, 4, 8), "safe", "x**12-13*x**10+62*x**8-2*x**7-134*x**6+12*x**5+129*x**4-22*x**3-44*x**2+12*x"),
    ("223", (2, 2, 3), "exception", "x**6-7*x**4+9*x**2-4*x"),
    ("233", (2, 3, 3), "exception", "x**7-8*x**5+17*x**3-4*x**2-10*x+4"),
    ("144", (1, 4, 4), "exception", "x**8-9*x**6+24*x**4-4*x**3-20*x**2+8*x"),
)

# The vertex sets are the complete automorphism-orbit partitions for possible
# roots.  As with CASES, independently expanded characteristic polynomials
# protect the certificates from graph-construction and rooting mistakes.
WEIGHTED_ENDPOINT_CASES = {
    "223": (
        ("branch", (0, 1), "x**6+x**5/2-7*x**4-2*x**3+9*x**2-3*x"),
        ("mid-length-2", (2, 3), "x**6+x**5/2-7*x**4-5*x**3/2+9*x**2-3*x/2-1"),
        ("internal-length-3", (4, 5), "x**6+x**5/2-7*x**4-5*x**3/2+9*x**2-3*x"),
    ),
    "233": (
        ("branch", (0, 1), "x**7+x**6/2-8*x**5-5*x**4/2+17*x**3-3*x**2/2-10*x+7/2"),
        ("mid-length-2", (2,), "x**7+x**6/2-8*x**5-3*x**4+17*x**3+x**2/2-10*x+2"),
        ("internal-length-3", (3, 4, 5, 6), "x**7+x**6/2-8*x**5-3*x**4+17*x**3-11*x+7/2"),
    ),
    "144": (
        ("branch", (0, 1), "x**8+x**7/2-9*x**6-3*x**5+24*x**4+x**3-20*x**2+6*x"),
        ("adjacent-to-branch", (2, 4, 5, 7), "x**8+x**7/2-9*x**6-7*x**5/2+24*x**4+5*x**3/2-21*x**2+5*x+1"),
        ("mid-length-4", (3, 6), "x**8+x**7/2-9*x**6-7*x**5/2+24*x**4+2*x**3-21*x**2+6*x"),
    ),
}


def theta_adjacency(lengths):
    """Construct Theta(a,b,c) from three internally disjoint u-v paths."""
    n = sum(lengths) - 1
    adjacency = sp.zeros(n)
    next_vertex = 2
    paths = []
    for length in lengths:
        internal = list(range(next_vertex, next_vertex + length - 1))
        path = [0, *internal, 1]
        next_vertex += length - 1
        paths.append(tuple(path))
        for u, v in zip(path, path[1:]):
            assert adjacency[u, v] == 0, "paths must be internally disjoint in a simple theta"
            adjacency[u, v] = adjacency[v, u] = 1
    assert next_vertex == n
    return adjacency, tuple(paths)


def root_multiplicity(poly, root):
    """Return the exact multiplicity of a rational root."""
    multiplicity = 0
    derivative = poly
    while derivative.eval(root) == 0:
        multiplicity += 1
        derivative = derivative.diff()
    return multiplicity


def sturm_isolate_all(poly):
    """Isolate every real root and independently audit every Sturm count."""
    intervals = poly.intervals(eps=ISOLATION_WIDTH)
    assert sum(multiplicity for _, multiplicity in intervals) == poly.degree()
    distinct_roots = len(intervals)
    assert poly.count_roots(-sp.oo, sp.oo) == distinct_roots

    audited = []
    for (left, right), multiplicity in intervals:
        assert left <= right and left.is_Rational and right.is_Rational
        if left == right:
            assert poly.eval(left) == 0
            assert root_multiplicity(poly, left) == multiplicity
        else:
            assert poly.eval(left) != 0 and poly.eval(right) != 0
            assert right - left <= ISOLATION_WIDTH
            assert poly.count_roots(left, right) == multiplicity
        audited.append((left, right, multiplicity))

    # Disjointness and exact separation from zero make the sign classification
    # used by the square bounds explicit rather than inferred numerically.
    for first, second in zip(audited, audited[1:]):
        assert first[1] < second[0]
    for left, right, _ in audited:
        assert right < 0 or left > 0 or (left == right == 0)
    return audited


def positive_square_bounds(intervals):
    lower = sp.S.Zero
    upper = sp.S.Zero
    positive_count = 0
    zero_count = 0
    for left, right, multiplicity in intervals:
        if left > 0:
            lower += multiplicity * left**2
            upper += multiplicity * right**2
            positive_count += multiplicity
        elif left == right == 0:
            zero_count += multiplicity
    return sp.factor(lower), sp.factor(upper), positive_count, zero_count


def format_interval(left, right, multiplicity):
    body = str(left) if left == right else f"({left}, {right})"
    return f"{body} x{multiplicity}"


def certify_weighted_endpoints(label, adjacency):
    """Certify s+(A-E_vv/2) > n for every root-orbit representative."""
    orbit_cases = WEIGHTED_ENDPOINT_CASES[label]
    n = adjacency.rows
    orbit_vertices = [vertex for _, vertices, _ in orbit_cases for vertex in vertices]
    assert sorted(orbit_vertices) == list(range(n))
    assert len(set(orbit_vertices)) == n

    print("  weighted-endpoint root-orbit certificates:")
    certified = 0
    for orbit_name, vertices, expected_expression in orbit_cases:
        expected = sp.Poly(sp.sympify(expected_expression), x)
        orbit_polynomials = []
        for vertex in vertices:
            weighted = adjacency.copy()
            weighted[vertex, vertex] -= sp.Rational(1, 2)
            assert weighted == weighted.T
            assert weighted - adjacency == sp.diag(
                *(-sp.Rational(1, 2) if index == vertex else 0 for index in range(n))
            )
            polynomial = weighted.charpoly(x).as_poly()
            assert polynomial == expected
            orbit_polynomials.append(polynomial)
        assert all(polynomial == orbit_polynomials[0] for polynomial in orbit_polynomials)

        polynomial = orbit_polynomials[0]
        intervals = sturm_isolate_all(polynomial)
        lower, upper, positive_count, zero_count = positive_square_bounds(intervals)
        positive_intervals = [item for item in intervals if item[0] > 0]
        # SymPy's half-line count includes a root at the finite endpoint zero.
        assert polynomial.count_roots(0, sp.oo) == len(positive_intervals) + (zero_count > 0)
        assert sum(item[2] for item in positive_intervals) == positive_count
        assert lower > n

        print(f"    PASS orbit={orbit_name}, roots={vertices}, representative={vertices[0]}")
        print(f"      A-E_vv/2 characteristic polynomial={polynomial.as_expr()}")
        print(f"      factorization={sp.factor(polynomial.as_expr())}")
        print(
            f"      all Sturm roots ({len(intervals)} intervals, multiplicity {n}): "
            + "; ".join(format_interval(*item) for item in intervals)
        )
        print(
            f"      positive Sturm roots ({len(positive_intervals)} intervals, "
            f"multiplicity {positive_count}): "
            + "; ".join(format_interval(*item) for item in positive_intervals)
        )
        print(f"      zero multiplicity={zero_count}")
        print(f"      exact s+ enclosure=[{lower}, {upper}]")
        print(f"      decimal enclosure=[{sp.N(lower, 12)}, {sp.N(upper, 12)}]")
        print(f"      lower - n = {sp.factor(lower - n)} > 0")
        certified += 1

    return certified


def main():
    passed = 0
    weighted_passed = 0
    for label, lengths, verdict, expected_expression in CASES:
        adjacency, paths = theta_adjacency(lengths)
        n = adjacency.rows
        target = n + TARGET_SURPLUS

        assert adjacency == adjacency.T
        assert all(value in (0, 1) for value in adjacency)
        assert all(adjacency[i, i] == 0 for i in range(n))
        assert sum(adjacency) // 2 == sum(lengths) == n + 1
        degrees = sorted(sum(adjacency[i, j] for j in range(n)) for i in range(n))
        assert degrees == [2] * (n - 2) + [3, 3]

        polynomial = adjacency.charpoly(x).as_poly()
        expected = sp.Poly(sp.sympify(expected_expression), x)
        assert polynomial == expected
        intervals = sturm_isolate_all(polynomial)
        lower, upper, positive_count, zero_count = positive_square_bounds(intervals)

        if verdict == "safe":
            assert lower > target
            relation = f"lower - target = {sp.factor(lower - target)} > 0"
        else:
            assert upper < target
            relation = f"target - upper = {sp.factor(target - upper)} > 0"

        print(f"PASS theta {label} = Theta{lengths}: {verdict.upper()}")
        print(f"  vertices={n}, edges={n + 1}, paths={paths}, degrees={degrees}")
        print(f"  adjacency={adjacency.tolist()}")
        print(f"  chi(x)={polynomial.as_expr()}")
        print(f"  factorization={sp.factor(polynomial.as_expr())}")
        print(f"  Sturm roots ({len(intervals)} intervals, multiplicity {n}):")
        print("    " + "; ".join(format_interval(*item) for item in intervals))
        print(
            f"  positive eigenvalues with multiplicity={positive_count}; "
            f"zero multiplicity={zero_count}"
        )
        print(f"  exact s+ enclosure=[{lower}, {upper}]")
        print(f"  decimal enclosure=[{sp.N(lower, 12)}, {sp.N(upper, 12)}]")
        print(f"  threshold={target}; {relation}")
        if verdict == "exception":
            weighted_passed += certify_weighted_endpoints(label, adjacency)
        passed += 1

    print(
        f"theta short-base gates: PASS ({passed}/{len(CASES)} graphs; "
        f"{weighted_passed} weighted root orbits; "
        "all roots exhausted by exact rational Sturm counts)"
    )


if __name__ == "__main__":
    main()
