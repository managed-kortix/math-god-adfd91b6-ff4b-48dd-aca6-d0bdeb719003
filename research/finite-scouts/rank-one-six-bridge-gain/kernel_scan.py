#!/usr/bin/env python3
"""Discovery-only scout over the authenticated rank-six kernel fixture.

The fixture encodes each loopless 2-connected multigraph kernel by upper-
triangle edge multiplicities.  For every kernel this script builds its unique
canonical shortest simple realization: in each parallel class one path has
length one and all remaining paths have length two.  It then tests every
marked vertex against several hostile C5-with-tree arms.  This is exhaustive
for those 1,198 fixed realizations and all labelled ports, but not for all path
parities/lengths or all rooted-tree payloads.
"""
from __future__ import annotations
import json, math, time
from pathlib import Path
import networkx as nx
from search import sigma, join, attach_leaves, attach_path

HERE=Path(__file__).resolve().parent
FIXTURE=HERE/'rank-six-kernels.json'

def pairs(n):
 for u in range(n):
  for v in range(u+1,n):yield u,v

def realize(n,code,parity_flip=None):
 """Shortest simple paths; optionally lengthen one indexed physical path by 1."""
 g=nx.Graph();g.add_nodes_from(range(n));nxt=n;physical=0
 for mult,(u,v) in zip(code,pairs(n)):
  for j in range(mult):
   length=1 if j==0 else 2
   if parity_flip==physical:length+=1
   if length==1:g.add_edge(u,v)
   else:
    prev=u
    for _ in range(length-1):g.add_edge(prev,nxt);prev=nxt;nxt+=1
    g.add_edge(prev,v)
   physical+=1
 return g

def arms():
 c=nx.cycle_graph(5);yield 'C5',c,0
 for t in (1,2,3,5,10,20):
  h=attach_leaves(c,0,t)
  for root,label in [(0,'hub'),(1,'near'),(2,'far'),(5,'leaf')]:yield f'C5+S{t}-{label}',h,root
 for t in (1,2,3,5,10):
  h=attach_path(c,0,t)
  for root,label in [(0,'hub'),(1,'near'),(2,'far'),(len(h)-1,'tip')]:yield f'C5+P{t}-{label}',h,root

def graph6(g):return nx.to_graph6_bytes(nx.convert_node_labels_to_integers(g),header=False).decode().strip()

def keep(d,key,row,k=30):
 d[key].append(row);d[key].sort(key=lambda z:z[key]);del d[key][k:]

def main():
 fixture=json.loads(FIXTURE.read_text()); ks=fixture['kernels']; AA=[]
 for label,U,u in arms():AA.append((label,U,u,sigma(U)))
 tops={x:[] for x in ['sigma_R','sigma_G','Gamma','F']};neg=[];t0=time.time();joins=0
 d5=math.sqrt(5)-2
 for ki,row in enumerate(ks):
  R=realize(row['n'],row['code']);sr=sigma(R)
  base={'kernel_index':ki,'kernel_n':row['n'],'kernel_code':row['code'],
        'R_n':len(R),'R_g6':graph6(R),'sigma_R':sr}
  # sigma_R is independent of ports/arms: one record per kernel.
  keep(tops,'sigma_R',dict(base,R_root=0,U_label=None,sigma_G=None,Gamma=None,F=None))
  for v in R:
   for label,U,u,su in AA:
    G=join(U,u,R,v);sg=sigma(G);gam=sg-su-sr;F=gam+sr-d5;joins+=1
    z=dict(base,R_root=v,U_label=label,U_g6=graph6(U),U_root=u,
      sigma_U=su,sigma_G=sg,Gamma=gam,F=F,G_g6=graph6(G),nG=len(G))
    for key in ['sigma_G','Gamma','F']:keep(tops,key,z)
    if sg<0 or F<0:neg.append(z)
 out={'scope':'all 1198 authenticated loopless no-cut-vertex rank-six kernels, each in canonical shortest simple realization (one direct path plus length-2 remaining paths per parallel class), every labelled R port; hostile C5 star/path arm list in script, stated roots; numerical discovery only',
      'counts':{'kernels':len(ks),'arms':len(AA),'joins':joins,'negative_sigma_G_or_F':len(neg)},
      'tops':tops,'negative':neg[:100],'seconds':time.time()-t0}
 (HERE/'kernel-results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'counts':out['counts'],'seconds':out['seconds'],
  'minima':{k:{q:v[0].get(q) for q in ['sigma_R','sigma_G','Gamma','F','kernel_index','kernel_n','R_n','R_root','U_label']} for k,v in tops.items()}},indent=2))
if __name__=='__main__':main()
