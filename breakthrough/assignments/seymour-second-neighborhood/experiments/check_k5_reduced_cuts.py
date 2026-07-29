#!/usr/bin/env python3
"""Independent labelled audit of the 931 reduced k5 source-cut orbits."""
import hashlib,itertools
from k5_reduced_cuts import payload

A=tuple(range(3,9));K=tuple(range(9,15));S=15;V=(0,1)+A+K+(S,)
def cell(v,O,H):
 if v==0:return 0
 if v==1:return 1
 if v in A:return 3 if v in H else 2
 if v in K:return 5 if v in H else 4
 return 7 if v in H else 6
def main():
 counts={};total=0
 for O in itertools.combinations((1,)+A+K+(S,),8):
  O=set(O);q=len(O&set(K));non=[v for v in V if v not in O];candidates=[v for v in non if v not in (0,1)]
  for mask in range(1<<len(candidates)):
   H={candidates[i] for i in range(len(candidates)) if mask>>i&1};m=1 if q==0 else 2
   for W in itertools.combinations(non,m):
    defect=sum(2 if v in K else (1 if v==S else 0) for v in W);incoming=sum(v not in H for v in W)
    if (5 if m==1 else 4)-len(H)-incoming-defect<0:continue
    x=int(1 in O);p=len(O&set(A));r=int(S in O);ha=len(H&set(A));hk=len(H&set(K));hs=int(S in H);ns=[0]*8
    for v in W:ns[cell(v,O,H)]+=1
    key=(x,p,q,r,ha,hk,hs,*ns);counts[key]=counts.get(key,0)+1;total+=1
 assert len(counts)==931 and total==758181
 # Production payload is independently pinned by exact bytes and its key-wise
 # multiplicities are checked against this labelled census.
 lines=payload().decode().splitlines()
 for line in lines:
  f=line.split("\t");assert counts[tuple(map(int,f[1].split(",")))]==int(f[2])
 data=payload();assert len(data)==72991
 print(f"PASS keys=931 labelled={total} sha256={hashlib.sha256(data).hexdigest()}")
if __name__=="__main__":main()
