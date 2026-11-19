#!/usr/bin/env python3
"""Exact structural probe for canonical m=5 B7 P6 parent 20.

Research utility only.  It reconstructs a disjoint/exhaustive first split by the
labelled C packet (internal orientation, degree-nine mask, and exact C->B
neighbourhoods modulo the stabilizer of the parent), then a second split by one
selected robust deletion witness for every high C vertex.  It does not claim
that any leaf is UNSAT unless a retained proof is separately replayed.
"""
import hashlib,itertools,json,subprocess,tempfile,time
from collections import Counter
from functools import lru_cache
from pathlib import Path

from snc_cnf import generate
import m5_selector_batch_cnf as parent_cover

FORMAT="m5-b7-parent20-structural-probe-v1"
BRANCH="B7";PARENT=20;C=(16,17);B=tuple(range(9,16));ROOT_FIXED_B=9
EXPECTED_PARENT=("P6",(0,2,1,3,1,3),frozenset({(0,9),(1,9),(1,16),(2,16),(2,17)}))

def parent_packet(index=PARENT):
    shape,word,weight=parent_cover.placement_rows(BRANCH)[index]
    holes=parent_cover.hole_projection(BRANCH,shape,word)
    if index==PARENT and (shape,word,holes)!=EXPECTED_PARENT:
        raise RuntimeError("canonical B7 parent 20 changed")
    return shape,word,weight,holes

def stabilizer(fixed_sets=()):
    """Permutations of B fixing root-hole endpoint 9 and every fixed subset."""
    fixed_sets=tuple(map(frozenset,fixed_sets))
    for image in itertools.permutations(B):
        permutation=dict(zip(B,image))
        if permutation[ROOT_FIXED_B]!=ROOT_FIXED_B:continue
        if all({permutation[v] for v in subset}==subset for subset in fixed_sets):
            yield permutation

def subset_orbits(size,group):
    universe=tuple(itertools.combinations(B,size));remaining=set(universe);out=[]
    while remaining:
        seed=min(remaining);orbit={tuple(sorted(p[v] for v in seed)) for p in group}
        if not orbit<=remaining:raise RuntimeError("invalid subset action")
        remaining-=orbit;out.append((min(orbit),len(orbit)))
    return tuple(out)

def bset_pair_orbits(size16,size17):
    """Orbits of ordered exact C->B neighbourhood pairs under Stab_B(9)."""
    group=tuple(stabilizer())
    universe={(x,y) for x in itertools.combinations(B,size16) for y in itertools.combinations(B,size17)}
    remaining=set(universe);out=[]
    while remaining:
        seed=min(remaining)
        orbit={(tuple(sorted(p[v] for v in seed[0])),tuple(sorted(p[v] for v in seed[1]))) for p in group}
        if not orbit<=remaining:raise RuntimeError("invalid pair action")
        remaining-=orbit;out.append((min(orbit),len(orbit)))
    return tuple(out)

def first_signatures():
    """Exact feasible C packet orbits, before any SAT solving.

    Put a_c=m(c,R union A).  Parent 20 has (a_16,a_17)=(2,1), no
    C--B hole, and no internal-C hole.  Every present R/A--C pair points
    C->(R/A), so the exact degree row is

        8+x_c = 9-a_c+d_C^+(c)+e(c,B),
        e(c,B) = x_c+a_c-1-d_C^+(c).

    The internal C pair is present, so exactly one orientation.
    """
    out=[]
    holes=parent_packet()[3]
    a_holes={u:sum(tuple(sorted((u,v))) in holes for v in range(9)) for u in C}
    if a_holes!={16:2,17:1}:raise RuntimeError("parent C--(R union A) incidence changed")
    for source,target in ((16,17),(17,16)):
        internal={16:int(source==16),17:int(source==17)}
        for high16,high17 in itertools.product((0,1),repeat=2):
            high={16:high16,17:high17}
            sizes={u:high[u]+a_holes[u]-1-internal[u] for u in C}
            if any(not 0<=sizes[u]<=len(B) for u in C):continue
            for local,((s16,s17),weight) in enumerate(bset_pair_orbits(sizes[16],sizes[17])):
                out.append({"ordinal":len(out),"key":f"{source}to{target}-h{high16}{high17}-o{local:02d}",
                    "source":source,"target":target,"high":(high16,high17),
                    "outB":(s16,s17),"orbit_weight":weight})
    expected=0
    for source in C:
        internal={16:int(source==16),17:int(source==17)}
        for h16,h17 in itertools.product((0,1),repeat=2):
            sizes={16:h16+a_holes[16]-1-internal[16],17:h17+a_holes[17]-1-internal[17]}
            if all(0<=sizes[u]<=len(B) for u in C):
                expected+=len(tuple(itertools.combinations(B,sizes[16])))*len(tuple(itertools.combinations(B,sizes[17])))
    if sum(x["orbit_weight"] for x in out)!=expected:
        raise RuntimeError("first signature orbit weights do not cover labelled packets")
    return tuple(out)

