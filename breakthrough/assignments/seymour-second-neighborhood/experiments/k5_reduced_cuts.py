#!/usr/bin/env python3
"""The 931 packet-feasible complete source-cut orbits for reduced k5."""
import argparse,hashlib,itertools,math
from k5_reduced_cnf import A,K,S,build,exact
from snc_cnf import threshold

A0=tuple(v for v in A if v!=2); CELLS=("W","ZI","AI","AH","KI","KH","SI","SH")
INC=(1,1,1,0,1,0,1,0);DEF=(0,0,0,0,2,2,1,1)

def compositions(n,sizes):
 for x in itertools.product(*(range(min(n,s)+1) for s in sizes)):
  if sum(x)==n:yield x

def keys():
 out=[]
 for x,p,q,r in itertools.product((0,1),range(7),range(7),(0,1)):
  if x+p+q+r!=8:continue
  m=1 if q==0 else 2
  for ha in range(7-p):
   for hk in range(7-q):
    for hs in range(2-r):
     sizes=(1,1-x,6-p-ha,ha,6-q-hk,hk,1-r-hs,hs)
     for ns in compositions(m,sizes):
      h=ha+hk+hs;rhs=(5 if m==1 else 4)-h-sum(ns[i]*(INC[i]+DEF[i]) for i in range(8))
      if rhs>=0:out.append((x,p,q,r,ha,hk,hs,*ns))
 return out

def representative(k):
 x,p,q,r,ha,hk,hs,*ns=k;AO=A0[:p];AH=A0[p:p+ha];AI=A0[p+ha:];KO=K[:q];KH=K[q:q+hk];KI=K[q+hk:]
 groups=({0},({1} if not x else set()),set(AI),set(AH),set(KI),set(KH),({S} if not r and not hs else set()),({S} if hs else set()))
 W=set()
 for g,n in zip(groups,ns):W.update(sorted(g)[:n])
 O=({1} if x else set())|set(AO)|set(KO)|({S} if r else set());H=set(AH)|set(KH)|({S} if hs else set());I={0}|({1} if not x else set())|set(AI)|set(KI)|({S} if not r and not hs else set())
 return O,I,H,W

def multiplicity(k):
 x,p,q,r,ha,hk,hs,*ns=k;sizes=(1,1-x,6-p-ha,ha,6-q-hk,hk,1-r-hs,hs)
 return math.comb(6,p)*math.comb(6-p,ha)*math.comb(6,q)*math.comb(6-q,hk)*math.prod(math.comb(s,n) for s,n in zip(sizes,ns))

def payload():
 lines=[]
 for i,k in enumerate(keys()):
  O,I,H,W=representative(k)
  lines.append(f"{i}\t{','.join(map(str,k))}\t{multiplicity(k)}\t{','.join(map(str,sorted(O)))}\t{','.join(map(str,sorted(I)))}\t{','.join(map(str,sorted(H)))}\t{','.join(map(str,sorted(W)))}\n")
 return "".join(lines).encode("ascii")

def emit(i,path):
 k=keys()[i];O,I,H,W=representative(k);c=build(explicit_holes=True)
 for v in range(16):
  if v==2:continue
  av=c.var(f"a_2_{v}");va=c.var(f"a_{v}_2")
  if v in O:c.add(av)
  elif v in I:c.add(va)
  else:c.add(-av);c.add(-va)
 for v in W:c.add(c.var(f"inacc_2_{v}"))
 m=len(W);h=len(H);incoming=len(W&I);defect=sum(2 if v in K else (1 if v==S else 0) for v in W);rhs=(5 if m==1 else 4)-h-incoming-defect
 R=set(range(16))-({2}|O|W);support={tuple(sorted((2,v))) for v in H}|{tuple(sorted((t,y))) for t in W for y in O}
 if m==2:support.add(tuple(sorted(W)))
 events=[c.var(f"a_{t}_{v}") for t in W for v in R]+[c.var(f"hole_{u}_{v}") for u in range(16) for v in range(u+1,16) if (u,v) not in support]
 exact(c,threshold(c,events,"packet_identity"),rhs)
 with open(path,"w",encoding="ascii",newline="\n") as f:
  for n,v in c.names.items():f.write(f"c var {v} {n}\n")
  f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
  for z in c.clauses:f.write(" ".join(map(str,z))+" 0\n")
 print(f"index={i} key={k} multiplicity={multiplicity(k)}")

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--list",action="store_true");p.add_argument("--index",type=int);p.add_argument("--output");a=p.parse_args()
 if a.list:print(payload().decode(),end="");print(f"count={len(keys())} multiplicity={sum(map(multiplicity,keys()))} sha256={hashlib.sha256(payload()).hexdigest()}")
 elif a.index is not None and a.output:emit(a.index,a.output)
 else:p.error("use --list or --index I --output FILE")
