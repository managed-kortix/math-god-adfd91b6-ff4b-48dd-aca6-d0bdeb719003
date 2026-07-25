# Tetracyclic cactus DNN residual frontier: triangles and pentagons

## DNN classification

For a tetracyclic cactus with cycle lengths `l1,...,l4`, the block identity is

`b + sum li = n+3`.

The sharp cactus DNN estimate therefore gives

`s+(G)-n >= 3-sum epsilon_li`,

where `epsilon_3=1`, `epsilon_5=5-2sqrt(5)`, even cycles contribute zero,
and the odd sequence decreases strictly. In the triangle/pentagon sector the
only DNN-residual multisets are

`{3,3,3,3}`, `{3,3,3,5}`, `{3,3,5,5}`.

More generally, the first family is `{3,3,3,q}` for every odd `q`; with only
two triangles, `{3,3,5,5}` is the unique residual because
`2 epsilon_5>1` but `epsilon_5+epsilon_7<1`.

The respective raw DNN slacks are `-1`, `-(5-2sqrt(5))`, and
`-(9-4sqrt(5))`. These are relaxation deficits, not observed graph deficits.

## Search coverage and outcome

The exact-core search enumerated both unlabeled four-node cycle block trees,
all assignments of the three/pentagon multiset, every shared-cut position,
and connector lengths zero or one. Isomorphic graphs were removed by an
isomorphism check after Weisfeiler--Lehman bucketing. Every core vertex was
tested as a massive-star root using the exact limiting identity

`lim_(t->infinity)(s+(G_t)-|G_t|)=deg_H(v)+s+(H-v)-|H|`.

Counts were 27, 99, and 182 nonisomorphic cores for the three multisets. A
separate four-arm scan allowed each arm length through eight. No
counterexample to `s+>=n` was found. All observed limiting slacks are positive.

The reproducible driver is
`positive-square-energy/experiments/tetracyclic_cactus_residual_search.py`.

## Massive-star frontier

### Rank 1: `{3,3,5,5}` with two remote pentagons

Take two triangles through a common vertex `v`. Join `v` by one bridge to each
of two disjoint pentagons, and attach `t` leaves at `v`. Deleting `v` leaves

`2 K2 disjoint-union 2 C5`.

Since the core has order 15, `deg(v)=6`, and `s+(C5)=7-sqrt(5)`,

`lim(s+-n)=6+2+2(7-sqrt(5))-15`
`          =7-2sqrt(5)`
`          =2.5278640450004206...`.

This is the smallest value in the complete connector-0/1 enumeration and the
arm-length-through-eight scan. Extra forest components incident directly at
`v` cancel from the limiting identity, so this is an asymptotic family rather
than a unique graph.

The exact quotient characteristic polynomial factors as

`(x-2)(x-1)(x+1)^2(x^2+x-1)^3 R_t(x)`,

where

`R_t(x)=x^6-2x^5-(t+8)x^4+(2t+13)x^3`
`       +(2t+10)x^2-(5t+10)x+2t`.

### Rank 2: `{3,3,3,5}` with one remote pentagon

Take three triangles through `v`, join `v` by one bridge to a disjoint
pentagon, and put the massive star at `v`. Deletion leaves `3 K2 union C5`, so

`lim(s+-n)=7+3+(7-sqrt(5))-12`
`          =5-sqrt(5)`
`          =2.7639320225002103...`.

For `{3,3,3,q}`, the same construction gives

`4-sec(pi/q)` if `q=1 mod 4`, and `3` if `q=3 mod 4`.

Thus the odd-cycle extension is minimized at `q=5`. The quotient factors as

`(x-1)^2(x+1)^3(x^2+x-1) S_t(x)`,

where

`S_t(x)=x^6-2x^5-(t+9)x^4+(2t+13)x^3`
`       +(2t+16)x^2-(5t+13)x+2t`.

### Rank 3: `{3,3,3,3}` bouquet

Put all four triangles through `v` and attach the massive star there. Deleting
`v` leaves `4 K2`, giving the exact limit `3`. The quotient is

`(x-1)^3(x+1)^4 [x^3-x^2-(t+8)x+t]`.

No connector-0/1 incidence or four-arm configuration through arm length eight
fell below 3 in this multiset.

## Shared-cluster frontier

If every cycle belongs to one shared-cut cluster (all three block-tree joins
have connector length zero), the lowest observed limit is

`2.593873751236949...`

for `{3,3,5,5}`. Its incidence is:

1. a triangle `T0` and a middle triangle `T1` share the star root `v`;
2. the two pentagons meet `T1` at its two other, distinct vertices;
3. the massive star is attached at `v`.

After deleting `v`, one component is `K2`; the other is exactly the bare graph
of two pentagons joined by one bridge edge. If `rho` is the latter graph's
surplus,

`rho=0.593873751236949...`, then the limit is exactly `2+rho`.

Writing the bridge-of-pentagons characteristic polynomial as

`h(x)=(x-1)(x^2-x-3)(x^2+x-1)^2(x^3-4x+1)`,

this description is exact even though `rho` has no short radical expression.
For the 13-vertex shared core itself, the massive-star quotient factors as

`(x-1)(x+1)(x^2+x-1)^2(x^3-4x+1) Q_t(x)`,

where

`Q_t(x)=x^5-2x^4-(t+6)x^3+(2t+7)x^2+(2t+8)x-3t`.

The next shared-cluster values are `2.709599840490714...` for another
`{3,3,5,5}` incidence, `2.854799920245357...` for `{3,3,3,5}`, and `3` for
the four-triangle bouquet.

## Interpretation

- No searched family approaches zero slack; the strongest candidate is
  `7-2sqrt(5)>2.52` above the conjectured threshold.
- The likely tetracyclic triangle/pentagon minimum is the remote-pentagon
  `{3,3,5,5}` family, not a fully shared cluster.
- The likely shared-cluster minimum is the middle-triangle incidence whose two
  non-root vertices carry the pentagons, with limit `2+rho`.
- DNN is qualitatively weakest on four triangles (deficit one), but its actual
  massive-star frontier is larger than the pentagonal frontiers.
- This is reconnaissance, not a sharpness proof. The unexcluded risks are
  longer general block-tree connectors outside the arm scan and genuinely
  multi-root unbounded tree allocations; neither is controlled by a
  concentration theorem here.
