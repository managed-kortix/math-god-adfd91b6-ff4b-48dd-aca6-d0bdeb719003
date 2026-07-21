#!/usr/bin/env python3
"""Compact independent PARI verification using persistent GP workers."""

from __future__ import annotations

import argparse
import hashlib
import multiprocessing as mp
import subprocess

import sympy as s

from pari_verify import gp_matrix
from search_geng import graph6_adjacency


def verify_chunk(graphs: list[str]) -> tuple[int, str, str]:
    gp = subprocess.Popen(
        ["gp", "-q"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, bufsize=1,
    )
    assert gp.stdin is not None and gp.stdout is not None
    gp.stdin.write("\\p 80\n")
    gp.stdin.flush()
    # GP acknowledges the precision command on stdout.
    while "realprecision" not in gp.stdout.readline():
        pass
    x = s.symbols("x")
    minimum: tuple[s.Float, str] | None = None
    try:
        for g6 in graphs:
            a = graph6_adjacency(g6.encode()).astype(int)
            gp.stdin.write(
                f"A={gp_matrix(a)};p=charpoly(A,x);print(Vec(p));"
                f"r=polrootsreal(p);print(sum(i=1,#r,if(r[i]>0,r[i]^2,0))-{len(a)})\n"
            )
            gp.stdin.flush()
            coeff_line = gp.stdout.readline().strip()
            slack_line = gp.stdout.readline().strip()
            if not coeff_line or not slack_line:
                raise RuntimeError(f"GP stopped at {g6}: {gp.stderr.read() if gp.stderr else ''}")
            got = [int(v) for v in coeff_line.strip("[]").split(",")]
            want = [int(v) for v in s.Matrix(a).charpoly(x).all_coeffs()]
            if got != want:
                raise RuntimeError(f"charpoly mismatch {g6}: GP={got} SymPy={want}")
            slack = s.Float(slack_line, 80)
            if slack <= 0:
                raise RuntimeError(f"nonpositive PARI slack {g6}: {slack_line}")
            if minimum is None or slack < minimum[0]:
                minimum = slack, g6
    finally:
        if gp.stdin:
            gp.stdin.write("quit\n")
            gp.stdin.close()
        gp.wait()
    assert minimum is not None
    return len(graphs), minimum[1], str(minimum[0])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-file", "-f", required=True)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    raw = open(args.from_file, "rb").read()
    graphs = [line.decode().strip() for line in raw.splitlines() if line.strip()]
    digest = hashlib.sha256(b"\n".join(g.encode() for g in graphs) + b"\n").hexdigest()
    chunks = [graphs[i::args.workers] for i in range(args.workers)]
    with mp.Pool(args.workers) as pool:
        results = pool.map(verify_chunk, chunks)
    minimum = min((s.Float(slack, 80), g6) for _, g6, slack in results)
    print(f"PASS count={sum(count for count, _, _ in results)} sha256={digest}")
    print(f"minimum_graph6={minimum[1]}")
    print(f"minimum_slack_80d={minimum[0]}")


if __name__ == "__main__":
    main()
