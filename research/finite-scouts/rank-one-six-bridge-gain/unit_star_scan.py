#!/usr/bin/env python3
"""Discovery scout for actual reduced unit-star rank-seven hulls.

A bridge-free/connected center C of cyclomatic rank c is joined by one bridge
to each of 7-c rank-one arms.  One distinguished arm U is deleted to leave R
of rank six.  Numerical discovery only; exact certificates are separate.
"""
from __future__ import annotations
import json, math
from pathlib import Path
from collections import Counter
import networkx as nx
from search import beta, sigma, orbits, attach_leaves

HERE=Path(__file__).resolve().parent

def graph6(g): return nx.to_graph6_bytes(nx.convert_node_labels_to_integers(g),header=False).decode().strip()

def arm(t=0):
 g=nx.cycle_graph(5)
 if t:
  g=attach_leaves(g,0,t); port=5
 else: port=0
 return g,port

def add_arm(g,center_port,A,aport):
 h=nx.disjoint_union(g,A);h.add_edge(center_port,len(g)+aport);return h

def build(C,port,c,selected_t=0,other_t=0):
 # selected U separately, R = center + remaining 6-c arms.
 R=C.copy()
 A,a=arm(other_t)
 for _ in range(6-c):R=add_arm(R,port,A,a)
 U,u=arm(selected_t)
 G=nx.disjoint_union(U,R);G.add_edge(u,len(U)+port)
 return U,u,R,port,G

def positive_block_profile(g):
 ranks=[]
 for vs in nx.biconnected_components(g):
  h=g.subgraph(vs); r=h.number_of_edges()-h.number_of_nodes()+1
  if r>0:ranks.append(r)
 assert sum(ranks)==beta(g)
 return tuple(sorted(ranks,reverse=True))


def actual_unit_star_eligible(g):
 """Reconstruct all physical bridge cuts; accept only 0|7 and 1|6."""
 bridges=list(nx.bridges(g)); h=g.copy(); h.remove_edges_from(bridges)
 comps=list(nx.connected_components(h)); where={v:i for i,C in enumerate(comps) for v in C}
 T=nx.Graph(); T.add_nodes_from(range(len(comps)))
 weights={i:beta(g.subgraph(C)) for i,C in enumerate(comps)}
 for a,b in bridges:T.add_edge(where[a],where[b])
 assert nx.is_tree(T) and sum(weights.values())==7
 for a,b in list(T.edges()):
  T.remove_edge(a,b); S=nx.node_connected_component(T,a); q=sum(weights[z] for z in S); T.add_edge(a,b)
  if q not in (0,1,6,7):return False
 return True

def centers():
 # c=0 only the minimal one-vertex zero center. c>=1 all atlas centers <=7.
 yield 0,nx.empty_graph(1),0,'K1'
 for C in nx.graph_atlas_g():
  if not C or not nx.is_connected(C) or len(C)>7:continue
  c=beta(C)
  if not 1<=c<=6:continue
  # A reduced star center is an actual bridge-free component. Atlas graph may
  # have internal bridges; record both, rather than silently excluding.
  for orb in orbits(C):yield c,C,orb[0],f'atlas-n{len(C)}-{graph6(C)}-o{orb[0]}'

def main():
 d=math.sqrt(5)-2; rows=[]
 for c,C,v,label in centers():
  for st in [0,1,2,3,5,10,20]:
   for ot in [0,1,2,5]:
    # Large all-arm payloads get expensive; bounded stated family.
    if ot and (7-c)*ot>30:continue
    U,u,R,r,G=build(C,v,c,st,ot)
    su,sr,sg=map(sigma,[U,R,G]);gam=sg-su-sr;F=gam+sr-d
    rows.append({'center_rank':c,'positive_block_rank_profile':positive_block_profile(R),
      'center_g6':graph6(C),'center_root':v,'center_label':label,
      'center_positive_component_count':len(positive_block_profile(C)),
      'actual_unit_star_eligible':actual_unit_star_eligible(G),
      'selected_arm_leaves':st,'other_arm_leaves':ot,
      'R_g6':graph6(R),'R_root':r,'U_g6':graph6(U),'U_root':u,'G_g6':graph6(G),
      'nG':len(G),'sigma_U':su,'sigma_R':sr,'sigma_G':sg,'Gamma':gam,'F':F})
 eligible_rows=[r for r in rows if r['actual_unit_star_eligible']]
 metrics=['sigma_G','Gamma','F'];best={}
 for row in eligible_rows:
  for met in metrics:
   key=(tuple(row['positive_block_rank_profile']),met)
   if key not in best or row[met]<best[key][met]:best[key]=row
 out={'scope':'generated common-center-port family, filtered by independently reconstructed physical bridge cuts: K1 center for c=0 and every rooted connected Graph Atlas center (order<=7) of rank c=1..6; selected C5 arm has 0,1,2,3,5,10,20 leaves at its cycle root and is bridged at a leaf; all other C5 arms independently use common payload size 0,1,2,5; all bridges meet one center port. Numeric discovery only.',
   'counts':{'rows':len(rows),'eligible_rows':len(eligible_rows),'negative_F':sum(r['F']<0 for r in eligible_rows),'negative_sigma_G':sum(r['sigma_G']<0 for r in eligible_rows)},
   'minima':[dict(metric=k[1],**v) for k,v in sorted(best.items())],
   'global':{m:min(eligible_rows,key=lambda r:r[m]) for m in metrics}}
 (HERE/'unit-star-results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(out['counts'])
 for m,r in out['global'].items():print(m,r[m],r['positive_block_rank_profile'],r['center_label'],'st/ot',r['selected_arm_leaves'],r['other_arm_leaves'],'sg',r['sigma_G'],'gam',r['Gamma'],'F',r['F'])
 print('profile F minima')
 for x in out['minima']:
  if x['metric']=='F':
   print(tuple(x['positive_block_rank_profile']),x['F'],x['center_label'],x['selected_arm_leaves'],x['other_arm_leaves'],x['sigma_G'],x['Gamma'])
if __name__=='__main__':main()
