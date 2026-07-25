# Exact certificate for four shared-cut `{3,5,5}` cores

## Scope and outcome

This note records the exact symbolic computation requested in task
`ses_0657bb7adffeU0Uo6IV4NY3KKL`. It concerns the four cactus cores in which
three cycle blocks of lengths `3,5,5` form a connected cluster using shared cut
vertices and no bridge blocks:

1. all three cycles share one cut vertex (the bouquet);
2. the triangle is the middle block and the pentagons meet it at distinct
   triangle vertices;
3. a pentagon is the middle block and its two cut vertices have cyclic distance
   one;
4. a pentagon is the middle block and its two cut vertices have cyclic distance
   two.

For every core, the polynomial

`Phi=2R(p+q)-I(pq-4)`

has strictly positive integer coefficients in independent positive vertex
activities. The reported term counts `2547,2192,2925,2895` are all correct,
and every minimum coefficient is `2`.

This is an exact algebraic certificate for the displayed polynomial inequality.
It is not, by itself, a theorem for arbitrary tree attachments: an additional
argument is required to connect the activities produced by tree compression to
the isolated-pentagon comparison represented by `p,q`.

## Explicit labeled cores

A cycle tuple lists vertices in cyclic order; its closing edge joins the last
entry to the first. All four graphs have vertex set `{0,...,10}` and exactly
the 13 edges supplied by the three listed cycles.

### Bouquet

`T=(0,1,2)`

`P=(0,3,4,5,6)`

`Q=(0,7,8,9,10)`

Thus `T intersect P=T intersect Q=P intersect Q={0}`.

### Triangle middle, distinct triangle vertices

`T=(0,1,2)`

`P=(0,3,4,5,6)`

`Q=(1,7,8,9,10)`

Here `T intersect P={0}`, `T intersect Q={1}`, and `P intersect Q` is empty.
The two cut vertices `0,1` are distinct vertices of the triangle.

### Pentagon middle, cut distance one

`T=(0,5,6)`

`P=(0,1,2,3,4)`

`Q=(1,7,8,9,10)`

The middle pentagon is `P`; the outer cycles meet it at `0` and `1`, which are
adjacent on `P`.

### Pentagon middle, cut distance two

`T=(0,5,6)`

`P=(0,1,2,3,4)`

`Q=(2,7,8,9,10)`

The middle pentagon is again `P`; its cut vertices are `0` and `2`, at cyclic
distance two. Up to reflection, distances one and two exhaust distinct pairs
of vertices on a pentagon.

The program checks these intersections, checks that no two cycle blocks share
an edge, and checks that every graph has vertices `0,...,10` and 13 edges. This
guards against the easy ambiguity between a middle triangle whose pentagons
share its same vertex and one whose pentagons use distinct vertices.

## Weighted matching partitions

Give vertex `v` an independent SymPy symbol `a_v`, declared positive. For any
vertex set `S`, define the signless weighted matching partition

`Z_S(a)=sum_(M matching in H[S]) product_(v in S-V(M)) a_v`.

Equivalently, if `v` is the least vertex of `S`, the script enumerates it by

`Z_S=a_v Z_(S-v)+sum_(vw in E(H[S])) Z_(S-{v,w})`,

with `Z_empty=1`. Write

`Z_{H-X}=Z_(V(H)-X)`.

Every partition used below is computed by this recurrence from the explicitly
listed edge set; there are no hand-entered partition formulas.

## Sachs real and imaginary parts

Use the normalized characteristic polynomial convention in which a selected
cycle of length `l` has multiplier `-2 i^(-l)`. Consequently a triangle has
multiplier `-2i`, while either pentagon has multiplier `+2i`.

Let `T,P,Q` denote the listed triangle and pentagons. A collection contributes
only when its cycles are vertex-disjoint. Since none of the four configurations
has all three cycles pairwise disjoint, there is no triple-cycle term. The
exact grouped Sachs parts are

`R=Z_H + 4 sum_(C in {P,Q}, T disjoint C) Z_{H-T-C}`
`        - 4 [P disjoint Q] Z_{H-P-Q},`

`I=-2 Z_{H-T}+2 Z_{H-P}+2 Z_{H-Q}.`

Here `[condition]` is one or zero. These formulas specialize as follows:

