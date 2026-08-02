# Cycle 264: exact midpoint--tail--Picard interface

## Decision

`C263-MG1` can supply the nominal retained trajectory for a Cycle 255 Euler
certificate, but an ordinary or interval-validated midpoint step is not by
itself an enclosure of the full PDE flow. The rigorous bridge is a recentered
interval Picard argument around the piecewise-affine midpoint trajectory,
driven by the Cycle 255 omitted-convolution boxes. In this bridge midpoint is
part of the certified reference path and its algebraic defects may be replayed
exactly; the proof of containment still comes from the full-PDE tail lemma and
the Picard inclusions.

This design freezes the interface `C264-MG255-IE1`. It does not select a new
family, rerun the retired Cycle 258 data, or claim an Euler `L^3` crossing.

## 1. Common equation and projections

Use normalized Haar measure on `(R/2pi Z)^2`, zero mean,
`omega_-k=conj(omega_k)`, `k^perp=(k_2,-k_1)`, and

\[
 \dot\omega_k=F(\omega)_k=
 \sum_{p+r=k}{p^\perp\cdot r\over |p|_2^2}\omega_p\omega_r.
 \tag{264.1}
\]

For `S_N={k:0<|k|_infinity<=N}`, write the exact retained equation as

\[
 \dot x=F_N(x)+r,\qquad
 F_N(x)=P_NF(x),\qquad r=P_NF(\omega)-F_N(P_N\omega).
 \tag{264.2}
\]

The production `F_N` is the C263 direct ordered convolution. A padded
`4N+1` replay is an implementation cross-check only. For each slab the Cycle
255 analytic bound supplies a box `R_j` containing every possible `r(t)` in
(264.2); no projected Galerkin trajectory is used as a tail estimate.

Choose exact rational `q0,M,alpha,T` with

\[
 q(t)=q_0(1-\alpha t),\quad A_{q_0}(\omega_0)\le M,
 \quad\alpha\ge M,\quad q(T)>1.                         \tag{264.3}
\]

The Cycle 255 lemma then gives, independently of all midpoint calculations,

\[
 A_{q(t)}(\omega(t))\le M,\qquad
 z_n(t)\le Mq(t)^{-n}.                                  \tag{264.4}
\]

On `I_j=[t_j,t_j+h_j]`, the verifier uses the smaller slab-end weight
`q_(j+1)=q(t_j+h_j)` in every omitted-convolution sum.

## 2. Midpoint reference path

The floating C263 solve generates candidate nodes `y_j`. Before certification,
every node is rounded to an explicitly stored rational complex vector obeying
Fourier reality. Candidate generation solves approximately

\[
 m_j={y_j+y_{j+1}\over2},\qquad
 \delta_j=y_{j+1}-y_j-h_jF_N(m_j).                      \tag{264.5}
\]

The certificate does not assert `delta_j=0`. The verifier recomputes an
outward interval for it. Define the exact rational affine reference

\[
 c_j(s)=y_j+s v_j,\qquad
 v_j={y_{j+1}-y_j\over h_j},\qquad 0\le s\le h_j.       \tag{264.6}
\]

Thus `c_j(h_j/2)=m_j` and

\[
 v_j-F_N(m_j)={\delta_j\over h_j}.                      \tag{264.7}
\]

Equation (264.7) makes the nonlinear-solve defect visible, but the continuous
defect is `v_j-F_N(c_j(s))-r(s)`, not merely `delta_j/h_j`. The variation of
`F_N` along the affine segment and the full-PDE tail forcing must both be
enclosed.

## 3. Recentered interval Picard slabs

Let `E_j` be a Fourier-real complex box for the error
`e(t)=P_N omega(t)-c_j(t)` throughout the slab, let `E_j^in` contain the entry
error, and let `E_j^out` contain the terminal error. Set

\[
 C_j=c_j([0,h_j]),\qquad W_j=C_j+E_j,
\]

and evaluate, with outward rational interval arithmetic,

\[
 D_j=F_N(W_j)+R_j-v_j.                                  \tag{264.8}
\]

