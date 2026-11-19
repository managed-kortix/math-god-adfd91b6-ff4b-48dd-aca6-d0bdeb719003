#!/usr/bin/env python3
"""Verify hostile local countermodels at opposite family-S margin extremes.

Both fixed oriented graphs have order 18, seven holes, highs 1 and 2, low root
0, N+(0)={1,...,8}, N++(0)={9,...,15}, and root-0 exact second neighborhood
unchanged after deleting either high.  Global badness and arc minimality are
not asserted.  They refute pruning based only on the family-S local package.
"""
N=18; W=0; HIGHS={1,2}; A=set(range(1,9)); B=set(range(9,16)); C={16,17}

ROWS={
"rho4_h0_C-hole": {
0:(1,2,3,4,5,6,7,8),
1:(3,4,6,7,10,12,13,14,15),
2:(1,3,4,8,10,12,13,14,15),
3:(4,5,7,8,9,12,13,14),
4:(5,6,8,9,10,12,14,15),
5:(1,2,6,8,9,10,12,15),
6:(2,3,8,9,10,13,14,15),
7:(2,4,5,6,11,13,14,15),
8:(1,7,9,10,11,12,13,15),
9:(0,1,2,7,10,11,16,17),
10:(0,3,7,13,14,15,16,17),
11:(0,1,2,3,4,5,6,10),
12:(0,6,7,9,10,11,14,17),
13:(0,4,5,9,11,12,15,16),
14:(0,5,8,9,11,13,16,17),
15:(0,3,9,11,12,14,16,17),
16:(3,4,5,6,7,8,11,12),
17:(1,4,5,6,7,8,11,13),
},
"rho0_h4_C-present": {
0:(1,2,3,4,5,6,7,8),
1:(3,4,6,7,8,9,10,11,12),
2:(1,3,4,5,6,7,8,13,15),
3:(4,7,9,11,12,13,14,15),
4:(5,6,9,10,11,12,14,15),
5:(1,3,6,7,9,10,11,15),
6:(3,9,10,11,12,13,14,15),
7:(4,6,9,10,11,12,13,14),
8:(3,4,5,6,7,10,11,12),
9:(0,2,8,10,11,12,16,17),
10:(0,2,3,11,13,15,16,17),
11:(0,2,12,13,14,15,16,17),
12:(0,2,5,10,13,14,16,17),
13:(0,5,8,9,14,15,16,17),
14:(0,2,5,8,9,10,16,17),
15:(0,7,8,9,12,14,16,17),
16:(1,2,3,4,5,6,7,8),
17:(0,1,2,3,4,6,7,16),
},
"singleton_ordinary_B_support": {
0:(1,2,3,4,5,6,7,8),
1:(2,3,4,8,10,11,12,14,15),
2:(3,4,7,8,10,11,12,13,14),
3:(4,9,10,11,12,13,14,15),
4:(7,8,10,11,12,13,14,15),
5:(1,2,3,4,7,11,13,14),
6:(1,2,3,4,5,10,11,13),
7:(1,3,6,8,12,13,14,15),
8:(3,5,6,10,12,13,14,15),
9:(0,1,5,6,7,8,16,17),
10:(0,5,7,9,14,15,16,17),
11:(0,7,8,9,10,12,16,17),
12:(0,5,6,9,10,13,16,17),
13:(0,1,9,10,11,14,16,17),
14:(0,6,9,11,12,15,16,17),
15:(0,5,6,9,11,12,16,17),
16:(0,1,2,3,4,5,6,17),
17:(0,1,2,3,4,5,7,8),
},
}

def n1(v,arcs): return {u for u in range(N) if (v,u) in arcs}
def n2(v,arcs):
    one=n1(v,arcs)
    return {z for y in one for z in n1(y,arcs)}-one-{v}

for name,rows in ROWS.items():
    arcs={(u,v) for u,row in rows.items() for v in row}
    assert all(len(rows[u])==(9 if u in HIGHS else 8) for u in range(N))
    assert all(not ((u,v) in arcs and (v,u) in arcs)
               for u in range(N) for v in range(u+1,N))
    holes=[(u,v) for u in range(N) for v in range(u+1,N)
           if (u,v) not in arcs and (v,u) not in arcs]
    assert len(holes)==7 and n1(W,arcs)==A and n2(W,arcs)==B
    for h in HIGHS:
        reduced={(u,v) for u,v in arcs if u!=h and v!=h}
        assert n2(W,reduced)==B
    rho=sum((c,b) in arcs for c in C for b in B)
    hT=sum(u<16 and v<16 for u,v in holes)
    missing_C=(16,17) in holes
    if name.startswith('rho4'):
        expected=(4,0,True)
    elif name.startswith('rho0'):
        expected=(0,4,False)
    else:
        expected=(0,4,False)
        assert {a for a in A if (a,9) in arcs}=={3}
    assert (rho,hT,missing_C)==expected
    seymour=[v for v in range(N) if len(n2(v,arcs))>=len(n1(v,arcs))]
    assert seymour                 # explicitly not a global counterexample
    print(f"PASS {name} rho={rho} hT={hT} C_hole={missing_C} "
          f"Seymour={seymour} holes={holes}")
