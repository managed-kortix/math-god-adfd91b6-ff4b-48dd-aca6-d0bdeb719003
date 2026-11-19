#!/usr/bin/env python3
"""Fast hostile tests for the family-S h=4 exact-badness machinery."""
import json,subprocess,tempfile
from pathlib import Path
from m7_family_s_badness_pilot import canonical_rows,build_base,build,write_cnf
from m7_family_s_type_rows import rows,swap_row

HERE=Path(__file__).resolve().parent;CHECK=HERE/'check_m7_family_s_badness_cnf.py'


def require(condition,message):
    if not condition:
        raise RuntimeError(message)


def run(path,*args):
    return subprocess.run([str(CHECK),str(path),*args],stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,text=True)


def main():
    labelled=[row for row in rows() if row[-1]==4];canonical=canonical_rows(False,4)
    require(len(labelled)==81,'labelled h4 row count')
    require(sum(row==swap_row(row) for row in labelled)==5,'fixed h4 row count')
    require(len(canonical)==43 and len(set(canonical))==43,'canonical h4 universe')
    with tempfile.TemporaryDirectory(prefix='m7bad-test-') as td:
        td=Path(td);base=td/'base.cnf';leaf=td/'leaf.cnf'
        c,_,_=build_base();write_cnf(c,base)
        require(run(base,'--base').returncode==0,'independent base check')
        c,_,_=build(canonical[0]);write_cnf(c,leaf);row=json.dumps(canonical[0],separators=(',',':'))
        require(run(leaf,'--row',row).returncode==0,'independent leaf check')
        raw=leaf.read_bytes()
        mutations=[raw.replace(b'c var 1 a_0_0',b'c var 1 evil_',1),
                   raw.replace(b'p cnf 23292 89236',b'p cnf 23292 89235',1),
                   raw.replace(b'-1 0\n',b'1 0\n',1),raw+b'1 0\n']
        for i,mutated in enumerate(mutations):
            bad=td/f'bad{i}.cnf';bad.write_bytes(mutated)
            require(run(bad,'--row',row).returncode!=0,f'CNF mutation {i} accepted')
    print('PASS badness h4 cover labelled_type_rows=81 fixed=5 canonical_orbits=43')
    print(f'PASS independent checker hostile_mutations={len(mutations)}')


if __name__=='__main__':
    main()
