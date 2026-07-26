# Common-cut residual bouquets: an exact rooted Schur-Sachs inequality

**Date:** 2026-07-26

## 1. Result

For a graph `G`, write

`D(G)=s+(G)-s-(G)` and `sigma(G)=s+(G)-|V(G)|`.

Let `B` be a one-vertex cycle bouquet: its cyclic blocks all contain one
vertex `x` and are otherwise vertex-disjoint. Arbitrary finite rooted trees
may be attached at every vertex of the bouquet. Put `T=C3` and `P=C5`.

**Theorem 1 (common-cut absorption).** The following bounds hold uniformly
over all attached trees.

1. If the cyclic blocks are `T^k Q`, where `k>=1` and `Q=C_q`, then

   `sigma(G)>k-delta_q` if `q=1 mod 4`, where
   `delta_q=sec(pi/q)-1<1`, and

   `sigma(G)>k` if `q` is even or `q=3 mod 4`.

2. If the cyclic blocks are `T^k PP`, where `k>=1`, then

   `sigma(G)>k+1-4/(3 sqrt(13))`.

In particular, every such bouquet satisfies `s+(G)>|V(G)|`. At octacyclic
rank the two sharp-DNN residual bouquets have the explicit margins

`T^7 Q:  sigma(G)>7-delta_q>6` for hostile `Q`, and `sigma(G)>7` otherwise;

`T^6 PP: sigma(G)>7-4/(3 sqrt(13))>6`.

The theorem is rank-free: no opening cost accumulates as `k` grows. It proves
the fully shared bouquets `(F7Q)` and the common-cut `T^6PP` bouquet left open
in `research/octacyclic-cactus-exact-status-2026-07-26.md`.

It does not prove the bridge-separated `A_k|Q` endpoint problem. There the
hostile cycle and the triangular bouquet do not share the Schur pivot, so the
scalar inequality below is no longer available.

## 2. Rooted characteristic pairs and exact tree elimination

For a forest `F`, define its signless matching partition

`Z_F(t)=sum_M t^(|V(F)|-2|M|)`, `t>0`.

If `T` is a tree rooted at the vertex `u` next to a core vertex, use the
rooted characteristic pair

`(phi_T(z),phi_(T-u)(z))`.

Since the characteristic and matching polynomials agree on a forest,

`phi_T(it)=i^|T| Z_T(t)`,

and therefore

`phi_T(it)/phi_(T-u)(it)=i q_T(t)`,

where

`q_T(t)=Z_T(t)/Z_(T-u)(t)>0`.

Orienting the branch away from the core and splitting a matching at its root
gives the exact recursion

`q_(u->p)(t)=t+sum_(w child of u) 1/q_(w->u)(t)>=t`.

Equivalently, Schur complementation of the branch changes the diagonal entry
`it` at its core neighbor to

`it-(phi_T(it)/phi_(T-u)(it))^(-1)=i(t+1/q_T(t))`.

After all branches at a core vertex `v` are removed, its diagonal is thus
`i a_v(t)`, with

`a_v(t)=t+sum_(u attached at v)1/q_(u->v)(t)=t+y_v(t)`,

`y_v(t)>=0`.

The eliminated determinants form a positive real factor after imaginary-axis
normalization. This is both the rooted-characteristic-polynomial Schur
reduction and the matching-BP reduction; they are the same identity.

## 3. The scalar bouquet formula

Let the bouquet have lobes `C_(ell_1),...,C_(ell_r)`. On lobe `j`, deleting
the common vertex `x` leaves a path on `ell_j-1` private vertices. With their
effective activities, put

`A_j=Z_(C_(ell_j)-x)>0`.

Let `B_j>0` be the sum of the two matching partitions obtained by matching
`x` to one of its two neighbors on lobe `j`. Splitting core matchings by the
status of `x` gives

`Z_B(a)=(prod_j A_j)(a_x+sum_j B_j/A_j)`.                 (3.1)

Normalize the characteristic polynomial by

