#!/usr/bin/env python3
"""Regenerate, authenticate, and replay the family-S h=4 DRAT package."""
import argparse,hashlib,json,lzma,subprocess,tempfile
from pathlib import Path
from m7_family_s_badness_pilot import canonical_rows,build,write_cnf

EXPECTED_DRAT_TRIM_SHA256='92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a'

def digest(x):return hashlib.sha256(x).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--proof-dir',type=Path,required=True);p.add_argument('--drat-trim',required=True)
    p.add_argument('--cnf-checker',required=True);x=p.parse_args()
    checker=Path(x.drat_trim).read_bytes()
    assert digest(checker)==EXPECTED_DRAT_TRIM_SHA256,('unexpected drat-trim binary',digest(checker))
    payload=json.loads(x.manifest.read_text(encoding='ascii'));data=canonical_rows(False)
    expected_files={f'm7-family-s-badness-h4-{i:02d}.drat.xz' for i in range(43)}
    actual_files={p.name for p in x.proof_dir.iterdir() if p.is_file()}
    assert actual_files==expected_files,(actual_files-expected_files,expected_files-actual_files)
    assert payload['schema']=='m7-family-s-badness-h4-v1' and payload['rows']==43
    assert len(payload['entries'])==43 and [z['index']for z in payload['entries']]==list(range(43))
    with tempfile.TemporaryDirectory(prefix='m7bad-verify-')as d:
        d=Path(d)
        for e,row in zip(payload['entries'],data):
            assert tupleize(e['row'])==row
            c,_,_=build(row);cnf=d/'row.cnf';proof=d/'row.drat';write_cnf(c,cnf)
            raw=cnf.read_bytes()
            assert len(raw)==e['cnf_bytes'] and digest(raw)==e['cnf_sha256']
            check=subprocess.run([x.cnf_checker,str(cnf),'--row',json.dumps(row,separators=(',',':'))],
                                 stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            assert check.returncode==0 and 'PASS independent badness CNF' in check.stdout
            packed=(x.proof_dir/e['proof_file']).read_bytes()
            assert len(packed)==e['compressed_proof_bytes'] and digest(packed)==e['compressed_proof_sha256']
            proof_raw=lzma.decompress(packed);assert len(proof_raw)==e['proof_bytes'] and digest(proof_raw)==e['proof_sha256']
            proof.write_bytes(proof_raw)
            replay=subprocess.run([x.drat_trim,str(cnf),str(proof)],stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,text=True)
            assert replay.returncode==0 and 's VERIFIED' in replay.stdout,(e['index'],replay.stdout[-1000:])
    print('PASS regenerated/authenticated/replayed family-S h4 proofs=43')

def tupleize(x):
    if isinstance(x,list):return tuple(tupleize(z)for z in x)
    return x

if __name__=='__main__':main()
