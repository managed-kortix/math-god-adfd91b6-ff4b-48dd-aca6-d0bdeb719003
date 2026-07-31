# Cycle 174: canonical-system truncation monotonicity and its equivalence gate

## Shifted xi target

Put

\[
 E_\omega(z)=\xi(\tfrac12+\omega-iz),\qquad \omega>0,
\]

and write `E#(z)=overline(E(overline z))`.  The standard shifted-xi
de Branges criterion is

\[
 \mathrm{RH}\quad\Longleftrightarrow\quad
 E_\omega\text{ is Hermite--Biehler for every }\omega>0.
\]

It is enough on the right to take positive rational `omega`, or any sequence of
positive shifts tending to zero.  Indeed, a zero with real part `beta>1/2`
becomes an upper-half-plane zero of `E_omega` as soon as
`0<omega<beta-1/2`; the functional equation supplies the converse half of the
zero symmetry.  Thus a construction uniform only for shifts bounded away from
zero cannot reach RH.

## Exact finite monotonicity lemma

Let `H(x)` be a locally integrable positive-semidefinite `2 by 2` Hamiltonian,
let

\[
 JY'(x,z)=zH(x)Y(x,z),\qquad
 J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},
 \qquad Y(0,z)=Y_0\in\mathbb R^2,
\]

and write `Y=(A,B)^T`.  With the convention `E_x=A(x,.)+iB(x,.)`, define

\[
 K_x(z,w)={A(x,z)\overline{B(x,w)}-B(x,z)\overline{A(x,w)}
             \over \pi(z-\overline w)}.
\]

### Lemma (finite canonical increments)

For `0<=s<t` and arbitrary points `z_1,...,z_m` and coefficients
`c_1,...,c_m`, one has the exact identity

\[
 \sum_{j,k}c_j\overline{c_k}
 [K_t(z_j,z_k)-K_s(z_j,z_k)]
 ={1\over\pi}\int_s^t
 \left\|H(x)^{1/2}\sum_jc_jY(x,z_j)\right\|^2dx\ge0.
\]

Consequently every finite kernel matrix is Loewner-monotone under interval
extension:

\[
 [K_s(z_j,z_k)]_{j,k=1}^m\preceq
 [K_t(z_j,z_k)]_{j,k=1}^m.
\]

The proof is just the Lagrange identity

\[
 {d\over dx}\{Y(x,w)^*JY(x,z)\}
 =(z-\overline w)Y(x,w)^*H(x)Y(x,z),
\]

integrated from `s` to `t`.  This is genuine production of positivity: each
new interval contributes a Gram square, simultaneously for every finite set of
spectral points.  It is not a decomposition into prime-local squares and is not
a finite Weil matrix calculation.

## Sharp production candidate

For each positive rational `omega`, construct a single trace-normalized positive
canonical system and an exhaustion `L_N` for which the endpoint kernels satisfy

\[
 K_{\omega,N}(z,w)\longrightarrow
 K_{E_\omega}(z,w)
 ={E_\omega(z)\overline{E_\omega(w)}
       -E_\omega^\#(z)\overline{E_\omega^\#(w)}
   \over 2\pi i(\overline w-z)}
\]

locally uniformly on `C by C`, with conventions adjusted by an inessential
overall positive constant.  Require, for example, that on one fixed interval
the Hamiltonian be positive definite on a set of positive measure.  The
integral formula then makes every upper-half-plane diagonal strictly positive.
The finite-increment lemma and passage to the limit give `K_E>=0`, while this
nondegeneracy gives the strict Hermite--Biehler inequality.  Doing this for
rational shifts tending to zero proves RH.

An arithmetic version would be especially sharp: piecewise-constant positive
Hamiltonians whose entries and breakpoints are explicit, together with a
locally uniform error bound for the endpoint kernel.  Unlike checking any fixed
matrix, the error theorem has to hold over the entire exhaustion and survive as
`omega` tends to zero.

## Equivalence no-go

The analytic candidate is not a weaker positivity principle.  The de Branges
inverse theorem and the canonical chain of de Branges subspaces give the reverse
implication: if `E` is Hermite--Biehler, its reproducing kernel has a positive
canonical-system realization, and finite initial intervals (equivalently,
nested de Branges subspaces) have kernels increasing to `K_E`.  Hence, after
the routine normalization and nondegeneracy clauses,

\[
 \boxed{
 \text{positive canonical exhaustion converging to }K_{E_\omega}
 \quad\Longleftrightarrow\quad E_\omega\text{ is Hermite--Biehler}.}
\]

Requiring these exhaustions for all positive shifts is therefore RH-equivalent.
The monotonicity identity tells exactly what a successful structural proof must
produce, but it supplies no positivity before a positive Hamiltonian realizing
the xi endpoint has been constructed.

There is a second finite-level warning.  For a fixed kernel and nested node sets,
the normalized minimum eigenvalue can only decrease by the variational
principle.  Schur-complement pivots are squared interpolation distances only
after kernel positivity is known.  Thus node refinement, Hankel-section
contraction, determinant ratios, or finite pivot positivity do not create an
independent route: over a dense exhaustion they are precisely the
Hermite--Biehler kernel criterion.

## Decision

The exact candidate is the explicit positive-Hamiltonian exhaustion with a
locally uniform endpoint-kernel error bound and shifts tending to zero.  It is
structurally beyond finite Weil positivity and prime-local SOS because interval
extension has an exact global Gram increment.  Existentially, however, it is
equivalent to the shifted Hermite--Biehler assertion and hence to RH.  Without a
new arithmetic construction of the Hamiltonian and the uniform endpoint bound,
canonical truncation monotonicity is an equivalence gate, not an RH advance.

No Riemann-hypothesis result is claimed.
