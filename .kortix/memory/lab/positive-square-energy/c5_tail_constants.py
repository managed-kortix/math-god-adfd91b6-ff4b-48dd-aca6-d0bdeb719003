#!/usr/bin/env python3
"""Exact rational constants for the q>=727 endpoint/Euler tail bound."""

import sympy as s

def main():
    # Margin from outlier r>5/3 and positive limiting phase integral.
    margin=2+s.Rational(1156,225)-(s.sqrt(5)+s.Rational(9,2))
    assert margin>s.Rational(2,5)  # equivalent to sqrt(5)<1007/450
    assert s.Rational(1007,450)**2>5
    # q/2-10 >=707/2 and pi<22/7.
    L=s.Rational(4)*s.Rational(22,7)/s.Rational(707,2)
    endpoint=L/4+s.Rational(15,32)*L
    interior=s.Rational(11,1000)
    total=endpoint+interior
    assert total<s.Rational(1,25)
    print(f"PASS exact tail margin>{s.Rational(2,5)} and quadrature error={total}<1/25")

if __name__=="__main__": main()
