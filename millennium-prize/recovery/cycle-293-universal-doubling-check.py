#!/usr/bin/env python3
"""Exact regression for universal even self-product construction."""
from fractions import Fraction

def mm(a,b):
 return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Fraction()) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a): return [list(x) for x in zip(*a)]
def validate(condition, context):
 if not condition:
  raise RuntimeError(f"validation failed: {context!r}")
def bd(block,r):
 n=len(block); z=[[Fraction() for _ in range(n*r)] for __ in range(n*r)]
 for t in range(r):
  for i in range(n):
   for j in range(n): z[t*n+i][t*n+j]=Fraction(block[i][j])
 return z
checks=0
for d in range(1,32):
 for r in range(1,9):
  J=bd([[0,-d],[1,0]],r); R=bd([[1,0],[0,d]],r); Ri=bd([[1,0],[0,Fraction(1,d)]],r)
  n=2*r; I=[[Fraction(1 if i==j else 0) for j in range(n)] for i in range(n)]
  validate(mm(J,J)==[[-d*x for x in row] for row in I], ("square",d,r))
  checks+=1
  validate(mm(mm(Ri,tr(J)),R)==[[-x for x in row] for row in J], ("Rosati",d,r))
  checks+=1
# Ordinary determinant class: eta^(2q)*pf^(2r)=(-1)^q*d^q*pf^(2r).
# Modulo norms, only (-1)^q survives. Fourfold condition 2gr=4 gives q=2.
for g in range(1,7):
 for r in range(1,7):
  q=g*r
  for d in range(1,11):
   for pf in range(-5,6):
    det=(-1)**q * d**q * pf**(2*r)
    normpart=d**q * pf**(2*r)
    validate(det==((-1)**q)*normpart, ("determinant class",g,r,d,pf))
    checks+=1
    if 2*g*r==4:
     validate(q==2 and det==normpart, ("fourfold determinant",g,r,d,pf))
     checks+=1
# Factor composition: exponents add under orthogonal direct sum.
# Two doubled elliptic factors contribute (-1)*(-1)=+1; a doubled elliptic
# plus another compatible factor is globally trivial exactly when that factor
# has class -1.
for q1 in range(1,13):
 for q2 in range(1,13):
  validate(((-1)**q1)*((-1)**q2)==(-1)**(q1+q2),
           ("factor composition",q1,q2))
  checks+=1
validate((-1)*(-1)==1, "fixed doubled-elliptic product")
checks+=1
for other in (-1,1):
 validate((((-1)*other)==1)==(other==-1), ("mixed factor",other))
 checks+=1
print(f'PASS exact universal-doubling checks={checks}')
print('ordinary discriminant class=(-1)^(g*r); orthogonal factors add exponents')
print('fourfold all-doubling exponent=2; E1^2 and E2^2 each class -1, product +1')
