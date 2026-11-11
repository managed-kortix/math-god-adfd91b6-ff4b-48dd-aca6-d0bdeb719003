#!/usr/bin/env python3
import argparse,json,os,subprocess,tempfile,time
from m5_b6_cnf import emit
from m5_b6_internal_cases import cases
SCHEMA=2

def topo(states):
 out=[0,0,0]
 for st,(u,v) in zip(states,((0,1),(0,2),(1,2))):
  if st==0:out[u]+=1
  elif st==1:out[v]+=1
 return sorted(range(3),key=lambda x:-out[x])
def variants(case):
 i,hc,r,H,states,tail=case;order=topo(states);source=15+order[0]
 if hc==1:return [((9,source),)]
 middle=15+order[1]
 # In the two-high rows vertex 9 is the normalized head of the unique
 # middle->B arc.  It is therefore a distinguished B vertex and cannot be
 # identified with a generic source witness by symmetry.  The five entries
 # below are the complete equality-pattern orbits: source witness tail/non-tail,
 # followed by middle witness internal/same non-tail/distinct non-tail.
 return [
  ((9,source),(source,middle)),
  ((9,source),(10,middle)),
  ((10,source),(source,middle)),
  ((10,source),(10,middle)),
  ((10,source),(11,middle)),
 ]
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",required=True);p.add_argument("--prior");p.add_argument("--cadical",required=True);p.add_argument("--seconds",type=int,default=20);p.add_argument("--output",required=True);a=p.parse_args();selected={x["case"] for x in json.load(open(a.input))["rows"] if x["status"]!="UNSAT"};prior=None
 if a.prior:
  old=json.load(open(a.prior))
  if old.get("schema")!=SCHEMA:raise SystemExit("incompatible prior witness-scout schema")
  prior={(x["case"],x["variant"]) for x in old["rows"] if x["status"]!="UNSAT"}
 rows=[]
 for n,case in enumerate(cases()):
  if n not in selected:continue
  i,hc,r,H,states,tail=case
  for v,W in enumerate(variants(case)):
   if prior is not None and (n,v) not in prior:continue
   with tempfile.TemporaryDirectory() as d:
    f=os.path.join(d,"x.cnf");emit(i,f,hc,r,H,states,tail,W);t=time.monotonic();q=subprocess.run(["timeout",str(a.seconds),a.cadical,"-q",f],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);secs=round(time.monotonic()-t,3)
   st={20:"UNSAT",10:"SAT",124:"UNKNOWN"}.get(q.returncode,f"EXIT_{q.returncode}");rows.append({"case":n,"variant":v,"status":st,"seconds":secs});print(n,v,st,secs,flush=True)
 with open(a.output,"w") as f:json.dump({"schema":SCHEMA,"cap_seconds":a.seconds,"rows":rows},f);f.write("\n")
if __name__=="__main__":main()
