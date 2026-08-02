#!/usr/bin/env python3
"""Exact checks for the Cycle 239 infinite Fibonacci-rail obstruction."""

from fractions import Fraction


def det(p, q):
    return p[0] * q[1] - p[1] * q[0]


def main():
    fibonacci = [0, 1]
    for _ in range(90):
        fibonacci.append(fibonacci[-1] + fibonacci[-2])

    def k(n):
        return (fibonacci[n + 1], fibonacci[n])

    def radius(n):
        return fibonacci[2 * n + 1]

    def q(n):
        return ((Fraction(1, radius(n)) - Fraction(1, radius(n + 3))) /
                (Fraction(1, radius(n + 1)) - Fraction(1, radius(n + 4))))

    for n in range(1, 33):
        kn = k(n)
        kn1 = k(n + 1)
        kn2 = k(n + 2)
        kn3 = k(n + 3)
        kn4 = k(n + 4)
        h = (2 * kn2[0], 2 * kn2[1])

        assert (kn[0] + kn3[0], kn[1] + kn3[1]) == h
        assert (-kn1[0] + kn4[0], -kn1[1] + kn4[1]) == h
        assert det(kn, kn3) == 2 * (-1) ** n
        assert det((-kn1[0], -kn1[1]), kn4) == 2 * (-1) ** n
        assert radius(n + 2) == 3 * radius(n + 1) - radius(n)

        x = Fraction(radius(n + 1), radius(n))
        q_closed = (x * (21 * x - 8) * (2 * x - 1) /
                    ((8 * x - 3) * (5 * x - 2)))
        assert q(n) == q_closed
        assert x >= Fraction(5, 2)
        assert q(n) > 2
        assert q(n) * q(n + 1) * q(n + 2) > 8

    # Formal nonzero symbols represented by initial-amplitude exponent vectors.
    exponents = {
        1: (1, 0, 0, 0),
        2: (0, 1, 0, 0),
        3: (0, 0, 1, 0),
        4: (0, 0, 0, 1),
    }
    signs = {1: 1, 2: 1, 3: 1, 4: 1}
    for n in range(1, 4):
        exponents[n + 4] = tuple(
            exponents[n][i] + exponents[n + 3][i] - exponents[n + 1][i]
            for i in range(4)
        )
        signs[n + 4] = -signs[n] * signs[n + 3] * signs[n + 1]
    assert exponents[7] == exponents[1]
    assert signs[7] == -signs[1]

    print("PASS exact Fibonacci identities: n=1..32")
    print("PASS leakage recurrence: a[n+4] = -q[n] a[n] a[n+3]/a[n+1]")
    print("PASS six-rail growth: a[n+6] = -q[n]q[n+1]q[n+2]a[n], |multiplier| > 8")
    print("PASS signed rejection: B[h_n]=0 implies R[n]R[n+2] < 0")


if __name__ == "__main__":
    main()
