#!/usr/bin/env python3
"""Emit the exact SAT shard for one canonical rho=5 leaf key."""
import argparse
from m8_rho5_leaves import DELTA, leaves
from snc_cnf import generate


def unit(c,name,value=True): c.add(c.var(name) if value else -c.var(name))


def representative(key):
    state,r0,r1,n0,n1,e0,e1,k,t=key
    d0,d1=DELTA[state]; a0=r0+1+d0-n0; a1=r1+1+d1-n1
    q0,q1=a0-e0,a1-e1
    common=set(range(2,2+k))
    only0=set(range(2+k,2+q0))
    only1=set(range(2+q0,2+q0+q1-k))
    Q0=common|only0; Q1=common|only1
    # B=9..15: first t common, then X0-only, then X1-only.
    both=set(range(9,9+t)); x0=both|set(range(9+t,9+r0))
    x1=both|set(range(9+r0,9+r0+r1-t))
    missing=set()
    if n0: missing.add((0,16))
    if n1: missing.add((0,17))
    if e0: missing.add((1,16))
    if e1: missing.add((1,17))
    missing|={(a,16) for a in Q0}|{(a,17) for a in Q1}
    if state=='M': missing.add((16,17))
    assert len(missing)==8
    return missing,x0,x1,state


def emit(key,path):
    missing,x0,x1,state=representative(key)
    c=generate(18,7,8,robust_witness=True,high_vertices=(1,),
               forced_witness=(0,1),arc_minimal=True)
    for i in range(18):
        for j in range(i+1,18): unit(c,f"h_{i}_{j}",(i,j) in missing)
    if state!='M': unit(c,'a_16_17',state=='01')
    for b in range(9,16): unit(c,f"a_16_{b}",b in x0)
    for b in range(9,16): unit(c,f"a_17_{b}",b in x1)
    with open(path,'w',encoding='ascii',newline='\n') as f:
        for name,num in c.names.items(): f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for clause in c.clauses: f.write(' '.join(map(str,clause))+' 0\n')
    return len(c.names),len(c.clauses)


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--index',type=int,required=True)
    p.add_argument('--output',required=True); x=p.parse_args(); data=list(leaves())
    if not 0<=x.index<len(data): p.error('index outside 0..734')
    v,c=emit(data[x.index],x.output)
    print(f"index={x.index} key={data[x.index]} vars={v} clauses={c}")
