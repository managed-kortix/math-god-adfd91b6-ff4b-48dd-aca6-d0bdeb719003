#!/usr/bin/env python3
"""Deterministic exact CNF for the three residual common-C family-D cells.

The distinguished labels are fixed as `u=0`, `r=1`, `q=2`, and
`C={16,17}`.  The canonical first/second layers depend on the overlap type.

Up to exchanging the rooted pairs (u,r) and (v,q), the exact t=8 overlap has
three types: an oriented root pair with both cross-high arcs, an oriented root
pair with one cross-high arc absent, or a root-pair hole.  The formula imposes
exact degrees, exact second neighborhoods, global strict badness, C_u=C_v=C,
|S_u cap S_v|=8, one exact aggregate cell, and robust preservation for u->r
and v->q.  It also imposes the universal family-D condition that no tight low
vertex robustly witnesses both highs.  It does not impose arc minimality.
"""
import argparse
import hashlib
from pathlib import Path
from snc_cnf import CNF, equiv_and, threshold

N=18
U,R,Q=0,1,2
C=(16,17)
HIGHS={R,Q}
CELLS=((0,0,2),(0,1,1),(1,0,1))
TYPES=("oriented-both","oriented-one","root-hole")


def canonical_partitions(kind):
    """Return (v,A_u,B_u,A_v,B_v) for one of the three root-swap orbits."""
    if kind=="oriented-both":
        # u->v; u is P=S_u\\S_v; Q is the ordinary low vertex 9.
        v=3
        au=set(range(1,9))
        su={U}|au
        av=(su-{U,v})|{9}
    elif kind=="oriented-one":
        # u->v; u is P and q is Q.  Thus u does not point to q.
        v=3
        au={R,v,4,5,6,7,8,9}
        su={U}|au
        av=(su-{U,v})|{Q}
    elif kind=="root-hole":
        # u and v are each in the other's exact second layer: P={u}, Q={v}.
        v=9
        au=set(range(1,9))
        av=set(au)
    else:
        raise ValueError("unknown overlap type")
    bu=set(range(N))-({U}|au|set(C))
    bv=set(range(N))-({v}|av|set(C))
    if len(au)!=8 or len(bu)!=7 or len(av)!=8 or len(bv)!=7:
        raise RuntimeError("internal canonical partition size error")
    if R not in au or Q not in av:
        raise RuntimeError("chosen robust witness arc absent internally")
    return v,au,bu,av,bv


def exact(c,lits,k,tag):
    out=threshold(c,lits,tag)
    if k:
        c.add(out[k-1])
    if k<len(lits):
        c.add(-out[k])


def build_core():
    c=CNF()
    a=[[c.var(f"a_{i}_{j}") for j in range(N)] for i in range(N)]
    q=[[c.var(f"q_{i}_{j}") for j in range(N)] for i in range(N)]
    p={}
    for i in range(N):
        c.add(-a[i][i]); c.add(-q[i][i])
    for i in range(N):
        for j in range(i+1,N):
            c.add(-a[i][j],-a[j][i])
    for i in range(N):
        for j in range(N):
            if i==j:
                continue
            paths=[]
            for k in range(N):
                if k in (i,j):
                    continue
                z=c.var(f"p_{i}_{k}_{j}")
                p[i,k,j]=z
                paths.append(z)
                equiv_and(c,z,a[i][k],a[k][j])
            reach=c.var(f"reach_{i}_{j}")
            for z in paths:
                c.add(-z,reach)
            c.add(-reach,*paths)
            # q_ij <-> (some two-walk i-k-j) AND not(i->j).
            c.add(-q[i][j],reach)
            c.add(-q[i][j],-a[i][j])
            c.add(q[i][j],-reach,a[i][j])
    for i in range(N):
        exact(c,[a[i][j] for j in range(N) if j!=i],
              9 if i in HIGHS else 8,f"d1_{i}")
        secs=threshold(c,[q[i][j] for j in range(N) if j!=i],f"d2_{i}")
        # Strict badness: highs have d++ <= 8, lows d++ <= 7.
        c.add(-secs[8 if i in HIGHS else 7])
    holes={}
    all_holes=[]
    for i in range(N):
        for j in range(i+1,N):
            z=c.var(f"h_{i}_{j}")
            holes[i,j]=z
            all_holes.append(z)
            c.add(-z,-a[i][j]); c.add(-z,-a[j][i])
            c.add(z,a[i][j],a[j][i])
    exact(c,all_holes,7,"holes")
    return c,a,q,p,holes


def add_root_partition(c,a,q,root,A,B):
    A=set(A); B=set(B)
    if len(A)!=8 or len(B)!=7 or A&B or root in A|B or set(C)&(A|B|{root}):
        raise ValueError("invalid root partition")
    if {root}|A|B|set(C)!=set(range(N)):
        raise ValueError("root partition does not cover the vertex set")
    for j in range(N):
        c.add(a[root][j] if j in A else -a[root][j])
        c.add(q[root][j] if j in B else -q[root][j])
    # C is exact inaccessible, not merely outside the first layer.
    for z in C:
        c.add(-q[root][z])
    return A,B


def add_preserved_second_layer(c,a,root,deleted,A,B):
    """N++_{D-deleted}(root)=N++_D(root)=B for a fixed rooted row.

    With the exact root partition, deletion cannot create exact second
    neighbors.  Preservation is therefore exactly alternate A-minus-deleted
    support for every b in B.
    """
    for b in sorted(B):
        c.add(*[a[k][b] for k in sorted(A-{deleted})])


