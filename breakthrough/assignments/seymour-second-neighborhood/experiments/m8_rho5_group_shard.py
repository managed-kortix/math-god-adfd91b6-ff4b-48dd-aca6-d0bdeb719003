#!/usr/bin/env python3
"""Emit one representative-free rho5 grouped CNF."""
import argparse
from m8_rho5_groups import groups
from m8_rho5_leaves import DELTA
from snc_cnf import generate, threshold


def unit(c,name,value=True): c.add(c.var(name) if value else -c.var(name))
def exact(c,lits,value,tag):
    out=threshold(c,lits,tag)
    if value: c.add(out[value-1])
    if value<len(lits): c.add(-out[value])


def emit(g,path):
    state,r0,r1,n0,n1,e0,e1=g; d0,d1=DELTA[state]
    q0=r0+1+d0-n0-e0; q1=r1+1+d1-n1-e1
    c=generate(18,7,8,robust_witness=True,high_vertices=(1,),
               forced_witness=(0,1),arc_minimal=True)
    for name,val in (("h_0_16",n0),("h_0_17",n1),("h_1_16",e0),("h_1_17",e1)):
        unit(c,name,bool(val))
    unit(c,'h_16_17',state=='M')
    if state=='01': unit(c,'a_16_17')
    elif state=='10': unit(c,'a_17_16')
    for b in range(9,16): unit(c,f'h_{b}_16',False); unit(c,f'h_{b}_17',False)
    exact(c,[c.var(f'h_{a}_16') for a in range(2,9)],q0,'group_Q0')
    exact(c,[c.var(f'h_{a}_17') for a in range(2,9)],q1,'group_Q1')
    exact(c,[c.var(f'a_16_{b}') for b in range(9,16)],r0,'group_X0')
    exact(c,[c.var(f'a_17_{b}') for b in range(9,16)],r1,'group_X1')
    with open(path,'w',encoding='ascii',newline='\n') as f:
        for name,num in c.names.items(): f.write(f'c var {num} {name}\n')
        f.write(f'p cnf {len(c.names)} {len(c.clauses)}\n')
        for clause in c.clauses: f.write(' '.join(map(str,clause))+' 0\n')
    return len(c.names),len(c.clauses)


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--index',type=int,required=True); p.add_argument('--output',required=True)
    x=p.parse_args(); data=list(groups())
    if not 0<=x.index<len(data): p.error(f'index outside 0..{len(data)-1}')
    v,c=emit(data[x.index],x.output); print(f'index={x.index} key={data[x.index]} vars={v} clauses={c}')
