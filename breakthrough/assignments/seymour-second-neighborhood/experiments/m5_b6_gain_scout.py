#!/usr/bin/env python3
import argparse,json,os,subprocess,tempfile,time
from m5_b6_cnf import emit
from m5_b6_internal_cases import cases
from m5_b6_witness_scout import variants
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",required=True);p.add_argument("--cadical",required=True);p.add_argument("--seconds",type=int,default=20);p.add_argument("--output",required=True);a=p.parse_args();hard={(x["case"],x["variant"],x["gain"],x["losses"]) for x in json.load(open(a.input))["rows"] if x["status"]!="UNSAT"};rows=[]
 for n,case in enumerate(cases()):
  i,hc,r,H,states,tail=case
  for v,W in enumerate(variants(case)):
   if (n,v,1,0) not in hard:continue
   for block in range(4):
    with tempfile.TemporaryDirectory() as d:
     f=os.path.join(d,"x.cnf");emit(i,f,hc,r,H,states,tail,W,(1,0),block);t=time.monotonic();q=subprocess.run(["timeout",str(a.seconds),a.cadical,"-q",f],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);secs=round(time.monotonic()-t,3)
    st={20:"UNSAT",10:"SAT",124:"UNKNOWN"}.get(q.returncode,f"EXIT_{q.returncode}");rows.append({"case":n,"variant":v,"block":block,"status":st,"seconds":secs});print(n,v,block,st,secs,flush=True)
 with open(a.output,"w") as f:json.dump({"cap_seconds":a.seconds,"rows":rows},f);f.write("\n")
if __name__=="__main__":main()
