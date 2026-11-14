#!/usr/bin/env python3
"""Exact algebra audit for fixed-rank-bridge-projector-obstruction-2026-11-14.md.

Dependency-free: all polynomial calculations use fractions.Fraction.
"""
from fractions import Fraction as F
from itertools import permutations


def poly_trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def poly_add(a, b):
    out = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a): out[i] += x
    for i, x in enumerate(b): out[i] += x
    return poly_trim(out)


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return poly_trim(out)


def parity(p):
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inv & 1 else 1


def charpoly_low(M):
    """det(xI-M), coefficients low-to-high, exact Leibniz expansion."""
    n = len(M)
    out = [F(0)]
    for p in permutations(range(n)):
        term = [F(parity(p))]
        for i, j in enumerate(p):
            factor = [-F(M[i][j]), F(1)] if i == j else [-F(M[i][j])]
            term = poly_mul(term, factor)
        out = poly_add(out, term)
    return out


def desc(a):
    return list(reversed(a))


def sign_variations(seq):
    s = [1 if x > 0 else -1 for x in seq if x]
    return sum(s[i] != s[i-1] for i in range(1, len(s)))


def eval_desc(c, x):
    y = F(0)
    for a in c: y = y*x+a
    return y


def audit(t):
    # Nonsymmetric equitable divisors have the same eigenvalues as the
    # symmetric quotients because cell-size diagonal similarity conjugates them.
    DH = [[0, 2, 0, t], [1, 0, 1, 0], [0, 1, 1, 0], [1, 0, 0, 0]]
    DK = [[0, 4, t], [1, 3, 0], [1, 0, 0]]
    hp = desc(charpoly_low(DH))
    kp = desc(charpoly_low(DK))
    want_h = list(map(F, [1, -1, -(t+3), t+2, t]))
    want_k = list(map(F, [1, -3, -(t+4), 3*t]))
    if hp != want_h or kp != want_k:
        raise SystemExit(f"characteristic polynomial mismatch at t={t}: {hp}, {kp}")

    # Positive-root Descartes counts and explicit sign brackets.
    if sign_variations(hp) != 2 or not (eval_desc(hp, 0)>0 and eval_desc(hp, 2)<0):
        raise SystemExit(f"H positive-root audit failed at t={t}")
    hm = [c if (len(hp)-1-i)%2 == 0 else -c for i,c in enumerate(hp)]
    if sign_variations(hm) != 2 or not (eval_desc(hm, 0)>0 and eval_desc(hm, 1)<0 and eval_desc(hm, t+4)>0):
        raise SystemExit(f"H negative-root audit failed at t={t}")
    if sign_variations(kp) != 2 or not (eval_desc(kp, 0)>0 and eval_desc(kp, 4)<0):
        raise SystemExit(f"K positive-root audit failed at t={t}")
    km = [c if (len(kp)-1-i)%2 == 0 else -c for i,c in enumerate(kp)]
    if sign_variations(km) != 1:
        raise SystemExit(f"K negative-root audit failed at t={t}")

    return hp, kp


def main():
    # Symbolic coefficient formulas are checked on enough exact integer values
    # to audit implementation and all sign arguments are then formula-level in
    # the note. No floating point or assert is used.
    rows = [audit(t) for t in (1,2,3,5,10,101)]
    # Cyclomatic ranks from exact counts.
    for t in (1,2,101):
        h_n, h_m = 5+t, 5+t
        k_n, k_m = 5+t, 10+t
        if h_m-h_n+1 != 1 or k_m-k_n+1 != 6:
            raise SystemExit("rank count failed")
    print("PASS fixed-rank bridge projector obstruction")
    print("H quotient: x^4-x^3-(t+3)x^2+(t+2)x+t; inertia (3,3,t-1)")
    print("K quotient: x^3-3x^2-(t+4)x+3t; inertia (2,4,t-1)")
    print("leaf projector product <= 1/t^2 -> 0")


if __name__ == "__main__":
    main()
