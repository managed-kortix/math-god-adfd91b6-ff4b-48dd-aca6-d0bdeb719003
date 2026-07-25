# First-chain sign gap for the cactus DNN bound

## Conclusion

Let `A=P-B` be the spectral decomposition into positive and negative parts,
so `B=A_-`, `P B=0`, and `s=tr(B^2)=s^-(G)`.  The first step of the DNN
chain has an exact, useful refinement.  If

`p = sum_{uv in E} max(B_uv,0)`,

then

`kappa(G)-s >= 8p + 16p^2/s`.                              (1)

Thus positive edge mass does not worsen the final estimate: it consumes DNN
slack.  For the two-`C5` residual, the required improvement is exactly

`2(5-2sqrt(5))-1 = 9-4sqrt(5) = 0.055728...`,

so (1) closes the case whenever

`p >= (9-4sqrt(5))/8`.

It does not close the general case.  Actual negative parts can have `p=0`;
this occurs already for the bare `C5-P3-C5` handcuff and for its tested
middle-star extensions.  Hence no uniform improvement can come from the sign
gap alone.

There is, however, an exact finite sum-of-squares identity forced by
`PB=0`.  It is the cleanest algebraic certificate produced by this route:

`-sum_{uv in E} B_uv(1+B_uv)`
`  = (1/2) sum_u B_uu^2 + sum_{uv notin E, u<v} B_uv^2 >= 0`. (2)

Identity (2), together with the entrywise quadratic equations

`A B + B^2 = 0`,                                                (3)

is a finite polynomial description of the extra constraints absent from the
DNN relaxation.  I did not obtain nonnegative multipliers that combine
(2)-(3) with positive semidefiniteness to certify `s<=n+2` for arbitrary
tree attachments.  That assertion remains open for the residual bicyclic
families.  Interpreted literally for all cacti of unrestricted cyclomatic
number, it is false (for example, a bouquet of three `C5` blocks has
`s^-=15.3396...>15=n+2`).

## Exact sign-gap calculation

The trace identity and the definition of `p` give

`sum_{uv in E} B_uv = -s/2`,

`sum_{uv in E} |B_uv| = s/2+2p`.

Applying the optimized DNN inequality to `M=B o B` therefore yields the
strictly refined chain

`(s+4p)^2`
` = 4 (sum_{uv in E}|B_uv|)^2`
` <= kappa(G) 1^T(B o B)1`
` = kappa(G)s`.

After division by `s>0`, this is exactly

`s+8p+16p^2/s <= kappa(G)`,

which proves (1).  The direction is worth emphasizing: although positive
edge entries make the intermediate absolute-value sum larger, that sum is
bounded above by the DNN certificate, so they force `s` downward.

For a bicyclic cactus with two `C5` blocks,

`kappa(G)=n+1+2(5-2sqrt(5))=n+2+(9-4sqrt(5))`.

Consequently (1) proves `s<=n+2` under the slightly weaker exact condition

`8p+16p^2/s >= 9-4sqrt(5)`.

The displayed lower bound on `p` is a convenient sufficient condition, not a
necessary one.

## The polynomial SOS identity

Write `b_uv=B_uv`.  Since `PB=0`,

`AB=(P-B)B=-B^2`.

Taking traces gives

`2 sum_{uv in E} b_uv = tr(AB) = -tr(B^2)=-s`.                (4)

On the other hand, expanding the Frobenius norm by diagonal, edge, and
nonedge positions gives

`s=sum_u b_uu^2+2sum_{uv in E}b_uv^2`
`    +2sum_{uv notin E, u<v}b_uv^2`.                          (5)

Adding `sum_E b_uv^2` to (4) and substituting (5) proves (2)
identically.  No sign assumption on the edge entries is used.

When every edge entry is nonpositive, set `x_uv=-b_uv`.  Then (2) reads

`sum_{uv in E} x_uv(1-x_uv)`
`  = (1/2)sum_u b_uu^2+sum_{uv notin E,u<v}b_uv^2`.            (6)

