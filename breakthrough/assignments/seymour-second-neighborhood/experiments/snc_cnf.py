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


def add_mu2_link(c, outs, secs, z):
    """Link z exactly to deficit two, assuming positive deficit at most two."""
    n = len(outs) + 1
    for t in range(2, n):
        c.add(z, -outs[t-1], secs[t-2])
    c.add(-z, outs[1])  # intrinsic exactness: deficit two needs d1>=2
    for t in range(1, n-2):
        c.add(-z, -secs[t-1], outs[t+1])
    c.add(-z, -secs[n-3]); c.add(-z, -secs[n-2])


def add_witness_for_deleted(c, n, u, a, q, pvar, mu2):
    witnesses=[]
    for w in range(n):
        if w == u: continue
        z=c.var(f"wit_{w}_{u}"); witnesses.append(z)
        c.add(-z, a[w][u]); c.add(-z, -mu2[w])
        for b in range(n):
            if b in (w,u): continue
            alternatives=[pvar[w,k,b] for k in range(n)
                          if k not in (w,u,b)]
            c.add(-z, -q[w][b], *alternatives)
    c.add(*witnesses)


def add_arc_minimality(c, n, i, j, a, q, pvar, mu2):
    """Exact necessary condition that deleting present arc i->j repairs i."""
    arc=a[i][j]
    gain=tuple(pvar[i,k,j] for k in range(n) if k not in (i,j))
    c.add(-arc,-mu2[i],*gain)
    no_loss={}
    for t in range(n):
        if t in (i,j): continue
        alternatives=tuple(pvar[i,k,t] for k in range(n) if k not in (i,j,t))
        block=(-q[i][t],-a[j][t],*alternatives)
        no_loss[t]=block
        c.add(-arc,*block,-mu2[i])
        c.add(-arc,*block,*gain)
    endpoints=tuple(no_loss)
    for x in range(len(endpoints)):
        for y in range(x+1,len(endpoints)):
            c.add(-arc,*no_loss[endpoints[x]],*no_loss[endpoints[y]])


def generate(n, bsize, missing, robust_witness=False, high_vertices=None,
             forced_witness=None, arc_minimal=False):
    if bsize not in (6, 7):
        raise ValueError("bsize must be 6 or 7")
    if n < 9 + bsize:
        raise ValueError("n must be at least 9+bsize for the rooted layers")
    if not 0 <= missing <= n * (n - 1) // 2:
        raise ValueError("missing count outside [0,C(n,2)]")
    high_vertices=None if high_vertices is None else set(high_vertices)
    if high_vertices is not None and any(v < 0 or v >= n for v in high_vertices):
        raise ValueError("high vertex outside range")
    if forced_witness is not None:
        w,u=forced_witness
        if not robust_witness or w==u or min(w,u)<0 or max(w,u)>=n:
            raise ValueError("invalid forced witness")
    c = CNF()
    a = [[c.var(f"a_{i}_{j}") for j in range(n)] for i in range(n)]
    q = [[c.var(f"q_{i}_{j}") for j in range(n)] for i in range(n)]
    pvar = {}
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
                pvar[i,k,j] = p
                equiv_and(c, p, a[i][k], a[k][j])
            r = c.var(f"r_{i}_{j}")
            for p in paths: c.add(-p, r)
            c.add(-r, *paths)
            c.add(-q[i][j], r); c.add(-q[i][j], -a[i][j])
            c.add(q[i][j], -r, a[i][j])
    out_thresholds, sec_thresholds, mu2 = [], [], []
    for i in range(n):
        outs = threshold(c, [a[i][j] for j in range(n) if j != i], f"d1_{i}")
        secs = threshold(c, [q[i][j] for j in range(n) if j != i], f"d2_{i}")
        out_thresholds.append(outs); sec_thresholds.append(secs)
        c.add(outs[7])                         # d1 >= 8
        upper = (n + 1) // 2
        if upper < n - 1: c.add(-outs[upper]) # d1 <= upper
        c.add(outs[0])
        for t in range(1, n-1):               # d2>=t => d1>=t+1
            c.add(-secs[t-1], outs[t])
        c.add(-secs[n-2])                     # d2 cannot be n-1
        for t in range(3, n):                 # d1>=t => d2>=t-2
            c.add(-outs[t-1], secs[t-3])
        z = c.var(f"mu2_{i}"); mu2.append(z)
        # z=false forces deficit one; z=true forces deficit at least two.
        # Together with the base deficit-in-{1,2} clauses, z is exact.
        add_mu2_link(c, outs, secs, z)
        # In order-18 normal-form shards all degrees are exactly eight or nine.
        if high_vertices is not None:
            c.add(outs[8] if i in high_vertices else -outs[8])
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
    if robust_witness:
        # For every deleted vertex u select a tight in-neighbor w such that no
        # old exact second neighbor of w loses all two-walks when u is removed.
        for u in range(n):
            add_witness_for_deleted(c,n,u,a,q,pvar,mu2)
        if forced_witness is not None:
            c.add(c.var(f"wit_{forced_witness[0]}_{forced_witness[1]}"))
    if arc_minimal:
        for i in range(n):
            for j in range(n):
                if i != j: add_arc_minimality(c,n,i,j,a,q,pvar,mu2)
    return c


def main():
    p=argparse.ArgumentParser(); p.add_argument('--n',type=int,required=True)
    p.add_argument('--b-size',type=int,choices=(6,7),required=True)
    p.add_argument('--missing',type=int,required=True); p.add_argument('--output',required=True)
    p.add_argument('--robust-witness',action='store_true')
    p.add_argument('--high',help='comma-separated exact degree-nine vertices; empty string means none')
    p.add_argument('--force-witness',help='w,u selector to force')
    p.add_argument('--arc-minimal',action='store_true')
    x=p.parse_args()
    high=None if x.high is None else tuple(int(v) for v in x.high.split(',') if v!='')
    fw=tuple(map(int,x.force_witness.split(','))) if x.force_witness else None
    c=generate(x.n,x.b_size,x.missing,x.robust_witness,high,fw,x.arc_minimal)
    with open(x.output,'w',encoding='ascii',newline='\n') as f:
        for name,num in c.names.items(): f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for clause in c.clauses: f.write(' '.join(map(str,clause))+' 0\n')
    print(f"vars={len(c.names)} clauses={len(c.clauses)} output={x.output}")


if __name__ == '__main__': main()
