#!/usr/bin/env python3
"""Final m=9 rows split by root-C holes, then internal-B holes."""
import argparse
from snc_cnf import generate, threshold
ROWS={(0,6),(0,5),(1,5)}
def exact(c,o,v):
    if v==0:c.add(-o[0])
    elif v==len(o):c.add(o[-1])
    else:c.add(o[v-1]);c.add(-o[v])
def H(c,u,v):return c.var(f"h_{min(u,v)}_{max(u,v)}")
def emit(r,k,g,hb,out):
    if (r,k) not in ROWS:raise ValueError("bad row")
    if g and hb is not None:raise ValueError("hB only when g=0")
    if not g and hb is None:raise ValueError("g=0 requires hB")
    c=generate(18,7,9,True,(),(0,1),True)
    for j in range(18):
        if j!=1:c.add(-H(c,1,j))
    exact(c,threshold(c,[c.var(f"a_{x}_{b}") for x in (16,17)
                         for b in range(9,16)],f"finrho{r}{k}{g}{hb}"),r)
    exact(c,threshold(c,[H(c,i,j) for i in range(16) for j in range(i+1,16)],
                      f"fink{r}{k}{g}{hb}"),k)
    exact(c,threshold(c,[H(c,0,16),H(c,0,17)],f"fing{r}{k}{g}{hb}"),g)
    if hb is not None:
        exact(c,threshold(c,[H(c,i,j) for i in range(9,16)
                             for j in range(i+1,16)],f"finhb{r}{k}{hb}"),hb)
    with open(out,"w",encoding="ascii",newline="\n") as f:
        for name,num in c.names.items():f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for cl in c.clauses:f.write(" ".join(map(str,cl))+" 0\n")
    print(f"rho={r} k={k} g={g} hB={hb} vars={len(c.names)} clauses={len(c.clauses)}")
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("rho",type=int);p.add_argument("k",type=int);p.add_argument("g",type=int,choices=(0,1,2));p.add_argument("output");p.add_argument("--hB",type=int);a=p.parse_args();emit(a.rho,a.k,a.g,a.hB,a.output)
