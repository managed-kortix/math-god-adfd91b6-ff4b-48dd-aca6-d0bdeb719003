#!/usr/bin/env python3
"""Compact independent PARI verification using persistent GP workers."""

from __future__ import annotations

import argparse
import hashlib
import multiprocessing as mp
import subprocess

from pari_verify import gp_matrix
from search_geng import graph6_adjacency


def verify_chunk(graphs: list[str]) -> tuple[int, str, str, str]:
    matrices = []
    for g6 in graphs:
        a = graph6_adjacency(g6.encode()).astype(int)
        matrices.append((g6, a))
    commands = ["\\p 80"]
    for _, a in matrices:
        commands.append(
            f"A={gp_matrix(a)};p=charpoly(A,x);print(Vec(p));"
            f"r=polrootsreal(p);print(sum(i=1,#r,if(r[i]>0,r[i]^2,0))-{len(a)})"
        )
    commands.append("quit")
    run = subprocess.run(
        ["gp", "-q"], input="\n".join(commands) + "\n", text=True,
        capture_output=True, check=True,
    )
    lines = [line.strip() for line in run.stdout.splitlines()
             if line.strip() and "realprecision" not in line]
    if len(lines) != 2 * len(graphs):
        raise RuntimeError(f"expected {2*len(graphs)} GP lines, got {len(lines)}")
    minimum: tuple[float, str, str] | None = None
    poly_digest = hashlib.sha256()
    for index, (g6, a) in enumerate(matrices):
            coeff_line = lines[2 * index]
            slack_line = lines[2 * index + 1]
            # Vec(charpoly) is an exact integer coefficient vector produced by
            # PARI. Parsing every coefficient also rejects malformed output.
            got = [int(v) for v in coeff_line.strip("[]").split(",")]
            if len(got) != len(a) + 1 or got[0] != 1:
                raise RuntimeError(f"malformed charpoly {g6}: {got}")
            poly_digest.update((g6 + "\t" + ",".join(map(str, got)) + "\n").encode())
            slack_float = float(slack_line)
            if slack_float <= 0:
                raise RuntimeError(f"nonpositive PARI slack {g6}: {slack_line}")
            if minimum is None or slack_float < minimum[0]:
                minimum = slack_float, g6, slack_line
    assert minimum is not None
    return len(graphs), minimum[1], minimum[2], poly_digest.hexdigest()


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
    minimum = min((float(slack), g6, slack) for _, g6, slack, _ in results)
    print(f"PASS count={sum(count for count, _, _, _ in results)} sha256={digest}")
    print(f"minimum_graph6={minimum[1]}")
    print(f"minimum_slack_80d={minimum[2]}")
    print("worker_exact_charpoly_sha256=" + ",".join(d for _, _, _, d in results))


if __name__ == "__main__":
    main()
