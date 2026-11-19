#!/usr/bin/env python3
"""Solve a bounded family-S exact-badness pilot and export SAT witnesses.

The solver is intentionally external.  This script validates its status and
full assignment against every emitted CNF clause before exporting an arc list;
``m7_family_s_badness_check.py`` then performs the independent semantic audit.
UNSAT output is only a scout result unless accompanied by a checked proof.
"""
import argparse,subprocess,tempfile
from pathlib import Path
from m7_family_s_badness_pilot import canonical_rows,build,write_cnf

N=18


def read_model(path):
    status=None;vals={}
    for line in Path(path).read_text(encoding='ascii').splitlines():
        if line.startswith('s '): status=line[2:].strip()
        elif line.startswith('v '):
            for x in map(int,line[2:].split()):
                if x: vals[abs(x)]=x>0
    return status,vals


def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True)
    p.add_argument('--index',type=int,required=True);p.add_argument('--graph')
    p.add_argument('--timeout',type=int,default=300)
    x=p.parse_args();data=canonical_rows(False)
    if not 0<=x.index<len(data):p.error('index outside the 43-row h=4 pilot')
    row=data[x.index];c,a,_=build(row)
    with tempfile.TemporaryDirectory(prefix='m7bad-') as d:
        cnf=Path(d)/'row.cnf';model=Path(d)/'model.out';write_cnf(c,cnf)
        cmd=[x.solver,'--no-colors','-t',str(x.timeout),'-w',str(model),str(cnf)]
        run=subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
        if run.returncode==20:
            print(f'UNSAT-SCOUT index={x.index} row={row!r}')
            return
        if run.returncode!=10:
            raise SystemExit(f'solver failed rc={run.returncode}: {run.stderr.strip()}')
        status,vals=read_model(model)
        assert status=='SATISFIABLE' and len(vals)>=len(c.names)
        assert all(any(vals[abs(z)]==(z>0) for z in clause) for clause in c.clauses)
        if not x.graph:p.error('--graph is required for a SAT result')
        arcs={(u,v) for u in range(N) for v in range(N) if vals[a[u][v]]}
        Path(x.graph).write_text(str(N)+'\n'+''.join(f'{u} {v}\n' for u,v in sorted(arcs)),encoding='ascii')
        print(f'SAT index={x.index} graph={x.graph} row={row!r}')

if __name__=='__main__':main()
