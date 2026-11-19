#!/usr/bin/env python3
"""Producer-independent byte reconstruction of common-C family-D CNFs.

This checker imports neither the producer nor snc_cnf.  It separately builds
all variables and clauses, hostile-parses the supplied DIMACS, and requires
byte equality.  Its small counter implementation is truth-tabled independently.
"""
import argparse
import hashlib
import itertools
from pathlib import Path

N=18
U,R,Q=0,1,2
C=(16,17)
HIGHS={R,Q}
CELLS=((0,0,2),(0,1,1),(1,0,1))
TYPES=("oriented-both","oriented-one","root-hole")

def canonical_partitions(kind):
    if kind=="oriented-both":
        v=3; au=set(range(1,9)); su={U}|au; av=(su-{U,v})|{9}
    elif kind=="oriented-one":
        v=3; au={R,v,4,5,6,7,8,9}; su={U}|au; av=(su-{U,v})|{Q}
    elif kind=="root-hole":
        v=9; au=set(range(1,9)); av=set(au)
    else: raise ValueError("unknown overlap type")
    bu=set(range(N))-({U}|au|set(C)); bv=set(range(N))-({v}|av|set(C))
    return v,au,bu,av,bv

class Formula:
    def __init__(self): self.names={}; self.clauses=[]
    def var(self,name):
        if name not in self.names: self.names[name]=len(self.names)+1
        return self.names[name]
    def add(self,*z): self.clauses.append(tuple(z))

def and_gate(c,y,x,z):
    c.add(-y,x); c.add(-y,z); c.add(y,-x,-z)

def count(c,inputs,tag):
    prev=[]
    for i,x in enumerate(inputs,1):
        cur=[]
        for t in range(1,i+1):
            y=c.var(f"cnt_{tag}_{i}_{t}"); cur.append(y)
            u=prev[t-1] if t<=len(prev) else None
            v=prev[t-2] if t>=2 else True
            if u is not None: c.add(-u,y)
            if v is True: c.add(-x,y)
            else: c.add(-x,-v,y)
            if u is None:
                if v is True: c.add(-y,x)
                else: c.add(-y,x); c.add(-y,v)
            elif v is True:
                c.add(-y,u,x)
            else:
                c.add(-y,u,x); c.add(-y,u,v)
        prev=cur
    return prev

def exact(c,lits,k,tag):
    out=count(c,lits,tag)
    if k: c.add(out[k-1])
    if k<len(lits): c.add(-out[k])

def audit_counter():
    for n in range(1,9):
        c=Formula(); xs=[c.var(f"x_{i}") for i in range(n)]; ys=count(c,xs,"audit")
        for bits in itertools.product((False,True),repeat=n):
            values={xs[i]:bits[i] for i in range(n)}
            for name,var in c.names.items():
                if name.startswith("cnt_audit_"):
                    _,_,i,t=name.split("_")
                    values[var]=sum(bits[:int(i)])>=int(t)
            if not all(any(values[abs(z)]==(z>0) for z in clause) for clause in c.clauses):
                raise RuntimeError("counter clause truth-table failure")
            if any(values[y]!=(sum(bits)>=k) for k,y in enumerate(ys,1)):
                raise RuntimeError("counter output truth-table failure")

def core():
    c=Formula()
    a=[[c.var(f"a_{i}_{j}") for j in range(N)] for i in range(N)]
    q=[[c.var(f"q_{i}_{j}") for j in range(N)] for i in range(N)]
    for i in range(N): c.add(-a[i][i]); c.add(-q[i][i])
    for i in range(N):
        for j in range(i+1,N): c.add(-a[i][j],-a[j][i])
    for i in range(N):
        for j in range(N):
            if i==j: continue
            paths=[]
            for k in range(N):
                if k in (i,j): continue
                z=c.var(f"p_{i}_{k}_{j}"); paths.append(z); and_gate(c,z,a[i][k],a[k][j])
            reach=c.var(f"reach_{i}_{j}")
            for z in paths: c.add(-z,reach)
            c.add(-reach,*paths)
            c.add(-q[i][j],reach); c.add(-q[i][j],-a[i][j]); c.add(q[i][j],-reach,a[i][j])
    for i in range(N):
        exact(c,[a[i][j] for j in range(N) if j!=i],9 if i in HIGHS else 8,f"d1_{i}")
        secs=count(c,[q[i][j] for j in range(N) if j!=i],f"d2_{i}")
        c.add(-secs[8 if i in HIGHS else 7])
    holes={}; all_holes=[]
    for i in range(N):
        for j in range(i+1,N):
            z=c.var(f"h_{i}_{j}"); holes[i,j]=z; all_holes.append(z)
            c.add(-z,-a[i][j]); c.add(-z,-a[j][i]); c.add(z,a[i][j],a[j][i])
    exact(c,all_holes,7,"holes")
    return c,a,q,holes

def root_row(c,a,q,root,A,B):
    A=set(A); B=set(B)
    for j in range(N):
        c.add(a[root][j] if j in A else -a[root][j])
        c.add(q[root][j] if j in B else -q[root][j])
    for z in C: c.add(-q[root][z])

def preserve(c,a,deleted,A,B):
    for b in sorted(B): c.add(*[a[k][b] for k in sorted(set(A)-{deleted})])

