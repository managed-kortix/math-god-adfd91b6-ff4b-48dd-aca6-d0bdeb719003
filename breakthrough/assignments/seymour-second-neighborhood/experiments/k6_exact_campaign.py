#!/usr/bin/env python3
"""Generate, check, and retain content-addressed LRATs for exact-pressure leaves."""
import argparse,hashlib,json,lzma,os,subprocess,tempfile,time
from concurrent.futures import ProcessPoolExecutor,as_completed

from k6_reduced_full_cuts import emit,keys,multiplicity


def sha(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()


def run_one(job):
 i,root,cadical,checker=job;leaf=os.path.join(root,"leaves",f"{i:04d}.json")
 if os.path.exists(leaf):return i,"SKIP"
 with tempfile.TemporaryDirectory(dir=os.path.join(root,"work")) as d:
  cnf=os.path.join(d,"leaf.cnf");lrat=os.path.join(d,"leaf.lrat");emit(i,cnf,exact_pressure=True)
  t=time.monotonic();r=subprocess.run([cadical,"--lrat","--no-binary","-q",cnf,lrat],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);secs=round(time.monotonic()-t,3)
  if r.returncode!=20:return i,f"SOLVER_{r.returncode}"
  chk=subprocess.run([checker,cnf,lrat],capture_output=True,text=True)
  if chk.returncode or "c VERIFIED" not in chk.stdout:
   # CaDiCaL 1.7.3 may omit a final proof step when the input already contains
   # an empty clause. Supply the one-line RUP derivation from that input clause.
   with open(cnf,encoding="ascii") as f:
    clauses=int(next(x for x in f if x.startswith("p cnf ")).split()[3])
   empty=None
   with open(cnf,encoding="ascii") as f:
    cid=0
    for line in f:
     if line.startswith(("c","p")):continue
     cid+=1
     if line.strip()=="0":empty=cid;break
   if empty is not None:
    with open(lrat,"w",encoding="ascii") as f:f.write(f"{clauses+1} 0 {empty} 0\n")
    chk=subprocess.run([checker,cnf,lrat],capture_output=True,text=True)
   if chk.returncode or "c VERIFIED" not in chk.stdout:return i,"CHECK_FAIL"
  ls=sha(lrat);obj=os.path.join(root,"objects",ls+".lrat.xz");tmp=obj+f".{os.getpid()}.partial"
  with open(lrat,"rb") as src,lzma.open(tmp,"wb",preset=3) as dst:
   while b:=src.read(1<<20):dst.write(b)
  os.replace(tmp,obj)
  rec={"index":i,"key":keys()[i],"multiplicity":multiplicity(keys()[i]),"cnf_sha256":sha(cnf),"cnf_bytes":os.path.getsize(cnf),"lrat_sha256":ls,"lrat_bytes":os.path.getsize(lrat),"object":os.path.basename(obj),"object_sha256":sha(obj),"object_bytes":os.path.getsize(obj),"seconds":secs,"status":"UNSAT_VERIFIED"}
  tmp=leaf+".partial"
  with open(tmp,"w") as f:json.dump(rec,f,sort_keys=True);f.write("\n")
  os.replace(tmp,leaf);return i,"UNSAT_VERIFIED"


def main():
 p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--cadical",required=True);p.add_argument("--checker",required=True);p.add_argument("--jobs",type=int,default=4);a=p.parse_args()
 for x in ("leaves","objects","work"):os.makedirs(os.path.join(a.root,x),exist_ok=True)
 jobs=[(i,a.root,a.cadical,a.checker) for i in range(len(keys()))]
 with ProcessPoolExecutor(max_workers=a.jobs) as ex:
  fs=[ex.submit(run_one,j) for j in jobs]
  for f in as_completed(fs):print(*f.result(),flush=True)

if __name__=="__main__":main()
