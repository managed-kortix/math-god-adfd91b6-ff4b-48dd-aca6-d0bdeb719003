# Cycle 180: anchored connected correlations and the full gap

The missing implication after Cycle 179 can be stated exactly.  Spatial
clustering of a unique vacuum is not enough.  What implies a Hamiltonian gap is
a volume-uniform *imaginary-time* connected estimate, normalized in the
physical vacuum Hilbert norm, on a form core dense in the whole vacuum
complement.  An anchored polymer estimate implies such a bound only when its
atoms have a volume-uniform stable synthesis and its connected kernel is
summable in both anchor variables.  These are the completeness hypotheses that
prevent spectator and escaping-state counterexamples.

The companion hostile audit `cycle-180-connected-local-control-no-go.md` gives
finite-volume local families showing why purely equal-time ground-state control
cannot replace the temporal and stable-synthesis assumptions below.

## Abstract connected-correlation criterion

Let `H` be a nonnegative self-adjoint operator on a Hilbert space `cal H`.  Let
`Omega` be normalized and assume

\[
 \ker H=\mathbb C\Omega .
\tag{180.1}
\]

Put `P=|Omega><Omega|` and `Q=I-P`.  Suppose a local `*`-algebra `cal A_loc`
acts on `Omega`, and that

\[
 {\cal D}_0=\{\xi_A:=Q A\Omega:A\in {\cal A}_{\rm loc}\}
\quad\hbox{has dense linear span in }Q{\cal H}.
\tag{180.2}
\]

This is the required vacuum-complement completeness condition.  For
`A,B in cal A_loc` define the connected Euclidean form

\[
 C_t(A,B)=\langle \xi_A,e^{-tH}\xi_B\rangle .
\tag{180.3}
\]

**Theorem 180.1 (uniform temporal clustering implies the full gap).**  Assume
there are `m>0`, `C<infinity`, and `t_0>=0`, independent of volume or other
regulators under consideration, such that for every `A in cal A_loc` and every
`t>=t_0`,

\[
 0\le C_t(A,A)\le C e^{-mt} C_0(A,A).
\tag{180.4}
\]

Here `cal A_loc` must be closed under finite linear combinations, so (180.4)
controls coherent sums and not merely a list of generators.  Then

\[
 \sigma(H)\subset\{0\}\cup[m,\infty),
 \qquad H\upharpoonright Q{\cal H}\ge m.
\tag{180.5}
\]

No semigroup gap, Poincare inequality, or spectral lower bound is assumed in
(180.4).

*Proof.*  Since `H>=0`, `e^{-tH}` is positive and leaves `Q cal H` invariant.
For fixed `t>=t_0`, (180.4), finite linear closure, and (180.2) extend by
continuity to every `f in Q cal H`:

\[
 \langle f,e^{-tH}f\rangle\le C e^{-mt}\|f\|^2.
\tag{180.6}
\]

If the spectral projection
`E_H((0,m-delta])Q` were nonzero for some `delta>0`, a unit vector in its range
would satisfy

\[
 e^{-(m-\delta)t}
 \le\langle f,e^{-tH}f\rangle
 \le C e^{-mt}
\]

for every sufficiently large `t`.  This is impossible once
`e^{delta t}>C`.  Taking the union over positive rational `delta` proves that
there is no spectrum in `(0,m)`.  Equation (180.1) removes an additional zero
sector and proves (180.5).  Notice that the prefactor `C` and the starting time
`t_0` do not reduce the resulting exponent.  QED.

There is also an integrated version which is often closer to what a convergent
polymer expansion directly supplies.

**Theorem 180.2 (connected susceptibility criterion).**  Under (180.1)--(180.2),
suppose that for all `A in cal A_loc`,

\[
 \int_0^\infty C_t(A,A)\,dt\le K C_0(A,A),
 \qquad K<\infty,
\tag{180.7}
\]

with the same `K` for all volumes.  Then

\[
 H\upharpoonright Q{\cal H}\ge K^{-1}.
\tag{180.8}
\]

*Proof.*  Positivity, density, and Fatou's lemma extend (180.7) to all
`f in Q cal H`: approximate `f` in norm by vectors from `cal D_0` and use the
pointwise continuity of the bounded form `e^{-tH}`.  The spectral theorem gives

\[
 \int_0^\infty\langle f,e^{-tH}f\rangle dt
 =\int_{(0,\infty)}\lambda^{-1}\,d\mu_f(\lambda)
 \le K\|f\|^2.
\tag{180.9}
\]

Thus the positive form `H^{-1}` on `Q cal H` is bounded by `K`.  A nonzero
spectral projection below `K^{-1}` would contradict (180.9), proving (180.8).
QED.

The normalization by `C_0(A,A)=||Q A Omega||^2` is essential.  A bound by an
operator norm or by a polymer norm stronger than the physical Hilbert norm does
not pass to the Hilbert completion without an additional comparison theorem.

## The anchored-polymer bridge

Here is a checkable sufficient formulation of that comparison theorem.  It
separates local cluster estimates from the global completeness step rather than
hiding the latter in the phrase "polymer norm."

Let `I` be a finite or countable set of anchored, centered polymer atoms
`xi_alpha in Q cal H`.  They may include position, shape, representation, and
intertwiner labels.  Assume:

1. **Stable synthesis.**  A dense subspace `cal D subset Q cal H` consists of
   finite sums `f=sum_alpha c_alpha xi_alpha`, and each `f in cal D` has at
   least one such representation satisfying

   \[
    \|c\|_{\ell^2(I)}\le\kappa\|f\|,
   \tag{180.10}
   \]

   with `kappa` uniform in volume.  Quotienting null relations among atoms is
   allowed.  This lower frame bound is the precise no-escaping-states
   assumption.

