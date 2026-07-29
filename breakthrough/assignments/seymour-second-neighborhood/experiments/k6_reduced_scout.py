#!/usr/bin/env python3
"""Run deterministic capped CaDiCaL scouts over the 65 reduced k6 cubes."""
import argparse
import json
import os
import subprocess
import tempfile
import time

from k6_reduced_cubes import keys, emit


def main():
    p=argparse.ArgumentParser();p.add_argument("--cadical",required=True)
    p.add_argument("--seconds",type=int,default=30);p.add_argument("--output",required=True)
    a=p.parse_args();rows=[]
    for i,k in enumerate(keys()):
        with tempfile.TemporaryDirectory() as d:
            cnf=os.path.join(d,"x.cnf");emit(i,cnf);start=time.monotonic()
            r=subprocess.run(["timeout",str(a.seconds),a.cadical,"-q",cnf],
                             stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            elapsed=round(time.monotonic()-start,3)
        status={10:"SAT",20:"UNSAT",124:"UNKNOWN"}.get(r.returncode,f"EXIT_{r.returncode}")
        rows.append({"index":i,"key":list(k),"status":status,"seconds":elapsed})
        print(i,status,elapsed,flush=True)
    with open(a.output,"w",encoding="ascii") as f:
        json.dump({"cap_seconds":a.seconds,"rows":rows},f,indent=2,sort_keys=True);f.write("\n")


if __name__=="__main__":main()
