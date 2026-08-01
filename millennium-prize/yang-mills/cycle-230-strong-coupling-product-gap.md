# Cycle 230: strong-coupling product gap before Gauss projection

This note isolates a rigorous volume-uniform strong-coupling theorem for the
Hamiltonian lattice gauge model. The useful architecture is not an overlapping
plaquette decomposition. It is the product electric Hamiltonian on link
Hilbert spaces, perturbed by bounded Wilson plaquette multipliers, followed by
restriction to the reducing Gauss-invariant space.

There are two levels of conclusion. Yarotsky's cluster expansion and later
Lie--Schwinger theorems cover the actual infinite-dimensional link spaces, but
their published hypotheses only produce an existential coupling threshold. A
standard finite-dimensional weak-interaction theorem gives an explicit,
conservative interval under stricter locality hypotheses. Thus the requested
explicit interval for the untruncated compact-group rotor is not obtained by
citing those theorems alone. Cycle 231 attempts a direct reconstruction for
square-lattice `SU(2)`, but hostile audit finds an invalid polymer count and
unquantified boundary and gap steps. It therefore supplies no numerical
endpoint.

## 1. Electric product Hamiltonian

Let `G` be a compact connected Lie group and let `rho` be a nonconstant unitary
representation of dimension `d_rho`. On a finite oriented hypercubic spatial
lattice `Lambda`, put

\[
 {\cal K}_\Lambda=\bigotimes_{e\in E(\Lambda)}L^2(G,dU_e),
 \qquad T_\Lambda=\sum_{e\in E(\Lambda)} C_e,              \tag{230.1}
\]

where `C_e=-Delta_e` is the positive bi-invariant Laplacian. Constants span the
kernel of one `C_e`. Let

\[
 c_G:=\min\{C_2(\pi):\pi\in\widehat G,\ \pi\ne\mathbf1\}>0. \tag{230.2}
\]

Peter--Weyl theory gives, with `Omega_Lambda=1`,

\[
 T_\Lambda\Omega_\Lambda=0,
 \qquad T_\Lambda\big|_{\Omega_\Lambda^\perp}\ge c_G.     \tag{230.3}
\]

This is an on-link product vacuum and a volume-independent electric gap. It is
not the two-plaquette floor `T>=3Q` of Cycle 228; it is the simpler bare-link
floor that a weak-interaction theorem needs.

For each spatial plaquette set

\[
 w_p(U)={1\over d_\rho}\operatorname{Re}\operatorname{Tr}
       \rho(U_{e_1}U_{e_2}U_{e_3}^{-1}U_{e_4}^{-1}),
 \qquad V_p=1-w_p.                                        \tag{230.4}
\]

Then `-1<=w_p<=1`, so

\[
                         0\le V_p\le2,\qquad \|V_p\|\le2. \tag{230.5}
\]

The dimensionless Kogut--Susskind Hamiltonian is

\[
 K_{\Lambda,\lambda}=T_\Lambda+\lambda\sum_pV_p,
 \qquad \lambda={2\over g^4}.                             \tag{230.6}
\]

The scalar in `V_p=1-w_p` is extensive but harmless: it shifts every energy by
the same `lambda |P(Lambda)|`. Weak-interaction theorems may instead use
`-w_p`, whose norm is one. No estimate below treats the norm of the full sum as
small.

## 2. Gauss projection is a reducing restriction

Let

\[
 P_\Lambda=\int_{G^{V(\Lambda)}}R(g)\,dg,
 \qquad {\cal H}_{\Lambda,\mathrm{phys}}=P_\Lambda{\cal K}_\Lambda. \tag{230.7}
\]

Both the electric Casimirs and traced plaquette multipliers commute with every
local gauge transformation. Hence

\[
 [K_{\Lambda,\lambda},P_\Lambda]=0,
 \qquad \Omega_\Lambda\in{\cal H}_{\Lambda,\mathrm{phys}}. \tag{230.8}
\]

The interacting ambient ground state is physical as well. On the connected
compact manifold `G^E`, the heat semigroup of `T_Lambda` plus a bounded real
potential is positivity improving. Its unique ground state can be chosen
strictly positive. A gauge transform is another normalized strictly positive
ground state, so uniqueness with the positive normalization makes it equal,
not merely equal up to phase. Haar averaging therefore fixes the ground state.

**Lemma 230.1 (restriction transfer).** Suppose a self-adjoint `K` commuting
with an orthogonal projector `P` has a unique normalized ground state `Omega`
in `ran P` and

\[
 K-E_0(K)\ge\gamma(I-|\Omega\rangle\langle\Omega|).        \tag{230.9}
\]

Then `K|_(ran P)` has the same ground energy, unique ground state, and gap at
least `gamma`.

