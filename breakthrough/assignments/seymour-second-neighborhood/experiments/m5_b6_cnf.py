#!/usr/bin/env python3
"""Standalone full minimal-counterexample CNF for one m=5 B6 placement."""
import argparse
from m5_b6_shapes import placements,SHAPES
from snc_cnf import generate,threshold

LABELS=((0,),tuple(range(1,9)),tuple(range(9,15)),tuple(range(15,18)))
def embedding(name,w):
 used=[0]*4;mp={}
 for v,c in enumerate(w):mp[v]=LABELS[c][used[c]];used[c]+=1
 return mp
def exact(c,o,v):
 if not o or not 0<=v<=len(o):raise ValueError("invalid exact-cardinality request")
 if v==0:c.add(-o[0])
 elif v==len(o):c.add(o[-1])
 else:c.add(o[v-1]);c.add(-o[v])
def emit(i,path,high_c=None,r=None,high_mask=None,cstates=None,tail=None,witnesses=(),arc_status=None,gain_block=None,gain_midpoint=None):
 if not 0<=i<len(placements()):raise ValueError("placement index out of range")
 if high_c is not None and not 0<=high_c<=3:raise ValueError("high_c out of range")
 if r is not None and not 0<=r<=18:raise ValueError("r out of range")
 if high_mask is not None and (any(j not in range(3) for j in high_mask) or len(set(high_mask))!=len(high_mask)):raise ValueError("invalid high mask")
 if cstates is not None and (len(cstates)!=3 or any(x not in (0,1,2) for x in cstates)):raise ValueError("invalid C-pair states")
 if tail is not None and tail not in range(3):raise ValueError("invalid C tail")
 if any(not (isinstance(w,int) and isinstance(u,int) and 0<=w<18 and 0<=u<18 and w!=u) for w,u in witnesses):raise ValueError("invalid witness")
 if arc_status is not None and not witnesses:raise ValueError("arc status requires a witness")
 if (gain_block is not None or gain_midpoint is not None) and arc_status is None:raise ValueError("gain refinement requires arc status")
 if gain_block is not None and gain_block not in range(4):raise ValueError("invalid gain block")
 if gain_midpoint is not None and (gain_midpoint not in range(9,15) or (witnesses and gain_midpoint==witnesses[0][0])):raise ValueError("invalid gain midpoint")
 name,w=placements()[i];n,edges=SHAPES[name];mp=embedding(name,w);E={tuple(sorted((mp[u],mp[v]))) for u,v in edges};c=generate(18,6,5,True,None,None,True)
 for u in range(18):
  for v in range(u+1,18):c.add(c.var(f"h_{u}_{v}") if (u,v) in E else -c.var(f"h_{u}_{v}"))
 if high_c is not None:exact(c,threshold(c,[c.var(f"cnt_d1_{u}_17_9") for u in range(15,18)],f"cube_highC_{high_c}"),high_c)
 if r is not None:exact(c,threshold(c,[c.var(f"a_{u}_{v}") for u in range(15,18) for v in range(9,15)],f"cube_r_{r}"),r)
 if high_mask is not None:
  for j,u in enumerate(range(15,18)):c.add(c.var(f"cnt_d1_{u}_17_9") if j in high_mask else -c.var(f"cnt_d1_{u}_17_9"))
 if cstates is not None:
  for state,(u,v) in zip(cstates,((15,16),(15,17),(16,17))):
   if state==0:c.add(c.var(f"a_{u}_{v}"))
   elif state==1:c.add(c.var(f"a_{v}_{u}"))
   else:c.add(c.var(f"h_{u}_{v}"))
 if tail is not None:
  for u in range(15,18):
   for v in range(9,15):c.add(c.var(f"a_{u}_{v}") if (u==15+tail and v==9) else -c.var(f"a_{u}_{v}"))
 for w,u in witnesses:c.add(c.var(f"wit_{w}_{u}"))
 if arc_status is not None:
  ai,aj=witnesses[0];gain=c.var(f"cube_gain_{ai}_{aj}");paths=[c.var(f"p_{ai}_{k}_{aj}") for k in range(18) if k not in (ai,aj)]
  for z in paths:c.add(-z,gain)
  c.add(-gain,*paths)
  losses=[]
  for t in range(18):
   if t in (ai,aj):continue
   loss=c.var(f"cube_loss_{ai}_{aj}_{t}");losses.append(loss);alts=[c.var(f"p_{ai}_{k}_{t}") for k in range(18) if k not in (ai,aj,t)]
   c.add(-loss,c.var(f"q_{ai}_{t}"));c.add(-loss,c.var(f"a_{aj}_{t}"))
   for z in alts:c.add(-loss,-z)
   c.add(loss,-c.var(f"q_{ai}_{t}"),-c.var(f"a_{aj}_{t}"),*alts)
  g,l=arc_status;c.add(gain if g else -gain);exact(c,threshold(c,losses,f"cube_losses_{ai}_{aj}_{l}"),l)
  if gain_block is not None:
   blocks=((0,),tuple(range(1,9)),tuple(v for v in range(9,15) if v!=ai),tuple(v for v in range(15,18) if v!=aj))
   for b in range(gain_block):
    for k in blocks[b]:c.add(-c.var(f"p_{ai}_{k}_{aj}"))
   c.add(*(c.var(f"p_{ai}_{k}_{aj}") for k in blocks[gain_block]))
  if gain_midpoint is not None:
   candidates=[k for k in range(9,15) if k!=ai]
   for k in candidates:
    if k<gain_midpoint:c.add(-c.var(f"p_{ai}_{k}_{aj}"))
   c.add(c.var(f"p_{ai}_{gain_midpoint}_{aj}"))
 with open(path,"w",encoding="ascii",newline="\n") as f:
  for key,val in c.names.items():f.write(f"c var {val} {key}\n")
  f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
  for z in c.clauses:f.write(" ".join(map(str,z))+" 0\n")
 print(f"index={i} shape={name} word={w} highC={high_c} r={r} high_mask={high_mask} cstates={cstates} tail={tail} support={sorted(E)} vars={len(c.names)} clauses={len(c.clauses)}")
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("index",type=int);p.add_argument("output");p.add_argument("--high-c",type=int);p.add_argument("--r",type=int);a=p.parse_args();emit(a.index,a.output,a.high_c,a.r)
