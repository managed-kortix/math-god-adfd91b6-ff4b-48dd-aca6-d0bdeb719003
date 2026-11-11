#!/usr/bin/env python3
"""Map complete-cut cubes to the 36 hard primary k6 parents."""
import json

from k6_reduced_full_cuts import keys as full_keys
from k6_reduced_cubes import keys as primary_keys


def parent(k):
    x,p,q,ha,hb,i,j=k
    # Full cells w,z,AI,AH,BI,BH collapse to primary w,z,A-nonout,B-nonout.
    collapse=(0,1,2,2,3,3);a,b=sorted((collapse[i],collapse[j]))
    counts=[0]*4;counts[a]+=1;counts[b]+=1
    return (x,p,q,*counts)


def hard_indices(path="k6-reduced-scout-20s.json"):
    with open(path,encoding="ascii") as f:d=json.load(f)
    if "rows" in d:return {tuple(row["key"]) for row in d["rows"] if row["status"]=="UNKNOWN"}
    return {primary_keys()[i] for i in d["unknown_indices"]}


def main():
    hard=hard_indices();children=[(i,k,parent(k)) for i,k in enumerate(full_keys()) if parent(k) in hard]
    print(f"hard_parents={len(hard)} hard_children={len(children)}")
    for i,k,p in children:print(f"{i}\t{','.join(map(str,k))}\t{','.join(map(str,p))}")


if __name__=="__main__":main()
