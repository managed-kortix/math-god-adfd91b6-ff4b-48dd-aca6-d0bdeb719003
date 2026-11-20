#!/usr/bin/env python3
"""Exact regression only; general embedding lemma is proved in accompanying note."""
def mul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
checks=0
for r in range(1,5):
    for d in range(1,12):
        m=2*r
        j=[[0]*m for _ in range(m)]
        for k in range(r):
            j[2*k][2*k+1]=-d
            j[2*k+1][2*k]=1
        expected=[[-d if a==b else 0 for b in range(m)] for a in range(m)]
        if mul(j,j)!=expected: raise RuntimeError((r,d))
        checks+=1
pairs=[(g,m) for g in range(1,5) for m in range(1,5) if g*m<=4 and m%2==0]
if pairs!=[(1,2),(1,4),(2,2)]: raise RuntimeError(pairs)
print('PASS integer block identities:',checks)
print('real-field support pairs:',pairs)
