#!/usr/bin/env python3
"""Standalone full minimal-counterexample CNF for one m=5 B6 placement."""
import argparse
from m5_b6_shapes import placements,SHAPES
from snc_cnf import generate,threshold

LABELS=((0,),tuple(range(1,9)),tuple(range(9,15)),tuple(range(15,18)))
def embedding(name,w):
 used=[0]*4;mp={}
 for v,c in enumerate(w):mp[v]=LABELS[c][used[c]];used[c]+=1
 return mp
def exact(c,o,v):
 if v==0:c.add(-o[0])
 elif v==len(o):c.add(o[-1])
 else:c.add(o[v-1]);c.add(-o[v])
def emit(i,path,high_c=None,r=None):
 name,w=placements()[i];n,edges=SHAPES[name];mp=embedding(name,w);E={tuple(sorted((mp[u],mp[v]))) for u,v in edges};c=generate(18,6,5,True,None,None,True)
 for u in range(18):
  for v in range(u+1,18):c.add(c.var(f"h_{u}_{v}") if (u,v) in E else -c.var(f"h_{u}_{v}"))
 if high_c is not None:exact(c,threshold(c,[c.var(f"cnt_d1_{u}_17_9") for u in range(15,18)],f"cube_highC_{high_c}"),high_c)
 if r is not None:exact(c,threshold(c,[c.var(f"a_{u}_{v}") for u in range(15,18) for v in range(9,15)],f"cube_r_{r}"),r)
 with open(path,"w",encoding="ascii",newline="\n") as f:
  for key,val in c.names.items():f.write(f"c var {val} {key}\n")
  f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
  for z in c.clauses:f.write(" ".join(map(str,z))+" 0\n")
 print(f"index={i} shape={name} word={w} highC={high_c} r={r} support={sorted(E)} vars={len(c.names)} clauses={len(c.clauses)}")
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("index",type=int);p.add_argument("output");p.add_argument("--high-c",type=int);p.add_argument("--r",type=int);a=p.parse_args();emit(a.index,a.output,a.high_c,a.r)
