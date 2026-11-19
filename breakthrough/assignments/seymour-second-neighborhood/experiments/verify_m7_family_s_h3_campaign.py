#!/usr/bin/env python3
"""Fail-closed independent-universe, identity, and DRAT replay for h=3."""
import argparse,hashlib,json,lzma,subprocess,tempfile
from pathlib import Path
from m7_family_s_badness_pilot import canonical_rows,build,write_cnf

EXPECTED_DRAT_TRIM_SHA256='92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a'
EXPECTED_SOURCE_SHA256={
 'm7_family_s_badness_pilot.py':'f68c0edd09e43971572fb325e2ba963bc8f79e3cc6751a274ff777be652a4257',
 'check_m7_family_s_badness_cnf.py':'5dfa458b87f70be9cc2bd66f33c18b7c7060534804fed795e331809558b3615a',
 'm7_family_s_h3_universe_check.py':'f2cc2ff859fd902c91db4ed809898bf778c61dcaf4a387be5e4612f375ebca18',
 'test_m7_family_s_h3_semantics.py':'94e535a38badacc4662127224e4711c99867f399b443101fe5594b21f8e03eef'}

def fail(msg):raise RuntimeError(msg)
def require(ok,msg):
    if not ok:fail(msg)
def digest(x):return hashlib.sha256(x).hexdigest()
def freeze(x):return tuple(freeze(y)for y in x)if isinstance(x,list)else x

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path,required=True);p.add_argument('--proof-dir',type=Path,required=True)
    p.add_argument('--drat-trim',required=True);p.add_argument('--cnf-checker',required=True);p.add_argument('--universe-checker',required=True);x=p.parse_args()
    drat=Path(x.drat_trim).read_bytes();require(digest(drat)==EXPECTED_DRAT_TRIM_SHA256,f'unexpected drat-trim sha256 {digest(drat)}')
    here=Path(__file__).resolve().parent
    for name,expected in EXPECTED_SOURCE_SHA256.items():
        got=digest((here/name).read_bytes());require(got==expected,f'unexpected source sha256 {name}: {got}')
    production=canonical_rows(False,3);require(len(production)==218,'production universe size')
    with tempfile.TemporaryDirectory(prefix='m7h3-verify-')as td:
        td=Path(td);ledger=td/'ordered-rows.json';ledger.write_text(json.dumps(production,separators=(',',':'))+'\n',encoding='ascii')
        uc=subprocess.run([x.universe_checker,'--ordered-ledger',str(ledger)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        require(uc.returncode==0 and 'canonical_orbits=218' in uc.stdout and 'labelled_C_swap_orbits=21735' in uc.stdout,f'universe check failed: {uc.stdout}')
        payload=json.loads(x.manifest.read_text(encoding='ascii'))
        require(set(payload)=={'schema','h','universe_rows','range','toolchain','entries','ordered_residual'},'manifest keys')
        require(payload['schema']=='m7-family-s-badness-h3-v1'and payload['h']==3 and payload['universe_rows']==218 and payload['range']==[0,218],'manifest metadata')
        tools=payload['toolchain'];expected_tools={'solver':{'name':'CaDiCaL','version':'1.7.3','source_commit':'38e073b389a877b0a0d3c91136d2443ab95fdeba','binary_sha256':'5bfb078ad14e690745df9667a69b4d148d58e1ef3e39f7f782a0a30e259d7f8a'},'proof_checker':{'name':'drat-trim','source_commit':'2e3b2dc0ecf938addbd779d42877b6ed69d9a985','binary_sha256':EXPECTED_DRAT_TRIM_SHA256},'compression':{'format':'xz','python_lzma_preset':9},'ordered_universe_sha256':'356bf301e8df633d503800ebfe79a5405011eca53dd9f69f76ba5a0b55cf3705','sources':EXPECTED_SOURCE_SHA256}
        require(tools==expected_tools,'manifest toolchain identities')
        entries=payload['entries'];require(payload['ordered_residual']==[],'nonempty residual')
        require(len(entries)==218 and [e.get('index')for e in entries]==list(range(218)),'entry index cover')
        rows=[freeze(e.get('row'))for e in entries];require(len(rows)==len(set(rows))and rows==production,'entry row ordered set')
        expected={f'm7-family-s-badness-h3-{i:03d}.drat.xz'for i in range(218)}
        actual={q.name for q in x.proof_dir.iterdir()if q.is_file()};require(actual==expected,f'artifact set missing={expected-actual} orphan={actual-expected}')
        for e,row in zip(entries,production):
            required={'index','row','cnf_bytes','cnf_sha256','proof_file','proof_bytes','proof_sha256','compressed_proof_bytes','compressed_proof_sha256'}
            require(set(e)==required,f'row {e.get("index")} manifest fields')
            i=e['index'];require(e['proof_file']==f'm7-family-s-badness-h3-{i:03d}.drat.xz',f'row {i} proof name')
            c,_,_=build(row);cnf=td/'row.cnf';proof=td/'row.drat';write_cnf(c,cnf);cr=cnf.read_bytes()
            require((len(cr),digest(cr))==(e['cnf_bytes'],e['cnf_sha256']),f'row {i} CNF identity')
            ck=subprocess.run([x.cnf_checker,str(cnf),'--row',json.dumps(row,separators=(',',':'))],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            require(ck.returncode==0 and 'PASS independent badness CNF' in ck.stdout,f'row {i} independent CNF check: {ck.stdout}')
            packed=(x.proof_dir/e['proof_file']).read_bytes();require((len(packed),digest(packed))==(e['compressed_proof_bytes'],e['compressed_proof_sha256']),f'row {i} packed proof identity')
            try:pr=lzma.decompress(packed)
            except lzma.LZMAError as ex:fail(f'row {i} xz decode: {ex}')
            require((len(pr),digest(pr))==(e['proof_bytes'],e['proof_sha256']),f'row {i} raw proof identity');proof.write_bytes(pr)
            rr=subprocess.run([x.drat_trim,str(cnf),str(proof)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            require(rr.returncode==0 and 'c detected empty clause' in rr.stdout and 's VERIFIED' in rr.stdout,f'row {i} DRAT replay: {rr.stdout[-1000:]}')
    print('PASS fail-closed h3 universe/CNF/artifact identity and DRAT replay rows=218 residual=0')

if __name__=='__main__':main()
