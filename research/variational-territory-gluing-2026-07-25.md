# Variational gluing for the residual `C3 + C_{4k+1}` case

## Exact PSD witness correction

Let

`M = [[A,E],[E^T,B]]`, `P=A_+`, `Q=B_+`,

where `E` is the omitted cross adjacency between two induced territories.  Let
`Pi` and `Omega` be the orthogonal projectors onto the positive spectral
subspaces of `A` and `B`, respectively.  Put

`D = Pi E Omega`.

Then

`s^+(M) >= s^+(A)+s^+(B)+||D||_F^2`.                    (1)

Proof.  Set `R=P direct_sum Q`, `C=[[0,E],[E^T,0]]`, and let `S` be the
positive spectral subspace of `A direct_sum B`.  For every PSD matrix `Z`
supported on `S`, the witness `R+Z` is PSD.  Since `A=P` on `range(Pi)` and
`B=Q` on `range(Omega)`, the variational identity gives

`2 tr(M(R+Z))-tr((R+Z)^2)`
` =s^+(A)+s^+(B)+2 tr(CZ)-tr(Z^2)`.

Maximizing over PSD `Z` supported on `S` gives

`s^+([[0,D],[D^T,0]])`.

The last matrix is bipartite and has positive eigenvalues equal to the
singular values of `D`; its positive square energy is `||D||_F^2`.  This
proves (1).  An optimizing witness is

`R + ([[0,D],[D^T,0]])_+`,

embedded in the positive spectral subspace.

Thus induced-subgraph superadditivity has an explicit, strictly positive
correction whenever `Pi E Omega` is nonzero.  If both territories are
connected and `E` is a nonzero nonnegative matrix, this compression is
nonzero: unit Perron vectors `x,y` belong to the two positive subspaces and
`x^T E y>0`.

## Exact two-dimensional mixing

For any unit vectors `x in range(Pi)` and `y in range(Omega)`, change the sign
of `y` so that

`gamma=x^T E y >=0`.

For a PSD `2 by 2` matrix `K=[[r,z],[z,s]]`, add `[x,y]K[x,y]^T` to
`P direct_sum Q`.  The gain in the variational objective is exactly

`4 gamma z-r^2-s^2-2z^2`.                                (2)

For fixed `z>=0`, positive semidefiniteness requires `rs>=z^2`; hence
`r^2+s^2>=2z^2`, with equality at `r=s=z`.  Optimizing
`4 gamma z-4z^2` gives

`r=s=z=gamma/2`

and the exact rank-one mixing gain

`gamma^2`.                                                (3)

The corresponding correction is

`(gamma/2)[x;y][x;y]^T`.

Optimizing (3) over `x,y` gives `||Pi E Omega||_op^2`.  Allowing all singular
directions simultaneously gives the Frobenius correction (1).

For a single bridge `uv`, `E=e_u e_v^T`, and (1) becomes

`s^+(M) >= s^+(A)+s^+(B)+Pi_uu Omega_vv`.                 (4)

Indeed, `Pi E Omega=(Pi e_u)(Omega e_v)^T`.  Formula (4) is the desired rooted
diagonal form: the root quantities are the positive spectral leverage scores
`Pi_uu` and `Omega_vv`.  It is at least the Perron-only gain
`(x_u y_v)^2`, but can be substantially larger.

If rooted diagonals of the positive parts themselves are preferred, spectral
calculus gives

`Pi >= P/rho(A)`, `Omega >= Q/rho(B)`.

Consequently the bridge correction also satisfies

`Pi_uu Omega_vv >= P_uu Q_vv/(rho(A)rho(B))`.              (5)

This is weaker than (4), but it uses exactly the rooted quantities
`(A_+)_uu,(B_+)_vv`.  The Perron-only version is

`Pi_uu Omega_vv >= x_u^2 y_v^2`,

because each positive projector contains the Perron rank-one projector.

For several omitted cross edges, the correction is exactly the square
Frobenius norm

`||Pi E Omega||_F^2`,                                     (6)

which automatically includes all interactions between edges.  Positivity of
Perron vectors proves strictness but does not justify replacing (6) by a sum
of independent edge gains.

## Reduction for the two territories

Let `H3` be an induced triangular unicyclic territory and `Hq` an induced
unicyclic territory whose cycle has length `q=4k+1`.  Write

`sigma_3=s^+(H3)-|H3|>0`,

`delta_q=|Hq|-s^+(Hq)>0`.

Ning--Zeng supplies both strict signs.  Applying (1) to the omitted cross
adjacency gives

`s^+(G) >= |G|+sigma_3-delta_q+||Pi_3 E Pi_q||_F^2`.       (7)

Consequently the residual follows from the rooted quantitative inequality

`delta_q-sigma_3 <= ||Pi_3 E Pi_q||_F^2`.                  (8)

For a bridge `uv`, this is simply

`delta_q-sigma_3 <= (Pi_3)_uu (Pi_q)_vv`.                  (9)

For a partition through a shared cyclic block, use the full cross adjacency
in (8), not one selected edge.

## Matching-ratio form of the remaining threshold

For an odd unicyclic graph `H` with unique cycle `C_l`, define the Ning--Zeng
ratio

`rho_H(t)=2 M_{H-V(C_l)}(t)/M_H(t)>0`,

where `M_K(t)=i^{-|K|} mu_K(it)` is the signless matching polynomial on the
positive imaginary axis.  Their phase identity gives

`s^+(H)-|H|=(2/pi) integral_0^infinity t arctan(rho_H(t)) dt`

when `l=3 mod 4`, and the negative of this expression when `l=1 mod 4`.
Therefore

`sigma_3=(2/pi) integral_0^infinity t arctan(rho_3(t)) dt`,

`delta_q=(2/pi) integral_0^infinity t arctan(rho_q(t)) dt`. (10)

The exact sufficient condition (8) is thus

`(2/pi) integral_0^infinity t`
`  [arctan(rho_q(t))-arctan(rho_3(t))] dt`
` <= ||Pi_3 E Pi_q||_F^2`.                                 (11)

Only the positive part of the left side requires payment.  Equation (11) is
the sharp joint territory reduction: triangle surplus and connector gain are
compared together against the bad unicyclic deficit.

## What remains

The gluing theorem is unconditional, but it does not alone prove (8) for
arbitrary rooted tree attachments.  Ning--Zeng establish the signs in (10),
not a bound relating the integral to root leverage scores.  Such leverage
scores, and Perron root coordinates even more clearly, can become small along
long or highly branched attachments.  Hence strict connector gain is not by
itself enough.

The residual is reduced to proving (11), possibly after optimizing the induced
territory partition.  A useful next lemma would be the bridge-local statement

`delta_q-sigma_3 <= (Pi_3)_uu (Pi_q)_vv`,

or a stronger tree-recursive inequality that bounds each Ning--Zeng matching
ratio integral by its rooted positive-projector diagonal.  No such inequality
is contained in the published Ning--Zeng argument, so claiming the residual
theorem before this threshold is proved would be premature.
