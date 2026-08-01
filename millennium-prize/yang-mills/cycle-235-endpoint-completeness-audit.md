# Cycle 235: endpoint-completeness audit and terminal `BR235` evidence

## Verdict

`PASS`, after the typed endpoint-port repair and the complete graph audit below.
In Yarotsky's exact time-sliced expansion, an excitation entering at
either temporal face cannot occur outside the support of an `I` or `J` event.
The apparently dangerous channel with no perturbative `I` event is not omitted:
it is exactly a string of `J` events. Thus the endpoint-completeness hypothesis
in the augmented boundary graph holds for the Cycle 232 labelled expansion.

Together with the exact typed augmented-graph identity, sector-pair direct sum,
outer-product and evaluation maps, uniform tilted estimate, one/two-face
separation, and open-ball spectral argument in the companion Cycle 235
manuscript, this is terminal `BR235 PASS` evidence. The conclusion is only the stated explicit
finite-lattice strong-coupling gap; it has no continuum Yang--Mills consequence.

## 1. Exact projector identity at the initial face

Use Yarotsky's exact one-step decomposition

\[
 e^{-t_0H_\Lambda}=\sum_{I\subset\Lambda}T_{\Lambda,I},
 \qquad
 T_{\Lambda,I}=T'_I e^{-t_0H_{\Lambda\setminus\Lambda_I,0}},
 \tag{235.23}
\]

and insert

