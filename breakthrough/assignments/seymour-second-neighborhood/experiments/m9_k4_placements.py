#!/usr/bin/env python3
"""Exact rooted-cell placements of degree>=2 vertices in a k=4 shape."""
import argparse
from m9_k4_shapes import P,build,exact
from snc_cnf import threshold

A=tuple(range(2,9)); B=tuple(range(9,16)); R=(0,)

def emit(rho,shape,alpha,beta,epsilon,out):
    n2=P[shape][0]
    if min(alpha,beta,epsilon)<0 or epsilon not in (0,1) or alpha+beta+epsilon!=n2:
        raise ValueError("placement counts must partition n2")
    c,ge2,_=build(rho,shape); tag=f"pl{rho}{shape}{alpha}{beta}{epsilon}"
    for cell,value,name in ((A,alpha,"a"),(B,beta,"b"),(R,epsilon,"r")):
        exact(c,threshold(c,[ge2[v] for v in cell],tag+name),value)
    with open(out,"w",encoding="ascii",newline="\n") as f:
        for name,num in c.names.items():f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for cl in c.clauses:f.write(" ".join(map(str,cl))+" 0\n")
    print(f"rho={rho} shape={shape} alpha={alpha} beta={beta} epsilon={epsilon} vars={len(c.names)} clauses={len(c.clauses)}")

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("rho",type=int,choices=range(3));p.add_argument("shape",choices=P);p.add_argument("alpha",type=int);p.add_argument("beta",type=int);p.add_argument("epsilon",type=int);p.add_argument("output");a=p.parse_args();emit(a.rho,a.shape,a.alpha,a.beta,a.epsilon,a.output)