def witness_candidates(signature,u):
    """All possible robust in-neighbours of high C vertex u.

    R and A have no arcs into C.  The other C vertex is eligible exactly when
    it is the internal predecessor.  A B vertex is eligible exactly when it is
    not in u's exact C->B neighbourhood.  (All C--B pairs are present.)
    """
    source,target=signature["source"],signature["target"]
    outB=set(signature["outB"][C.index(u)])
    internal=(source,) if u==target else ()
    return internal+tuple(b for b in B if b not in outB)

def witness_orbits(signature):
    high_vertices=tuple(u for u,h in zip(C,signature["high"]) if h)
    choices=tuple(witness_candidates(signature,u) for u in high_vertices)
    universe=set(itertools.product(*choices)) if choices else {()}
    group=tuple(stabilizer(signature["outB"]));remaining=set(universe);out=[]
    while remaining:
        seed=min(remaining)
        orbit={tuple(p.get(w,w) for w in seed) for p in group}
        if not orbit<=remaining:raise RuntimeError("invalid witness action")
        remaining-=orbit;out.append((min(orbit),len(orbit)))
    if sum(weight for _,weight in out)!=len(universe):raise RuntimeError("witness orbit weight mismatch")
    return high_vertices,choices,tuple(out),len(group)

def add_parent_units(cnf):
    _,_,_,holes=parent_packet()
    for pair in parent_cover.PAIRS:
        cnf.add(cnf.var(f"h_{pair[0]}_{pair[1]}") if pair in holes else -cnf.var(f"h_{pair[0]}_{pair[1]}"))

def build_leaf(signature,witnesses=()):
    cnf=generate(18,7,5,robust_witness=True,arc_minimal=True);add_parent_units(cnf)
    cnf.add(cnf.var(f"a_{signature['source']}_{signature['target']}"))
    for u,high,outB in zip(C,signature["high"],signature["outB"]):
        cnf.add(cnf.var(f"cnt_d1_{u}_17_9") if high else -cnf.var(f"cnt_d1_{u}_17_9"))
        for b in B:cnf.add(cnf.var(f"a_{u}_{b}") if b in outB else -cnf.var(f"a_{u}_{b}"))
    high_vertices,_,orbits,_=witness_orbits(signature)
    # The empty tuple is the unique genuine witness choice when no C vertex is
    # high.  Validate all callers uniformly; do not silently accept an omitted
    # witness for a high signature.
    if witnesses not in {rep for rep,_ in orbits}:raise ValueError("not a canonical witness orbit")
    for u,w in zip(high_vertices,witnesses):cnf.add(cnf.var(f"wit_{w}_{u}"))
    return cnf

def payload():
    records=[FORMAT]
    shape,word,weight,holes=parent_packet()
    records += [f"parent\t{PARENT}\t{shape}\t{''.join(parent_cover.CELLS[x] for x in word)}\t{weight}\t"+
                ','.join(f'{u}-{v}' for u,v in sorted(holes)),
                "columns\tfirst,key,source,target,high16,high17,outB16,outB17,packet-weight,witness,witness-weight"]
    leaves=0
    for sig in first_signatures():
        high_vertices,choices,orbits,group_size=witness_orbits(sig)
        for local,(W,weight) in enumerate(orbits):
            records.append(f"{sig['ordinal']:02d}\t{sig['key']}\t{sig['source']}\t{sig['target']}\t"+
                f"{sig['high'][0]}\t{sig['high'][1]}\t"+
                f"{','.join(map(str,sig['outB'][0])) or '-'}\t{','.join(map(str,sig['outB'][1])) or '-'}\t"+
                f"{sig['orbit_weight']}\t{','.join(map(str,W)) or '-'}\t{weight}")
            leaves+=1
    records.insert(2,f"first-signatures\t{len(first_signatures())}\twitness-leaves\t{leaves}")
    return ('\n'.join(records)+'\n').encode('ascii')

