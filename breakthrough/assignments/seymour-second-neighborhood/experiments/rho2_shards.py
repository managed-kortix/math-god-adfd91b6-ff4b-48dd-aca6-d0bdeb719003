#!/usr/bin/env python3
"""Emit exact rho=2 order-18 shards, indexed by k=number of T-holes."""
import argparse
from snc_cnf import generate, threshold


def emit(k, output):
    c = generate(18, 7, 8, robust_witness=True, high_vertices=(1,),
                 forced_witness=(0, 1), arc_minimal=True)
    rho = threshold(c, [c.var(f"a_{x}_{b}") for x in (16, 17)
                        for b in range(9, 16)], f"rho2_k{k}")
    c.add(rho[1]); c.add(-rho[2])
    ht = threshold(c, [c.var(f"h_{i}_{j}") for i in range(16)
                       for j in range(i + 1, 16)], f"ht2_k{k}")
    if k == 0:
        c.add(-ht[0])
    else:
        c.add(ht[k - 1]); c.add(-ht[k])
    with open(output, "w", encoding="ascii", newline="\n") as f:
        for name, num in c.names.items():
            f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for clause in c.clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    print(f"k={k} vars={len(c.names)} clauses={len(c.clauses)}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("k", type=int, choices=range(4))
    p.add_argument("output"); a = p.parse_args(); emit(a.k, a.output)
