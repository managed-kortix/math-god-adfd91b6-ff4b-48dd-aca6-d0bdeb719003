#!/usr/bin/env python3
"""Supporting fail-closed checks for the attached-theta phase proof."""

from fractions import Fraction
from itertools import combinations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class Poly:
    def __init__(self, terms=None):
        self.terms = {m: Fraction(c) for m, c in (terms or {}).items() if c}

    @staticmethod
    def constant(value):
        return Poly({(): value}) if value else Poly()

    @staticmethod
    def variable(index, count):
        powers = [0] * count
        powers[index] = 1
        return Poly({tuple(powers): 1})

    def padded(self, count):
        return Poly({m + (0,) * (count - len(m)): c for m, c in self.terms.items()})

    def __add__(self, other):
        other = as_poly(other)
        count = max(self.variables(), other.variables())
        terms = dict(self.padded(count).terms)
        for monomial, coefficient in other.padded(count).terms.items():
            terms[monomial] = terms.get(monomial, Fraction(0)) + coefficient
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-as_poly(other))

    def __rsub__(self, other):
        return as_poly(other) - self

    def __mul__(self, other):
        other = as_poly(other)
        count = max(self.variables(), other.variables())
        left = self.padded(count).terms
        right = other.padded(count).terms
        terms = {}
        for m1, c1 in left.items():
            for m2, c2 in right.items():
                monomial = tuple(a + b for a, b in zip(m1, m2))
                terms[monomial] = terms.get(monomial, Fraction(0)) + c1 * c2
        return Poly(terms)

    __rmul__ = __mul__

    def variables(self):
        return max((len(m) for m in self.terms), default=0)

    def nonnegative(self):
        return all(coefficient >= 0 for coefficient in self.terms.values())

    def set_zero_from(self, index):
        return Poly({m: c for m, c in self.terms.items() if not any(m[index:])})

    def __eq__(self, other):
        other = as_poly(other)
        count = max(self.variables(), other.variables())
        return self.padded(count).terms == other.padded(count).terms


def as_poly(value):
    return value if isinstance(value, Poly) else Poly.constant(value)


ZERO = Poly.constant(0)
ONE = Poly.constant(1)


def matching_partition(vertices, edges, activities):
    total = ZERO
    for size in range(len(edges) + 1):
        for chosen in combinations(edges, size):
            covered = set()
            valid = True
            for u, v in chosen:
                if u in covered or v in covered:
                    valid = False
                    break
                covered.update((u, v))
            if valid:
                term = ONE
                for vertex in vertices:
                    if vertex not in covered:
                        term *= activities[vertex]
                total += term
    return total


def path_edges(path):
    return list(zip(path, path[1:]))


def continuant(values):
    km2 = ONE
    if not values:
        return km2
    km1 = values[0]
    for value in values[1:]:
        km2, km1 = km1, value * km1 + km2
    return km1


def path_packets(path, activities):
    length = len(path) - 1
    interior = [activities[v] for v in path[1:-1]]
    d = continuant(interior)
    if length == 1:
        return d, ZERO, ZERO, ONE
    left = continuant(interior[1:])
    right = continuant(interior[:-1])
    middle = ZERO if length == 2 else continuant(interior[1:-1])
    return d, left, right, middle


def theta_paths(lengths):
    paths = []
    next_vertex = 2
    for length in lengths:
        interior = list(range(next_vertex, next_vertex + length - 1))
        next_vertex += length - 1
        paths.append([0] + interior + [1])
    return paths, list(range(next_vertex))


def induced_partition(vertices, edges, activities, deleted=()):
    deleted = set(deleted)
    retained = [v for v in vertices if v not in deleted]
    retained_edges = [(u, v) for u, v in edges if u not in deleted and v not in deleted]
    return matching_partition(retained, retained_edges, activities)


def variables(vertices):
    count = len(vertices)
    return {vertex: Poly.variable(vertex, count) for vertex in vertices}


def check_packet_identity(lengths, mutation=None):
    paths, vertices = theta_paths(lengths)
    activities = variables(vertices)
    edges = sum((path_edges(path) for path in paths), [])
    cycle_vertices = set(paths[0] + paths[1])
    cycle_edges = path_edges(paths[0]) + path_edges(paths[1])
    d, left, right, middle = path_packets(paths[2], activities)
    if mutation == "middle-sign":
        middle = -middle
    z = matching_partition(sorted(cycle_vertices), cycle_edges, activities)
    zx = induced_partition(sorted(cycle_vertices), cycle_edges, activities, (0,))
    zy = induced_partition(sorted(cycle_vertices), cycle_edges, activities, (1,))
    zxy = induced_partition(sorted(cycle_vertices), cycle_edges, activities, (0, 1))
    rhs = z * d + zx * left + zy * right + zxy * middle
    return matching_partition(vertices, edges, activities) == rhs


def check_low_packets(mutation=None):
    a = variables(list(range(3)))
    got1 = path_packets([0, 1], a)
    got2 = path_packets([0, 2, 1], a)
    if mutation == "length-two-middle":
        got2 = got2[:3] + (ONE,)
    return got1 == (ONE, ZERO, ZERO, ONE) and got2 == (a[2], ONE, ONE, ZERO)


def bare_cycle_partition(length, t):
    vertices = list(range(length))
    edges = [(i, (i + 1) % length) for i in vertices]
    return matching_partition(vertices, edges, {i: t for i in vertices})


