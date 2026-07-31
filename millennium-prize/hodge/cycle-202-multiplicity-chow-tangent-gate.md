# Cycle 202: multiplicity Chow tangents do not yet evade the dense-open gate

## Question

Cycle 201B proves a branchwise obstruction for embedded deformations of a
reduced graph union, but the Hilbert-to-Chow differential need not be
surjective at a reducible or nonreduced cycle. Here we isolate the extra
first-order directions at

\[
 Z=\sum_{k=0}^6 m_k\Gamma_k,
 \qquad \Gamma_k=\Gamma_{(2+i)^k},
\]

and ask whether one of them can project to a PEL direction excluded from every
embedded reduced-branch deformation.

## Generic multiplicity calculation

At the generic point of one smooth codimension-three component, the normal
slice is `N = A^3`. The cycle `m Gamma` has transverse cycle `m[0]`, whose
completed Chow germ is the completion at the origin of

\[
 \operatorname {Sym}^m(N)=N^m/S_m.
\]

In characteristic zero its cotangent space has the multisymmetric generators

\[
 p_\alpha=\sum_{j=1}^m x_j^\alpha,
 \qquad 1\leq |\alpha|\leq m.
\]

Consequently

\[
 \boxed{\dim T_{m[0]}\operatorname {Sym}^m(\mathbb A^3)
       =\sum_{d=1}^m {d+2\choose2}={m+3\choose3}-1.}              \tag{202.1}
\]

Only the three degree-one generators occur in the differential from the
ordered reduced-branch cover `N^m`. The generators with `|alpha| >= 2` are
genuine singular Chow tangent directions: they can be nonzero although every
first-order displacement of the ordered branches has zero image in those
coordinates. Thus multiplicity really does create Chow tangents missed by the
reduced-branch calculation of Cycle 201B. This dimension statement alone does
not say that every such tangent is absent from every nonreduced Hilbert chart;
the Hilbert-to-Chow image depends on the selected generic thickening.

The degree-one part on the ordered-branch image is the trace

\[
 \operatorname {tr}:T_{m[0]}\operatorname {Sym}^m(N)\longrightarrow N,
 \qquad (v_1,\ldots,v_m)\longmapsto\sum_jv_j.                     \tag{202.2}
\]

After applying the global normal obstruction map, an embedded deformation, or
a Chow tangent which lifts to the ordered branch cover, satisfies

\[
 m_k\rho_k(B)=0,
 \qquad \rho_k(B)=Q^{-1}B^t-5^kB,
 \quad Q=\operatorname{diag}(1,1,3).                             \tag{202.3}
\]

Here the factor `m_k` is the trace of the fundamental cycle; the normal
displacement variables cannot solve a nonzero cohomological obstruction. The
higher multisymmetric coordinates do not occur in the differential of the
ordered cover, and therefore cannot repair (202.3) on any split or embedded
branch covered by that model. Since `rho_k` is injective for `k >= 1`, every
such branch retaining `m_k Gamma_k` has zero PEL base image as soon as it
retains one nonunit vertex.

This does not prove the same assertion for an arbitrary branch through the
singular Chow point. A relative local equation can have linear terms in the
higher multisymmetric generators even though those generators are invisible
on the ordered cover. Computing those terms is exactly the Chow-versus-Hilbert
gap. Thus the new tangent directions are candidates for an escape, not already
proved vertical relative to `S`.

## Multiplicity graph

Make a graph with one vertex for each distinct generic component and an edge
for each nonempty intersection. For the seven scalar graphs all distinct
intersections are finite and transverse (Cycle 199). Hence

* vertex `k` carries the generic multisymmetric tangent of dimension
  `{m_k+3 choose 3}-1` and obstruction equation (202.3);
* edge terms are supported at finitely many closed points;
* edge and incidence terms restrict to zero at every generic vertex;
* no edge term changes the degree-one generic trace on an embedded or split
  branch.

Thus the associated generic graded tangent is

\[
 \operatorname {gr}_{\rm gen}T_{[Z]}\operatorname {Chow}
 =\bigoplus_k T_{m_k[0]}\operatorname {Sym}^{m_k}(N_k),           \tag{202.4}
\]

up to additional point-supported incidence terms. Equation (202.4) is not a
claim that the complete local Chow ring is a product: a branch whose general
cycle is irreducible can have extra intersection-supported gluing. In
particular, (202.4) alone does not determine the differential to the relative
base.

For the Cycle 169 endpoint multiplicities, the vertex tangent dimensions are
enormous. For example the `Gamma_0` vertex alone has dimension

\[
 5315800223169845837723884703346373473867767333984375.
\]

All generators of degree at least two map to zero under the ordered-cover
differential. Whether some of them have a nonzero relative-base coupling on a
different Chow branch is not determined by their number. Large tangent
dimension is therefore neither evidence for nor an obstruction to base
domination.

## Rational equivalence

There are two different quotients that must not be conflated.

First, rational equivalence inside one affine normal fiber can kill many
degree-zero transverse zero-cycle expressions. On the ordered or embedded
locus this does not repair (202.3), which is imposed before passing to a
quotient of special-fiber cycles. It does not settle the singular Chow
directions outside that locus.

Second, a global rational-equivalence incidence can couple distinct vertices
and can replace the displayed generic valuations altogether. Its tangent is
not computed by quotienting (202.4) by an unspecified vector space of
"infinitesimal rational equivalences." One must choose an actual finite-type
incidence stratum, as in Cycle 196, and differentiate its universal cycle.
Every such tangent still satisfies the necessary infinitesimal cycle-class
condition

\[
 \delta_B\operatorname {cl}(C)=0,                                \tag{202.5}
\]

because rationally equivalent cycles have the same cohomology class. For an
effective pair `(C^+,C^-)`, (202.5) is required separately for `C^+` and
`C^-`; horizontality of `C^+-C^-` only says that their two variations agree.
It does not say that either variation vanishes.

This exposes the remaining finite calculation. If `sigma_k` denotes the
semiregularity/cycle-class image of the generic trace at `Gamma_k`, define

\[
 K_+(B)=\sum_{k\in\{0,2,4,5\}}c_k\sigma_k(\rho_k(B)),\qquad
 K_-(B)=\sum_{k\in\{1,3,6\}}(-c_k)\sigma_k(\rho_k(B)).             \tag{202.6}
\]

The projector identity proves `K_+=K_-`; it does not prove `K_+=K_-=0`.
Cycle 169's direct-sum component obstruction proves rigidity on the displayed
component-preserving chart, but it is not by itself a computation of an
arbitrary local Chow branch. To close every Chow escape at these endpoints,
one must compute the rank of the common map in (202.6) and then control every
rational-equivalence incidence capable of changing the generic valuations.

## Outcome

No full PEL base direction is produced. The calculation does show that the
absolute Chow tangent at a multiplicity vertex is vastly larger than the image
of the ordered reduced-branch cover. Consequently the Cycle 201B Hilbert
obstruction cannot simply be declared to compute the whole Chow tangent.
Embedded thickenings and split branches still obey the degree-one trace gate,
and finite intersection edges do not alter that conclusion.

An escape, if one exists, must use the higher multisymmetric directions in the
relative local Chow equations or change the generic valuations through a
specified global rational equivalence. The present calculation neither
identifies such a branch nor proves that none exists. The next exact tests are
the rank computation (202.6), with explicit semiregularity matrices, and the
differential of a proposed finite-type rational-equivalence witness. Until one
of those supplies a rank-nine base image, the requested full nonembedded base
direction remains unconstructed. No Hodge-conjecture result is claimed.
