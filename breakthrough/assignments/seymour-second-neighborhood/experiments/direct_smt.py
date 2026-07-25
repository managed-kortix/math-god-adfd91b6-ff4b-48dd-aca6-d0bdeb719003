#!/usr/bin/env python3
"""Exact fixed-order SMT search for a counterexample with a rooted layer branch."""
import argparse
import hashlib
import z3


def build(n, bsize, timeout_ms, missing, minimality):
    s, A = 0, range(1, 9)
    B = range(9, 9 + bsize)
    a = [[z3.Bool(f"a_{i}_{j}") for j in range(n)] for i in range(n)]
    q = [[z3.Bool(f"q_{i}_{j}") for j in range(n)] for i in range(n)]
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    for i in range(n):
        solver.add(z3.Not(a[i][i]), z3.Not(q[i][i]))
    for i in range(n):
        for j in range(i + 1, n):
            solver.add(z3.Not(z3.And(a[i][j], a[j][i])))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            r = z3.Or([z3.And(a[i][k], a[k][j]) for k in range(n)])
            solver.add(q[i][j] == z3.And(r, z3.Not(a[i][j])))
    degrees = []
    deficits = []
    for i in range(n):
        d1 = z3.Sum([z3.If(a[i][j], 1, 0) for j in range(n)])
        d2 = z3.Sum([z3.If(q[i][j], 1, 0) for j in range(n)])
        mu2 = z3.Bool(f"mu2_{i}")
        solver.add(d1 >= 8, d1 <= (n + 1) // 2,
                   d2 == d1 - 1 - z3.If(mu2, 1, 0))
        degrees.append(d1); deficits.append(mu2)
    if minimality:
        # Necessary vertex-minimality condition: every deleted vertex u has a
        # tight in-neighbor witness. This is the cheap relaxation of the full
        # deletion-robust second-neighborhood identity.
        for u in range(n):
            solver.add(z3.Or([z3.And(a[w][u], z3.Not(deficits[w]))
                              for w in range(n) if w != u]))
        # Exact necessary arc-minimality inequality.  For e=i->j, g says j is
        # demoted to exact distance two after deletion; lost endpoints are old
        # exact second neighbors whose every two-walk uses j as midpoint.
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                g = z3.Or([z3.And(a[i][k], a[k][j])
                           for k in range(n) if k != j])
                lost = []
                for t in range(n):
                    if t == i:
                        continue
                    alternate = z3.Or([z3.And(a[i][k], a[k][t])
                                       for k in range(n) if k != j])
                    lost.append(z3.And(q[i][t], a[j][t], z3.Not(alternate)))
                loss_count = z3.Sum([z3.If(x, 1, 0) for x in lost])
                solver.add(z3.Implies(a[i][j],
                    z3.If(deficits[i],
                          z3.And(g, loss_count == 0),
                          loss_count <= z3.If(g, 1, 0))))
    # Redundant global edge lower bound materially strengthens propagation.
    solver.add(z3.Sum([z3.If(a[i][j], 1, 0)
                       for i in range(n) for j in range(n)]) >= 8 * n)
    # Canonical rooted |A|=8, |B|=bsize branch.
    for j in range(n):
        solver.add(a[s][j] == z3.BoolVal(j in A))
        if j != s:
            solver.add(q[s][j] == z3.BoolVal(j in B))
    solver.add(z3.Not(deficits[s]) if bsize == 7 else deficits[s])
    # Expose root-layer implications directly.
    R = range(9 + bsize, n)
    for b in B:
        solver.add(z3.Or([a[x][b] for x in A]))
    for x in A:
        for r in R:
            solver.add(z3.Not(a[x][r]))
    if bsize == 6:
        for b in B:
            solver.add(z3.Sum([z3.If(a[x][b], 1, 0) for x in A]) >= 2)
        for x in A:
            solver.add(z3.Or([a[y][x] for y in A]))
        solver.add(z3.Sum([z3.If(a[x][b], 1, 0) for x in A for b in B]) <= 47)
    if n == 18:
        for d in degrees:
            solver.add(z3.Or(d == 8, d == 9))
        absent = z3.Sum([z3.If(z3.And(z3.Not(a[i][j]), z3.Not(a[j][i])), 1, 0)
                         for i in range(n) for j in range(i + 1, n)])
        if missing is not None:
            solver.add(absent == missing)
    # Within each rooted layer, nondecreasing adjacency rows as a light,
    # satisfiability-preserving symmetry break is deliberately omitted: plain
    # integer row ordering can interact with outside labels unless fully proved.
    return solver, a


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--b-size", type=int, choices=(6, 7), required=True)
    p.add_argument("--timeout-ms", type=int, default=300000)
    p.add_argument("--output")
    p.add_argument("--missing", type=int)
    p.add_argument("--minimality", action="store_true")
    args = p.parse_args()
    if args.n < 9 + args.b_size:
        p.error("n too small for fixed layers")
    if args.n * (args.n - 1) // 2 < 8 * args.n:
        print("unsat")
        print("certificate=edge capacity: C(n,2) < 8n")
        return
    if args.n == 17:
        print("unsat")
        print("certificate=minimum degree 8 forces a regular tournament; every in-neighbor is at distance two")
        return
    if args.missing is not None and (args.n != 18 or not 0 <= args.missing <= 9):
        p.error("--missing is currently an n=18 branch in [0,9]")
    solver, a = build(args.n, args.b_size, args.timeout_ms, args.missing,
                      args.minimality)
    result = solver.check()
    print(result)
    if result == z3.sat:
        model = solver.model()
        arcs = [(i, j) for i in range(args.n) for j in range(args.n)
                if z3.is_true(model.eval(a[i][j], model_completion=True))]
        text = str(args.n) + "\n" + "".join(f"{i} {j}\n" for i, j in arcs)
        digest = hashlib.sha256(text.encode()).hexdigest()
        print(f"arcs={len(arcs)} sha256={digest}")
        if args.output:
            with open(args.output, "w", encoding="ascii", newline="\n") as out:
                out.write(text)
            print("wrote=" + args.output)
    if result == z3.unknown:
        print("reason=" + solver.reason_unknown())


if __name__ == "__main__":
    main()
