# Rank-seven single-block structural theorem: exact reduction and obstructions

## Scope and target

For a finite graph `X`, put

`kappa(X)=min_R sum_(uv in E(X)) 2/(1-R_uv)`,

where `R` ranges over correlation matrices, and write the DNN excess as

`delta_R(X)=sum_(uv in E(X)) 2/(1-R_uv)-|E(X)|`.

This note develops the structural theorem needed for one 2-connected block of
cyclomatic rank seven. The target is a feasible Gram with excess at most six.
It proves the analytic reduction to a finite canonical-plus-coordinate ledger,
gives exact path and equality atoms, and identifies the precise marked condition
under which a rank-six certificate lifts after an edge is opened. It does not
claim that the resulting finite rank-seven ledger has been enumerated or
certified.

## Lemma 1 (rank-seven suppression)

Let `B` be a finite simple 2-connected graph of cyclomatic rank seven.
Suppressing all degree-two vertices gives a loopless 2-connected multigraph
`K` of minimum degree at least three such that

`|E(K)|=|V(K)|+6`, `2<=|V(K)|<=12`.                            (1)

Conversely, `B` is a simple realization of such a kernel: every physical edge
of `K` is replaced by a positive-length path, replacement paths have disjoint
interiors, and they meet only at their prescribed branch endpoints.

### Proof

Suppression preserves connectedness and `|E|-|V|`. A loop in the suppressed
kernel would come from a cycle meeting the rest of the block at only one branch
vertex, contrary to 2-connectivity. If `n=|V(K)|`, then minimum degree three
and (1) give `3n<=2n+12`, hence `n<=12`. Reversing suppression gives the path
model. Simplicity remains a separate condition, particularly in a parallel
class. `QED`

For order twelve every vertex is cubic. More generally,

`sum_v (deg_K(v)-3)=12-|V(K)|`,                               (2)

so the top kernel orders are controlled by a bounded total degree excess.

## Lemma 2 (exact rank-independent path atom)

Fix unit branch vectors with endpoint correlation `r`. If their kernel edge is
realized by a path of length `q>=1`, the least contribution in excess of its
`q` edges is

`f_q(r)=q tan^2(acos((-1)^q r)/(2q)).`                         (3)

For fixed parity,

`f_(q+2)(r)<=f_q(r)`,                                         (4)

with strict inequality unless the transformed endpoint correlation
`(-1)^q r` is one.

### Proof

Alternately negate vectors along the path. The transformed endpoints are at
angle `beta=acos((-1)^q r)`. The spherical triangle inequality and convexity
of the edge cost make `q` equal angles optimal, proving (3). For real `q>0`,
differentiation of `q tan^2(beta/(2q))`, with `z=beta/(2q)`, has the sign of

`sin(z)cos(z)-2z`,

which is negative for `0<z<pi/2` and zero when `beta=0`. Endpoint cases follow
by one-sided limits. `QED`

Thus every path is an independent energy atom once the common branch Gram has
been fixed. Internal vectors for different paths can be installed in mutually
orthogonal auxiliary spaces.

## Lemma 3 (canonical simple representatives)

In a parallel class of multiplicity `m` with exactly `o` odd paths, define the
canonical simple lengths, up to permutation inside the class, by

```text
o=0: (2,...,2),
o>0: (1,3,...,3,2,...,2),
```

where the second row has `o` odd entries. If `c` is the product of these class
representatives, every simple realization `l` in the same physical parity
orbit can be ordered so that

`c<=l` coordinatewise and `l-c` is entrywise even.             (5)

### Proof

Simplicity allows at most one unit path in a parallel class. The shortest even
length is two; after the possible unique unit path, the shortest odd length is
three. This proves (5). `QED`

## Theorem 4 (canonical-plus-coordinate finite reduction)

Let `K` be a rank-seven kernel with ordered physical edges
`e_1,...,e_p`. For every physical parity orbit let `c` be its canonical simple
vector and put

`F(c)={c} union {c+2e_i:1<=i<=p}.`                            (6)

Assume every orbit has one of the following exact owners.

1. A coarse owner supplies one branch Gram whose exact eliminated path excess
   is at most six at `c` and remains at most six under every same-parity
   coordinate lengthening.
2. A frontier owner supplies an exact feasible Gram-chain certificate of excess
   at most six for every target in `F(c)`.
3. A structural owner proves the same final spectral conclusion for its exact
   target scope and includes an explicit all-length and rooted-tree lift.

Assume also that regenerated target keys are the disjoint union of checked
owner keys. Then every finite simple realization of `K`, with arbitrary finite
rooted trees attached at branch or internal path vertices, satisfies

