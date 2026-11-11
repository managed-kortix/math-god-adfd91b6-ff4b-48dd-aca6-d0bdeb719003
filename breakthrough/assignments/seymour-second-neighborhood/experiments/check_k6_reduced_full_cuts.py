#!/usr/bin/env python3
"""Independent labelled census for all 1,110 complete source-cut orbits."""
import hashlib
import itertools

A=tuple(range(3,9));B=tuple(range(9,16));V=(0,1)+A+B


def main():
 counts={};total=0
 for O in itertools.combinations((1,)+A+B,8):
  O=set(O);non=[v for v in V if v not in O]
  candidates=[v for v in non if v not in (0,1)]
  for mask in range(1<<len(candidates)):
   H={candidates[i] for i in range(len(candidates)) if mask>>i&1}
   for W in itertools.combinations(non,2):
    x=int(1 in O);p=len(O&set(A));q=len(O&set(B));ha=len(H&set(A));hb=len(H&set(B))
    def cell(v):
     if v==0:return 0
     if v==1:return 1
     if v in A:return 3 if v in H else 2
     return 5 if v in H else 4
    i,j=sorted(map(cell,W));k=(x,p,q,ha,hb,i,j);counts[k]=counts.get(k,0)+1;total+=1
 assert len(counts)==1110 and total==3171168
 lines=[]
 for n,k in enumerate(sorted(counts)):
  x,p,q,ha,hb,i,j=k;AO=A[:p];AH=A[p:p+ha];AI=A[p+ha:];BO=B[:q];BH=B[q:q+hb];BI=B[q+hb:]
  groups=({0},({1} if not x else set()),set(AI),set(AH),set(BI),set(BH));need=[0]*6;need[i]+=1;need[j]+=1
  W=set()
  for t,c in enumerate(need):W.update(sorted(groups[t])[:c])
  O=({1} if x else set())|set(AO)|set(BO);H=set(AH)|set(BH);I={0}|({1} if not x else set())|set(AI)|set(BI)
  lines.append(f"{n}\t{','.join(map(str,k))}\t{counts[k]}\t{','.join(map(str,sorted(O)))}\t{','.join(map(str,sorted(I)))}\t{','.join(map(str,sorted(H)))}\t{','.join(map(str,sorted(W)))}\n")
 data="".join(lines).encode();print(f"PASS keys=1110 labelled={total} sha256={hashlib.sha256(data).hexdigest()}")

if __name__=="__main__":main()
