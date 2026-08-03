# Cycle 271: ND270 admission-threshold audit

## Verdict: ITEM 3 OVERCLAIM REMOVED; EXACT LOCAL-PRODUCTION GATE

Read hostilely, the phrase in `ND270-ADMISSION` requiring a mechanism
"capable of" changing the complete velocity `L^3` by the target factor is not a
well-defined pre-compute predicate. A finite analytic initial-data family does
not determine such a capability by its formula alone. For each member, the
factor-two statement is a statement about its unique Euler trajectory. Proving
that statement before trajectory work is already an `ND251` endpoint proof;
asserting it from stretching, mode coupling, nonstationarity, or the absence of
a known cap is only plausibility.

The admission gate must therefore separate two claims:

1. **active production:** the Euler vector field changes the complete velocity
   `L^3` at the printed datum in the desired direction;
2. **target crossing:** the resulting full Euler trajectory attains a directed
   ratio strictly above `2+eta_0`.

Only the first claim belongs to pre-compute admission. The second belongs to
promotion and still requires a directed full-trajectory enclosure. This avoids
both proof-before-compute and admission by an unfalsifiable word such as
"plausible" or "capable."

## Exact finite criterion

Let the proposal print a smooth real mean-zero divergence-free analytic family
`a -> u_a` on `T^3`, a rational parameter box `P`, one rational witness
`a_* in P`, and one direction `sigma in {+1,-1}`. Use the proposal's fixed
normalization of Haar measure and the mean-zero pressure

\[
 -\Delta p_* = \partial_i\partial_j(u_{*,i}u_{*,j}),
 \qquad \int_{\mathbb T^3}p_*=0.                         \tag{271.1}
\]

Define

\[
 F(u)=\int_{\mathbb T^3}|u|^3,
 \qquad
 \mathcal P_3(u_*)=3\int_{\mathbb T^3}
 p_*\,u_*\mathbin\cdot\nabla |u_*|.                    \tag{271.2}
\]

For smooth Euler, `dF(u(t))/dt|_{t=0}=mathcal P_3(u_*)`. Replace item 3 by the
following finite, checkable requirement.

> Print exact certificates that `u_*` is nonplanar and not stationary up to a
> Galilean translation, and print a finite directed analytic/interval
> evaluation of (271.1)--(271.2) yielding rational numbers `q>0` and `M<infinity`
> such that
> \[
>    \sigma\mathcal P_3(u_*)\ge q,
>    \qquad F(u_*)\le M.                                 \tag{271.3}
> \]
> The pressure solve and the tails in both integrals must use the same declared
> analytic-norm majorant as item 4, with every truncation index and outward
> rounding rule printed in advance.

The normalized lower bound
`sigma mathcal P_3(u_*)/F(u_*) >= q/M>0` is an exact certificate of directed
production in the **complete** velocity `L^3`, rather than in vorticity, strain,
a component, or a projection. Here `sigma=-1` denotes the backward-time
direction. If zeros of `u_*`
prevent the proposal's chosen analytic quadrature from certifying
`u_* dot grad|u_*|`, it must instead partition the domain and give directed
integrable bounds; a formal differentiation is not a certificate.

Nonplanarity must be certified from the full Fourier support, for example by
three nonzero coefficients with wave vectors spanning `R^3`; nonstationarity
modulo translation must be certified by a nonzero Fourier coefficient of
`-P(u_* dot grad u_*)+c dot grad u_*` after either solving the finite equations
for the constant `c` or excluding every `c`. These are finite witnesses, not
genericity claims.

No lower bound in (271.3), however large, certifies a factor-two endpoint: its
sign can reverse immediately, and energy conservation supplies no persistence
time. Conversely, failure to prove (271.3) does not show that the family cannot
cross two; it shows only that the proposed architecture has not supplied the
required finite admission witness.

## Revised decision boundary

- `ND270-ADMIT` means only that one frozen family has a certified genuinely 3D
  active complete-`L^3` production witness and the item 4--6 validation
  machinery. It is authorization for the finite manifest, not evidence of an
  `ND251` crossing.
- `ND270-ARCH-WALL` is returned when the proposal lacks the finite witness
  (271.1)--(271.3), supplies only a proxy quantity, or invokes an unquantified
  mechanism. The verdict is architecture-local, not a no-go theorem.
- Promotion remains exactly the predeclared outward-rounded full-field endpoint
  ratio `>2+eta_0`. No positive derivative, Galerkin crossing, sampled
  trajectory, or absence of a known upper bound can substitute for it.

Thus no proposed family can honestly pass a pre-compute demand that item 3
itself establish factor-two capability, unless it has already done the
trajectory proof that admission was meant to precede. The exact finite repair
is the local-production criterion (271.1)--(271.3), with factor two reserved for
the promotion gate.
