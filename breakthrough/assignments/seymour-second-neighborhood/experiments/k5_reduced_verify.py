#!/usr/bin/env python3
"""Fresh verifier for every reduced k5 packet LRAT object."""
import argparse,hashlib,json,lzma,os,subprocess,tempfile
from k5_reduced_cuts import emit,keys,multiplicity
def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--checker",required=True);a=p.parse_args();total=0
 for i,k in enumerate(keys()):
  with open(os.path.join(a.root,"leaves",f"{i:04d}.json")) as f:r=json.load(f)
  assert r["index"]==i and tuple(r["key"])==k and r["multiplicity"]==multiplicity(k) and r["status"]=="UNSAT_VERIFIED"
  obj=os.path.join(a.root,"objects",r["object"]);assert sha(obj)==r["object_sha256"]
  with tempfile.TemporaryDirectory(dir=os.path.join(a.root,"work")) as d:
   cnf=os.path.join(d,"x.cnf");proof=os.path.join(d,"x.lrat");emit(i,cnf);assert sha(cnf)==r["cnf_sha256"]
   with lzma.open(obj,"rb") as src,open(proof,"wb") as dst:
    while b:=src.read(1<<20):dst.write(b)
   assert sha(proof)==r["lrat_sha256"]
   q=subprocess.run([a.checker,cnf,proof],capture_output=True,text=True);assert q.returncode==0 and "c VERIFIED" in q.stdout
  total+=r["multiplicity"]
 print(f"PASS leaves={len(keys())} labelled={total}")
if __name__=="__main__":main()
