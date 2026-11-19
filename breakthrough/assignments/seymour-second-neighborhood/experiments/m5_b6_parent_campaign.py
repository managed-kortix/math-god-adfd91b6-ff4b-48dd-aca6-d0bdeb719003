#!/usr/bin/env python3
"""Direct content-addressed LRAT campaign for all 4,355 m5 B6 parents."""
import argparse,hashlib,json,lzma,os,subprocess,tempfile,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from m5_b6_cnf import emit
from m5_b6_shapes import placements,payload
EXPECTED="e5873a71afa80a126079e2aa7ce716f7d6c8347c241489b616cfb8f67d305ed9"
def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()
def verify_saved(i,root,checker):
 meta=os.path.join(root,"leaves",f"{i:04d}.json")
 try:
  with open(meta,encoding="utf-8") as f:r=json.load(f)
  name,w=placements()[i];key=[name,list(w)]
  if r.get("index")!=i or r.get("key")!=key or r.get("status")!="UNSAT_VERIFIED":return False,"META_MISMATCH"
  proofhash=r.get("lrat_sha256");basename=proofhash+".lrat.xz"
  if r.get("object")!=basename:return False,"OBJECT_NAME_MISMATCH"
  obj=os.path.join(root,"objects",basename)
  if not os.path.isfile(obj) or sha(obj)!=r.get("object_sha256") or os.path.getsize(obj)!=r.get("object_bytes"):return False,"OBJECT_MISMATCH"
  with tempfile.TemporaryDirectory(dir=os.path.join(root,"work")) as d:
   cnf=os.path.join(d,"x.cnf");proof=os.path.join(d,"x.lrat");emit(i,cnf)
   if sha(cnf)!=r.get("cnf_sha256") or os.path.getsize(cnf)!=r.get("cnf_bytes"):return False,"CNF_MISMATCH"
   h=hashlib.sha256();size=0
   with lzma.open(obj,"rb") as src,open(proof,"wb") as dst:
    while b:=src.read(1<<20):dst.write(b);h.update(b);size+=len(b)
   if h.hexdigest()!=proofhash or size!=r.get("lrat_bytes"):return False,"LRAT_MISMATCH"
   q=subprocess.run([checker,cnf,proof],capture_output=True,text=True)
   if q.returncode or "c VERIFIED" not in q.stdout:return False,"READBACK_CHECK_FAIL"
  return True,"READBACK_VERIFIED"
 except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError,lzma.LZMAError) as e:return False,"READBACK_ERROR_"+type(e).__name__
def one(job):
 i,root,solver,checker=job;meta=os.path.join(root,"leaves",f"{i:04d}.json")
 if os.path.exists(meta):
  ok,status=verify_saved(i,root,checker)
  return i,status if ok else status
 with tempfile.TemporaryDirectory(dir=os.path.join(root,"work")) as d:
  cnf=os.path.join(d,"x.cnf");proof=os.path.join(d,"x.lrat");emit(i,cnf);t=time.monotonic();q=subprocess.run([solver,"--lrat","--no-binary","-q",cnf,proof],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);secs=round(time.monotonic()-t,3)
  if q.returncode!=20:return i,f"SOLVER_{q.returncode}"
  q=subprocess.run([checker,cnf,proof],capture_output=True,text=True)
  if q.returncode or "c VERIFIED" not in q.stdout:return i,"CHECK_FAIL"
  ps=sha(proof);obj=os.path.join(root,"objects",ps+".lrat.xz");tmp=obj+f".{os.getpid()}.partial"
  with open(proof,"rb") as src,lzma.open(tmp,"wb",preset=3) as dst:
   while b:=src.read(1<<20):dst.write(b)
  os.replace(tmp,obj);name,w=placements()[i];r={"index":i,"key":[name,w],"cnf_sha256":sha(cnf),"cnf_bytes":os.path.getsize(cnf),"lrat_sha256":ps,"lrat_bytes":os.path.getsize(proof),"object":os.path.basename(obj),"object_sha256":sha(obj),"object_bytes":os.path.getsize(obj),"seconds":secs,"status":"UNSAT_VERIFIED"}
  # Check the persisted compressed object, not only the temporary solver file.
  with tempfile.NamedTemporaryFile(dir=d) as restored:
   h=hashlib.sha256();size=0
   with lzma.open(obj,"rb") as src:
    while b:=src.read(1<<20):restored.write(b);h.update(b);size+=len(b)
   restored.flush()
   if h.hexdigest()!=ps or size!=r["lrat_bytes"]:return i,"PERSISTED_OBJECT_MISMATCH"
   q=subprocess.run([checker,cnf,restored.name],capture_output=True,text=True)
   if q.returncode or "c VERIFIED" not in q.stdout:return i,"PERSISTED_CHECK_FAIL"
  with open(meta+".partial","w") as f:json.dump(r,f,sort_keys=True);f.write("\n")
  os.replace(meta+".partial",meta);return i,"UNSAT_VERIFIED"
def main():
 p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--cadical",required=True);p.add_argument("--checker",required=True);p.add_argument("--jobs",type=int,default=4);a=p.parse_args()
 rows=placements()
 if len(rows)!=4355 or hashlib.sha256(payload()).hexdigest()!=EXPECTED:raise RuntimeError("placement cover identity mismatch")
 for d in ("leaves","objects","work"):os.makedirs(os.path.join(a.root,d),exist_ok=True)
 with ProcessPoolExecutor(max_workers=a.jobs) as ex:
  fs=[ex.submit(one,(i,a.root,a.cadical,a.checker)) for i in range(len(placements()))]
  results=[]
  for f in as_completed(fs):
   z=f.result();results.append(z);print(*z,flush=True)
 good={"UNSAT_VERIFIED","READBACK_VERIFIED"}
 if sorted(i for i,_ in results)!=list(range(len(rows))) or any(st not in good for _,st in results):raise SystemExit("campaign incomplete or readback failed")
 print(f"PASS leaves={len(rows)}",flush=True)
if __name__=="__main__":main()
