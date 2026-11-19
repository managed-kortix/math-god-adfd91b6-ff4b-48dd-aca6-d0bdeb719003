#!/usr/bin/env python3
"""Hostile python -O negatives for the h=4 strict verifier contract."""
import json,os,subprocess,tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
VERIFY=HERE/'verify_m7_family_s_badness_campaign.py'
MANIFEST=HERE/'m7-family-s-badness-h4-manifest.json'
PROOFS=HERE.parent/'certificates/m7-family-s-badness-h4'
CNF_CHECKER=HERE/'check_m7_family_s_badness_cnf.py'
PINNED_DRAT=Path(os.environ.get('M7_H4_DRAT_TRIM','/workspace/drat-trim-audit/drat-trim'))


def require(condition,message):
    if not condition:
        raise RuntimeError(message)


def write_json(path,payload):
    path.write_text(json.dumps(payload,indent=2,separators=(',',': '))+'\n',encoding='ascii')


def run(manifest,proofs,drat=PINNED_DRAT,checker=CNF_CHECKER):
    return subprocess.run(['python3','-O',str(VERIFY),'--manifest',str(manifest),
        '--proof-dir',str(proofs),'--drat-trim',str(drat),'--cnf-checker',str(checker)],
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)


def expect_failure(label,result):
    require(result.returncode!=0,f'{label}: mutation accepted\n{result.stdout}')


def clone(value):
    return json.loads(json.dumps(value))


def main():
    require(PINNED_DRAT.is_file(),f'pinned drat-trim not found: {PINNED_DRAT}')
    original=json.loads(MANIFEST.read_text(encoding='ascii'))
    # Baseline first: this makes the test itself reject a package that cannot
    # complete a full optimized replay before any hostile mutation is applied.
    baseline=run(MANIFEST,PROOFS)
    require(baseline.returncode==0 and
            'PASS fail-closed regenerated/authenticated/replayed family-S h4 proofs=43' in baseline.stdout,
            f'optimized baseline replay failed:\n{baseline.stdout}')
    with tempfile.TemporaryDirectory(prefix='.m7h4-mutate-',dir=HERE) as td:
        td=Path(td)
        false=Path('/bin/false')
        expect_failure('/bin/false drat-trim',run(MANIFEST,PROOFS,false,CNF_CHECKER))
        expect_failure('/bin/false CNF checker',run(MANIFEST,PROOFS,PINNED_DRAT,false))

        # Complete hard-linked proof set; tests never copy or alter repository artifacts.
        proofset=td/'proofs';proofset.mkdir()
        for proof in PROOFS.iterdir():
            (proofset/proof.name).hardlink_to(proof)

        mutations=[]
        payload=clone(original);payload['unknown']=0;mutations.append(('top-unknown-field',payload))
        payload=clone(original);payload['entries'][0]['unknown']=0;mutations.append(('entry-unknown-field',payload))
        payload=clone(original);payload['entries'][0],payload['entries'][1]=payload['entries'][1],payload['entries'][0];mutations.append(('entry-order',payload))
        payload=clone(original);payload['entries'][1]['row']=payload['entries'][0]['row'];mutations.append(('duplicate-row',payload))
        payload=clone(original);payload['entries'].pop();mutations.append(('missing-row',payload))
        payload=clone(original);payload['entries'].append(clone(payload['entries'][0]));mutations.append(('extra-row',payload))
        payload=clone(original);payload['entries'][0]['row'][4]=3;mutations.append(('row-change',payload))
        payload=clone(original);payload['entries'][0]['cnf_sha256']='0'*64;mutations.append(('cnf-hash',payload))
        payload=clone(original);payload['entries'][0]['compressed_proof_sha256']='0'*64;mutations.append(('proof-hash',payload))
        for label,payload in mutations:
            manifest=td/f'{label}.json';write_json(manifest,payload)
            expect_failure(label,run(manifest,proofset))

        missing=proofset/original['entries'][0]['proof_file'];missing.unlink()
        expect_failure('missing artifact',run(MANIFEST,proofset))
        missing.hardlink_to(PROOFS/missing.name)
        orphan=proofset/'orphan';orphan.write_bytes(b'x')
        expect_failure('extra artifact',run(MANIFEST,proofset));orphan.unlink()

        artifact=proofset/original['entries'][0]['proof_file']
        artifact.unlink();mutated=bytearray((PROOFS/artifact.name).read_bytes());mutated[-1]^=1;artifact.write_bytes(mutated)
        expect_failure('artifact mutation',run(MANIFEST,proofset))

    print(f'PASS h4 verifier python-O hostile_mutations={2+len(mutations)+3}')


if __name__=='__main__':
    main()
