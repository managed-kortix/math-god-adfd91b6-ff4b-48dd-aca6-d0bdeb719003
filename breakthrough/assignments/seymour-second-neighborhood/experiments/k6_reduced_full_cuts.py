#!/usr/bin/env python3
"""Complete source-2 cut/witness orbits refining the 65 primary cubes."""
import argparse
import hashlib
import itertools
import math

from k6_reduced_cnf import A,B,build

A0=tuple(v for v in A if v!=2)
CELLS=("w","z","AI","AH","BI","BH")


def keys():
 out=[]
 for x in (0,1):
  for p in range(7):
   q=8-x-p
   if not 0<=q<=7:continue
   for ha in range(6-p+1):
    for hb in range(7-q+1):
     sizes=(1,1-x,6-p-ha,ha,7-q-hb,hb)
     for i in range(6):
      for j in range(i,6):
       need=[0]*6;need[i]+=1;need[j]+=1
       if all(need[t]<=sizes[t] for t in range(6)):
        out.append((x,p,q,ha,hb,i,j))
 return out


def representative(k):
 x,p,q,ha,hb,i,j=k
 AO=A0[:p];AH=A0[p:p+ha];AI=A0[p+ha:]
 BO=B[:q];BH=B[q:q+hb];BI=B[q+hb:]
 groups=({0},({1} if not x else set()),set(AI),set(AH),set(BI),set(BH))
 need=[0]*6;need[i]+=1;need[j]+=1
 witnesses=set()
 for t,n in enumerate(need):witnesses.update(sorted(groups[t])[:n])
 outgoing=({1} if x else set())|set(AO)|set(BO)
 holes=set(AH)|set(BH)
 incoming=({0}|({1} if not x else set())|set(AI)|set(BI))
 assert len(outgoing)==8 and len(witnesses)==2
 return outgoing,incoming,holes,witnesses


def multiplicity(k):
 x,p,q,ha,hb,i,j=k
 sizes=(1,1-x,6-p-ha,ha,7-q-hb,hb);need=[0]*6;need[i]+=1;need[j]+=1
 return (math.comb(6,p)*math.comb(6-p,ha)*math.comb(7,q)*math.comb(7-q,hb)*
         math.prod(math.comb(sizes[t],need[t]) for t in range(6)))


def payload():
 lines=[]
 for n,k in enumerate(keys()):
  O,I,H,W=representative(k)
  lines.append(f"{n}\t{','.join(map(str,k))}\t{multiplicity(k)}\t"
               f"{','.join(map(str,sorted(O)))}\t{','.join(map(str,sorted(I)))}\t"
               f"{','.join(map(str,sorted(H)))}\t{','.join(map(str,sorted(W)))}\n")
 return "".join(lines).encode("ascii")


def emit(index,path,packet_pressure=False):
 k=keys()[index];O,I,H,W=representative(k);c=build()
 for v in range(16):
  if v==2:continue
  uv=c.var(f"a_2_{v}");vu=c.var(f"a_{v}_2")
  if v in O:c.add(uv)
  elif v in I:c.add(vu)
  else:c.add(-uv);c.add(-vu)
 for v in W:c.add(c.var(f"inacc_2_{v}"))
 if packet_pressure:
  # For selected inaccessible witnesses t,u, exact degree and the global
  # six-hole identity imply e^+({t,u},R) <= s, where
  # s=5-|H|-|W intersect I|-2|W intersect B| and |R|=5.
  s=5-len(H)-len(W&I)-2*len(W&set(B))
  if s<0:c.add()
  else:
   R=set(range(16))-({2}|O|W)
   lits=[c.var(f"a_{t}_{r}") for t in sorted(W) for r in sorted(R)]
   for combo in itertools.combinations(lits,s+1):c.add(*(-v for v in combo))
 with open(path,"w",encoding="ascii",newline="\n") as f:
  for name,num in c.names.items():f.write(f"c var {num} {name}\n")
  f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
  for clause in c.clauses:f.write(" ".join(map(str,clause))+" 0\n")
 print(f"index={index} key={k} multiplicity={multiplicity(k)}")


if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--list",action="store_true");p.add_argument("--index",type=int);p.add_argument("--output");p.add_argument("--packet-pressure",action="store_true");a=p.parse_args()
 if a.list:
  print(payload().decode(),end="");print(f"count={len(keys())} multiplicity={sum(map(multiplicity,keys()))} sha256={hashlib.sha256(payload()).hexdigest()}")
 elif a.index is not None and a.output:emit(a.index,a.output,a.packet_pressure)
 else:p.error("use --list or --index I --output FILE")
