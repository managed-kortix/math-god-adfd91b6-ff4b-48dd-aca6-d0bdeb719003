# Cycle 229: Gauss-projected finite-size coercivity and its frustration obstruction

This note gives an explicit bounded-operator local-to-global theorem for
overlapping two-plaquette blocks.  The theorem is formulated first on the
unconstrained tensor product of link Hilbert spaces and is then compressed by
the global Gauss projector.  Thus it does not incorrectly tensor-factor the
physical Hilbert space.  For a square lattice the exact bulk overlap loss is at
most `22 eta`.

The theorem is rigorous for bounded block operators only; it does not directly
cover the unbounded electric Kogut--Susskind blocks.  Independently, the natural
shifted Kogut--Susskind blocks at positive magnetic coupling have incompatible
local vacua.  This is an architecture obstruction to this
Knabe/detectability implementation, not an obstruction to every finite-size
criterion and not a Yang--Mills mass-gap result.

## 1. Ambient and physical spaces

Let `G` be a compact connected gauge group equipped with a nonconstant faithful
Wilson representation, and let `Lambda` be a finite square lattice with
periodic boundary conditions and side lengths at least five.  Put

\[
 {\cal K}_\Lambda=\bigotimes_{e\in E(\Lambda)}L^2(G,dU_e).
                                                               \tag{229.1}
\]

For `g=(g_x)_(x in V)`, let `R(g)` act on an oriented link by
`U_(xy) -> g_x U_(xy) g_y^(-1)`.  The orthogonal Gauss projector is

\[
 P_\Lambda=\int_{G^{V(\Lambda)}}R(g)\,dg,
 \qquad {\cal H}_{\Lambda,\mathrm{phys}}=P_\Lambda{\cal K}_\Lambda.
                                                               \tag{229.2}
\]

This Haar-average definition, rather than a product of plaquette class spaces,
is used throughout.  If `X` is a union of links, an operator on
`K_X=\bigotimes_(e in X)L^2(G)` is embedded as
`A_X\otimes I_(X^c)`.  A local
operator is admissible when this extension commutes with every `R(g)`, and
hence with `P_Lambda`.  Electric Casimirs and traced Wilson plaquettes are
admissible.  Here `w_p` denotes the normalized real part of the Wilson trace.
Spectral projections of an admissible self-adjoint operator are also
admissible.

Let `B` be the set of unordered pairs of edge-adjacent plaquettes.  A block
`B={p,q}` contains their seven links.  On a periodic square lattice every
plaquette occurs in four blocks and every link occurs in seven blocks.  Thus,
in the normalization of Cycles 226 and 228,

\[
 k_B={1\over7}\sum_{e\subset p\cup q}C_e
       +{\lambda\over4}\sum_{r\in\{p,q\}}(1-w_r),
 \qquad K_{\Lambda,\lambda}=\sum_{B\in{\cal B}}k_B.    \tag{229.3}
\]

Multiplying one block by seven gives exactly the Cycle 226 shared-link
operator at coupling `lambda_block=7 lambda/4`.  After maximal-tree gauge
fixing its invariant sector is `L^2(G^2)^Ad`; for `G=SU(2)` its electric
eigenvalues are `3C_a+3C_b+C_c`.  Equation (229.3) therefore preserves the
mandatory simultaneous-conjugation and shared-intertwiner check.

Two blocks are called dependent when their seven-link supports intersect.
For one horizontal dual edge, the plaquettes incident to its seven primal
links are its two endpoints and their six other dual neighbors.  These eight
dual vertices induce nine dual edges.  Hence exactly `4*8-9=23` dual edges
have at least one endpoint in this set, one of which is the original block.
Every bulk block therefore has exactly

\[
                         D=23-1=22                         \tag{229.4}
\]

other dependent blocks.  This safe constant avoids any use of a
plaquette-tensor decomposition.  Link-disjoint block operators commute.

## 2. A bounded Gauss-projected overlap theorem

**Theorem 229.1 (overlap coercivity).**  Let `(h_B)_(B in B)` be nonnegative,
bounded self-adjoint admissible local operators on the ambient link tensor
product.  Suppose:

1. `h_B^2 >= gamma h_B` for every block and one `gamma>0`;
2. for every dependent pair,
   `{h_B,h_C} >= -eta(h_B+h_C)` with one `eta>=0`;
3. link-disjoint pairs strongly commute; and
4. the common physical zero space
   `G_phys=P_Lambda(intersection_B ker h_B)` is nonzero.

