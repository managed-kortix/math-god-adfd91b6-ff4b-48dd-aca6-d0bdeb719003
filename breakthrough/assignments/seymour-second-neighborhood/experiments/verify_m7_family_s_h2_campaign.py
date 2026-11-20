#!/usr/bin/env python3
"""Fail-closed independent-universe, identity, budget, and DRAT replay for h=2."""
import argparse,hashlib,json,lzma,re,subprocess,sys,tempfile
from pathlib import Path,PurePath
from m7_family_s_badness_pilot import canonical_rows,build,write_cnf

CAP=250_000_000
EXPECTED_DRAT='92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a'
EXPECTED_SOURCES={
 'm7_family_s_badness_pilot.py':'f68c0edd09e43971572fb325e2ba963bc8f79e3cc6751a274ff777be652a4257',
 'check_m7_family_s_badness_cnf.py':'5dfa458b87f70be9cc2bd66f33c18b7c7060534804fed795e331809558b3615a',
 'm7_family_s_h2_universe_check.py':'dd1f8c6d0365d8a440caff569198b1f030655bc179fe200a0aab637ff46df72e',
 'test_m7_family_s_h2_semantics.py':'629cac3511d3dc2b16b923950a1b3cc43bd4067833cc21e32051ccb707b21f5e',
 'snc_cnf.py':'adab04953d3697ec004e28ad145dda5b0f04d07ee8dd20d95655f6e32877d68e',
 'm7_family_s_type_rows.py':'9375c99968a65ecb35b99372b609e87c9c9806fa26f745b47c5d87dd15f215fc'}
HEX64=re.compile(r'[0-9a-f]{64}\Z')

def fail(x):raise RuntimeError(x)
def require(x,msg):
    if not x:fail(msg)
def digest(x):return hashlib.sha256(x).hexdigest()
def freeze(x):return tuple(freeze(y)for y in x)if isinstance(x,list)else x
def type_exact_equal(x,y):
    if type(x)is not type(y):return False
    if type(x)is dict:return x.keys()==y.keys()and all(type_exact_equal(x[k],y[k])for k in x)
    if type(x)is list:return len(x)==len(y)and all(type_exact_equal(a,b)for a,b in zip(x,y))
    return x==y

