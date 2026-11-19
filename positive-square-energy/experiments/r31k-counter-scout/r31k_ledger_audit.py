#!/usr/bin/env python3
"""Combinatorial audit of the proposed three-case full R31-K ledger.

Uses the same exhaustive recursively attached block realizations as
r31k_scout.py.  This does not prove spectral contracts; it asks whether the
profile-count inequalities in Cases I--III can fail on generated physical
block-cut trees.
"""
from __future__ import annotations
import argparse,collections,itertools,json
from r31k_scout import generate_cores, adjacency, block_vertices, tarjan_blocks

PROFILES={'T4':(3,3,3,3),'T3C5':(3,3,3,5),'T3C7':(3,3,3,7),'T2C5C5':(3,3,5,5)}


def rooted_inventory(g):
    blocks=tarjan_blocks(g); b=len(blocks)
    data=[]
    memberships=collections.defaultdict(list)
    for i,B in enumerate(blocks):
        V=block_vertices(B);rank=len(B)-len(V)+1
        if rank==0:kind=('bridge',2)
        elif len(V)==4 and len(B)==6:kind=('K4',4)
        elif rank==1 and len(B)==len(V):kind=('cycle',len(V))
        else:raise AssertionError
        data.append((B,V,rank,kind))
        for v in V:memberships[v].append(i)
    cuts={v for v,L in memberships.items() if len(L)>1}
    T=[set() for _ in range(b+g[0])]
    for v in cuts:
        for i in memberships[v]:T[i].add(b+v);T[b+v].add(i)
    root=next(i for i,x in enumerate(data) if x[3][0]=='K4')
    par=[-2]*len(T);par[root]=-1;stack=[root];order=[]
    while stack:
        u=stack.pop();order.append(u)
        for v in T[u]:
            if par[v]==-2:par[v]=u;stack.append(v)
    cycles=[i for i,x in enumerate(data) if x[3][0]=='cycle']
    bridges={i for i,x in enumerate(data) if x[3][0]=='bridge'}
    def route(i):
        z=[];x=i
        while x!=-1:z.append(x);x=par[x]
        return list(reversed(z))
    root_cycles=[];away_cycles=[]
    for i in cycles:
        if any(x<b and x in bridges for x in route(i)):
            away_cycles.append(i)
        else:root_cycles.append(i)
    direct_tri=[]
    for i in root_cycles:
        r=route(i)
        if data[i][3][1]==3 and r==[root,r[1],i]:direct_tri.append(i)
    # Hostile away singleton means its first-bridge component has exactly one
    # cycle and that cycle has length 1 mod 4. Identify by first bridge route.
    groups=collections.defaultdict(list)
    for i in away_cycles:
        r=route(i); fb=next(x for x in r if x<b and x in bridges)
        groups[fb].append(i)
    hostile_singletons=[]
    for group in groups.values():
        if len(group)==1 and data[group[0]][3][1]%4==1:hostile_singletons+=group
    return data,par,root,root_cycles,away_cycles,direct_tri,groups,hostile_singletons,route


def audit(g):
    data,par,root,R,A,direct,groups,hostile,route=rooted_inventory(g)
    lengths={i:data[i][3][1] for i in R+A}
    a=len(hostile);r=len(R)
    if direct:
        # Case I only needs hostile singleton away count <= total away cycles=4-r.
        assert a<=4-r
        return 'I',{'r':r,'a':a,'slack':4-r-a}
    root_tris=[i for i in R if lengths[i]==3]
    if root_tris:
        # First positive block after root on each route to a root triangle.
        first_nontri=set()
        for i in root_tris:
            pos=[x for x in route(i)[1:] if x<len(data) and data[x][2]>0]
            assert pos and pos[-1]==i
            assert lengths[pos[0]]!=3  # no direct T and only cycles are positive
            first_nontri.add(pos[0])
        # The report's u is any root-side nontriangle demand not absorbed into
        # one of the selected first-nontriangle downstream subtrees. A cycle j
        # is absorbed iff one selected first nontriangle is an ancestor of j.
        def ancestor(x,y): return x in route(y)
        root_nontri=[i for i in R if lengths[i]!=3]
        unabsorbed=[i for i in root_nontri if not any(ancestor(f,i) for f in first_nontri)]
        u=len(unabsorbed)
        return 'II',{'r':r,'a':a,'first_nontriangles':len(first_nontri),'u':u,
                     'u_plus_a':u+a,'claimed_ok':u+a<=1}
    return 'III',{'r':r,'a':a,'r_plus_a':r+a,'claimed_ok':r+a<=2}


def main():
 p=argparse.ArgumentParser();p.add_argument('--max-bridge',type=int,default=2);p.add_argument('--output');args=p.parse_args()
 out={};viol=[]
 for name,profile in PROFILES.items():
  graphs,layers=generate_cores(profile,args.max_bridge)
  cases=collections.Counter();stats=collections.Counter()
  for g in graphs:
   case,z=audit(g);cases[case]+=1
   if case=='II' and not z['claimed_ok']:viol.append((name,case,z,g))
   if case=='III' and not z['claimed_ok']:viol.append((name,case,z,g))
   stats[(case,tuple(sorted(z.items())))]+=1
  out[name]={'graphs':len(graphs),'cases':dict(cases),'distinct_case_records':len(stats),
             'case_records':[{'case':k[0],'data':dict(k[1]),'count':v} for k,v in sorted(stats.items(),key=str)]}
 out['violations']=[{'profile':x[0],'case':x[1],'data':x[2],'n':x[3][0],'edges':sorted(x[3][1])} for x in viol]
 text=json.dumps(out,indent=2,sort_keys=True,default=list)+'\n'
 if args.output:open(args.output,'w').write(text)
 else:print(text,end='')

if __name__=='__main__':main()
