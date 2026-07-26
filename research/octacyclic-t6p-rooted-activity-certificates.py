#!/usr/bin/env python3
"""Exact Schur/Sachs certificate search for the four rooted T^6 P kernels.

The search is attachment-uniform: every core vertex v has activity a_v=t+y_v
with y_v >= 0 after arbitrary rooted trees are Schur-complemented.  A failed
coefficient in the y-constant specialization is therefore an exact obstruction
to a coefficientwise certificate in all activity variables.
"""

from fractions import Fraction
from functools import lru_cache
import hashlib


KERNELS = {
    "R1": ("private", 0, ((0, 6), (0, 7), (1, 6), (2, 7), (3, 6), (4, 6), (5, 7))),
    "R2": ("private", 0, ((0, 6), (0, 7), (1, 6), (1, 8), (2, 7), (3, 6), (4, 7), (5, 8))),
    "R3": ("private", 0, ((0, 6), (0, 7), (1, 6), (1, 8), (2, 7), (3, 6), (3, 9), (4, 8), (5, 9))),
    "R4": ("cut", 6, ((0, 6), (0, 7), (1, 6), (1, 8), (2, 7), (3, 6), (3, 9), (4, 8), (5, 9))),
}


def realize(kind, root_label, incidence):
    cuts = sorted({cut for _, cut in incidence})
    cut_vertex = {cut: index for index, cut in enumerate(cuts)}
    next_vertex = len(cuts)
    triangles = []
    private = {}
    for cycle in range(6):
        vertices = [cut_vertex[cut] for item, cut in incidence if item == cycle]
        while len(vertices) < 3:
            private.setdefault(cycle, []).append(next_vertex)
            vertices.append(next_vertex)
            next_vertex += 1
        triangles.append(tuple(vertices))
    root = private[root_label][0] if kind == "private" else cut_vertex[root_label]
    pentagon = (root, next_vertex, next_vertex + 1, next_vertex + 2, next_vertex + 3)
    vertex_count = next_vertex + 4
    cycles = triangles + [pentagon]
    edges = set()
    for cycle in cycles:
        for left, right in zip(cycle, cycle[1:] + cycle[:1]):
            edges.add(tuple(sorted((left, right))))
    return vertex_count, tuple(sorted(edges)), tuple(triangles), pentagon


def add(left, right):
    size = max(len(left), len(right))
    return tuple(
        (left[index] if index < len(left) else 0)
        + (right[index] if index < len(right) else 0)
        for index in range(size)
    )


def shift(poly):
    return (0,) + poly


def scale(poly, scalar):
    return tuple(scalar * coefficient for coefficient in poly)


def multiply(left, right):
    answer = [0] * (len(left) + len(right) - 1)
    for left_degree, left_coefficient in enumerate(left):
        for right_degree, right_coefficient in enumerate(right):
            answer[left_degree + right_degree] += left_coefficient * right_coefficient
    return tuple(answer)


def matching_polynomial(vertex_count, edges, deleted):
    remaining = ((1 << vertex_count) - 1) & ~sum(1 << vertex for vertex in deleted)
    neighbors = [0] * vertex_count
    for left, right in edges:
        neighbors[left] |= 1 << right
        neighbors[right] |= 1 << left

    @lru_cache(maxsize=None)
    def visit(mask):
        if not mask:
            return (1,)
        bit = mask & -mask
        vertex = bit.bit_length() - 1
        rest = mask ^ bit
        answer = shift(visit(rest))
        choices = neighbors[vertex] & rest
        while choices:
            other_bit = choices & -choices
            answer = add(answer, visit(rest ^ other_bit))
            choices ^= other_bit
        return answer

    return visit(remaining)


def activity_matching_polynomial(vertex_count, edges, deleted):
    remaining = ((1 << vertex_count) - 1) & ~sum(1 << vertex for vertex in deleted)
    neighbors = [0] * vertex_count
    for left, right in edges:
        neighbors[left] |= 1 << right
        neighbors[right] |= 1 << left

    @lru_cache(maxsize=None)
    def visit(mask):
        if not mask:
            return {0: 1}
        bit = mask & -mask
        vertex = bit.bit_length() - 1
        rest = mask ^ bit
        answer = {unmatched | bit: coefficient for unmatched, coefficient in visit(rest).items()}
        choices = neighbors[vertex] & rest
        while choices:
            other_bit = choices & -choices
            for unmatched, coefficient in visit(rest ^ other_bit).items():
                answer[unmatched] = answer.get(unmatched, 0) + coefficient
            choices ^= other_bit
        return answer

    return visit(remaining)


