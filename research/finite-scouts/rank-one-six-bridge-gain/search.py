#!/usr/bin/env python3
"""Nonexhaustive numerical scout for rank-(1,6) one-bridge joins.

The atlas pass is exhaustive only for connected unlabeled side graphs of order
<=7 represented in NetworkX's Graph Atlas.  The generated pass adds selected
cores plus rooted trees/leaves.  Floating point is discovery only; certify.py
rebuilds chosen records and proves comparisons with exact characteristic
polynomials and Sturm-isolated rational root intervals.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, sys, time
from pathlib import Path
from collections import defaultdict
import numpy as np
import networkx as nx

OUT = Path(__file__).resolve().parent


def beta(g):
    return g.number_of_edges()-g.number_of_nodes()+nx.number_connected_components(g)

def canonical_wl(g):
    # Discovery identity only, never claimed a canonical isomorphism key.
    return nx.weisfeiler_lehman_graph_hash(g, iterations=max(3,len(g)))

def graph6(g):
    h=nx.convert_node_labels_to_integers(g, ordering='sorted')
    return nx.to_graph6_bytes(h,header=False).decode().strip()

def from_g6(s): return nx.from_graph6_bytes(s.encode())

def spectrum(g):
    A=nx.to_numpy_array(g,dtype=float)
    return np.linalg.eigvalsh(A)

def splus_from_eigs(w):
    # eigenvalues in discovery records are well away from tolerance except zeros
    return float(np.dot(w[w>1e-9],w[w>1e-9]))

def sigma(g): return splus_from_eigs(spectrum(g))-len(g)

def orbits(g):
    """Exact vertex orbits via pairwise rooted colored-graph isomorphism.

    This avoids enumerating a potentially factorial automorphism group.
    """
    nodes=list(g.nodes())
    remaining=set(nodes); out=[]
    # Cheap exact-isomorphism invariants reduce calls.
    tri=nx.triangles(g)
    ecc=nx.eccentricity(g) if nx.is_connected(g) and len(g)>1 else {v:0 for v in g}
    while remaining:
        a=min(remaining); orbit=[]
        ga=g.copy();nx.set_node_attributes(ga,False,'_root');ga.nodes[a]['_root']=True
        inva=(g.degree(a),tri[a],ecc[a])
        for b in sorted(remaining):
            if (g.degree(b),tri[b],ecc[b])!=inva: continue
            gb=g.copy();nx.set_node_attributes(gb,False,'_root');gb.nodes[b]['_root']=True
            nm=nx.algorithms.isomorphism.categorical_node_match('_root',False)
            if nx.is_isomorphic(ga,gb,node_match=nm): orbit.append(b)
        for b in orbit:remaining.remove(b)
        out.append(orbit)
    return out

def join(h,u,k,v):
    g=nx.disjoint_union(h,k)
    g.add_edge(u,len(h)+v)
    return g

def rec(side, root, label, source):
    return {'g6':graph6(side),'root':int(root),'label':label,'source':source,
            'n':len(side),'m':side.number_of_edges(),'beta':beta(side)}

def cycle_with_rooted_tree(q,tree,cycle_root,tree_root):
    c=nx.cycle_graph(q)
    t=nx.convert_node_labels_to_integers(tree)
    # Identify tree_root with cycle_root; tree has no required nontrivial size.
    mapping={tree_root:cycle_root}
    nxt=q
    for x in t:
        if x!=tree_root: mapping[x]=nxt;nxt+=1
    h=nx.compose(c,nx.relabel_nodes(t,mapping))
    return nx.convert_node_labels_to_integers(h)

def attach_leaves(g,at,count):
    h=g.copy();n=len(h)
    for i in range(count):h.add_edge(at,n+i)
    return h

def attach_path(g,at,length):
    h=g.copy();p=at
    for _ in range(length):
        q=len(h);h.add_edge(p,q);p=q
    return h

def rank6_cores():
    out=[]
    # Complete and dense named cores.
    out.append(('K5',nx.complete_graph(5)))
    h=nx.complete_graph(5);h.remove_edge(0,1);h.add_node(5);h.add_edges_from([(5,0),(5,1)])
    # m=11,n=6 beta=6
    out.append(('K5-edge-subdivision',h))
    # Cycle bouquet B6: six C5s share a vertex (large but sparse).
    b=nx.Graph();b.add_node(0);n=1
    for i in range(6):
        vs=[0]+list(range(n,n+4));n+=4
        for a,c in zip(vs,vs[1:]+vs[:1]):b.add_edge(a,c)
    out.append(('six-C5-bouquet',b))
    # Friendship-like six triangle bouquet.
    f=nx.Graph();f.add_node(0);n=1
    for i in range(6):f.add_edges_from([(0,n),(n,n+1),(n+1,0)]);n+=2
    out.append(('six-triangle-bouquet',f))
    return out

def collect_sides(args):
    atlas=nx.graph_atlas_g()
    us=[];hs=[]
    for g in atlas:
        if not g or not nx.is_connected(g):continue
        b=beta(g)
        if b==1 and len(g)<=args.atlas_n:
            for orb in orbits(g):us.append(rec(g,orb[0],f'atlas-U-n{len(g)}-{graph6(g)}-o{orb[0]}','atlas'))
        if b==6 and len(g)<=args.atlas_n:
            for orb in orbits(g):hs.append(rec(g,orb[0],f'atlas-H-n{len(g)}-{graph6(g)}-o{orb[0]}','atlas'))
    # Every unlabeled tree <= tree_n, attached at all tree/cycle root orbits.
    seen=set((x['g6'],x['root']) for x in us)
    for tn in range(1,args.tree_n+1):
      trees=[nx.empty_graph(1)] if tn==1 else list(nx.generators.nonisomorphic_trees(tn))
      for ti,t in enumerate(trees):
       for torb in orbits(t):
        tr=torb[0]
        for q in range(3,args.cycle_n+1):
         for cr in range((q//2)+1): # attachment at 0; marked root all distances modulo reflection
          h=cycle_with_rooted_tree(q,t,0,tr)
          root=cr
          key=(graph6(h),root)
          if key not in seen:
           seen.add(key);us.append(rec(h,root,f'C{q}+tree{tn}.{ti}@d{cr}','generated-unicyclic-tree'))
          # also root at each added tree orbit representative
          # mapping reconstruction: root on cycle enough plus all actual graph orbits below
         # ensure all root orbits of each resulting side included
         h=cycle_with_rooted_tree(q,t,0,tr)
         for orb in orbits(h):
          key=(graph6(h),orb[0])
          if key not in seen:
           seen.add(key);us.append(rec(h,orb[0],f'C{q}+tree{tn}.{ti}@o{orb[0]}','generated-unicyclic-tree'))
    # Structured rank-six cores with stars and paths, every resulting vertex orbit.
    hseen=set((x['g6'],x['root']) for x in hs)
    for name,c in rank6_cores():
      variants=[(name,c)]
      for at in [0]:
       for leaves in range(1,args.leaves+1):variants.append((f'{name}+{leaves}leaves@{at}',attach_leaves(c,at,leaves)))
       for length in range(1,args.path+1):variants.append((f'{name}+P{length}@{at}',attach_path(c,at,length)))
      for label,h in variants:
       assert beta(h)==6
       for orb in orbits(h):
        key=(graph6(h),orb[0])
        if key not in hseen:
         hseen.add(key);hs.append(rec(h,orb[0],label+f'-o{orb[0]}','generated-rank6-core'))
    return us,hs

def evaluate_pair(u,h):
    U=from_g6(u['g6']);H=from_g6(h['g6'])
    G=join(U,u['root'],H,h['root'])
    su=sigma(U);sh=sigma(H);sg=sigma(G)
    gamma=sg-su-sh # n cancellation: s+(G)-s+(U)-s+(H)
    delta5=math.sqrt(5.0)-2.0
    F=gamma+sh-delta5
    payment=gamma+su # = sigma(G)-sigma(H)
    return {'sigma_G':sg,'sigma_U':su,'sigma_H':sh,'Gamma':gamma,'payment':payment,'F':F,
            'U':u,'H':h,'G_g6':graph6(G),'nG':len(G)}

def keep_small(heap,record,key,k):
    heap.append(record);heap.sort(key=lambda x:x[key]);del heap[k:]

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--atlas-n',type=int,default=7)
 p.add_argument('--tree-n',type=int,default=5)
 p.add_argument('--cycle-n',type=int,default=10)
 p.add_argument('--leaves',type=int,default=30)
 p.add_argument('--path',type=int,default=12)
 p.add_argument('--top',type=int,default=30)
 p.add_argument('--hostile-only',action='store_true',help='keep rank-one sides with sigma<0 (discovery float)')
 p.add_argument('--output',default=str(OUT/'search-results.json'))
 args=p.parse_args()
 us,hs=collect_sides(args)
 if args.hostile_only:
  us=[u for u in us if sigma(from_g6(u['g6'])) < -1e-8]
 fields=['sigma_G','payment','Gamma','F']
 tops={f:[] for f in fields};neg=[]
 t0=time.time();count=0
 usigma={}
 hsigma={}
 for i,u in enumerate(us):
  for h in hs:
   r=evaluate_pair(u,h);count+=1
   for f in fields:keep_small(tops[f],r,f,args.top)
   if r['sigma_G'] < -1e-8:neg.append(r)
 result={'scope':{'atlas_n':args.atlas_n,'tree_n':args.tree_n,'cycle_n':args.cycle_n,
                  'leaves':args.leaves,'path':args.path,
                  'atlas_statement':'all connected unlabeled graph-atlas sides through stated order; all vertex automorphism orbits',
                  'generated_statement':'selected named cores and every nonisomorphic tree through tree_n; not exhaustive beyond atlas'},
         'counts':{'rooted_U':len(us),'rooted_H':len(hs),'joins':count,'negative_sigma_G':len(neg)},
         'tops':tops,'negative':sorted(neg,key=lambda x:x['sigma_G'])[:args.top],
         'seconds':time.time()-t0,'versions':{'python':sys.version,'numpy':np.__version__,'networkx':nx.__version__}}
 Path(args.output).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 print(json.dumps({'counts':result['counts'],'seconds':result['seconds'],
                   'minima':{f:(tops[f][0][f],tops[f][0]['U']['label'],tops[f][0]['H']['label']) for f in fields}},indent=2))
if __name__=='__main__':main()
