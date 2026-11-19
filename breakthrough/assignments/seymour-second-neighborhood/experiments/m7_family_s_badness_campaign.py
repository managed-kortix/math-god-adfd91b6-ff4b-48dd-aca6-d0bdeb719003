#!/usr/bin/env python3
"""Run and independently check the 43-row h=4 exact-badness campaign.

CaDiCaL emits one DRAT proof per UNSAT row.  drat-trim checks each proof.  A
SAT assignment is checked against the producer CNF, exported as an arc list,
and audited by the producer-independent semantic checker.  Proofs and transient
witnesses live in a temporary directory unless an authenticated package is
explicitly requested.
"""
import argparse,hashlib,json,lzma,subprocess,tempfile
from pathlib import Path
from m7_family_s_badness_pilot import canonical_rows,build,write_cnf
from m7_family_s_badness_check import observed_row,n1,n2

N=18; W=0; A=set(range(1,9)); B=set(range(9,16)); HIGHS={1,2}
DRAT_TRIM_SHA256='92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a'
DRAT_TRIM={
    'name':'drat-trim',
    'source_url':'https://github.com/marijnheule/drat-trim.git',
    'source_commit':'2e3b2dc0ecf938addbd779d42877b6ed69d9a985',
    'source_tree':'b4e75a5f8c89d664652727458369cb5e0b610e31',
    'source_blob':'cf8a676ffcc7ef5a47124bbafc9b680a2df333e0',
    'source_sha256':'d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee',
    'build_command':'gcc drat-trim.c -std=c99 -O2 -o drat-trim',
    'compiler':'gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0',
    'elf_build_id':'83768248f9562e7a5b87b8530e078148fe0b62a6',
    'binary_sha256':DRAT_TRIM_SHA256,
}
SOURCES={
    'm7_family_s_badness_pilot.py':'f68c0edd09e43971572fb325e2ba963bc8f79e3cc6751a274ff777be652a4257',
    'check_m7_family_s_badness_cnf.py':'5dfa458b87f70be9cc2bd66f33c18b7c7060534804fed795e331809558b3615a',
}


def fail(message):
    raise RuntimeError(message)


