#!/usr/bin/env python3
"""Split an m=9, k=3 isolate shard by the unlabeled T-hole shape."""
import argparse
from snc_cnf import generate, threshold

PROFILES = {"matching": (0, 0), "p3_edge": (1, 0), "p4": (2, 0),
            "claw": (1, 1), "triangle": (3, 0)}


def exact(c, outs, value):
    if value == 0: c.add(-outs[0])
    elif value == len(outs): c.add(outs[-1])
    else: c.add(outs[value-1]); c.add(-outs[value])


def emit(rho_value, shape, output):
    c=generate(18,7,9,robust_witness=True,high_vertices=(),
               forced_witness=(0,1),arc_minimal=True)
    for j in range(18):
        if j != 1: c.add(-c.var(f"h_{min(1,j)}_{max(1,j)}"))
    rho=threshold(c,[c.var(f"a_{x}_{b}") for x in (16,17)
                     for b in range(9,16)],f"m9s_r{rho_value}_{shape}")
    exact(c,rho,rho_value)
    holes=[c.var(f"h_{i}_{j}") for i in range(16) for j in range(i+1,16)]
    exact(c,threshold(c,holes,f"m9s_ht_r{rho_value}_{shape}"),3)
    ge2=[]; ge3=[]
    for v in range(16):
        inc=[c.var(f"h_{min(v,u)}_{max(v,u)}") for u in range(16) if u!=v]
        deg=threshold(c,inc,f"m9s_deg_{v}_r{rho_value}_{shape}")
        ge2.append(deg[1]); ge3.append(deg[2])
    n2,n3=PROFILES[shape]
    exact(c,threshold(c,ge2,f"m9s_n2_r{rho_value}_{shape}"),n2)
    exact(c,threshold(c,ge3,f"m9s_n3_r{rho_value}_{shape}"),n3)
    with open(output,"w",encoding="ascii",newline="\n") as f:
        for name,num in c.names.items(): f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for clause in c.clauses: f.write(" ".join(map(str,clause))+" 0\n")
    print(f"rho={rho_value} shape={shape} vars={len(c.names)} clauses={len(c.clauses)}")


if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("rho",type=int,choices=range(4))
    p.add_argument("shape",choices=PROFILES); p.add_argument("output")
    a=p.parse_args(); emit(a.rho,a.shape,a.output)
