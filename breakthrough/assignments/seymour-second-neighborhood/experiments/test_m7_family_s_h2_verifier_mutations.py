#!/usr/bin/env python3
"""Fast fail-closed hostile negatives for the integrated h=2 verifier."""
import argparse,json,os,subprocess,sys,tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
VERIFY=HERE/'verify_m7_family_s_h2_campaign.py'
MANIFEST=HERE/'m7-family-s-badness-h2-manifest.json'
PROOFS=HERE.parent/'certificates/m7-family-s-badness-h2'
CNF=HERE/'check_m7_family_s_badness_cnf.py'
UNIVERSE=HERE/'m7_family_s_h2_universe_check.py'

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def dump(path,payload):path.write_text(json.dumps(payload,indent=2,separators=(',',': '))+'\n',encoding='ascii')
def clone(x):return json.loads(json.dumps(x))
def run(manifest,proofs,drat,cnf=CNF,universe=UNIVERSE):
    return subprocess.run([sys.executable,'-O','-B',str(VERIFY),'--manifest',str(manifest),
        '--proof-dir',str(proofs),'--drat-trim',str(drat),'--cnf-checker',str(cnf),
        '--universe-checker',str(universe)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
def reject(label,result,needle):
    require(result.returncode!=0,f'{label} mutation accepted')
    require(needle in result.stdout,f'{label} failed at wrong gate; wanted {needle!r}:\n{result.stdout[-2000:]}')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--drat-trim',type=Path,required=True);a=ap.parse_args()
    original=json.loads(MANIFEST.read_text(encoding='ascii'))
    with tempfile.TemporaryDirectory(dir=HERE,prefix='.m7h2-mutate-')as raw:
        td=Path(raw);fake=td/'fake';fake.write_text('#!/bin/sh\necho marker\n',encoding='ascii');fake.chmod(0o755)
        tests=[]
        x=clone(original);x['entries'][0],x['entries'][1]=x['entries'][1],x['entries'][0];tests.append(('order',x,'row 0 index order'))
        x=clone(original);x['entries'][1]['row']=x['entries'][0]['row'];tests.append(('duplicate-row',x,'ordered row set'))
        x=clone(original);x['entries'].pop();tests.append(('missing-row',x,'entry count'))
        x=clone(original);x['entries'][0]['cnf_sha256']='0'*64;tests.append(('cnf-hash',x,'row 0 CNF identity'))
        x=clone(original);x['entries'][0]['compressed_proof_sha256']='0'*64;tests.append(('proof-hash',x,'row 0 packed identity'))
        x=clone(original);x['range']=[0,998];tests.append(('range',x,'manifest package range'))
        x=clone(original);delta=250_000_000-sum(e['compressed_proof_bytes']for e in x['entries']);x['entries'][0]['compressed_proof_bytes']+=delta;tests.append(('exclusive-cap-equality',x,'artifact cap violated 250000000 >= 250000000'))
        x=clone(original);x['h']=2.0;tests.append(('numeric-type-alias',x,'manifest metadata'))
        x=clone(original);x['toolchain']['compression']['python_lzma_preset']=9.0;tests.append(('nested-numeric-type-alias',x,'toolchain/runtime metadata'))
        for label,payload,needle in tests:
            man=td/f'{label}.json';dump(man,payload);reject(label,run(man,PROOFS,a.drat_trim),needle)
        duplicate=td/'duplicate-key.json';text=MANIFEST.read_text(encoding='ascii');duplicate.write_text(text.replace('"schema":','"schema":"shadow",\n  "schema":',1),encoding='ascii')
        reject('duplicate-key',run(duplicate,PROOFS,a.drat_trim),'duplicate JSON key')
        proofset=td/'proofs';proofset.mkdir()
        for p in PROOFS.iterdir():os.link(p,proofset/p.name)
        missing=proofset/'m7-family-s-badness-h2-000.drat.xz';missing.unlink()
        reject('missing-artifact',run(MANIFEST,proofset,a.drat_trim),'artifact set missing=')
        os.link(PROOFS/missing.name,missing);(proofset/'orphan').write_bytes(b'x')
        reject('orphan-artifact',run(MANIFEST,proofset,a.drat_trim),'orphan=')
        (proofset/'orphan').unlink();(proofset/'orphan-dir').mkdir()
        reject('orphan-directory',run(MANIFEST,proofset,a.drat_trim),'nonregular or symlink artifact')
        reject('checker-pin',run(MANIFEST,PROOFS,fake),'wrong drat-trim binary source identity')
        reject('CNF-helper-substitution',run(MANIFEST,PROOFS,a.drat_trim,cnf=fake),'wrong CNF checker source identity')
        reject('universe-helper-substitution',run(MANIFEST,PROOFS,a.drat_trim,universe=fake),'wrong universe checker source identity')
    print(f'PASS h2 hostile verifier mutations={len(tests)+7} exact failure gates')
if __name__=='__main__':main()
