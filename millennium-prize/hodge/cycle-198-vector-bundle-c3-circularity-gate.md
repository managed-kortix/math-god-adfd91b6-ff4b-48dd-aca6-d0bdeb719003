# Cycle 198: the unpinned vector-bundle `c_3` route is a Hodge reformulation

## Setup

Let `S` be the nine-dimensional nonsplit `Q(i)` PEL component through

\[
A_0=E_i^3\times E_i^3,
\]

and let `W` be its rational rank-two local system of exceptional degree-six
Weil classes.  Write `P_W` for the algebraic correspondence projector from
Cycle 151.  The proposed vector-bundle target is

\[
(VB_3)\qquad
\text{find a bundle }E\text{ on }A_{\bar\eta}\text{ with }
P_W(c_3(E))\ne0.
\]

Here `bar eta` is the geometric generic point of `S`.

## Circularity theorem

`(VB_3)` proves the Hodge conjecture for the Weil space on this component.
Indeed, `c_3(E)` is already the class of an algebraic codimension-three cycle.
The projector is algebraic, and a nonzero rational vector in the irreducible
rank-two Weil space, together with its `Q(i)` transform, spans that space.
Spreading `E` after finite base change gives a dominating relative cycle, so
the standard proper-Chow propagation argument carries algebraicity to every
fiber of the marked component.

Conversely, assume the Weil classes on the geometric generic fiber are
algebraic.  The rational Chern character is an isomorphism

\[
K_0(A_{\bar\eta})_{\mathbb Q}\simeq
\bigoplus_j CH^j(A_{\bar\eta})_{\mathbb Q}.
\]

Choose the inverse image of a pure codimension-three class: all of its Chern
character components except `ch_3` are zero.  After clearing a denominator,
write it as `[E]-[F]`.  Then `E` and `F` have equal rank, `c_1`, and `c_2` in
rational Chow, while `P_W(ch_3(E)-ch_3(F))` is nonzero.  The identity

\[
\operatorname {ch}_3(E)=
\frac{c_1(E)^3-3c_1(E)c_2(E)+3c_3(E)}6
\]

therefore gives

\[
\operatorname {ch}_3(E)-\operatorname {ch}_3(F)
=\frac12(c_3(E)-c_3(F)).
\]

Consequently at least one of `E,F` has nonzero projected `c_3`.  Hence `(VB_3)`
is equivalent to generic algebraicity of the Weil classes; no generic
lower-degree Hodge-class classification is needed for the converse.

The same conclusion applies if one asks merely for an unspecified perfect
complex: rational algebraic `K_0` and rational Chow contain the same
information.  Replacing a cycle by an existential `K_0`, `ch_3`, or `c_3`
lift does not create a seed.

## A non-equivalent exact gate

Pin a bundle or perfect complex `E_0` constructed independently on the special
fiber, with `P_W(c_3(E_0)) != 0`, and ask whether this particular object deforms
in all nine PEL directions.  For a Kodaira--Spencer direction
`v in T_0S`, its first obstruction is

\[
o_{E_0}(v)=\operatorname {At}(E_0)\mathbin{\lrcorner}\kappa(v)
\in\operatorname {Ext}^2(E_0,E_0).
\]

The first exact checkpoint is

\[
\boxed{o_{E_0}:T_0S\longrightarrow\operatorname {Ext}^2(E_0,E_0)
\text{ is the zero map}.}
\]

After choosing a finite locally free resolution, this is a finite nine-column
matrix calculation.  It is genuinely non-equivalent: algebraicity of the flat
Weil class does not imply that this chosen `E_0` deforms, and first-order
vanishing alone does not imply algebraicity on the generic fiber.  All-order
deformation and algebraization of `E_0` would supply the required dominating
algebraic family.  Failure only rejects `E_0`; it does not reject other bundles
or cycles.  Passing the first-order gate still requires the quadratic
Maurer--Cartan obstruction and then formal effectivity/algebraization.

This also explains the failure of the Cycle 153 projector object.  Its Chern
character is correct, but its Atiyah obstruction is block diagonal.  Chern
supertrace cancellation occurs only after applying semiregularity and does not
cancel the individual `Ext^2` obstructions.  Asking for another unspecified
bundle with the same Chern class would return to the equivalent existential
target.

## Next smallest obstruction

The next bounded test should be the first-order Atiyah matrix for one explicit,
non-split extension that is not quasi-isomorphic to a direct sum of graph
objects.  The candidate must satisfy all three conditions before any
second-order work:

1. its projected `ch_3` is the already certified nonzero Cycle 151 Weil class;
2. its locally free resolution and all extension/gluing maps are explicit; and
3. its nine-column Atiyah obstruction matrix has rank zero.

The smallest decisive output is therefore either one nonzero matrix entry,
which kills that candidate, or an exact rank-zero certificate.  Transverse
graph extensions should not be revisited: Cycles 153--154 show that their cross
`Ext` occurs in degree three and cannot alter the degree-two Atiyah obstruction.
The first admissible candidate must use nontransverse support or genuinely new
support outside the graph category.  Only after rank zero is certified should
the Cycle 197 quadratic-jet system be instantiated.

No Hodge case is proved here.  The result is a route classification: the
unpinned `c_3` existence problem is circular/equivalent, whereas deformation of
one pinned explicit object supplies a non-equivalent, falsifiable sequence of
checkpoints toward a sufficient construction.