\[
 1_{{\cal H}_\Lambda}=1_{{\cal H}_{\Lambda_I}}\otimes
 \sum_{J\subset\Lambda\setminus\Lambda_I}
 P_{{\cal H}'_J}P_{\Omega_{(\Lambda\setminus\Lambda_I)\setminus J,0}}.
 \tag{235.24}
\]

For an endpoint sector

\[
 Q_A=\bigotimes_{x\in A}(1-|\Omega_x\rangle\langle\Omega_x|)
     \bigotimes_{x\notin A}|\Omega_x\rangle\langle\Omega_x|,
 \tag{235.25}
\]

orthogonality of the one-site vacuum/excited projections gives the exact
identity

\[
 P_{{\cal H}'_J}P_{\Omega_{(\Lambda\setminus\Lambda_I)\setminus J,0}}Q_A
 =0
 \quad\hbox{unless}\quad J=A\setminus\Lambda_I.
 \tag{235.26}
\]

Consequently, in every nonzero labelled summand at the initial face,

\[
 A_-\subset \Lambda_{I_1}\cup J_1.                         \tag{235.27}
\]

If `x` belongs to `A_- intersect Lambda_(I_1)`, then it lies under an `I`
event, whose spatial support is `tilde Lambda_(I_1)`. If instead
`x in A_- setminus Lambda_(I_1)`, (235.26) says `x in J_1`, hence it belongs
to the `J` event labelled `(1,x)`, whose spatial support is `tilde {x}`.
Both event supports occupy the two layers adjacent to the first time step.
Thus every non-vacuum initial leg is incident to a labelled bulk event.

This is stronger than a support-only assertion: (235.26) identifies the actual
projector through which the endpoint tensor leg enters the local contraction.

## 2. Final-face identity

Let

\[
 S(I,J)=T_{\Lambda,I}P_{{\cal H}'_J}
 P_{\Omega_{(\Lambda\setminus\Lambda_I)\setminus J,0}}.
 \tag{235.28}
\]

The rightmost projector in the last factor prepares vacuum outside
`Lambda_(I_N) union J_N`, excitations on `J_N`, and an unrestricted state on
`Lambda_(I_N)`. The remaining factor `T'_(I_N)` acts only on
`tilde Lambda_(I_N)`, while the commuting classical evolution cannot create an
excitation outside its input excited sector. Therefore

\[
 \operatorname{Ran}S(I_N,J_N)\subset
 \left(\bigotimes_{x\notin
   (\widetilde\Lambda_{I_N}\cup J_N)}\Omega_x\right)
 \otimes{
 \cal H}_{\widetilde\Lambda_{I_N}\cup J_N}.               \tag{235.29}
\]

Orthogonality with `Q_(A_+)` now implies that a nonzero final contraction must
satisfy

\[
 A_+\subset\widetilde\Lambda_{I_N}\cup J_N.                \tag{235.30}
\]

Every point in the first set is in the support of an `I` event, and every
point in the second is in the support of a `J` event. Hence every non-vacuum
final leg is also incident to a represented bulk component. Equivalently one
may apply the initial-face argument to the adjoint, time-reflected product.

## 3. Finite hostile configuration: bare propagation is represented

In any finite periodic volume realizing the Cycle 232 geometry, the minimal
proposed counterconfiguration occupies one site `x`, uses one time step, and
has endpoint sectors `A_-=A_+={x}`. Set

\[
 I_1=\varnothing,\qquad J_1=\{x\}.                         \tag{235.31}
\]

For a normalized excited eigenvector `u_x perpendicular Omega_x`, tensor the
vacuum on all other sites. The corresponding matrix element is

\[
 \langle u_x\otimes\Omega,
 e^{-t_0H_{\Lambda,0}}(u_x\otimes\Omega)\rangle>0.          \tag{235.32}
\]

There is no `I` event, but there is one labelled `J` event `(1,x)`. Its
two-layer support meets both endpoint legs, so the augmented graph has one bulk
vertex adjacent to both endpoint vertices. The channel is represented.

More generally, for length `N`, take `I_k=emptyset` and `J_k={x}` for every
`k`. The `N` adjacent two-layer `J` supports overlap successively and form one
connected bulk component from time `0` to time `N`. This is precisely bare
classical-semigroup propagation through the `J` sectors, not identity
propagation and not a counterexample to endpoint
completeness.

## 4. Complete endpoint-wire and shared-constraint audit

The endpoint check is not merely a support count. Expand a fixed labelled
summand before any tensor contraction and classify every one-site Hilbert leg.
An interior leg occurs once as an upper leg and once as the matching lower leg,
so the time-slice contraction joins it exactly once. A leg selected by a vacuum
factor terminates at the displayed rank-one vacuum projector. At time `0`,
(235.26) puts each remaining non-vacuum leg in exactly one `I_1` support or
`J_1` sector. At time `N`, (235.29)--(235.30), or equivalently the adjoint
initial-face argument, does the same. Those remaining legs terminate at the
formal endpoint ports `b_-` and `b_+`. The ports are linear resources, not
chosen endpoint vectors; vectors are inserted only by the final evaluation
map.

These three classes--interior contraction, vacuum termination, and endpoint
port--exhaust the legs of the exact `I/J` projector resolution. In particular,
the all-`J` string in Section 3 is present in the first class between slices and
the third class at its ends. There is no unclassified leg and hence no omitted
wire.

The same enumeration audits shared constraints. Local contractions shared by
events are exactly the support-overlap edges used to form ordinary bulk
components. After those edges are contracted, otherwise disjoint components
can share only `b_-` or `b_+`, and all components using a given port are joined
to its unique endpoint vertex. Thus the companion `G_aug` is the complete
tensor incidence graph. Its distinct connected components share neither a wire
nor an endpoint resource and therefore tensor-factor; every shared contraction
or port appears as an edge or common endpoint vertex. Artificial full boundary
faces are absent from this enumeration: they are charged in polymer size only
and are not bulk incompatibilities.

For separate one-face graph components the uncontracted tensors have types
`f in H_-^*` and `y in H_+`. Their joint two-port tensor is the map
`y boxtimes f in Hom(H_-,H_+)`, `(y boxtimes f)(h)=f(h)y`. A genuine two-face
component already has this `Hom(H_-,H_+)` type. The sector-pair direct sum and
the evaluation `T mapsto <xi_+,T xi_->` therefore account for every complete
graph component without adding maps of unlike type.

## 5. Terminal `BR235` record

The five frozen tests are discharged as follows.

1. **Exact identity:** the augmented-component partition and inverse give the
   typed gas identity (235.8), with boundary profile spaces (235.6), the
   outer-product map (235.7), and evaluation (235.7a).
2. **Entangled endpoints:** endpoint labels are unsplit ports, sector pairs form
   a direct sum, and endpoint vectors enter only through evaluation; no spatial
   factorization is used.
3. **Uniform tilted activity:** (235.13)--(235.17) give an `N`-independent
   radius for every `theta<log(3/e)` after summing hidden labels.
4. **Separated faces:** (235.18)--(235.20) include both genuine two-face
   objects and clusters joining separate one-face marks through ordinary
   objects.
5. **Spectral closure:** (235.20)--(235.22) give the full ambient open-ball
   argument, continuity of ground-state rank, and commuting Haar restriction.

Sections 1--4 above remove the sole fail-closed hypothesis left in that proof
and audit that its complete tensor graph omits no wire or shared constraint.
Therefore `BR235` is terminal with status `PASS`. On periodic spatial tori
realizing the Cycle 232 cells without self-identification,

\[
 |\lambda|\le {1\over8(15970360332)^{416}},\qquad
 \Delta_\Lambda(K_\lambda)\ge
 {\log3-1\over56\log15970360332}.                          \tag{235.33}
\]

This does not satisfy `CA235`: it neither follows the continuum trajectory
`lambda(a)->infinity` nor supplies reflection-positive compactness,
Osterwalder--Schrader reconstruction, or a positive physical continuum mass.

## Source check

The identities used here are Yarotsky's equations defining `T_(Lambda,I)`, the
`J`-sector resolution, configuration weights, and support in Section 2 of
D. A. Yarotsky, *Ground states in relatively bounded quantum perturbations of
classical lattice systems*, Commun. Math. Phys. 261 (2006), 799--819,
arXiv:math-ph/0412040. In particular, his support contains
`tilde J_k union tilde J_(k+1)` on each layer, so a boundary `J_1` or `J_N`
label is literally part of the represented space-time configuration.
