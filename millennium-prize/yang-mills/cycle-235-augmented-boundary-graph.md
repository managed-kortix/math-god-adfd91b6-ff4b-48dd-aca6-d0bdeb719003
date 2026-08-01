# Cycle 235: augmented boundary graph and exact boundary factorization

## Verdict

Cycle 234 can be repaired without a temporal no-cut fusion. For each bulk
configuration, first take its ordinary connected components. Adjoin one vertex
for each occupied endpoint and join that vertex to every bulk component incident
to that endpoint. The marked objects are exactly the connected components of
this augmented graph. This is a canonical partition, including the hostile case
of spatially disjoint endpoint families whose time projections cover the whole
slab.

The endpoint vertices are unsplit input/output ports, not vectors. Endpoint
vectors are inserted only through the final evaluation map. Consequently the
typed tensor-network factorization is valid for arbitrary entangled endpoint
vectors: no factorization over spatial subsets is used. Two separate one-face
augmented components combine by the explicit outer-product map, not because
there is a vacuum time cut. A marked component containing both endpoint
vertices contains an ordinary connected bulk component incident to both faces
and hence has temporal size at least the slab length.

With the Cycle 232 bulk hypotheses and the endpoint-completeness identity
proved in the companion endpoint audit, the summed marked activities obey the Cycle 234 bound after
this corrected definition. Marked KP then controls both a genuine two-face mark
and a logarithmic cluster joining separate one-face marks. Thus, subject to
those explicit expansion hypotheses, the finite-volume ambient gap claim is
restored at

\[
 |\lambda|\le {1\over8(15970360332)^{416}},                 \tag{235.1}
\]

with

\[
 \Delta_\Lambda(K_\lambda)\ge
 {\log3-1\over56\log15970360332}.                           \tag{235.2}
\]

For the Cycle 232 labelled expansion this is a strong-coupling lattice theorem:
the projector identity proves that endpoint transmission through an `I` support
or a represented `J` string exhausts every non-vacuum endpoint leg. It is not a
continuum Yang--Mills construction or mass-gap proof. Small self-identifying
tori and unspecified open spatial boundaries remain outside the literal
geometry convention.

## 1. Augmented graph and canonical partition

Fix endpoint sectors `A_-`, `A_+ subset Lambda`. Include `b_-` or `b_+`
whenever that face comes from an inserted endpoint vector; omit it only when the
face is the reference vacuum term. In particular, the `A=emptyset` component
of an inserted vector still has an endpoint vertex, which may be isolated. Let
`C` be one term in the exact Euclidean expansion and let

\[
 {\cal P}(C)=\{P_1,\ldots,P_m\}                              \tag{235.3}
\]

be the unique decomposition of its bulk events into connected components under
the Cycle 232 support-overlap relation. Define the finite bipartite augmented
graph `G_aug(C)` as follows.

1. Its vertices are `P_1,...,P_m` and the occupied endpoint vertices `b_-`,
   `b_+`.
2. Join `b_-` to `P_i` exactly when the local tensor represented by `P_i` has a
   non-vacuum leg at time `0`; define incidence with `b_+` similarly at time
   `N`.
3. There are no extra edges. In particular, temporal overlap of projections is
   not an edge and failure of a complete vacuum time cut is not an edge.

For the Cycle 232/Yarotsky expansion, the completeness property follows from
the endpoint-sector projector identity: at the initial face
`J_1=A_- setminus Lambda_(I_1)` in every nonzero term, and at the final face
`A_+ subset tilde Lambda_(I_N) union J_N`. Thus every non-vacuum leg is in an
`I` or `J` event support. In particular, bare classical transmission is a
represented string of `J` events. The companion endpoint audit gives the full
local matrix-element proof. An expansion using a different event convention
would still have to establish the same property.

One may equivalently retain overlap edges between bulk event vertices before
contracting their connected components. Contracting those edges gives the
graph above.

For every connected component `D` of `G_aug(C)`, let `gamma(D)` contain its
bulk components and its endpoint labels. It is ordinary, `-`, `+`, or `+-`
according as `D` contains neither endpoint, only `b_-`, only `b_+`, or both.
Write `B(gamma)` for the union of its actual bulk event supports and
`R(gamma) subset {b_-,b_+}` for its endpoint resources. The charged-size
convention is

