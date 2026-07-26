#!/usr/bin/env python3
"""Emit exact rho=0 or rho=1 order-18 shards indexed by T-hole count."""
import argparse
from snc_cnf import generate, threshold


def emit(r, k, output):
    c = generate(18, 7, 8, robust_witness=True, high_vertices=(1,),
                 forced_witness=(0, 1), arc_minimal=True)
    rho = threshold(c, [c.var(f"a_{x}_{b}") for x in (16, 17)
                        for b in range(9, 16)], f"rho{r}_k{k}")
    if r == 0:
        c.add(-rho[0])
    else:
        c.add(rho[r - 1]); c.add(-rho[r])
    ht = threshold(c, [c.var(f"h_{i}_{j}") for i in range(16)
                       for j in range(i + 1, 16)], f"ht{r}_k{k}")
    if k == 0:
        c.add(-ht[0])
    else:
        c.add(ht[k - 1]); c.add(-ht[k])
    with open(output, "w", encoding="ascii", newline="\n") as f:
        for name, num in c.names.items(): f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for clause in c.clauses: f.write(" ".join(map(str, clause)) + " 0\n")
    print(f"rho={r} k={k} vars={len(c.names)} clauses={len(c.clauses)}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("rho", type=int, choices=(0, 1))
    p.add_argument("k", type=int); p.add_argument("output"); a = p.parse_args()
    if not 0 <= a.k <= 5-a.rho: p.error("k must lie in 0..5-rho")
    emit(a.rho, a.k, a.output)