def add_not_preserved(c,a,root,deleted,A,B,tag):
    """Encode failure of N++ preservation after deleting an outneighbor.

    Some b in the exact second layer has deleted as an A-predecessor and has no
    other A-predecessor.  Selector gates make the existential explicit.
    """
    selectors=[]
    for b in sorted(B):
        s=c.var(f"fail_{tag}_{b}")
        selectors.append(s)
        c.add(-s,a[deleted][b])
        for k in sorted(A-{deleted}):
            c.add(-s,-a[k][b])
    c.add(*selectors)


def add_no_shared_low(c,a,q):
    """No low vertex is a robust witness for both high vertices r and q.

    A low x can robustly witness deletion of a high d exactly when x is tight
    (d++(x)=7), x->d, and every old exact second neighbor has an alternate
    first-layer predecessor other than d.  We build exact gates for these
    properties and forbid their conjunction at each low x.
    """
    lows=sorted(set(range(N))-HIGHS)
    all_vertices=set(range(N))
    for x in lows:
        tight=threshold(c,[q[x][j] for j in range(N) if j!=x],f"robust_tight_{x}")[6]
        for d in (R,Q):
            gate=c.var(f"robust_{x}_{d}")
            # gate <-> tight AND a[x,d] AND every required alternate-support
            # disjunction.
            # The deleted high d itself is removed from the post-deletion
            # vertex set and therefore is not a preservation target.
            requirements=[]
            for b in sorted(all_vertices-{x,d}):
                support=c.var(f"alt_{x}_{d}_{b}")
                paths=[]
                for k in sorted(all_vertices-{x,d,b}):
                    p=c.var(f"altpath_{x}_{d}_{k}_{b}")
                    paths.append(p)
                    equiv_and(c,p,a[x][k],a[k][b])
                for p in paths:
                    c.add(-p,support)
                c.add(-support,*paths)
                req=c.var(f"req_{x}_{d}_{b}")
                # req <-> (not q[x,b]) OR support.
                c.add(-req,-q[x][b],support)
                c.add(req,q[x][b])
                c.add(req,-support)
                requirements.append(req)
            c.add(-gate,tight)
            c.add(-gate,a[x][d])
            for req in requirements:
                c.add(-gate,req)
            c.add(gate,-tight,-a[x][d],*[-req for req in requirements])
        c.add(-c.var(f"robust_{x}_{R}"),-c.var(f"robust_{x}_{Q}"))


def build(cell,kind):
    if tuple(cell) not in CELLS:
        raise ValueError("cell must be one of the three residual cells")
    if kind not in TYPES:
        raise ValueError("unknown overlap type")
    x,z,h=map(int,cell)
    v,au,bu,av,bv=canonical_partitions(kind)
    c,a,q,p,holes=build_core()

    # Both exact rooted rows and their selected robust arcs.
    add_root_partition(c,a,q,U,au,bu)
    add_root_partition(c,a,q,v,av,bv)
    c.add(a[U][R])
    c.add(a[v][Q])

    # Both selected deletion-witness systems.  The explicit cross failures are
    # redundant consequences of the universal disjoint-family gate, but retain
    # a direct local audit whenever the corresponding cross-high arc exists.
    add_preserved_second_layer(c,a,U,R,au,bu)
    add_preserved_second_layer(c,a,v,Q,av,bv)
    if Q in au:
        add_not_preserved(c,a,U,Q,au,bu,"u_q")
    if R in av:
        add_not_preserved(c,a,v,R,av,bv,"v_r")
    add_no_shared_low(c,a,q)

    # Exact synchronized aggregate cell.  U=S_u union S_v and
    # W=V\(C union U); T=V\C.
    SU={U}|au
    SV={v}|av
    if len(SU&SV)!=8:
        raise RuntimeError("internal canonical t=8 error")
    union=SU|SV
    W=set(range(N))-(set(C)|union)
    T=set(range(N))-set(C)
    c_to_w=[]
    c_w_holes=[]
    for cc in C:
        for w in sorted(W):
            c_to_w.append(a[cc][w])
            c_w_holes.append(holes[min(cc,w),max(cc,w)])
    t_holes=[holes[i,j] for i in sorted(T) for j in sorted(T) if i<j]
    exact(c,c_to_w,x,"cell_x")
    exact(c,c_w_holes,z,"cell_z")
    exact(c,t_holes,h,"cell_h")

    meta={"cell":tuple(cell),"kind":kind,"u":U,"v":v,
          "r":R,"q":Q,"A_u":tuple(sorted(au)),"B_u":tuple(sorted(bu)),
          "A_v":tuple(sorted(av)),"B_v":tuple(sorted(bv)),
          "C":C,"S_intersection":tuple(sorted(SU&SV)),
          "S_union":tuple(sorted(union)),"W":tuple(sorted(W))}
    return c,a,q,meta


def write_cnf(c,path):
    with open(path,"w",encoding="ascii",newline="\n") as f:
        for name,num in c.names.items():
            f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for clause in c.clauses:
            f.write(" ".join(map(str,clause))+" 0\n")


def parse_cell(text):
    try:
        z=tuple(map(int,text.split(",")))
    except ValueError as e:
        raise argparse.ArgumentTypeError("cell must be x,z,h") from e
    if z not in CELLS:
        raise argparse.ArgumentTypeError("not a residual cell")
    return z


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cell",type=parse_cell,required=True)
    p.add_argument("--kind",choices=TYPES,required=True)
    p.add_argument("--output",type=Path,required=True)
    x=p.parse_args()
    c,_,_,meta=build(x.cell,x.kind)
    write_cnf(c,x.output)
    raw=x.output.read_bytes()
    print(f"PASS vars={len(c.names)} clauses={len(c.clauses)} sha256={hashlib.sha256(raw).hexdigest()}")
    print("meta="+repr(meta))

if __name__=="__main__":
    main()
