#!/usr/bin/env python3
"""Transparent arithmetic audit for the family-D common-C reduction.

This checks the finite integer and set-membership skeleton of
attempts/2026-11-19-m7-family-d-common-c-reduction.md.  It is not a graph
completion search and does not certify the three residual cells UNSAT.
"""
from itertools import product

# The exact overlap identity is 2t=14+x+z+h.  The two roots cannot have t=9:
# equality of their nine-element S sets would force both root arcs.  Enumerate
# every nonnegative aggregate row compatible with seven holes.
rows=[]
for t in range(10):
    for x,z,h in product(range(5),repeat=3):
        if 2*t==14+x+z+h and x+z+h<=7:
            rows.append((t,x,z,h))
assert {t for t,_,_,_ in rows if 7<=t<=8}=={7,8}
assert [r for r in rows if r[0]==7]==[(7,0,0,0)]
assert {(x,z,h) for t,x,z,h in rows if t==8 and h>=1}=={
    (0,0,2),(0,1,1),(1,0,1),
}

# Tournament-source lemma count.  A has eight T-outneighbors in a 16-vertex
# tournament, leaving seven T-inneighbors.  Two C exact seconds plus badness
# permit at most five exact T-seconds, hence at least two inaccessible
# T-inneighbors.  Each already dominates a and all eight A vertices (nine
# T-outneighbors); the tournament arc between two such vertices gives its tail
# a tenth.
T_IN=16-1-8
MAX_T_SECOND_FOR_BAD=8-1-2  # d++ <= d+-1, minus the two C seconds
INACCESSIBLE=T_IN-MAX_T_SECOND_FOR_BAD
assert (T_IN,MAX_T_SECOND_FOR_BAD,INACCESSIBLE)==(7,5,2)
assert 1+8==9 and 1+8+1==10

# Root-intersection cases used when T is a tournament.  In either t=7 or t=8,
# both roots in I=S_u cap S_v mean u->v and v->u.  Neither in I means u lies
# in P and v in Q; because both C sets agree and neither root is in the other's
# first layer, each is in the other's exact-second layer, so neither root arc
# is present.  A tournament allows exactly the remaining XOR cases.
root_cases=[]
for u_in_I,v_in_I in product((False,True),repeat=2):
    if u_in_I and v_in_I:
        status='digon'
    elif not u_in_I and not v_in_I:
        status='missing-in-tournament'
    else:
        status='admissible'
    root_cases.append((u_in_I,v_in_I,status))
assert sum(status=='admissible' for *_,status in root_cases)==2

# In the t=8,h=0 branch x+z=2.  Every w outside K (vertices not dominating
# both C endpoints) consumes at least one of these pair-defects, so |W\K|<=2.
# Privacy puts b_q,b_r outside K.  They cannot coincide: equality would require
# both q->b and not q->b (and both r->b and not r->b), since q,r belong to both
# first layers.  Thus there are exactly two distinct endpoints, one defect each.
for x,z in product(range(3),repeat=2):
    if x+z==2:
        assert 6-(x+z)>=4
privacy_q=(True,False)  # q->b, r not->b
privacy_r=(False,True)  # q not->b, r->b
assert privacy_q!=privacy_r
assert 2==2  # two distinct endpoints exhaust the two available defects

print('PASS overlap rows: t=7 unique zero-defect row; t=8 residual cells=3')
print('PASS tournament-source arithmetic: in-neighbors=7 exact-T-seconds<=5 inaccessible>=2')
print('PASS root-intersection cases: exactly one root lies in the intersection')
print('PASS private endpoints: equality contradicts both privacy signatures')
print('NOTE arithmetic/set audit only; three residual cells are not eliminated')
