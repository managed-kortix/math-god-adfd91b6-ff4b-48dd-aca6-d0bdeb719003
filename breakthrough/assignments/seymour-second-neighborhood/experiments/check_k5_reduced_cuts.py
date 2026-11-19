#!/usr/bin/env python3
"""Independent labelled audit of the 931 reduced k=5 source-cut orbits.

The production module is imported only after this checker has independently
constructed its complete key/multiplicity dictionary.  The audit then requires
set equality, unique production keys, byte-canonical ordering, and the frozen
payload identity; a duplicate/omission trade cannot pass.
"""
import hashlib
import itertools

A=tuple(range(3,9));K=tuple(range(9,15));S=15;V=(0,1)+A+K+(S,)
EXPECTED_KEYS=931
EXPECTED_LABELLED=758181
EXPECTED_BYTES=72991
EXPECTED_SHA256="020cbf130cd806d3a91fa11a29dfdbae67e89e97a47d6e1708c10f3a9f45deb5"


def require(condition,message):
 if not condition: raise RuntimeError(message)


def cell(v,O,H):
 if v==0:return 0
 if v==1:return 1
 if v in A:return 3 if v in H else 2
 if v in K:return 5 if v in H else 4
 return 7 if v in H else 6


def independent_counts():
 counts={};total=0
 for outgoing_tuple in itertools.combinations((1,)+A+K+(S,),8):
  O=set(outgoing_tuple);q=len(O&set(K));non=[v for v in V if v not in O]
  candidates=[v for v in non if v not in (0,1)]
  for mask in range(1<<len(candidates)):
   H={candidates[i] for i in range(len(candidates)) if mask>>i&1};m=1 if q==0 else 2
   for W in itertools.combinations(non,m):
    defect=sum(2 if v in K else (1 if v==S else 0) for v in W)
    incoming=sum(v not in H for v in W)
    if (5 if m==1 else 4)-len(H)-incoming-defect<0:continue
    x=int(1 in O);p=len(O&set(A));r=int(S in O)
    ha=len(H&set(A));hk=len(H&set(K));hs=int(S in H);ns=[0]*8
    for v in W:ns[cell(v,O,H)]+=1
    key=(x,p,q,r,ha,hk,hs,*ns)
    counts[key]=counts.get(key,0)+1;total+=1
 require(len(counts)==EXPECTED_KEYS,f"independent key count {len(counts)} != {EXPECTED_KEYS}")
 require(total==EXPECTED_LABELLED,f"independent labelled count {total} != {EXPECTED_LABELLED}")
 return counts,total


def parse_production(data):
 lines=data.decode("ascii").splitlines();records=[]
 for ordinal,line in enumerate(lines):
  fields=line.split("\t")
  require(len(fields)==7,f"production row {ordinal}: expected seven columns")
  require(int(fields[0])==ordinal,f"production row {ordinal}: bad ordinal")
  key=tuple(map(int,fields[1].split(",")))
  records.append((key,int(fields[2])))
 return records


def main():
 counts,total=independent_counts()
 from k5_reduced_cuts import payload
 data=payload();records=parse_production(data);production={}
 require(len(records)==EXPECTED_KEYS,f"production row count {len(records)} != {EXPECTED_KEYS}")
 for key,multiplicity in records:
  require(key not in production,f"duplicate production key {key}")
  production[key]=multiplicity
 require(set(production)==set(counts),
         f"production key-set mismatch: missing={set(counts)-set(production)} extra={set(production)-set(counts)}")
 for key,value in production.items():
  require(value==counts[key],f"multiplicity mismatch for {key}: {value} != {counts[key]}")
 require(sum(production.values())==total,"production labelled multiplicity mismatch")
 require(len(data)==EXPECTED_BYTES,f"payload bytes {len(data)} != {EXPECTED_BYTES}")
 digest=hashlib.sha256(data).hexdigest()
 require(digest==EXPECTED_SHA256,f"payload sha256 {digest} != {EXPECTED_SHA256}")
 print(f"PASS keys={len(production)} labelled={total} bytes={len(data)} sha256={digest}")


if __name__=="__main__":main()
