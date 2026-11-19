#!/usr/bin/env python3
"""Run and independently check the 43-row h=4 exact-badness campaign.

CaDiCaL emits one DRAT proof per UNSAT row.  drat-trim checks each proof.  A
SAT assignment is checked against the producer CNF, exported as an arc list,
and audited by the producer-independent semantic checker.  Proofs and transient
witnesses live in a temporary directory and are not repository artifacts.
"""
import argparse,hashlib,json,lzma,subprocess,tempfile
from pathlib import Path
from m7_family_s_badness_pilot import canonical_rows,build,write_cnf
from m7_family_s_badness_check import observed_row,n1,n2

N=18; W=0; A=set(range(1,9)); B=set(range(9,16)); HIGHS={1,2}


def read_model(path):
    status=None;vals={}
    for line in Path(path).read_text(encoding='ascii').splitlines():
        if line.startswith('s '):status=line[2:].strip()
        elif line.startswith('v '):
            for x in map(int,line[2:].split()):
                if x:vals[abs(x)]=x>0
    return status,vals


def semantic_check(arcs,row):
    assert all(not ((u,v) in arcs and (v,u) in arcs)
               for u in range(N) for v in range(u+1,N))
    one=[n1(arcs,u) for u in range(N)];two=[n2(arcs,u) for u in range(N)]
    assert [len(z) for z in one]==[9 if u in HIGHS else 8 for u in range(N)]
    assert all(len(two[u])<len(one[u]) for u in range(N))
    got,holes=observed_row(arcs)
    assert len(holes)==7 and got==row
    assert one[W]==A and two[W]==B
    for high in sorted(HIGHS):
        reduced={(u,v) for u,v in arcs if u!=high and v!=high}
        assert n2(reduced,W)==B


def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True)
    p.add_argument('--drat-trim',required=True);p.add_argument('--cnf-checker')
    p.add_argument('--proof-dir',type=Path);p.add_argument('--manifest',type=Path)
    p.add_argument('--timeout',type=int,default=300)
    x=p.parse_args();data=canonical_rows(False);sat=[];unsat=[];ledger=[]
    if (x.proof_dir is None)!=(x.manifest is None):p.error('--proof-dir and --manifest must be used together')
    if x.proof_dir:x.proof_dir.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='m7bad-campaign-') as d:
        d=Path(d)
        for i,row in enumerate(data):
            c,a,_=build(row);cnf=d/f'{i}.cnf';model=d/f'{i}.model';proof=d/f'{i}.drat'
            write_cnf(c,cnf)
            if x.cnf_checker:
                check=subprocess.run([x.cnf_checker,str(cnf),'--row',json.dumps(row,separators=(',',':'))],
                                     stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                assert check.returncode==0 and 'PASS independent badness CNF' in check.stdout,(i,check.stdout)
            run=subprocess.run([x.solver,'--no-colors','-t',str(x.timeout),'-w',str(model),str(cnf),str(proof)],
                               stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
            if run.returncode==20:
                check=subprocess.run([x.drat_trim,str(cnf),str(proof)],stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,text=True)
                assert check.returncode==0 and 's VERIFIED' in check.stdout,(i,check.stdout[-1000:])
                cnf_raw=cnf.read_bytes();proof_raw=proof.read_bytes()
                ledger.append({'index':i,'row':row,'cnf_bytes':len(cnf_raw),
                    'cnf_sha256':hashlib.sha256(cnf_raw).hexdigest(),
                    'proof_bytes':len(proof_raw),'proof_sha256':hashlib.sha256(proof_raw).hexdigest()})
                if x.proof_dir:
                    packed=lzma.compress(proof_raw,format=lzma.FORMAT_XZ,preset=9)
                    target=x.proof_dir/f'm7-family-s-badness-h4-{i:02d}.drat.xz';target.write_bytes(packed)
                    ledger[-1].update(compressed_proof_bytes=len(packed),
                        compressed_proof_sha256=hashlib.sha256(packed).hexdigest(),proof_file=target.name)
                unsat.append(i);continue
            if run.returncode!=10:
                raise SystemExit(f'row {i}: solver failed rc={run.returncode}: {run.stderr.strip()}')
            status,vals=read_model(model)
            assert status=='SATISFIABLE' and len(vals)>=len(c.names)
            assert all(any(vals[abs(z)]==(z>0) for z in clause) for clause in c.clauses)
            arcs={(u,v) for u in range(N) for v in range(N) if vals[a[u][v]]}
            semantic_check(arcs,row);sat.append(i)
    if x.manifest:
        payload={'schema':'m7-family-s-badness-h4-v1','rows':len(data),'entries':ledger}
        x.manifest.write_text(json.dumps(payload,indent=2,separators=(',',': '))+'\n',encoding='ascii')
    print(f'PASS exact-badness h4 rows={len(data)} checked_UNSAT={len(unsat)} semantic_SAT={len(sat)}')
    print('PASS UNSAT_indices='+json.dumps(unsat,separators=(',',':')))
    print('PASS SAT_indices='+json.dumps(sat,separators=(',',':')))

if __name__=='__main__':main()
