#!/usr/bin/env python3
"""Independent census/classifier for four-edge simple graphs."""
import itertools, collections

def inv(edges):
    d=collections.Counter(v for e in edges for v in e); E=set(edges); V=tuple(d)
    tri=sum(tuple(sorted((a,b))) in E and tuple(sorted((a,c))) in E and
            tuple(sorted((b,c))) in E for a,b,c in itertools.combinations(V,3))
    q=sum(d[u]>=2 and d[v]>=2 for u,v in edges)
    return (sum(x>=2 for x in d.values()),sum(x>=3 for x in d.values()),
            sum(x>=4 for x in d.values()),tri,q)

expected={(4,0,0,0,4):210,(3,1,0,1,3):840,(3,0,0,0,2):3360,
          (3,0,0,1,3):560,(2,1,0,0,1):3360,(1,1,1,0,0):280,
          (2,0,0,0,1):5040,(2,0,0,0,0):2520,(1,1,0,0,0):1680,
          (1,0,0,0,0):2520,(0,0,0,0,0):105}
edges=list(itertools.combinations(range(8),2)); hist=collections.Counter()
for chosen in itertools.combinations(edges,4): hist[inv(chosen)]+=1
assert hist==expected,(hist,expected)
print("PASS four-edge shapes=11 labelled=20475")
