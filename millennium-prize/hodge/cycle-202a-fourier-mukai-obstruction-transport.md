# Cycle 202A: Fourier--Mukai full-support transport does not cancel the graph obstruction

## Relative setup

Let

\[
A_0=E_i^3\times E_i^3,
\qquad F_k=O_{\Gamma_{u^k}},
\qquad u=2+i,
\]

and retain the nine-dimensional PEL germ `S` and projector class

\[
\xi=\sum_{k=0}^6c_k[F_k],
\qquad \operatorname {ch}(\xi)=D_0\alpha _0
\]

from Cycles 200--201.  Write `A^` for the dual abelian scheme and `P` for the
normalized relative Poincare bundle on `A x_S A^`.  The relative transform

\[
\Phi_P(-)=Rp_{2*}(p_1^*(-)\otimes P)
\]

is an equivalence of relative perfect categories.  A polarization identifies
`A^` with `A` up to an isogeny, which is enough for the rational exceptional
cohomology calculation below.

The untwisted transform does not produce full support.  If `i:B -> A_0` is an
abelian subvariety of dimension three, then

\[
\Phi_P(i_*O_B)\simeq O_{B^\perp}[-3]
\]

up to the harmless degree-zero line bundle fixed by normalization.  Thus the
Fourier--Mukai transform of a graph sheaf is another shifted sheaf on a
threefold, its annihilator, rather than a bundle on the sixfold.

There is nevertheless an explicit full-support version.  Choose a relatively
ample line bundle `L` on `A` and put

\[
V_k=\Phi_P(F_k\otimes L).
\tag{202.1}
\]

The restriction `L|Gamma_(u^k)` is ample.  For every degree-zero line bundle
`M` on that graph,

\[
H^j(\Gamma_{u^k},L|\Gamma_{u^k}\otimes M)=0\quad(j>0).
\]

Cohomology and base change therefore show that `V_k` is a vector bundle on all
of `A_0^`, of rank

\[
\operatorname {rk}V_k=\chi(\Gamma_{u^k},L|\Gamma_{u^k})>0.
\tag{202.2}
\]

Applying (202.1) termwise to the split signed projector object gives a bounded
complex of full-support vector bundles

\[
P_D^{\rm FM}=\Phi_P(P_D\otimes L),
\qquad [P_D^{\rm FM}]=\Phi_{P,*}(e^{c_1(L)}\xi).
\tag{202.3}
\]

This construction changes the geometric appearance of the object but not its
derived deformation problem.

## Exceptional Chern character

On rational cohomology the transform is

\[
\mathcal F_P(\gamma)
=p_{2*}\bigl(p_1^*\gamma\,e^{c_1(P)}\bigr).
\tag{202.4}
\]

For a sixfold it sends the codimension-`q` part to codimension `6-q`.  Since
`ch(F_k)=[Gamma_(u^k)]` is pure of codimension three,

\[
\operatorname {ch}_3(V_k)
=\mathcal F_P([\Gamma_{u^k}]).
\tag{202.5}
\]

Indeed, the positive-degree terms in `e^{c_1(L)}[Gamma_(u^k)]` have codimension
greater than three and contribute only to target codimension less than three;
they cannot enter (202.5).  Consequently

\[
\operatorname {ch}_3(P_D^{\rm FM})
=\mathcal F_P(D_0\alpha _0).
\tag{202.6}
\]

The degree-six Fourier transform is an isomorphism and carries the exceptional
Weil plane of `A_0` to the dual exceptional Weil plane.  After polarization
identification, (202.6) has nonzero exceptional projection.  Thus (202.1)
really does provide full-support bundles, and (202.3) a full-support bundle
complex, retaining the exceptional degree-six Chern character.  This does not
produce a generic algebraic class: these are still special-fiber objects.

## Exact transport of the Atiyah obstruction

Let `v in T_0S` and let `S_v=Spec(C[epsilon]/(epsilon^2))` be the corresponding
first-order PEL deformation.  Both `L` and `P` extend over `S_v`.  Hence
tensoring by `L` and applying `Phi_P` give an equivalence over `S_v`, not merely
an equivalence of the central fibers.  Set

\[
\Psi=\Phi_P\circ(-\otimes L).
\]

For every perfect complex `E`, the induced Ext isomorphism satisfies

\[
\Psi_*\bigl(\operatorname {At}(E)\mathbin{\lrcorner}\kappa_A(v)\bigr)
=\operatorname {At}(\Psi(E))
 \mathbin{\lrcorner}\kappa_{A^}(v).
\tag{202.7}
\]

Equivalently,

\[
o_{\Psi(E)}(v)=\Psi_*(o_E(v)).
\tag{202.8}
\]

One can also see (202.8) without an Atiyah-class formula: `E` lifts to `S_v`
if and only if its image under the relative equivalence lifts, and the inverse
relative transform gives the converse.  Since the map on `Ext^2` is an
isomorphism,

\[
o_E(v)=0\quad\Longleftrightarrow\quad
o_{\Psi(E)}(v)=0.
\tag{202.9}
\]

The full nine-column obstruction maps therefore have equal kernels and equal
ranks after the natural tangent identification.  In particular,

\[
\operatorname {rank}(o_{V_0})=6
\]

for the transformed diagonal graph, and every Cycle 199 clean-pair extension
or cone still has obstruction rank at least eight after transform.  Every
finite seven-graph twisted complex of class `xi` remains obstructed by the
Cycle 200 theorem.

For the split projector complex the transformed obstruction is still block
diagonal under the equivalence.  The cancellation

\[
\iota_v\operatorname {ch}_3(P_D^{\rm FM})=0
\]

is only the Fourier transform of the old semiregularity/supertrace
cancellation.  It does not cancel the individual classes in
`Ext^2(P_D^FM,P_D^FM)`.  The branch obstruction has not disappeared; it has
been encoded as an endomorphism-valued obstruction of a full-support bundle.

## Scope of the no-go

Using a kernel defined only on the special fiber would not evade (202.9).  If
the kernel does not extend over `S_v`, its own deformation obstruction adds a
new term, so the resulting central-fiber equivalence gives no relative object
and no evidence of cancellation.  If it does extend, relative equivalence
forces (202.9).  The same dichotomy applies to standard autoequivalences,
including shifts, translations, tensor products by deforming line bundles,
duality, isogeny pull-push where it is an equivalence, and their compositions.

Nor does the transform close the Cycle 201 Karoubi boundary.  It identifies
the graph-generated thick category with the transformed bundle-generated thick
category and transports each retract obstruction corner isomorphically.  An
unknown unobstructed retract on one side is exactly an unknown unobstructed
retract on the other.

Therefore Fourier--Mukai transport answers the proposed test sharply:

\[
\boxed{\text{full support can be obtained, but obstruction cancellation cannot.}}
\]

The dense-branch proof is no longer visible in the bundle presentation, but
the raw Atiyah class is conjugated by the relative equivalence and remains
nonzero.  A viable candidate must change the derived object or the deformation
problem, not merely its Fourier--Mukai presentation.  No Hodge-conjecture case
is proved here.
