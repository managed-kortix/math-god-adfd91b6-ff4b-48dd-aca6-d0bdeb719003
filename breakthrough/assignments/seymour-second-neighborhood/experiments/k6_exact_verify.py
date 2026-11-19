#!/usr/bin/env python3
"""Freshly verify every retained exact-pressure campaign proof object."""
import argparse,hashlib,json,lzma,os,subprocess,tempfile
from k6_reduced_full_cuts import emit,keys,multiplicity

EXPECTED_LEAVES=1110
EXPECTED_LABELLED=3171168


def require(condition,message):
 if not condition: raise RuntimeError(message)


def sha(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()


def checked_lrat(checker,cnf,proof,ordinal):
 q=subprocess.run([checker,cnf,proof],capture_output=True,text=True)
 require(q.returncode==0,f"leaf {ordinal}: checker exit {q.returncode}: {q.stdout}{q.stderr}")
 require(q.stdout.splitlines().count("c VERIFIED")==1,
         f"leaf {ordinal}: checker did not emit exactly one literal c VERIFIED")


def main():
 p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--checker",required=True);a=p.parse_args()
 require(os.path.isfile(a.checker) and os.access(a.checker,os.X_OK),"proof checker is not an executable file")
 work=os.path.join(a.root,"work");os.makedirs(work,exist_ok=True)
 cover=keys();require(len(cover)==EXPECTED_LEAVES,f"cover has {len(cover)} leaves")
 total=0
 for i,k in enumerate(cover):
  meta=os.path.join(a.root,"leaves",f"{i:04d}.json")
  with open(meta,encoding="utf-8") as f:r=json.load(f)
  require(r["index"]==i,f"leaf {i}: index mismatch")
  require(tuple(r["key"])==k,f"leaf {i}: key mismatch")
  require(r["multiplicity"]==multiplicity(k),f"leaf {i}: multiplicity mismatch")
  require(r["status"]=="UNSAT_VERIFIED",f"leaf {i}: unverified status {r['status']}")
  obj=os.path.join(a.root,"objects",r["object"])
  require(os.path.isfile(obj),f"leaf {i}: missing object {obj}")
  require(sha(obj)==r["object_sha256"],f"leaf {i}: object digest mismatch")
  with tempfile.TemporaryDirectory(dir=work) as d:
   cnf=os.path.join(d,"x.cnf");proof=os.path.join(d,"x.lrat")
   emit(i,cnf,exact_pressure=True)
   require(sha(cnf)==r["cnf_sha256"],f"leaf {i}: regenerated CNF digest mismatch")
   with lzma.open(obj,"rb") as src,open(proof,"wb") as dst:
    while b:=src.read(1<<20):dst.write(b)
   require(sha(proof)==r["lrat_sha256"],f"leaf {i}: raw LRAT digest mismatch")
   checked_lrat(a.checker,cnf,proof,i)
  total+=r["multiplicity"]
 require(total==EXPECTED_LABELLED,f"labelled multiplicity {total} != {EXPECTED_LABELLED}")
 print(f"PASS leaves={len(cover)} labelled={total}")


if __name__=="__main__":main()
