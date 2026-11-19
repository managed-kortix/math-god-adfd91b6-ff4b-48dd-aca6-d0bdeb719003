#!/usr/bin/env python3
"""Fast hostile tests for the family-S h=4 exact-badness machinery."""
import json,subprocess,tempfile
from pathlib import Path
from m7_family_s_badness_pilot import canonical_rows,build_base,build,write_cnf
from m7_family_s_type_rows import rows,swap_row

HERE=Path(__file__).resolve().parent;CHECK=HERE/'check_m7_family_s_badness_cnf.py'

def run(path,*args):return subprocess.run([str(CHECK),str(path),*args],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
def main():
    labelled=[r for r in rows()if r[-1]==4];can=canonical_rows(False)
    assert len(labelled)==81 and sum(r==swap_row(r)for r in labelled)==5 and len(can)==43
    with tempfile.TemporaryDirectory(prefix='m7bad-test-')as d:
        d=Path(d);base=d/'base.cnf';leaf=d/'leaf.cnf'
        c,_,_=build_base();write_cnf(c,base);assert run(base,'--base').returncode==0
        c,_,_=build(can[0]);write_cnf(c,leaf);row=json.dumps(can[0],separators=(',',':'))
        assert run(leaf,'--row',row).returncode==0
        raw=leaf.read_bytes()
        mutations=[raw.replace(b'c var 1 a_0_0',b'c var 1 evil_',1),
                   raw.replace(b'p cnf 23292 89236',b'p cnf 23292 89235',1),
                   raw.replace(b'-1 0\n',b'1 0\n',1),raw+b'1 0\n']
        for i,z in enumerate(mutations):
            bad=d/f'bad{i}.cnf';bad.write_bytes(z);assert run(bad,'--row',row).returncode!=0
    print('PASS badness h4 cover labelled_type_rows=81 fixed=5 canonical_orbits=43')
    print(f'PASS independent checker hostile_mutations={len(mutations)}')
if __name__=='__main__':main()
