#!/usr/bin/env python3

c = (
    317131927490234375,
    -2073948378906250,
    12564289203125,
    -56707735500,
    27598945,
    3626326,
    -68381,
)

graph_degrees = tuple((1 + 5**k) ** 2 * (1 + 3 * 5**k) for k in range(7))
d_plus = sum(max(x, 0) * d for x, d in zip(c, graph_degrees))
d_minus = sum(max(-x, 0) * d for x, d in zip(c, graph_degrees))
a_plus = sum(max(x, 0) for x in c)
a_minus = sum(max(-x, 0) for x in c)

assert graph_degrees == (
    16,
    576,
    51376,
    5969376,
    735159376,
    91621109376,
    11445800859376,
)
assert d_plus == 6072151396206990896
assert d_minus == 2315779370123038256
assert a_plus == 317144491810662771
assert a_minus == 2074005086710131
assert a_plus - a_minus == 315070486723952640

m = 15626
m3 = m**3
p3_coefficient = (a_plus - a_minus) * m3
degree_y_plus = 360 * m3 * a_plus - d_minus
degree_y_minus = 360 * m3 * a_plus - d_plus

assert m3 == 3815429734376
assert p3_coefficient == 1202129303470887655672003952640
assert degree_y_plus == 435615308693266367131405038684304
assert degree_y_minus == 435615308693262610759378954731664
assert degree_y_plus - degree_y_minus == d_plus - d_minus
assert all(360 * m3 > d for d in graph_degrees)

print("graph degrees:", graph_degrees)
print("A_plus, A_minus:", a_plus, a_minus)
print("d_plus, d_minus:", d_plus, d_minus)
print("m, m^3:", m, m3)
print("P^3 coefficient:", p3_coefficient)
print("residual degrees:", tuple(360 * m3 - d for d in graph_degrees))
print("Y_plus degree:", degree_y_plus)
print("Y_minus degree:", degree_y_minus)
print("PEL tangent potential dimensions: (3, 0, 0, 0, 0, 0, 0)")
print("all Cycle 202 arithmetic checks passed")
