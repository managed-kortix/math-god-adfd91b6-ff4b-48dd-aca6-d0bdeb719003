#!/usr/bin/env python3
"""Exhaustively compare set and independently coded Boolean-matrix semantics."""
import argparse
import itertools
from verify_set import neighborhoods


def matrix_oracle(n, arcs):
    a = [[False] * n for _ in range(n)]
    for u, v in arcs:
        a[u][v] = True
    n1, n2 = [], []
    for v in range(n):
        one, two = set(), set()
        for z in range(n):
            r2 = any(a[v][y] and a[y][z] for y in range(n))
            if a[v][z]: one.add(z)
            if z != v and not a[v][z] and r2: two.add(z)
        n1.append(one); n2.append(two)
    return n1, n2


def graphs(n):
    pairs = list(itertools.combinations(range(n), 2))
    for state in itertools.product(range(3), repeat=len(pairs)):
        yield [(u, v) if s == 1 else (v, u)
               for s, (u, v) in zip(state, pairs) if s]


def main(limit):
    total = 0
    for n in range(1, limit + 1):
        count = passing = 0
        for arcs in graphs(n):
            x = neighborhoods(n, arcs)
            y = matrix_oracle(n, arcs)
            assert x == y, (n, arcs, x, y)
            passing += all(len(x[1][v]) < len(x[0][v]) for v in range(n))
            count += 1
        print(f"n={n} graphs={count} counterexamples={passing}")
        total += count
    print(f"PASS total={total}")


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--max-n', type=int, default=5)
    main(p.parse_args().max_n)
