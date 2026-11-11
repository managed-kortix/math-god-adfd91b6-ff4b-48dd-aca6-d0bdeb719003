#!/usr/bin/env python3
"""65 semantic symmetry cubes for the reduced all-seven k6 CNF."""
import argparse
import hashlib
import math

from k6_reduced_cnf import A, B, build

A0=tuple(v for v in A if v!=2)


def keys():
    out=[]
    for x in (0,1):
      for p in range(7):
        q=8-x-p
        if not 0<=q<=7:continue
        cells=(1,1-x,6-p,7-q) # w,z,A-nonout,B-nonout
        for rw in range(cells[0]+1):
         for rz in range(cells[1]+1):
          for ra in range(cells[2]+1):
           for rb in range(cells[3]+1):
            if rw+rz+ra+rb==2:out.append((x,p,q,rw,rz,ra,rb))
    return out


def multiplicity(k):
    x,p,q,rw,rz,ra,rb=k
    return math.comb(6,p)*math.comb(7,q)*math.comb(6-p,ra)*math.comb(7-q,rb)


def representative(k):
    x,p,q,rw,rz,ra,rb=k
    outgoing=({1} if x else set())|set(A0[:p])|set(B[:q])
    non_a=A0[p:];non_b=B[q:]
    witnesses=(({0} if rw else set())|({1} if rz else set())|
               set(non_a[:ra])|set(non_b[:rb]))
    assert len(outgoing)==8 and len(witnesses)==2 and not(outgoing&witnesses)
    return outgoing,witnesses


def payload():
    lines=[]
    for i,k in enumerate(keys()):
        outgoing,witnesses=representative(k)
        lines.append(f"{i}\t{','.join(map(str,k))}\t{multiplicity(k)}\t"
                     f"{','.join(map(str,sorted(outgoing)))}\t"
                     f"{','.join(map(str,sorted(witnesses)))}\n")
    return "".join(lines).encode("ascii")


def emit(index,out):
    k=keys()[index];outgoing,witnesses=representative(k);c=build()
    for v in range(16):
        if v==2:continue
        lit=c.var(f"a_2_{v}")
        c.add(lit if v in outgoing else -lit)
    for v in witnesses:c.add(c.var(f"inacc_2_{v}"))
    with open(out,"w",encoding="ascii",newline="\n") as f:
        for name,num in c.names.items():f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for clause in c.clauses:f.write(" ".join(map(str,clause))+" 0\n")
    print(f"index={index} key={k} multiplicity={multiplicity(k)} vars={len(c.names)} clauses={len(c.clauses)}")


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--list",action="store_true")
    p.add_argument("--index",type=int);p.add_argument("--output");a=p.parse_args()
    if a.list:
        print(payload().decode("ascii"),end="")
        print(f"count={len(keys())} multiplicity={sum(map(multiplicity,keys()))} sha256={hashlib.sha256(payload()).hexdigest()}")
    elif a.index is not None and a.output:emit(a.index,a.output)
    else:p.error("use --list or --index I --output FILE")
