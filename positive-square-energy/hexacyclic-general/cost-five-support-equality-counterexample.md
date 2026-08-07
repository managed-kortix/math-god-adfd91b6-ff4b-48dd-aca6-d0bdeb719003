# A third cost-five support equality ledger

## Verdict

The proposed orders-eight-through-ten exclusion is false at support level. A
canonical rank-six residual can have true correlation optimum five without
being five mixed-pair atoms or a tetrahedral simplex plus two mixed atoms.

The smallest explicit counterexample is order-eight residual source `78755` on
`K883`. Its sparse row, in the support order

```text
04,06,14,15,17,23,25,27,35,37,46,67
```

is

```text
0,1,1,1,0,1,1,1,1,1,1,1.
```

Thus `04` and `17` are even singleton contractions, `06` is a mixed doubled
bundle, and the remaining nine supports are odd singletons. Contracting `04`
and `17` gives the quotient map

```text
0,1,2,3,0,4,5,1.
```

On this quotient the positive ledger is

```text
triangle:    14,46,67
tetrahedron: 15,23,25,27,35,37
mixed pair:  06.
```

The triangle and tetrahedron share only quotient vertex `1`. The mixed pair
`06` lies on the same quotient pair as triangle edge `46`. Therefore the row
has the distinct atomic decomposition

```text
K3 simplex + K4 simplex + one mixed pair,
```

with lower-bound ledger `1+3+1=5`.

## Exact lower bound

Write `f(r)=(1+r)/(1-r)` for an odd unit path. Besides the mixed-pair and
tetrahedral inequalities already proved in `cost-five-equality-face-lemma.md`,
the triangle inequality is

`sum_(ij in K3) f(R_ij) >= 1`,

with equality exactly at the equilateral correlations `R_ij=-1/2`. Indeed,
strict convexity and the tangent at `-1/2` give

`f(r) >= 7/9+(8/9)r`.

For a three-by-three correlation matrix,

`sum_(i<j) R_ij >= -3/2`

because `1^T R 1>=0`. Summing the tangents gives the bound one, and equality
forces all three correlations to be `-1/2`.

Apply this triangle dual, the tetrahedral dual

`sum_(ij in K4) f(R_ij) >= 3`,

and the scalar mixed-pair dual

`f_1(r)+f_2(r)>=1`.

The two contracted paths are nonnegative and the three displayed positive
packets are disjoint as physical paths, even though the triangle and mixed
packet use the same quotient pair. Hence every Gram has objective at least
`1+3+1=5`.

## Exact attainment

Put correlation `-1/2` on the triangle, correlation `-1/3` on the tetrahedron,
and glue their regular-simplex Grams at their common unit vector. One explicit
gluing makes every cross-block correlation the product of its two correlations
with the common vector. This is positive semidefinite: realize the components
orthogonal to the common vector in mutually orthogonal subspaces. Pull the Gram
back through the two contractions.

The mixed bundle `06` has endpoint correlation `-1/2`, so its odd and even
paths cost `1/3+2/3=1`. The triangle costs `3(1/3)=1`, the tetrahedron costs
`6(1/2)=3`, and the contractions cost zero. Thus the feasible value is five;
combined with the dual lower bound, the true optimum is exactly five.

This is a new equality support geometry, not merely another completion of one
of the two previously known geometries: it has one mixed pair and nine odd
simplex edges, versus five mixed pairs or two mixed pairs and six odd `K4`
edges.

## Exhaustive support certificate

`positive-square-energy/experiments/rank6_orders8_10_atom_ledger_search.py`
regenerates all tetrahedral-residual support orbits from the locked rank-six
fixture, using no numerical Gram census. It exhaustively searches signed
singleton contractions and partitions the remaining odd support into complete
`K3`/`K4` simplex atoms and mixed-pair atoms of total dual cost five. For each
new row it constructs the rational glued quotient Gram, checks every principal
minor exactly, and audits the physical path ledger and exact cost.

The search finds eight residual orbits with the new `K3+K4+mixed` ledger:

```text
order 8:  source 78755 K883; source 97350 K942
order 9:  source 93749 K1060; sources 169635,169965 K1119;
          source 173903 K1123
order 10: source 105465 K1188; source 124181 K1197
```

Run:

```sh
python3 positive-square-energy/experiments/rank6_orders8_10_atom_ledger_search.py
python3 -O positive-square-energy/experiments/rank6_orders8_10_atom_ledger_search.py
```

The finite search is not needed to establish the explicit `K883` counterexample;
it certifies that the same omitted support geometry recurs at all three orders.
Accordingly the desired structural theorem must be enlarged by at least the
triangle-plus-tetrahedron-plus-mixed equality family.
