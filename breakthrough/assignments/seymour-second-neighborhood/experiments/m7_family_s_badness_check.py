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


def fail(message):
    raise RuntimeError(message)


def require(condition,message):
    if not condition:
        fail(message)


def read_graph(path):
    try:
        lines=[line.strip() for line in open(path,encoding='ascii') if line.strip()]
    except (OSError,UnicodeError) as ex:
        fail(f'graph read failed: {ex}')
    try:
        order=int(lines[0]) if lines else None
    except ValueError as ex:
        fail(f'invalid order line: {ex}')
    require(order==N,'expected order 18')
    arcs=set()
    for line in lines[1:]:
        try:
            fields=line.split();require(len(fields)==2,f'invalid arc line {line!r}')
            u,v=map(int,fields)
        except ValueError as ex:
            fail(f'invalid arc line {line!r}: {ex}')
        require(0<=u<N and 0<=v<N and u!=v and (u,v) not in arcs,
                f'invalid or duplicate arc {line!r}')
        arcs.add((u,v))
    return arcs


def n1(arcs,u):
    return {v for v in range(N) if (u,v) in arcs}


def n2(arcs,u):
    one=n1(arcs,u)
    return {v for x in one for v in range(N) if (x,v) in arcs}-one-{u}


def observed_row(arcs):
    def atype(u):
        bits=tuple(int((u,z) not in arcs and (z,u) not in arcs) for z in C)
        try:
            return ATYPES.index(bits)
        except ValueError as ex:
            fail(f'invalid A/C incidence at vertex {u}: {bits}: {ex}')
    distinguished=tuple(atype(u) for u in (0,1,2))
    a_counts=tuple(Counter(atype(u) for u in range(3,9))[t] for t in range(4))
    btypes=[]
    for b in sorted(B):
        symbols=[]
        for z in C:
            if (z,b) in arcs:
                symbols.append(0)
            elif (b,z) in arcs:
                symbols.append(1)
            else:
                symbols.append(2)
        btypes.append(3*symbols[0]+symbols[1])
    b_counts=tuple(Counter(btypes)[t] for t in range(9))
    if (16,17) not in arcs and (17,16) not in arcs:
        state='M'
    elif (16,17) in arcs:
        state='01'
    else:
        state='10'
    holes=[(u,v) for u in range(N) for v in range(u+1,N)
           if (u,v) not in arcs and (v,u) not in arcs]
    h=sum(u<16 and v<16 for u,v in holes)
    return (state,distinguished,a_counts,b_counts,h),holes


def parse_expected(text):
    try:
        value=json.loads(text)
    except json.JSONDecodeError as ex:
        fail(f'row JSON parse failed: {ex}')
    require(type(value) is list and len(value)==5,'row must have five fields')
    state,distinguished,a_counts,b_counts,h=value
    require(state in ('M','01','10'),'row state')
    require(type(distinguished) is list and len(distinguished)==3,'row distinguished fields')
    require(type(a_counts) is list and len(a_counts)==4,'row A counts')
    require(type(b_counts) is list and len(b_counts)==9,'row B counts')
    require(type(h) is int and 0<=h<=4,'row h')
    values=distinguished+a_counts+b_counts
    require(all(type(z) is int and z>=0 for z in values),'row integer fields')
    return (state,tuple(distinguished),tuple(a_counts),tuple(b_counts),h)


def check_graph(arcs,expected):
    require(all(not ((u,v) in arcs and (v,u) in arcs)
                for u in range(N) for v in range(u+1,N)),'digon detected')
    one=[n1(arcs,u) for u in range(N)];two=[n2(arcs,u) for u in range(N)]
    require([len(z) for z in one]==[9 if u in HIGHS else 8 for u in range(N)],
            'wrong outdegree sequence')
    require(all(len(two[u])<len(one[u]) for u in range(N)),'global badness fails')
    got,holes=observed_row(arcs)
    require(len(holes)==7 and got==expected,f'wrong holes/type row: got={got} expected={expected}')
    require(one[W]==A and two[W]==B,'wrong root layers')
    for high in sorted(HIGHS):
        reduced={(u,v) for u,v in arcs if u!=high and v!=high}
        require(n2(reduced,W)==B,f'robustness fails after deleting high {high}')
    return holes,two


def main():
    p=argparse.ArgumentParser();p.add_argument('--graph',required=True)
    p.add_argument('--row',required=True,help='JSON row printed by the scout')
    x=p.parse_args();expected=parse_expected(x.row);arcs=read_graph(x.graph)
    holes,two=check_graph(arcs,expected)
    print(f'PASS semantic family-S witness row={json.dumps(expected,separators=(",",":"))}')
    print(f'PASS holes={holes} d2={[len(z) for z in two]}')


if __name__=='__main__':
    main()
