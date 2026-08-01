#!/usr/bin/env python3
from fractions import Fraction as Q


p, r, s = Q(1), Q(2), Q(1)
d = p - 2 * r + s
delta = p * s - r * r

a = delta / d
b = d**3 / delta**2
c = delta * (p - r) / d**2

assert (d, delta) == (Q(-2), Q(-3))
assert (a, b, c) == (Q(3, 2), Q(-8, 9), Q(3, 4))


def pi_kernel(z, w):
    return a + b * (c - a * z) * (c - a * w)


node_matrix = [[pi_kernel(z, w) for w in (Q(0), Q(1))]
               for z in (Q(0), Q(1))]
assert node_matrix == [[p, r], [r, s]]

g2 = [[b * c * c, b * c], [b * c, b]]
assert g2 == [[Q(-1, 2), Q(-2, 3)], [Q(-2, 3), Q(-8, 9)]]
assert g2[0][0] + g2[1][1] == Q(-25, 18)
assert g2[0][0] * g2[1][1] - g2[0][1] ** 2 == 0

negative_mass = -b * (1 + c * c)
assert negative_mass == Q(25, 18)

clipped = [[a, a], [a, a]]
clipped_error = max(abs(clipped[j][k] - node_matrix[j][k])
                    for j in range(2) for k in range(2))
assert clipped_error == Q(1, 2)

# The characteristic polynomial of T is lambda^2 - 2 lambda - 3.
assert p + s == 2
assert delta == -3
assert (3**2 - (p + s) * 3 + delta) == 0
assert ((-1)**2 - (p + s) * (-1) + delta) == 0

print("two-cell exact fit: PASS")
print(f"a={a}, b={b}, c={c}, negative_mass={negative_mass}")
print(f"clipped pi-normalized entrywise error={clipped_error}")
