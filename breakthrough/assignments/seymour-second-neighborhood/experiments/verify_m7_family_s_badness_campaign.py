#!/usr/bin/env python3
"""Fail-closed regeneration, identity authentication, and DRAT replay for h=4."""
import argparse,hashlib,json,lzma,subprocess,tempfile
from pathlib import Path
from m7_family_s_badness_pilot import canonical_rows,build,write_cnf

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
    'binary_sha256':'92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a',
}
EXPECTED_SOURCES={
    'm7_family_s_badness_pilot.py':'f68c0edd09e43971572fb325e2ba963bc8f79e3cc6751a274ff777be652a4257',
    'check_m7_family_s_badness_cnf.py':'5dfa458b87f70be9cc2bd66f33c18b7c7060534804fed795e331809558b3615a',
}
TOP_FIELDS={'schema','h','universe_rows','ordered_universe_sha256','toolchain','sources','entries'}
ENTRY_FIELDS={'index','row','cnf_bytes','cnf_sha256','proof_bytes','proof_sha256',
              'compressed_proof_bytes','compressed_proof_sha256','proof_file'}


def fail(message):
    raise RuntimeError(message)


def require(condition,message):
    if not condition:
        fail(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def tupleize(value):
    if isinstance(value,list):
        return tuple(tupleize(item) for item in value)
    return value


def checked_object(value,fields,label):
    require(type(value) is dict,f'{label}: expected object')
    require(set(value)==fields,f'{label}: fields missing={fields-set(value)} unknown={set(value)-fields}')
    return value


def checked_nonnegative_int(value,label):
    require(type(value) is int and value>=0,f'{label}: expected nonnegative integer')
    return value


def checked_sha256(value,label):
    require(type(value) is str and len(value)==64 and all(c in '0123456789abcdef' for c in value),
            f'{label}: expected lowercase SHA-256')
    return value


def ordered_universe_digest(rows):
    raw=''.join(json.dumps(row,separators=(',',':'))+'\n' for row in rows).encode('ascii')
    return digest(raw)


def load_manifest(path,production):
    try:
        payload=json.loads(path.read_text(encoding='ascii'))
    except (OSError,UnicodeError,json.JSONDecodeError) as ex:
        fail(f'manifest read/parse failed: {ex}')
    checked_object(payload,TOP_FIELDS,'manifest')
    require(payload['schema']=='m7-family-s-badness-h4-v2','manifest schema')
    require(type(payload['h']) is int and payload['h']==4,'manifest h')
    require(type(payload['universe_rows']) is int and payload['universe_rows']==43,'manifest universe_rows')
    require(payload['ordered_universe_sha256']==ordered_universe_digest(production),'manifest ordered universe identity')
    require(payload['toolchain']=={'proof_checker':DRAT_TRIM,'compression':{'format':'xz','python_lzma_preset':9}},
            'manifest toolchain identities')
    require(payload['sources']==EXPECTED_SOURCES,'manifest source identities')
    entries=payload['entries']
    require(type(entries) is list and len(entries)==43,'manifest entry count')
    seen_rows=set();seen_files=set()
    for position,(entry,row) in enumerate(zip(entries,production)):
        checked_object(entry,ENTRY_FIELDS,f'entry {position}')
        require(type(entry['index']) is int and entry['index']==position,f'entry {position}: index/order')
        require(tupleize(entry['row'])==row,f'entry {position}: row/order')
        frozen=tupleize(entry['row'])
        require(frozen not in seen_rows,f'entry {position}: duplicate row')
        seen_rows.add(frozen)
        expected_name=f'm7-family-s-badness-h4-{position:02d}.drat.xz'
        require(type(entry['proof_file']) is str and entry['proof_file']==expected_name,
                f'entry {position}: proof filename')
        require(entry['proof_file'] not in seen_files,f'entry {position}: duplicate proof filename')
        seen_files.add(entry['proof_file'])
        for field in ('cnf_bytes','proof_bytes','compressed_proof_bytes'):
            checked_nonnegative_int(entry[field],f'entry {position}: {field}')
        for field in ('cnf_sha256','proof_sha256','compressed_proof_sha256'):
            checked_sha256(entry[field],f'entry {position}: {field}')
    require(seen_rows==set(production),'manifest row set')
    return entries


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--proof-dir',type=Path,required=True)
    p.add_argument('--drat-trim',required=True)
    p.add_argument('--cnf-checker',required=True)
    x=p.parse_args()

    try:
        checker=Path(x.drat_trim).read_bytes()
    except OSError as ex:
        fail(f'drat-trim read failed: {ex}')
    require(digest(checker)==DRAT_TRIM['binary_sha256'],
            f'unexpected drat-trim binary sha256 {digest(checker)}')
    here=Path(__file__).resolve().parent
    for name,expected in EXPECTED_SOURCES.items():
        got=digest((here/name).read_bytes())
        require(got==expected,f'unexpected source sha256 {name}: {got}')

    production=canonical_rows(False,4)
    require(len(production)==43 and len(set(production))==43,'production universe size/uniqueness')
    entries=load_manifest(x.manifest,production)
    expected_files={entry['proof_file'] for entry in entries}
    try:
        actual_files={path.name for path in x.proof_dir.iterdir() if path.is_file()}
        nonfiles={path.name for path in x.proof_dir.iterdir() if not path.is_file()}
    except OSError as ex:
        fail(f'proof directory read failed: {ex}')
    require(not nonfiles,f'proof directory contains non-files: {nonfiles}')
    require(actual_files==expected_files,
            f'artifact set missing={expected_files-actual_files} orphan={actual_files-expected_files}')

    with tempfile.TemporaryDirectory(prefix='m7bad-verify-') as td:
        td=Path(td)
        for entry,row in zip(entries,production):
            i=entry['index']
            c,_,_=build(row);cnf=td/'row.cnf';proof=td/'row.drat';write_cnf(c,cnf)
            raw=cnf.read_bytes()
            require((len(raw),digest(raw))==(entry['cnf_bytes'],entry['cnf_sha256']),
                    f'row {i}: CNF identity')
            check=subprocess.run([x.cnf_checker,str(cnf),'--row',json.dumps(row,separators=(',',':'))],
                                 stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            require(check.returncode==0 and 'PASS independent badness CNF' in check.stdout,
                    f'row {i}: independent CNF check: {check.stdout[-1000:]}')
            packed=(x.proof_dir/entry['proof_file']).read_bytes()
            require((len(packed),digest(packed))==(entry['compressed_proof_bytes'],entry['compressed_proof_sha256']),
                    f'row {i}: packed proof identity')
            try:
                proof_raw=lzma.decompress(packed)
            except lzma.LZMAError as ex:
                fail(f'row {i}: xz decode: {ex}')
            require((len(proof_raw),digest(proof_raw))==(entry['proof_bytes'],entry['proof_sha256']),
                    f'row {i}: raw proof identity')
            proof.write_bytes(proof_raw)
            replay=subprocess.run([x.drat_trim,str(cnf),str(proof)],stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,text=True)
            require(replay.returncode==0 and 'c detected empty clause' in replay.stdout and 's VERIFIED' in replay.stdout,
                    f'row {i}: DRAT replay: {replay.stdout[-1000:]}')
    print('PASS fail-closed regenerated/authenticated/replayed family-S h4 proofs=43')


if __name__=='__main__':
    main()
