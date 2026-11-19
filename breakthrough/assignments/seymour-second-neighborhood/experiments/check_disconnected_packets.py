#!/usr/bin/env python3
"""Independent exact packet census for three disconnected four-hole shapes.

For every orientation of the present support pairs, inaccessible pair I, and
support cut R=S intersect H, this checks the forced crossing orientations and
the exact outside-S row capacity.  It additionally verifies that some
inaccessible endpoint is saturated on the support.  For that endpoint t,
with Q the holes from t into R and W its support outneighbors outside S,

    N+(t) = (S minus Q) union W,
    S = (N+(t) minus W) union Q.

Thus the fixed global row and the checked unique cut reconstruct the full S,
not merely S intersect H.  A packet label consequently supports at most one
source.  Bitsets make the complete 2^17 census deterministic and fast.
"""
import itertools

SHAPES={
 "p4_edge":{
   "n":6,"holes":{(0,1),(1,2),(2,3),(4,5)},"maximum":3,"accepted":640,
   "labels":{(0,2),(1,2),(1,3),(1,4),(1,5),(2,4),(2,5)},
   "maximum_families":{frozenset(((0,2),(1,4),(1,5))),frozenset(((1,3),(2,4),(2,5)))},
 },
 "two_p3":{
   "n":6,"holes":{(0,1),(1,2),(3,4),(4,5)},"maximum":2,"accepted":640,
   "labels":{(0,4),(1,3),(1,4),(1,5),(2,4)},
   "maximum_families":{frozenset(((1,4),x)) for x in ((0,4),(1,3),(1,5),(2,4))},
 },
 "p3_two_edges":{
   "n":7,"holes":{(0,1),(1,2),(3,4),(5,6)},"maximum":2,"accepted":8192,
   "labels":{(1,3),(1,4),(1,5),(1,6)},
   "maximum_families":{frozenset(((1,3),(1,4))),frozenset(((1,5),(1,6)))},
 },
}

def variable_masks(m):
    total=1<<m
    universe=(1<<total)-1
    masks=[]
    for i in range(m):
        block=1<<i; one=(1<<block)-1; mask=0
        for start in range(block,total,2*block): mask |= one<<start
        masks.append(mask)
    return universe,masks

def literal_mask(u,v,pair_index,masks,universe):
    edge=tuple(sorted((u,v))); truth=masks[pair_index[edge]]
    return truth if u<v else universe^truth

def count_masks(literals,universe):
    counts=[universe]
    for lit in literals:
        false=universe^lit
        nxt=[0]*(len(counts)+1)
        for k,mask in enumerate(counts):
            nxt[k] |= mask&false
            nxt[k+1] |= mask&lit
        counts=nxt
    return counts

def census(spec):
    n=spec["n"]; holes=spec["holes"]
    pairs=[p for p in itertools.combinations(range(n),2) if p not in holes]
    index={p:i for i,p in enumerate(pairs)}
    universe,masks=variable_masks(len(pairs))
    cuts={}
    for I in itertools.combinations(range(n),2):
      rest=set(range(n))-set(I)
      for rt in itertools.chain.from_iterable(itertools.combinations(rest,k) for k in range(len(rest)+1)):
        R=set(rt); accepted=universe; equality=[]; valid=True
        for t in I:
          Q={s for s in R if tuple(sorted((t,s))) in holes}; q=len(Q)
          if q<1: valid=False;break
          for s in R:
            if tuple(sorted((t,s))) not in holes:
              accepted &= literal_mask(t,s,index,masks,universe)
          outside=set(range(n))-R-{t}
          outgoing=[literal_mask(t,s,index,masks,universe) for s in outside
                    if tuple(sorted((t,s))) not in holes]
          counts=count_masks(outgoing,universe); bound=q-1
          accepted &= sum(counts[:bound+1])
          equality.append(counts[bound])
        if not valid: continue
        # Some endpoint must use all q-1 available outside-S slots on the
        # support; this is the exact reconstruction witness described above.
        accepted &= equality[0] | equality[1]
        if accepted: cuts[I,tuple(sorted(R))]=accepted

    by_label={}
    for (label,R),mask in cuts.items():
        previous=by_label.get(label,0)
        if previous&mask:
            raise RuntimeError(f"nonunique support cut for label {label}")
        by_label[label]=previous|mask
    labels=set(by_label)
    active=[]; ordered=sorted(labels)
    for size in range(1,len(ordered)+1):
      for subset in itertools.combinations(ordered,size):
        common=universe
        for label in subset: common &= by_label[label]
        if common: active.append((frozenset(subset),common))
    maximum=max(map(lambda x:len(x[0]),active),default=0)
    families={family for family,_ in active if len(family)==maximum}
    accepted=sum(mask.bit_count() for mask in cuts.values())
    return len(pairs),labels,maximum,families,accepted

def require(condition,message):
    if not condition: raise RuntimeError(message)

def main():
 for name,spec in SHAPES.items():
  m,labels,maximum,families,accepted=census(spec)
  require(labels==spec["labels"],f"{name}: packet labels changed: {sorted(labels)}")
  require(maximum==spec["maximum"],f"{name}: maximum {maximum}")
  require(families==spec["maximum_families"],f"{name}: maximum families changed")
  require(accepted==spec["accepted"],f"{name}: accepted-state count {accepted}")
  print(f"PASS {name} orientations={1<<m} accepted={accepted} "
        f"maximum_sources={maximum} cut_multiplicity=1 saturated=all")

if __name__=="__main__":main()
