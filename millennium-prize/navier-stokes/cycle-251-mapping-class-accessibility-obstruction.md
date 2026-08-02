# Cycle 251: mapping-class obstruction to the Cycle 250 endpoints

## Verdict: CERTIFIED FIXED PAIRS REJECTED, REPLACEMENTS GATED

Every Cycle 250 instance passing the finite Morse/essential-contour certificate
below is not joined by a smooth Euler orbit in either direction.
This conclusion is stronger than observing that its displayed toral
automorphism is not a flow map: no area-preserving endpoint map isotopic to the
identity can transport these two fixed endpoint functions. In particular, one
cannot repair this fixed pair by replacing `B_N^-1` with a Hamiltonian map that
has exactly the same pullback on `omega_0`.

The obstruction is finite and topological. It uses the mapping class forced on
the stabilizer of the initial vorticity. It is independent of all vorticity
Casimirs and kinetic energy, which the pair was constructed to match.

This does not reject a different nearby endpoint produced by a Hamiltonian map.
Cycle 251's weak-density construction changes the transported function on a
small set and retunes its amplitude, so the stabilizer argument below does not
apply to that new pair. Such replacements face the separate circulation gate
derived below.

## Euler flow maps are Hamiltonian here

On the oriented torus write the velocity as

\[
 u=K\omega=\nabla^\perp\Delta^{-1}\omega.
\]

Its spatial mean is zero and contraction with the area form is the exact
one-form `d Delta^-1 omega`, up to the fixed sign convention. Consequently the
Lagrangian flow of this velocity is a Hamiltonian isotopy. In particular, at
every finite time its endpoint `eta_T` has trivial mapping class:

\[
 [\eta_T]=I\quad\hbox{in }\operatorname{SL}(2,\mathbb Z).       \tag{251.1}
\]

This is stricter than orientation and area preservation.

## Stabilizer lemma

Let `f:T^2 -> R` be a Morse function having an essential regular level
component. If a diffeomorphism `s` satisfies `f o s=f`, then the mapping class
`[s]` is not hyperbolic.

Indeed, choose a regular value and collect the finitely many essential
components of that level. The map `s` permutes them. Some positive power `s^m`
therefore fixes the unoriented primitive homology class `+/-h` of one such
component. Thus

\[
 [s]^m h=\pm h.                                         \tag{251.2}
\]

A hyperbolic matrix in `SL(2,Z)` has no nonzero integral vector periodic up to
sign: (251.2) would give an eigenvalue `+1` or `-1` for a positive power,
whereas its eigenvalues have moduli different from one. This proves the lemma.

For a simple Morse function on `T^2`, an essential regular component exists;
equivalently, its Reeb graph contains the handle cycle. For the Cycle 250
separable analytic profile this can instead be certified directly: in the
unimodular coordinates

\[
 r=x,\qquad s=-Nx+y,
\]

one has

\[
 \omega_0(r,s)=F_\varepsilon'(r)+t_*\cos s.             \tag{251.3}
\]

Its critical equations and Hessian are

