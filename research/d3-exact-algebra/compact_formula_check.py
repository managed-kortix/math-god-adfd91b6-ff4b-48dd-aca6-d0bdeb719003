#!/usr/bin/env python3
"""Derive/check compact exact one-sum formulas for every D+T^3 incidence."""
from collections import defaultdict
import importlib.util
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'))
sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)

# Poly in activity-variable names plus formal h (i); exponents arbitrary.
def clean(p): return {m:c for m,c in p.items() if c}
def add(*ps):
 o=defaultdict(int)
 for p in ps:
  for m,c in p.items():o[m]+=c
 return clean(o)
def scale(p,c): return clean({m:c*v for m,v in p.items()})
def mul(*ps):
 o={():1}
 for p in ps:
  n=defaultdict(int)
  for a,x in o.items():
   for b,y in p.items():n[tuple(sorted(a+b))]+=x*y
  o=clean(n)
 return o
def var(x):return {(x,):1}
def con(c):return {():c} if c else {}
def cp(r,i):return add(r,{tuple(sorted(m+('h',))):c for m,c in i.items()})
def split(p):
 r=defaultdict(int);i=defaultdict(int)
 for m,c in p.items():
  h=m.count('h');assert h in (0,1);q=list(m);q.remove('h') if h else None;(i if h else r)[tuple(q)]+=c
 return clean(r),clean(i)
def cmul(a,b):
 ar,ai=split(a);br,bi=split(b)
 return cp(add(mul(ar,br),scale(mul(ai,bi),-1)),add(mul(ar,bi),mul(ai,br)))
def q(a,b):return cp(add(mul(var(a),var(b)),con(1)),con(-2)) # d +? Actually triangle response is d host+(e-2i)deleted

def zpoly(vertices,edges,deleted=()):
 # matching polynomial, variables names exactly vertices
 V=tuple(sorted(set(vertices)-set(deleted)));E={tuple(sorted(e)) for e in edges if not(set(e)&set(deleted))}
 from functools import lru_cache
 adj={v:set() for v in V}
 for a,b in E:adj[a].add(b);adj[b].add(a)
 @lru_cache(None)
 def f(A):
  if not A:return con(1)
  v=A[0];rest=A[1:];o=mul(var(v),f(rest))
  for w in adj[v]&set(rest):o=add(o,f(tuple(x for x in rest if x!=w)))
  return o
 return f(V)
def psi(vertices,edges):
 R,I,_=d3.full_sachs_polynomial(tuple(sorted(vertices)),frozenset(tuple(sorted(e)) for e in edges))
 V=tuple(sorted(vertices));
 def cv(X):
  o={}
  for mask,c in X.items():o[tuple(V[j] for j in range(len(V)) if mask>>j&1)]=c
  return o
 return cp(cv(R),cv(I))

def delete_poly(vertices,edges,deleted):
 W=set(vertices)-set(deleted);F={e for e in edges if not(set(e)&set(deleted))};return psi(W,F)
def tri_data(label):
 a,b=label+'a',label+'b'; d=add(mul(var(a),var(b)),con(1)); q=cp(add(var(a),var(b)),con(-2));return d,q

def direct_formula(roots):
 Dv={'A','B','x','z'};De={('A','B'),('A','x'),('B','x'),('A','z'),('B','z')};D=psi(Dv,De)
 ds=[];qs=[]
 for j in range(1,4):d,qv=tri_data('T'+str(j));ds.append(d);qs.append(qv)
 out={}
 for mask in range(8):
  coeff=cp(con(1),{})
  deleted=set();valid=True
  for j in range(3):
   if mask>>j&1:
    # At one cut vertex, at most one incident triangle can occupy the root.
    if roots[j] in deleted: valid=False; break
    coeff=cmul(coeff,qs[j]);deleted.add(roots[j])
   else:coeff=cmul(coeff,cp(ds[j],{}))
  if valid:out=add(out,cmul(coeff,delete_poly(Dv,De,deleted)))
 return out

# General recursive triangle-tree response pair (F,Fminus-entry) via one-sum.
def attach(host,host_del,root,label):
 d,qv=tri_data(label)
 return add(cmul(cp(d,{}),host),cmul(qv,host_del))