The exact acceptance tests are

\[
 E_j^{in}+[0,h_j]D_j\subseteq \operatorname{int}E_j,
 \qquad
 E_j^{in}+h_jD_j\subseteq E_j^{out}.                   \tag{264.9}
\]

The first strict inclusion proves a Picard self-map and gives the full tube;
the second gives the endpoint. At the first slab,
`P_N omega_0-y_0` must lie in `E_0^in`. Subsequent slabs require

\[
 y_j+E_{j-1}^{out}\subseteq y_j+E_j^{in},               \tag{264.10}
\]

where the same stored node `y_j` is used on both sides. Equivalently, a
certificate may store absolute `A_j,W_j,B_j` boxes and replay the original
Cycle 255 inclusions

\[
 A_j+[0,h_j](F_N(W_j)+R_j)\subseteq W_j,
 \quad A_j+h_j(F_N(W_j)+R_j)\subseteq B_j.              \tag{264.11}
\]

The recentered form (264.9) is preferred because subtracting `v_j` exposes a
small defect and avoids wrapping around a large trajectory. It is the Picard
self-map written in the exact translated variable `e=x-c_j`, so it directly
proves `x(t) in c_j(t-t_j)+E_j`. The verifier derives absolute output boxes
from that statement. It must not additionally demand the coarse box test
(264.11): loss of the time correlation between `c_j(s)` and `s v_j` can make
(264.11) fail even when the mathematically equivalent recentered operator is a
contraction.

An interval Newton or Krawczyk proof that (264.5) has an exact discrete root
may tighten `y_(j+1)` and `delta_j`, but it proves only existence of a midpoint
step. It cannot replace (264.9). Conversely, (264.9) remains valid with
nonzero `delta_j`; exact solution of the discrete equation is not required.

## 4. Invariants and their exact role

For the unforced Galerkin field, C263 gives

\[
 \langle x,F_N(x)\rangle_Z=0,
 \qquad \langle x,F_N(x)\rangle_E=0.                   \tag{264.12}
\]

Therefore the rational nominal nodes satisfy the replayable identities

\[
 Q(y_{j+1})-Q(y_j)=\langle m_j,\delta_j\rangle_Q,
 \qquad Q\in\{Z,E\},                                   \tag{264.13}
\]

up to only the verifier's outward arithmetic. These are useful integrity gates
and midpoint normally produces a lower-drift center, which can materially
shrink `E_j`.

They are not full-PDE conservation equations. The retained part exchanges both
quadratic quantities with unresolved modes. If a forced midpoint equation
uses `r_j^mid in R_j`, then the identity is instead

\[
 Q(y_{j+1})-Q(y_j)
 =h_j\langle m_j,r_j^{mid}\rangle_Q
  +\langle m_j,\delta_j^{forced}\rangle_Q.              \tag{264.14}
\]

Continuous full Euler energy and enstrophy are conserved, and their exact
initial values may be intersected with slab enclosures that include the tail.
That intersection is a rigorous optional contractor. Tail contributions must
be bounded from (264.4), and retained conservation must never be imposed by
itself. In particular, no certificate may reject legitimate tail exchange by
forcing `Z(P_N omega)` or `E(P_N omega)` to be constant.

The resulting classification is:

1. Floating C263 midpoint with no interval replay: candidate generation only.
2. Interval Newton for the finite midpoint equation: rigorous discrete
   Galerkin step only, still candidate generation for the PDE theorem.
3. Rational midpoint reference plus (264.4), (264.8)--(264.10): part of a
   rigorous full-PDE enclosure.
4. C263 invariant identities: rigorous redundant checks on the nominal
   Galerkin step; optional full-invariant contractors require explicit tail
   bounds and are never substitutes for Picard containment.

## 5. Certificate schema

A successful ASCII JSON object has format
`c264-mg255-interval-enclosure-v1`. Unknown or duplicate keys fail closed.
Canonical rationals are signed integer strings or reduced `p/q` strings; all
complex boxes are pairs of closed rational intervals.

Required top-level fields are:

