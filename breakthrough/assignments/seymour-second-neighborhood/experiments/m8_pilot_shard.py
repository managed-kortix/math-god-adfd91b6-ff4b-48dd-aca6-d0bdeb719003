#!/usr/bin/env python3
"""Emit one genuine corrected-sixth-row terminal pilot shard."""
import argparse
from snc_cnf import generate


def unit(c,name,value=True): c.add(c.var(name) if value else -c.var(name))


def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',required=True); x=p.parse_args()
    c=generate(18,7,8,robust_witness=True,high_vertices=(1,),
               forced_witness=(0,1),arc_minimal=True)
    # A=1..8, B=9..15, C=16,17. Missing graph:
    # c0 misses v,r; c1 misses v,r,a2,a3,a4,a5.
    missing={(0,16),(1,16),(0,17),(1,17),(2,17),(3,17),(4,17),(5,17)}
    for i in range(18):
        for j in range(i+1,18):
            unit(c,f"h_{i}_{j}",(i,j) in missing)
    unit(c,'a_16_17')
    # rho0=0; rho1=5, canonically first five B vertices.
    for b in range(9,16): unit(c,f"a_16_{b}",False)
    for b in range(9,16): unit(c,f"a_17_{b}",b<=13)
    with open(x.output,'w',encoding='ascii',newline='\n') as f:
        for name,num in c.names.items(): f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for clause in c.clauses: f.write(' '.join(map(str,clause))+' 0\n')
    print(f"vars={len(c.names)} clauses={len(c.clauses)} output={x.output}")


if __name__=='__main__': main()
