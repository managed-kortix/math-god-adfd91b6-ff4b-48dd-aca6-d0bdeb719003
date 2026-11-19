#!/usr/bin/env python3
import argparse,json,os,subprocess,tempfile,time
from m5_b6_cnf import emit
from m5_b6_internal_cases import cases
def main():
 p=argparse.ArgumentParser();p.add_argument("--cadical",required=True);p.add_argument("--seconds",type=int,default=5);p.add_argument("--output",required=True);p.add_argument("--input");a=p.parse_args();rows=[]
 selected=None
 if a.input:selected={x["case"] for x in json.load(open(a.input))["rows"] if x["status"]!="UNSAT"}
 for n,(i,hc,r,H,states,tail) in enumerate(cases()):
  if selected is not None and n not in selected:continue
  with tempfile.TemporaryDirectory() as d:
   f=os.path.join(d,"x.cnf");emit(i,f,hc,r,H,states,tail);t=time.monotonic();q=subprocess.run(["timeout",str(a.seconds),a.cadical,"-q",f],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);secs=round(time.monotonic()-t,3)
  st={20:"UNSAT",10:"SAT",124:"UNKNOWN"}.get(q.returncode,f"EXIT_{q.returncode}");rows.append({"case":n,"parent":i,"status":st,"seconds":secs});print(n,i,st,secs,flush=True)
 with open(a.output,"w") as f:json.dump({"cap_seconds":a.seconds,"rows":rows},f);f.write("\n")
if __name__=="__main__":main()
