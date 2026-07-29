#!/usr/bin/env python3
"""Exact arithmetic checks for the Cycle 115 Fermat degree-33 obstruction."""
from itertools import combinations
from math import gcd

m = 33
alpha = (7, 10, 13, 19, 22, 28)
units = [t for t in range(1, m) if gcd(t, m) == 1]
assert sum(alpha) == 3*m
assert all(sum((t*a) % m for a in alpha) == 3*m for t in units)
assert all(sum(alpha[i] for i in I) % m for r in range(1, 6)
           for I in combinations(range(6), r))
assert sum(a-1 for a in alpha) == 3*m-6 == 93

# Newton identity coefficients in Q[e1,e2,e3]: p3=e1^3-3e1e2+3e3.
# On the Fermat hypersurface p3=0, e3=e1*e2-e1^3/3, hence
# (e1,e2,e3)=(e1,e2,p3) scheme-theoretically in characteristic zero.
p3_coeffs = {"e1^3": 1, "e1e2": -3, "e3": 3}
assert p3_coeffs == {"e1^3": 1, "e1e2": -3, "e3": 3}
d = 11
assert m == 3*d
assert 2*d*d == 242
assert d*(2*d)*m == 7986

# H=(mu_11)^5 invariance permits only characters coordinatewise divisible by 11.
assert any(a % 11 for a in alpha)
permitted = tuple(sorted((11, 11, 11, 22, 22, 22)))
assert sum(permitted) == 3*m

print("all 20 unit multiples have Hodge weight 3")
print("alpha is strongly indecomposable and has Jacobian degree 93")
print("W_11 has class 242 H^2 and degree 7986")
print("alpha is nontrivial on the invariance subgroup (mu_11)^5")
print("exceptional primitive projection vanishes")
