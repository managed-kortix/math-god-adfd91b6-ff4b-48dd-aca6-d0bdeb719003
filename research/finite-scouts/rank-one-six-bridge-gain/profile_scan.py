#!/usr/bin/env python3
"""Numerically classify rank-six candidates by positive-block profile.
Discovery only. Exact certificates are produced separately.
"""
import json
from collections import Counter,defaultdict
from pathlib import Path
import networkx as nx
from search import beta,sigma,orbits,join,attach_leaves,attach_path

def block_profile(g):
 ranks=[]
 for vs in nx.biconnected_components(g):
  h=g.subgraph(vs);r=h.number_of_edges()-h.number_of_nodes()+1
  if r>0:ranks.append(r)
 assert sum(ranks)==beta(g)
 return tuple(sorted(ranks,reverse=True))
def unit_star_eligible(g,root):
 """Whether attaching the selected unit arm at root yields only 1|6 hull cuts.

 Delete every physical bridge of R, contract the resulting bridge-free
 components, assign each its cyclomatic rank, and add one external rank-one
 arm at ``root``.  The actual reduced hull is a unit-star candidate exactly
 when every quotient edge has weighted split 1|6 (zero-rank connector tails
 are harmless and give 0|7 before suppression).
 """
 bridges=list(nx.bridges(g));h=g.copy();h.remove_edges_from(bridges)
 comps=list(nx.connected_components(h));where={v:i for i,C in enumerate(comps) for v in C}
 T=nx.Graph();T.add_nodes_from(range(len(comps)+1));weights={}
 for i,C in enumerate(comps):weights[i]=beta(g.subgraph(C))
 for a,b in bridges:T.add_edge(where[a],where[b])
 ext=len(comps);T.add_node(ext);weights[ext]=1;T.add_edge(where[root],ext)
 assert nx.is_tree(T) and sum(weights.values())==7
 for a,b in list(T.edges()):
  T.remove_edge(a,b);side=nx.node_connected_component(T,a);q=sum(weights[z] for z in side);T.add_edge(a,b)
  if q not in (0,1,6,7):return False
 return True

def main():
 atlas=[]
 for g in nx.graph_atlas_g():
  if g and nx.is_connected(g) and beta(g)==6:
   for o in orbits(g):atlas.append(('atlas',g,o[0]))
 # Payload variants of every atlas rank6 graph through 7: one leaf/path rooted at each orbit rep,
 # ports include every resulting orbit. This provides profiles plus adverse marks.
 variants=list(atlas)
 for _,g,a in atlas:
  for kind,k in [('leaf',1),('path2',2),('path4',4)]:
   h=attach_leaves(g,a,k) if kind=='leaf' else attach_path(g,a,k)
   for o in orbits(h):variants.append((kind,h,o[0]))
 # Hostile U: bare C5 at each orbit and C5+one leaf at every orbit.
 Us=[]
 c=nx.cycle_graph(5)
 for o in orbits(c):Us.append(('C5',c,o[0]))
 cl=attach_leaves(c,0,1)
 for o in orbits(cl):Us.append(('C5+leaf',cl,o[0]))
 delta5=5**.5-2
 best={}; counts=Counter()
 for src,R,v in variants:
  prof=block_profile(R);counts[prof]+=1
  for un,U,u in Us:
   G=join(U,u,R,v);su=sigma(U);sr=sigma(R);sg=sigma(G);gam=sg-su-sr;F=gam+sr-delta5
   row={'profile':prof,'R_g6':nx.to_graph6_bytes(R,header=False).decode().strip(),'R_root':v,
    'R_source':src,'U':un,'U_g6':nx.to_graph6_bytes(U,header=False).decode().strip(),'U_root':u,
    'sigma_R':sr,'sigma_U':su,'sigma_G':sg,'Gamma':gam,'F':F,
    'unit_star_eligible':unit_star_eligible(R,v),'R_n':len(R),'G_n':len(G)}
   for metric in ['sigma_G','Gamma','F']:
    key=(prof,metric)
    if key not in best or row[metric]<best[key][metric]:best[key]=row
 out={'counts_by_profile':{str(k):v for k,v in sorted(counts.items())},
      'minima':[dict(metric=m,**best[(p,m)]) for p in sorted(set(k[0] for k in best)) for m in ['sigma_G','Gamma','F']],
      'scope':'all rooted graph-atlas rank-six graphs (order<=7), plus one-leaf/P2/P4 attachments at each atlas root and all resulting root orbits; U=C5 or C5+one leaf; nonexhaustive payload extension'}
 Path(__file__).with_name('profile-results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print('profiles',counts)
 for r in out['minima']:
  if r['metric']=='F':print(r['profile'],'F',r['F'],'sg',r['sigma_G'],'gam',r['Gamma'],'sr',r['sigma_R'],r['R_g6'],r['R_root'],r['U'],r['U_root'])
if __name__=='__main__':main()
