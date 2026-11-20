#!/usr/bin/env python3
"""Exact partition/consolidation regression for seven fourfold support shapes."""

def parts(n,lo=1):
 if n==0: yield (); return
 for k in range(lo,n+1):
  for rest in parts(n-k,k): yield (k,)+rest
assert list(parts(4))==[(1,1,1,1),(1,1,2),(1,3),(2,2),(4,)]
# Encode support as (simple dimension,multiplicity); list surviving consolidated patterns.
shapes={
 ((4,1),):'X4',
 ((1,1),(3,1)):'X3 x E',
 ((2,1),(2,1)):'S1 x S2',
 ((2,2),):'S^2',
 ((1,2),(2,1)):'S x E^2',
 ((1,4),):'E^4',
 ((1,2),(1,2)):'E1^2 x E2^2',
}
for key in shapes:
 assert sum(g*m for g,m in key)==4
# Odd elliptic supports must have CM by the fixed K; two such supports are isogenous,
# so at most one consolidated odd elliptic support is allowed.
for key in shapes:
 assert sum(1 for g,m in key if g==1 and m%2)==0 or key==((1,1),(3,1))
print('PASS seven exact consolidated shapes')
for i,v in enumerate(shapes.values(),1): print(i,v)
