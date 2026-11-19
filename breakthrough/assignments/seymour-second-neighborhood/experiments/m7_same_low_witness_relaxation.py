#!/usr/bin/env python3
"""Check an explicit m=7 local relaxation with one low witness for both highs.

This is intentionally not an SNC counterexample: global badness and arc
minimality are omitted.  No solver is required; the fixed arc rows are checked
directly under exact-distance-two semantics.
"""
N=18; W=0; HIGHS={1,2}; A=set(range(1,9)); B=set(range(9,16))
ROWS={
0:(1,2,3,4,5,6,7,8),
1:(2,3,4,5,6,7,10,11,15),
2:(3,5,6,7,9,10,11,13,15),
3:(4,6,8,9,10,11,13,15),
4:(2,6,8,9,10,11,12,13),
5:(3,4,6,8,9,12,13,14),
6:(8,9,10,11,12,13,14,15),
7:(3,4,5,6,8,12,13,14),
8:(1,2,9,10,11,12,13,14),
9:(0,1,7,12,13,14,16,17),
10:(7,9,11,12,14,15,16,17),
11:(0,7,9,12,14,15,16,17),
12:(1,2,3,13,14,15,16,17),
13:(0,1,10,11,14,15,16,17),
14:(0,1,2,3,4,15,16,17),
15:(0,4,5,7,8,9,16,17),
16:(0,1,3,4,5,7,8,17),
17:(0,2,3,4,5,6,7,8),
}
ARCS={(u,v) for u,row in ROWS.items() for v in row}

def n1(v,arcs=ARCS): return {u for u in range(N) if (v,u) in arcs}
def n2(v,arcs=ARCS):
    one=n1(v,arcs)
    return {z for y in one for z in n1(y,arcs)}-one-{v}

assert all(u not in ROWS[u] for u in range(N))
assert all(not ((u,v) in ARCS and (v,u) in ARCS) for u in range(N) for v in range(u+1,N))
assert all(len(ROWS[u])==(9 if u in HIGHS else 8) for u in range(N))
holes=[(u,v) for u in range(N) for v in range(u+1,N)
       if (u,v) not in ARCS and (v,u) not in ARCS]
assert holes==[(0,10),(0,12),(1,17),(2,16),(5,10),(5,11),(6,16)]
assert n1(W)==A and n2(W)==B
for h in sorted(HIGHS):
    assert (W,h) in ARCS
    reduced={(u,v) for u,v in ARCS if u!=h and v!=h}
    assert n2(W,reduced)==B
print('PASS local shared-low-witness relaxation')
print('holes',holes)
for h in sorted(HIGHS):
    reduced={(u,v) for u,v in ARCS if u!=h and v!=h}
    print(f'delete={h} N1={sorted(n1(W,reduced))} N2={sorted(n2(W,reduced))}')
