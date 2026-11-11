#!/usr/bin/env python3
"""Exact 155 internal-C refinements of the 23 hard m5 B6 parents."""
import itertools
from m5_b6_cnf import embedding
from m5_b6_shapes import placements,SHAPES
HARD1={104,138,389,394,941,1462,1564,1572,2188,2331,2339}
HARD2={100,367,391,881,1498,1506,2467,2573,2576,2944,3872,3875}
def cases():
 out=[]
 for i in sorted(HARD1|HARD2):
  name,w=placements()[i];_,edges=SHAPES[name];mp=embedding(name,w);E={tuple(sorted((mp[u],mp[v]))) for u,v in edges};M=[sum(tuple(sorted((15+j,v))) in E for v in range(9)) for j in range(3)];hc,r=(1,0) if i in HARD1 else (2,1)
  for states in itertools.product(range(3),repeat=3):
   pairs=((0,1),(0,2),(1,2));
   if any((states[k]==2)!=(tuple(sorted((15+u,15+v))) in E) for k,(u,v) in enumerate(pairs)):continue
   t=[0,0,0]
   for st,(u,v) in zip(states,pairs):
    if st==0:t[u]+=1
    elif st==1:t[v]+=1
   for tail in ([None] if r==0 else range(3)):
    x=tuple(j for j in range(3) if 1-M[j]+t[j]+(1 if tail==j else 0)==1)
    if len(x)==hc and all(1-M[j]+t[j]+(1 if tail==j else 0) in (0,1) for j in range(3)):out.append((i,hc,r,x,states,tail))
 return out
if __name__=="__main__":
 from collections import Counter
 q=cases();print(Counter(i for i,*_ in q));print(f"count={len(q)}")