2. **Two-sided anchored summability.**  For

   \[
    K_t(\alpha,\beta)
      =\langle\xi_\alpha,e^{-tH}\xi_\beta\rangle,
   \tag{180.11}
   \]

   there are positive Schur weights `p_alpha` and a function `a(t)` such that

   \[
   \begin{split}
    \sup_\alpha {1\over p_\alpha}
      \sum_\beta |K_t(\alpha,\beta)|p_\beta&\le a(t),\\
    \sup_\beta {1\over p_\beta}
      \sum_\alpha |K_t(\alpha,\beta)|p_\alpha&\le a(t).
   \end{split}
   \tag{180.12}
   \]

   Equivalently, one may assume directly that the absolute connected polymer
   kernel defines an `ell^2` operator of norm at most `a(t)`.  Formula (180.12)
   is the usual anchored row-and-column test.  A bound only on polymers meeting
   one fixed anchor is insufficient unless translations and the second Schur
   estimate turn it into (180.12).

**Theorem 180.3 (polymer norm to full spectral gap).**  Under (180.1),
(180.10), and (180.12),

\[
 \langle f,e^{-tH}f\rangle
 \le \kappa^2 a(t)\|f\|^2,
 \qquad f\in Q{\cal H}.
\tag{180.13}
\]

Consequently:

* if `a(t)<=C e^{-mt}` for all `t>=t_0`, then the full gap is at least `m`;
* if `A:=int_0^infinity a(t)dt<infinity`, then the full gap is at least
  `(kappa^2 A)^(-1)`.

*Proof.*  The weighted Schur test applied to (180.12) gives
`||K_t||_(ell^2 to ell^2)<=a(t)` (rescale the atoms and coefficients first if
the chosen convention places the weights in the coefficient norm).  For a
stable finite representation of `f`,

\[
 \langle f,e^{-tH}f\rangle
 =\sum_{\alpha,\beta}\overline{c_\alpha}
   K_t(\alpha,\beta)c_\beta
 \le a(t)\|c\|_2^2
 \le\kappa^2a(t)\|f\|^2.
\tag{180.14}
\]

Density extends this to `Q cal H`.  The two conclusions now follow from
Theorems 180.1 and 180.2.  QED.

This theorem permits a Banach polymer norm only insofar as it proves the two
Hilbert-space statements (180.10) and (180.12).  Entrywise decay of each fixed
polymer, absolute convergence at one anchor, or density without the uniform
constant `kappa` does not suffice.

## Product rotors and general local Hamiltonians

For a product Hamiltonian

\[
 H_\Lambda=\sum_{x\in\Lambda}(h_x-e_x),\qquad
 \Omega_\Lambda=\bigotimes_{x\in\Lambda}\phi_x,
\tag{180.15}
\]

assume `phi_x` is the unique one-site ground state and
`h_x-e_x>=gamma_x(I-|phi_x><phi_x|)`.  Decompose the tensor product into the
orthogonal sectors whose finite set `X` records the excited sites.  These are
centered anchored polymer sectors, stable synthesis is orthogonal with
`kappa=1`, and the energy on every nonempty sector is at least
`sum_(x in X) gamma_x`.  Hence

\[
 H_\Lambda\upharpoonright Q_\Lambda\ge
 \min_{x\in\Lambda}\gamma_x.
\tag{180.16}
\]

For identical Mathieu rotors from Cycle 179 this gives the exact uniform lower
bound `gamma`.  The spectator vacua are factored out before the polymer label is
formed, so the vanishing all-low bare-Casimir weight `a_D^(|Lambda|-1)` never
appears.  This explains why the connected decomposition succeeds while the
global bare Fourier cube fails.  It does not prove an interacting Yang--Mills
cluster expansion.

For a general interacting local Hamiltonian, uniqueness and equal-time spatial
clustering still do not supply any hypothesis of Theorem 180.1 or 180.3.  For
example, on an infinite product of two-level sites let

\[
 H=\sum_x\varepsilon_x |1_x\rangle\langle1_x|,
 \qquad \varepsilon_x>0,\quad\inf_x\varepsilon_x=0.
\tag{180.17}
\]

The product vacuum is unique and connected correlations of disjoint local
observables vanish exactly, yet one-site excitations have energies tending to
zero.  Thus the gap is zero.  Every fixed local observable even has temporal
decay, but with a support-dependent exponent; precisely the uniformity and
stable full-complement control required above are absent.

## Exact assumptions needed in the Yang--Mills route

A usable lattice or OS argument must therefore establish, without presupposing
a gap:

1. a nonnegative vacuum-subtracted self-adjoint Hamiltonian and a unique vacuum,
   after Gauss' law and all transmitted sectors are removed;
2. cyclic completeness of centered local physical observables in the physical
   vacuum complement;
3. either the variance-normalized temporal estimate (180.4), the susceptibility
   estimate (180.7), or an anchored expansion proving both stable synthesis
   (180.10) and two-sided summability (180.12);
4. constants uniform in volume, boundary conditions, lattice spacing at the
   chosen physical scale, and every quotient used in the limit; and
5. a separate OS limiting argument that transports the resulting full
   quadratic-form bound and identifies the limiting vacuum complement.

The temporal exponent or susceptibility may be proved by a convergent polymer
expansion, Dobrushin-type influence estimate, block dynamics, or a direct
resolvent expansion.  It may not be assumed as an already-known bound on
`||Qe^{-tH}Q||`, since that is the desired gap in functional-calculus form.
Cycle 180 proves the abstract conversion and identifies the exact global bridge;
it does not establish these uniform hypotheses for four-dimensional quantum
Yang--Mills theory.  No Yang--Mills mass gap is claimed.
