#!/usr/bin/env python3
import argparse,json,os,subprocess,tempfile,time
from m5_b6_cnf import emit
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",required=True);p.add_argument("--cadical",required=True);p.add_argument("--seconds",type=int,default=5);p.add_argument("--output",required=True);a=p.parse_args();parents=[r["index"] for r in json.load(open(a.input))["rows"] if r["status"]!="UNSAT"];rows=[]
 for i in parents:
  for hc in (0,1,2,3):
   for r in range(19):
    with tempfile.TemporaryDirectory() as d:
     f=os.path.join(d,"x.cnf");emit(i,f,hc,r);t=time.monotonic();q=subprocess.run(["timeout",str(a.seconds),a.cadical,"-q",f],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);secs=round(time.monotonic()-t,3)
    st={20:"UNSAT",10:"SAT",124:"UNKNOWN"}.get(q.returncode,f"EXIT_{q.returncode}");rows.append({"index":i,"high_c":hc,"r":r,"status":st,"seconds":secs});print(i,hc,r,st,secs,flush=True)
 with open(a.output,"w") as f:json.dump({"cap_seconds":a.seconds,"rows":rows},f);f.write("\n")
if __name__=="__main__":main()
