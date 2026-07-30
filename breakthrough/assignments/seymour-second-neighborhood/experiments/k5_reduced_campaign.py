#!/usr/bin/env python3
"""Retain content-addressed LRATs for all 931 reduced k5 packet leaves."""
import argparse,hashlib,json,lzma,os,subprocess,tempfile,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from k5_reduced_cuts import emit,keys,multiplicity

def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()
def one(job):
 i,root,solver,checker=job;meta=os.path.join(root,"leaves",f"{i:04d}.json")
 if os.path.exists(meta):return i,"SKIP"
 with tempfile.TemporaryDirectory(dir=os.path.join(root,"work")) as d:
  cnf=os.path.join(d,"x.cnf");proof=os.path.join(d,"x.lrat");emit(i,cnf);t=time.monotonic();r=subprocess.run([solver,"--lrat","--no-binary","-q",cnf,proof],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);secs=round(time.monotonic()-t,3)
  if r.returncode!=20:return i,f"SOLVER_{r.returncode}"
  q=subprocess.run([checker,cnf,proof],capture_output=True,text=True)
  if q.returncode or "c VERIFIED" not in q.stdout:return i,"CHECK_FAIL"
  ps=sha(proof);obj=os.path.join(root,"objects",ps+".lrat.xz");tmp=obj+f".{os.getpid()}.partial"
  with open(proof,"rb") as src,lzma.open(tmp,"wb",preset=3) as dst:
   while b:=src.read(1<<20):dst.write(b)
  os.replace(tmp,obj);rec={"index":i,"key":keys()[i],"multiplicity":multiplicity(keys()[i]),"cnf_sha256":sha(cnf),"cnf_bytes":os.path.getsize(cnf),"lrat_sha256":ps,"lrat_bytes":os.path.getsize(proof),"object":os.path.basename(obj),"object_sha256":sha(obj),"object_bytes":os.path.getsize(obj),"seconds":secs,"status":"UNSAT_VERIFIED"}
  with open(meta+".partial","w") as f:json.dump(rec,f,sort_keys=True);f.write("\n")
  os.replace(meta+".partial",meta);return i,"UNSAT_VERIFIED"
def main():
 p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--cadical",required=True);p.add_argument("--checker",required=True);p.add_argument("--jobs",type=int,default=4);a=p.parse_args()
 for d in ("leaves","objects","work"):os.makedirs(os.path.join(a.root,d),exist_ok=True)
 with ProcessPoolExecutor(max_workers=a.jobs) as ex:
  fs=[ex.submit(one,(i,a.root,a.cadical,a.checker)) for i in range(len(keys()))]
  for f in as_completed(fs):print(*f.result(),flush=True)
if __name__=="__main__":main()