def fail(c,a,deleted,A,B,tag):
    ss=[]
    for b in sorted(B):
        s=c.var(f"fail_{tag}_{b}"); ss.append(s); c.add(-s,a[deleted][b])
        for k in sorted(set(A)-{deleted}): c.add(-s,-a[k][b])
    c.add(*ss)

def no_shared_low(c,a,q):
    lows=sorted(set(range(N))-HIGHS); all_vertices=set(range(N))
    for x in lows:
        tight=count(c,[q[x][j] for j in range(N) if j!=x],f"robust_tight_{x}")[6]
        for d in (R,Q):
            gate=c.var(f"robust_{x}_{d}"); requirements=[]
            for b in sorted(all_vertices-{x,d}):
                support=c.var(f"alt_{x}_{d}_{b}"); paths=[]
                for k in sorted(all_vertices-{x,d,b}):
                    p=c.var(f"altpath_{x}_{d}_{k}_{b}"); paths.append(p)
                    and_gate(c,p,a[x][k],a[k][b])
                for p in paths: c.add(-p,support)
                c.add(-support,*paths)
                req=c.var(f"req_{x}_{d}_{b}")
                c.add(-req,-q[x][b],support); c.add(req,q[x][b]); c.add(req,-support)
                requirements.append(req)
            c.add(-gate,tight); c.add(-gate,a[x][d])
            for req in requirements: c.add(-gate,req)
            c.add(gate,-tight,-a[x][d],*[-req for req in requirements])
        c.add(-c.var(f"robust_{x}_{R}"),-c.var(f"robust_{x}_{Q}"))

def reconstruct(cell,kind):
    x,z,h=cell; v,au,bu,av,bv=canonical_partitions(kind)
    c,a,q,holes=core()
    root_row(c,a,q,U,au,bu); root_row(c,a,q,v,av,bv)
    c.add(a[U][R]); c.add(a[v][Q])
    preserve(c,a,R,au,bu); preserve(c,a,Q,av,bv)
    if Q in au: fail(c,a,Q,au,bu,"u_q")
    if R in av: fail(c,a,R,av,bv,"v_r")
    no_shared_low(c,a,q)
    SU={U}|au; SV={v}|av; union=SU|SV; W=set(range(N))-(set(C)|union); T=set(range(N))-set(C)
    exact(c,[a[cc][w] for cc in C for w in sorted(W)],x,"cell_x")
    exact(c,[holes[min(cc,w),max(cc,w)] for cc in C for w in sorted(W)],z,"cell_z")
    exact(c,[holes[i,j] for i in sorted(T) for j in sorted(T) if i<j],h,"cell_h")
    meta={"v":v,"A_u":tuple(sorted(au)),"B_u":tuple(sorted(bu)),
          "A_v":tuple(sorted(av)),"B_v":tuple(sorted(bv)),"W":tuple(sorted(W))}
    return c,meta

def serialize(c):
    raw="".join(f"c var {num} {name}\n" for name,num in c.names.items())
    raw+=f"p cnf {len(c.names)} {len(c.clauses)}\n"
    raw+="".join(" ".join(map(str,z))+" 0\n" for z in c.clauses)
    return raw.encode("ascii")

def hostile_parse(raw):
    try: lines=raw.decode("ascii").splitlines()
    except UnicodeDecodeError as e: raise ValueError("non-ASCII CNF") from e
    names=[]; clauses=[]; header=None
    for line_no,line in enumerate(lines,1):
        if line.startswith("c var "):
            if header is not None: raise ValueError("variable map after header")
            f=line.split(maxsplit=3)
            if len(f)!=4 or int(f[2])!=len(names)+1 or f[3] in names: raise ValueError("bad variable map")
            names.append(f[3]); continue
        if line.startswith("p "):
            if header is not None: raise ValueError("duplicate header")
            f=line.split()
            if len(f)!=4 or f[:2]!=["p","cnf"]: raise ValueError("bad header")
            header=tuple(map(int,f[2:])); continue
        if header is None: raise ValueError(f"unexpected pre-header line {line_no}")
        vals=tuple(map(int,line.split()))
        if not vals or vals[-1]!=0 or 0 in vals[:-1]: raise ValueError("bad clause line")
        clauses.append(vals[:-1])
    if header!=(len(names),len(clauses)): raise ValueError("dimension mismatch")
    if any(abs(z)>len(names) for clause in clauses for z in clause): raise ValueError("literal out of range")
    return names,clauses

def parse_cell(text):
    try: z=tuple(map(int,text.split(",")))
    except ValueError as e: raise argparse.ArgumentTypeError("cell must be x,z,h") from e
    if z not in CELLS: raise argparse.ArgumentTypeError("not a residual cell")
    return z

def main():
    p=argparse.ArgumentParser(); p.add_argument("cnf",type=Path)
    p.add_argument("--cell",type=parse_cell,required=True); p.add_argument("--kind",choices=TYPES,required=True)
    x=p.parse_args(); audit_counter(); c,meta=reconstruct(x.cell,x.kind)
    raw=x.cnf.read_bytes(); names,clauses=hostile_parse(raw); expected=serialize(c)
    if names!=list(c.names) or clauses!=c.clauses or raw!=expected:
        raise RuntimeError("CNF differs from independent reconstruction")
    print(f"PASS independent common-C CNF vars={len(names)} clauses={len(clauses)} sha256={hashlib.sha256(raw).hexdigest()}")
    print("meta="+repr(meta))

if __name__=="__main__": main()
