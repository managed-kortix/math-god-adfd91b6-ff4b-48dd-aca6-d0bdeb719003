#!/usr/bin/env python3
"""Direct verifier for reduced k6 orientations and selected bad rows."""
import argparse

W,Z=0,1;A=set(range(2,9));B=set(range(9,16));N=16


def parse(path):
    rows={}
    with open(path,encoding="ascii") as f:
        for raw in f:
            raw=raw.strip()
            if not raw or raw.startswith("#"):continue
            vals=list(map(int,raw.split()));u,*vs=vals
            if u in rows or not 0<=u<N or len(vs)!=len(set(vs)) or u in vs:
                raise ValueError("malformed row")
            rows[u]=set(vs)
    if set(rows)!=set(range(N)):raise ValueError("need rows 0..15")
    return rows


def verify(rows,selected):
    for u in range(N):
        target=6 if u in B else 8
        assert len(rows[u])==target
        assert all(0<=v<N and u not in rows[v] for v in rows[u])
    assert rows[W]=={Z}|A
    assert all((Z in rows[v])^(v in rows[Z]) for v in range(N) if v!=Z)
    assert all(any(b in rows[a] for a in A) for b in B)
    holes=[]
    for u in range(N):
        for v in range(u+1,N):
            if v not in rows[u] and u not in rows[v]:holes.append((u,v))
    assert len(holes)==6 and all(Z not in e for e in holes)
    inaccessible={}
    for a in sorted(A):
        inaccessible[a]={t for t in range(N) if t!=a and t not in rows[a]
                         and not any(y in rows[a] and t in rows[y] for y in range(N))}
        if a in selected:assert len(inaccessible[a])>=2
    print(f"PASS holes={holes}")
    for a in sorted(A):print(f"a={a} inaccessible={sorted(inaccessible[a])}")


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("file");p.add_argument("--omit",type=int,choices=A)
    x=p.parse_args();selected=A if x.omit is None else A-{x.omit};verify(parse(x.file),selected)