If `c=gamma-D eta>0`, then, for `H=sum_B h_B`,

\[
 H^2\ge cH,
 \qquad
 H\big|_{{\cal H}_{\Lambda,\mathrm{phys}}\ominus
                 {\cal G}_{\rm phys}}\ge c.               \tag{229.5}
\]

In particular the physical spectral gap is at least `gamma-22 eta` for the
square-lattice two-plaquette cover.

**Proof.**  On the ambient tensor product,

\[
 H^2=\sum_Bh_B^2+\sum_{B<C}\{h_B,h_C\}.
\]

The first sum is at least `gamma H`.  A disjoint pair contributes
`2h_Bh_C>=0`.  The dependent pairs contribute at least
`-eta sum_(B~C)(h_B+h_C)`.  Each `h_B` occurs at most `D` times in the latter
sum, proving `H^2 >= (gamma-D eta)H`.  The spectral theorem then gives
`spec(H) subset {0} union [c,infinity)` and
`ker H=intersection_B ker h_B`.

Admissibility gives `[H,P_Lambda]=0`, so the physical space reduces `H` and
compression preserves the form inequality.  Its zero space is exactly
`G_phys`; applying the same spectral statement on its orthogonal complement
proves (229.5).  No factorization of `P_Lambda K_Lambda` was used.  QED.

Boundedness is part of the theorem, not a technical shorthand.  In particular,
Theorem 229.1 does not apply directly to blocks containing the unbounded
electric Casimirs.  Such an application would require a separate unbounded
operator or closed-form theorem that justifies the domain of `H^2`, every
product `h_Bh_C`, the anticommutator sum, and passage from core inequalities to
the asserted spectral inequality.  Those facts are not supplied here.

The same proof permits nonuniform constants:

\[
 h_B^2\ge\gamma_Bh_B,\quad
 \{h_B,h_C\}\ge-\eta_{BC}(h_B+h_C)
 \quad\Longrightarrow\quad
 c=\min_B\left(\gamma_B-\sum_{C:C\sim B}\eta_{BC}\right). \tag{229.6}
\]

This is the elementary Knabe square argument.  When the `h_B` are projections,
`gamma=1`; products of their kernels may then be organized as a detectability
operator, but that reorganization does not improve (229.5) without an
additional angle estimate.

## 3. Finite tests and the unbounded-pencil boundary

Every constant in Theorem 229.1 is local.

* `gamma_B` is the first positive eigenvalue of `h_B` (or any certified lower
  bound for it).
* For bounded `h_B,h_C`, `eta_BC` is the nonnegative part of the bottom
  generalized spectral value

\[
 \eta_{BC}=\max\left\{0,
 -\inf_{\psi:\langle\psi,(h_B+h_C)\psi\rangle>0}
 {\langle\psi,\{h_B,h_C\}\psi\rangle
  \over\langle\psi,(h_B+h_C)\psi\rangle}\right\}.   \tag{229.7}
\]

It lives on the union of two dependent blocks, not on a tensor product of their
physical quotients.  In the bounded setting one computes it in the
unconstrained union-link space, decomposes by the vertex gauge action if
desired, and only then applies the appropriate Gauss projector.  All relative
block placements form a finite list.

For an unbounded electric pencil, (229.7) is only a conditional diagnostic.  It
does not define or certify an anticommutator inequality until one has specified
a common product/form domain, proved that the numerator has a semibounded
closable realization representing `h_Bh_C+h_Ch_B`, and shown that its closed
inequality has the meaning required by a separate unbounded overlap theorem.
Theorem 229.1 itself supplies none of these steps.

A spin cutoff is fail-closed only after bounding the omitted sector.  For
`SU(2)`, let `Pi_J` retain link spins at most `J`.  To certify a proposed
`gamma`, one proves `h_B^2-gamma h_B>=0`; to certify a proposed `eta`, one
proves

\[
             \{h_B,h_C\}+\eta(h_B+h_C)\ge0.               \tag{229.8}
\]

For a bounded operator pencil, split by `Pi_J`, enclose the finite block
exactly, and bound its tail and off-diagonal blocks.  For an unbounded electric
pencil this Schur protocol is conditional: one must first construct a
self-adjoint or closed semibounded realization of that particular pencil,
prove that the cutoff decomposition respects its form domain, and certify a
positive lower bound and resolvent control on the omitted tail.  Explicit
Casimir eigenvalues, Wilson norm bounds, and Cauchy estimates for first-order
electric--Wilson commutators are ingredients, not a substitute for those
domain and closure proofs.  If any prerequisite is absent, if the Schur
complement is not justified, or if the resulting intervals do not prove
`c>0`, the test returns failure.  Ritz values alone are not accepted.  Cycle
228 supplies the smallest-block electric floor but does not construct or
certify the unbounded overlap pencil (229.8).

