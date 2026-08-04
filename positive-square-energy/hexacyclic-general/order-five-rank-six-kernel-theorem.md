# Complete order-five rank-six kernel theorem

## Theorem

Let `K` be any of the 84 order-five kernels in the exact rank-six suppressed
kernel classification. Let `B` be any simple subdivision of `K`, and obtain
`G` by attaching an arbitrary finite rooted tree at every vertex of `B`. Then

`s^+(G) >= |V(G)|`.

The proof is disjunctive: 1120 finite-frontier targets have exact rational DNN
certificates of excess at most five, two have exact symbolic equality
certificates, and the all-odd `K5` family has an attachment-uniform structural
proof. No DNN excess-five claim is made for that last family.

## Exact frontier

The digest-locked census contains 84 kernels, 33,151 physical parity rows and
25,168 genuine automorphism orbits. The regular-tetrahedron sieve certifies
25,065 orbits and leaves 103. Every kernel has ten suppressed paths. Taking the
canonical shortest vector and all ten one-coordinate length-plus-two vectors
gives exactly

`103 * 11 = 1133`

targets. Their disjoint closure ledger is

| method | targets |
|:---|---:|
| strict/exact rational Gram cost at most five | 1120 |
| K61 symbolic equality | 1 |
| K98 symbolic equality | 1 |
| all-odd K110 structural targets | 11 |
| total | 1133 |

Fixed-parity path monotonicity closes coordinatewise descendants of every DNN
target. The K110 descendants require the separate complete argument below.

More explicitly, the two equality templates are needed only at the canonical
length vectors. Every noncanonical subdivision in either K61 or K98 has some
physical path longer than canonical by at least two. Choose such a path `j`.
The one-coordinate `j` frontier is one of the 1120 exact rational DNN targets,
and the given length vector is its coordinatewise same-parity descendant.
Thus monotonicity closes it, including simultaneous lengthening of any number
of other paths. There is no unsupported inference that a canonical equality
template itself remains valid after lengthening.

## Exact equality Grams

Rows and columns are branch vertices `0,1,2,3,4`. For K61 use

```text
[ 1    0    0  -1/2 -1/2 ]
[ 0    1  -1/2   0   -1/2 ]
[ 0  -1/2   1  -1/2   0   ]
[-1/2  0  -1/2   1    0   ]
[-1/2 -1/2  0    0    1   ]
```

Its five doubled bundles are `03,04,12,14,23`; each contains one odd unit path
and one even length-two path. Endpoint correlation `-1/2` becomes `1/2` on the
odd path and costs `1/3`. On the even path an exact midpoint has correlation
`1/2` with both endpoints and costs `2/3`. Every bundle therefore costs one,
so the total is exactly five.

For K98 use

```text
[ 1   -1/3  3/5  -1/3 -1/3 ]
[-1/3  1    2/5  -1/3 -1/3 ]
[ 3/5  2/5   1   -1/2 -1/2 ]
[-1/3 -1/3 -1/2   1   -1/3 ]
[-1/3 -1/3 -1/2 -1/3   1   ]
```

The six unit paths on the actual `K4` induced by `{0,1,3,4}` each cost `1/2`,
for a subtotal of three. Each doubled bundle `23,24` has an odd unit path of
cost `1/3` and an even length-two path of cost `2/3`. The total is again five.
The verifier checks symmetry, unit diagonal and every principal minor of both
rational matrices, as well as each path realization and the exact totals.

## All-odd K5

K110 is the simple `K5`, and its residual row makes all ten paths odd.

The all-unit DNN obstruction is exact, not numerical. If `r_ij` are the ten
off-diagonal correlations of five unit vectors, positivity gives

`0 <= ||u_0+...+u_4||^2 = 5 + 2 sum r_ij`,

so their average is at least `-1/4`. The odd unit-path cost
`f(r)=(1+r)/(1-r)` is increasing and convex. Jensen's inequality yields

`sum f(r_ij) >= 10 f(-1/4) = 6`.

The regular four-simplex Gram, with every off-diagonal entry `-1/4`, attains
six. Thus a universal excess-five DNN theorem misses this graph by exactly one,
and a structural conclusion is necessary.

- If all paths are unit, the core is an actual `K5`. Choose a branch vertex
  and its complete rooted tree as one induced tree. The complement is an actual
  attached `K4`. Its surplus is strictly greater than two, so induced
  superadditivity gives total surplus strictly greater than one.
- If exactly one path is long, put all its internal vertices and every tree
  rooted there in one induced nonempty tree, of surplus `-1`. The complement is
  an actual attached `K5-e`. For the latter, put either endpoint of the missing
  edge and its rooted tree in an induced tree; its complement is an actual
  attached `K4`. Hence the `K5-e` surplus is strictly greater than one, and it
  pays the first deleted tree strictly.
- If at least two paths are long, choose two. Under `Aut(K5)=S5`, two edges are
  either incident or disjoint. The verifier contains one exact rational
  dimension-five Gram certificate of cost strictly below five for each orbit
  at the vector where precisely those two paths have length three. The actual
  subdivision is a coordinatewise same-parity descendant: the chosen paths
  have odd length at least three, and every other path has odd length at least
  one. Fixed-parity monotonicity therefore covers arbitrary further
  lengthening, whether or not additional paths are long.

These cases are exhaustive and are uniform in the rooted trees: every tree is
assigned with its unique root, every opening uses all internal-path owners, and
the induced pieces are disjoint and exhaustive. This also explains why the
eleven canonical/one-coordinate K110 residual targets need not, and should not,
be relabeled as DNN certificates. The numerical one-long value near
`5.00582080171` is recorded only as motivation, not used as an obstruction
theorem or as proof input.

## Exact audit

Run both modes (the normal invocation also compares its output with `-O`):

```text
python3 research/rank-six-order-five-kernel-theorem-verifier.py
python3 -O research/rank-six-order-five-kernel-theorem-verifier.py
```

The verifier digest-locks the census and raw rational results, reconstructs the
full 1133-key Cartesian frontier, verifies all 1120 rational witnesses with
`Fraction`, checks every entry and principal minor of the two equality Grams
with `Fraction`, checks their path costs, checks the exact 13-key
residual set, audits the K110 openings, and verifies both strict two-long orbit
certificates. Thus the former experimental frontier is now a complete exact
order-five theorem; no main/master theorem file is changed.
