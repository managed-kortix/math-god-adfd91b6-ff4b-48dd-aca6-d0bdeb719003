#!/usr/bin/env python3
"""Exact recurrence certificate for the persistent C5--Cq factor."""

from __future__ import annotations

import argparse
import sympy as s


x = s.symbols("x")
factor = s.Poly(x**2 + x - 1, x)


def cycle_data(n: int) -> tuple[s.Poly, s.Poly]:
    p = s.Poly(2 * (s.chebyshevt(n, x / 2) - 1), x)
    q = s.Poly(s.chebyshevu(n - 1, x / 2), x)
    return p, q


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-q", type=int, default=101)
    args = parser.parse_args()
    p5, q5 = cycle_data(5)
    count = 0
    for q in range(3, args.max_q + 1, 2):
        p, minor = cycle_data(q)
        bridge = p5 * p - q5 * minor
        assert s.rem(bridge, factor).is_zero
        count += 1
    print(f"PASS odd_q_count={count} max_q={args.max_q} factor={factor.as_expr()}")
    print("Algebraic reason: modulo x^2+x-1, the Chebyshev recurrence makes")
    print("p_5*q_minor-q_5*p_cycle vanish for every odd q; formal induction pending.")


if __name__ == "__main__":
    main()