**Proof.** The range of `P` reduces `K`; (230.9) can therefore be restricted to
`ran P`. Since `Omega` belongs to that range, the restricted spectral bottom is
`E_0(K)`, and equality can occur only on `span{Omega}`. QED.

Thus Gauss' law cannot decrease an already proved ambient gap. The physical
space need not tensor-factor, and no local physical quotient is used.

## 3. An explicit theorem with stricter hypotheses

Bravyi--DiVincenzo--Loss, Commun. Math. Phys. 284 (2008), Theorem 1, considers a
finite graph of qubits, an on-site product Hamiltonian of gap `Delta`, and
two-local edge perturbations of norm at most `J`. If the graph has maximum
degree `D`, it proves a unique ground state and gap at least `Delta/2` whenever

\[
 |\epsilon|\le {2^{-17}\Delta\over DJ}.                   \tag{230.10}
\]

Consequently, if a chosen finite-dimensional encoding realizes each Wilson
interaction as one bounded two-local edge term of norm `J<=1` on a graph of
degree `D_p`, then

\[
 |\lambda|\le {2^{-17}c_G\over D_p},
 \qquad \Delta_{\Lambda,\mathrm{phys}}(\lambda)\ge {c_G\over2}. \tag{230.11}
\]

This is explicit but is **not** directly a theorem for (230.6). A Wilson
plaquette is four-local on links, `L^2(G)` is infinite-dimensional, and an
arbitrary finite Peter--Weyl cutoff is not a qubit. A genuinely four-local
theorem needs its own hypergraph constant. Formula (230.11) is therefore an
encoding benchmark, not an interval for the untruncated gauge rotor.

## 4. What Yarotsky supplies

Yarotsky, Commun. Math. Phys. 261 (2006), considers a tensor product over sites,
possibly with infinite-dimensional one-site Hilbert spaces. His unperturbed
finite-range terms are diagonal in a product partition, have the product vector
as their nondegenerate local vacuum, and are normalized to have local gap one.
The perturbing local forms satisfy

\[
 |\phi_x(v,v)|\le\alpha\|h_x^{1/2}v\|^2+\beta\|v\|^2.     \tag{230.12}
\]

Theorem 1 asserts that sufficiently small positive `alpha,beta`, depending only
on dimension and interaction range, give a unique finite-volume ground state
and a positive volume-independent gap. Theorem 2 allows any `0<alpha<1` after
splitting the perturbation into a purely relatively bounded part and a bounded
part with

\[
 \|\phi_x^{(b)}\|\le
 \delta(\varkappa,\nu,\Lambda_0)(1-\alpha)^{\varkappa(\nu+1)},
 \qquad \varkappa>1.                                     \tag{230.13}
\]

For (230.6), first make the tensor-site bookkeeping literal. Assign every
positively oriented link leaving `x` to the unit-cell site `x`, whose one-site
space is

\[
 {\frak h}_x=\bigotimes_{i=1}^{d_s}L^2(G).                \tag{230.14}
\]

Choose one finite cell set `Lambda_0` containing all sites whose assigned links
occur in a plaquette based at the origin. Let `r` be the number of translates
`Lambda_0+x` containing a fixed assigned link, and define

\[
 h_x={1\over c_G}\sum_{e:\,\operatorname{cell}(e)\in\Lambda_0+x}C_e,
 \qquad \sum_xh_x={r\over c_G}T_\Lambda.                 \tag{230.15}
\]

Each `h_x` is diagonal in the Peter--Weyl product partition on
`frak h_(Lambda_0+x)`, has the constant vector as its unique local ground
state, and has local gap one. Let `Phi_x` be minus the sum of the normalized
Wilson multipliers for the finitely many oriented plaquette types based at
`x`. If their number is `s`, then `||Phi_x||<=s`, and, up to the scalar magnetic
shift,

\[
 {r\over c_G}K_{\Lambda,\lambda}
 =\sum_xh_x+{r\lambda\over c_G}\sum_x\Phi_x+\text{scalar}. \tag{230.16}
\]

There is no relatively bounded part, and each bounded perturbing form has norm
at most `rs|lambda|/c_G`. This is exactly a single-species `Z^(d_s)` tensor
system of the form used by Yarotsky, with infinite-dimensional separable
one-site space and one fixed interaction set. The theorem yields

\[
 \lambda_Y(G,\rho,d_s):={c_G\beta_Y(d_s,\Lambda_0)\over rs}>0,
 \quad |\lambda|<\lambda_Y
 \Longrightarrow
 \inf_\Lambda\Delta_{\Lambda,\mathrm{phys}}(\lambda)>0.  \tag{230.17}
\]

