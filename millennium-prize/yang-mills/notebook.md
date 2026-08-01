# Notebook

## Bounded scout cycle 226

Two adjacent `SU(2)` squares reduce by tree gauge fixing to
`L^2(SU(2)^2)^Ad`, with simultaneous rather than independent conjugation.  In
the normalized coupled basis `Phi_(ab)^c`, the seven-link electric operator is
exactly `3C_a+3C_b+C_c`; the shared-link spin `c` obstructs a tensor sum of the
one-plaquette Hamiltonians.  Its natural `a,b<=1/2` spin-cutoff compression has
dimension five and Ritz gap `3.141511514718...` at `lambda=1`; the tensor sum of
the corresponding two-state one-plaquette compressions has cutoff Ritz gap
`sqrt(10)=3.162277660168...`.  Here `sqrt(10)` is not the full one-plaquette
gap, which is approximately `3.11386381151`.  The finite matrices witness the
structural simultaneous-conjugation and `c`-sector obstruction, but give no
ordering or tensorization statement for untruncated gaps.  The verifier trusts
the displayed representation-theory reduction and recoupling entries and
certifies only the ensuing polynomial and spectral enclosures.  Full audit:
`cycle-226-two-plaquette-shared-link-gap.md`.

## Bounded scout cycle 181

The one-square `SU(2)` lattice reduces exactly by Gauss' law to the class space
`L^2(SU(2))^Ad`.  In its orthonormal character basis `e_n=chi_(n/2)`, the
dimensionless Kogut--Susskind block is the Jacobi matrix with diagonal
`n(n+2)+lambda` and neighboring entries `-lambda/2`.  Centering these atoms on
the interacting vacuum gives exact Gram matrix `I-aa*`; the temporal criterion
on every finite coherent synthesis is the largest generalized eigenvalue of
`M_I(t)c=q G_I c`.  For the half-line closure, the omitted tail obeys
`T_N>=(N+1)(N+3)`, while its boundary resolvent lies between the reciprocal of
its exact boundary diagonal minus `x` and the reciprocal tail floor minus `x`.
The resulting rank-one Schur complements and exact Sturm counts enclose `E_0`,
`E_1`, and the gap.  They certify `3` at `lambda=0` and a gap tightly around
`3.11386381151` at `lambda=1`.  This is a rigorous half-line toy benchmark, not
a volume-uniform or continuum Yang--Mills gap.  Full derivation:
`cycle-181-one-plaquette-atomic-gap.md`.

## Cycle 180 spectator norm

The incomplete tensor product over the dressed one-site vacuum gives the exact
spectator-free norm for product rotors. With `K=phi^perp`, it is unitarily
`direct-sum_(X finite) K^(tensor X)`; squared norms sum over actual excitation
supports, while every vacuum spectator contributes one. The normalized product
Hamiltonian is `direct-sum_X sum_(i in X)k_i`. A dressed one-site spectral tail
therefore contracts by `exp(-s Lambda_D)`, uniformly in volume, whether a high
excitation occurs anywhere or at a specified finite anchor. The shared-edge
`U(1)` loop quotient is unitarily the same construction. For an interacting
gauge vacuum, the GNS norm still removes identity spectators and a local-algebra
exhaustion gives an exact martingale decomposition, but support orthogonality and
dynamical tail invariance require the stable-synthesis/split estimate isolated
in the companion Cycle 180 work. Full derivation:
`cycle-180-dressed-vacuum-excitation-norm.md`. No Yang--Mills mass gap is
claimed.

## Cycle 180

The exact connected-correlation implication is now isolated.  If centered local
vectors are dense in the full vacuum complement and their imaginary-time
autocorrelations obey the volume-uniform physical-variance bound
`C_t(A,A)<=C exp(-m t) C_0(A,A)` for all finite local linear combinations, the
spectral theorem gives the full gap `H|_Q>=m`; no semigroup norm gap is assumed.
The integrated susceptibility bound `int C_t dt<=K C_0` instead gives gap
`K^(-1)`.  An anchored polymer estimate reaches these criteria only with a
uniform lower frame/stable-synthesis bound and two-sided Schur summability of
the connected temporal kernel.  Spatial clustering, fixed-polymer decay, or
density without the frame constant is insufficient.  Product rotors have the
orthogonal excitation-sector decomposition with frame constant one, whereas an
inhomogeneous product of two-level sites with excitation energies tending to
zero has a unique exactly clustered vacuum and zero gap.  Full theorem and
proof: `cycle-180-anchored-correlation-gap.md`.  No Yang--Mills mass gap is
claimed.  The companion hostile constructions in
`cycle-180-connected-local-control-no-go.md` exhibit invisible soft sectors and
rare delocalized excitations, reinforcing that equal-time local control alone
does not provide the required bridge.

