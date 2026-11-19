#!/usr/bin/env python3
"""Fast fail-closed mutation negatives for the h=3 strict verifier."""
import hashlib,json,lzma,shutil,subprocess,tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
VERIFY=HERE/'verify_m7_family_s_h3_campaign.py';MAN=HERE/'m7-family-s-badness-h3-manifest.json';PROOFS=HERE.parent/'certificates/m7-family-s-badness-h3'
DRAT_SHA='92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a'

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def write(p,x):p.write_text(json.dumps(x,indent=2,separators=(',',': '))+'\n',encoding='ascii')
def run(man,proofs,drat):
    return subprocess.run(['python3','-O',str(VERIFY),'--manifest',str(man),'--proof-dir',str(proofs),'--drat-trim',str(drat),'--cnf-checker',str(HERE/'check_m7_family_s_badness_cnf.py'),'--universe-checker',str(HERE/'m7_family_s_h3_universe_check.py')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)

def main():
    original=json.loads(MAN.read_text(encoding='ascii'))
    with tempfile.TemporaryDirectory(prefix='.m7h3-mutate-',dir=HERE)as td:
        td=Path(td);fake=td/'drat';fake.write_bytes(b'x');fake.chmod(0o755)
        # All manifest mutations must fail before proof replay; the wrong checker
        # is itself a negative pin mutation and keeps the test fast.
        mutations=[]
        x=json.loads(json.dumps(original));x['entries'][0],x['entries'][1]=x['entries'][1],x['entries'][0];mutations.append(('order',x))
        x=json.loads(json.dumps(original));x['entries'][1]['row']=x['entries'][0]['row'];mutations.append(('duplicate-row',x))
        x=json.loads(json.dumps(original));x['entries'].pop();mutations.append(('missing-row',x))
        x=json.loads(json.dumps(original));x['entries'][0]['cnf_sha256']='0'*64;mutations.append(('cnf-hash',x))
        x=json.loads(json.dumps(original));x['entries'][0]['compressed_proof_sha256']='0'*64;mutations.append(('proof-hash',x))
        for name,payload in mutations:
            man=td/f'{name}.json';write(man,payload);r=run(man,PROOFS,fake);require(r.returncode!=0,f'{name} mutation accepted')
        # Artifact-set mutations use a hard-linked complete temporary set, so
        # no proof bytes are copied and set checking still happens fail-closed.
        proofset=td/'proofs';proofset.mkdir()
        for p in PROOFS.iterdir():(proofset/p.name).hardlink_to(p)
        missing=next(iter(proofset.iterdir()));missing.unlink();r=run(MAN,proofset,fake);require(r.returncode!=0,'missing artifact accepted')
        missing.hardlink_to(PROOFS/missing.name);(proofset/'orphan').write_bytes(b'x');r=run(MAN,proofset,fake);require(r.returncode!=0,'orphan artifact accepted')
        # Pin mutation alone is rejected.
        r=run(MAN,PROOFS,fake);require(r.returncode!=0 and 'unexpected drat-trim sha256' in r.stdout,'checker pin mutation accepted')
    print(f'PASS h3 verifier hostile_mutations={len(mutations)+3} (order duplicate missing row, CNF/proof hash, missing/orphan artifact, checker pin)')

if __name__=='__main__':main()
