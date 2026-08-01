# Cycle 234: direct boundary insertion for bounded Wilson perturbations

## Verdict

**RETRACT.**  The sector decomposition (234.6)--(234.7) and the use of the
Cycle 232 operator-norm estimate with arbitrary unit endpoint vectors are
legitimate.  The claimed marked-polymer factorization is not established,
however.  Spatially disjoint endpoint-connected components can have overlapping
time ranges and collectively leave no complete vacuum time cut, without an
intersecting support chain joining the two endpoint faces.  Section 1 calls
this a `+-` object, but its asserted connected-chain property is false and no
exact configuration-to-gas identity or canonical vacuum-cut factorization is
proved.  Consequently (234.11) and the two-face implication used in (234.16)
do not follow from the stated construction.  The full-Hilbert gap
(234.4) is therefore retracted; the Cycle 232 bulk certificate and Cycle 233
cyclic-subspace bound remain unaffected.

Put

\[
 c=2\,191^4=2\,661\,726\,722,
 \quad q=6c=15\,970\,360\,332,
 \quad \eta=q^{-1},                                      \tag{234.1}
\]

and fix

\[
 0<\theta<\theta_*:=\log(3/e),\qquad
 x_\theta:=c\eta e^{1+\theta}<\frac12,
 \qquad \kappa_\theta:={x_\theta\over1-x_\theta}<1.    \tag{234.2}
\]

For a periodic spatial lattice `Lambda`, write `L=|Lambda|` and define the
explicit, deliberately wasteful constants

\[
 D_{L,\theta}:=
 2^Le^{2(1+\theta)L}\exp(2L\kappa_\theta),
 \qquad
 r_{L,\theta}:=
 \min\left\{1,{1-\kappa_\theta\over8D_{L,\theta}}\right\}.
                                                               \tag{234.3}
\]

The proposed estimate below would give every `v` with
`||v||<r_(L,theta)` a marked expansion uniform in `N`.  If its missing
factorization were supplied, it would have the same tilt `theta` as the bulk
gas and would imply the candidate full ambient Hilbert-space gap

\[
 \Delta_\Lambda(4K_\lambda)\ge
 {\log3-1\over14\log15970360332},\qquad
 \Delta_\Lambda(K_\lambda)\ge
 {\log3-1\over56\log15970360332}                         \tag{234.4}
\]

whenever

\[
 |\lambda|\le {1\over8(15970360332)^{416}}.               \tag{234.5}
\]

The second candidate number in (234.4) is approximately `7.495 x 10^-5`.  The
proposed argument is for periodic tori on which the Cycle 232 interaction-cell convention is
literal.  Degenerate very small tori, where a plaquette or an interaction cell
self-identifies, require a separate finite list of normalizations; this is a
geometry convention issue, not a boundary-insertion obstruction.

## 1. Boundary sectors and marked polymers

For `A subset Lambda`, let

\[
 Q_A=\bigotimes_{x\in A}(1-|\Omega_x\rangle\langle\Omega_x|)
     \bigotimes_{x\notin A}|\Omega_x\rangle\langle\Omega_x|.
                                                               \tag{234.6}
\]

These are only `2^L` orthogonal projections even though every one-site Hilbert
space is infinite dimensional.  Write `v_A=Q_Av`.  Cauchy--Schwarz gives the
only boundary decomposition estimate that is needed:

\[
 \sum_{A\subset\Lambda}\|v_A\|
 \le 2^{L/2}\|v\|.                                      \tag{234.7}
\]

Expand each Euclidean step exactly as in Cycle 232 and insert (234.6) at the
two ends.  Start with one of the three non-vacuum matrix elements

\[
 \langle e^{-t_0NH}v,\Omega\rangle,
 \quad\langle e^{-t_0NH}\Omega,v\rangle,
 \quad\langle e^{-t_0NH}v,v\rangle.                       \tag{234.8}
\]

Decompose its bulk configuration into connected components.  Components not
connected to an occupied endpoint sector are ordinary vacuum polymers and
factor exactly as in Yarotsky's Lemma 4.  At each face, fuse all components
connected to that endpoint sector into one object, including spatially
separated components at the same face.  This full-face fusion is necessary
because `v_A` may be entangled and its endpoint matrix element need not
factorize over spatial components.  If a component chain joins
the two endpoint sectors, fuse both face objects and that chain into one
two-face object.  Give the resulting object `gamma` a mark `-`, `+`, or `+-`
according as it meets the initial face, final face, or both, and set

