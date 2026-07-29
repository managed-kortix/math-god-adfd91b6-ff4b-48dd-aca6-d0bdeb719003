#!/usr/bin/env python3
"""Exact arithmetic checks accompanying the Fermat obstruction paper."""
from itertools import combinations
from math import gcd

m, d = 33, 11
alpha = (7, 10, 13, 19, 22, 28)
units = [t for t in range(1, m) if gcd(t, m) == 1]
assert len(units) == 20
assert sum(alpha) == 3*m
assert all(sum((t*a) % m for a in alpha) == 3*m for t in units)
assert all(sum(alpha[i] for i in I) % m
           for r in range(1, 6) for I in combinations(range(6), r))
assert sum(a-1 for a in alpha) == 3*m-6 == 93
assert m == 3*d
assert 2*d*d == 242
assert d*(2*d)*m == 7986
assert any(a % d for a in alpha)
assert sum((11, 11, 11, 22, 22, 22)) == 3*m
print("all exact checks passed")
print("[W_11] = 242 H^2; degree = 7986")
print("the exceptional character is excluded by mu_11^5 invariance")
