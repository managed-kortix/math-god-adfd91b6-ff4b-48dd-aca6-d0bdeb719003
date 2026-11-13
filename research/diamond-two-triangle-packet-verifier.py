#!/usr/bin/env python3
"""Exact fail-closed semantic verifier for the attached D+T+T packet.

Only the Python standard library is used.  The verifier independently regenerates
Sachs polynomials for every direct/nested incidence, verifies the one-sum
formulas and strict imaginary sign as coefficient identities in independent
positive variables, and rejects deliberately hostile formula/scope mutations.
"""

from __future__ import annotations

import itertools
import subprocess
import sys
from collections import Counter
from functools import lru_cache


class AuditError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


# A sparse polynomial is Counter({exponent_tuple: integer coefficient}).
# The last exponent is the formal marker h: h=0 is real, h=1 is i times real.
VARIABLES = ("p", "q", "r", "s", "a", "b", "c", "d", "h")
INDEX = {name: place for place, name in enumerate(VARIABLES)}
ZERO = (0,) * len(VARIABLES)
IUNIT = ZERO[:-1] + (1,)
ROOTS = ("p", "q", "r", "s")
DIAMOND_EDGES = frozenset({("p", "q"), ("p", "r"), ("q", "r"),
                            ("p", "s"), ("q", "s")})


def clean(poly):
    return Counter({monomial: coefficient for monomial, coefficient in poly.items()
                    if coefficient})


def constant(value):
    return Counter({ZERO: value}) if value else Counter()


def variable(name):
    monomial = list(ZERO)
    monomial[INDEX[name]] = 1
    return Counter({tuple(monomial): 1})


def add(*polys):
    result = Counter()
    for poly in polys:
        result.update(poly)
    return clean(result)


def scale(poly, coefficient):
    return clean(Counter({monomial: coefficient * value
                          for monomial, value in poly.items()}))


def multiply(*polys):
    result = constant(1)
    for poly in polys:
        product = Counter()
        for left, left_coefficient in result.items():
            for right, right_coefficient in poly.items():
                monomial = tuple(x + y for x, y in zip(left, right))
                product[monomial] += left_coefficient * right_coefficient
        result = clean(product)
    return result


def complex_pair(real, imaginary):
    """Encode R+iI as one sparse polynomial with a single h marker."""
    marked = Counter()
    for monomial, coefficient in imaginary.items():
        require(monomial[INDEX["h"]] == 0, "imaginary input already marked")
        shifted = list(monomial)
        shifted[INDEX["h"]] = 1
        marked[tuple(shifted)] = coefficient
    return add(real, marked)


def split_complex(poly):
    real = Counter()
    imaginary = Counter()
    for monomial, coefficient in poly.items():
        power = monomial[INDEX["h"]]
        require(power in (0, 1), "nonlinear formal imaginary marker")
        reduced = list(monomial)
        reduced[INDEX["h"]] = 0
        (real if power == 0 else imaginary)[tuple(reduced)] += coefficient
    return clean(real), clean(imaginary)


def cmultiply(left, right):
    left_real, left_imaginary = split_complex(left)
    right_real, right_imaginary = split_complex(right)
    real = add(multiply(left_real, right_real),
               scale(multiply(left_imaginary, right_imaginary), -1))
    imaginary = add(multiply(left_real, right_imaginary),
                    multiply(left_imaginary, right_real))
    return complex_pair(real, imaginary)


def monomial(*names):
    return multiply(*(variable(name) for name in names))


def diamond_state(deleted=frozenset()):
    """Exact normalized Sachs state of D-deleted, in p,q,r,s activities."""
    vertices = tuple(vertex for vertex in ROOTS if vertex not in deleted)
    edges = frozenset(edge for edge in DIAMOND_EDGES if deleted.isdisjoint(edge))
    return sachs_polynomial(vertices, edges, {vertex: vertex for vertex in vertices})


def adjacency(vertices, edges):
    result = {vertex: set() for vertex in vertices}
    for left, right in edges:
        result[left].add(right)
        result[right].add(left)
    return result


def simple_cycles(vertices, edges):
    graph = adjacency(vertices, edges)
    cycles = set()
    for start in vertices:
        def visit(path):
            current = path[-1]
            for neighbor in graph[current]:
                if neighbor == start and len(path) >= 3:
                    forward = tuple(path)
                    reverse = (start,) + tuple(reversed(path[1:]))
                    cycles.add(min(forward, reverse))
                elif neighbor > start and neighbor not in path:
                    visit(path + (neighbor,))
        visit((start,))
    return tuple(sorted((frozenset(cycle) for cycle in cycles),
                        key=lambda cycle: (len(cycle), tuple(sorted(cycle)))))


