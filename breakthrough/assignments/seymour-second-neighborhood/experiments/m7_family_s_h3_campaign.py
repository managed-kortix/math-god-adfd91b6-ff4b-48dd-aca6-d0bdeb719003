#!/usr/bin/env python3
"""Proof-producing, resumable campaign for all 218 family-S h=3 rows."""
import argparse,hashlib,json,lzma,subprocess,tempfile
from pathlib import Path
from m7_family_s_badness_pilot import canonical_rows,build,write_cnf

N=18;W=0;A=set(range(1,9));B=set(range(9,16));HIGHS={1,2}

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def digest(x):return hashlib.sha256(x).hexdigest()
def n1(arcs,u):return {v for v in range(N)if(u,v)in arcs}
def n2(arcs,u):
    one=n1(arcs,u);return {v for x in one for v in range(N)if(x,v)in arcs}-one-{u}
def read_model(path):
    status=None;vals={}
    for line in path.read_text(encoding='ascii').splitlines():
        if line.startswith('s '):status=line[2:].strip()
        elif line.startswith('v '):
            for z in map(int,line[2:].split()):
                if z:vals[abs(z)]=z>0
    return status,vals

def semantic_check(arcs):
    require(all(not((u,v)in arcs and(v,u)in arcs)for u in range(N)for v in range(u+1,N)),'digon')
    one=[n1(arcs,u)for u in range(N)];two=[n2(arcs,u)for u in range(N)]
    require([len(x)for x in one]==[9 if u in HIGHS else 8 for u in range(N)],'degree sequence')
    require(all(len(two[u])<len(one[u])for u in range(N)),'not globally bad')
    require(one[W]==A and two[W]==B,'root layers')
    for high in HIGHS:
        red={(u,v)for u,v in arcs if u!=high and v!=high}
        require(n2(red,W)==B,f'robustness deleting {high}')

def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True);p.add_argument('--drat-trim',required=True)
    p.add_argument('--cnf-checker',required=True);p.add_argument('--proof-dir',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True);p.add_argument('--timeout',type=int,default=300)
    p.add_argument('--start',type=int,default=0);p.add_argument('--stop',type=int,default=218);x=p.parse_args()
    rows=canonical_rows(False,3);require(len(rows)==218,'production h3 universe not 218')
    require(0<=x.start<=x.stop<=218,'invalid campaign range');x.proof_dir.mkdir(parents=True,exist_ok=True)
    ledger=[];residual=[]
    with tempfile.TemporaryDirectory(prefix='m7h3-campaign-')as td:
        td=Path(td)
        for i in range(x.start,x.stop):
            row=rows[i];c,a,_=build(row);cnf=td/'row.cnf';model=td/'model';proof=td/'proof.drat';write_cnf(c,cnf)
            row_text=json.dumps(row,separators=(',',':'))
            ck=subprocess.run([x.cnf_checker,str(cnf),'--row',row_text],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            require(ck.returncode==0 and 'PASS independent badness CNF' in ck.stdout,f'row {i} CNF check failed: {ck.stdout}')
            run=subprocess.run([x.solver,'--no-colors','-t',str(x.timeout),'-w',str(model),str(cnf),str(proof)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
            if run.returncode==20:
                rr=subprocess.run([x.drat_trim,str(cnf),str(proof)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                require(rr.returncode==0 and 'c detected empty clause' in rr.stdout and 's VERIFIED' in rr.stdout,f'row {i} proof failed: {rr.stdout[-1000:]}')
                cr=cnf.read_bytes();pr=proof.read_bytes();packed=lzma.compress(pr,format=lzma.FORMAT_XZ,preset=9)
                name=f'm7-family-s-badness-h3-{i:03d}.drat.xz';(x.proof_dir/name).write_bytes(packed)
                ledger.append({'index':i,'row':row,'cnf_bytes':len(cr),'cnf_sha256':digest(cr),'proof_file':name,
                    'proof_bytes':len(pr),'proof_sha256':digest(pr),'compressed_proof_bytes':len(packed),'compressed_proof_sha256':digest(packed)})
            elif run.returncode==10:
                status,vals=read_model(model);require(status=='SATISFIABLE'and len(vals)>=len(c.names),f'row {i} incomplete SAT model')
                require(all(any(vals[abs(z)]==(z>0)for z in clause)for clause in c.clauses),f'row {i} model violates CNF')
                arcs={(u,v)for u in range(N)for v in range(N)if vals[a[u][v]]};semantic_check(arcs)
                residual.append({'index':i,'row':row,'status':'SAT'})
            else:residual.append({'index':i,'row':row,'status':'UNKNOWN','returncode':run.returncode,'stderr':run.stderr.strip()})
            for path in (model,proof):
                if path.exists():path.unlink()
    payload={'schema':'m7-family-s-badness-h3-v1','h':3,'universe_rows':218,'range':[x.start,x.stop],
             'entries':ledger,'ordered_residual':residual}
    x.manifest.write_text(json.dumps(payload,indent=2,separators=(',',': '))+'\n',encoding='ascii')
    print(f'PASS h3 campaign range={x.start}:{x.stop} checked_UNSAT={len(ledger)} residual={len(residual)}')

if __name__=='__main__':main()
