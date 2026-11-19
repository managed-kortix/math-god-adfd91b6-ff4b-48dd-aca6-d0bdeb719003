#!/usr/bin/env python3
"""Emit exact-badness CNF pilots for canonical family-S type rows.

This is deliberately separate from arc minimality.  It fixes one canonical
C-incidence type row, exact degrees (highs 1,2 have 9; all others 8), exactly
seven holes, the shared-low root and its simultaneous robustness, and exact
SNC badness d++(v)<d+(v) for every vertex.  No vertex/arc-minimality clauses
are included.

The default subset is h=4 for backward compatibility.  Use --h to select any
residual-T-hole cell, --all for all 13,117 canonical rows, or --index for one
row in the selected ordered subset.
"""
import argparse,hashlib,json
from pathlib import Path
from m7_family_s_type_rows import rows,swap_row
from snc_cnf import CNF,equiv_and,threshold

N=18; W=0; A=set(range(1,9)); B=set(range(9,16)); C=(16,17); HIGHS={1,2}
ATYPES=((0,0),(0,1),(1,0),(1,1))

def exact(c,lits,k,tag):
    out=threshold(c,lits,tag)
    if k: c.add(out[k-1])
    if k<len(lits): c.add(-out[k])

def canonical_rows(all_rows=False,h=4):
    data=sorted({min(x,swap_row(x)) for x in rows()})
    return data if all_rows else [x for x in data if x[-1]==h]

def build_base():
    c=CNF();a=[[c.var(f'a_{i}_{j}') for j in range(N)]for i in range(N)]
    q=[[c.var(f'q_{i}_{j}') for j in range(N)]for i in range(N)]
    for i in range(N):c.add(-a[i][i]);c.add(-q[i][i])
    for i in range(N):
        for j in range(i+1,N):c.add(-a[i][j],-a[j][i])
    for i in range(N):
        for j in range(N):
            if i==j:continue
            paths=[]
            for k in range(N):
                if k in (i,j):continue
                p=c.var(f'p_{i}_{k}_{j}');paths.append(p);equiv_and(c,p,a[i][k],a[k][j])
            reach=c.var(f'reach_{i}_{j}')
            for p in paths:c.add(-p,reach)
            c.add(-reach,*paths)
            c.add(-q[i][j],reach);c.add(-q[i][j],-a[i][j]);c.add(q[i][j],-reach,a[i][j])
    for i in range(N):
        exact(c,[a[i][j]for j in range(N)if j!=i],9 if i in HIGHS else 8,f'd1_{i}')
        # Exact badness: d2 <= 8 for highs, <=7 for lows.
        secs=threshold(c,[q[i][j]for j in range(N)if j!=i],f'd2_{i}')
        c.add(-secs[8 if i in HIGHS else 7])
    holes=[]
    for i in range(N):
        for j in range(i+1,N):
            h=c.var(f'h_{i}_{j}');holes.append(h)
            c.add(-h,-a[i][j]);c.add(-h,-a[j][i]);c.add(h,a[i][j],a[j][i])
    exact(c,holes,7,'holes')
    # Root row and simultaneous robustness after deleting each high.
    for j in range(N):c.add(a[W][j] if j in A else -a[W][j])
    for b in B:
        c.add(*[a[x][b]for x in sorted(A-{1})])
        c.add(*[a[x][b]for x in sorted(A-{2})])
    return c,a,q

def add_row(c,a,row):
    # Exact canonical C-incidence representative.  Labels 3,...,8 and
    # 9,...,15 realize the row's sorted multiplicity representatives.
    state,distinguished,a_counts,b_counts,h=row
    atypes=list(distinguished)+sum(([t]*n for t,n in enumerate(a_counts)),[])
    for u,t in zip([0,1,2]+list(range(3,9)),atypes):
        for k,z in enumerate(C):
            if ATYPES[t][k]:c.add(-a[u][z]);c.add(-a[z][u])
            else:c.add(a[z][u]);c.add(-a[u][z])
    btypes=sum(([t]*n for t,n in enumerate(b_counts)),[])
    for b,t in zip(sorted(B),btypes):
        for k,z in enumerate(C):
            x=(t//3,t%3)[k]
            if x==0:c.add(a[z][b]);c.add(-a[b][z])
            elif x==1:c.add(a[b][z]);c.add(-a[z][b])
            else:c.add(-a[b][z]);c.add(-a[z][b])
    if state=='M':c.add(-a[16][17]);c.add(-a[17][16])
    elif state=='01':c.add(a[16][17]);c.add(-a[17][16])
    else:c.add(a[17][16]);c.add(-a[16][17])

def build(row):
    c,a,q=build_base();add_row(c,a,row);return c,a,q

def write_cnf(c,path):
    with open(path,'w',encoding='ascii',newline='\n')as f:
        for name,num in c.names.items():f.write(f'c var {num} {name}\n')
        f.write(f'p cnf {len(c.names)} {len(c.clauses)}\n')
        for z in c.clauses:f.write(' '.join(map(str,z))+' 0\n')

def main():
    p=argparse.ArgumentParser();p.add_argument('--all',action='store_true')
    p.add_argument('--h',type=int,choices=range(5),default=4)
    p.add_argument('--index',type=int);p.add_argument('--base',action='store_true')
    p.add_argument('--output',required=True)
    x=p.parse_args();data=canonical_rows(x.all,x.h)
    if x.base:
        if x.index is not None or x.all or x.h!=4:p.error('--base cannot be combined with --index/--all/--h')
        c,_,_=build_base();write_cnf(c,x.output);raw=Path(x.output).read_bytes()
        print(f'PASS base vars={len(c.names)} clauses={len(c.clauses)} sha256={hashlib.sha256(raw).hexdigest()}')
        return
    if x.index is None:
        raw=('m7-family-s-badness-pilot-v1\n'+f'rows={len(data)}\n'+
             '\n'.join(json.dumps(r,separators=(',',':'))for r in data)+'\n').encode()
        print(f'PASS rows={len(data)} sha256={hashlib.sha256(raw).hexdigest()}')
        Path(x.output).write_bytes(raw);return
    if not 0<=x.index<len(data):p.error('index outside selected subset')
    c,_,_=build(data[x.index]);write_cnf(c,x.output)
    raw=Path(x.output).read_bytes()
    print(f'PASS index={x.index} vars={len(c.names)} clauses={len(c.clauses)} sha256={hashlib.sha256(raw).hexdigest()}')
    print('row='+json.dumps(data[x.index],separators=(',',':')))
if __name__=='__main__':main()
