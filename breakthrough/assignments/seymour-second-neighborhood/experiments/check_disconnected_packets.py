#!/usr/bin/env python3
"""Transparent saturated packet census for the three disconnected shapes."""
import itertools

SHAPES={
 "p4_edge":(6,{(0,1),(1,2),(2,3),(4,5)},3),
 "two_p3":(6,{(0,1),(1,2),(3,4),(4,5)},2),
 "p3_two_edges":(7,{(0,1),(1,2),(3,4),(5,6)},2),
}

def oriented(bits,pairs,u,v):
    i=pairs.index(tuple(sorted((u,v))))
    return bits[i] if u<v else not bits[i]

def states(n,holes,bits):
    pairs=[p for p in itertools.combinations(range(n),2) if p not in holes]
    out=[]
    for I in itertools.combinations(range(n),2):
      rest=set(range(n))-set(I)
      for rt in itertools.chain.from_iterable(itertools.combinations(rest,k) for k in range(len(rest)+1)):
        R=set(rt);ok=True
        for t in I:
          q=sum(tuple(sorted((t,s))) in holes for s in R)
          if q<1:ok=False;break
          # Forced positive arcs into R.
          if any(tuple(sorted((t,s))) not in holes and not oriented(bits,pairs,t,s) for s in R):ok=False;break
          # Exact degree leaves at most q-1 support arcs outward beyond R.
          outside=set(range(n))-R-{t}
          used=sum(tuple(sorted((t,s))) not in holes and oriented(bits,pairs,t,s) for s in outside)
          if used>q-1:ok=False;break
        if ok:out.append((I,tuple(sorted(R))))
    return out

def main():
 for name,(n,holes,want) in SHAPES.items():
  pairs=[p for p in itertools.combinations(range(n),2) if p not in holes]
  maximum=0;multiplicity=0
  for bits in itertools.product((False,True),repeat=len(pairs)):
    st=states(n,holes,bits);labels=[i for i,_ in st]
    multiplicity=max(multiplicity,max((labels.count(i) for i in set(labels)),default=0))
    maximum=max(maximum,len(set(labels)))
  assert maximum==want and multiplicity<=1
  print(f"PASS {name} orientations={1<<len(pairs)} maximum={maximum} cut_multiplicity={multiplicity}")

if __name__=="__main__":main()
