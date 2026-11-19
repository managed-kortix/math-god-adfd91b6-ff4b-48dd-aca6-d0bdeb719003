#!/usr/bin/env python3
"""Independent semantic checker for a family-S exact-badness SAT witness.

Input is a plain arc list written by ``m7_family_s_badness_scout.py``.  This
checker does not import the CNF producer: it recomputes every graph-theoretic
condition directly from the arc set and checks the selected canonical type row.
"""
import argparse,json
from collections import Counter

N=18; W=0; A=set(range(1,9)); B=set(range(9,16)); C=(16,17); HIGHS={1,2}
ATYPES=((0,0),(0,1),(1,0),(1,1))


def read_graph(path):
    lines=[x.strip() for x in open(path,encoding='ascii') if x.strip()]
    if not lines or int(lines[0])!=N: raise ValueError('expected order 18')
    arcs=set()
    for line in lines[1:]:
        u,v=map(int,line.split())
        if not (0<=u<N and 0<=v<N) or u==v or (u,v) in arcs:
            raise ValueError(f'invalid or duplicate arc {line!r}')
        arcs.add((u,v))
    return arcs


def n1(arcs,u): return {v for v in range(N) if (u,v) in arcs}
def n2(arcs,u):
    one=n1(arcs,u)
    return {v for x in one for v in range(N) if (x,v) in arcs}-one-{u}


def observed_row(arcs):
    def atype(u):
        bits=tuple(int((u,z) not in arcs and (z,u) not in arcs) for z in C)
        return ATYPES.index(bits)
    distinguished=tuple(atype(u) for u in (0,1,2))
    a_counts=tuple(Counter(atype(u) for u in range(3,9))[t] for t in range(4))
    bt=[]
    for b in sorted(B):
        symbols=[]
        for z in C:
            if (z,b) in arcs: symbols.append(0)
            elif (b,z) in arcs: symbols.append(1)
            else: symbols.append(2)
        bt.append(3*symbols[0]+symbols[1])
    b_counts=tuple(Counter(bt)[t] for t in range(9))
    if (16,17) not in arcs and (17,16) not in arcs: state='M'
    elif (16,17) in arcs: state='01'
    else: state='10'
    holes=[(u,v) for u in range(N) for v in range(u+1,N)
           if (u,v) not in arcs and (v,u) not in arcs]
    h=sum(u<16 and v<16 for u,v in holes)
    return (state,distinguished,a_counts,b_counts,h),holes


def main():
    p=argparse.ArgumentParser();p.add_argument('--graph',required=True)
    p.add_argument('--row',required=True,help='JSON row printed by the scout')
    x=p.parse_args();expected=json.loads(x.row)
    expected=(expected[0],tuple(expected[1]),tuple(expected[2]),tuple(expected[3]),expected[4])
    arcs=read_graph(x.graph)
    assert all(not ((u,v) in arcs and (v,u) in arcs)
               for u in range(N) for v in range(u+1,N))
    one=[n1(arcs,u) for u in range(N)];two=[n2(arcs,u) for u in range(N)]
    assert [len(z) for z in one]==[9 if u in HIGHS else 8 for u in range(N)]
    assert all(len(two[u])<len(one[u]) for u in range(N))
    got,holes=observed_row(arcs)
    assert len(holes)==7 and got==expected,(got,expected)
    assert one[W]==A and two[W]==B
    for high in sorted(HIGHS):
        reduced={(u,v) for u,v in arcs if u!=high and v!=high}
        assert n2(reduced,W)==B
    print(f'PASS semantic family-S witness row={json.dumps(expected,separators=(",",":"))}')
    print(f'PASS holes={holes} d2={[len(z) for z in two]}')

if __name__=='__main__':main()
