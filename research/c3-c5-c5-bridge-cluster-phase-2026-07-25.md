# Weighted phase reconnaissance for `{3,5,5}` bridge clusters

## Structural reduction

Suppress every maximal bridge path in the minimal connected subcactus containing
the three cyclic blocks. If all cycles are vertex-disjoint, the resulting tree
on the cycle terminals is either:

1. a path, with the triangle at a leaf or at the internal terminal; or
2. a `Y`, necessarily with all cycles at leaves (the triangle is a leaf).

At a path terminal incident twice with the connector tree, the two incidences
may use the same cycle vertex or distinct vertices. For `C3` the distinct case
has one separation class; for `C5` it has cyclic distances one and two.

If exactly one pair of cycles shares a cut vertex, suppressing bridges leaves a
shared pair plus a singleton joined by one bridge path. The shared pair is
`C3-C5` or `C5-C5`. For `C3-C5`, the singleton path may attach at the common
cut, elsewhere on the triangle, or at pentagon distance one or two from the
cut. For `C5-C5`, exchange of the two pentagons leaves attachment distances
zero, one, and two on one member. These are all one-shared-pair incidences.
Configurations with two shared adjacencies or a three-cycle bouquet are the
four no-bridge shared-cluster cores covered by the separate exact certificate.

## Sachs polynomials and candidate comparisons

After off-core tree elimination, give every retained vertex an independent
positive activity and write

`D_J=Z_(H-V(J))`, with `D_J=0` when the cycles in `J` meet.

For `T=C3` and `P,Q=C5`, normalized Sachs expansion gives

`R=Z_H+4D_TP+4D_TQ-4D_PQ`,

`I=2(D_P+D_Q-D_T)+8D_TPQ`.

The triple term occurs only for three vertex-disjoint cycles. Let `p,q` be the
isolated weighted pentagon matching partitions. The phase comparison with the
two isolated pentagons has cross product

`Phi=Im((p+2i)(q+2i) conjugate(R+iI))`

`   =2R(p+q)-I(pq-4)`.                                      (1)

Positivity of (1) says that the core phase is below the sum of the two weighted
pentagon phases. This is the useful direction: those two phase integrals have
the established pentagonal upper bounds, and bare `C5+C5` is enough only after
one separately invokes activity monotonicity on each isolated lobe.

For the isolated triangle partition `r`, the two obvious alternatives are

`Phi_times=[2r(p+q)-2(pq-4)]R`
`          -[r(pq-4)+4(p+q)]I`,                             (2)

corresponding to multiplication by `r-2i`, and

`Phi_divide=r Phi+2[2(p+q)I+(pq-4)R]`,                     (3)

which is the denominator-cleared comparison after division by `r-2i`.
Neither (2) nor (3) is coefficientwise nonnegative in the tested bridge cores.
Thus adjoining or cancelling the triangle factor does not repair failures of
(1).

## Exact coefficient results for short bridge paths

The script uses independent activities, exact integer arithmetic, and explicit
matching recursion. A connector length is its number of bridge edges. For all
path arm lengths in `{1,2}`, all `Y` arm triples in `{1,2}^3`, and all
shared-pair bridge lengths in `{1,2}`, coefficient positivity of (1) is as
follows.

### Path, all cycles disjoint

- Triangle internal: all tested cases are positive, with minimum coefficient
  `2`.
- Triangle leaf, middle pentagon: all are positive except the asymmetric
  incidences `(left,right)=(2,1)` with distinct middle attachment points.
  Distance one has six negative coefficients; distance two has three. The
  same abstract warning applies after reflection: the exceptional orientation
  is the one where the length-two arm ends at the triangle and the length-one
  arm ends at the other pentagon.
- Same-vertex middle attachment (`distance 0`) is positive throughout the
  length-two scan.

At lengths `(3,3)`, both a triangle-internal path and a pentagon-internal path
already fail, each with minimum coefficient `-8`. Hence positivity is not a
length-independent path theorem.

### `Y`, all cycles disjoint

- Positive for `(1,1,1)`, `(1,1,2)`, `(1,2,1)`, `(2,1,1)`, `(2,1,2)`, and
  `(2,2,1)`, where the first coordinate is the triangle arm.
- Negative for `(1,2,2)` and `(2,2,2)`: each has 25 negative coefficients and
  minimum `-8`.
- The failure is not only a two-arm threshold: `(1,1,3)` also fails, with 15
  negative coefficients and minimum `-4`.

### One shared pair plus singleton bridge

- Shared `C3-C5`, singleton path attached at the common cut or away from it on
  the triangle: positive for bridge lengths one and two.
- Shared `C3-C5`, path attached on the pentagon at distance one or two: negative
  at bridge length one (six or three negative coefficients), positive at length
  two, and negative again at length three. Thus parity alone does not explain
  the sign.
- Shared `C5-C5`, singleton triangle path: positive at every attachment distance
  for bridge lengths one and two, but the distance-one length-three example
  fails with eight negative coefficients and minimum `-8`.

All positive cases above have minimum nonzero coefficient `2`.

## Minimal counterexample monomials

Vertex labels are generated explicitly by the script. In the first failing
shared `C3-C5` core, with pentagon attachment distance one and one bridge edge,
the minimum-total-degree negative monomial is

`-2 a6 a10 a11`.

Here `a6` is the shared pentagon vertex opposite the listed cut direction,
`a10` is the last non-root vertex of the singleton pentagon, and `a11` is its
bridge endpoint/root. At attachment distance two the corresponding first
witness is

`-2 a3 a10 a11`.

For the first failing `Y`, arms `(1,2,2)`, a still smaller witness appears:

`-8 a0`,

where `a0` is the `Y` junction activity. For `(2,2,2)` it becomes `-8 a0 a1`,
using the first triangle-arm vertex. These low-degree terms show that the
coefficient obstruction belongs to the connector tree, not to a high-degree
cycle product.

## Triangle-factor verdict

For representative positive and negative incidences, (2) has many negative
coefficients (already 8208 in the shortest same-root path example), and (3)
also fails in most incidences. In the shortest triangle-middle paths, (3) is
positive, but by length two it fails. Direct comparisons formed by multiplying
the core rather than the comparator by `r-2i` also have thousands of negative
coefficients. There is therefore no coefficientwise rescue among the simple
choices

`(p+2i)(q+2i)`,

`(p+2i)(q+2i)(r-2i)`,

or `(p+2i)(q+2i)/(r-2i)`.

The exact residual formulas (1)--(3) remain useful for a more structured
matching involution or a connector-continuant factorization, but raw activity
coefficient positivity cannot provide the desired all-length phase bound.

## Reproduction and limitation

Run, for example,

```text
python positive-square-energy/experiments/c3_c5_c5_bridge_cluster_phase.py --max-length 2 --comparisons two_C5
```

The script is
`positive-square-energy/experiments/c3_c5_c5_bridge_cluster_phase.py`.
This is a symbolic reconnaissance result, not a proof or disproof of the
pointwise inequalities on the restricted activity locus produced by actual
tree compression. A negative coefficient disproves only the strongest
coefficientwise certificate over independent activities; the polynomial may
still be positive on that locus or even on the whole positive orthant.
