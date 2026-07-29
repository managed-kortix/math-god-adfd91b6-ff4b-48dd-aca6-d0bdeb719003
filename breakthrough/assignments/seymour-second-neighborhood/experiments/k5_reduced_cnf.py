#!/usr/bin/env python3
"""Common sound 16-vertex relaxation of final m=9 k=5 rows."""
import argparse
from snc_cnf import CNF,threshold
from k6_reduced_cnf import exact

W,Z=0,1;A=tuple(range(2,9));K=tuple(range(9,15));S=15;B=K+(S,);N=16

def build():
 c=CNF();arc={(u,v):c.var(f"a_{u}_{v}") for u in range(N) for v in range(N) if u!=v}
 for u in range(N):
  for v in range(u+1,N):c.add(-arc[u,v],-arc[v,u])
 for v in (Z,)+A:c.add(arc[W,v])
 for b in B:c.add(-arc[W,b])
 for v in range(N):
  if v!=Z:c.add(arc[Z,v],arc[v,Z])
 for b in B:c.add(*(arc[a,b] for a in A))
 for u in range(N):
  target=6 if u in K else (7 if u==S else 8)
  exact(c,threshold(c,[arc[u,v] for v in range(N) if v!=u],f"deg{u}"),target)
 for a in A:
  hit=c.var(f"hitK_{a}")
  for b in K:c.add(-arc[a,b],hit)
  c.add(-hit,*(arc[a,b] for b in K))
  ws=[]
  for t in range(N):
   if t==a:continue
   q=c.var(f"inacc_{a}_{t}");ws.append(q);c.add(-q,-arc[a,t])
   for y in range(N):
    if y not in (a,t):c.add(-q,-arc[a,y],-arc[y,t])
  out=threshold(c,ws,f"inacc_count_{a}");c.add(out[0]);c.add(-hit,out[1])
 return c

def emit(path):
 c=build()
 with open(path,"w",encoding="ascii",newline="\n") as f:
  for n,v in c.names.items():f.write(f"c var {v} {n}\n")
  f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
  for x in c.clauses:f.write(" ".join(map(str,x))+" 0\n")
 print(f"vars={len(c.names)} clauses={len(c.clauses)}")

if __name__=="__main__":p=argparse.ArgumentParser();p.add_argument("output");a=p.parse_args();emit(a.output)