def check_bare_injection(limit=12, mutation=None):
    t = Poly.variable(0, 1)
    for ell0 in range(2, limit + 1, 2):
        for ell1 in range(1, limit + 1, 2):
            cycle_length = ell0 + ell1
            cycle = (continuant([t] * cycle_length)
                     + continuant([t] * (cycle_length - 2)))
            lhs = cycle * continuant([t] * (ell1 - 1))
            coefficient = 3 if mutation == "injection-factor" else 2
            difference = lhs - coefficient * continuant([t] * (ell0 - 1))
            if not difference.nonnegative() or difference == ZERO:
                return False
    return True


def check_one_hostile_packet(lengths, mutation=None):
    ell0, ell1, ell2 = lengths
    require((ell0 + ell1) % 4 == 1, "C1 must be hostile")
    require((ell0 + ell2) % 4 == 3, "C2 must be favorable")
    require((ell1 + ell2) % 4 == 0, "even cycle must be zero mod four")
    paths, vertices = theta_paths(lengths)
    count = len(vertices) + 1
    t = Poly.variable(0, count)
    activities = {v: t + Poly.variable(v + 1, count) for v in vertices}
    edges = sum((path_edges(path) for path in paths), [])
    zh = matching_partition(vertices, edges, activities)
    d0 = matching_partition(paths[0][1:-1], path_edges(paths[0][1:-1]), activities)
    a = matching_partition(paths[1][1:-1], path_edges(paths[1][1:-1]), activities)
    b = matching_partition(paths[2][1:-1], path_edges(paths[2][1:-1]), activities)
    zq = bare_cycle_partition(ell0 + ell1, t)
    even_coefficient = 3 if mutation == "one-hostile-even-sign" else 2
    difference = zh - even_coefficient * d0 - zq * (b - a)
    bare = difference.set_zero_from(1)
    bare_expected = (zq * continuant([t] * (ell1 - 1))
                     - even_coefficient * continuant([t] * (ell0 - 1)))
    if ell2 == 1:
        bare_expected += (continuant([t] * (ell0 - 1))
                          * continuant([t] * (ell1 - 1)))
    else:
        bare_expected += (
            2 * continuant([t] * (ell0 + ell1 - 1))
            * continuant([t] * (ell2 - 2))
            + continuant([t] * (ell0 - 1))
            * continuant([t] * (ell1 - 1))
            * continuant([t] * (ell2 - 3))
        )
    return (difference.nonnegative() and bare == bare_expected
            and bare.nonnegative() and bare != ZERO)


def check_even_packet(length0, lengthj, omitted_length, mutation=None):
    require(length0 % 2 == 1, "P0 must be odd in the two-hostile zero-mod channel")
    require(lengthj % 2 == 0 and omitted_length % 2 == 0, "even paths required")
    paths, vertices = theta_paths((length0, lengthj, omitted_length))
    activities = variables(vertices)
    cycle_vertices = set(paths[0] + paths[1])
    cycle_edges = path_edges(paths[0]) + path_edges(paths[1])
    interior0 = paths[0][1:-1]
    d0 = matching_partition(interior0, path_edges(interior0), activities)
    zx = induced_partition(sorted(cycle_vertices), cycle_edges, activities, (0,))
    zy = induced_partition(sorted(cycle_vertices), cycle_edges, activities, (1,))
    zxy = induced_partition(sorted(cycle_vertices), cycle_edges, activities, (0, 1))
    _, left, right, middle = path_packets(paths[2], activities)
    original = zx * left + zy * right + zxy * middle - 2 * d0
    factored = ((zx - d0) * left + d0 * (left - 1)
                + (zy - d0) * right + d0 * (right - 1)
                + zxy * middle)
    if mutation == "endpoint-factor":
        factored += d0
    differences = (zx - d0, zy - d0, left - 1, right - 1)
    return original == factored and all(poly.nonnegative() for poly in differences)


def check_phase_ledger(mutation=None):
    hostile_count = 3 if mutation == "hostile-count" else 2
    delta_upper = Fraction(1, 4)
    d_lower = -2 * hostile_count * delta_upper
    edge_surplus = 0 if mutation == "edge-surplus" else 1
    s_plus_surplus = edge_surplus + d_lower / 2
    return (hostile_count <= 2 and d_lower >= -1 and -4 * delta_upper > -2
            and Fraction(5) < Fraction(25, 4) and s_plus_surplus > 0)


def run_checks(mutation=None):
    packet_lengths = ((2, 3, 1), (2, 1, 3), (3, 2, 2), (1, 4, 2), (4, 3, 2))
    if not all(check_packet_identity(lengths, mutation) for lengths in packet_lengths):
        return False
    if not check_low_packets(mutation) or not check_bare_injection(mutation=mutation):
        return False
    one_hostile_lengths = ((2, 3, 1), (4, 1, 3))
    if not all(check_one_hostile_packet(lengths, mutation) for lengths in one_hostile_lengths):
        return False
    even_lengths = ((1, 2, 2), (3, 2, 4), (1, 4, 2), (5, 4, 4))
    if not all(check_even_packet(*lengths, mutation=mutation) for lengths in even_lengths):
        return False
    return check_phase_ledger(mutation)


def main():
    require(run_checks(), "canonical attached-theta certificate failed")
    mutations = (
        "middle-sign",
        "length-two-middle",
        "injection-factor",
        "one-hostile-even-sign",
        "endpoint-factor",
        "hostile-count",
        "edge-surplus",
    )
    rejected = sum(not run_checks(mutation) for mutation in mutations)
    require(rejected == len(mutations), "a hostile mutation survived")
    print(
        "arbitrary attached theta phase verifier: PASS "
        f"(packets=5, monotone-packets=2, even-factors=4, "
        f"mutations={rejected}/{len(mutations)})"
    )


if __name__ == "__main__":
    main()
