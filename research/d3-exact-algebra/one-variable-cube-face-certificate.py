#!/usr/bin/env python3
"""Exact low-dimensional search for five synthetic abstract defect records.

For every choice of one free nondefect activity x and every assignment of the
other eight nondefect activities to {0,1}, prove H(x)<0 and B(x)<=0 throughout x>=0,Q(x)>0,
where H=AQ-BP is the I=0 boundary numerator. Since P<=0 on the closed orthant (strict in the positive interior), this proves the
full ray implication I=P+yQ>=0 => R=A+yB<0.  This is a finite exact rational
certificate (5*9*2^8 = 11520 rays), not a certificate on the full orthant.
"""
import importlib.util
from collections import defaultdict
from fractions import Fraction
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'))
sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)

def split(X,b):
 a,q={},{}
 for m,c in X.items():(q if m&b else a)[m^b if m&b else m]=c
 return a,q

def restrict(X,zero,var):
 o=defaultdict(int)
 for m,c in X.items():
  if m&zero:continue
  o[1 if m&(1<<var) else 0]+=c
 return dict(o)

def mul(a,b):
 o=defaultdict(int)
 for i,c in a.items():
  for j,e in b.items():o[i+j]+=c*e
 return dict(o)

def sub(a,b):
 o=defaultdict(int);o.update(a)
 for i,c in b.items():o[i]-=c
 return dict(o)

def val(c,x):return sum(Fraction(a)*x**i for i,a in c.items())

def certify_nonpositive_affine(q,b):
 # Certify B(x)<=0 on x>=0,Q(x)>0. Both are affine.
 q0,q1=q.get(0,0),q.get(1,0);b0,b1=b.get(0,0),b.get(1,0)
 if q1==0:
  if q0<=0:return True
  return b0<=0 and b1<=0
 if q1<0:
  if q0<=0:return True
  U=Fraction(q0,-q1)
  return b0<=0 and Fraction(b0)+Fraction(b1)*U<=0
 L=max(Fraction(0),Fraction(-q0,q1))
 return Fraction(b0)+Fraction(b1)*L<=0 and b1<=0

def certify_ray(q,h):
 # q is affine and h is quadratic (possibly lower degree), integer coefficients.
 q0,q1=q.get(0,0),q.get(1,0)
 h0,h1,h2=h.get(0,0),h.get(1,0),h.get(2,0)
 # The legal set {x>=0:q(x)>0} is either empty, [0,U), (L,infty), or all [0,infty).
 if q1==0:
  if q0<=0:return True
  L,U=Fraction(0),None
 elif q1<0:
  if q0<=0:return True
  L,U=Fraction(0),Fraction(q0,-q1)
 else:
  L,U=max(Fraction(0),Fraction(-q0,q1)),None
 # A convex quadratic cannot be bounded above by a negative number on an
 # unbounded interval unless it is decreasing affine/concave there.  In all
 # cases it suffices to inspect finite endpoints and an interior vertex when
 # h2<0.  The upper q-bound is open; nonpositivity there plus strict negativity
 # at all legal extrema suffices, with the identically-zero case excluded.
 cand=[L]
 if U is not None:cand.append(U)
 if h2<0:
  xv=Fraction(-h1,2*h2)
  if xv>=L and (U is None or xv<=U):cand.append(xv)
 if U is None:
  if h2>0 or (h2==0 and h1>0):return False
 # Strict at every attained candidate; at open U allow equality only if the
 # polynomial is not zero immediately to its left (the other checks ensure it).
 for x in cand:
  hx=val(h,x)
  if U is not None and x==U:
   if hx>0:return False
   # If H vanishes at the excluded endpoint, it must be negative immediately
   # to the left. For a quadratic this is equivalent to H'(U)>=0, unless a
   # double root (which would give nonnegative values nearby).
   if hx==0:
    deriv=h1+2*h2*x
    if deriv<=0:return False
  elif hx>=0:return False
 return True

total=0
for rec in sorted(d3.bare_defect_formulas(),key=repr):
 V,E=d3.graph_for(rec);R,I,_=d3.full_sachs_polynomial(V,E)
 Ia=d3.activity_expansion(I);j=[k for k,v in Ia.items() if v>0][0][0].bit_length()-1
 A,B=split(R,1<<j);P0,Q=split(I,1<<j);inds=[i for i in range(len(V)) if i!=j]
 count=0
 for var in inds:
  oth=[i for i in inds if i!=var];alloth=sum(1<<i for i in oth)
  for bits in range(1<<len(oth)):
   one=sum(1<<i for k,i in enumerate(oth) if bits>>k&1);zero=alloth^one
   aa,bb,pp,qq=(restrict(X,zero,var) for X in (A,B,P0,Q))
   h=sub(mul(aa,qq),mul(bb,pp))
   assert certify_ray(qq,h),(rec,V[var],bits,qq,h)
   assert certify_nonpositive_affine(qq,bb),(rec,V[var],bits,qq,bb)
   count+=1
 assert count==9*2**8
 total+=count
 print('PASS',repr(rec),'rays',count)
assert total==5*9*2**8
print('TOTAL exact certified rays',total)
