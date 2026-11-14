#!/usr/bin/env python3
"""Leaf-deletion phase cross products for every synthetic abstract record."""
import importlib.util
from collections import defaultdict
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'));sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)

def leafs(rec):
 k=rec[0]
 if k=='direct3':return [('T1',rec[1][0]),('T2',rec[1][1]),('T3',rec[1][2])]
 if k=='chain2+direct':return [('T2','T1a'),('T3',rec[2])]
 if k=='fork':return [('T2','T1a'),('T3','T1a' if rec[2]=='same' else 'T1b')]
 if k=='chain3':return [('T3','T2a')]
def subgraph(V,E,deleted):
 W=tuple(v for v in V if v not in deleted);F=frozenset(e for e in E if not(set(e)&set(deleted)));return W,F
def embed(X,smallV,bigV):
 ix={v:i for i,v in enumerate(bigV)};o={}
 for m,c in X.items():o[tuple(1 if (v in smallV and m>>smallV.index(v)&1) else 0 for v in bigV)]=c
 return o
def gen(X,V):return {tuple(1 if m>>i&1 else 0 for i in range(len(V))):c for m,c in X.items()}
def mul(a,b):
 o=defaultdict(int)
 for x,c in a.items():
  for y,d in b.items():o[tuple(i+j for i,j in zip(x,y))]+=c*d
 return {k:v for k,v in o.items() if v}
def add(a,b,scale=1):
 o=defaultdict(int);o.update(a)
 for k,v in b.items():o[k]+=scale*v
 return {k:v for k,v in o.items() if v}
def activity(X):
 # z_i=t+y_i with arbitrary exponents (cross products can have exponent two).
 o=defaultdict(int)
 import math,itertools
 for ex,c in X.items():
  for ys in itertools.product(*(range(e+1) for e in ex)):
   coef=c
   for e,y in zip(ex,ys):coef*=math.comb(e,y)
   o[(ys,sum(ex)-sum(ys))]+=coef
 return {k:v for k,v in o.items() if v}
def signs(x):return sum(v>0 for v in x.values()),sum(v<0 for v in x.values())
for rec in sorted(d3.records(),key=repr):
 V,E=d3.graph_for(rec);Rg,Ig,_=d3.full_sachs_polynomial(V,E);Rg,Ig=gen(Rg,V),gen(Ig,V)
 for lab,root in leafs(rec):
  priv={lab+'a',lab+'b'};XV,XE=subgraph(V,E,priv);YV,YE=subgraph(XV,XE,{root})
  Rx,Ix,_=d3.full_sachs_polynomial(XV,XE);Ry,Iy,_=d3.full_sachs_polynomial(YV,YE)
  Rx,Ix=embed(Rx,XV,V),embed(Ix,XV,V);Ry,Iy=embed(Ry,YV,V),embed(Iy,YV,V)
  # host=G-private leaf; deleted=host-root.
  Ch=add(mul(Ix,Ry),mul(Rx,Iy),-1)     # Im(host * conjugate(deleted))
  Cg=add(mul(Ig,Ry),mul(Rg,Iy),-1)     # Im(full * conjugate(deleted))
  Cha,Cga=activity(Ch),activity(Cg)
  print(repr(rec),lab,'root',root,
        'host_cross',signs(Ch),signs(Cha),'host_terms',len(Cha),
        'full_cross',signs(Cg),signs(Cga),'full_terms',len(Cga))
