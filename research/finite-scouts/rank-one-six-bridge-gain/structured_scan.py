#!/usr/bin/env python3
"""Broader but sparse structured scan; discovery only."""
import json
from pathlib import Path
import networkx as nx, numpy as np
from search import beta,sigma,join,rank6_cores,attach_leaves,attach_path

def main():
 Us=[]
 for q in range(3,21):
  c=nx.cycle_graph(q)
  for r in sorted(set([0,1,q//2])):Us.append((f'C{q}-r{r}',c,r))
  for leaves in [1,2,5,10,25]:
   h=attach_leaves(c,0,leaves)
   for r in sorted(set([0,1,q//2,q])):Us.append((f'C{q}+S{leaves}-r{r}',h,r))
  for path in [1,2,5,10,20]:
   h=attach_path(c,0,path)
   for r in sorted(set([0,1,q//2,q+path-1])):Us.append((f'C{q}+P{path}-r{r}',h,r))
 Hs=[]
 for name,c in rank6_cores():
  for leaves in [0,1,2,5,10,25]:
   h=c if leaves==0 else attach_leaves(c,0,leaves)
   for r in sorted(set([0,len(c)-1,len(h)-1])):Hs.append((f'{name}+S{leaves}-r{r}',h,r))
  for path in [1,2,5,10,20]:
   h=attach_path(c,0,path)
   for r in sorted(set([0,len(c),len(h)-1])):Hs.append((f'{name}+P{path}-r{r}',h,r))
 rng=np.random.default_rng(3)
 for n in [6,7,8,10,12]:
  for j in range(12):
   h=nx.random_labeled_tree(n,seed=int(rng.integers(1<<31)))
   non=list(nx.non_edges(h));rng.shuffle(non);h.add_edges_from(non[:6])
   if beta(h)==6:
    for r in rng.choice(n,size=min(2,n),replace=False):Hs.append((f'random-{n}.{j}-r{r}',h,int(r)))
 UU=[(a,g,r,sigma(g)) for a,g,r in Us];HH=[(a,g,r,sigma(g)) for a,g,r in Hs]
 best={k:[] for k in ['sigma_G','payment','Gamma']};neg=[]
 def keep(k,row):best[k].append(row);best[k].sort(key=lambda x:x[k]);del best[k][20:]
 for un,U,u,su in UU:
  for hn,H,v,sh in HH:
   G=join(U,u,H,v);sg=sigma(G);row={'U':un,'H':hn,'sigma_U':su,'sigma_H':sh,
      'sigma_G':sg,'Gamma':sg-su-sh,'payment':sg-sh,'nG':len(G)}
   for k in best:keep(k,row)
   if sg< -1e-8:neg.append(row)
 out={'counts':{'U':len(UU),'H':len(HH),'joins':len(UU)*len(HH),'negative':len(neg)},'tops':best,
      'scope':'selected cycles with stars/paths, four named rank-six cores with stars/paths, and random tree-plus-six-edge cores; nonexhaustive'}
 Path(__file__).with_name('structured-results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'counts':out['counts'],'minima':{k:v[0] for k,v in best.items()}},indent=2))
if __name__=='__main__':main()