## Hostile cycle 180

Connected local control does not by itself imply a full-complement gap. Two
finite-range qubit families make the failure exact. A product model with an
`exp(-N)` soft on-site sector has a unique product vacuum, zero connected
correlations, exact local ground-state tails, and gap `exp(-N)`. A less visible
model combines unit-coefficient nearest-neighbor swap-antisymmetry projections
with one unit boundary pin. Its unique product vacuum has the same perfect local
control, while the uniform one-particle trial state has energy `1/N`, forcing
the gap to zero; on every fixed `ell`-site region its reduced state is only
`2 ell/N` in trace norm from the vacuum. GHZ finite-volume states instead
fail clustering, while broken-symmetry or topological examples expose sector
selection. Therefore connected/polymer decay needs a separate finite-size,
local-gap, martingale/detectability, or coercive local-to-global theorem
covering all moving and global sectors. Full derivation:
`cycle-180-connected-local-control-no-go.md`. No Yang--Mills mass gap is
claimed.

## Hostile cycle 179

Ground-state conjugation does not itself prove locality: even a nearest-neighbor
harmonic Hamiltonian has drift kernel `A^(1/2)`, which is dense, and on the
physical gauge space all derivatives must remain horizontal while plaquette
coordinates obey Bianchi constraints.  More decisively, a fixed local Casimir
cube fails even when the transform is exactly local.  For `N` product Mathieu
rotors with dressed one-site vacuum `phi`, let `a_D=||p_D phi||^2<1` and cut off
every site's Fourier degree by `D`.  A first excited rotor tensored with `N-1`
dressed vacua can be corrected into the exact Casimir tail and converges back to
that one-particle state because the all-low spectator weight is `a_D^(N-1)`.
Hence `liminf_N ||S_N(s)(I-Pi_(D,N))|| >= exp(-s gamma)` for every finite `D`.
The same model is realized on the gauge quotient of `N` loops sharing one
reference edge, so plaquette overlap and Gauss invariance do not repair it.
Global bare local-Casimir tails are retired; only anchored connected/polymer
norms or ground-state-adapted local spectral sectors remain possible.  Full
derivation: `cycle-179-local-ground-transform-no-go.md`.  No Yang--Mills mass
gap is claimed.

## Bounded scout cycle 178

The proposed Wilson representation low/tail split fails before continuum
passage if its tail norm is unweighted.  In the one-plaquette `SU(2)` physical
class space, `w=chi_(1/2)/2` satisfies
`w chi_j=(chi_(j+1/2)+chi_(j-1/2))/2`; hence for every representation cutoff
`Pi_J`, the gauge-invariant escaping state `chi_(J+1/2)` obeys
`||Pi_J w(I-Pi_J)||>=1/2`.  Closed plaquette spin networks survive Gauss'
quotient, and disjoint plaquettes force HS cost at least `sqrt(K)/2` for `K`
channels.  Weak-coupling magnetic coefficients multiply rather than remove the
constant.  A live tail estimate must include ordering-sensitive electric
Casimir smoothing.  On the boundary state, a symmetrically heat-damped magnetic
term still costs at least
`(lambda_beta/2) exp[-t{J(J+1)+(J+1/2)(J+3/2)}/2]`, forcing
`tJ^2 >= log(lambda_beta)+O(1)` merely to keep this channel bounded.  Full
derivation: `cycle-178-wilson-low-tail-adversary.md`.

