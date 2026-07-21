#!/usr/bin/env python3
"""Independent PARI/GP verification of graph characteristic polynomials/slack."""

from __future__ import annotations

import argparse
import subprocess

import sympy as s

from search_geng import graph6_adjacency


def gp_matrix(a) -> str:
    return "[" + ";".join(",".join(str(int(v)) for v in row) for row in a) + "]"


def verify(g6: str) -> tuple[str, str]:
    a = graph6_adjacency(g6.encode()).astype(int)
    x = s.symbols("x")
    expected = str(s.Poly(s.Matrix(a).charpoly(x).as_expr(), x).as_expr()).replace("**", "^")
    script = f"""\\p 80
A={gp_matrix(a)};
p=charpoly(A,x);
print(p);
r=polrootsreal(p);
sp=sum(i=1,#r,if(r[i]>0,r[i]^2,0));
print(sp-{len(a)});
quit
"""
    run = subprocess.run(["gp", "-q"], input=script, text=True, capture_output=True, check=True)
    lines = [
        line.strip()
        for line in run.stdout.splitlines()
        if line.strip() and "realprecision" not in line
    ]
    if len(lines) != 2:
        raise RuntimeError(f"unexpected GP output: {run.stdout!r} stderr={run.stderr!r}")
    # Compare exact coefficient vectors in Python after parsing GP's exact polynomial.
    got = s.Poly(s.sympify(lines[0].replace("^", "**")), x)
    want = s.Poly(s.sympify(expected.replace("^", "**")), x)
    if got != want:
        raise RuntimeError(f"charpoly mismatch: GP={got.as_expr()} SymPy={want.as_expr()}")
    return lines[0], lines[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-file", "-f", required=True)
    args = parser.parse_args()
    for line in open(args.from_file):
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        g6 = fields[1] if len(fields) > 1 else fields[0]
        poly, slack = verify(g6)
        print(f"{g6}\tPARI_CHARPOLY_MATCH\tslack={slack}\tpoly={poly}")


if __name__ == "__main__":
    main()
