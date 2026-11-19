#!/usr/bin/env python3
"""Generate the exact nine-leaf common-C DRAT package and manifest."""
import argparse
import hashlib
import json
import lzma
import subprocess
import tempfile
from pathlib import Path
from m7_family_d_common_c_cnf import CELLS,TYPES,build,write_cnf

SCHEMA="m7-family-d-common-c-v1"
CADICAL_SOURCE_COMMIT="38e073b389a877b0a0d3c91136d2443ab95fdeba"
DRAT_TRIM_SOURCE_COMMIT="2e3b2dc0ecf938addbd779d42877b6ed69d9a985"


def require(condition,message):
    if not condition:raise RuntimeError(message)


def digest(raw):return hashlib.sha256(raw).hexdigest()


def run_checked(cmd,description):
    run=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    require(run.returncode==0,f"{description}: exit {run.returncode}: {run.stdout[-2000:]}")
    return run.stdout


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--solver",required=True);p.add_argument("--drat-trim",required=True)
    p.add_argument("--cnf-checker",required=True);p.add_argument("--proof-dir",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True);p.add_argument("--timeout",type=int,default=300)
    x=p.parse_args()
    x.proof_dir.mkdir(parents=True,exist_ok=True)
    require(not any(x.proof_dir.iterdir()),"proof directory must be empty")
    entries=[]
    with tempfile.TemporaryDirectory(prefix="m7d-common-c-campaign-") as td:
        td=Path(td)
        index=0
        for cell in CELLS:
            for kind in TYPES:
                c,_,_,meta=build(cell,kind)
                stem=f"m7-family-d-common-c-{''.join(map(str,cell))}-{kind}"
                cnf=td/(stem+".cnf");proof=td/(stem+".drat");model=td/(stem+".model")
                write_cnf(c,cnf)
                checker_out=run_checked([x.cnf_checker,str(cnf),"--cell",",".join(map(str,cell)),"--kind",kind],f"leaf {index} CNF checker")
                require("PASS independent common-C CNF" in checker_out,f"leaf {index}: checker success marker absent")
                solve=subprocess.run([x.solver,"--no-colors","-t",str(x.timeout),"-w",str(model),str(cnf),str(proof)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                require(solve.returncode==20,f"leaf {index}: solver did not return UNSAT: rc={solve.returncode}: {solve.stdout[-2000:]}")
                replay=run_checked([x.drat_trim,str(cnf),str(proof),"-f"],f"leaf {index} DRAT replay")
                require(replay.replace("\r","\n").splitlines().count("s VERIFIED")==1,f"leaf {index}: replay marker absent or duplicated")
                cnf_raw=cnf.read_bytes();proof_raw=proof.read_bytes()
                packed=lzma.compress(proof_raw,format=lzma.FORMAT_XZ,preset=9)
                target=x.proof_dir/(stem+".drat.xz");target.write_bytes(packed)
                entries.append({"index":index,"cell":list(cell),"kind":kind,"meta":{k:list(v) if isinstance(v,tuple) else v for k,v in meta.items()},
                    "vars":len(c.names),"clauses":len(c.clauses),"cnf_bytes":len(cnf_raw),"cnf_sha256":digest(cnf_raw),
                    "proof_file":target.name,"proof_bytes":len(proof_raw),"proof_sha256":digest(proof_raw),
                    "compressed_proof_bytes":len(packed),"compressed_proof_sha256":digest(packed)})
                index+=1
    expected={e["proof_file"] for e in entries};actual={z.name for z in x.proof_dir.iterdir() if z.is_file()}
    require(actual==expected,f"artifact-set mismatch extra={actual-expected} missing={expected-actual}")
    payload={"schema":SCHEMA,"cells":[list(z) for z in CELLS],"types":list(TYPES),"leaves":len(entries),
             "solver_source_commit":CADICAL_SOURCE_COMMIT,"solver_sha256":digest(Path(x.solver).read_bytes()),
             "drat_trim_source_commit":DRAT_TRIM_SOURCE_COMMIT,"drat_trim_sha256":digest(Path(x.drat_trim).read_bytes()),"entries":entries}
    x.manifest.write_text(json.dumps(payload,indent=2,separators=(",",": "))+"\n",encoding="ascii")
    print(f"PASS generated_checked_replayed leaves={len(entries)}")
    print(f"PASS manifest_sha256={digest(x.manifest.read_bytes())}")

if __name__=="__main__":main()
