#!/usr/bin/env python3
"""Dependency-free mod 7^8 height certificate for 433a1."""

from fractions import Fraction
from math import isqrt

P7, N, MOD = 7, 8, 7**8
E2 = 4471315
P = (Fraction(0), Fraction(1))
Q = (Fraction(-1), Fraction(1))


def add(a, b):
    if a is None: return b
    if b is None: return a
    x1, y1 = a; x2, y2 = b
    if x1 == x2 and y2 == -y1-x1: return None
    if a != b:
        lam = (y2-y1)/(x2-x1); nu = (y1*x2-y2*x1)/(x2-x1)
    else:
        lam = (3*x1*x1-y1)/(2*y1+x1); nu = (-x1**3+2)/(2*y1+x1)
    x3 = lam*lam+lam-x1-x2; y3 = -(lam+1)*x3-nu
    assert y3*y3+x3*y3 == x3**3+1
    return x3, y3


def mul(n, point):
    out = None
    while n:
        if n & 1: out = add(out, point)
        point = add(point, point); n //= 2
    return out


def coords(point):
    x, y = point; d = isqrt(x.denominator)
    assert d*d == x.denominator and y.denominator == d**3
    return x.numerator, y.numerator, d


def val(n):
    if not n: return 10**9
    n=abs(n); v=0
    while n%7==0: n//=7; v+=1
    return v


def integral_mod(q, modulus):
    q=Fraction(q); a,b=q.numerator,q.denominator; vb=val(b); va=val(a)
    assert va>=vb; a//=7**vb; b//=7**vb
    return a*pow(b,-1,modulus)%modulus


def term_mod(c,t,e):
    q=Fraction(c)*t**e; va,vb=val(q.numerator),val(q.denominator); v=va-vb
    assert v>=0
    if v>=N: return 0
    m=7**(N-v); u=(q.numerator//7**va)*pow(q.denominator//7**vb,-1,m)%m
    return 7**v*u%MOD


def sigmas(e):
    e=Fraction(e)
    return [Fraction(1),Fraction(1,2),Fraction(1,3)+e/24,
      Fraction(1,4)+e/16,
      Fraction(115,576)+7*e/96+e**2/1152,
      Fraction(191,1152)+5*e/64+5*e**2/2304,
      Fraction(5959,10368)+Fraction(5567,69120)*e+Fraction(25,6912)*e**2+e**3/82944,
      Fraction(2125,1296)+Fraction(11249,138240)*e+Fraction(35,6912)*e**2+Fraction(7,165888)*e**3,
      Fraction(48464785,13934592)+Fraction(2352157,17418240)*e+Fraction(21379,3317760)*e**2+Fraction(91,995328)*e**3+e**4/7962624]


SIGMA=sigmas(E2)


def log7(u):
    guard=7**12; x=(pow(u,6,guard)-1)%guard; assert x%7==0
    s=sum((1 if k%2 else -1)*Fraction(x**k,k) for k in range(1,17))/6
    return integral_mod(s,MOD)


def height(point):
    a,b,d=coords(mul(11,point)); t=(-d*a*pow(b,-1,MOD))%MOD
    sigma_over_t=sum(term_mod(c,t,e) for e,c in enumerate(SIGMA))%MOD
    u=(-a*pow(b,-1,MOD)*sigma_over_t)%MOD
    logarithm=log7(u); h=(-2*pow(121,-1,MOD)*logarithm)%MOD
    return h,t,u,logarithm,(a,b,d)


def main():
    hp=height(P); hq=height(Q); hs=height(add(P,Q))
    assert hp[:4] == (2952047,2984226,21604,2992388)
    assert hq[:4] == (4713289,3990287,1891275,203665)
    assert hs[:4] == (4915575,62475,4404863,5259765)
    cross=((hs[0]-hp[0]-hq[0])*pow(2,-1,MOD))%MOD
    assert cross==1507520
    regulator=(hp[0]*hq[0]-cross*cross)%MOD
    assert regulator==2495619 and regulator%343==294
    print("Cycle 145 high-precision height certificate")
    print("height matrix mod 7^8 =",((hp[0],cross),(cross,hq[0])))
    print("regulator mod 7^8 =",regulator)
    print("regulator / 7^2 mod 7^6 =",regulator//49)
    print("all exact checks passed")


if __name__ == "__main__": main()
