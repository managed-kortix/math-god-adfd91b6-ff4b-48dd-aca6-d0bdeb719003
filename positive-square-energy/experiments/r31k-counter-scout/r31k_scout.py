#!/usr/bin/env python3
"""NONPROMOTIONAL finite R31-K topology/spectral scout.

Generates simple connected graphs whose positive-rank blocks are one literal K4
and four literal cycles.  Cycles are attached recursively at any existing
vertex, either by a shared cut (distance 0) or by a bridge path of bounded
length.  Canonical certificates remove graph isomorphs.  Optional leaf growth
exhausts rooted-forest payloads of bounded total order.  Floating spectra are
only a target finder; selected candidates can be certified by exact integer
characteristic polynomials and rational Sturm isolation.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
import pynauty

Graph = tuple[int, frozenset[tuple[int,int]]]


def edge(u:int,v:int)->tuple[int,int]:
    assert u!=v
    return (u,v) if u<v else (v,u)


def k4()->Graph:
    return 4, frozenset(itertools.combinations(range(4),2))


def adjacency(g:Graph):
    n,E=g
    A=[set() for _ in range(n)]
    for u,v in E:
        A[u].add(v); A[v].add(u)
    return A


def certificate(g:Graph)->bytes:
    n,E=g
    A=adjacency(g)
    pg=pynauty.Graph(number_of_vertices=n, directed=False,
                     adjacency_dict={i:list(A[i]) for i in range(n)})
    return pynauty.certificate(pg)


def canonical_graph(g:Graph)->Graph:
    # Used only for stable witness serialization, not dedup itself.  Building
    # from canon_label avoids a pynauty canon_graph bug on large color classes.
    n,E=g
    A=adjacency(g)
    pg=pynauty.Graph(number_of_vertices=n,directed=False,
                     adjacency_dict={i:list(A[i]) for i in range(n)})
    lab=pynauty.canon_label(pg)
    image={old:new for new,old in enumerate(lab)}
    CE=frozenset(edge(image[u],image[v]) for u,v in E)
    return n,CE


def attach_cycle(g:Graph, at:int, q:int, bridge_length:int)->Graph:
    """Attach a new literal C_q at existing vertex at.

    bridge_length=0 identifies one cycle vertex with at.  For d>=1, add a
    d-edge path from at to a new cycle root, then q-1 private cycle vertices.
    """
    n,E=g; out=set(E)
    if bridge_length==0:
        root=at
    else:
        prev=at
        for _ in range(bridge_length):
            root=n; n+=1; out.add(edge(prev,root)); prev=root
    cyc=[root]+list(range(n,n+q-1)); n+=q-1
    for i in range(q): out.add(edge(cyc[i],cyc[(i+1)%q]))
    return n,frozenset(out)


def add_leaf(g:Graph,at:int)->Graph:
    n,E=g
    return n+1,E|frozenset((edge(at,n),))


def dedup(graphs):
    d={}
    for g in graphs:
        c=certificate(g)
        d.setdefault(c,g)
    return list(d.values())


def generate_cores(profile:tuple[int,...], max_bridge:int, progress=False):
    states={tuple(sorted(profile)): {certificate(k4()):k4()}}
    layer_counts=[]
    while states:
        # all states here have the same number of cycles remaining
        rem_count=len(next(iter(states)))
        if rem_count==0:
            assert len(states)==1
            return list(states[()].values()),layer_counts
        next_states:dict[tuple[int,...],dict[bytes,Graph]]={}
        raw=0
        for rem,bucket in states.items():
            for q in sorted(set(rem)):
                rr=list(rem); rr.remove(q); rr=tuple(rr)
                target=next_states.setdefault(rr,{})
                for g in bucket.values():
                    for v in range(g[0]):
                        for d in range(max_bridge+1):
                            h=attach_cycle(g,v,q,d); raw+=1
                            target.setdefault(certificate(h),h)
        layer_counts.append({"attached":len(profile)-rem_count+1,"raw":raw,
                             "unique":sum(map(len,next_states.values())),
                             "states":{str(k):len(v) for k,v in sorted(next_states.items())}})
        if progress: print('layer',layer_counts[-1],file=sys.stderr,flush=True)
        states=next_states
    raise AssertionError


def grow_payloads(bases:list[Graph], extra_vertices:int, progress=False):
    current={certificate(g):g for g in bases}
    counts=[len(current)]
    levels=[list(current.values())]
    for step in range(1,extra_vertices+1):
        nxt={}
        raw=0
        for g in current.values():
            for v in range(g[0]):
                h=add_leaf(g,v); raw+=1
                nxt.setdefault(certificate(h),h)
        current=nxt
        levels.append(list(current.values()));counts.append(len(current))
        if progress: print('payload',step,'raw',raw,'unique',len(current),file=sys.stderr,flush=True)
    return levels,counts


def matrix(g:Graph):
    n,E=g; A=np.zeros((n,n),dtype=float)
    for u,v in E:A[u,v]=A[v,u]=1.
    return A


def sigma_float(g:Graph):
    vals=np.linalg.eigvalsh(matrix(g))
    # Eigenvalues within roundoff of zero contribute a negligible square; use
    # sign at zero because the spectral definition uses strictly positive.
    return float(np.square(vals[vals>0]).sum()-g[0]),vals


def tarjan_blocks(g:Graph):
    """Return edge-biconnected blocks (bridges are singleton blocks)."""
    n,E=g; A=adjacency(g)
    disc=[-1]*n; low=[0]*n; parent=[-1]*n; stack=[]; blocks=[]; tick=0
    def dfs(u):
        nonlocal tick
        disc[u]=low[u]=tick;tick+=1
        for v in A[u]:
            e=edge(u,v)
            if disc[v]<0:
                parent[v]=u;stack.append(e);dfs(v);low[u]=min(low[u],low[v])
                if low[v]>=disc[u]:
                    block=[]
                    while True:
                        x=stack.pop();block.append(x)
                        if x==e:break
                    blocks.append(frozenset(block))
            elif v!=parent[u] and disc[v]<disc[u]:
                stack.append(e);low[u]=min(low[u],disc[v])
    dfs(0); assert all(x>=0 for x in disc) and not stack
    return blocks


def block_vertices(B):return frozenset(itertools.chain.from_iterable(B))


def inventory(g:Graph):
    blocks=tarjan_blocks(g)
    pos=[];bridges=[]
    for B in blocks:
        V=block_vertices(B); rank=len(B)-len(V)+1
        (bridges if rank==0 else pos).append((B,V,rank))
    kinds=[]
    for B,V,r in pos:
        deg=collections.Counter(itertools.chain.from_iterable(B))
        if len(V)==4 and len(B)==6 and all(x==3 for x in deg.values()): kind='K4'
        elif len(B)==len(V) and all(x==2 for x in deg.values()):kind=f'C{len(V)}'
        else:kind=f'OTHER({len(V)},{len(B)},{r})'
        kinds.append(kind)
    return blocks,pos,bridges,tuple(sorted(kinds))


def topology_stats(g:Graph):
    blocks,pos,bridges,kinds=inventory(g)
    assert kinds.count('K4')==1 and len(kinds)==5
    # Build block-cut tree. Block ids 0..b-1; articulation nodes b+v.
    b=len(blocks); memberships=collections.defaultdict(list)
    for i,B in enumerate(blocks):
        for v in block_vertices(B):memberships[v].append(i)
    cuts={v for v,L in memberships.items() if len(L)>1}
    T=[set() for _ in range(b+g[0])]
    for v in cuts:
        for i in memberships[v]:T[i].add(b+v);T[b+v].add(i)
    root=next(i for i,(B,V,r) in enumerate([(B,block_vertices(B),len(B)-len(block_vertices(B))+1) for B in blocks])
              if len(V)==4 and len(B)==6 and r==3)
    # root traversal and first bridge separation; block bridge iff singleton edge
    par=[-2]*len(T);par[root]=-1;q=collections.deque([root]);order=[]
    while q:
        u=q.popleft();order.append(u)
        for v in T[u]:
            if par[v]==-2:par[v]=u;q.append(v)
    pos_block_indices=[]; cycle_indices=[]; bridge_indices=[]
    for i,B in enumerate(blocks):
        V=block_vertices(B);r=len(B)-len(V)+1
        if r>0:pos_block_indices.append(i)
        if r==1:cycle_indices.append(i)
        if r==0:bridge_indices.append(i)
    def path_has_bridge(i):
        x=i
        while x!=root:
            if x<b and x in bridge_indices:return True
            x=par[x]
        return False
    root_cycles=[i for i in cycle_indices if not path_has_bridge(i)]
    direct_tri=0
    for i in root_cycles:
        V=block_vertices(blocks[i])
        if len(V)==3:
            # Path B-cut-T has exactly 2 edges in block-cut tree.
            x=i;dist=0
            while x!=root:x=par[x];dist+=1
            if dist==2:direct_tri+=1
    # away cycle group sizes after deleting first bridges: components of graph
    # with all bridge edges deleted, then report cyclic block counts in each.
    A=adjacency(g)
    bridge_edges={next(iter(blocks[i])) for i in bridge_indices}
    comp=[-1]*g[0];cc=[]
    for s in range(g[0]):
        if comp[s]>=0:continue
        cid=len(cc);verts=[];dq=[s];comp[s]=cid
        while dq:
            u=dq.pop();verts.append(u)
            for v in A[u]:
                if edge(u,v) in bridge_edges:continue
                if comp[v]<0:comp[v]=cid;dq.append(v)
        cc.append(verts)
    cyc_by_comp=collections.Counter()
    for i in cycle_indices:
        v=next(iter(block_vertices(blocks[i])));cyc_by_comp[comp[v]]+=1
    root_comp=comp[next(iter(block_vertices(blocks[root])))]
    away_groups=tuple(sorted((x for c,x in cyc_by_comp.items() if c!=root_comp),reverse=True))
    # Positive-block depths (number of positive ancestors), captures nesting.
    depths=[]
    for i in cycle_indices:
        x=i;d=0
        while x!=root:
            x=par[x]
            if x<b:
                V=block_vertices(blocks[x]);r=len(blocks[x])-len(V)+1
                if r>0:d+=1
        depths.append(d)
    return {"bridges":len(bridges),"cuts":len(cuts),"root_cycles":len(root_cycles),
            "direct_root_triangles":direct_tri,"away_cycle_groups":away_groups,
            "cycle_positive_depths":tuple(sorted(depths)),"kinds":kinds}


def load_exact_module(path:Path):
    spec=importlib.util.spec_from_file_location('r31_exact',path)
    m=importlib.util.module_from_spec(spec);sys.modules['r31_exact']=m
    assert spec.loader;spec.loader.exec_module(m);return m


def exact_certificate(g:Graph,exact,bits=48):
    n,E=g
    poly=exact.characteristic_polynomial(n,set(E))
    intervals=exact.isolate_positive_roots_with_multiplicity(poly,bits)
    lo=sum(mult*a*a for a,b,mult in intervals)-n
    hi=sum(mult*b*b for a,b,mult in intervals)-n
    return {"charpoly":poly,
            "positive_root_intervals":[[exact.rational_text(a),exact.rational_text(b),m] for a,b,m in intervals],
            "sigma_interval":[exact.rational_text(lo),exact.rational_text(hi)]},lo,hi


def stable_id(g:Graph):
    g=canonical_graph(g)
    raw=(str(g[0])+';'+','.join(f'{u}-{v}' for u,v in sorted(g[1]))).encode()
    return hashlib.sha256(raw).hexdigest()[:16]


def graph_record(g:Graph,s=None,include_edges=True):
    if s is None:s,_=sigma_float(g)
    h=canonical_graph(g)
    z={"id":stable_id(g),"n":g[0],"m":len(g[1]),"sigma_float":s,
       "topology":topology_stats(g)}
    if include_edges:z['canonical_edges']=[list(e) for e in sorted(h[1])]
    return z


def star_attach(g:Graph,site:int,leaves:int):
    out=g
    for _ in range(leaves):out=add_leaf(out,site)
    return out


def path_attach(g:Graph,site:int,length:int):
    n,E=g;E=set(E);prev=site
    for _ in range(length):
        E.add(edge(prev,n));prev=n;n+=1
    return n,frozenset(E)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--max-bridge',type=int,default=1)
    p.add_argument('--payload-extra',type=int,default=0)
    p.add_argument('--profile',action='append',choices=['T4','T3C5','T3C7','T2C5C5'])
    p.add_argument('--exact-keep',type=int,default=20)
    p.add_argument('--exact-bits',type=int,default=44)
    p.add_argument('--progress',action='store_true')
    p.add_argument('--output')
    p.add_argument('--skip-rays',action='store_true')
    p.add_argument('--skip-exact',action='store_true')
    p.add_argument('--repo',default='/workspace/repo')
    args=p.parse_args()
    profiles={'T4':(3,3,3,3),'T3C5':(3,3,3,5),'T3C7':(3,3,3,7),'T2C5C5':(3,3,5,5)}
    wanted=args.profile or list(profiles)
    exact=load_exact_module(Path(args.repo)/'research/shared_triangle_rooted_exact.py')
    report={"scope":{"max_bridge_per_recursive_attachment":args.max_bridge,
                     "payload_extra_vertices":args.payload_extra,
                     "profiles":wanted},"profiles":{}}
    global_rows=[]
    start=time.time()
    for name in wanted:
        cores,layers=generate_cores(profiles[name],args.max_bridge,args.progress)
        levels,payload_counts=grow_payloads(cores,args.payload_extra,args.progress)
        allgraphs=list(itertools.chain.from_iterable(levels))
        rows=[];topocount=collections.Counter();signs=collections.Counter()
        minrow=None
        for g in allgraphs:
            s,vals=sigma_float(g)
            signs['positive' if s>1e-8 else 'nonpositive_or_near']+=1
            topo=topology_stats(g)
            key=(topo['bridges'],topo['root_cycles'],topo['direct_root_triangles'],topo['away_cycle_groups'],topo['cycle_positive_depths'])
            topocount[str(key)]+=1
            row=(s,g)
            if minrow is None or s<minrow[0]:minrow=row
            rows.append(row);global_rows.append((s,name,g))
        rows.sort(key=lambda x:x[0])
        exact_rows=[]
        for s,g in rows[:args.exact_keep]:
            rec=graph_record(g,s)
            if not args.skip_exact:
                cert,lo,hi=exact_certificate(g,exact,args.exact_bits)
                rec['exact']=cert
            exact_rows.append(rec)
        report['profiles'][name]={"profile":profiles[name],"core_count":len(cores),
            "layer_counts":layers,"payload_counts_by_extra_order":payload_counts,
            "tested_graphs":len(allgraphs),"float_signs":dict(signs),
            "topology_signature_count":len(topocount),
            "topology_signature_census":dict(topocount),
            "minimum":exact_rows[0],"exact_closest":exact_rows}
    global_rows.sort(key=lambda x:x[0])
    # Adversarial star/path rays from the globally closest bare cores.  Search
    # every vertex site and powers on a geometric grid.
    rays=[]
    if not args.skip_rays:
        seen=set()
        for s,name,g in global_rows[:min(25,len(global_rows))]:
            cid=certificate(g)
            if cid in seen:continue
            seen.add(cid)
            for site in range(g[0]):
                for kind in ('star','path'):
                    for size in (1,2,3,5,10,20,50,100,200):
                        h=star_attach(g,site,size) if kind=='star' else path_attach(g,site,size)
                        val,_=sigma_float(h)
                        rays.append((val,name,g,site,kind,size,h))
        rays.sort(key=lambda x:x[0])
        report['adversarial_payload_rays']={
           "tested":len(rays),
           "float_signs":dict(collections.Counter('positive' if x[0]>1e-8 else 'nonpositive_or_near' for x in rays)),
           "minimum":{"base_profile":rays[0][1],"base_id":stable_id(rays[0][2]),"site":rays[0][3],
                      "kind":rays[0][4],"size":rays[0][5],"graph":graph_record(rays[0][6],rays[0][0])},
           "closest_20":[{"sigma_float":x[0],"base_profile":x[1],"base_id":stable_id(x[2]),
                          "site":x[3],"kind":x[4],"size":x[5],"n":x[6][0]} for x in rays[:20]]}
    report['elapsed_seconds']=time.time()-start
    text=json.dumps(report,indent=2,sort_keys=True,default=list)+'\n'
    if args.output:Path(args.output).write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
