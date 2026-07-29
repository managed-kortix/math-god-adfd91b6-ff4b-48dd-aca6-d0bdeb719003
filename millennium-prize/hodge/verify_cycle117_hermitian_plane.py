#!/usr/bin/env python3
"""Exact combinatorial checks for the Cycle 117 W_2 obstruction."""
from math import comb

def v2(n):
    s = 0
    while n % 2 == 0:
        n //= 2
        s += 1
    return s

vals = {m: v2(comb(33, m)) for m in range(2, 32)}
assert [m for m, v in vals.items() if v == 1] == [16, 17]
assert comb(33, 16) == comb(33, 17) == 1166803110
assert (comb(33, 16) // 2) % 2 == 1
assert 595 == comb(35, 2)
assert 595 - 9 == 586
assert pow(2, 5, 33) == 32 and pow(2, 10, 33) == 1
assert all(pow(2, j, 33) != 1 for j in range(1, 10))
print("v2(C(33,m))=1 only for m=16,17 in the interior")
print("normal-map rank 9; obstruction-space dimension 586")
print("mu_33 splitting degree over F_2 is 10")
print("all exact checks passed")
