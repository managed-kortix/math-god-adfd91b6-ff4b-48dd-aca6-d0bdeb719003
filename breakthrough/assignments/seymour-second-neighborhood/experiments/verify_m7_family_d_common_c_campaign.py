#!/usr/bin/env python3
"""Fail-closed regeneration, authentication, and replay of nine common-C leaves."""
import argparse
import hashlib
import json
import lzma
import os
import subprocess
import tempfile
from pathlib import Path
from m7_family_d_common_c_cnf import CELLS,TYPES,build,write_cnf

SCHEMA="m7-family-d-common-c-v1"
EXPECTED_CADICAL_SOURCE_COMMIT="38e073b389a877b0a0d3c91136d2443ab95fdeba"
EXPECTED_DRAT_TRIM_SOURCE_COMMIT="2e3b2dc0ecf938addbd779d42877b6ed69d9a985"
EXPECTED_DRAT_TRIM_SHA256="92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a"


def require(condition,message):
    if not condition:raise RuntimeError(message)


def digest(raw):return hashlib.sha256(raw).hexdigest()


def read_json_exact(path):
    raw=path.read_bytes()
    try:text=raw.decode("ascii")
    except UnicodeDecodeError as exc:raise RuntimeError("manifest is not ASCII") from exc
    decoder=json.JSONDecoder()
    try:payload,end=decoder.raw_decode(text)
    except json.JSONDecodeError as exc:raise RuntimeError("invalid manifest JSON") from exc
    require(text[end:].strip()=="","trailing content after manifest JSON")
    return payload


def exact_keys(obj,expected,where):
    require(isinstance(obj,dict),f"{where}: expected object")
    got=set(obj);expected=set(expected)
    require(got==expected,f"{where}: keys differ extra={got-expected} missing={expected-got}")


def run(cmd,where):
    q=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    require(q.returncode==0,f"{where}: exit {q.returncode}: {q.stdout[-2000:]}")
    return q.stdout


def main():
    p=argparse.ArgumentParser();p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--proof-dir",type=Path,required=True);p.add_argument("--drat-trim",required=True)
    p.add_argument("--cnf-checker",required=True);x=p.parse_args()
    checker=Path(x.drat_trim)
    require(checker.is_file() and os.access(checker,os.X_OK),"drat-trim is not executable")
    require(digest(checker.read_bytes())==EXPECTED_DRAT_TRIM_SHA256,"unexpected drat-trim binary digest")
    payload=read_json_exact(x.manifest)
    exact_keys(payload,{"schema","cells","types","leaves","solver_source_commit","solver_sha256","drat_trim_source_commit","drat_trim_sha256","entries"},"manifest")
    require(payload["schema"]==SCHEMA,"wrong schema")
    require(payload["cells"]==[list(z) for z in CELLS],"cell order mismatch")
    require(payload["types"]==list(TYPES),"overlap-type order mismatch")
    require(payload["leaves"]==len(CELLS)*len(TYPES)==9,"wrong leaf count")
    require(payload["solver_source_commit"]==EXPECTED_CADICAL_SOURCE_COMMIT,"manifest solver source commit mismatch")
    require(payload["drat_trim_source_commit"]==EXPECTED_DRAT_TRIM_SOURCE_COMMIT,"manifest checker source commit mismatch")
    require(payload["drat_trim_sha256"]==EXPECTED_DRAT_TRIM_SHA256,"manifest checker digest mismatch")
    expected_pairs=[(cell,kind) for cell in CELLS for kind in TYPES]
    entries=payload["entries"]
    require(isinstance(entries,list) and len(entries)==9,"manifest entries are not exactly nine")
    expected_files={f"m7-family-d-common-c-{''.join(map(str,c))}-{k}.drat.xz" for c,k in expected_pairs}
    require(x.proof_dir.is_dir(),"proof directory absent")
    actual_files={z.name for z in x.proof_dir.iterdir() if z.is_file()}
    require(actual_files==expected_files,f"artifact-set mismatch extra={actual_files-expected_files} missing={expected_files-actual_files}")
    entry_keys={"index","cell","kind","meta","vars","clauses","cnf_bytes","cnf_sha256","proof_file","proof_bytes","proof_sha256","compressed_proof_bytes","compressed_proof_sha256"}
    with tempfile.TemporaryDirectory(prefix="m7d-common-c-verify-") as td:
        td=Path(td)
        seen=set()
        for index,((cell,kind),entry) in enumerate(zip(expected_pairs,entries)):
            exact_keys(entry,entry_keys,f"entry {index}")
            require(entry["index"]==index,f"entry {index}: index mismatch")
            require(entry["cell"]==list(cell) and entry["kind"]==kind,f"entry {index}: cover key mismatch")
            pair=(tuple(entry["cell"]),entry["kind"]);require(pair not in seen,f"entry {index}: duplicate cover key");seen.add(pair)
            c,_,_,meta=build(cell,kind);cnf=td/f"{index}.cnf";proof=td/f"{index}.drat";write_cnf(c,cnf)
            expected_meta={k:list(v) if isinstance(v,tuple) else v for k,v in meta.items()}
            require(entry["meta"]==expected_meta,f"entry {index}: metadata mismatch")
            require(entry["vars"]==len(c.names) and entry["clauses"]==len(c.clauses),f"entry {index}: dimensions mismatch")
            cnf_raw=cnf.read_bytes();require(entry["cnf_bytes"]==len(cnf_raw) and entry["cnf_sha256"]==digest(cnf_raw),f"entry {index}: regenerated CNF mismatch")
            check=run([x.cnf_checker,str(cnf),"--cell",",".join(map(str,cell)),"--kind",kind],f"entry {index} independent CNF checker")
            markers=[z for z in check.splitlines() if z.startswith("PASS independent common-C CNF")]
            require(len(markers)==1,f"entry {index}: CNF checker marker absent or duplicated")
            require(entry["proof_file"] in expected_files,f"entry {index}: unexpected proof filename")
            packed=(x.proof_dir/entry["proof_file"]).read_bytes()
            require(entry["compressed_proof_bytes"]==len(packed) and entry["compressed_proof_sha256"]==digest(packed),f"entry {index}: compressed proof mismatch")
            try:proof_raw=lzma.decompress(packed,format=lzma.FORMAT_XZ)
            except lzma.LZMAError as exc:raise RuntimeError(f"entry {index}: invalid xz proof") from exc
            require(entry["proof_bytes"]==len(proof_raw) and entry["proof_sha256"]==digest(proof_raw),f"entry {index}: raw proof mismatch")
            proof.write_bytes(proof_raw)
            replay=run([x.drat_trim,str(cnf),str(proof),"-f"],f"entry {index} DRAT replay")
            require(replay.replace("\r","\n").splitlines().count("s VERIFIED")==1,f"entry {index}: replay marker absent or duplicated")
    require(seen==set(expected_pairs),"cover key set is incomplete")
    print("PASS authenticated_regenerated_replayed common-C leaves=9")

if __name__=="__main__":main()