def no_duplicates(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError(f'duplicate JSON key {k!r}')
        out[k]=v
    return out

def load_json(path):
    return json.loads(path.read_text(encoding='ascii'),object_pairs_hook=no_duplicates,
                      parse_constant=lambda x:(_ for _ in()).throw(ValueError(f'nonfinite JSON {x}')))

def exact_int(x,msg,minimum=0):require(type(x)is int and x>=minimum,msg)
def exact_hash(x,msg):require(type(x)is str and HEX64.fullmatch(x) is not None,msg)

def validate_row(row,i):
    require(type(row)is list and len(row)==5,f'row {i} JSON shape')
    state,dist,ac,bc,h=row
    require(type(state)is str and state in ('M','01','10'),f'row {i} state type')
    require(type(dist)is list and len(dist)==3 and all(type(z)is int and 0<=z<=3 for z in dist),f'row {i} distinguished types')
    require(type(ac)is list and len(ac)==4 and all(type(z)is int and z>=0 for z in ac)and sum(ac)==6,f'row {i} A counts')
    require(type(bc)is list and len(bc)==9 and all(type(z)is int and z>=0 for z in bc)and sum(bc)==7,f'row {i} B counts')
    require(type(h)is int and h==2,f'row {i} h type')

def safe_name(name,i):
    expected=f'm7-family-s-badness-h2-{i:03d}.drat.xz'
    require(type(name)is str and name==expected,'unsafe or wrong proof filename')
    require(PurePath(name).name==name and not PurePath(name).is_absolute()and'..'not in PurePath(name).parts,'unsafe proof path')

def pin_program(path,expected,name):
    require(path.is_file()and not path.is_symlink(),f'{name} invalid or symlink')
    require(digest(path.read_bytes())==expected,f'wrong {name} source identity')

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path,required=True);p.add_argument('--proof-dir',type=Path,required=True)
    p.add_argument('--drat-trim',type=Path,required=True);p.add_argument('--cnf-checker',type=Path,required=True);p.add_argument('--universe-checker',type=Path,required=True);x=p.parse_args()
    require(x.proof_dir.is_dir()and not x.proof_dir.is_symlink(),'proof directory invalid or symlink')
    pin_program(x.drat_trim,EXPECTED_DRAT,'drat-trim binary')
    here=Path(__file__).resolve().parent
    for name,expected in EXPECTED_SOURCES.items():pin_program(here/name,expected,f'source {name}')
    pin_program(x.cnf_checker,EXPECTED_SOURCES['check_m7_family_s_badness_cnf.py'],'CNF checker')
    pin_program(x.universe_checker,EXPECTED_SOURCES['m7_family_s_h2_universe_check.py'],'universe checker')
    rows=canonical_rows(False,2);require(len(rows)==999,'production h2 universe size')
    with tempfile.TemporaryDirectory(prefix='m7h2-verify-')as td:
        td=Path(td);ledger=td/'rows.json';ledger.write_text(json.dumps(rows,separators=(',',':'))+'\n',encoding='ascii')
        uc=subprocess.run([sys.executable,'-O','-B',str(x.universe_checker),'--ordered-ledger',str(ledger)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        require(uc.returncode==0 and'canonical_orbits=999'in uc.stdout and'labelled_C_swap_orbits=532665'in uc.stdout,f'universe check: {uc.stdout}')
        payload=load_json(x.manifest)
        require(type(payload)is dict and set(payload)=={'schema','h','universe_rows','range','artifact_cap_exclusive_bytes','toolchain','entries','ordered_residual'},'manifest keys')
        require(payload['schema']=='m7-family-s-badness-h2-v1'and type(payload['h'])is int and payload['h']==2 and type(payload['universe_rows'])is int and payload['universe_rows']==999,'manifest metadata')
        require(type(payload['range'])is list and len(payload['range'])==2 and all(type(z)is int for z in payload['range'])and payload['range']==[0,999],'manifest package range');start,stop=0,999
        require(type(payload['artifact_cap_exclusive_bytes'])is int and payload['artifact_cap_exclusive_bytes']==CAP,'manifest cap');require(type(payload['ordered_residual'])is list and payload['ordered_residual']==[],'nonempty package residual')
        expected_tools={'solver':{'name':'CaDiCaL','version':'1.7.3','source_commit':'38e073b389a877b0a0d3c91136d2443ab95fdeba','binary_sha256':'5bfb078ad14e690745df9667a69b4d148d58e1ef3e39f7f782a0a30e259d7f8a'},'proof_checker':{'name':'drat-trim','source_commit':'2e3b2dc0ecf938addbd779d42877b6ed69d9a985','binary_sha256':EXPECTED_DRAT},'compression':{'format':'xz','python_lzma_preset':9},'ordered_universe_sha256':'f75ccdf6075085bbfe1cb1b9f1058452a37c644f0870057fcc38a3ef05e16d0b','sources':EXPECTED_SOURCES,'runtime':{'python':'3.12.13','python_binary_sha256':'7d43f6e86a6c6dd12005ec77eb2055f1be3f1bb3adedf8afe0a87973fa7371ce','liblzma_sha256':'26b37d25f7ca2a2d348de8ecabacda12e921cd933b21fa069a179760db77219d'}}
        require(type_exact_equal(payload['toolchain'],expected_tools),'toolchain/runtime metadata')
        es=payload['entries'];require(type(es)is list and len(es)==stop-start,'entry count')
        fields={'index','row','cnf_bytes','cnf_sha256','proof_file','proof_bytes','proof_sha256','compressed_proof_bytes','compressed_proof_sha256'}
        for j,e in enumerate(es):
            require(type(e)is dict and set(e)==fields,f'row {j} manifest fields')
            exact_int(e['index'],f'row {j} index type');require(e['index']==j,f'row {j} index order')
            validate_row(e['row'],j)
            for key in ('cnf_bytes','proof_bytes','compressed_proof_bytes'):exact_int(e[key],f'row {j} {key} type')
            for key in ('cnf_sha256','proof_sha256','compressed_proof_sha256'):exact_hash(e[key],f'row {j} {key} syntax')
            safe_name(e['proof_file'],j)
        erows=[freeze(e['row'])for e in es];require(len(erows)==len(set(erows))and erows==rows[start:stop],'ordered row set')
        expected={f'm7-family-s-badness-h2-{i:03d}.drat.xz'for i in range(start,stop)}
        items=list(x.proof_dir.iterdir());require(all(q.is_file()and not q.is_symlink()for q in items),'nonregular or symlink artifact')
        actual={q.name for q in items};require(actual==expected,f'artifact set missing={expected-actual} orphan={actual-expected}')
        packed_total=sum(e['compressed_proof_bytes']for e in es);require(packed_total<CAP,f'artifact cap violated {packed_total} >= {CAP}')
        for e,row in zip(es,rows[start:stop]):
            i=e['index'];c,_,_=build(row);cnf=td/'row.cnf';proof=td/'row.drat';write_cnf(c,cnf);cr=cnf.read_bytes();require((len(cr),digest(cr))==(e['cnf_bytes'],e['cnf_sha256']),f'row {i} CNF identity')
            ck=subprocess.run([sys.executable,'-O','-B',str(x.cnf_checker),str(cnf),'--row',json.dumps(row,separators=(',',':'))],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            require(ck.returncode==0 and'PASS independent badness CNF'in ck.stdout,f'row {i} CNF check: {ck.stdout}')
            path=x.proof_dir/e['proof_file'];pk=path.read_bytes();require((len(pk),digest(pk))==(e['compressed_proof_bytes'],e['compressed_proof_sha256']),f'row {i} packed identity')
            try:pr=lzma.decompress(pk)
            except lzma.LZMAError as ex:fail(f'row {i} xz: {ex}')
            require((len(pr),digest(pr))==(e['proof_bytes'],e['proof_sha256']),f'row {i} raw identity');proof.write_bytes(pr)
            rr=subprocess.run([str(x.drat_trim),str(cnf),str(proof)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            require(rr.returncode==0 and'c detected empty clause'in rr.stdout and's VERIFIED'in rr.stdout,f'row {i} DRAT: {rr.stdout[-1000:]}')
    print(f'PASS fail-closed h2 package={start}:{stop} universe/CNF/artifacts/DRAT rows={len(es)} residual=0 packed_bytes={packed_total} cap_exclusive={CAP}')

if __name__=='__main__':main()
