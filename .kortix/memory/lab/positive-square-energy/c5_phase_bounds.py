#!/usr/bin/env python3
"""Exact Sturm certificates for coarse C5 phase derivative bounds."""

import sympy as s

c=s.symbols("c")
N=-4*(c-1)*(32*c**5-24*c**3+2*c+5)
D=256*c**8-256*c**7-576*c**6+576*c**5+384*c**4-400*c**3-60*c**2+92*c-17

def constant_sign(expr, sign):
    p=s.Poly(expr,c)
    assert p.count_roots(-1,1)==0
    assert sign*p.eval(0)>0

def main():
    # delta'=N/D. D<0 and -10<delta'<10.
    constant_sign(D,-1)
    constant_sign(N-10*D,1)
    constant_sign(N+10*D,-1)
    # delta''=-sin(theta)(N'D-ND')/D^2; certify its square <60^2.
    residual=s.expand((1-c*c)*(s.diff(N,c)*D-N*s.diff(D,c))**2-3600*D**4)
    constant_sign(residual,-1)
    print("PASS exact phase bounds |delta'|<10 and |delta''|<60 on [0,pi]")

if __name__=="__main__": main()