The complementary ordered-semigroup calculation makes the surviving finite
theorem exact. For `K_lambda=C+lambda W`, `W>=0`, let `P_D=1_[0,D](C)` and let
`Pi_D` project in the interacting-vacuum complement onto `Q P_D H`. Its exact
orthogonal tail is `QH intersect ker(P_D)`, not the range of `Q(I-P_D)Q`.
Duhamel ordering then gives
`||S_s(I-Pi_D)||<=exp(sE_0)[exp(-s Lambda_D)+
(lambda||W||/Lambda_D)(1-exp(-s Lambda_D))]`. Together with the whole-low-block
bound `||S_s Pi_D||<=q_D`, this yields
`||S_s||<=sqrt(q_D^2+R_D^2)` and an explicit finite-lattice gap. The criterion
is uniform over volumes if uniform `q_D,R_D` exist, but the displayed proof
does not furnish them: `||W||` and `E_0` are extensive and fixed total degree
misses the dressed volume vacuum. Linked-cluster vacuum renormalization and a
local connected tail estimate remain necessary, and `lambda=2/g^4` becomes
large on the asymptotically free continuum path. Full derivation:
`cycle-178-electric-casimir-tail.md`. No Yang--Mills mass gap is claimed.

## Bounded scout cycle 174

Wilson-loop contraction plus qualitative density cannot form an intermediate
mass-gap criterion.  The exact atomic version is: if every normalized Wilson
generator obeys `||Sw_alpha||<=rho` and each `f` has an approximant
`g=sum c_alpha w_alpha` with error `epsilon||f||` and coefficient cost
`sum|c_alpha|<=A||f||`, then `||S||<=epsilon+rho A`.  Coefficient control is
essential: two individually contracted generators can span an uncontracted
eigenvector by coherent addition.  Contraction on an entire Wilson trial space
and relative approximation error `epsilon` instead gives
`||S||<=q+(1+q)epsilon`; but a proper linear trial subspace has worst-case
relative error exactly one.  A second structured checkpoint must separately
prove low-complexity contraction
`||S Pi_M||<=q_M` and moving-tail control
`||S(I-Pi_M)||<=r_M`, with `q_M^2+r_M^2<1`.  The escaping-vector model shows
that fixed-loop density or pointwise approximation cannot replace the tail
bound.  Full derivation: `cycle-174-wilson-atomic-approximation-wall.md`.

## Bounded scout cycle 83

Exact straight-link pushforward blocking is gauge-equivariant and reflection
positive, and the Wilson `SU(2)` character coefficients and tails are explicit.
In four dimensions the exact induced action nevertheless occupies an infinite
loop/polymer/intertwiner Banach space. A two-channel common-cone matrix neither
controls that tail nor the full physical Hilbert complement, and a UV-normalized
positive Lyapunov functional is perturbatively obstructed. Uniform Banach-tail
closure, weak-to-strong basin entry, OS compactness/nontriviality, and physical
completeness remain missing. No Yang--Mills result is claimed.

Bounded scout is queued to verify the spectral-theorem implication with all
ceilings and limit quantifiers, and to distinguish full-operator contraction
from finite variational subspace measurements.

## Bounded scout tick 2

If the full physical transfer operator obeys
`<f,T^ceil(r0/a)f> <= q||f||^2` on the vacuum complement, positivity and the
spectral theorem give a finite-cutoff gap
`log(1/q)/(a ceil(r0/a))`, tending to `log(1/q)/r0`. Passage to the continuum
requires convergence of these rounded-time quadratic forms on a dense set of
vacuum-orthogonal states. Fixed-time correlator convergence, finite trial-space
contraction, or a merely nontrivial OS limit does not suffice.

## Bounded scout cycle 36

Escaping spectral states give an exact obstruction to trial-space or
pointwise-correlator evidence.  Let the vacuum complement be `ell^2(N)`, fix
`0<q<1`, and define positive contractions

`T_n=q I+(1-q) P_(e_n)`.

For every fixed finite coordinate trial space, `T_n` eventually restricts to
`q I`.  For every fixed `f in ell^2`,

`<f,T_n f>=q||f||^2+(1-q)|f_n|^2 -> q||f||^2`.

Nevertheless `T_n e_n=e_n`, so every cutoff has spectral radius one on the
vacuum complement and zero transfer-Hamiltonian gap.  Pointwise convergence of
all fixed correlators, even with eventual contraction on every fixed trial
space, cannot replace a uniform full-complement estimate controlling states
that escape with the cutoff.

## Bounded scout cycle 39

The same escaping-state example defeats even strong operator convergence.  For
`T_n=qI+(1-q)P_(e_n)` and every fixed `f in ell^2(N)`,

`||(T_n-qI)f||=(1-q)|f_n| -> 0`.

Thus `T_n -> qI` in the strong operator topology, not merely through quadratic
forms.  Nevertheless `T_n e_n=e_n` and `||T_n||=1` for every `n`, so every
cutoff transfer Hamiltonian still has zero gap.  A strongly convergent,
strictly contractive continuum transfer operator does not by itself yield the
uniform full-complement estimate required before taking the limit.

