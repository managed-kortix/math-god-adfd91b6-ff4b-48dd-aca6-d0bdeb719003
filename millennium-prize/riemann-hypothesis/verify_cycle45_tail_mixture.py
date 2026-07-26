#!/usr/bin/env python3
"""Certified convexity obstruction for the Cycle 45 power-mixture route."""

from flint import arb, ctx

from certify_complete_gram import complete_energies


def main() -> None:
    bits = 256
    ctx.prec = bits
    energies = complete_energies(230, bits)
    y = {n: arb(n).log().log() for n in range(228, 231)}
    A = {n: arb(n).log() * energies[n] for n in range(228, 231)}

    def slope(a: int, b: int):
        return (A[b] - A[a]) / (y[b] - y[a])

    s0 = slope(228, 229)
    s1 = slope(229, 230)
    d2 = (s1 - s0) / (y[230] - y[228])
    assert s0 < 0
    assert s1 < 0
    assert d2 < 0
    print("slope[228,229] =", s0)
    print("slope[229,230] =", s1)
    print("divided_difference[228,229,230] =", d2)
    print("cycle 45 positive-mixture convexity obstruction certified")


if __name__ == "__main__":
    main()
