#!/usr/bin/env python3
"""Exact polynomial certificate that the limiting C5 phase integral is positive."""

import sympy as s

c,t=s.symbols("c t")
N=-4*(c-1)*(32*c**5-24*c**3+2*c+5)
D=256*c**8-256*c**7-576*c**6+576*c**5+384*c**4-400*c**3-60*c**2+92*c-17
COEFF=[s.Rational(v,1000) for v in
       [-1176,932897,-18738928,160421290,-784298040,2400555593,
        -4738265457,6012185972,-4728030260,2094110383,-398872274]]
P=sum(v*c**k for k,v in enumerate(COEFF))

def main():
    # D<0.  E=PD-N<0 implies P>N/D=delta'. Endpoint c=1 is equality.
    E=s.Poly(s.expand(P*D-N),c)
    assert E.count_roots(0,1)==1 and E.eval(0)<0 and E.eval(s.Rational(999,1000))<0
    J=s.simplify(sum(4*v*s.integrate(s.cos(t)**(k+2),(t,0,s.pi/2))
                     for k,v in enumerate(COEFF)))
    # J upper-bounds integral 4 cos^2(theta) delta'(theta). Prove J<-2pi
    # with the classical upper bound pi<355/113.
    residual=s.simplify(J+2*s.pi)
    upper=residual.subs(s.pi,s.Rational(355,113))
    assert upper<0
    print("PASS polynomial majorant delta'<=P and phase integral I=-2-J/pi>0")
    print(f"J+2pi={residual}")
    print(f"upper_using_pi_355/113={upper}")

if __name__=="__main__": main()