def require(condition,message):
    if not condition:
        fail(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def universe_digest(rows):
    return digest(''.join(json.dumps(row,separators=(',',':'))+'\n' for row in rows).encode('ascii'))


def read_model(path):
    status=None;vals={}
    try:
        lines=Path(path).read_text(encoding='ascii').splitlines()
    except (OSError,UnicodeError) as ex:
        fail(f'model read failed: {ex}')
    for line in lines:
        if line.startswith('s '):
            status=line[2:].strip()
        elif line.startswith('v '):
            try:
                literals=map(int,line[2:].split())
            except ValueError as ex:
                fail(f'malformed model literal: {ex}')
            for literal in literals:
                if literal:
                    vals[abs(literal)]=literal>0
    return status,vals


def semantic_check(arcs,row):
    require(all(not ((u,v) in arcs and (v,u) in arcs)
                for u in range(N) for v in range(u+1,N)),'semantic check: digon')
    one=[n1(arcs,u) for u in range(N)];two=[n2(arcs,u) for u in range(N)]
    require([len(z) for z in one]==[9 if u in HIGHS else 8 for u in range(N)],
            'semantic check: outdegree sequence')
    require(all(len(two[u])<len(one[u]) for u in range(N)),'semantic check: global badness')
    got,holes=observed_row(arcs)
    require(len(holes)==7 and got==row,'semantic check: hole count/type row')
    require(one[W]==A and two[W]==B,'semantic check: root layers')
    for high in sorted(HIGHS):
        reduced={(u,v) for u,v in arcs if u!=high and v!=high}
        require(n2(reduced,W)==B,f'semantic check: robustness after deleting {high}')


def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True)
    p.add_argument('--drat-trim',required=True);p.add_argument('--cnf-checker')
    p.add_argument('--proof-dir',type=Path);p.add_argument('--manifest',type=Path)
    p.add_argument('--timeout',type=int,default=300)
    x=p.parse_args();data=canonical_rows(False,4);sat=[];unsat=[];ledger=[]
    require(len(data)==43 and len(set(data))==43,'campaign universe size/uniqueness')
    if (x.proof_dir is None)!=(x.manifest is None):
        p.error('--proof-dir and --manifest must be used together')
    try:
        drat_raw=Path(x.drat_trim).read_bytes()
    except OSError as ex:
        fail(f'drat-trim read failed: {ex}')
    require(digest(drat_raw)==DRAT_TRIM_SHA256,
            f'unexpected drat-trim binary sha256 {digest(drat_raw)}')
    if x.proof_dir:
        x.proof_dir.mkdir(parents=True,exist_ok=True)
        require(not any(x.proof_dir.iterdir()),'proof directory must be empty')
    with tempfile.TemporaryDirectory(prefix='m7bad-campaign-') as td:
        td=Path(td)
        for i,row in enumerate(data):
            c,a,_=build(row);cnf=td/f'{i}.cnf';model=td/f'{i}.model';proof=td/f'{i}.drat'
            write_cnf(c,cnf)
            if x.cnf_checker:
                check=subprocess.run([x.cnf_checker,str(cnf),'--row',json.dumps(row,separators=(',',':'))],
                                     stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                require(check.returncode==0 and 'PASS independent badness CNF' in check.stdout,
                        f'row {i}: independent CNF check: {check.stdout[-1000:]}')
            run=subprocess.run([x.solver,'--no-colors','-t',str(x.timeout),'-w',str(model),str(cnf),str(proof)],
                               stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
            if run.returncode==20:
                check=subprocess.run([x.drat_trim,str(cnf),str(proof)],stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,text=True)
                require(check.returncode==0 and 'c detected empty clause' in check.stdout and 's VERIFIED' in check.stdout,
                        f'row {i}: DRAT check: {check.stdout[-1000:]}')
                cnf_raw=cnf.read_bytes();proof_raw=proof.read_bytes()
                ledger.append({'index':i,'row':row,'cnf_bytes':len(cnf_raw),
                    'cnf_sha256':digest(cnf_raw),'proof_bytes':len(proof_raw),'proof_sha256':digest(proof_raw)})
                if x.proof_dir:
                    packed=lzma.compress(proof_raw,format=lzma.FORMAT_XZ,preset=9)
                    target=x.proof_dir/f'm7-family-s-badness-h4-{i:02d}.drat.xz';target.write_bytes(packed)
                    ledger[-1].update(compressed_proof_bytes=len(packed),
                        compressed_proof_sha256=digest(packed),proof_file=target.name)
                unsat.append(i);continue
            if run.returncode!=10:
                fail(f'row {i}: solver failed rc={run.returncode}: {run.stderr.strip()}')
            status,vals=read_model(model)
            require(status=='SATISFIABLE','SAT model status')
            require(set(vals)==set(range(1,len(c.names)+1)),'SAT model variable domain/completeness')
            require(all(any(vals[abs(z)]==(z>0) for z in clause) for clause in c.clauses),
                    'SAT model fails producer CNF')
            arcs={(u,v) for u in range(N) for v in range(N) if vals[a[u][v]]}
            semantic_check(arcs,row);sat.append(i)
    if x.manifest:
        payload={'schema':'m7-family-s-badness-h4-v2','h':4,'universe_rows':len(data),
            'ordered_universe_sha256':universe_digest(data),
            'toolchain':{'proof_checker':DRAT_TRIM,'compression':{'format':'xz','python_lzma_preset':9}},
            'sources':SOURCES,'entries':ledger}
        x.manifest.write_text(json.dumps(payload,indent=2,separators=(',',': '))+'\n',encoding='ascii')
    print(f'PASS exact-badness h4 rows={len(data)} checked_UNSAT={len(unsat)} semantic_SAT={len(sat)}')
    print('PASS UNSAT_indices='+json.dumps(unsat,separators=(',',':')))
    print('PASS SAT_indices='+json.dumps(sat,separators=(',',':')))


if __name__=='__main__':
    main()
