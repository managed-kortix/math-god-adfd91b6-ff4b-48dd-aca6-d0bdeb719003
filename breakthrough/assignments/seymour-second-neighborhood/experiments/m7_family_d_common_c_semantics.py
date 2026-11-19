#!/usr/bin/env python3
"""Direct graph-semantic audit for common-C family-D SAT assignments."""
from m7_family_d_common_c_cnf import N,U,R,Q,C,HIGHS,canonical_partitions

def n1(arcs,u,vertices=None):
    if vertices is None: vertices=set(range(N))
    return {v for v in vertices if (u,v) in arcs}

def n2(arcs,u,vertices=None):
    if vertices is None: vertices=set(range(N))
    one=n1(arcs,u,vertices)
    return {v for v in vertices-{u}-one if any((u,k) in arcs and (k,v) in arcs for k in vertices-{u,v})}

def holes(arcs):
    return {(i,j) for i in range(N) for j in range(i+1,N) if (i,j) not in arcs and (j,i) not in arcs}

def partition(arcs,root):
    A=n1(arcs,root); B=n2(arcs,root); Cset=set(range(N))-({root}|A|B)
    return A,B,Cset

def preserved(arcs,root,deleted):
    full=n2(arcs,root)
    vertices=set(range(N))-{deleted}
    reduced={(i,j) for i,j in arcs if i!=deleted and j!=deleted}
    # The deleted first neighbor is absent from the reduced vertex set, so the
    # exact equality is between the surviving parts of the two neighborhoods.
    return n2(reduced,root,vertices)==full-{deleted}

def robust_low(arcs,root,deleted):
    vertices=set(range(N))
    return (len(n1(arcs,root,vertices))==len(n2(arcs,root,vertices))+1 and
            (root,deleted) in arcs and preserved(arcs,root,deleted))

def semantic_check(arcs,cell,kind):
    if any((i,i) in arcs for i in range(N)): raise RuntimeError("loop")
    if any((i,j) in arcs and (j,i) in arcs for i in range(N) for j in range(i+1,N)): raise RuntimeError("digon")
    out=[n1(arcs,i) for i in range(N)]; sec=[n2(arcs,i) for i in range(N)]
    expected=[9 if i in HIGHS else 8 for i in range(N)]
    if [len(x) for x in out]!=expected: raise RuntimeError("wrong outdegrees")
    if any(len(sec[i])>=len(out[i]) for i in range(N)): raise RuntimeError("not globally bad")
    hs=holes(arcs)
    if len(hs)!=7: raise RuntimeError("wrong hole count")
    Au,Bu,Cu=partition(arcs,U)
    v,expected_au,expected_bu,expected_av,expected_bv=canonical_partitions(kind)
    Av,Bv,Cv=partition(arcs,v)
    if Au!=expected_au or Bu!=expected_bu or Cu!=set(C): raise RuntimeError("wrong u partition")
    if Av!=expected_av or Bv!=expected_bv or Cv!=set(C): raise RuntimeError("wrong v partition")
    if R not in Au or Q not in Av: raise RuntimeError("selected witness arcs absent")
    if len(({U}|Au)&({v}|Av))!=8: raise RuntimeError("t is not eight")
    if not preserved(arcs,U,R) or not preserved(arcs,v,Q): raise RuntimeError("chosen robustness absent")
    if Q in Au and preserved(arcs,U,Q): raise RuntimeError("u is also a robust low witness for q")
    if R in Av and preserved(arcs,v,R): raise RuntimeError("v is also a robust low witness for r")
    for low in sorted(set(range(N))-HIGHS):
        if robust_low(arcs,low,R) and robust_low(arcs,low,Q):
            raise RuntimeError(f"shared low robust witness {low}")
    union=({U}|Au)|({v}|Av); W=set(range(N))-(set(C)|union); T=set(range(N))-set(C)
    x=sum((cc,w) in arcs for cc in C for w in W)
    z=sum(tuple(sorted((cc,w))) in hs for cc in C for w in W)
    h=sum((i,j) in hs for i in T for j in T if i<j)
    if (x,z,h)!=tuple(cell): raise RuntimeError(f"wrong cell {(x,z,h)}")
    return {"cell":tuple(cell),"kind":kind,"v":v,
            "A_v":sorted(Av),"B_v":sorted(Bv),"C":list(C),"W":sorted(W),
            "holes":sorted(hs),"outdegrees":expected,
            "second_degrees":[len(s) for s in sec]}