\[
 \supp\gamma=({0}\times\Lambda\text{ if marked }-)
 \cup({N}\times\Lambda\text{ if marked }+)
 \cup\{\text{supports of its fused bulk components}\}.    \tag{234.9}
\]

The activity `z_v(gamma)` is the sum of all endpoint labels and all underlying
configurations giving this same fused object.  Thus a marked polymer is defined
by a summed activity, not by one formal summand.  A hard-core collection may
contain at most one mark of each face.  If it contains separate `-` and `+`
marks, their activities multiply: a complete vacuum time cut gives precisely
this factorization.  If no such cut exists, the object is instead a single
`+-` mark.  Ordinary polymers retain the Cycle 232 incompatibility relation.
This is the unproved step.  Connected-component decomposition is not the same
as temporal vacuum-cut decomposition.  For example, two spatially disjoint
component families may have overlapping time projections whose union meets
every time layer.  There is then no complete vacuum cut, but there is also no
intersecting chain from time `0` to time `N`.  Fusing the families is possible,
and their union still charges every time layer, but that is a different lemma
from the one stated.  A canonical renewal decomposition or an equivalent exact
configuration-to-gas identity, followed by a summed activity bound for the
resulting objects, is required here; saying that no inclusion-exclusion is
needed does not provide that identity.

## 2. Uniform summed-activity estimate

The norm proof of Cycle 232, equations (232.12)--(232.16), is an operator-norm
proof before contraction with the endpoint vacuum.  It therefore remains valid
after replacing either endpoint by a unit vector in `ran Q_A`.  Each underlying
bulk component still contributes at most `eta` per support point.  Summing the
endpoint labels costs (234.7).  A component attached to a fixed face point has
tilted absolute sum at most

\[
 \sum_{n\ge1}(c\eta e^{1+\theta})^n
 =\kappa_\theta.                                          \tag{234.10}
\]

Root every fused component at the first face point it meets.  Forgetting
compatibility and allowing an independent rooted collection at every face
point only enlarges the sum.  The exponential formula and (234.10) then give

\[
 \sum_{\gamma:\,\text{marked at prescribed faces}}
 |z_v(\gamma)|e^{(1+\theta)|\supp\gamma|}
 \le D_{L,\theta}(2\|v\|+\|v\|^2).                       \tag{234.11}
\]

Here `e^(2(1+theta)L)` pays for two marked full faces, `2^L` pays
for all pairs of endpoint sectors, and `exp(2L kappa_theta)` pays, with room to
spare, for rooted collections at two faces.  Thus (234.11) follows term by term
and is uniform in `N`.  Both factors from (234.7) are retained in the quadratic
matrix element; no dimension-independent boundary decomposition is assumed.

For `||v||<r_(L,theta)`, (234.11) is at most
`(1-kappa_theta)/2`.  The ordinary KP inequality has slack
`1-kappa_theta`, since a support of size `s` sees at most
`kappa_theta s`.  The standard proof of the pinned KP estimate may therefore
be repeated with distinguished marked polymers.  Indeed, a mark of support
size `s` sees ordinary tilted activity at most `kappa_theta s`, while an
ordinary polymer or another mark sees at most the global marked sum in
(234.11).  Reserving half the slack verifies the KP inequalities for the
enlarged gas.  No count of individual boundary summands is required; their
absolute sum is precisely (234.11).

## 3. One-face and two-face bounds

Let `W_v(X)` denote the Ursell weight of a cluster containing a marked polymer
(one `+-` mark or one of the separate one-face marks), and charge multiplicity
by

\[
 \|X\|_s=|\supp\gamma|+
 \sum_{\chi\in X\setminus\{\gamma\}}n_X(\chi)|\supp\chi|.
                                                               \tag{234.13}
\]

The marked pinned-tree proof and the remaining KP slack give a finite explicit
prefactor, for example

\[
 \sum_{X:\,X\text{ contains a mark}}
 |W_v(X)|e^{\theta\|X\|_s}
 \le {2D_{L,\theta}(2\|v\|+\|v\|^2)
       \over1-\kappa_\theta}.                              \tag{234.14}
\]

The precise harmless factor `2` depends on the rooted-tree convention; the
displayed larger value follows by reserving half the KP slack.

