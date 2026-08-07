# Cost-five equality faces for rank-six canonical kernels

## Scope

This note proves an analytic equality-locus lemma for the two symbolic geometries
that occur in the rank-six frontier. It supplies the missing lower bound: the
displayed cost-five Grams are not merely feasible certificates but global
minimizers of their canonical correlation objectives.

Here "equality face" follows the frontier terminology. Because the path
objective is convex but nonlinear, its minimizer locus need not be a face of
the elliptope in the strict convex-geometric sense.

The result does **not** assert that every order-eight through order-ten row has
one of these two support ledgers. A complete theorem still has to exclude a
third, coupled equality ledger. The point of the lemma is that this remaining
step is now purely combinatorial/SDP-face separation, rather than verification
of the two known geometries.

## Correlation objective

For a path of length `l` whose branch-end correlation is `r`, exact path
elimination gives the excess

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                       (1)

Thus a canonical parity row has objective

`Phi(R)=sum_P f_(l(P))(R_(u(P),v(P)))`,                     (2)

where `R` ranges over the elliptope `R psd`, `diag(R)=1`. In particular,

`f_1(r)=(1+r)/(1-r)`.                                       (3)

The value at `r=1` is interpreted as `+infinity`.

Call a pair of parallel canonical paths **mixed** if one has length one and
the other has length two. Call a path a **contraction** at a Gram point if its
transformed endpoint correlation is one, so its contribution is zero.

## Lemma 1 (the mixed-pair atom)

For `-1<=r<1`,

`f_1(r)+f_2(r)>=1`,                                         (4)

with equality if and only if `r=-1/2`.

### Proof

Put `r=cos(theta)` and `t=tan(theta/4)`, where `0<t<=1`; the endpoint `t=0`
has infinite odd-path cost. The odd and even contributions are

`f_1(r)=cot^2(theta/2)` and `f_2(r)=2tan^2(theta/4)`.

Writing `x=t^2` gives

`f_1(r)+f_2(r)=1/(4x)-1/2+9x/4 >= 1`,                       (5)

by AM-GM. Equality holds exactly when `x=1/3`, equivalently
`theta=2pi/3` and `r=-1/2`. `QED`

This is a scalar dual certificate. In particular, five independent mixed
pairs already contribute at least five; positive semidefiniteness is needed
only to decide whether their five equality correlations have a simultaneous
Gram completion.

## Lemma 2 (the tetrahedral SDP atom)

Let `R` be the correlation matrix of four unit vectors. Then

`sum_(1<=i<j<=4) f_1(R_ij) >= 3`.                            (6)

Equality holds if and only if

`R_ij=-1/3` for every `i!=j`.                                (7)

### Proof

The strictly convex function in (3) has tangent at `r=-1/3`

`f_1(r) >= 7/8+(9/8)r`,                                     (8)

with equality only at `r=-1/3`. Summing over the six pairs and using the
elliptope constraint gives

`sum_(i<j) f_1(R_ij)`
` >= 21/4+(9/8)sum_(i<j)R_ij`
` = 3+(9/16) 1^T R 1`
` >= 3`.                                                     (9)

The last term is the explicit SDP-dual stress certificate. Equality in (9)
forces equality in all six strict tangent inequalities, hence (7). Conversely,
the regular-simplex correlation matrix satisfies (7), is positive semidefinite,
and has six contributions of `1/2`. `QED`

## Theorem (atomic cost-five equality faces)

Consider a canonical rank-six correlation objective after zero-cost signed
contractions have been identified.

1. If its nonzero ledger consists of five mixed pairs, then `min Phi=5` if and
   only if the five prescribed correlations `-1/2` have a positive semidefinite
   completion. Every minimizer has all five mixed correlations equal to
   `-1/2`.
2. If its nonzero ledger consists of six odd unit paths forming all edges of a
   `K4`, together with two mixed pairs incident with an additional quotient
   vertex, then `min Phi=5` if and only if the prescribed tetrahedral and mixed
   correlations have a positive semidefinite completion. Every minimizer has
   tetrahedral correlations `-1/3` and both mixed correlations `-1/2`.
3. In the first case, if the five quotient supports form a cycle, the minimizer
   locus is precisely the signed-five-cycle PSD-completion locus. In the second
   case it is precisely the tetrahedron-plus-apex PSD-completion locus.

### Proof

Every contraction contribution is nonnegative. In the first case, Lemma 1
gives the lower bound `5`, and a PSD completion of the equality correlations
attains it. Its equality clause forces all five prescribed edge entries.

In the second case, Lemma 2 gives `3` on the six tetrahedral paths and Lemma 1
gives `1+1` on the two mixed pairs. Again, a PSD completion attains the lower
bound, and the equality clauses force every prescribed entry. Signed
contractions merely switch rows and columns by `+1` or `-1`, preserving PSD
and converting the forced entries into the signed quotient entries. This gives
the two locus descriptions. `QED`

The theorem classifies equality loci, not unique Gram matrices. Unspecified chord or
apex correlations may vary over a positive-dimensional PSD-completion face.
For example, after fixing a regular tetrahedron and apex correlations
`(-1/2,-1/2,b,1-b)`, the Gram is PSD exactly when

`1/2+b^2+(1-b)^2 <= 4/3`;                                   (10)

hence the tetrahedron-plus-apex equality locus contains a continuum of Grams.
Any claim that equality forces one displayed Gram matrix, rather than one of
the two support geometries, is therefore false.

## Lemma 3 (rigidity under same-parity lengthening)

For fixed transformed endpoint angle `beta`,

`l tan^2(beta/(2l))`                                         (11)

strictly decreases with real `l>=1` unless `beta=0`. Therefore replacing a
canonical path by a same-parity path two edges longer strictly decreases the
value of the same branch Gram unless that path was a contraction.

### Proof

With `z=beta/(2l)`, differentiation has the sign of
`sin(z)cos(z)-z`, which is negative for `0<z<pi/2`. The value is identically
zero when `beta=0`. `QED`

Consequently, a canonical atomic equality row remains an equality target only
along contraction coordinates. This explains, without numerical optimization,
the `canonical plus three contractions` equality keys in the order-eight
symbolic fixture; every noncontraction coordinate frontier is strict.

## Remaining classification obligation

For a full orders-eight-through-ten theorem it is enough to prove the following
separation statement.

> If a canonical rank-six row has correlation optimum five, then after
> switching and contracting every zero-cost path, its positive path ledger is
> either five mixed pairs on a five-cycle or six odd `K4` edges plus two mixed
> apex pairs.

The lemmas above then identify the entire equality locus and Lemma 3 handles all
one-coordinate frontiers. What is still missing is an exposing inequality for
an arbitrary residual support that either decomposes its objective into these
atoms or leaves a positive strictness margin. Feasible rational Grams below
five prove strictness row by row, but they do not supply this global
combinatorial separation theorem.