`s^+(G)>=|V(G)|`.                                              (7)

### Proof

If `l=c`, use its canonical owner. Otherwise (5) gives an `i` such that
`c+2e_i<=l`. Start from that coordinate owner, retain its branch vectors, and
replace all paths that must grow by their equal-angle chains. Lemma 2 shows
that the excess cannot increase. The coarse case starts directly at `c`; the
structural case uses its stated lift. Hence the realized cyclic core, with `L`
edges, has `kappa(B)<=L+6` in every DNN-owned case.

Rank seven gives `|V(B)|=L-6`. If the attached rooted trees have `t` edges,
one-vertex additivity of `kappa` and `kappa(T)=|E(T)|` give

`kappa(G)<=L+6+t`.

Using `s^-(G)<=kappa(G)` and `s^+(G)+s^-(G)=2|E(G)|`,

`s^+(G)>=2(L+t)-(L+6+t)=L-6+t=|V(G)|`.

Different frontier targets may use different Grams. No parity-changing
subdivision or spectral subdivision monotonicity is used. `QED`

The coordinate targets in (6) are essential for residual rows. A canonical
cost-six Gram alone need not control a descendant if the descendant must start
from a different Gram; fixed-parity monotonicity only applies while its branch
Gram is retained.

## Lemma 5 (mixed-pair and simplex atoms)

The following lower bounds are exact.

### Mixed pair

For one odd unit path and one even length-two path on the same branch pair,

`f_1(r)+f_2(r)>=1`,                                           (8)

with equality exactly at `r=-1/2`.

Indeed, with `r=cos(theta)` and `x=tan^2(theta/4)`, the left side is

`1/(4x)-1/2+9x/4>=1`.

### Simplex

Let `R` be the Gram of `k>=3` unit vectors. Then

`sum_(i<j) f_1(R_ij)>=(k-1)(k-2)/2`,                          (9)

with equality exactly at the regular-simplex correlations

`R_ij=-1/(k-1)` for every `i!=j`.                              (10)

### Proof of the simplex bound

The function `f_1(r)=(1+r)/(1-r)` is strictly convex. Its tangent at
`r_0=-1/(k-1)` is exact only at `r_0`. Sum the tangent inequalities and use

`sum_(i<j)R_ij=(1^T R 1-k)/2>=-k/2`.

The resulting constant is `(k-1)(k-2)/2`. Equality forces every strict tangent
to be tight, giving (10); the regular-simplex Gram attains it. `QED`

The first simplex costs are therefore

```text
triangle: 1, tetrahedron: 3, four-simplex (K5 support): 6.
```

## Corollary 6 (proved atomic equality geometries at budget six)

After zero-cost signed contractions, each of the following ledgers has global
minimum six exactly when its forced correlations admit a common PSD completion:

1. six mixed pairs, each forced to correlation `-1/2`;
2. all ten odd unit paths of a `K5`, forced to the regular four-simplex
   correlation `-1/4`;
3. any PSD-completable edge-disjoint or one-sum assembly of mixed-pair and
   simplex atoms whose exact costs from Lemma 5 total six.

Every minimizer forces the listed correlations. This class includes, but is not
limited to, the cost partitions

`6`, `3+3`, `3+1+1+1`, and `1+1+1+1+1+1`.                    (11)

A signed six-cycle quotient of mixed bundles always supplies an example of the
first type: if `S` is its signed adjacency matrix, `I-S/2` is PSD because the
spectrum of every signed cycle lies in `[-2,2]`.

This is an exact list of equality geometries generated by these atoms, not an
exhaustive classification of every possible cost-six Gram. A coupled equality
face not decomposable into mixed-pair and simplex stresses is a genuine
remaining obstruction. Nonuniqueness of unspecified completion entries also
means that equality determines a support geometry, not necessarily one Gram.

By Lemma 2, lengthening any noncontraction path by two strictly lowers the same
Gram's cost. Therefore canonical atomic equality can persist on a coordinate
frontier only when that coordinate is a signed contraction.

## Lemma 7 (rank-six edge-opening lift with one credit)

Let `K` have rank seven and choose a physical edge `e=ab`. Remove `e`; after
retaining all path lengths and suppressing degree-two vertices as desired, the
remaining connected cyclic graph has rank six and may be a block tree. Suppose
it has an exact marked Gram certificate with excess `E_0<=5`, retaining unit
vectors at the marked endpoints `a,b` with correlation `r`.

