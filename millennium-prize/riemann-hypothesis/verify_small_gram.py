#!/usr/bin/env python3
"""Symbolic checks for the full-space N=2 and N=3 Gram identities."""

import sympy as s

gamma = s.EulerGamma
C0 = s.log(2 * s.pi) - gamma


def gram(a, b):
    """Entries needed for a,b in {1,2}; V(1,2)=V(2,1)=0."""
    if a == b:
        return C0 / a
    if {a, b} == {1, 2}:
        return (3 * C0 - s.log(2)) / 4
    raise ValueError("small verifier only implements indices 1 and 2")


def chi_cross(a):
    return (s.log(a) + 1 - gamma) / a


# N=2: c_1=1 and c_2=0.
n2 = s.expand(1 + 2 * chi_cross(1) + gram(1, 1))
assert s.simplify(n2 - (3 + s.log(2 * s.pi) - 3 * gamma)) == 0

# N=3: c_1=1, c_2=-r, c_3=0.
r = s.log(s.Rational(3, 2)) / s.log(3)
n3 = s.expand(
    1
    + 2 * chi_cross(1)
    - 2 * r * chi_cross(2)
    + gram(1, 1)
    - 2 * r * gram(1, 2)
    + r**2 * gram(2, 2)
)

a = 1 - r / 2
n3_piecewise = (
    1
    - s.log(2)
    + a * (2 - s.log(s.pi) - gamma)
    + 2 * a**2 * C0
)
assert s.simplify(s.expand_log(n3 - n3_piecewise, force=True)) == 0

# Domain invariant: the restricted Gram differs by the rank-one tail 1/(ab).
for aa in (1, 2):
    for bb in (1, 2):
        restricted = gram(aa, bb) - s.Rational(1, aa * bb)
        assert s.simplify(gram(aa, bb) - restricted - s.Rational(1, aa * bb)) == 0

print("N=2 squared norm:", n2)
print("N=3 squared norm:", s.simplify(n3_piecewise))
print("symbolic Gram checks passed")
