#!/usr/bin/env python3
import importlib.util
from collections import defaultdict,Counter
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'));sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)
def split(X,b):
 a={};q={}
 for m,c in X.items():(q if m&b else a)[m^b if m&b else m]=c
 return a,q
def mult(a,b):
 o=defaultdict(int)
 for m,c in a.items():
  for n,d in b.items():o[(m^n,m&n)]+=c*d
 return {k:v for k,v in o.items() if v}
def sub(a,b):
 o=defaultdict(int);o.update(a)
 for k,v in b.items():o[k]-=v
 return {k:v for k,v in o.items() if v}
for rec in sorted(d3.bare_defect_formulas(),key=repr):
 V,E=d3.graph_for(rec);R,I,_=d3.full_sachs_polynomial(V,E);Ia=d3.activity_expansion(I);bit=[k for k,v in Ia.items() if v>0][0][0]
 A,B=split(R,bit);Pp,Q=split(I,bit);H=sub(mult(A,Q),mult(B,Pp));
 def signs(X):return (sum(c>0 for c in X.values()),sum(c<0 for c in X.values()))
 # Degree signatures and overlap counts
 print(rec,'raw A/B/P/Q',len(A),signs(A),len(B),signs(B),len(Pp),signs(Pp),len(Q),signs(Q),'H',len(H),signs(H),'Hconst',H.get((0,0)))
