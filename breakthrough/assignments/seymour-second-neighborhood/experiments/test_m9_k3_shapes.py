#!/usr/bin/env python3
"""Independent census of all three-edge graphs on six vertices."""
import itertools, collections

edges=list(itertools.combinations(range(6),2)); hist=collections.Counter()
for chosen in itertools.combinations(edges,3):
    d=[0]*6
    for u,v in chosen: d[u]+=1; d[v]+=1
    hist[tuple(sorted(d,reverse=True))]+=1
expected={(1,1,1,1,1,1):15,(2,1,1,1,1,0):180,
          (2,2,1,1,0,0):180,(3,1,1,1,0,0):60,
          (2,2,2,0,0,0):20}
assert hist==expected,(hist,expected)
print("PASS three-edge shapes=5 labelled=455")