```text
format, normalization, family, analytic_tail, retained_system,
midpoint_reference, partition, slabs, invariant_replay,
analytic_norms, cubature, conclusion, digests
```

Their required contents are:

- `normalization`: torus, Haar normalization, Fourier sign, `k^perp`,
  Biot--Savart multiplier, zero mode, reality convention, and mode norm;
- `family`: Cycle 255 enumeration index and all formula-defining parameters,
  or a new separately frozen deterministic family identifier; exact initial
  coefficient generator and digest are mandatory;
- `analytic_tail`: `q0,M,alpha,T`, exact initial low and infinite-tail
  contributions to `A_q0`, all three margins in (264.3), and the Cycle 255
  lemma identifier;
- `retained_system`: `N`, ordered mode list, convolution convention,
  direct-RHS implementation digest, padded replay policy, and arithmetic
  policy;
- `midpoint_reference`: for every slab, exact rational `y_j,y_(j+1),m_j,v_j`,
  recomputed `delta_j` enclosure, Newton residual enclosure if a solve was
  attempted, and optional interval-Newton proof data;
- `partition`: exact `t_j,h_j`, mode ordering, and shared-node identifiers;
- `slabs`: `E_j^in,E_j,E_j^out`, derived `C_j,W_j`, slab-end `q_(j+1)`,
  retained shell masses, omitted-convolution boxes `R_j`, defect boxes `D_j`,
  and margins for both inclusions (264.9);
- `invariant_replay`: nominal `Z,E`, tangency boxes, both sides of (264.13),
  Cauchy--Schwarz defect bounds, and optional full-PDE invariant contractors
  with separate retained and tail contributions;
- `analytic_norms`: upward retained-plus-tail bounds needed for velocity,
  gradient, higher derivative, and any Cycle 256 transfer constants;
- `cubature`: grid and Taylor policy plus initial/final mode boxes; point
  values and normalized-Haar cubic integrals are verifier outputs;
- `conclusion`: orientation and the exact derived inequality `L_out>8U_in`;
  equality fails, and reverse orientation is accepted only as time reversal of
  one already enclosed smooth full Euler segment;
- `digests`: generator, manifest, split slab payloads, verifier source, and all
  formula/version identifiers that affect replay.

Large arrays may live in digest-bound binary or JSONL payloads, but the manifest
must state counts, mode/slab order, byte length, and SHA-256. Missing modes,
slabs, tail terms, or payloads reject the artifact.

## 6. Replay order and trust boundary

The verifier performs the following operations in order.

1. Parse strictly; verify canonical rationals, dimensions, reality, zero mean,
   mode completeness, hashes, and exact family coefficients.
2. Recompute `A_q0`, (264.3), every slab-end weight, and the analytic cap
   (264.4). Reject any `q_(j+1)<=1`.
3. Recompute direct retained convolutions, optional padded cross-checks, shell
   masses, and complete low-mode remainder boxes. A supplied `R_j` must contain
   the recomputed remainder.
4. Recompute the rational affine path, midpoint residual, `C_j,W_j,D_j`, both
   inclusions (264.9), the derived absolute output boxes, and endpoint chaining
   (264.10). Stored derived boxes may be wider but never narrower than
   recomputation.
5. Replay nominal invariant identities and any optional full-invariant
   contractors. Failure of a redundant nominal gate rejects implementation
   integrity; passing it does not compensate for a failed Picard inclusion.
6. Recompute analytic norm conversions and endpoint cubature from the enclosed
   Fourier boxes and infinite tail, then derive the strict conclusion.

The only full-PDE acceptance path is

```text
exact initial datum
  -> shrinking analytic tail
  -> complete omitted-convolution boxes
  -> recentered Picard tube and endpoint chain
  -> full-tail endpoint cubature
  -> strict rational L3 inequality.
```

Midpoint conservation improves the numerical center and supplies strong
cross-checks. It becomes part of a rigorous enclosure only through its exact
rational reference path and a validated continuous defect/Picard argument; the
invariant-preserving discrete update alone remains insufficient.
