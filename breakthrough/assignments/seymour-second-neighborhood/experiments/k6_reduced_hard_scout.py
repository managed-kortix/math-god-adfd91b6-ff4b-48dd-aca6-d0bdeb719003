#!/usr/bin/env python3
"""Capped scouts for the 671 complete-cut children of hard primary cubes."""
import argparse,json,os,subprocess,tempfile,time

from k6_reduced_full_cuts import emit,keys
from k6_reduced_hard_cuts import hard_indices,parent


def main():
 p=argparse.ArgumentParser();p.add_argument("--cadical",required=True);p.add_argument("--seconds",type=int,default=5);p.add_argument("--output",required=True);p.add_argument("--exact-pressure",action="store_true");a=p.parse_args()
 hard=hard_indices();indices=[i for i,k in enumerate(keys()) if parent(k) in hard];rows=[]
 for n,i in enumerate(indices):
  with tempfile.TemporaryDirectory() as d:
   cnf=os.path.join(d,"x.cnf");emit(i,cnf,packet_pressure=not a.exact_pressure,exact_pressure=a.exact_pressure);start=time.monotonic();r=subprocess.run(["timeout",str(a.seconds),a.cadical,"-q",cnf],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);elapsed=round(time.monotonic()-start,3)
  status={10:"SAT",20:"UNSAT",124:"UNKNOWN"}.get(r.returncode,f"EXIT_{r.returncode}");rows.append({"index":i,"status":status,"seconds":elapsed});print(n,i,status,elapsed,flush=True)
 with open(a.output,"w") as f:json.dump({"cap_seconds":a.seconds,"rows":rows},f,indent=2,sort_keys=True);f.write("\n")

if __name__=="__main__":main()