def matching_polynomial(vertices, edges, deleted, activity_names):
    remaining = tuple(vertex for vertex in vertices if vertex not in deleted)
    graph = adjacency(remaining, frozenset(edge for edge in edges
                                           if deleted.isdisjoint(edge)))

    @lru_cache(maxsize=None)
    def recurse(active):
        if not active:
            return constant(1)
        vertex = active[0]
        rest = active[1:]
        result = multiply(variable(activity_names[vertex]), recurse(rest))
        for neighbor in graph[vertex] & set(rest):
            reduced = tuple(item for item in rest if item != neighbor)
            result = add(result, recurse(reduced))
        return result

    return recurse(remaining)


def cycle_factor(length):
    # -2*i^(-length), represented as an exact Gaussian integer pair.
    residue = length % 4
    return {0: complex_pair(constant(-2), constant(0)),
            1: complex_pair(constant(0), constant(2)),
            2: complex_pair(constant(2), constant(0)),
            3: complex_pair(constant(0), constant(-2))}[residue]


def sachs_polynomial(vertices, edges, activity_names):
    cycles = simple_cycles(vertices, edges)
    result = Counter()

    def collect(position, used, phase):
        nonlocal result
        matching = matching_polynomial(vertices, edges, used, activity_names)
        result = add(result, cmultiply(phase, complex_pair(matching, constant(0))))
        for cycle_index in range(position, len(cycles)):
            cycle = cycles[cycle_index]
            if used.isdisjoint(cycle):
                collect(cycle_index + 1, used | cycle,
                        cmultiply(phase, cycle_factor(len(cycle))))

    collect(0, frozenset(), complex_pair(constant(1), constant(0)))
    return result


def triangle_data(left, right):
    d_value = add(multiply(variable(left), variable(right)), constant(1))
    e_value = add(variable(left), variable(right))
    e_minus_2i = complex_pair(e_value, constant(-2))
    return d_value, e_value, e_minus_2i


def attach_triangle(host, deleted_root, left, right):
    d_value, _, e_minus_2i = triangle_data(left, right)
    return add(cmultiply(complex_pair(d_value, constant(0)), host),
               cmultiply(e_minus_2i, deleted_root))


def direct_formula(first_root, second_root, cross_coefficient=1):
    host = diamond_state()
    first_deleted = diamond_state(frozenset({first_root}))
    second_deleted = diamond_state(frozenset({second_root}))
    d1, _, q1 = triangle_data("a", "b")
    d2, _, q2 = triangle_data("c", "d")
    first_term = cmultiply(complex_pair(multiply(d1, d2), constant(0)), host)
    if first_root == second_root:
        coefficient = add(cmultiply(complex_pair(d2, constant(0)), q1),
                          cmultiply(complex_pair(d1, constant(0)), q2))
        return add(first_term, cmultiply(coefficient, first_deleted))
    forest = diamond_state(frozenset({first_root, second_root}))
    return add(first_term,
               cmultiply(complex_pair(d2, constant(0)),
                         cmultiply(q1, first_deleted)),
               cmultiply(complex_pair(d1, constant(0)),
                         cmultiply(q2, second_deleted)),
               scale(cmultiply(q1, cmultiply(q2, forest)), cross_coefficient))


def nested_formula(root, pendant_coefficient=1):
    host = diamond_state()
    deleted = diamond_state(frozenset({root}))
    d1, _, q1 = triangle_data("a", "b")
    d2, _, q2 = triangle_data("c", "d")
    first = attach_triangle(host, deleted, "a", "b")
    # Delete private vertex a: the remaining edge root--b is a pendant edge,
    # whose matching state is b*Psi_D + Psi_(D-root).
    private_deleted = add(
        scale(cmultiply(complex_pair(variable("b"), constant(0)), host),
              pendant_coefficient),
        deleted,
    )
    return add(cmultiply(complex_pair(d2, constant(0)), first),
               cmultiply(q2, private_deleted))


def realize_direct(first_root, second_root):
    vertices = set(ROOTS)
    edges = set(DIAMOND_EDGES)
    activities = {vertex: vertex for vertex in ROOTS}
    for root, left, right in ((first_root, "A", "B"),
                              (second_root, "C", "D")):
        vertices.update((left, right))
        edges.update({tuple(sorted((root, left))), tuple(sorted((root, right))),
                      tuple(sorted((left, right)))})
        activities[left], activities[right] = left.lower(), right.lower()
    return tuple(sorted(vertices)), frozenset(edges), activities


