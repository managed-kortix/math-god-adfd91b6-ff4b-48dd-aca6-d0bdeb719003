#!/usr/bin/env python3
"""Exact rational interval certificate H<0 whenever Q>0 on the equal-activity defect line."""
import importlib.util
from fractions import Fraction
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'));sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)
# Chosen common rational separator: every Q root is < 1/3; every H root is > 2/5.
# Descartes: Q(u) has exactly one positive root (+--- coefficients), H(u) exactly one
# positive root (positive leading block then negative tail, read descending).
def peval(coeff,u):return sum(Fraction(c)*u**k for k,c in enumerate(coeff))
def conv(a,b):
 o=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):o[i+j]+=x*y
 return o
def sub(a,b):
 n=max(len(a),len(b));return [(a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0) for i in range(n)]
def even(c):
 assert all(x==0 for i,x in enumerate(c) if i%2);return [c[2*i] for i in range((len(c)+1)//2)]
def odd_over_t(c):
 assert all(x==0 for i,x in enumerate(c) if i%2==0);return [c[2*i+1] for i in range(len(c)//2)]
for rec,(v,(A,B),(Pp,Q)) in sorted(d3.bare_defect_formulas().items(),key=lambda z:repr(z[0])):
 Au,Bu,Pu,Qu=even(A),odd_over_t(B),odd_over_t(Pp),even(Q)
 Hu=sub(conv(Au,Qu),[0]+conv(Bu,Pu)) # B=t Bu, P=t Pu -> BP=u Bu Pu
 # Strip high zero; coefficients low first.
 while Hu and Hu[-1]==0:Hu.pop()
 # exact Descartes sign variations
 def var(c):
  s=[1 if x>0 else -1 for x in reversed(c) if x];return sum(a!=b for a,b in zip(s,s[1:]))
 assert var(Qu)==1 and var(Hu)==1
 # P<0; B is increasing in u and remains negative through u=1/3.
 assert all(c <= 0 for c in Pu) and any(c < 0 for c in Pu)
 assert Bu[0] < 0 and all(c >= 0 for c in Bu[1:]) and peval(Bu,Fraction(1,3)) < 0
 assert peval(Qu,Fraction(0))>0 and peval(Qu,Fraction(1,3))<0
 assert peval(Hu,Fraction(0))<0 and peval(Hu,Fraction(2,5))<0 and peval(Hu,Fraction(4))>0
 # If I=P+yQ>=0, then Q>0 and y>=-P/Q. Unique roots give
 # u<rootQ<1/3<2/5<rootH, hence H<0. Also B<0 there, so
 # R(y)<=R(-P/Q)=H/Q<0.
 print(repr(rec),'defect',v,'B(1/3)=',peval(Bu,Fraction(1,3)),'Q(1/3)=',peval(Qu,Fraction(1,3)),'H(2/5)=',peval(Hu,Fraction(2,5)),'variations',var(Qu),var(Hu))
