# Cycle 180: dressed-vacuum excitation norm and spectator quotient

Cycle 179 shows that a bare local Fourier cube counts the Fourier tails of all
dressed-vacuum spectators and therefore sends a fixed one-particle state into
the global tail as the volume grows. This note gives the exact replacement in
the product-rotor model. The replacement is the incomplete tensor product, or
equivalently the GNS space of local excitations over the dressed product
vacuum. Vacuum spectators then have norm one and carry no cutoff label.

The construction gives an exact isometry and an exact local spectral-tail
contraction for product rotors. It also identifies what survives after the
Gauss quotient and which additional statement would be needed for an
interacting Yang--Mills vacuum. No Yang--Mills mass gap is claimed.

## Product-vacuum local excitation space

Let `H_1` be a separable Hilbert space, let `phi` be a unit vector, and set

\[
 E=|\phi\rangle\langle\phi|,\qquad R=I-E,\qquad
 K=R{\cal H}_1.
\tag{180.1}
\]

For a finite set `Lambda`, put `H_Lambda=H_1^(tensor Lambda)`. If
`Lambda` is contained in `Lambda'`, use the dressed-vacuum embedding

\[
 J_{\Lambda,\Lambda'}v
   =v\otimes\phi^{\otimes(\Lambda'\setminus\Lambda)}.
\tag{180.2}
\]

These maps are isometries. Their Hilbert inductive limit is the incomplete
tensor product `H_phi`. It is also the GNS Hilbert space of the quasi-local
matrix algebra in the product state
`omega_phi(A)=<phi^(tensor Lambda),A phi^(tensor Lambda)>`: a local operator
`A` represents the vector `[A]=A Omega`, and adjoining identity operators on
spectator sites does not change either the vector or its norm.

Let `P_fin(I)` denote the finite subsets of the infinite site set `I`, and
define the labeled Fock-like space

\[
 {\cal F}_{\rm loc}(K)
   =\bigoplus_{X\in{\cal P}_{\rm fin}(I)}K^{\otimes X},
 \qquad K^{\otimes\varnothing}=\mathbb C.
\tag{180.3}
\]

This is not bosonic or fermionic Fock space: sites label the tensor factors, so
there is no symmetrization.

**Proposition 180.1 (exact spectator isometry).** There is a unitary

\[
 U:{\cal F}_{\rm loc}(K)\longrightarrow{\cal H}_\phi
\tag{180.4}
\]

which sends `otimes_(i in X) k_i` to the incomplete tensor having entry `k_i`
at `i in X` and entry `phi` at every spectator site. In particular,

\[
 \left\|U(c_X)_{X}\right\|^2
   =\sum_{X\in{\cal P}_{\rm fin}(I)}\|c_X\|^2.
\tag{180.5}
\]

To prove this, first work in a finite `Lambda`. Expanding
`H_1=C phi direct-sum K` gives the orthogonal identity

\[
 {\cal H}_\Lambda
 =\widehat\bigoplus_{X\subseteq\Lambda}
   K^{\otimes X}\otimes\phi^{\otimes(\Lambda\setminus X)}.
\tag{180.6}
\]

The embedding (180.2) preserves every already present summand and introduces
no new excitation. Passing to the inductive-limit completion proves (180.4)
and (180.5). Surjectivity follows because finite tensors are dense in the
incomplete tensor product.

There is also a useful coefficient formula. For `v in H_A`, where `A` is
finite, define

\[
 v_X=\left(\bigotimes_{i\in X}R_i\right)
     \left(\bigotimes_{j\in A\setminus X}E_j\right)v,
 \qquad X\subseteq A.
\tag{180.7}
\]

After deleting the displayed `phi` factors, `v_X` is an element of
`K^(tensor X)`, and

\[
 v=\sum_{X\subseteq A}v_X,\qquad
 \|v\|^2=\sum_{X\subseteq A}\|v_X\|^2.
\tag{180.8}
\]

Thus (180.8), rather than a bare Fourier cube on every site in the volume, is
the desired norm/decomposition. A local excitation pays only for its actual
support `X`; an arbitrary number of dressed spectators contributes the exact
factor one.

## Exact product dynamics

Let `h` be self-adjoint and bounded below on `H_1`, suppose

\[
 h\phi=e_0\phi,
 \qquad k=(h-e_0)|_K\ge\gamma I_K
\tag{180.9}
\]

for some `gamma>0`, and let `H_Lambda=sum_(i in Lambda)h_i`. Since the ground
line and its orthogonal complement reduce `h`, Proposition 180.1 intertwines
the vacuum-normalized product Hamiltonian with

\[
 U^*(H-e_0|\Lambda|)U
 =\widehat\bigoplus_{X\subseteq\Lambda}
   \sum_{i\in X}k_i.
\tag{180.10}
\]

The compatible vacuum-normalized finite-volume semigroups induce a positive
GNS generator `L` on `H_phi`; (180.10) holds for `L` on the inductive-limit
core and then by closure. It immediately gives

\[
 \left.e^{-s(H-e_0|\Lambda|)}\right|_{X}
 =\bigotimes_{i\in X}e^{-sk_i},
 \qquad
 \|e^{-s(H-e_0|\Lambda|)}Q_\Omega\|\le e^{-s\gamma}.
\tag{180.11}
\]

Equality holds in the last bound when `gamma=inf sigma(k)`. Unlike the Cycle
179 bare cube, (180.11) has no volume-dependent vacuum-energy factor and no
spectator tail.

## Local spectral tail

Choose a one-site *dressed* spectral cutoff

\[
 r_D={\bf1}_{[0,D]}(k),\qquad t_D=I_K-r_D,
 \qquad
 \Lambda_D=\inf\sigma(k|_{t_DK}).
\tag{180.12}
\]

Empty tails are assigned `Lambda_D=+infinity`. In the summand indexed by `X`,
expand every `K=r_DK direct-sum t_DK`. Let `T_D` be the orthogonal sum of the
components containing at least one `t_DK` factor. Equivalently, `T_D` is the
closed span of finite-excitation vectors having a high dressed excitation at
some occupied site. Vacuum factors are not tested by `r_D` or `t_D`.

**Proposition 180.2 (exact local-tail contraction).** For every `s>=0`,

\[
 \|e^{-sL}P_{T_D}\|\le e^{-s\Lambda_D}.
\tag{180.13}
\]

For a finite anchor `A`, the same estimate holds for the subspace `T_(D,A)` in
which at least one high excitation occurs at a site of `A`, irrespective of
the low excitations outside `A`:

\[
 \|e^{-sL}P_{T_{D,A}}\|\le e^{-s\Lambda_D}.
\tag{180.14}
\]

Indeed, all one-site spectral projections in (180.12) commute with `k`. On
each refined tensor summand containing a high factor, (180.10) is bounded below
by `Lambda_D`; every other occupied factor is nonnegative. The spectral
theorem proves (180.13)--(180.14), with equality in (180.13) whenever the
one-particle high sector has spectral bottom `Lambda_D`. If `k` has compact
resolvent, then `Lambda_D` tends to infinity and the tail contracts to zero for
each fixed positive `s`, uniformly in the number of spectators.

For the Mathieu rotor of Cycle 179, take `H_1=L^2(S^1)`, use its positive
ground state `phi`, and use spectral projectors of `h-e_0` on `K`, not Fourier
projectors on the original `L^2(S^1)`. The state
`psi tensor phi^(tensor(N-1))` then lies exactly in the singleton sector
`X={1}` for every `N`. Its norm and cutoff classification are independent of
`N`; the factor `a_D^(N-1)` never appears. This pinpoints the distinction
between a dressed-excitation tail and the disproved bare-Casimir cube.

The result does not by itself prove a product gap without the one-site input
`gamma>0`; in this test model that input is already the complete gap theorem.
Its value is narrower: it proves that the proposed norm removes the spectator
obstruction exactly and that its local high tail has the desired
volume-independent heat contraction.

## Gauge extension

The overlapping `U(1)` loop model in Cycle 179 inherits the construction
without modification. On the two-vertex graph with parallel edges
`e_0,e_1,...,e_N`, the gauge-invariant coordinates

\[
 y_i=\theta_i-\theta_0
\tag{180.15}
\]

identify the physical quotient, with its quotient Haar measure, unitarily with
`L^2((S^1)^N)`. Under this unitary, the loop Hamiltonian (179.7), its product
ground state, the excitation decomposition (180.6), and the tail estimates
(180.13)--(180.14) are identical. Thus the spectator quotient is compatible
with Gauss invariance and overlapping loops in this exact gauge model.

For a general compact gauge group, fixing a maximal tree leaves independent
loop holonomies with a residual simultaneous conjugation. Products of
one-loop class functions form a gauge-invariant closed product subspace, and a
product class-function vacuum gives the same isometry there. The full physical
space is larger: intertwiners, residual conjugation, Bianchi relations, and the
electric metric generally couple the loop variables. Consequently the product
proof cannot simply be asserted on the whole Yang--Mills Hilbert space.

The coordinate-free candidate is nevertheless clear. Let `A_loc^G` be the
quasi-local gauge-invariant observable algebra and let `omega` be the
interacting vacuum state. Its GNS space is

\[
 {\cal H}_\omega
 =\overline{{\cal A}_{\rm loc}^G/{\cal N}_\omega},
 \qquad
 \|[A]\|_\omega^2=\omega(A^*A),
 \qquad [A]=[A\,1_{\rm spectator}].
\tag{180.16}
\]

Equation (180.16) always factors identity spectators. For a nested exhaustion
`A_1 subset A_2 subset ...`, let `H_n` be the closure of
`{[A]:A in A_n^G}`. Orthogonal projection gives the exact, but
ordering-dependent, martingale decomposition

\[
 {\cal H}_\omega
 =\mathbb C\Omega\ \widehat\oplus\
   \widehat\bigoplus_{n\ge1}(H_n\ominus H_{n-1}),
\tag{180.17}
\]

after taking `H_0=C Omega` and deleting zero increments. This is a valid GNS
local-excitation norm after Gauss' law and does not count remote identity
spectators.

What is missing is precisely the interacting analogue of (180.10)--(180.14):
vacuum-preserving, gauge-invariant local conditional expectations or spectral
sectors whose increments have a volume-uniform energy lower bound and whose
high tail exhausts the full GNS vacuum complement. In an interacting state,
disjoint local algebras are correlated, so the support-indexed summands in
(180.6) are not orthogonal, and the Hamiltonian need not preserve the
martingale increments in (180.17). Proving a split/cluster estimate strong
enough to control these two failures is the gauge-extension lemma; it is not a
formal consequence of the GNS construction.

Cycle 180 therefore resolves the spectator-norm design exactly for product
rotors and for their exact `U(1)` gauge realization. It reduces the genuine
Yang--Mills step to a concrete proposition about the interacting physical
vacuum: construct gauge-local excitation sectors, quasi-orthogonal uniformly
in volume, and prove an analogue of the dressed spectral-tail bound (180.14)
on their complete GNS sum.
