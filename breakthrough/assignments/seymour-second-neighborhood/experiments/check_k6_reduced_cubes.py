#!/usr/bin/env python3
"""Independent labelled census for the reduced source-row cube cover."""
import hashlib
import itertools

A=tuple(range(3,9));B=tuple(range(9,16))


def main():
    counts={};total=0
    for out in itertools.combinations((1,)+A+B,8):
        O=set(out);non=[v for v in (0,1)+A+B if v not in O]
        for wit in itertools.combinations(non,2):
            x=int(1 in O);p=len(O&set(A));q=len(O&set(B));W=set(wit)
            key=(x,p,q,int(0 in W),int(1 in W),len(W&set(A)),len(W&set(B)))
            counts[key]=counts.get(key,0)+1;total+=1
    assert len(counts)==65 and total==63063
    # Reconstruct production serialization independently.
    lines=[]
    for i,k in enumerate(sorted(counts)):
        x,p,q,rw,rz,ra,rb=k
        outgoing=({1} if x else set())|set(A[:p])|set(B[:q])
        witnesses=(({0} if rw else set())|({1} if rz else set())|
                   set(A[p:p+ra])|set(B[q:q+rb]))
        lines.append(f"{i}\t{','.join(map(str,k))}\t{counts[k]}\t"
                     f"{','.join(map(str,sorted(outgoing)))}\t"
                     f"{','.join(map(str,sorted(witnesses)))}\n")
    data="".join(lines).encode("ascii")
    print(f"PASS keys=65 labelled={total} sha256={hashlib.sha256(data).hexdigest()}")


if __name__=="__main__":main()