Here `beta_Y(d_s,Lambda_0)` denotes any bounded-part threshold supplied by
Yarotsky's Theorem 1 after the unit-gap normalization. This displays all gauge-
model constants `c_G,r,s`; the remaining theorem constant is existential.

Periodic boxes of sufficiently large side fit the theorem's convention. Open
boxes require the corresponding boundary version or a separate uniform
boundary audit. Lemma 230.1 then gives the physical statement.

The key boundary at the level of the printed theorem is quantitative: Yarotsky states existence of the admissible
`alpha,beta`, `delta`, and resulting gap. The proof chooses a time step and a
polymer smallness parameter and invokes standard cluster-expansion estimates;
it does not print a closed numerical `lambda_Y` or a closed numerical gap. Thus
(230.17) is rigorous and volume-uniform but **not by itself an explicit lambda
interval** in the requested sense. Reconstructing numbers requires fixing every
polymer-counting and convergence constant throughout the proof; citing the
theorem does not do it. Cycle 231 records an incomplete reconstruction attempt
in the square-lattice `SU(2)` specialization.

The later higher-dimensional Lie--Schwinger results of Del Vecchio--Froehlich--
Pizzo--Rossi make the same boundary clear. Their bounded theorem (J. Math.
Phys. 63, 073503 (2022)) assumes finite-dimensional on-site spaces. Their
unbounded theorem (arXiv:2108.13907) permits separable spaces and local form
bounds

\[
 |\langle\psi,V_X\psi\rangle|
 \le a_R\langle\psi,(H_X^0+1)\psi\rangle,                 \tag{230.18}
\]

and concludes gap at least `1/2` for `|t|<t_d`, uniformly in volume. But `t_d`
is only asserted to be sufficiently small, not evaluated numerically.

## 5. Frustration and theorem boundaries

This route bypasses Cycle 229's incompatible overlapping local vacua. The
reference terms are the commuting on-link electric Casimirs and have one common
product vacuum. Wilson plaquettes are perturbations; they are not required to
annihilate that vacuum or to share local interacting ground states. The
perturbed Hamiltonian is generally frustrated, but the perturbative theorem
constructs its dressed unique vacuum globally.

The exact conclusion and exclusions are:

1. **Rigorous qualitative lattice theorem.** For every fixed compact connected
   `G`, fixed Wilson representation, and fixed spatial dimension, there is a
   nonzero strong-coupling interval with a volume-uniform gap on the physical
   Hilbert space.
2. **No explicit untruncated interval from the cited theorem statements.**
   Their smallness thresholds are existential. Formula (230.11) is explicit
   only under the finite-dimensional, two-local encoding hypotheses stated
   there; Cycle 231's square-lattice `SU(2)` audit does not close the missing
   polymer-count, boundary, or gap constants.
3. **No direct elementary norm bound.** The total Wilson norm is extensive, so
   Weyl's inequality gives `c_G-O(|Lambda| lambda)`, not a uniform result. The
   linked-cluster or local block-diagonalization mechanism is essential.
4. **No need for frustration-free Wilson blocks.** The only frustration-free
   object is the electric reference product Hamiltonian.
5. **No continuum Yang--Mills consequence.** Strong coupling means
   `lambda=2/g^4` small. The asymptotically free continuum path has `g(a)->0`
   and `lambda->infinity`, outside this perturbative interval. OS tightness,
   reflection positivity, nontriviality, scale setting, and reconstruction are
   untouched.

Restoring dimensions, any dimensionless bound `gamma(lambda)` would read

\[
 \Delta_{\Lambda,\mathrm{phys}}(a,g)
 \ge {g^2\over2a}\gamma(2/g^4).                           \tag{230.19}
\]

Equation (230.19) is a fixed-lattice strong-coupling statement, not a positive
continuum mass in physical units.

## References checked

* D. A. Yarotsky, *Ground states in relatively bounded quantum perturbations of
  classical lattice systems*, Commun. Math. Phys. 261 (2006), 799--819,
  arXiv:math-ph/0412040.
* S. Bravyi, D. P. DiVincenzo, and D. Loss, *Polynomial-time algorithm for
  simulation of weakly interacting quantum spin systems*, Commun. Math. Phys.
  284 (2008), 481--507, arXiv:0707.1894.
* S. Del Vecchio, J. Froehlich, A. Pizzo, and S. Rossi, *Local iterative
  block-diagonalization of gapped Hamiltonians: a new tool in singular
  perturbation theory*, J. Math. Phys. 63 (2022), 073503,
  arXiv:2007.07667.
* S. Del Vecchio, J. Froehlich, and A. Pizzo, *Block-diagonalization of
  infinite-volume lattice Hamiltonians with unbounded interactions*,
  arXiv:2108.13907.