## Bounded scout cycle 41

Escaping states survive convergence at every fixed integer Euclidean time, not
only at one transfer step.  For `T_n=qI+(1-q)P_(e_n)` and every `k>=1`,

`T_n^k=q^kI+(1-q^k)P_(e_n)`.

Thus `T_n^k -> q^kI` strongly for each fixed `k`, so all fixed-state
integer-time correlators converge with exponential factor `q^k`.  Yet
`T_n^k e_n=e_n` and `||T_n^k||=1` for every cutoff and every `k`; the cutoff
transfer Hamiltonian still has zero gap.  Simultaneous strong convergence of
all fixed transfer powers is therefore insufficient without a uniform
full-vacuum-complement bound.

## Bounded scout cycle 42

The escaping-state example survives the whole fixed continuous functional
calculus. For every bounded continuous `f:[0,1]->C`,

`f(T_n)=f(q)I+(f(1)-f(q))P_(e_n) -> f(q)I`

strongly. Yet every `T_n` retains eigenvalue one, norm one, and zero
transfer-Hamiltonian gap. Thus even strong convergence of all fixed continuous
spectral observables cannot replace cutoff-uniform control of the moving
spectral edge.

## Bounded scout cycle 43

The same example defeats the entire fixed bounded Borel calculus. For
`T_n=qI+(1-q)P_(e_n)` and any fixed bounded Borel function `phi` on `[0,1]`,

\[
\phi(T_n)=\phi(q)I+(\phi(1)-\phi(q))P_{e_n}
\longrightarrow \phi(q)I
\]

strongly, because the `n`th coordinate of every fixed `ell^2` vector tends to
zero. This includes the endpoint projection
`1_{\{1\}}(T_n)=P_(e_n)->0` strongly. Yet every `T_n` retains eigenvalue one
and zero transfer-Hamiltonian gap. Hence even convergence of all fixed bounded
Borel spectral observables misses a moving edge state; cutoff-uniform norm
control is indispensable. This abstract no-go neither constructs Yang--Mills
theory nor proves a mass gap.

## Bounded scout cycle 50

If resolvents `(H_n+1)^(-1)` converge strongly and form a collectively compact
family, self-adjointness upgrades convergence to operator norm. Norm-resolvent
convergence is equivalent, for nonnegative self-adjoint operators, to norm
convergence of `exp(-tH_n)` at any one fixed `t>0`, and transfers the lower
spectral edge. Collective compactness is sufficient but not necessary. No
Yang--Mills cutoff is shown to satisfy these hypotheses, so no mass gap is
proved.

## Bounded scout cycle 46

Norm-resolvent convergence is strong enough to exclude the escaping-edge
example. If nonnegative self-adjoint vacuum-complement Hamiltonians satisfy
`||(H_n+1)^(-1)-(H+1)^(-1)||->0`, then

\[
{1\over1+\inf\sigma(H_n)}=\|(H_n+1)^{-1}\|
\longrightarrow\|(H+1)^{-1}\|={1\over1+\inf\sigma(H)},
\]

so their spectral edges converge. A limiting bound `H>=mI` therefore gives
`H_n>=(m-epsilon)I` eventually, and fixed-time transfer norms converge. The
vacuum sectors must first be consistently removed and identified. This is only
an abstract sufficient topology; no Yang--Mills construction, convergence, or
mass gap is proved.

## Bounded scout cycle 59

Strong resolvent convergence transfers the gap exactly when resolvent norms
converge. Collective compactness or positive trace convergence suffices;
individual compactness and a uniform trace bound do not, by an escaping
eigenvalue counterexample. No Yang--Mills cutoff is shown to satisfy the
sufficient hypotheses, so no mass gap is proved.

## Bounded scout cycle 63

Collective compactness of cutoff resolvents is equivalent to uniform spatial
tightness of every bounded-energy spectral projector relative to one fixed
finite-rank exhaustion. Under a uniform high-energy heat-tail bound, this is
equivalent to spatial heat-trace tightness. Scalar heat-trace bounds alone fail:
an escaping zero-energy eigenvector preserves uniform traces and strong
resolvent convergence while destroying collective compactness. No Yang--Mills
cutoff is shown to satisfy spatial tightness, so no mass gap is proved.