Thus the diagonal and nonedge mass is exactly the aggregate deviation of the
edge variables from the roots `0,1`.  This is genuine information beyond
double nonnegativity, but it has no fixed positive lower bound: it is
homogeneous neither in `B` nor in arbitrary DNN optimizers, because equation
(3) fixes the spectral scale.

## Why a canonical odd-cycle optimizer cannot lift

The obstruction can be seen exactly on a `C5` atom.  Put

`phi=(1+sqrt(5))/2`.

The canonical folded DNN optimizer on `C5` is

`M=x(2 cos(pi/5) I+A(C5))=x(phi I+A(C5))`.

If it were `B o B` and equality held in the first chain step, its edge signs
would have to be negative.  Hence on the atom one would have edge entries
`-a` and diagonal entries `sqrt(phi)a`, where `a=sqrt(x)>0`.

Even allowing one cut vertex to receive arbitrary extra diagonal mass from
the rest of a cactus, delete that vertex.  The remaining principal `P4`
submatrix would be

`H=a(sqrt(phi)I-A(P4))`.

Its least eigenvalue is

`lambda_min(H)=a(sqrt(phi)-2cos(pi/5))`
`             =a(sqrt(phi)-phi)<0`.                           (7)

This contradicts `B>=0`.  More quantitatively, every positive semidefinite
matrix `K` on those four vertices satisfies

`||K-H||_op >= a(phi-sqrt(phi))`.                              (8)

Indeed, Weyl's inequality gives
`lambda_min(K)<=lambda_min(H)+||K-H||_op`, and the left side is nonnegative.
Thus the canonical atom is separated from every spectral lift by the exact
operator-norm gap in (8).

This does not yet give the needed objective loss `9-4sqrt(5)`.  There are two
reasons.  First, the cycle proof canonizes a DNN matrix by folding and cyclic
averaging; closeness of the objective does not immediately give entrywise
closeness before those operations.  Second, arbitrary tree attachments may
make every cycle vertex a cut vertex, so there need not be a four-vertex run
whose diagonal receives no mass from other blocks.  A complete stability
proof must quantify both losses.

## Local equations and the cubic trace

The off-diagonal form of (3) is completely explicit:

`sum_{w adjacent to u} B_wv + sum_w B_uw B_wv = 0`             (9)

for every ordered pair `u,v`.  These equations do not support the proposed
operation of simply discarding terms.  Positive semidefiniteness fixes the
sign of the diagonal entries but not of nonedge entries, and even in the
important regime `p=0` it fixes edge signs only.  Both sums in (9) can
therefore contain cancellations.

The cubic trace supplies another exact equality but no missing inequality:

`tr(A^3)=tr(P^3)-tr(B^3)=6 tau(G)`,                            (10)

where `tau(G)` is the number of triangles.  Equivalently,
`tr(B^3)=tr(P^3)-6tau(G)`.  In the two-`C5` family this reduces to
`tr(B^3)=tr(P^3)` and gives no sign-sensitive separation from the canonical
cycle atoms.  Multiplying (3) by `B` and tracing gives only the tautological
form `tr(AB^2)=-tr(B^3)`.  Thus neither (9) with unsigned term deletion nor
the third moment alone yields the `9-4sqrt(5)` stability gap.

## Exact finite certificate currently available

For a fixed graph, the spectral lift satisfies the following finite system:

1. `B>=0` in the positive-semidefinite sense;
2. `AB+B^2=0` entrywise;
3. `s=tr(B^2)=-2 sum_E B_uv`;
4. the SOS equality (2);
5. `(s+4p)^2<=kappa(G)s`, with `p=sum_E max(B_uv,0)`.

Items 2-4 are equalities, not relaxations.  They rigorously characterize the
failure of a generic DNN optimizer to be a spectral lift and give the exact
first-chain stability term.  What is missing for arbitrary attached trees is
a graph-uniform SOS consequence

`n+2+2 sum_E B_uv >= 0`,

or equivalently `s<=n+2`.  The canonical-atom separation (8) shows where such
a consequence could originate, but it does not supply the required global
conversion from matrix distance to DNN objective loss.
