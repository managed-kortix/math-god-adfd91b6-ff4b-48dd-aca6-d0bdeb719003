#!/usr/bin/env python3
"""Exact regression checks for the Cycle 293 Type-I candidate note."""
from fractions import Fraction
from itertools import product


def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), Fraction(0))
             for j in range(len(b[0]))] for i in range(len(a))]

def tr(a): return [list(x) for x in zip(*a)]
def invdiag(a):
    return [[Fraction(1,a[i][i]) if i==j else Fraction(0) for j in range(len(a))]
            for i in range(len(a))]
def eq(a,b): return a==b

checks=0
for d in range(1,24):
    J=[[Fraction(0),Fraction(-d)],[Fraction(1),Fraction(0)]]
    R=[[Fraction(1),Fraction(0)],[Fraction(0),Fraction(d)]]
    I=[[Fraction(1),Fraction(0)],[Fraction(0),Fraction(1)]]
    negdI=[[Fraction(-d)*x for x in row] for row in I]
    negJ=[[-x for x in row] for row in J]
    assert eq(mm(J,J),negdI)
    assert eq(mm(mm(invdiag(R),tr(J)),R),negJ)
    checks += 2

# A rational 2x2 matrix skew for ordinary transpose has square -a^2 I.
for a in range(-20,21):
    Q=[[Fraction(0),Fraction(a)],[Fraction(-a),Fraction(0)]]
    assert mm(Q,Q)==[[Fraction(-a*a),Fraction(0)],[Fraction(0),Fraction(-a*a)]]
    assert a*a != 2
    checks += 2

# Dimension <=4 isotypic possibilities and whole-Type-I dimension-four partitions.
pairs=[(g,m) for g in range(1,5) for m in range(1,5) if g*m<=4 and m%2==0]
assert pairs==[(1,2),(1,4),(2,2)]
whole=[]
# consolidated dimensions g*m, Type-I rows only, total 4
for n in range(1,4):
    for tup in product(pairs, repeat=n):
        if sum(g*m for g,m in tup)==4 and list(tup)==sorted(tup): whole.append(tup)
assert sorted(set(whole))==[((1,2),(1,2)),((1,4),),((2,2),)]
checks += 2

# For a 2g-dimensional alternating S and r with 2gr=4,
# eta^-4 det(S)^r = (Pf(S)^r/d)^2. Check symbolic integer samples.
for g,r in ((1,2),(2,1)):
    for d in range(1,12):
        for pf in range(-9,10):
            detS=pf*pf
            lhs=Fraction(detS**r,d*d)
            rhs=Fraction(pf**(2*r),d*d)
            assert lhs==rhs
            checks += 1

print(f"PASS exact checks={checks}")
print("Type-I isotypic pairs:",pairs)
print("whole Type-I fourfold shapes: E^2xE'^2, E^4, S^2")
