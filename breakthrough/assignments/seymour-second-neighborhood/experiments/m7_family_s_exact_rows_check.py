#!/usr/bin/env python3
"""Independent generating-function check of m7_family_s_exact_rows.py."""
from collections import Counter
from itertools import combinations

W,A,B=0,tuple(range(1,9)),tuple(range(9,16))
U=(W,)+A


def masks(n):
    return range(1<<n)


def row_poly(d):
    """Count one labelled C row by (C->B count, holes incident to row)."""
    out=Counter()
    for hu in masks(9):
        a=hu.bit_count(); r=a-1-d
        if not 0<=r<=7: continue
        for ob in masks(7):
            if ob.bit_count()!=r: continue
            available=((1<<7)-1)^ob
            hb=available
            while True:
                out[a+hb.bit_count()]+=1
                if hb==0:break
                hb=(hb-1)&available
    return out


def fixed_poly():
    """C-swap-fixed missing-C-pair rows (the two labelled masks coincide)."""
    out=Counter()
    for hu in masks(9):
        a=hu.bit_count();r=a-1
        if not 0<=r<=7:continue
        for ob in masks(7):
            if ob.bit_count()!=r:continue
            available=((1<<7)-1)^ob
            hb=available
            while True:
                out[2*(a+hb.bit_count())+1]+=1
                if hb==0:break
                hb=(hb-1)&available
    return out


def convolution(p,q,offset=0):
    z=Counter()
    for i,x in p.items():
        for j,y in q.items():z[i+j+offset]+=x*y
    return z


def main():
    p0,p1=row_poly(0),row_poly(1)
    # Present C-pair: two directions, one d=1 row and one d=0 row.
    # Missing C-pair: both rows have d=0 and contributes one hole.
    used=Counter()
    for holes,n in convolution(p1,p0).items():used[holes]+=2*n
    for holes,n in convolution(p0,p0,1).items():used[holes]+=n
    labelled={h:used[7-h] for h in range(8) if used[7-h]}
    fixed_used=fixed_poly()
    fixed={h:fixed_used[7-h] for h in range(8) if fixed_used[7-h]}
    orbits={h:(labelled[h]+fixed.get(h,0))//2 for h in labelled}
    assert sum(labelled.values())==138188079
    assert sum(fixed.values())==3789
    assert orbits=={0:61327035,1:7214130,2:532665,3:21735,4:369}
    print(f"PASS independent family-S exact-C labelled={sum(labelled.values())}")
    print(f"PASS fixed={sum(fixed.values())} orbits={sum(orbits.values())} by_h={orbits}")

if __name__=='__main__':main()
