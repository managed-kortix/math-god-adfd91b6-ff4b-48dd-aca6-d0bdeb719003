#!/usr/bin/env python3
"""Sound reduced 16-vertex relaxation of final m=9, rho=0, k=6."""
import argparse

from snc_cnf import CNF, threshold

W,Z=0,1
A=tuple(range(2,9))
B=tuple(range(9,16))
N=16


def exact(c, outputs, value):
    if value == 0: c.add(-outputs[0])
    elif value == len(outputs): c.add(outputs[-1])
    else: c.add(outputs[value-1]); c.add(-outputs[value])


def build(selected=A):
    selected=set(selected); c=CNF()
    arc={(u,v):c.var(f"a_{u}_{v}") for u in range(N) for v in range(N) if u!=v}
    for u in range(N):
        for v in range(u+1,N): c.add(-arc[u,v],-arc[v,u])
    for v in (Z,)+A: c.add(arc[W,v])
    for b in B: c.add(-arc[W,b])
    for v in range(N):
        if v!=Z: c.add(arc[Z,v],arc[v,Z])
    for b in B: c.add(*(arc[a,b] for a in A))
    for u in range(N):
        target=6 if u in B else 8
        exact(c,threshold(c,[arc[u,v] for v in range(N) if v!=u],f"deg{u}"),target)
    for a in sorted(selected):
        witnesses=[]
        for t in range(N):
            if t==a: continue
            s=c.var(f"inacc_{a}_{t}");witnesses.append(s)
            c.add(-s,-arc[a,t])
            for y in range(N):
                if y not in (a,t): c.add(-s,-arc[a,y],-arc[y,t])
        # Select exactly two genuine inaccessible vertices. Since selectors are
        # implications, this is existentially equivalent to at least two being
        # inaccessible; unselected inaccessible vertices remain permitted.
        exact(c,threshold(c,witnesses,f"two_inacc_{a}"),2)
    return c


def emit(out, selected=A):
    c=build(selected)
    with open(out,"w",encoding="ascii",newline="\n") as f:
        for name,num in c.names.items(): f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for clause in c.clauses: f.write(" ".join(map(str,clause))+" 0\n")
    print(f"selected={','.join(map(str,selected))} vars={len(c.names)} clauses={len(c.clauses)}")


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("output");p.add_argument("--omit",type=int,choices=A)
    a=p.parse_args();selected=A if a.omit is None else tuple(v for v in A if v!=a.omit)
    emit(a.output,selected)