## 4. Exact obstruction for shifted Kogut--Susskind blocks

The formal choice one would like to use for (229.3) is

\[
 e_B=\inf\operatorname{spec}k_B,
 \qquad h_B=k_B-e_B.                                      \tag{229.9}
\]

It gives a nonnegative self-adjoint unbounded operator and
`h_B^2 >= gamma_B h_B` by spectral calculus when the block has a positive first
gap.  It is not covered by Theorem 229.1, and independently its local kernels
do **not** satisfy the common-vacuum condition when `lambda>0`.

**Proposition 229.2 (overlapping local vacua are incompatible).**  For
`lambda>0`, two distinct blocks sharing a plaquette and each having links
outside the other have

\[
             \ker(k_B-e_B)\cap\ker(k_C-e_C)=\{0\}
                                                              \tag{229.10}
\]

after extension to the union-link Hilbert space.  The statement already holds
before Gauss projection.

**Proof.**  On the compact connected manifold `G^7`, `k_B` is a uniformly
elliptic Laplacian plus a bounded real potential.  Its heat semigroup is
positivity improving, so its ground state `phi_B` is unique and strictly
positive.  Hence the extended kernel is
`span{phi_B}\otimes K_(B^c)`.

Let `X=B\C` and `Y=B intersect C`.  If a nonzero vector belonged to both
extended kernels, its reduced density matrix on `B` would be the pure state
`|phi_B><phi_B|`.  The `C | C^c` product forced by the second kernel makes that
same reduced density matrix a product across `X|Y`.  Therefore `phi_B` would
factor as `f(X)g(Y)`.

This factorization is impossible.  Write `B={p,q}` and `C={p,r}`.  The three
links of `q` outside `p` lie in `X`, while the link shared by `p` and `q` lies
in `Y`; the entire `p`-Wilson term depends only on `Y`.  Dividing the
ground-state equation by the strictly positive product would therefore write
the `q`-Wilson potential as a sum of an `X`-function and a `Y`-function,
because every link Laplacian acts on only one factor.  But fixing all other
links and varying one link on each side gives a nonzero mixed difference
(equivalently, choose equal nonzero Lie-algebra directions in the mixed second
derivative at the identity) of
`Re Tr(U_1 U_2 U_3^(-1)U_4^(-1))`.  This contradiction proves (229.10).  QED.

Consequently `intersection_B ker h_B={0}` for the canonical cover.  If a
separate unbounded square theorem and its overlap hypotheses were established,
its estimate could at most prove a lower bound on the absolute spectrum of

\[
 \sum_Bh_B=K_{\Lambda,\lambda}-\sum_Be_B,              \tag{229.11}
\]

but this operator has no zero vacuum.  Such a bound does not control
`K-E_0(K)` and therefore is not a spectral-gap bound.  Replacing `h_B` by the
projectors onto local excited spaces has the same incompatible-kernel problem;
the detectability lemma cannot repair an empty common ground space.

This is the promised obstruction: the non-tensor Gauss issue is completely
handled by ambient embedding and projection, while non-frustration-freeness
blocks the direct Knabe/martingale/detectability route based only on overlapping
two-plaquette vacua.  A live non-frustration-free criterion must use larger
windows and boundary-energy corrections, or control the global ground-state
conditional expectations; neither datum is contained in the Cycle 226/228
two-plaquette gaps.

## 5. Scaling and trust boundary

With the convention used in the preceding Yang--Mills cycles,
`H_KS=(g^2/(2a))K_lambda` and `lambda=2/g^4`.  A proved dimensionless constant
`c(lambda)` from a bounded realization of (229.5), or from a separately proved
unbounded analogue, would yield

\[
                         \Delta_{\rm phys}(a,g)
       \ge {g^2\over2a}c(2/g^4).                         \tag{229.12}
\]

The present canonical blocks do not meet the theorem's common-vacuum
hypothesis, so (229.12) is not obtained.  Moreover the continuum path has
`g(a)->0` and `lambda->infinity`; Cycle 228's positive interval
`lambda_block<12/7` does not cover it.  Even a future volume-uniform lattice
bound would leave continuum tightness, reflection positivity, nontriviality,
and Osterwalder--Schrader reconstruction as separate gates.