`Psi_G(t)=i^(-n) phi_G(it)=prod_h (t+i lambda_h)`.

In the grouped Sachs expansion a cycle of length `ell` has multiplier

`omega_ell=-2 i^(-ell)`.

Two bouquet cycles meet at `x`, so no two can occur in one vertex-disjoint
Sachs collection. If lobe `j` is selected, deleting its whole cycle leaves
the private paths of all other lobes and contributes `prod_(h!=j) A_h`.
After removing the positive tree factor `K(t)` and the positive factor
`prod_j A_j`, the entire characteristic polynomial is therefore the single
rooted Schur expression

`W_G(t):=Psi_G(t)/(K(t) prod_j A_j)`

`       =a_x+sum_j (B_j+omega_(ell_j))/A_j`.              (3.2)

Formula (3.2) is exact. In particular,

`omega_ell=-2i` for `ell=3 mod 4`,

`omega_ell=+2i` for `ell=1 mod 4`,

and `omega_ell` is real for even `ell`.

The positive factors removed in (3.2) do not affect the continuous argument
of `Psi_G`. This reduces every attached-tree bouquet to one scalar rational
function whose variables satisfy only `a_v>=t`.

## 4. One distinguished cycle

Assume first that the lobes are `T^k Q`, `k>=1`, and `q=1 mod 4`. Write
`A_Q,B_Q` for the distinguished lobe and `A_j,B_j` for the triangles. From
(3.2),

`W_G=X+2i(1/A_Q-sum_(j=1)^k 1/A_j)`,                    (4.1)

where

`X=a_x+B_Q/A_Q+sum_(j=1)^k B_j/A_j>0`.                  (4.2)

Let `Z_q(t)` be the bare signless matching partition of `C_q`. The weighted
matching partition of the distinguished cycle, using activity `a_x` at its
root, is

`a_x A_Q+B_Q`.

Every activity is at least `t`, and matching partitions have nonnegative
coefficients. Hence

`A_Q X=a_x A_Q+B_Q+A_Q sum_j B_j/A_j`

`     > a_x A_Q+B_Q >= Z_q(t)`.                           (4.3)

The strict inequality uses `k>=1` and `B_j>0`.

Let `Theta_G(t)` be the continuous argument tending to zero at infinity. If
the imaginary part in (4.1) is nonpositive, then

`Theta_G(t)<=0<atan(2/Z_q(t))`.

If it is positive, (4.3) gives

`2(1/A_Q-sum_j 1/A_j)/X < 2/(A_Q X) < 2/Z_q(t)`.

Thus in all cases

`Theta_G(t)<theta_q(t):=atan(2/Z_q(t)).`                  (4.4)

For `q=1 mod 4`, the isolated-cycle calculation is

`D(C_q)=-2 delta_q`, `delta_q=sec(pi/q)-1`,

and the signed Coulson identity is

`D(G)=-(4/pi) integral_0^infinity t Theta_G(t) dt`.       (4.5)

Integrating (4.4) in (4.5) yields

`D(G)>D(C_q)=-2 delta_q`.                                 (4.6)

There are `k+1` cycles, so `|E(G)|=n+k` and

`sigma(G)=k+D(G)/2>k-delta_q`.                            (4.7)

If `q=3 mod 4`, every odd-cycle term in (3.2) has negative imaginary
part. If `q` is even, its Sachs term is real while the `k` triangle terms
still give a strictly negative imaginary part. In both cases `W_G(t)` lies
in the open lower half-plane for every `t>0`. Its continuous argument is
therefore negative, even if the real part changes sign. Equation (4.5) gives
`D(G)>0`, and consequently `sigma(G)>k`.

This proves Theorem 1(1), including the case `Q=T`.

## 5. Two pentagons

Now let the lobes be `T^k PP`, `k>=1`. Put

`X_PP=a_x+B_1/A_1+B_2/A_2`,

`Y_PP=2/A_1+2/A_2`.

The normalized two-pentagon bouquet with the same root and pentagon
activities is `X_PP+iY_PP`. Formula (3.2) for the full bouquet is