\[
 \begin{split}
 \operatorname{ch}\gamma(D)={}&B(\gamma(D))\\
 &\cup(\{0\}\mathbin\times\Lambda\quad\hbox{if }b_-\in D)\\
 &\cup(\{N\}\mathbin\times\Lambda\quad\hbox{if }b_+\in D).
 \end{split}                                                \tag{235.4}
\]

Set `|gamma|_ch=|operatorname{ch} gamma|`. The artificial full faces in
(235.4) are charged only in this size; they pay for an unsplit, possibly
entangled endpoint port. They are not bulk support and create neither graph
edges nor incompatibilities. Precisely, two objects are compatible iff

\[
 B(\gamma)\cap B(\gamma')=\varnothing,
 \qquad R(\gamma)\cap R(\gamma')=\varnothing.               \tag{235.4a}
\]

The first condition uses actual event supports (with the Cycle 232
interaction-neighbourhood convention), and the second forbids endpoint-resource
reuse. Thus an ordinary object meeting a boundary layer is not incompatible
with a marked object merely because the artificial face charged to the latter
contains that point. This distinction is necessary for the exact identity.

**Partition lemma.** The map

\[
 C\longmapsto\{\gamma(D):D\in\pi_0(G_{\rm aug}(C))\}        \tag{235.5}
\]

is a canonical partition of every configuration into compatible augmented
objects. Conversely, a compatible collection of augmented objects, together
with one internal configuration from each object, has a unique disjoint union
configuration. These maps are inverse.

Indeed, connected components of a finite graph partition its vertex set
uniquely. Distinct ordinary bulk components have disjoint noninteracting local
tensors by the definition of the bulk decomposition. Compatibility forbids
overlap of bulk supports and reuse of either endpoint vertex, so disjoint union
recovers both the bulk components and all endpoint incidences. Reconstructing
`G_aug` therefore recovers the original graph components. This proof does not
mention a time cut.

The hostile interleaving from Cycle 234 is now harmless. If one family is
incident only to `b_-` and another only to `b_+`, they are two marked augmented
components even when their time projections overlap and jointly meet every
layer. If an augmented component contains both endpoints, graph connectivity
forces some bulk vertex `P_i` to be adjacent to both: after removing the only
two endpoint vertices, a path from `b_-` to `b_+` has the form
`b_- - P_i - b_+`, because distinct bulk connected components have no edges.
Thus that `P_i` is itself a connected bulk component incident to both faces.

## 2. Typed endpoint-port factorization

Work before contraction with endpoint vectors. Fix a sector pair
`alpha=(A_-,A_+)` and put `H_-=Q_(A_-){cal H}_Lambda` and
`H_+=Q_(A_+){cal H}_Lambda`. The symbols `b_-` and `b_+` are ports--linear
input/output resources--not vectors. For boundary profile
`tau subset {-,+}`, define

\[
 E_\alpha^\varnothing=\mathbb C,\qquad E_\alpha^-=H_-^*,
 \qquad E_\alpha^+=H_+,\qquad
 E_\alpha^{+-}=\operatorname{Hom}(H_-,H_+).                \tag{235.6}
\]

The fiber-summed open tensor of an object with profile `tau` is a typed element
`z_alpha(gamma) in E_alpha^tau`. Across sector pairs its activity lies in the
finite direct sum `E^tau=directsum_alpha E_alpha^tau`; maps with different
domains or codomains are never added. Sector projection selects the `alpha`
summand before evaluation.

A single two-face object supplies `T in Hom(H_-,H_+)`. Separate marks supply
`f in H_-^*` and `y in H_+`; their contraction-free combination is the explicit
outer-product map

\[
 y\boxtimes f:H_-\longrightarrow H_+,
 \qquad (y\boxtimes f)(h)=f(h)y.                            \tag{235.7}
\]

For a compatible collection `Gamma`, set
`R(Gamma)=union_(gamma in Gamma)R(gamma)` and multiply its ordinary scalar activities.
Use (235.7) if it contains separate `-` and `+` marks, use the map itself if it
contains a `+-` mark, and retain the functional or vector if only one endpoint
resource occurs. Denote the result by
`Phi_alpha(Gamma) in E_alpha^(R(Gamma))`. Compatibility (235.4a) makes these
cases exhaustive. Only now insert arbitrary, possibly spatially entangled,
endpoint vectors `xi_- in H_-`, `xi_+ in H_+`, through

\[
 \begin{array}{ll}
 \operatorname{ev}^{\varnothing}(c)=c,&
 \operatorname{ev}^-(f)=f(\xi_-),\\
 \operatorname{ev}^+(y)=\langle\xi_+,y\rangle,&
 \operatorname{ev}^{+-}(T)=\langle\xi_+,T\xi_-\rangle.
 \end{array}                                                \tag{235.7a}
\]

Thus `ev^(+-)(y boxtimes f)=f(xi_-)<xi_+,y>`. Ports remain unsplit and
endpoint vectors occur only in evaluation; no product-state hypothesis enters.

For fixed sectors, each `z_alpha(gamma)` sums all internal labelled bulk
configurations in its fiber of (235.5), in the corresponding space (235.6).
Absolute convergence permits regrouping, and the inverse partition map gives
the typed exact gas identity

\[
 \langle\xi_+,e^{-t_0NH_\Lambda}\xi_-\rangle
 =\sum_{\substack{\Gamma\ \mathrm{compatible}\\
                   R(\Gamma)=\{b_-,b_+\}}}
   \operatorname{ev}^{R(\Gamma)}_{\xi_+,\xi_-}
      \bigl(\Phi_\alpha(\Gamma)\bigr).                     \tag{235.8}
\]

For general endpoint vectors, decompose by the orthogonal sector projectors and
sum (235.8) over `alpha`. This evaluates the finite sector-pair direct sum; it
does not add unlike maps inside one `Hom` space. Taking vacuum and inserted
components of `Omega+v` recovers the vacuum, linear, and quadratic terms. For
scalar KP, apply (235.7a) first and majorize by the norms of (235.6). KP is not
applied to an undefined product of open tensors.

### Endpoint completeness and complete tensor-graph audit

Yarotsky's exact `I/J` resolution supplies the needed endpoint completeness.
At the initial face, orthogonality gives
`J_1=A_- setminus Lambda_(I_1)` in every nonzero sector summand. At the final
face, the last factor has vacuum outside
`tilde Lambda_(I_N) union J_N`, so a nonzero contraction requires
`A_+ subset tilde Lambda_(I_N) union J_N`. Every non-vacuum endpoint port is
therefore incident to an actual `I` or `J` event. In particular,
`I_k=emptyset`, `J_k={x}` for every `k` is a connected chain of overlapping
two-layer `J` events: bare propagation is represented, not an omitted wire.

For completeness, list before contraction every local tensor factor in a
labelled time-sliced summand and every one-site Hilbert leg on its lower and
upper faces. Each interior leg occurs exactly twice and is joined by its
time-slice contraction. Each vacuum-projected leg terminates at its displayed
rank-one vacuum projector. By the `I/J` identities, every remaining boundary
leg occurs exactly once at `b_-` or `b_+`. Hence every leg is internal,
vacuum-terminated, or an endpoint port; there is no fourth class and no omitted
wire.

The shared constraints are also exhaustive. Support-overlap contractions lie
inside one bulk component. The only constraint shared by otherwise disjoint
components is reuse of the same endpoint port. Contracting all bulk-overlap
edges and adjoining `b_-`,`b_+` therefore gives the complete incidence graph
`G_aug`, not a subgraph. Distinct graph components have neither a contracted
wire nor a shared endpoint resource, so their open tensors tensor-factor;
conversely every such separation appears in `G_aug`. Thus (235.7) omits no
contraction, (235.4a) lists every shared constraint, and artificial charged
faces cannot create incompatibility.

## 3. Summed marked activity

Use the repaired Cycle 232 constants

\[
 c=2\,191^4=2\,661\,726\,722,
 \quad q=6c=15\,970\,360\,332,
 \quad\eta=q^{-1},                                         \tag{235.9}
\]

and fix

\[
 0<\theta<\theta_*:=\log(3/e),\quad
 x_\theta=c\eta e^{1+\theta}<\frac12,
 \quad\kappa_\theta={x_\theta\over1-x_\theta}<1.         \tag{235.10}
\]

The Cycle 232 estimate is an operator-norm estimate before endpoint
contraction. It therefore bounds the norms in (235.6), uniformly over unit
vectors in every sector. A connected bulk component rooted at a prescribed
face point has tilted absolute sum at most

\[
 \sum_{n\ge1}(c\eta e^{1+\theta})^n=\kappa_\theta.          \tag{235.11}
\]

Set `L=|Lambda|` and

\[
 D_{L,\theta}=2^Le^{2(1+\theta)L}
                  \exp(2L\kappa_\theta).                   \tag{235.12}
\]

Then the corrected augmented objects satisfy

\[
 \sum_{\gamma:\,\gamma\ \mathrm{marked}}
 \|{\bf z}_v(\gamma)\|e^{(1+\theta)|\gamma|_{\rm ch}}
 \le M_{L,\theta}(v):=
 D_{L,\theta}(2\|v\|+\|v\|^2),                            \tag{235.13}
\]

uniformly in `N`.

Here is the full overcount. Sector decomposition gives

\[
 \sum_A\|Q_Av\|\le2^{L/2}\|v\|.                           \tag{235.14}
\]

Order the occupied faces, with `-` before `+`. Assign each incident bulk
component to the first occupied face at which it is incident, and root it at the
first incident point of that face in a fixed order. Thus every component is
owned and rooted exactly once, including a component incident to both faces.
Forget compatibility and permit an independent set of rooted components at
every one of the `L` points on each face. The exponential formula and (235.11)
cost at most `exp(L kappa_theta)` per face. Pay
`exp((1+theta)L)` for each full face in (235.4). For two faces, (235.14) costs
at most `2^L ||v||^2`; the linear terms are smaller than the deliberately
wasteful common factor in (235.12). Dropping the ownership restriction then
only adds independently rooted choices. One must not represent a two-face
component twice and replace its one activity by the product of two copies; that
would not be a monotone overcount when the activity is smaller than one. The
single-owner injection avoids that error. This proves (235.13) for augmented
components, including the sum over every internal fiber. It does not use
termwise control as a substitute for summed control.

Choose

\[
 r_{L,\theta}=
 \min\left\{1,{1-\kappa_\theta\over8D_{L,\theta}}\right\}.
                                                               \tag{235.15}
\]

For `||v||<r_(L,theta)`, (235.13) is at most
`(1-kappa_theta)/2`. Apply scalar KP to the contracted norm majorants described
after (235.8), with `a(gamma)=|gamma|_ch`. The ordinary tilted
incompatibility sum is at most `kappa_theta |gamma|_ch`. An ordinary object
sees incompatible marks by at most the global marked sum (235.13). A marked
object sees ordinary objects only through `B(gamma)`, whose size is at most
`|gamma|_ch`, and it sees incompatible marks through endpoint-resource reuse;
the latter is bounded by the global marked sum. This includes repeated or
same-face marks in the cluster majorant, although compatible gas configurations
use each face only once. Since every charged size is nonzero, both KP
inequalities are bounded by

\[
 \left(\kappa_\theta+{1-\kappa_\theta\over2}\right)
 |\gamma|_{\rm ch}<|\gamma|_{\rm ch}.
\]

The standard rooted-cluster consequence bounds the sum with a chosen marked
occurrence by its tilted activity times `exp(a(gamma))`. Summing the chosen
occurrence over all marks bounds all clusters containing a mark by
`M_(L,theta)(v)`, overcounting a cluster once for each marked occurrence.
Therefore the following deliberately weaker estimate holds. With multiplicity
charged by

\[
 \|X\|_s=\sum_{\gamma\in X}n_X(\gamma)|\gamma|_{\rm ch},   \tag{235.16}
\]

one may take the conservative marked-cluster bound

\[
 \sum_{X:\,X\text{ contains a mark}}
 |W_v(X)|e^{\theta\|X\|_s}
 \le {2M_{L,\theta}(v)\over1-\kappa_\theta}.                \tag{235.17}
\]

The displayed factor `2/(1-kappa_theta)` is thus conservative; no individual
marked-object count is needed.

## 4. Joint endpoint dependence and temporal decay

A logarithmic cluster depends jointly on both endpoints in exactly two ways:

1. it contains a `+-` augmented object; or
2. it contains separate `-` and `+` objects joined in the cluster
   incompatibility graph, possibly through ordinary polymers.

In the first case, Section 1 supplies a connected bulk component incident to
both faces. Because its event supports are connected by overlap and each event
has a contiguous two-layer time support, its actual bulk support meets every
intermediate time layer. In the second case, an incompatibility path may contain
formal same-face edges between marks which reuse `b_-` or `b_+`. Contract each
maximal run of such edges. Every transition between the resulting initial-face
group, ordinary objects, and final-face group is an actual bulk-overlap edge.
Non-isolated members of the initial and final groups are incident to their
respective boundary layers; an isolated endpoint-only mark cannot be the source
of an actual transition. The resulting chain of actual supports therefore meets
every intermediate layer. Artificial full-face intersections are not edges in
this argument.
Therefore in both cases

\[
 \|X\|_s\ge N.                                              \tag{235.18}
\]

Repeated polymers cause no problem because (235.16) charges multiplicity.
Combining (235.17)--(235.18) gives the exact two-face estimate

\[
 \sum_{X:\,X\text{ depends on both faces}}|W_v(X)|
 \le {2M_{L,\theta}(v)\over1-\kappa_\theta}e^{-\theta N}.
                                                               \tag{235.19}
\]

This includes the separate-mark logarithmic clusters omitted in Cycle 234.
The interleaved but cluster-disconnected hostile configuration contributes to
the product of two one-face partition factors; it is not a jointly connected
term of the logarithm and needs no temporal decay.

Clusters involving only the initial face have an absolutely convergent
half-slab limit. Comparing the finite slab to that limit leaves only clusters
whose support reaches distance `N`; the singleton-pinned KP argument of Cycle
233 and (235.16) bound the difference by `O(e^{-delta N})` for every
`0<delta<theta`. The final face is identical after time reflection. Ordinary
bulk clusters have the Cycle 233 decomposition. Hence

\[
 \log\langle e^{-t_0NH}(\Omega+v),\Omega+v\rangle
 =b_{0,\Lambda}(v)+b_{1,\Lambda}N
   +O_{L,v,\delta}(e^{-\delta N}),                           \tag{235.20}
\]

where `b_(1,Lambda)` is the vacuum bulk coefficient and is independent of `v`.
The radius (235.15) is allowed to depend on `L` but is independent of `N` and
of the direction of `v`.

## 5. Full finite-volume gap

The remaining inference is the valid open-ball argument already isolated in
Cycles 233--234. Positivity of the spectral measure and (235.20) exclude
spectrum in

\[
 (E_\Lambda,E_\Lambda+\delta/t_0)                           \tag{235.21}
\]

for every vector in the open ball `Omega+B(0,r_(L,theta))`. If `P` is the
spectral projection onto (235.21), then `P Omega=0` and
`P(Omega+v)=0` throughout that ball. For arbitrary `psi`, choose nonzero `s`
with `||s psi||<r_(L,theta)`; then `sP psi=0`, so `P=0` on the ambient Hilbert
space. The common linear coefficient in (235.20) similarly rules out spectrum
below the vacuum cyclic bottom.

For the bounded Wilson family, finite-volume norm-resolvent continuity along
the segment from `0` to `lambda`, compact resolvent, and the same exclusion
prevent the simple ground projection at zero coupling from changing rank.
With `t_0=14 log q` for `4K_lambda`, first let `delta` increase to `theta` and
then `theta` increase to `log(3/e)`. This gives

\[
 \Delta_\Lambda(4K_\lambda)\ge
 {\log3-1\over14\log15970360332},\qquad
 \Delta_\Lambda(K_\lambda)\ge
 {\log3-1\over56\log15970360332},                           \tag{235.22}
\]

at (235.1). The Haar Gauss projector commutes with the Hamiltonian and contains
the positive ground state, so restriction to the physical finite-volume
Hilbert space preserves this lower bound.

## 6. Fail-closed boundary

The proof establishes only the following scope.

1. The local Euclidean expansion must have the exact disjoint-component tensor
   factorization used in Cycle 232; (235.8) makes that dependency explicit.
2. Every non-vacuum endpoint leg must be represented by an incident bulk
   component. A bare transmission channel must be promoted to such a component
   before the partition lemma applies.
3. Endpoint incidence means an actual non-vacuum tensor leg at the face, not
   overlap of a time projection and not absence of a vacuum cut.
4. Activities are Banach-valued fiber sums and are bounded in operator norm
   before contraction with arbitrary endpoint vectors.
5. Joint temporal decay is asserted only for a connected logarithmic cluster
   carrying both endpoint labels. Disconnected interleaved families factor and
   are not falsely assigned decay.
6. The constants concern periodic spatial tori realizing the Cycle 232 cells
   without self-identification. Other boundary conventions require a fresh
   geometry audit.
7. No step addresses the weak-coupling continuum trajectory
   `lambda=2/g^4 -> infinity`, OS reconstruction, or nontriviality of a
   continuum limit. Therefore (235.22) is not a Millennium Prize solution.
