#!/usr/bin/env python3
import argparse,json,os,subprocess,tempfile,time
from m5_b6_cnf import emit
from m5_b6_shapes import placements
def main():
 p=argparse.ArgumentParser();p.add_argument("--cadical",required=True);p.add_argument("--seconds",type=int,default=2);p.add_argument("--output",required=True);a=p.parse_args();rows=[]
 for i in range(len(placements())):
  with tempfile.TemporaryDirectory() as d:
   f=os.path.join(d,"x.cnf");emit(i,f);t=time.monotonic();r=subprocess.run(["timeout",str(a.seconds),a.cadical,"-q",f],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);secs=round(time.monotonic()-t,3)
  st={20:"UNSAT",10:"SAT",124:"UNKNOWN"}.get(r.returncode,f"EXIT_{r.returncode}");rows.append({"index":i,"status":st,"seconds":secs});print(i,st,secs,flush=True)
 with open(a.output,"w") as f:json.dump({"cap_seconds":a.seconds,"rows":rows},f);f.write("\n")
if __name__=="__main__":main()
