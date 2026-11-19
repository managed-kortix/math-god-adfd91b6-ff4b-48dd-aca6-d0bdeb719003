#!/usr/bin/env python3
"""Independent checker for the frozen B7 parent-20 packet/witness ledger.

This checker deliberately does not import ``m5_b7_parent20_probe``.  It parses
only the ledger, reconstructs the canonical parent from the independently
checked m=5 parent-cover module, then rebuilds both orbit partitions by direct
labelled enumeration.  It checks decomposition only; it makes no UNSAT claim.
"""
import argparse,hashlib,itertools
from collections import Counter
from pathlib import Path

import check_m5_selector_batch_cnf as cover

FORMAT="m5-b7-parent20-structural-probe-v1"
BRANCH="B7";PARENT=20;C=(16,17);B=tuple(range(9,16));ROOT_FIXED_B=9
EXPECTED_PARENT=("P6","RBACAC",frozenset({(0,9),(1,9),(1,16),(2,16),(2,17)}))
EXPECTED=(3152,"e3807a2c5ca3ae8347f71ae0daa295a7d6f0f996155c06f2de4e86a413886595")

# Independent reconstruction of the parent-cover row using the checker's own
# canonical enumeration, not the producer's placement_rows implementation.
def parent_packet():
    rows=cover.reconstruct_rows(BRANCH)
    shape,word,weight=rows[PARENT]
    holes=cover.project_holes(BRANCH,shape,word)
    if (shape,word,holes)!=EXPECTED_PARENT:raise RuntimeError("canonical parent 20 changed")
    return shape,word,weight,holes

def group(fixed_sets=()):
    fixed_sets=tuple(map(frozenset,fixed_sets))
    for image in itertools.permutations(B):
        p=dict(zip(B,image))
        if p[ROOT_FIXED_B]!=ROOT_FIXED_B:continue
        if all({p[x] for x in S}==S for S in fixed_sets):yield p

def packet_universe():
    holes=parent_packet()[3]
    a={u:sum(tuple(sorted((u,v))) in holes for v in range(9)) for u in C}
    if a!={16:2,17:1}:raise RuntimeError("parent C incidence changed")
    out=set()
    for source in C:
        internal={16:int(source==16),17:int(source==17)}
        for high in itertools.product((0,1),repeat=2):
            sizes={u:high[C.index(u)]+a[u]-1-internal[u] for u in C}
            if any(not 0<=sizes[u]<=len(B) for u in C):continue
            for s16 in itertools.combinations(B,sizes[16]):
                for s17 in itertools.combinations(B,sizes[17]):out.add((source,high,s16,s17))
    return out

def witness_choices(packet):
    source,high,s16,s17=packet;target=33-source
    outsets={16:set(s16),17:set(s17)}
    highs=tuple(u for u,h in zip(C,high) if h)
    choices=[]
    for u in highs:
        internal=(source,) if u==target else ()
        choices.append(internal+tuple(b for b in B if b not in outsets[u]))
    return highs,tuple(choices)

def parse(path):
    raw=Path(path).read_bytes()
    if (len(raw),hashlib.sha256(raw).hexdigest())!=EXPECTED:raise RuntimeError("ledger identity mismatch")
    lines=raw.decode("ascii").splitlines()
    if lines[:1]!=[FORMAT]:raise RuntimeError("format mismatch")
    pf=lines[1].split("\t")
    shape,word,weight,holes=parent_packet()
    if pf != ["parent",str(PARENT),shape,word,str(weight),
              ",".join(f"{u}-{v}" for u,v in sorted(holes))]:raise RuntimeError("parent row mismatch")
    summary=lines[2].split("\t")
    if summary != ["first-signatures","14","witness-leaves","68"]:raise RuntimeError("summary mismatch")
    if lines[3]!="columns\tfirst,key,source,target,high16,high17,outB16,outB17,packet-weight,witness,witness-weight":
        raise RuntimeError("columns mismatch")
    rows=[]
    def vertices(x):return () if x=="-" else tuple(map(int,x.split(",")))
    for line in lines[4:]:
        f=line.split("\t")
        if len(f)!=11:raise RuntimeError("malformed row")
        rows.append({"first":int(f[0]),"key":f[1],"source":int(f[2]),"target":int(f[3]),
          "high":(int(f[4]),int(f[5])),"out":(vertices(f[6]),vertices(f[7])),
          "packet_weight":int(f[8]),"witness":vertices(f[9]),"witness_weight":int(f[10])})
    return raw,rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument("ledger",type=Path);args=ap.parse_args()
    raw,rows=parse(args.ledger)
    byfirst={}
    for row in rows:
        byfirst.setdefault(row["first"],[]).append(row)
    if sorted(byfirst)!=list(range(14)):raise RuntimeError("first ordinals not contiguous")
    G=tuple(group());covered=[];weighted_witness=0
    for ordinal,leaves in sorted(byfirst.items()):
        first=leaves[0]
        stable=("key","source","target","high","out","packet_weight")
        if any(any(row[k]!=first[k] for k in stable) for row in leaves):raise RuntimeError("first packet fields vary")
        if first["target"]!=33-first["source"]:raise RuntimeError("bad C orientation")
        packet=(first["source"],first["high"],*first["out"])
        support={(packet[0],packet[1],tuple(sorted(p[v] for v in packet[2])),tuple(sorted(p[v] for v in packet[3]))) for p in G}
        if len(support)!=first["packet_weight"]:raise RuntimeError("packet orbit weight mismatch")
        covered.extend(support)
        highs,choices=witness_choices(packet);universe=set(itertools.product(*choices)) if choices else {()}
        subgroup=tuple(group(first["out"]));expanded=[]
        for local,row in enumerate(leaves):
            if row["witness"] not in universe:raise RuntimeError("ineligible witness")
            support={tuple(p.get(w,w) for w in row["witness"]) for p in subgroup}
            if len(support)!=row["witness_weight"]:raise RuntimeError("witness orbit weight mismatch")
            expanded.extend(support)
        if set(expanded)!=universe or len(expanded)!=len(set(expanded)):
            raise RuntimeError("witness leaves not disjoint/exhaustive")
        weighted_witness+=first["packet_weight"]*len(universe)
    universe=packet_universe()
    if set(covered)!=universe or len(covered)!=len(set(covered)):raise RuntimeError("packet rows not disjoint/exhaustive")
    if len(rows)!=68 or len(universe)!=92 or weighted_witness!=3081:raise RuntimeError("frozen totals changed")
    print(f"PASS parent=20 first=14 labelled-packets=92 witness-leaves=68 weighted-labelled-witness-packets=3081 bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}")
if __name__=="__main__":main()