Reinsert `e` as a path of length `q`. The marked rank-six certificate lifts to
a rank-seven certificate of excess at most six if and only if the displayed
certificate satisfies

`E_0+f_q(r)<=6`.                                               (12)

In particular, an exact-budget rank-six certificate (`E_0=5`) lifts precisely
when

`f_q(r)<=1`.                                                   (13)

For the first two lengths this condition is

```text
q=1: r<=0,
q=2: r>=-7/9.
```

### Proof

Keep the rank-six branch Gram and install the optimal equal-angle chain from
Lemma 2 on the reinserted path, in a fresh auxiliary subspace. Excesses add,
which proves (12). For `q=1`, `f_1(r)=(1+r)/(1-r)<=1` exactly when `r<=0`.
For `q=2`, writing `r=cos(theta)` gives
`2 tan^2(theta/4)<=1`; since
`cos(4 atan(1/sqrt(2)))=-7/9`, this is equivalent to `r>=-7/9`. `QED`

Same-parity lengthening of the opened path preserves (12). Thus the reusable
rank-six object is not an unmarked certificate but a certificate carrying its
endpoint correlation and exact slack `6-E_0`.

## Obstruction 8 (why ordinary rank-six certificates do not automatically lift)

The completed rank-six theorem supplies excess at most five, but that statement
alone records neither a common marked Gram nor the correlation needed in (12).
Consequently it cannot be promoted formally to rank seven by adding an edge.
At equality it has only one unit of path credit, and a unit edge with positive
endpoint correlation has `f_1(r)>1`.

The induced-opening route has an even sharper accounting barrier. Delete an
internal vertex of a subdivided rank-seven path together with its rooted tree.
The retained graph `H` has rank six and

`sigma(G)>=sigma(H)-1`, where `sigma(X)=s^+(X)-|V(X)|`.        (14)

A rank-six DNN certificate of excess `E_0` gives

`sigma(H)>=5-E_0`.                                            (15)

Paying the deleted nonempty tree therefore requires `E_0<=4`, not merely the
known universal budget `E_0<=5`. These are two distinct valid routes:

1. **Gram reinsertion:** use the marked endpoint condition (12), allowing
   `E_0=5` when the new path costs at most one;
2. **induced deletion:** prove one full unit of rank-six spectral credit, for
   example by a certificate with `E_0<=4`.

Mixing the two accountings is invalid. An unquantified strict rank-six result,
an unmarked cost-five certificate, or edge addition without the marked
correlation proves neither route.

## Exact remaining finite problem

To complete the one-block rank-seven theorem it is enough to perform these
finite tasks.

1. Enumerate the loopless 2-connected minimum-degree-three rank-seven kernels
   on orders `2,...,12` and their physical parity orbits.
2. Apply Theorem 4 with exact ownership of every canonical-plus-coordinate key.
3. Remove the atomic cost-six rows of Corollary 6 only after exact support and
   PSD-completion checks; search explicitly for coupled equality faces.
4. Use Lemma 7 only with rank-six records augmented by exact marked endpoint
   correlations and slack. Route every failure of (12) back to a direct
   rank-seven frontier owner or to the stronger induced-deletion condition.

The natural cubic formula below is a useful coarse sieve, but not a uniform
replacement for this finite problem.

## Proposition 9 (cubic signed-imbalance Gram and exact obstruction)

For a cubic order-twelve kernel, let `m_uv` be the physical multiplicity and
`o_uv` the number of odd paths in that bundle. Define

`G_uu=1`, `G_uv=(m_uv-2o_uv)/3` on the support, and `G_uv=0` otherwise. (16)

Then `G` is PSD. Indeed,

`sum_(v!=u)|m_uv-2o_uv|<=sum_(v!=u)m_uv=3`,

so `G` is symmetric diagonally dominant with nonnegative diagonal. For a path
of length `L`, with transformed correlation `t=(-1)^L G_uv`, the exact rational
upper atom

`f_L(G_uv)<= (1-t)/(L(1+t))`                                  (17)

is fixed-parity monotone. Hence (16)--(17) give a linear-time exact coarse
certificate whenever their sum is at most six.

This formula is not uniform. On any simple cubic order-twelve kernel with every
physical path odd of length one, (16) is `G=I-A/3`; every one of the eighteen
edges has correlation `-1/3` and excess `f_1(-1/3)=1/2`. Its total excess is
exactly nine, which is greater than six. Thus diagonal dominance is correct,
but the local signed imbalance `m-2o` alone cannot prove the desired theorem.
A successful uniform cubic Gram, if one exists, must use nonlocal cycle or
cut information, or select among several Gram geometries.