def formulas(rec):
 Dv={'A','B','x','z'};De={('A','B'),('A','x'),('B','x'),('A','z'),('B','z')};D=psi(Dv,De)
 kind=rec[0]
 if kind=='direct3':return direct_formula(rec[1])
 if kind=='chain2+direct':
  u,v=rec[1:];d1,q1=tri_data('T1');d2,q2=tri_data('T2');d3,q3=tri_data('T3')
  Du=delete_poly(Dv,De,{u});Dvdel=delete_poly(Dv,De,{v});Duv=delete_poly(Dv,De,{u,v})
  # chain branch T1 with T2 at private T1a:
  # F12 = d2(d1 D+q1 Du)+q2(T1b D+Du)
  # deleting v from F12: same expression with D,D_u replaced D_v,D_{u,v}
  b=var('T1b')
  F12=add(cmul(cp(mul(d1,d2),{}),D),cmul(cp(d2,{}),cmul(q1,Du)),cmul(q2,add(cmul(cp(b,{}),D),Du)))
  if u == v:
   # The direct triangle and chain share the host root.  Deleting it separates the
   # private two-triangle chain from D-u; the deleted state is their product.
   a1,b1='T1a','T1b';a2,b2='T2a','T2b'
   branchV={a1,b1,a2,b2};branchE={(a1,b1),(a1,a2),(a1,b2),(a2,b2)}
   F12v = cmul(Dvdel, psi(branchV,branchE))
  else:
   F12v=add(cmul(cp(mul(d1,d2),{}),Dvdel),cmul(cp(d2,{}),cmul(q1,Duv)),cmul(q2,add(cmul(cp(b,{}),Dvdel),Duv)))
  return add(cmul(cp(d3,{}),F12),cmul(q3,F12v))
 if kind=='fork':
  root=rec[1];occ=rec[2];d1,q1=tri_data('T1');d2,q2=tri_data('T2');d3,q3=tri_data('T3');Du=delete_poly(Dv,De,{root})
  # First combine child triangles on the host T1, then attach resulting branch to D.
  # Easier explicit recursive over full graph states: X=D+T1, then attach T2 at a and T3 at a/b.
  X=attach(D,Du,root,'T1')
  # X-a = b D + Du ; X-b = a D + Du; X-{a,b}=D
  a,b=var('T1a'),var('T1b')
  Xa=add(cmul(cp(b,{}),D),Du);Xb=add(cmul(cp(a,{}),D),Du)
  if occ=='same':
   # attach both at a; subset formula: when >=1 child active, delete a only.
   return add(cmul(cp(mul(d2,d3),{}),X),
     cmul(add(cmul(q2,cp(d3,{})),cmul(cp(d2,{}),q3)),Xa))
  # split at a,b; cross deletes both
  return add(cmul(cp(mul(d2,d3),{}),X),cmul(cp(d3,{}),cmul(q2,Xa)),cmul(cp(d2,{}),cmul(q3,Xb)),cmul(q2,cmul(q3,D)))
 if kind=='chain3':
  u=rec[1];d1,q1=tri_data('T1');d2,q2=tri_data('T2');d3,q3=tri_data('T3');Du=delete_poly(Dv,De,{u});a1,b1=var('T1a'),var('T1b');a2,b2=var('T2a'),var('T2b')
  X1=attach(D,Du,u,'T1'); X1a=add(cmul(cp(b1,{}),D),Du)
  X2=attach(X1,X1a,'T1a','T2')
  # Delete T2a: pendant T2b on T1a, so b2*X1 + X1a
  X2a=add(cmul(cp(b2,{}),X1),X1a)
  return attach(X2,X2a,'T2a','T3')
 raise ValueError(rec)

for rec in sorted(d3.records(),key=repr):
 V,E=d3.graph_for(rec);exact=psi(set(V),set(E));f=formulas(rec)
 if f!=exact:
  print('FAIL',rec,'extra',len(set(f.items())-set(exact.items())),'missing',len(set(exact.items())-set(f.items())))
  # print differences
  dif=add(f,scale(exact,-1));print(sorted(dif.items())[:10]);raise SystemExit(1)
 print('PASS',repr(rec),'complex_terms',len(exact))