- bouquet: `R=Z_H`;
- triangle middle: `R=Z_H-4Z_{H-P-Q}`;
- pentagon middle, either distance: `R=Z_H+4Z_{H-T-Q}`.

The imaginary formula is the same in all four cases. Although the latter two
real parts contain a positive mixed triangle-pentagon term, and the triangle-
middle real part contains a negative two-pentagon term, the final expanded
certificates are coefficientwise positive.

## Isolated weighted pentagons and `Phi`

Let

`p=Z_P(a|_P)` and `q=Z_Q(a|_Q)`

be the matching partitions of the isolated 5-cycles on the same vertex
activities. Their edge sets include only the five edges of the corresponding
cycle. Thus the two isolated normalized Sachs polynomials are `p+2i` and
`q+2i`, and

`(p+2i)(q+2i)=(pq-4)+2i(p+q).`

If the core Sachs polynomial is `R+iI`, the oriented cross product with this
comparison product is

`Im(((p+2i)(q+2i)) conjugate(R+iI))`
` =2R(p+q)-I(pq-4)=Phi.`

The script constructs this expression exactly, expands it as a multivariate
polynomial in the ordered generators `(a0,...,a10)` over `ZZ`, and checks every
nonzero coefficient.

## Exact results

The canonical SymPy `Poly.terms()` stream consists of each exponent tuple and
its integer coefficient, in SymPy's deterministic monomial order. The script
hashes the ASCII lines `exponent_tuple:coefficient` with SHA-256.

| core | terms | min | max | SHA-256 |
|---|---:|---:|---:|---|
| bouquet | 2547 | 2 | 32 | `8112f2944f9823177afd48deccfb958ac960548e09d9d838e4965c33eb39e979` |
| triangle middle, distinct vertices | 2192 | 2 | 32 | `4fdb04cee38f0c0e2ac2de6dff7e641c2e190a3c018af8308a5c69e378de2ba2` |
| pentagon middle, distance 1 | 2925 | 2 | 36 | `bfa73346f169f28ec6109418ce22fe44daaae6b081ade30074932b139f0828f4` |
| pentagon middle, distance 2 | 2895 | 2 | 36 | `5c6c213471a856cb743afda8e62407d7d27de5984b612c70ab411499011db437` |

Thus `Phi>0` throughout the positive activity orthant in every listed core.
Indeed coefficient positivity gives `Phi>0` already whenever all activities
are nonnegative and at least one monomial evaluates positively; positivity of
all `a_v` makes this immediate.

## Reproduction

From the repository root, run

```text
python positive-square-energy/experiments/c3_c5_c5_shared_cluster_certificate.py
```

The expected output is

```text
PASS bouquet terms=2547 min_coefficient=2 max_coefficient=32 sha256=8112f2944f9823177afd48deccfb958ac960548e09d9d838e4965c33eb39e979
PASS triangle_middle_distinct_vertices terms=2192 min_coefficient=2 max_coefficient=32 sha256=4fdb04cee38f0c0e2ac2de6dff7e641c2e190a3c018af8308a5c69e378de2ba2
PASS pentagon_middle_cut_distance_1 terms=2925 min_coefficient=2 max_coefficient=36 sha256=bfa73346f169f28ec6109418ce22fe44daaae6b081ade30074932b139f0828f4
PASS pentagon_middle_cut_distance_2 terms=2895 min_coefficient=2 max_coefficient=36 sha256=5c6c213471a856cb743afda8e62407d7d27de5984b612c70ab411499011db437
```

All validations use explicit `RuntimeError` checks rather than Python
`assert`, so running with `python -O` does not disable the certificate checks.
The computation uses exact SymPy integer arithmetic and has no numerical step.

## Interpretation and limitation

The calculation proves the exact coefficient statements and the positivity of
`Phi` for the four explicitly weighted cores. Since `Phi` is the cross product
of `R+iI` with `(p+2i)(q+2i)`, it supplies the corresponding pointwise phase
ordering whenever those two expressions are the intended core and comparison
polynomials and their continuous argument branches are fixed compatibly.

No broader graph theorem is claimed here. In particular, if arbitrary rooted
trees are eliminated into effective core activities, one must separately show
that the chosen isolated pentagon factors `p+2i,q+2i` are the correct phase
comparison for that compression and control any common positive factors and
argument branches. The present certificate is the exact algebraic component
needed for such an argument, not a substitute for it.