def grouped_sachs(vertex_count, edges, triangles, pentagon):
    cycles = triangles + (pentagon,)
    multipliers = (-2j,) * 6 + (2j,)
    answer = (0,)
    for mask in range(1 << 7):
        deleted = set()
        multiplier = 1
        legal = True
        for index, cycle in enumerate(cycles):
            if not mask & (1 << index):
                continue
            if deleted.intersection(cycle):
                legal = False
                break
            deleted.update(cycle)
            multiplier *= multipliers[index]
        if legal:
            answer = add(
                answer,
                scale(
                    matching_polynomial(vertex_count, edges, frozenset(deleted)),
                    multiplier,
                ),
            )
    return (
        tuple(int(coefficient.real) for coefficient in answer),
        tuple(int(coefficient.imag) for coefficient in answer),
    )


def grouped_sachs_activity(vertex_count, edges, triangles, pentagon):
    cycles = triangles + (pentagon,)
    multipliers = (-2j,) * 6 + (2j,)
    answer = {}
    for mask in range(1 << 7):
        deleted = set()
        multiplier = 1
        for index, cycle in enumerate(cycles):
            if mask & (1 << index):
                if deleted.intersection(cycle):
                    break
                deleted.update(cycle)
                multiplier *= multipliers[index]
        else:
            for unmatched, coefficient in activity_matching_polynomial(
                vertex_count, edges, frozenset(deleted)
            ).items():
                answer[unmatched] = answer.get(unmatched, 0) + multiplier * coefficient
    return (
        {
            unmatched: int(coefficient.real)
            for unmatched, coefficient in answer.items()
            if coefficient.real
        },
        {
            unmatched: int(coefficient.imag)
            for unmatched, coefficient in answer.items()
            if coefficient.imag
        },
    )


def shift_to_nonnegative_orthant(activity_poly, vertex_count, scalar=1):
    """Substitute a_v=t+y_v; key is (t degree, y-mask)."""
    answer = {}
    for activity_mask, coefficient in activity_poly.items():
        coefficient *= scalar
        y_mask = activity_mask
        while True:
            key = (activity_mask.bit_count() - y_mask.bit_count(), y_mask)
            answer[key] = answer.get(key, 0) + coefficient
            if not y_mask:
                break
            y_mask = (y_mask - 1) & activity_mask
    return {key: coefficient for key, coefficient in answer.items() if coefficient}


def multivariate_audit(poly, vertex_count):
    failed = tuple(sorted((key, coefficient) for key, coefficient in poly.items() if coefficient < 0))
    payload = "\n".join(
        f"{t_degree}:{y_mask:0{vertex_count}b}:{coefficient}"
        for (t_degree, y_mask), coefficient in sorted(poly.items())
    ).encode("ascii")
    return len(poly), failed, min(poly.values()), max(poly.values()), hashlib.sha256(payload).hexdigest()


def add_multivariate(left, right):
    answer = dict(left)
    for key, coefficient in right.items():
        answer[key] = answer.get(key, 0) + coefficient
        if not answer[key]:
            del answer[key]
    return answer


def scale_multivariate(poly, scalar):
    return {key: scalar * coefficient for key, coefficient in poly.items()}


def multiply_by_univariate(poly, univariate):
    answer = {}
    for (t_degree, y_mask), coefficient in poly.items():
        for extra_degree, extra_coefficient in enumerate(univariate):
            if extra_coefficient:
                key = (t_degree + extra_degree, y_mask)
                answer[key] = answer.get(key, 0) + coefficient * extra_coefficient
    return {key: coefficient for key, coefficient in answer.items() if coefficient}


def evaluate_multivariate(poly, t_value, y_values):
    answer = Fraction(0)
    for (t_degree, y_mask), coefficient in poly.items():
        term = Fraction(coefficient) * t_value**t_degree
        while y_mask:
            bit = y_mask & -y_mask
            term *= y_values[bit.bit_length() - 1]
            y_mask ^= bit
        answer += term
    return answer


