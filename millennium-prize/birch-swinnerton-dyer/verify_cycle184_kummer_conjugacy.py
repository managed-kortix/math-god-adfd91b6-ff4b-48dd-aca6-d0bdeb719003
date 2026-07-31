#!/usr/bin/env python3
"""Exact checks for the Cycle 184 semidirect Kummer conjugacy theorem."""


P = 7
J = (1, 1, 0, 1)


def matmul(a, b):
    return tuple(
        sum(a[2 * i + k] * b[2 * k + j] for k in range(2)) % P
        for i in range(2)
        for j in range(2)
    )


def det(a):
    return (a[0] * a[3] - a[1] * a[2]) % P


def act(a, v):
    return (
        (a[0] * v[0] + a[1] * v[1]) % P,
        (a[2] * v[0] + a[3] * v[1]) % P,
    )


def canonical_projective(row):
    x, y = row
    if x == 0 and y == 0:
        return None
    if x:
        inverse = pow(x, -1, P)
        return (1, y * inverse % P)
    return (0, 1)


def main():
    gl2 = [
        (a, b, c, d)
        for a in range(P)
        for b in range(P)
        for c in range(P)
        for d in range(P)
        if det((a, b, c, d))
    ]
    centralizer = [b for b in gl2 if matmul(b, J) == matmul(J, b)]
    expected = {
        (a, b, 0, a)
        for a in range(1, P)
        for b in range(P)
    }
    assert set(centralizer) == expected
    assert len(centralizer) == P * (P - 1)

    # For J, (J-I)V is the x-axis, so the quotient coordinate is y.
    induced_scalars = set()
    for b in centralizer:
        image = act(b, (0, 1))
        induced_scalars.add(image[1])
        assert image[1] == b[0]
    assert induced_scalars == set(range(1, P))

    rows = [(x, y) for x in range(P) for y in range(P)]
    orbit_labels = {canonical_projective(row) for row in rows}
    assert len(orbit_labels) == P + 2  # zero plus |P^1(F_p)| = p+1

    r29 = (1, 5)
    r113 = (1, 4)
    row_det = (r29[0] * r113[1] - r29[1] * r113[0]) % P
    assert row_det == 6
    assert canonical_projective(r29) != canonical_projective(r113)

    print("Cycle 184 semidirect Kummer conjugacy checks")
    print("p =", P)
    print("centralizer size =", len(centralizer))
    print("quotient-row orbits =", len(orbit_labels))
    print("rows =", r29, r113)
    print("row determinant =", row_det)
    print("Kummer Frobenius classes are distinct")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
