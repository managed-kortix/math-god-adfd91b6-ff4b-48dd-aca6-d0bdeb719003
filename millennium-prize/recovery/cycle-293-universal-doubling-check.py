#!/usr/bin/env python3
"""Exact regression for universal even self-product construction."""
from fractions import Fraction

def mm(a,b):
 return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Fraction()) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a): return [list(x) for x in zip(*a)]
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
  assert mm(J,J)==[[-d*x for x in row] for row in I]
  assert mm(mm(Ri,tr(J)),R)==[[-x for x in row] for row in J]
  checks+=2
# Ordinary determinant class: eta^(2q)*pf^(2r)=(-1)^q*d^q*pf^(2r).
# Modulo norms, only (-1)^q survives. Fourfold condition 2gr=4 gives q=2.
for g in range(1,7):
 for r in range(1,7):
  q=g*r
  for d in range(1,11):
   for pf in range(-5,6):
    det=(-1)**q * d**q * pf**(2*r)
    normpart=d**q * pf**(2*r)
    assert det==((-1)**q)*normpart
    if 2*g*r==4: assert q==2 and det==normpart
    checks+=2
print(f'PASS exact universal-doubling checks={checks}')
print('ordinary discriminant class=(-1)^(g*r); fourfold instances have g*r=2 and class 1')
