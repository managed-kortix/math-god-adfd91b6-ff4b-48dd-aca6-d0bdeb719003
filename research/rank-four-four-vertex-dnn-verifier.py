#!/usr/bin/env python3
"""Fail-closed audit of the proposed four-vertex rank-four DNN packet.

This file intentionally uses only the Python standard library.  Certificate
search is not part of the proof: CERTIFICATES is immutable candidate data,
while all physical rows, switching orbits, Gram entries, and costs are
regenerated and checked with Fraction arithmetic.  The current candidates do
not transport to all physical rows, so this verifier deliberately exits with
a blocker rather than claiming the theorem.
"""

from fractions import Fraction
from itertools import combinations, permutations, product


KERNELS = (
    (0, 1, 2, 1, 2, 1),
    (0, 1, 2, 2, 1, 1),
    (0, 1, 2, 2, 2, 0),
    (0, 1, 2, 3, 1, 0),
    (1, 1, 1, 1, 1, 2),
)

# Each entry will be (kernel index, canonical q row, (a_0,a_1,a_2,a_3)).
# The planar vectors have angles 4 atan(a_i).  Rational quarter-angle
# differences make both their Gram matrix and all canonical path costs exact.
CERTIFICATES = (
    (0, (0, 0, 0, 0, 0, 0), (0, 0, 0, 0)),
    (0, (0, 0, 0, 0, 0, 1), (0, "-1/1000", "-349/1000", "187/1000")),
    (0, (0, 0, 0, 0, 1, 0), (0, "-447/1000", "-127/1000", "13/200")),
    (0, (0, 0, 0, 0, 1, 1), (0, "-83/250", "-391/1000", "107/500")),
    (0, (0, 0, 0, 0, 2, 0), (0, "1537/1000", "-91/500", "47/500")),
    (0, (0, 0, 1, 0, 1, 0), (0, "1/1000", "181/1000", "-228/125")),
    (1, (0, 0, 0, 0, 0, 0), (0, 0, 0, 0)),
    (1, (0, 0, 0, 0, 0, 1), (0, "-37/250", "-347/1000", "19/100")),
    (1, (0, 0, 0, 0, 1, 0), (0, "249/500", "207/1000", "-53/500")),
    (1, (0, 0, 0, 1, 0, 0), (0, "-3/8", "127/1000", "-13/200")),
    (1, (0, 0, 0, 1, 0, 1), (0, "-4/25", "39/100", "-43/200")),
    (1, (0, 0, 1, 1, 0, 0), (0, "-101/125", "-9/50", "-547/1000")),
    (2, (0, 0, 0, 0, 0, 0), (0, 0, 0, 0)),
    (2, (0, 0, 0, 0, 1, 0), (0, "77/200", "247/1000", "-127/1000")),
    (2, (0, 0, 0, 0, 2, 0), (0, "-89/50", "171/500", "-37/200")),
    (2, (0, 0, 0, 1, 0, 0), (0, "257/1000", "-247/1000", "127/1000")),
    (2, (0, 0, 0, 1, 1, 0), (0, "-577/1000", "1/1000", "-1/1000")),
    (2, (0, 0, 1, 1, 0, 0), (0, "-1731/1000", "1/1000", "-347/200")),
    (2, (0, 0, 1, 1, 1, 0), ("x", "1/3", 0, "1/3", "1/3", "1/3", "1/3")),
    (3, (0, 0, 0, 0, 0, 0), (0, 0, 0, 0)),
    (3, (0, 0, 0, 0, 1, 0), (0, "-21/10", "67/200", "-181/1000")),
    (3, (0, 0, 0, 1, 0, 0), (0, "-137/500", "89/500", "-91/1000")),
    (3, (0, 0, 0, 1, 1, 0), (0, "-277/200", "39/250", "-81/1000")),
    (3, (0, 0, 1, 0, 0, 0), (0, "73/250", "107/500", "271/500")),
    (3, (0, 0, 1, 1, 0, 0), (0, "133/250", "29/1000", "573/1000")),
    (4, (0, 0, 0, 0, 0, 0), (0, 0, 0, 0)),
    (4, (0, 0, 0, 0, 0, 1), (0, "-1/500", "-119/500", "239/1000")),
    (4, (0, 0, 0, 0, 0, 2), (0, "1/1000", "13/40", "77/25")),
    (4, (0, 0, 0, 0, 1, 0), (0, "-147/500", "23/500", "32/125")),
    (4, (0, 0, 0, 0, 1, 1), (0, "261/1000", "19/125", "-191/500")),
    (4, (0, 0, 0, 1, 1, 0), (0, "-111/250", "251/1000", "1/4")),
    (4, (0, 0, 0, 1, 1, 1), (0, "-63/125", "493/1000", "27/1000")),
    (4, (0, 0, 0, 1, 1, 2), (0, "1/1000", "62/125", "1013/500")),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pairs():
    return tuple(combinations(range(4), 2))


def relabel(row, permutation):
    lookup = dict(zip(pairs(), row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in pairs())


def automorphisms(kernel):
    return tuple(p for p in permutations(range(4)) if relabel(kernel, p) == kernel)


def physical_rows(kernel):
    return tuple(product(*(range(m + 1) for m in kernel)))


def switch_row(kernel, row, switch_bits):
    return tuple(m - q if switch_bits[u] ^ switch_bits[v] else q
                 for (u, v), m, q in zip(pairs(), kernel, row))


def canonical_row(kernel, row):
    switched = (switch_row(kernel, row, (0,) + bits)
                for bits in product((0, 1), repeat=3))
    return min(relabel(candidate, p)
               for candidate in switched for p in automorphisms(kernel))


def orbit_transport(kernel, row):
    target = canonical_row(kernel, row)
    for bits in product((0, 1), repeat=3):
        switch_bits = (0,) + bits
        switched = switch_row(kernel, row, switch_bits)
        for permutation in automorphisms(kernel):
            if relabel(switched, permutation) == target:
                return target, switch_bits, permutation
    raise RuntimeError("canonical orbit transport was not found")


def quarter_tangent(a, b):
    """Return tan(alpha/4), alpha the smaller angle between two vectors."""
    denominator = 1 + a * b
    if denominator == 0:
        return Fraction(0)
    raw = abs((a - b) / denominator)
    if raw > 1:
        raw = 1 / raw
    return raw


def negate_quarter_tangent(t):
    """Quarter-angle tangent after negating the endpoint correlation."""
    return abs((1 - t) / (1 + t))


def correlation(t):
    return (1 - 6 * t * t + t ** 4) / (1 + t * t) ** 2


def odd_cost(t):
    require(t != 0, "odd canonical path has infinite certificate cost")
    return ((1 - t * t) / (2 * t)) ** 2


def even_cost(t):
    return 2 * t * t


def determinant(matrix):
    work = [list(row) for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((r for r in range(column, len(work))
                      if work[r][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result *= value
        for j in range(column, len(work)):
            work[column][j] /= value
        for i in range(column + 1, len(work)):
            factor = work[i][column]
            for j in range(column, len(work)):
                work[i][j] -= factor * work[column][j]
    return result


def gram(parameters):
    ts = {(u, v): quarter_tangent(parameters[u], parameters[v])
          for u, v in pairs()}
    matrix = [[Fraction(int(i == j)) for j in range(4)] for i in range(4)]
    for (u, v), t in ts.items():
        matrix[u][v] = matrix[v][u] = correlation(t)
    return tuple(tuple(row) for row in matrix), ts


def gram_from_squares(squares):
    matrix = [[Fraction(int(i == j)) for j in range(4)] for i in range(4)]
    for (u, v), x in zip(pairs(), squares):
        matrix[u][v] = matrix[v][u] = (1 - 6 * x + x * x) / (1 + x) ** 2
    return tuple(tuple(row) for row in matrix)


def certificate_cost(kernel, row, parameters):
    if parameters[0] == "x":
        squares = tuple(Fraction(x) for x in parameters[1:])
        require(len(squares) == 6, "square certificate has wrong width")
        total = Fraction(0)
        for x, multiplicity, odd_count in zip(squares, kernel, row):
            if odd_count:
                require(x > 0, "odd path has infinite square-certificate cost")
                total += odd_count * (1 - x) ** 2 / (4 * x)
            total += (multiplicity - odd_count) * 2 * x
        return total, gram_from_squares(squares)
    matrix, ts = gram(parameters)
    total = Fraction(0)
    for edge, multiplicity, odd_count in zip(pairs(), kernel, row):
        if not multiplicity:
            require(odd_count == 0, "nonedge has nonzero bundle count")
            continue
        t = ts[edge]
        if odd_count:
            total += odd_count * odd_cost(t)
        total += (multiplicity - odd_count) * even_cost(t)
    return total, matrix


def switched_certificate_cost(kernel, row, parameters, switch_bits):
    total = Fraction(0)
    for (u, v), multiplicity, odd_count in zip(pairs(), kernel, row):
        if not multiplicity:
            continue
        t = quarter_tangent(parameters[u], parameters[v])
        if switch_bits[u] ^ switch_bits[v]:
            t = negate_quarter_tangent(t)
        if odd_count:
            total += odd_count * odd_cost(t)
        total += (multiplicity - odd_count) * even_cost(t)
    return total


def transported_cost(kernel, row, parameters, switch_bits, permutation):
    inverse = tuple(permutation.index(v) for v in range(4))
    if parameters[0] == "x":
        require(not any(switch_bits), "square fixture requires canonical transport")
        require(permutation == tuple(range(4)), "square fixture requires canonical labelling")
        return certificate_cost(kernel, row, parameters)[0]
    pulled = tuple(parameters[inverse[v]] for v in range(4))
    return switched_certificate_cost(kernel, row, pulled, switch_bits)


def principal_submatrix(matrix, indices):
    return tuple(tuple(matrix[i][j] for j in indices) for i in indices)


def audit():
    require(tuple(sum(kernel) for kernel in KERNELS) == (7,) * 5,
            "kernel edge ledger changed")
    rows = tuple(tuple(physical_rows(kernel)) for kernel in KERNELS)
    require(tuple(map(len, rows)) == (72, 72, 54, 48, 96),
            "physical-row counts changed")
    require(sum(map(len, rows)) == 342, "physical-row total changed")

    representatives = tuple(tuple(sorted({canonical_row(kernel, row)
                                          for row in kernel_rows}))
                            for kernel, kernel_rows in zip(KERNELS, rows))
    require(tuple(map(len, representatives)) == (6, 6, 7, 6, 8),
            "orbit counts by kernel changed")
    require(sum(map(len, representatives)) == 33, "orbit total changed")

    fixture = {(kernel_index, row): (parameters if parameters[0] == "x" else
                                     tuple(Fraction(x) for x in parameters))
               for kernel_index, row, parameters in CERTIFICATES}
    require(len(fixture) == len(CERTIFICATES), "duplicate certificate key")
    expected_keys = {(i, row) for i, reps in enumerate(representatives) for row in reps}
    require(set(fixture) == expected_keys, "certificate fixture is not orbit-exact")

    worst = Fraction(0)
    for key in sorted(expected_keys):
        kernel_index, row = key
        parameters = fixture[key]
        require(len(parameters) in (4, 7), "certificate parameter width changed")
        cost, matrix = certificate_cost(KERNELS[kernel_index], row, parameters)
        for size in range(1, 5):
            for indices in combinations(range(4), size):
                require(determinant(principal_submatrix(matrix, indices)) >= 0,
                        "Gram matrix failed exact principal-minor PSD test")
        require(cost <= 3, "exact canonical excess exceeds three")
        worst = max(worst, cost)

    # Every physical row maps to one and only one checked orbit key.
    covered = 0
    transport_failures = 0
    for i, (kernel, kernel_rows) in enumerate(zip(KERNELS, rows)):
        for row in kernel_rows:
            representative, switch_bits, permutation = orbit_transport(kernel, row)
            require((i, representative) in fixture,
                    "physical row lacks an orbit certificate")
            require(len(switch_bits) == 4 and len(permutation) == 4,
                    "malformed orbit transport witness")
            parameters = fixture[(i, representative)]
            if parameters[0] == "x":
                if row != representative:
                    transport_failures += 1
            else:
                try:
                    physical_cost = transported_cost(
                        kernel, row, parameters, switch_bits, permutation)
                except RuntimeError:
                    transport_failures += 1
                else:
                    if physical_cost > 3:
                        transport_failures += 1
            covered += 1
    require(covered == 342, "physical coverage ledger changed")
    return representatives, worst, transport_failures


def main():
    representatives, worst, transport_failures = audit()
    print("four-vertex rank-four DNN census: exact enumeration passed")
    print("physical_rows_by_kernel: 72,72,54,48,96 (total 342)")
    print("orbits_by_kernel: " + ",".join(str(len(x)) for x in representatives) +
          " (total 33)")
    print(f"maximum_certified_excess: {worst}")
    print(f"failed_physical_transports: {transport_failures}")
    require(transport_failures == 0,
            "BLOCKER: orbit representatives do not certify every physical row")


if __name__ == "__main__":
    main()