For a one-face mark, translate the unmarked part away from that face and use
(234.14).  Its total contribution is an absolutely convergent constant
`b_(face,Lambda)(v)`, independent of `N`, plus a tail bounded for every
`0<delta<theta` by

\[
 C_{L,v,\theta,\delta}e^{-\delta N}.                       \tag{234.15}
\]

Conditional on the missing temporal factorization, a genuine two-face object
must at least charge every time layer, which would give `||X||_s>=N` and the
following estimate.  The stronger connected-chain assertion is false for the
interleaved, spatially disjoint case described above.  Moreover a logarithmic
cluster may connect separate `-` and `+` marks through ordinary polymers; such
clusters are not covered by the displayed derivation, which discusses only a
distinguished `+-` mark.  Thus (234.16) is presently conditional:

\[
 \sum_{X:\,X\text{ connects both faces}}|W_v(X)|
 \le {2D_{L,\theta}(2\|v\|+\|v\|^2)
       \over1-\kappa_\theta}e^{-\theta N}.                 \tag{234.16}
\]

Equations (234.15) and (234.16) are the separate one-face and two-face
estimates missing in Cycle 233.  In particular,

\[
 \log\langle e^{-t_0NH}(\Omega+v),\Omega+v\rangle
 =b_{0,\Lambda}(v)+b_{1,\Lambda}N
  +O_{L,v,\delta}(e^{-\delta N}),                          \tag{234.17}
\]

where `b_(1,Lambda)` is the vacuum bulk coefficient and is independent of `v`.

## 4. Passage to the full Hilbert space

Fix `delta<theta<theta_*`.  The spectral measure of every vector in the open
ball `Omega+B(0,r_(L,theta))` has no mass in

\[
 (E_\Lambda,E_\Lambda+\delta/t_0).                         \tag{234.18}
\]

Indeed, any positive mass there would give a slower exponential in the
positive Laplace transform than the remainder in (234.17).  If `P` is the
spectral projection onto (234.18), then `P Omega=0` by the bulk expansion and
`P(Omega+v)=0` by (234.17).  For arbitrary `psi`, choose nonzero `s` with
`||s psi||<r_(L,theta)`; then `sP psi=0`.  Thus `P=0` on the entire ambient
Hilbert space.  The fact that (234.17) has the same linear coefficient for the
whole open ball also excludes spectrum below the cyclic bottom: a vector with
overlap on a lower spectral interval would have a strictly slower leading
Laplace exponent after rescaling into the ball.  Thus `E_Lambda` here is the
bottom of the full spectrum, not merely the cyclic bottom.

If (234.17) were proved on the stated open ball, the spectral argument above
would be valid: positivity avoids any ambiguity from complex formal cluster
weights, and rescaling arbitrary directions makes the open-ball inference
complete.  The bounded Wilson family is norm-resolvent continuous in each fixed finite
volume.  At `lambda=0` its ground state is simple.  The full-space exclusion
(234.18), valid uniformly along the segment from `0` to `lambda`, prevents the
isolated ground projection from changing rank.  Taking first `delta` to
`theta`, then `theta` to `theta_*`, proves (234.4).  Finally the Haar Gauss
projector commutes with the Hamiltonian and contains the positive ground state,
so restriction to the physical Hilbert space preserves the same lower bound.

## 5. Scope and exact obstruction avoided

The full-face convention makes the admissible radius decay at least
exponentially in `L`; the deliberately wasteful constant (234.3) makes it
decay even faster.  This is harmless:
the open-ball argument is performed separately at each finite spatial volume,
even though its Hilbert space is infinite dimensional, and rescales an
arbitrary Hilbert-space direction.  Requiring a
volume-uniform radius would be an unnecessary and generally false strengthening.

There is, however, a genuine obstruction to the naive formulation.  A
two-face object defined merely by saying that its support contains both full
faces has support cardinality `2L`, independent of `N`, and need not carry any
temporal decay.  The connected vacuum-cut subtraction in Section 1 is
  therefore mandatory.  The stated correction, however, does not handle
  temporally interleaved, spatially disjoint endpoint components.  Until an
  exact renewal/factorization identity and its marked KP bound are proved,
  bounded Wilson perturbations retain the Cycle 233 boundary-insertion
  obstruction at the Cycle 232 constants.
