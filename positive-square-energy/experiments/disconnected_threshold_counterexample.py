#!/usr/bin/env python3
"""Exact certificate for a disconnected edge-threshold counterexample.

X = D disjoint-union 117 C5 disjoint-union C13, where D is ``HQzV]zn``.
Adding the nonedge {2,3} crosses s+(X)=|X|.  All spectral root bounds use
SymPy's exact rational root isolation; algebraic cycle terms are bounded by
exact rational interval arithmetic through minimal polynomials.
"""

from __future__ import annotations

import networkx as nx
import sympy as sp


def energy_bounds(a: sp.Matrix, eps: sp.Rational) -> tuple[sp.Expr, sp.Rational, sp.Rational]:
    x = sp.symbols("x")
    p = sp.Poly(a.charpoly(x).as_expr(), x)
    lo = sp.Rational(0)
    hi = sp.Rational(0)
    for (l, r), mult in p.intervals(eps=eps):
        if r <= 0:
            continue
        if l <= 0:
            raise AssertionError("positive root interval meets zero")
        lo += mult * l**2
        hi += mult * r**2
    return sp.factor(p.as_expr()), lo, hi


def main() -> None:
    d = nx.from_graph6_bytes(b"HQzV]zn")
    assert len(d) == 9 and not d.has_edge(2, 3)
    a = sp.Matrix(nx.to_numpy_array(d, nodelist=range(9), dtype=int))
    b = a.copy()
    b[2, 3] = b[3, 2] = 1
    eps = sp.Rational(1, 10**35)
    pa, alo, ahi = energy_bounds(a, eps)
    pb, blo, bhi = energy_bounds(b, eps)

    # C5 surplus is 2-sqrt(5).  For C13 (13 == 1 mod 4), surplus is
    # 1-sec(pi/13).  Isolate y=sec(pi/13) as the unique root near 1.03 of
    # its exact resultant polynomial, derived from 2*cos(pi/13).
    y = sp.symbols("y")
    z = sp.symbols("z")
    # Phi_26(z), with z=exp(i*pi/13); eliminate z from y(z+z^-1)=2.
    phi26 = sp.cyclotomic_poly(26, z)
    sec_poly = sp.Poly(sp.resultant(phi26, y * (z**2 + 1) - 2 * z, z), y).sqf_part()
    sec_candidates = [iv for iv, _ in sec_poly.intervals(eps=eps)
                      if iv[0] > 1 and iv[1] < sp.Rational(11, 10)]
    assert len(sec_candidates) == 1
    seclo, sechi = sec_candidates[0]
    # The paper identifies this root with sec(pi/13), using cos(x)>1-x^2/2
    # and pi<22/7 to place sec(pi/13) in (1,11/10).
    sqrt5lo = sp.Rational(22360679774997896964091736687312762, 10**34)
    sqrt5hi = sp.Rational(22360679774997896964091736687312763, 10**34)
    assert sqrt5lo**2 < 5 < sqrt5hi**2

    # Total slack = s+(D)-9 +117(2-sqrt5)+(1-sec(pi/13)).
    before_lo = alo - 9 + 117 * (2 - sqrt5hi) + (1 - sechi)
    before_hi = ahi - 9 + 117 * (2 - sqrt5lo) + (1 - seclo)
    after_lo = blo - 9 + 117 * (2 - sqrt5hi) + (1 - sechi)
    after_hi = bhi - 9 + 117 * (2 - sqrt5lo) + (1 - seclo)
    assert before_lo > 0
    assert after_hi < 0

    print("chi_D =", pa)
    print("chi_D+e =", pb)
    print("sec polynomial =", sec_poly.as_expr())
    print("before slack interval =", (before_lo, before_hi))
    print("after slack interval =", (after_lo, after_hi))
    print("decimals before =", (sp.N(before_lo, 18), sp.N(before_hi, 18)))
    print("decimals after =", (sp.N(after_lo, 18), sp.N(after_hi, 18)))
    print("EXACT CERTIFICATE PASSED")


if __name__ == "__main__":
    main()
