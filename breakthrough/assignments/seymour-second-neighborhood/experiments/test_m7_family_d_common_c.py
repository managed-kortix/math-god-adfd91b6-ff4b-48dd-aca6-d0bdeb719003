#!/usr/bin/env python3
"""Hostile finite tests for the common-C family-D nine-case cover."""
import subprocess
import tempfile
from pathlib import Path
from m7_family_d_common_c_cnf import CELLS,TYPES,build,write_cnf

HERE=Path(__file__).resolve().parent
CHECK=HERE/"check_m7_family_d_common_c_cnf.py"

def check(path,cell,kind):
    return subprocess.run([str(CHECK),str(path),"--cell",",".join(map(str,cell)),"--kind",kind],
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)

def require(cond,msg):
    if not cond: raise RuntimeError(msg)

def main():
    seen=[]
    with tempfile.TemporaryDirectory(prefix="m7d-common-c-test-") as d:
        d=Path(d)
        for cell in CELLS:
            for kind in TYPES:
                c,_,_,meta=build(cell,kind); path=d/f"{cell}-{kind}.cnf"; write_cnf(c,path)
                run=check(path,cell,kind)
                require(run.returncode==0,(cell,kind,run.stdout[-1000:]))
                require(tuple(meta["cell"])==cell and meta["kind"]==kind,"bad metadata")
                require(len(meta["S_intersection"])==8 and len(meta["W"])==6,"bad t/W")
                seen.append((cell,kind,len(c.names),len(c.clauses)))
        # Independent checker must reject map, clause, header, truncation, and
        # wrong-case mutations.
        cell,kind=CELLS[0],TYPES[0]; c,_,_,_=build(cell,kind); good=d/"good.cnf"; write_cnf(c,good); raw=good.read_bytes()
        header=f"p cnf {len(c.names)} {len(c.clauses)}".encode()
        mutations=[raw.replace(b"c var 1 a_0_0",b"c var 1 evil_",1),
                   raw.replace(header,f"p cnf {len(c.names)} {len(c.clauses)-1}".encode(),1),
                   raw.replace(b"-1 0\n",b"1 0\n",1),raw[:-4],raw+b"1 0\n"]
        for i,z in enumerate(mutations):
            bad=d/f"bad-{i}.cnf"; bad.write_bytes(z)
            require(check(bad,cell,kind).returncode!=0,f"mutation {i} accepted")
        require(check(good,CELLS[1],kind).returncode!=0,"wrong cell accepted")
        require(check(good,cell,TYPES[1]).returncode!=0,"wrong overlap type accepted")
        # Swapping the one-cross-high placement without exchanging both rooted
        # pairs must change the canonical CNF and be rejected.
        one,_,_,_=build(cell,"oriented-one"); one_path=d/"one.cnf"; write_cnf(one,one_path)
        one_raw=one_path.read_bytes()
        swapped_cross=one_raw.replace(b"-3 0\n",b"3 0\n",1)
        bad_cross=d/"bad-cross-placement.cnf";bad_cross.write_bytes(swapped_cross)
        require(check(bad_cross,cell,"oriented-one").returncode!=0,"cross-high placement mutation accepted")
        # Weakening the universal family-D condition by removing one low's
        # final no-common-witness clause must be rejected byte-for-byte.
        robust_u=one.names["robust_0_1"];robust_q=one.names["robust_0_2"]
        target=f"-{robust_u} -{robust_q} 0\n".encode()
        require(one_raw.count(target)==1,"universal disjointness target is not unique")
        weak=one_raw.replace(target,b"",1);bad_weak=d/"bad-weak-universal.cnf";bad_weak.write_bytes(weak)
        require(check(bad_weak,cell,"oriented-one").returncode!=0,"universal disjointness weakening accepted")
    require({(c,p) for c,p,_,_ in seen}=={(c,p) for c in CELLS for p in TYPES},"nine-case cover mismatch")
    print(f"PASS synchronized cases={len(seen)} cells={len(CELLS)} overlap_types={len(TYPES)}")
    print(f"PASS independent reconstruction all_cases={len(seen)} hostile_mutations={len(mutations)+4}")
    print("dimensions="+repr(seen))

if __name__=="__main__": main()
