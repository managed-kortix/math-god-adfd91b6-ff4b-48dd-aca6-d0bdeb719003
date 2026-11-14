#!/usr/bin/env python3
"""Emit exact compact R/I formulas for all 14 D3 incidence records.

Notation: D_S=R_S+i I_S; d_j=a_j b_j+1; e_j=a_j+b_j;
q_j=e_j-2i. Output expands q-products into real and imaginary parts but
leaves the diamond deletion states symbolic.  The u=v chain record uses the
explicit private branch response.
"""
import itertools
from collections import defaultdict
OWN=('A','B','x')
# Sparse real polynomial represented as dict monomial tuple -> integer.
def clean(p):return {tuple(sorted(m)):c for m,c in p.items() if c}
def add(*ps):
 o=defaultdict(int)
 for p in ps:
  for m,c in p.items():o[tuple(sorted(m))]+=c
 return clean(o)
def scale(p,c):return clean({m:c*v for m,v in p.items()})
def mul(*ps):
 o={():1}
 for p in ps:
  n=defaultdict(int)
  for a,c in o.items():
   for b,d in p.items():n[tuple(sorted(a+b))]+=c*d
  o=clean(n)
 return o
def con(c):return {():c} if c else {}
def var(x):return {(x,):1}
# Complex pair (real poly,imag poly).
def ca(*zs):return (add(*(z[0] for z in zs)),add(*(z[1] for z in zs)))
def cm(*zs):
 r,i=con(1),{}
 for a,b in zs:r,i=add(mul(r,a),scale(mul(i,b),-1)),add(mul(r,b),mul(i,a))
 return r,i
def rv(x):return (var(x),{})
def d(j):return rv(f'd{j}')
def q(j):return (var(f'e{j}'),con(-2))
def h(S=()):
 k=''.join(sorted(set(S),key=OWN.index));s='_'+k if k else ''
 return var('R'+s),var('I'+s)
def expr(p):
 def key(x):return (len(x[0]),x[0])
 out=[]
 for m,c in sorted(p.items(),key=key):
  mon='*'.join(m);body=(str(abs(c))+'*' if abs(c)!=1 and mon else str(abs(c)) if not mon else '')+mon
  out.append((('-' if c<0 else '') if not out else (' - ' if c<0 else ' + '))+body)
 return ''.join(out) or '0'
def direct(roots):
 terms=[]
 for mask in range(8):
  S=[j for j in range(3) if mask>>j&1];rs=[roots[j] for j in S]
  if len(set(rs))<len(rs):continue
  terms.append(cm(*[(q(j+1) if j in S else d(j+1)) for j in range(3)],h(rs)))
 return ca(*terms)
def chain(u,w):
 D,Du,Dw,Duw=h(),h((u,)),h((w,)),h((u,w,))
 F=ca(cm(d(1),d(2),D),cm(d(2),q(1),Du),cm(q(2),ca(cm(rv('b1'),D),Du)))
 if u!=w:
  Fw=ca(cm(d(1),d(2),Dw),cm(d(2),q(1),Duw),cm(q(2),ca(cm(rv('b1'),Dw),Duw)))
 else:
  # Psi(B12)=a1*a2*b1*b2+a1*b1+a2*b1+a2*b2+b1*b2+1-2i*b1.
  RB=add(mul(var('a1'),var('a2'),var('b1'),var('b2')),mul(var('a1'),var('b1')),mul(var('a2'),var('b1')),mul(var('a2'),var('b2')),mul(var('b1'),var('b2')),con(1))
  IB=scale(var('b1'),-2);Fw=cm((RB,IB),Dw)
 return ca(cm(d(3),F),cm(q(3),Fw))
def fork(occ):
 D,Dx=h(),h(('x',));X=ca(cm(d(1),D),cm(q(1),Dx));Xa=ca(cm(rv('b1'),D),Dx);Xb=ca(cm(rv('a1'),D),Dx)
 if occ=='same':return ca(cm(d(2),d(3),X),cm(q(2),d(3),Xa),cm(d(2),q(3),Xa))
 return ca(cm(d(2),d(3),X),cm(d(3),q(2),Xa),cm(d(2),q(3),Xb),cm(q(2),q(3),D))
def chain3():
 D,Dx=h(),h(('x',));X1=ca(cm(d(1),D),cm(q(1),Dx));X1m=ca(cm(rv('b1'),D),Dx);X2=ca(cm(d(2),X1),cm(q(2),X1m));X2m=ca(cm(rv('b2'),X1),X1m);return ca(cm(d(3),X2),cm(q(3),X2m))
def emit(rec,Z):
 print('record',repr(rec));print('  R =',expr(Z[0]));print('  I =',expr(Z[1]))
for roots in itertools.combinations_with_replacement(OWN,3):
 if 'x' in roots:emit(('direct3',roots),direct(roots))
for u in OWN:
 for w in OWN:
  if 'x' in (u,w):emit(('chain2+direct',u,w),chain(u,w))
emit(('fork','x','same'),fork('same'));emit(('fork','x','split'),fork('split'));emit(('chain3','x'),chain3())
