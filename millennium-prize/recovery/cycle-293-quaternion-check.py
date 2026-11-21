#!/usr/bin/env python3
"""Exact matrix checks; quaternion index theorem is proved in the note."""
from fractions import Fraction

def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Fraction())
             for j in range(len(b[0]))] for i in range(len(a))]
def tr(a): return [list(x) for x in zip(*a)]
def validate(condition, context):
    if not condition:
        raise RuntimeError(f"validation failed: {context!r}")

checks=0
for d in range(1,101):
    J=[[Fraction(),Fraction(-d)],[Fraction(1),Fraction()]]
    R=[[Fraction(1),Fraction()],[Fraction(),Fraction(d)]]
    Ri=[[Fraction(1),Fraction()],[Fraction(),Fraction(1,d)]]
    I=[[Fraction(1),Fraction()],[Fraction(),Fraction(1)]]
    validate(mm(J,J)==[[-d*x for x in row] for row in I], ("square",d))
    checks+=1
    validate(mm(mm(Ri,tr(J)),R)==[[-x for x in row] for row in J], ("Rosati",d))
    checks+=1
# Kronecker repeats for m=2s, as entries lie in the central F.
for s in range(1,17):
  d=7; n=2*s
  B=[[Fraction() for _ in range(n)] for __ in range(n)]
  for k in range(s): B[2*k][2*k+1]=-d; B[2*k+1][2*k]=1
  validate(mm(B,B)==[[Fraction(-d if i==j else 0) for j in range(n)] for i in range(n)],
           ("central repeat",s))
  checks+=1
print(f'PASS exact central-block checks={checks}')
print('hostile example in note: Hamilton D, K=Q(sqrt(-7)); local invariant proof is analytic, not this regression')
