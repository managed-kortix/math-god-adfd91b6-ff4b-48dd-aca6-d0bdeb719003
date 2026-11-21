#!/usr/bin/env python3
"""Temporary exact H-family q-row orbit enumerator; does not touch repo."""
import sys
sys.path.insert(0,'/workspace/repo/breakthrough/assignments/seymour-second-neighborhood/experiments')
from snc_cnf import generate
N=18; V=0; Q=1

def comp3(n):
    for o in range(n+1):
        for i in range(n-o+1):
            yield (o,i,n-o-i)

def rows(case):
    if case=='A':
        R=2; G1=tuple(range(3,9)); G2=tuple(range(9,16))
    elif case=='B':
        R=9; G1=tuple(range(2,9)); G2=tuple(range(10,16))
    else: raise ValueError(case)
    # Distinguished incidence is (v_hole, number of C_v holes); v is fixed,
    # while only C0,C1 may be swapped.
    rr=[]
    for x in comp3(len(G1)):
        for y in comp3(len(G2)):
            if x[0]+y[0] != 8: continue # q->r is ninth outarc
            for vh in (0,1):
                for ch in range(3):
                    if x[2]+y[2]+vh+ch <= 7:
                        rr.append((x,y,vh,ch))
    return R,G1,G2,rr

def build(case, robust=True):
    R,G1,G2,rr=rows(case)
    c=generate(18,7,7,False,{Q,R},None,False)
    # H chain. v->q is already forced by rooted A; q->r is extra.
    c.add(c.var(f'a_{Q}_{R}'))
    if robust:
        # v survives deletion of q: each b in B_v has A_v\{q} predecessor.
        A=set(range(1,9)); B=set(range(9,16))
        for b in sorted(B):
            c.add(*[c.var(f'a_{x}_{b}') for x in sorted(A-{Q})])
        # q survives deletion of r: every q-exact-second endpoint has an
        # alternative q--k--x path with k != r.
        for x in range(N):
            if x in (Q,R): continue
            c.add(-c.var(f'q_{Q}_{x}'),
                  *[c.var(f'p_{Q}_{k}_{x}') for k in range(N)
                    if k not in (Q,R,x)])
    return c,(R,G1,G2,rr)

def assumptions(c,info,row):
    R,G1,G2,rr=info
    x,y,vh,ch=row
    lits=[]
    def group(g,t):
        o,i,h=t
        for z,u in enumerate(g):
            if z<o: lits.extend([c.var(f'a_1_{u}'),-c.var(f'a_{u}_1')])
            elif z<o+i: lits.extend([-c.var(f'a_1_{u}'),c.var(f'a_{u}_1')])
            else: lits.extend([-c.var(f'a_1_{u}'),-c.var(f'a_{u}_1')])
    group(G1,x); group(G2,y)
    # v fixed (not swappable with C).
    if vh: lits.extend([-c.var('a_1_0'),-c.var('a_0_1')])
    else: lits.extend([-c.var('a_1_0'),c.var('a_0_1')])
    # C pair canonical under its S2 only.
    for z,u in enumerate((16,17)):
        if z<ch: lits.extend([-c.var(f'a_1_{u}'),-c.var(f'a_{u}_1')])
        else: lits.extend([-c.var(f'a_1_{u}'),c.var(f'a_{u}_1')])
    return lits

if __name__=='__main__':
    from collections import Counter
    for case in 'AB':
        *_,rr=rows(case)
        print(case,len(rr),
              Counter((r[2],r[3]) for r in rr),
              Counter(r[0][2]+r[1][2]+r[2]+r[3] for r in rr))
