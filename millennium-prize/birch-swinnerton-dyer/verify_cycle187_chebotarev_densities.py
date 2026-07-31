#!/usr/bin/env python3
"""Exact finite-group checks for the Cycle 187 Chebotarev table."""

from fractions import Fraction


P = 7


def det(a):
    return (a[0] * a[3] - a[1] * a[2]) % P


def mul(a, b):
    return tuple(
        sum(a[2 * i + k] * b[2 * k + j] for k in range(2)) % P
        for i in range(2)
        for j in range(2)
    )


def inv(a):
    d_inv = pow(det(a), -1, P)
    return (
        a[3] * d_inv % P,
        -a[1] * d_inv % P,
        -a[2] * d_inv % P,
        a[0] * d_inv % P,
    )


def residual_type(a):
    trace = (a[0] + a[3]) % P
    discriminant = (trace * trace - 4 * det(a)) % P
    scalar = a[1] == a[2] == 0 and a[0] == a[3]
    has_one = (1 - trace + det(a)) % P == 0
    if a == (1, 0, 0, 1):
        return "identity"
    if has_one and discriminant == 0:
        return "unipotent"
    if has_one:
        return "split_one"
    if scalar:
        return "scalar_no_one"
    if discriminant == 0:
        return "jordan_no_one"
    if pow(discriminant, (P - 1) // 2, P) == 1:
        return "split_no_one"
    return "irreducible"


def main():
    gl2 = [
        (a, b, c, d)
        for a in range(P)
        for b in range(P)
        for c in range(P)
        for d in range(P)
        if det((a, b, c, d))
    ]
    assert len(gl2) == (P * P - 1) * (P * P - P) == 2016

    unseen = set(gl2)
    residual_classes = []
    while unseen:
        a = next(iter(unseen))
        conjugates = {mul(mul(b, a), inv(b)) for b in gl2}
        centralizer = [b for b in gl2 if mul(a, b) == mul(b, a)]
        assert len(conjugates) * len(centralizer) == len(gl2)
        unseen -= conjugates
        residual_classes.append((residual_type(a), len(centralizer)))

    residual_summary = {}
    for kind, centralizer_size in residual_classes:
        residual_summary.setdefault(kind, []).append(centralizer_size)
    expected_residual = {
        "identity": [2016],
        "unipotent": [42],
        "split_one": [36] * 5,
        "scalar_no_one": [2016] * 5,
        "jordan_no_one": [42] * 5,
        "split_no_one": [36] * 10,
        "irreducible": [48] * 21,
    }
    assert {k: sorted(v) for k, v in residual_summary.items()} == expected_residual

    table = [
        ("identity/zero", 1, 1, Fraction(1, 4_840_416)),
        ("identity/projective rank one", 1, 8, Fraction(1, 100_842)),
        ("identity/rank two", 1, 1, Fraction(1, 2_401)),
        ("nonidentity unipotent/zero", 1, 1, Fraction(1, 2_058)),
        ("nonidentity unipotent/projective", 1, 8, Fraction(1, 343)),
        ("split {1,lambda}/zero", 5, 1, Fraction(1, 1_764)),
        ("split {1,lambda}/projective", 5, 8, Fraction(1, 294)),
        ("scalar lambda I, lambda != 1", 5, 1, Fraction(1, 2_016)),
        ("Jordan lambda, lambda != 1", 5, 1, Fraction(1, 42)),
        ("split distinct, neither eigenvalue 1", 10, 1, Fraction(1, 36)),
        ("irreducible quadratic", 21, 1, Fraction(1, 48)),
    ]
    total_density = sum(
        residual_count * affine_count * density
        for _, residual_count, affine_count, density in table
    )
    assert total_density == 1
    collision_index = sum(
        residual_count * affine_count * density * density
        for _, residual_count, affine_count, density in table
    )
    assert collision_index == Fraction(78_876_293_599, 3_904_937_842_176)
    unipotent_row_collision = Fraction(1 + 8 * 6 * 6, 49 * 49)
    assert unipotent_row_collision == Fraction(289, 2_401)

    largest = max(table, key=lambda row: row[3])
    assert largest[0] == "split distinct, neither eigenvalue 1"
    assert largest[3] == Fraction(1, 36)
    assert largest[3] / 2 == Fraction(1, 72)
    assert Fraction(1, 343) / 2 == Fraction(1, 686)

    print("Cycle 187 exact Chebotarev density checks")
    print("|GL_2(F_7)| =", len(gl2))
    print("residual conjugacy classes =", len(residual_classes))
    print("full Kummer conjugacy classes =", sum(r * a for _, r, a, _ in table))
    for label, residual_count, affine_count, density in table:
        print(label, residual_count, affine_count, density)
    print("total density =", total_density)
    print("full-class collision index =", collision_index)
    print("unipotent row collision probability =", unipotent_row_collision)
    print("densest L0 class =", largest[0], largest[3])
    print("with (q/29)=1 =", largest[3] / 2)
    print("unipotent fixed-projective class with (q/29)=1 =", Fraction(1, 686))
    print("all exact checks passed")


if __name__ == "__main__":
    main()