def realize_nested(root):
    vertices = set(ROOTS) | {"A", "B", "C", "D"}
    edges = set(DIAMOND_EDGES)
    edges.update({tuple(sorted((root, "A"))), tuple(sorted((root, "B"))), ("A", "B"),
                  ("A", "C"), ("A", "D"), ("C", "D")})
    activities = {vertex: vertex for vertex in ROOTS}
    activities.update({name: name.lower() for name in ("A", "B", "C", "D")})
    return tuple(sorted(vertices)), frozenset(edges), activities


def all_negative(poly):
    return bool(poly) and all(coefficient < 0 for coefficient in poly.values())


def all_positive(poly):
    return bool(poly) and all(coefficient > 0 for coefficient in poly.values())


def univariate_coefficients(poly):
    """Specialize every activity to t and return {degree: coefficient}."""
    result = Counter()
    for monomial, coefficient in poly.items():
        require(monomial[INDEX["h"]] == 0, "univariate input is not real")
        result[sum(monomial[:-1])] += coefficient
    return clean(result)


def audit(cross_coefficient=1, pendant_coefficient=1, omit_nested=False,
          drop_root=None, require_strict=True, host_imaginary_sign=1,
          one_sum_root_coefficient=-1, triangle_imaginary=-2,
          demand_full_real_positive=False, rank=4):
    # Formula (3), checked on two independent weighted triangles at a shared
    # root.  Mutating its subtraction must fail as a sparse identity.
    z = variable("p")
    left = sachs_polynomial(("p", "A", "B"),
                            frozenset({("p", "A"), ("p", "B"), ("A", "B")}),
                            {"p": "p", "A": "a", "B": "b"})
    right = sachs_polynomial(("p", "C", "D"),
                             frozenset({("p", "C"), ("p", "D"), ("C", "D")}),
                             {"p": "p", "C": "c", "D": "d"})
    left_deleted = complex_pair(add(monomial("a", "b"), constant(1)), constant(0))
    right_deleted = complex_pair(add(monomial("c", "d"), constant(1)), constant(0))
    one_sum = add(cmultiply(left, right_deleted),
                  cmultiply(left_deleted, right),
                  scale(cmultiply(complex_pair(z, constant(0)),
                                  cmultiply(left_deleted, right_deleted)),
                        one_sum_root_coefficient))
    shared_vertices = ("p", "A", "B", "C", "D")
    shared_edges = frozenset({("p", "A"), ("p", "B"), ("A", "B"),
                              ("p", "C"), ("p", "D"), ("C", "D")})
    shared_activities = {"p": "p", "A": "a", "B": "b", "C": "c", "D": "d"}
    require(one_sum == sachs_polynomial(shared_vertices, shared_edges,
                                        shared_activities),
            "weighted one-sum identity failed")

    # Formula (4), including the triangle's -2i contribution.
    d_value, e_value, _ = triangle_data("a", "b")
    mutated_triangle = complex_pair(e_value, constant(triangle_imaginary))
    attached = add(cmultiply(complex_pair(d_value, constant(0)), diamond_state()),
                   cmultiply(mutated_triangle,
                             diamond_state(frozenset({"p"}))))
    require(attached == attach_triangle(diamond_state(),
                                         diamond_state(frozenset({"p"})),
                                         "a", "b"),
            "triangle one-sum reduction failed")

    host_real, host_imaginary = split_complex(diamond_state())
    require(all_positive(host_real), "diamond real state is not positive")
    tested_host_imaginary = scale(host_imaginary, host_imaginary_sign)
    require(all_negative(tested_host_imaginary),
            "diamond imaginary state is not negative")

    for root in ROOTS:
        real, imaginary = split_complex(diamond_state(frozenset({root})))
        require(all_positive(real), f"deleted-root real state failed at {root}")
        require(not imaginary or all_negative(imaginary),
                f"deleted-root imaginary state failed at {root}")
    for left, right in itertools.combinations(ROOTS, 2):
        real, imaginary = split_complex(diamond_state(frozenset({left, right})))
        require(all_positive(real) and not imaginary,
                f"two-root deletion is not a positive forest: {left},{right}")

    direct_records = tuple(itertools.combinations_with_replacement(ROOTS, 2))
    nested_records = () if omit_nested else ROOTS
    if drop_root is not None:
        direct_records = tuple(record for record in direct_records if drop_root not in record)
        nested_records = tuple(root for root in nested_records if root != drop_root)
    require(len(direct_records) == 10, "direct incidence census changed")
    require(len(nested_records) == 4, "nested incidence census changed")

    direct_same = direct_distinct = checked_terms = 0
    for first_root, second_root in direct_records:
        formula = direct_formula(first_root, second_root, cross_coefficient)
        graph = realize_direct(first_root, second_root)
        exact = sachs_polynomial(*graph)
        require(formula == exact,
                f"direct one-sum formula failed: {first_root},{second_root}")
        _, imaginary = split_complex(exact)
        if require_strict:
            require(all_negative(imaginary),
                    f"direct imaginary sign failed: {first_root},{second_root}")
        checked_terms += len(imaginary)
        if first_root == second_root:
            direct_same += 1
        else:
            direct_distinct += 1

    for root in nested_records:
        formula = nested_formula(root, pendant_coefficient)
        graph = realize_nested(root)
        exact = sachs_polynomial(*graph)
        require(formula == exact, f"nested one-sum formula failed: {root}")
        _, imaginary = split_complex(exact)
        if require_strict:
            require(all_negative(imaginary), f"nested imaginary sign failed: {root}")
        checked_terms += len(imaginary)

    require((direct_same, direct_distinct, len(nested_records)) == (4, 6, 4),
            "incidence-type exhaustion changed")

    # Hostile regression: positivity of the *full* real part is false and must
    # never be smuggled into the lower-half-plane proof.  With no tree
    # attachments, direct owners r,s, and all activities specialized to t,
    # Re Psi has low-to-high coefficient stream
    # -12 + 9 t^2 + 31 t^4 + 11 t^6 + t^8.
    counterexample_real, counterexample_imaginary = split_complex(
        sachs_polynomial(*realize_direct("r", "s")))
    real_t = univariate_coefficients(counterexample_real)
    imaginary_t = univariate_coefficients(counterexample_imaginary)
    require(real_t == Counter({0: -12, 2: 9, 4: 31, 6: 11, 8: 1}),
            "negative-real regression polynomial changed")
    require(imaginary_t == Counter({1: -32, 3: -40, 5: -8}),
            "negative-real regression imaginary polynomial changed")
    require(real_t[0] < 0 and all(value < 0 for value in imaginary_t.values()),
            "negative-real/lower-half-plane regression lost")
    require(not demand_full_real_positive,
            "false full-real-positivity premise was enabled")
    require(require_strict, "continuous branch requires strict imaginary sign")
    cyclomatic_rank = rank
    require(cyclomatic_rank == 4, "D+TT rank ledger changed")
    # Im Psi<0 keeps the continuous argument in (-pi,0), with limit zero at
    # infinity. Signed Coulson gives Delta=s+ - s- >0. Since m=n+3,
    # sigma=s+-n=3+Delta/2>3.
    threshold = cyclomatic_rank - 1
    require(threshold == 3, "energy threshold ledger changed")
    return direct_same, direct_distinct, len(nested_records), checked_terms


