# Cycle 241: additive-motive wall and punctured-support gate

## Verdict

Retain the Cycle 240 category

\[
 \mathcal C=\operatorname {thick}\langle F_0,\ldots,F_6\rangle,
 \qquad \xi=\sum_{k=0}^6c_k[F_k].
\]

Arbitrary coefficients, cyclic variants, and passage to the universal additive
noncommutative motive do not strengthen the Cycle 201 trace argument. This is a
formal wall, not merely another failed detector. A geometric support filtration
does reveal one genuinely stronger target, but the required comparison from a
raw Atiyah corner to that target is additional input and is not supplied by
additivity. Consequently this route assigns

\[
 \boxed{\text{abstract additive/cyclic-motive route: WALL}.}
\]

## Universal additive-invariant wall

Let `A` be any small idempotent-complete stable category and let `x` be an
object. It determines an exact functor

\[
 \phi_x:\operatorname {Perf}(k)\longrightarrow A,
 \qquad k\longmapsto x.
\]

In the additive noncommutative-motive category,

\[
 \operatorname {Hom}(U_{\rm add}(k),U_{\rm add}(A))\simeq K_0(A),
 \tag{241.1}
\]

and the motive of `phi_x` corresponds exactly to `[x]`. It follows that if
`E:A->D` is any additive invariant and `tau_x` is any objectwise class obtained
naturally from `E(phi_x)`, then

\[
 [x]=[y]\quad\Longrightarrow\quad \tau_x=\tau_y.
 \tag{241.2}
\]

This remains true after tensoring the target with any coefficient ring or
spectrum and after applying any further functor. Therefore coefficients cannot
make a characteristic class obtained solely by applying an additive invariant
to `phi_x` distinguish two objects of the same `K_0` class.

Apply this with `A=C`. Every object of class `xi` has the same image under every
such construction as the known split signed graph object. Ordinary, negative,
and periodic cyclic homology are additive invariants; their Chern characters
are instances of (241.2). Under HKR, the contraction of their traced Atiyah
class is

\[
 \iota_v\operatorname {ch}(\xi)=0
 \tag{241.3}
\]

on the selected PEL tangent space. The split object has nonzero raw Atiyah
obstruction despite (241.3). Hence no implication

\[
 \tau_E=0\Longrightarrow o_v(E)=0
 \quad\text{or}\quad
 o_v(E)\ne0\Longrightarrow\tau_E\ne0
\]

strong enough for `KI240` can hold for this family of invariants. A
projector-inserted trace does not escape the theorem: it is the trace of the
image object and again corresponds to its `K_0` class. Retaining the untraced
corner escapes additivity but is precisely the unknown class
`e[2]o_v(C)e`.

This proves a strict wall for all objectwise invariants factoring through
`U_add`, not only the individual Hochschild constructions tested in Cycle 201.

## What a support filtration actually adds

Put `G_k=Gamma_{u^k}` and

\[
 V_k=A_0\setminus\bigcup_{\ell\ne k}G_\ell,
 \qquad G_k^\circ=G_k\cap V_k.
\]

For `k!=ell`, `G_k intersect G_ell` is the kernel of the nonzero isogeny
`u^k-u^ell` on `E_i^3`, hence is finite. Thus `G_k^o` is the abelian
threefold `G_k` minus finitely many points. Since its normal bundle is locally
free, local-cohomology depth gives

\[
 H^q_{G_k\setminus G_k^\circ}(G_k,N_{G_k/A_0})=0\quad(q<3)
\]

and therefore

\[
 H^1(G_k,N_{G_k/A_0})
 \xrightarrow{\sim}
 H^1(G_k^\circ,N_{G_k^\circ/V_k}).
 \tag{241.4}
\]

This repairs one specific defect in Cycle 200: unlike a small affine generic
open, the punctured branch does not kill the global normal Kodaira--Spencer
class.

Restriction of `[E]=xi` to `V_k`, followed by the codimension-three cycle map
from the topological filtration on `K_0`, gives generic Euler multiplicity
`c_k` along `G_k^o`. It is important not to call generic length a homomorphism
on unrestricted ambient `K_0`: at the codimension-three local ring a
finite-length perfect module has zero class in ordinary `K_0`. The valid
statement uses the supported/topological filtration and its associated cycle.

Thus a possible stronger detector has the desired value

\[
 \lambda_{k,v}(E)=c_k\,\rho_k(v)
 \in H^1(G_k^\circ,N_{G_k^\circ/V_k}),
 \tag{241.5}
\]

which is nonzero for a suitable `v`, since `c_k!=0` and Cycle 200 proves
`rho_k` is nonzero. It separates branches before the global Hochschild trace
cancels them.

## Exact remaining comparison lemma

To turn (241.5) into `KI240 PASS`, one must prove the following statement for
arbitrary perfect complexes, including arbitrary Karoubi images.

**Punctured-support comparison (`PSC`).** Let `X` be a first-order deformation
of a smooth variety, let `G` be a smooth regularly embedded component of the
special-fiber support, and let `P` be a perfect special-fiber complex supported
on `G` after the other components are removed. If `P` has generic Euler
multiplicity `m`, then

\[
 o_v(P)=0\quad\Longrightarrow\quad m\rho_G(v)=0
 \text{ in }H^1(G,N_{G/X}).
 \tag{241.6}
\]

For `P=O_G` and for complexes carrying a filtration by shifts of `O_G`, this is
the standard leading normal obstruction used in Cycle 200. The needed scope is
strictly larger. A localized cyclic Chern character gives a traced class with
support, but identifying its first-order boundary with (241.5) for an arbitrary
perfect complex whose support itself may move is not a formal consequence of
HKR, devissage, or (241.1). Nor does ambient `K_0` equality provide a lift of a
class in the fixed-support category `Perf_G(X)`.

Accordingly, simply declaring a map

\[
 \operatorname {Ext}^2(P,P)\longrightarrow H^1(G,N_{G/X})
\]

whose value is `m rho_G(v)` would assume `PSC`. The ordinary semiregularity map
lands instead in a Hodge/local-cohomology target and may forget precisely the
untraced normal information at issue. This cycle does not promote that
declaration to a proof.

If `PSC` is established by a supported Goodwillie--Jones boundary computation,
a deformation-to-the-normal-cone argument, or a support-Fitting theorem for
derived-flat lifts, then (241.4)--(241.6) immediately prove `KI240` for every
noncentral projector, without projector classification. Conversely, a perfect
complex violating `PSC` is an exact counterexample to this indispensable
intermediate lemma and gives `WALL` for the punctured-support route, though not
necessarily `KI240 FAIL`.

## Scope

The universal-motive argument strictly extends the Cycle 201 no-go from named
trace/Hochschild constructions to every objectwise additive invariant and all
coefficient changes. The punctured-open calculation is a genuine refinement
and a sharply stated next gate, but `PSC` remains unproved by this method. This
note does not decide `KI240`; a separate projector-normal-form argument may do
so. No Hodge-conjecture result or bad retract is claimed.
