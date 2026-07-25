#!/usr/bin/env python3
"""Deterministic exact CNF generator for rooted fixed-order SNC shards."""
import argparse


class CNF:
    def __init__(self): self.names, self.clauses = {}, []
    def var(self, name):
        if name not in self.names: self.names[name] = len(self.names) + 1
        return self.names[name]
    def add(self, *lits): self.clauses.append(tuple(lits))


def equiv_and(c, y, x, z):
    c.add(-y, x); c.add(-y, z); c.add(y, -x, -z)


def threshold(c, inputs, tag):
    """Exact unary outputs out[t-1] iff at least t inputs are true."""
    prev = []
    for i, x in enumerate(inputs, 1):
        cur = []
        for t in range(1, i + 1):
            y = c.var(f"cnt_{tag}_{i}_{t}"); cur.append(y)
            u = prev[t-1] if t <= len(prev) else None
            v = prev[t-2] if t >= 2 else True
            # y <-> u OR (x AND v), with constants simplified.
            if u is not None: c.add(-u, y)
            if v is True: c.add(-x, y)
            else: c.add(-x, -v, y)
            if u is None:
                if v is True: c.add(-y, x)
                else: c.add(-y, x); c.add(-y, v)
            elif v is True:
                c.add(-y, u, x)
            else:
                c.add(-y, u, x); c.add(-y, u, v)
        prev = cur
    return prev


def generate(n, bsize, missing):
    if n < 9 + bsize:
        raise ValueError("n must be at least 9+bsize for the rooted layers")
    if not 0 <= missing <= n * (n - 1) // 2:
        raise ValueError("missing count outside [0,C(n,2)]")
    c = CNF()
    a = [[c.var(f"a_{i}_{j}") for j in range(n)] for i in range(n)]
    q = [[c.var(f"q_{i}_{j}") for j in range(n)] for i in range(n)]
    for i in range(n): c.add(-a[i][i]); c.add(-q[i][i])
    for i in range(n):
        for j in range(i + 1, n): c.add(-a[i][j], -a[j][i])
    for i in range(n):
        for j in range(n):
            if i == j: continue
            paths = []
            for k in range(n):
                if k in (i, j): continue
                p = c.var(f"p_{i}_{k}_{j}"); paths.append(p)
                equiv_and(c, p, a[i][k], a[k][j])
            r = c.var(f"r_{i}_{j}")
            for p in paths: c.add(-p, r)
            c.add(-r, *paths)
            c.add(-q[i][j], r); c.add(-q[i][j], -a[i][j])
            c.add(q[i][j], -r, a[i][j])
    for i in range(n):
        outs = threshold(c, [a[i][j] for j in range(n) if j != i], f"d1_{i}")
        secs = threshold(c, [q[i][j] for j in range(n) if j != i], f"d2_{i}")
        c.add(outs[7])                         # d1 >= 8
        upper = (n + 1) // 2
        if upper < n - 1: c.add(-outs[upper]) # d1 <= upper
        c.add(outs[0])
        for t in range(1, n-1):               # d2>=t => d1>=t+1
            c.add(-secs[t-1], outs[t])
        c.add(-secs[n-2])                     # d2 cannot be n-1
        for t in range(3, n):                 # d1>=t => d2>=t-2
            c.add(-outs[t-1], secs[t-3])
    hs = []
    for i in range(n):
        for j in range(i + 1, n):
            h = c.var(f"h_{i}_{j}"); hs.append(h)
            c.add(-h, -a[i][j]); c.add(-h, -a[j][i]); c.add(h, a[i][j], a[j][i])
    hm = threshold(c, hs, "missing")
    if missing: c.add(hm[missing-1])
    if missing < len(hs): c.add(-hm[missing])
    A, B = set(range(1, 9)), set(range(9, 9+bsize))
    for j in range(n):
        c.add(a[0][j] if j in A else -a[0][j])
        c.add(q[0][j] if j in B else -q[0][j])
    for b in B: c.add(*[a[x][b] for x in sorted(A)])
    for x in A:
        for r in range(9+bsize, n): c.add(-a[x][r])
    return c


def main():
    p=argparse.ArgumentParser(); p.add_argument('--n',type=int,required=True)
    p.add_argument('--b-size',type=int,choices=(6,7),required=True)
    p.add_argument('--missing',type=int,required=True); p.add_argument('--output',required=True)
    x=p.parse_args(); c=generate(x.n,x.b_size,x.missing)
    with open(x.output,'w',encoding='ascii',newline='\n') as f:
        for name,num in c.names.items(): f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for clause in c.clauses: f.write(' '.join(map(str,clause))+' 0\n')
    print(f"vars={len(c.names)} clauses={len(c.clauses)} output={x.output}")


if __name__ == '__main__': main()