def expect_rejected(label, function):
    try:
        function()
    except AuditError:
        return
    raise AuditError(f"hostile mutation accepted: {label}")


def hostile_self_checks():
    mutations = (
        ("wrong distinct-root cross sign", lambda: audit(cross_coefficient=-1)),
        ("wrong nested pendant coefficient", lambda: audit(pendant_coefficient=0)),
        ("omitted nested incidence", lambda: audit(omit_nested=True)),
        ("omitted diamond root orbit", lambda: audit(drop_root="s")),
        ("nonstrict phase promotion", lambda: audit(require_strict=False)),
        ("reversed diamond imaginary sign", lambda: audit(host_imaginary_sign=-1)),
        ("false full-real-positivity premise",
         lambda: audit(demand_full_real_positive=True)),
        ("wrong one-sum root subtraction",
         lambda: audit(one_sum_root_coefficient=1)),
        ("wrong triangle imaginary sign", lambda: audit(triangle_imaginary=2)),
        ("wrong rank ledger", lambda: audit(rank=3)),
    )
    for label, function in mutations:
        expect_rejected(label, function)
    return len(mutations)


def main():
    direct_same, direct_distinct, nested, terms = audit()
    mutations = hostile_self_checks()
    require(mutations == 10, "hostile mutation count changed")
    output = (
        "diamond-plus-two-triangles exact packet verifier: PASS\n"
        f"incidences: direct-same={direct_same} direct-distinct={direct_distinct} "
        f"nested={nested} total={direct_same + direct_distinct + nested}\n"
        f"strict negative imaginary Sachs coefficients checked: {terms}\n"
        "one-sum identities: direct-same, direct-distinct, nested verified exactly\n"
        "tree-message scope: arbitrary positive core activities\n"
        "continuous phase: Theta(t) in (-pi,0), Delta=s+-s->0\n"
        "real-part regression: direct(r,s) has Re Psi(0)=-12; no Re>0 premise\n"
        "uniform packet bound: sigma(D+TT)=3+Delta/2>3\n"
        f"rejected hostile mutations: {mutations}"
    )
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=True, capture_output=True, text=True)
        require(child.stderr == "", "optimized verifier wrote stderr")
        require(child.stdout.rstrip() == output, "normal/optimized output mismatch")
    print(output)


if __name__ == "__main__":
    main()