`W_G=X+iY`,

`X=X_PP+sum_(j=1)^k B_j/A_j>X_PP>0`,

`Y=Y_PP-2 sum_(j=1)^k 1/A_j<Y_PP`.                        (5.1)

If `Y<=0`, then `Arg W_G<=0<Arg(X_PP+iY_PP)`. If `Y>0`, both increasing the
positive denominator and decreasing the numerator strictly decrease the
arctangent. Hence, pointwise,

`Theta_G(t)<Theta_PP(t)`.                                  (5.2)

The exact two-pentagon coefficient certificate applies to arbitrary
activities `a_v=t+y_v`, `y_v>=0`. If `D_0(t)=t^4+7t^2+9`, it proves

`Theta_PP(t)<=atan(4/(t D_0(t)))<=4/(t D_0(t))`.           (5.3)

For reference, writing `A_1,A_2` for the two private `P4` matching
partitions and `R=a_x A_1 A_2+B_1 A_2+A_1 B_2`, the finite polynomial
inequality behind (5.3) is

`2R>=t(t^4+7t^2+9)(A_1+A_2)`.                              (5.4)

It is coefficientwise nonnegative after every activity is replaced by
`t+y`; the existing exact expansion has 1290 positive-coefficient monomials.

Combining (5.2)-(5.3) with Coulson gives

`D(G)>-(4/pi) integral_0^infinity 4/D_0(t) dt`

`    =-8/(3 sqrt(13))`,                                    (5.5)

because

`integral_0^infinity 4/(t^4+7t^2+9) dt=2pi/(3 sqrt(13))`.

There are `k+2` cycles, so `|E(G)|=n+k+1`. Averaging (5.5) with
`s+(G)+s-(G)=2|E(G)|` gives

`sigma(G)>k+1-4/(3 sqrt(13))`,                             (5.6)

which proves Theorem 1(2).

## 6. Exact octacyclic consequences

For the fully shared `T^7Q` bouquet, (4.7) gives

`s+(G)-n>7-(sec(pi/q)-1)=8-sec(pi/q)>6`

when `q=1 mod 4`; all other congruence classes give `s+(G)-n>7`.
This is much more than the merely positive margin required to close `(F7Q)`.

For the common-cut `T^6PP` bouquet, (5.6) gives

`s+(G)-n>7-4/(3 sqrt(13))>6`,

where the last comparison follows already from `4/(3 sqrt(13))<1`.

Thus neither octacyclic common-cut bouquet is a counterexample. The old
opening ledger failed because it charged one full tree unit for destroying a
lobe. The exact Schur-Sachs formula retains all lobes and shows instead that
every triangle simultaneously adds a positive real matching term and a
favorable negative imaginary Sachs term. For `T^kQ` this makes the bouquet
phase no larger than the isolated hostile-cycle phase; for `T^kPP` it makes
the phase strictly smaller than the already controlled two-pentagon phase.

## 7. Scope boundary

The proof uses the common vertex twice: it forbids every multi-cycle Sachs
term, and it turns the core determinant into the scalar sum (3.2). It therefore
settles common-cut bouquets of every rank in the two residual patterns, with
arbitrary rooted trees, but does not automatically settle:

1. a triangular bouquet joined by a nonempty bridge path to `Q`;
2. one- or two-triangle router chains between two pentagon hubs; or
3. a shared-cut cluster with several cut vertices.

Those configurations have genuine multi-pivot Schur complements. They require
an endpoint-export or matrix-valued phase inequality rather than the scalar
common-cut inequality proved here.

## 8. Verification

The only finite symbolic certificate invoked is (5.4), independently recorded
and executable at

`positive-square-energy/experiments/c5_bouquet_matching_certificate.py`.

Run

`python positive-square-energy/experiments/c5_bouquet_matching_certificate.py`.

The remaining identities are exact one-line Schur, matching, Sachs, and
Coulson calculations. No numerical eigenvalue sampling, attachment reduction,
or unproved edge-monotonicity is used.