def verify_cover():
    signatures=first_signatures();keys=[s['key'] for s in signatures]
    if len(keys)!=len(set(keys)):raise RuntimeError("duplicate first key")
    # Independently reconstruct every labelled feasible packet and assert unique
    # canonical-orbit membership by explicit group action.
    labelled=[];holes=parent_packet()[3]
    a_holes={u:sum(tuple(sorted((u,v))) in holes for v in range(9)) for u in C}
    for source,target in ((16,17),(17,16)):
      internal={16:int(source==16),17:int(source==17)}
      for high in itertools.product((0,1),repeat=2):
       sizes={u:high[C.index(u)]+a_holes[u]-1-internal[u] for u in C}
       if any(not 0<=sizes[u]<=len(B) for u in C):continue
       for s16 in itertools.combinations(B,sizes[16]):
        for s17 in itertools.combinations(B,sizes[17]):labelled.append((source,high,s16,s17))
    covered=[]
    G=tuple(stabilizer())
    supports=[]
    for sig in signatures:
      support={(sig['source'],sig['high'],tuple(sorted(p[v] for v in sig['outB'][0])),tuple(sorted(p[v] for v in sig['outB'][1]))) for p in G}
      if len(support)!=sig['orbit_weight']:
          raise RuntimeError("first signature orbit weight is wrong")
      supports.append(support);covered.extend(support)
    # Reconstruct pairwise disjointness and exhaustion without trusting the
    # representative-generation routine or its orbit weights.
    if (set(covered)!=set(labelled) or len(covered)!=len(set(covered))
            or sum(s['orbit_weight'] for s in signatures)!=len(labelled)):
        raise RuntimeError("first split is not disjoint/exhaustive")
    leaf_count=0;labelled_witness=0
    for sig in signatures:
        high,choices,orbits,_=witness_orbits(sig)
        leaf_count+=len(orbits);labelled_witness+=sig['orbit_weight']*sum(w for _,w in orbits)
        universe=set(itertools.product(*choices)) if choices else {()}
        subgroup=tuple(stabilizer(sig['outB']));supports=[]
        for rep,weight in orbits:
            support={tuple(permutation.get(x,x) for x in rep) for permutation in subgroup}
            if len(support)!=weight:raise RuntimeError("witness orbit weight is wrong")
            supports.append(support)
        expanded=[item for support in supports for item in support]
        if set(expanded)!=universe or len(expanded)!=len(set(expanded)):
            raise RuntimeError("witness split is not disjoint/exhaustive")
    data=payload()
    return {"format":FORMAT,"parent":PARENT,"first_signatures":len(signatures),"first_labelled_packets":len(labelled),
            "witness_leaves":leaf_count,"weighted_labelled_witness_packets":labelled_witness,
            "payload_bytes":len(data),"payload_sha256":hashlib.sha256(data).hexdigest()}

def write_cnf(path,first,witness):
    signatures=first_signatures();sig=signatures[first]
    _,_,orbits,_=witness_orbits(sig);W=orbits[witness][0]
    cnf=build_leaf(sig,W)
    with Path(path).open('w',encoding='ascii',newline='\n') as f:
        for name,number in cnf.names.items():f.write(f"c var {number} {name}\n")
        f.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:f.write(' '.join(map(str,clause))+' 0\n')

def scout(solver,seconds):
    rows=[]
    for sig in first_signatures():
        high,_,orbits,_=witness_orbits(sig)
        for witness_ordinal,(W,weight) in enumerate(orbits):
            cnf=build_leaf(sig,W)
            with tempfile.NamedTemporaryFile(mode="w",suffix=".cnf",encoding="ascii") as handle:
                handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
                for clause in cnf.clauses:handle.write(' '.join(map(str,clause))+' 0\n')
                handle.flush();start=time.monotonic()
                result=subprocess.run(["timeout",str(seconds),solver,"-q",handle.name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                elapsed=round(time.monotonic()-start,3)
            status={10:"SAT",20:"UNSAT",124:"UNKNOWN"}.get(result.returncode,f"EXIT_{result.returncode}")
            row={"first":sig["ordinal"],"key":sig["key"],"witness":witness_ordinal,"representative":W,
                 "packet_weight":sig["orbit_weight"],"witness_weight":weight,"status":status,"seconds":elapsed}
            rows.append(row);print(json.dumps(row,sort_keys=True),flush=True)
    return rows

def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--payload');p.add_argument('--cnf');p.add_argument('--first',type=int);p.add_argument('--witness',type=int)
    p.add_argument('--scout-solver');p.add_argument('--seconds',type=int,default=10);p.add_argument('--scout-output');a=p.parse_args()
    result=verify_cover()
    if a.payload:Path(a.payload).write_bytes(payload())
    if a.cnf:
        if a.first is None or a.witness is None:p.error('--cnf requires --first and --witness')
        write_cnf(a.cnf,a.first,a.witness)
    if a.scout_solver:
        rows=scout(a.scout_solver,a.seconds)
        data={"format":FORMAT,"cover":result,"solver":a.scout_solver,"cap_seconds":a.seconds,"rows":rows}
        if a.scout_output:Path(a.scout_output).write_text(json.dumps(data,sort_keys=True)+"\n")
        result={**result,"scout_counts":dict(Counter(row["status"] for row in rows))}
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
