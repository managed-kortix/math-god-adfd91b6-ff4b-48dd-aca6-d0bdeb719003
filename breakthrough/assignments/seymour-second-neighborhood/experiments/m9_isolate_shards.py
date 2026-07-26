#!/usr/bin/env python3
"""Emit aggregate m=9 shards rooted at a robust witness of a missing isolate."""
import argparse
from snc_cnf import generate, threshold


def exact(c, outputs, value):
    if value == 0: c.add(-outputs[0])
    else: c.add(outputs[value-1]); c.add(-outputs[value])


def emit(rho_value, k, output):
    c = generate(18, 7, 9, robust_witness=True, high_vertices=(),
                 forced_witness=(0, 1), arc_minimal=True)
    for j in range(18):
        if j != 1: c.add(-c.var(f"h_{min(1,j)}_{max(1,j)}"))
    rho = threshold(c, [c.var(f"a_{x}_{b}") for x in (16,17)
                        for b in range(9,16)], f"m9_rho{rho_value}_k{k}")
    exact(c, rho, rho_value)
    ht = threshold(c, [c.var(f"h_{i}_{j}") for i in range(16)
                       for j in range(i+1,16)], f"m9_ht{rho_value}_k{k}")
    exact(c, ht, k)
    with open(output,"w",encoding="ascii",newline="\n") as f:
        for name,num in c.names.items(): f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for clause in c.clauses: f.write(" ".join(map(str,clause))+" 0\n")
    print(f"rho={rho_value} k={k} vars={len(c.names)} clauses={len(c.clauses)}")


if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("rho",type=int); p.add_argument("k",type=int)
    p.add_argument("output"); a=p.parse_args()
    if not 0<=a.rho<=6 or not 0<=a.k<=6-a.rho: p.error("need 0<=rho<=6 and 0<=k<=6-rho")
    emit(a.rho,a.k,a.output)