\[
 F_\varepsilon''(r)=0,\quad \sin s=0,\qquad
 \operatorname{Hess}\omega_0=
 \operatorname{diag}(F_\varepsilon'''(r),-t_*\cos s).  \tag{251.4}
\]

Thus a finite directed root-isolation certificate showing that every zero of
`F_epsilon''` is simple, followed by one regular essential contour witness,
is enough for the lemma. The Cycle 250 existence choice must be restricted to
such a certified `epsilon`. Without this certificate the static construction
remains kinematic, but the present rejection is not yet a certificate for that
particular parameter; no genericity assertion substitutes for root isolation.

## Application to the endpoint pair

Cycle 250 proves

\[
 \omega_1=\omega_0\circ B_N,
 \qquad
 B_N=\begin{pmatrix}1&N\\N&N^2+1\end{pmatrix},
 \qquad N\geq1.                                       \tag{251.5}
\]

Suppose an endpoint map `eta`, isotopic to the identity, transported the same
pair:

\[
 \omega_1=\omega_0\circ\eta^{-1}.                     \tag{251.6}
\]

Composing (251.5)--(251.6) on the right by `eta` gives

\[
 \omega_0\circ s=\omega_0,
 \qquad s=B_N\circ\eta.                               \tag{251.7}
\]

Hence `s` belongs to the stabilizer of `omega_0`, while

\[
 [s]=B_N,
 \qquad \operatorname{tr}B_N=N^2+2>2.                 \tag{251.8}
\]

The matrix `B_N` is hyperbolic, contradicting the stabilizer lemma. The reverse
transport forces `B_N^-1` and is rejected identically. Therefore, after the
finite Morse/essential-contour certificate in (251.4),

\[
 \boxed{\text{the certified Cycle 250 endpoint pair is not Euler accessible.}} \tag{251.9}
\]

## Kelvin--Reeb circulation invariant

Let `alpha=u^flat` be the velocity one-form. Smooth Euler gives

\[
 \partial_t\alpha+\mathcal L_u\alpha=-d\Pi             \tag{251.10}
\]

for a scalar `Pi`. If `eta_t` is the Lagrangian map, integration around any
closed material curve `C_t=eta_t(C_0)` yields Kelvin's exact invariant

\[
 \oint_{C_t}\alpha_t=\oint_{C_0}\alpha_0.              \tag{251.11}
\]

For a Morse vorticity, regular level components are material curves. Therefore
an Euler endpoint correspondence induces an isomorphism of measured Reeb
graphs that preserves not only the vorticity value and pushed-forward area
measure but also the circulation function

\[
 c_i(x)=\oint_{\pi_i^{-1}(x)}(K\omega_i)^\flat          \tag{251.12}
\]

on every regular Reeb edge, with the standard Kirchhoff compatibility at
vertices. It must also preserve the circulation periods on a chosen homology
basis, equivalently the harmonic/impulse datum once conventions are fixed.
Equations (251.11)--(251.12) are strictly stronger than Casimirs and energy.

Thus any explicit Hamiltonian-isotopic replacement must print a graph
isomorphism and prove `c_1 o g=c_0` by directed integration. A mismatch at one
rationally isolated regular level is a finite exact rejection witness. The
weak-density Hamiltonian construction controls only finite `L^p` observables;
it does not control these contour integrals and therefore does not pass this
gate automatically.

Even exact circulation and impulse matching classify the relevant coadjoint
data, not the orbit of the Euler energy Hamiltonian inside that data. They are
necessary, not sufficient. No exact invariant presently derived here excludes
every possible Hamiltonian replacement. If all static invariants match, the
remaining honest alternatives are a uniqueness theorem for the self-induced
initial-value problem that identifies its endpoint, or a rigorous enclosure of
that unique solution showing that the proposed endpoint is absent.

## Why the other exact invariants do not decide the fixed pair

- The measured Reeb graphs of the two vorticities are isomorphic because
  `B_N` itself conjugates their level sets and preserves area.
- Every ordinary vorticity Casimir agrees by the same change of variables.
- The kinetic energies agree by the amplitude tuning in Cycle 250.
- The toral impulse, interpreted as the harmonic/mean-velocity component, is
  zero at both endpoints because Biot--Savart produces mean-zero velocity.
- Circulation on the measured Reeb graph can reject other static pairs, but it
  is unnecessary for the fixed Cycle 250 pair: the mapping-class stabilizer
  obstruction already excludes every identity-isotopic correspondence.

Thus matching energy, Casimirs, measured Reeb data, and impulse would still not
repair the Cycle 250 pair.

## Sharpened finite admission gate

For a static pair `omega_1=omega_0 o A` on `T^2`, do not proceed directly from
energy and Casimirs to a path residual. Require the following finite packet.

1. Certify the endpoint identity, all claimed scalar invariants, and the
   mapping class `A in SL(2,Z)` exactly.
2. Certify that `omega_0` is Morse and exhibit one essential regular level
   component. Record the finite set `H(omega_0)` of its primitive unoriented
   homology labels at one or more separating regular values.
3. Reject if `A` cannot permute the corresponding finite labelled contour
   sets. In particular, reject immediately when `|tr A|>2`, since a hyperbolic
   class cannot preserve any nonempty finite set of primitive homology labels.
4. Only for survivors compare harmonic impulse and the circulation function
   (251.12) on an explicitly matched measured Reeb graph. Reject on one
   directed interval separating the two circulation values.
5. Only after all coadjoint and identity-component tests pass enclose the unique
   Euler solution from `omega_0` and prove that its endpoint equals the target,
   equivalently supply a zero-residual self-induced Lagrangian path. Passing
   items 1--4 remains necessary, not sufficient.

For the same fixed endpoint functions, changing the conjugating map by an
identity-class map leaves the forced stabilizer class `A`, so the Cycle 250
pair fails item 3 exactly. A replacement that changes the endpoint function,
as in the separate Hamiltonian weak-density construction, starts again at item
1 and must pass item 4 rather than inheriting the rejection. No Euler orbit,
Navier--Stokes counterexample, regularity result, or Millennium solution is
claimed.