def orthant_witness(poly, failed, vertex_count):
    if not failed:
        return None
    for (unused_degree, mask), unused_coefficient in failed[:100]:
        del unused_degree, unused_coefficient
        for t_value in (Fraction(1), Fraction(1, 10), Fraction(1, 100)):
            for magnitude in (1, 10, 100, 1000, 10000):
                values = [Fraction(0)] * vertex_count
                for vertex in range(vertex_count):
                    if mask & (1 << vertex):
                        values[vertex] = Fraction(magnitude)
                value = evaluate_multivariate(poly, t_value, values)
                if value < 0:
                    return t_value, mask, magnitude, value
    return None


def negative_terms(poly):
    return tuple(
        (degree, coefficient)
        for degree, coefficient in reversed(tuple(enumerate(poly)))
        if coefficient < 0
    )


def evaluate(poly, point):
    answer = Fraction(0)
    for coefficient in reversed(poly):
        answer = answer * point + coefficient
    return answer


def first_negative_value(poly):
    for denominator in (100, 20, 10, 5, 2, 1, 10):
        point = Fraction(1, denominator)
        value = evaluate(poly, point)
        if value < 0:
            return point, value
    return None


def format_polynomial(poly):
    terms = []
    for degree, coefficient in reversed(tuple(enumerate(poly))):
        if not coefficient:
            continue
        sign = "+" if coefficient > 0 else "-"
        magnitude = abs(coefficient)
        variable = "" if degree == 0 else ("t" if degree == 1 else f"t^{degree}")
        factor = "" if variable and magnitude == 1 else str(magnitude)
        terms.append((sign, factor + variable))
    if not terms:
        return "0"
    sign, term = terms[0]
    answer = ("-" if sign == "-" else "") + term
    return answer + "".join(f" {sign} {term}" for sign, term in terms[1:])


def main():
    z5 = (0, 5, 0, 5, 0, 1)
    for name, (kind, root_label, incidence) in KERNELS.items():
        vertex_count, edges, triangles, pentagon = realize(kind, root_label, incidence)
        real, imag = grouped_sachs(vertex_count, edges, triangles, pentagon)
        activity_real, activity_imag = grouped_sachs_activity(
            vertex_count, edges, triangles, pentagon
        )
        real_chart = shift_to_nonnegative_orthant(activity_real, vertex_count)
        lower_half_plane = shift_to_nonnegative_orthant(activity_imag, vertex_count, -1)
        imag_chart = shift_to_nonnegative_orthant(activity_imag, vertex_count)
        cross_product = add_multivariate(
            scale_multivariate(real_chart, 2),
            scale_multivariate(multiply_by_univariate(imag_chart, z5), -1),
        )
        tests = {
            "real_chart_R": real,
            "lower_half_plane_-I": scale(imag, -1),
            "pentagon_cross_product_2R-Z5I": add(scale(real, 2), scale(multiply(z5, imag), -1)),
        }
        print(f"{name}: n={vertex_count} root={kind}:{root_label}")
        print(f"  R={format_polynomial(real)}")
        print(f"  I={format_polynomial(imag)}")
        for activity_label, activity_test in (
            ("R", real_chart),
            ("-I", lower_half_plane),
            ("2R-Z5I", cross_product),
        ):
            term_count, multivariate_failed, minimum, maximum, digest = multivariate_audit(
                activity_test, vertex_count
            )
            print(
                f"  full_activity_{activity_label}: "
                f"terms={term_count} negative_terms={len(multivariate_failed)} "
                f"min={minimum} max={maximum} sha256={digest}"
            )
            if multivariate_failed:
                print(f"    first_failed_terms={multivariate_failed[:20]}")
                print(
                    "    exact_orthant_witness(t,mask,M,value)="
                    f"{orthant_witness(activity_test, multivariate_failed, vertex_count)}"
                )
        for label, polynomial in tests.items():
            failed = negative_terms(polynomial)
            witness = first_negative_value(polynomial)
            print(f"  {label}: negative_y_constant_terms={failed}")
            print(f"    negative_rational_witness={witness}")
        print()


if __name__ == "__main__":
    main()
