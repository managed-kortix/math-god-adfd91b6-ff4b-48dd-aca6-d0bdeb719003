#!/usr/bin/env python3
"""Canonical rooted-layer placements of the five uncovered m=5 supports."""
import hashlib,itertools

SHAPES={
 "P6":(6,((0,1),(1,2),(2,3),(3,4),(4,5))),
 "P4_P3":(7,((0,1),(1,2),(2,3),(4,5),(5,6))),
 "C3_P3":(6,((0,1),(1,2),(0,2),(3,4),(4,5))),
 "C4_K2":(6,((0,1),(1,2),(2,3),(0,3),(4,5))),
 "P3_P3_K2":(8,((0,1),(1,2),(3,4),(4,5),(6,7))) }
CELLS="RABC";CAP=(1,8,6,3)

def automorphisms(n,edges):
 E={tuple(sorted(e)) for e in edges};return [p for p in itertools.permutations(range(n)) if {tuple(sorted((p[u],p[v]))) for u,v in E}==E]
def placements():
 out=[]
 for name,(n,edges) in SHAPES.items():
  aut=automorphisms(n,edges)
  for w in itertools.product(range(4),repeat=n):
   if any(w.count(i)>CAP[i] for i in range(4)):continue
   if any({w[u],w[v]}=={0,1} for u,v in edges):continue
   orbit=[tuple(w[p[i]] for i in range(n)) for p in aut]
   if w==min(orbit):out.append((name,w))
 return out
def payload():return "".join(f"{i}\t{name}\t{''.join(CELLS[x] for x in w)}\n" for i,(name,w) in enumerate(placements())).encode()
if __name__=="__main__":
 from collections import Counter
 p=payload();print(Counter(n for n,_ in placements()));print(f"count={len(placements())} bytes={len(p)} sha256={hashlib.sha256(p).hexdigest()}")
