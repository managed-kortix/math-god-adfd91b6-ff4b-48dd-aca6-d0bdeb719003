#!/usr/bin/env python3
"""Exact regression certificate for S_q power sums through degree 16."""

from __future__ import annotations

import sympy as s

x = s.symbols("x")

FORMS = [0, 2, lambda q:q+11, 8, lambda q:3*q+49, 37,
         lambda q:10*q+236, 177, lambda q:35*q+1169, 872,
         lambda q:126*q+5861, 4413, lambda q:462*q+29548, 22817,
         lambda q:1716*q+149349, 119788, lambda q:6435*q+755809]

def symmetric_poly(q: int) -> s.Poly:
    p5=s.Poly(2*(s.chebyshevt(5,x/2)-1),x)
    m5=s.Poly(s.chebyshevu(4,x/2),x)
    p=s.Poly(2*(s.chebyshevt(q,x/2)-1),x)
    m=s.Poly(s.chebyshevu(q-1,x/2),x)
    persistent=s.Poly(x*x+x-1,x)
    bridge=s.div(p5*p-m5*m,persistent)[0]
    k=(q-1)//2
    retained=s.Poly(s.chebyshevu(k,x/2)+s.chebyshevu(k-1,x/2),x)
    quotient,remainder=s.div(bridge,retained)
    assert remainder.is_zero
    return quotient

def closed_form(q: int) -> s.Poly:
    d=(q+7)//2
    pattern=[(0,1),(1,-2),(2,-1),(3,4),(4,-3),(5,1),(7,1),(8,-2),(9,1)]
    return s.Poly(sum(c*s.chebyshevu(d-offset,x/2)
                      for offset,c in pattern if d>=offset),x)

def power_sums(poly: s.Poly, degree: int) -> list[s.Expr]:
    coeff=poly.all_coeffs(); out=[]
    for j in range(1,degree+1):
        value=sum(coeff[i]*out[j-i-1] for i in range(1,min(j,len(coeff))))
        if j<len(coeff): value += j*coeff[j]
        out.append(s.expand(-value))
    return out

def main() -> None:
    # Degree >=16 starts at q=25; checks multiple residue classes and larger q.
    for q in range(25,66,2):
        exact=symmetric_poly(q)
        assert exact==closed_form(q)
        got=power_sums(exact,16)
        expected=[FORMS[j](q) if callable(FORMS[j]) else FORMS[j]
                  for j in range(1,17)]
        assert got==expected
    print("PASS exact S_q moment formulas through degree 16 for odd q=25..65")
    print("A symbolic recurrence proof for all odd q remains before theorem use.")

if __name__=="__main__": main()
