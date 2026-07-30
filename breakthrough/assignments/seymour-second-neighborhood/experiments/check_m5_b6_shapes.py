#!/usr/bin/env python3
"""Independent orbit audit for the 4,355 m=5 B6 placements."""
import hashlib,itertools
SHAPES={"P6":(6,((0,1),(1,2),(2,3),(3,4),(4,5))),"P4_P3":(7,((0,1),(1,2),(2,3),(4,5),(5,6))),"C3_P3":(6,((0,1),(1,2),(0,2),(3,4),(4,5))),"C4_K2":(6,((0,1),(1,2),(2,3),(0,3),(4,5))),"P3_P3_K2":(8,((0,1),(1,2),(3,4),(4,5),(6,7)))}
def aut(n,edges):
 E={tuple(sorted(e)) for e in edges};return [p for p in itertools.permutations(range(n)) if {tuple(sorted((p[u],p[v]))) for u,v in E}==E]
def main():
 rows=[];counts={}
 for name,(n,edges) in SHAPES.items():
  G=aut(n,edges);count=0
  for w in itertools.product(range(4),repeat=n):
   if w.count(0)>1 or w.count(1)>8 or w.count(2)>6 or w.count(3)>3:continue
   if any({w[u],w[v]}=={0,1} for u,v in edges):continue
   if w!=min(tuple(w[p[i]] for i in range(n)) for p in G):continue
   rows.append((name,w));count+=1
  counts[name]=count
 assert counts=={"P6":688,"P4_P3":1459,"C3_P3":283,"C4_K2":194,"P3_P3_K2":1731}
 data="".join(f"{i}\t{n}\t{''.join('RABC'[x] for x in w)}\n" for i,(n,w) in enumerate(rows)).encode();assert len(data)==85330
 print(f"PASS placements={len(rows)} sha256={hashlib.sha256(data).hexdigest()}")
if __name__=="__main__":main()
