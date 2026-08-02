# Cycle 241: connective Karoubi normal form for the graph category

## Result

Let

\[
 A_0=E_i^3\times E_i^3,\qquad
 F_k=O_{\Gamma_{u^k}},\quad u=2+i,\quad 0\leq k\leq6,
\]

and let `Tw(F)` be the category of finite twisted complexes formed from finite
direct sums of shifts of the seven `F_k`.  Write

\[
 \mathcal C=\operatorname {thick}\langle F_0,\ldots,F_6\rangle.
\]

The apparent Karoubi gap in Cycles 200--201 closes because the minimal Ext
category of these generators is connective and has semisimple degree zero.

**Connective Karoubi normal-form theorem.**  Every object of `C` is isomorphic
to an object of `Tw(F)`.  More precisely, every finite strict projector packet
`(C,d,e)`, including every noncentral idempotent `e`, has a finite stable normal
form

\[
 (C,d,e)\simeq (D\oplus D',d_D\oplus d_{D'},1_D\oplus0),             \tag{241.1}
\]

where `D` and `D'` are finite minimal twisted complexes on the same seven
generators.  The equivalence is obtained by finitely many scalar cancellations,
degree-zero changes of basis, and nilpotent triangular corrections.  It neither
assumes that `e` is central nor places a bound on the number of cells.

Consequently `Tw(F)` is already idempotent complete and

\[
 \operatorname {Kar}(\operatorname {Tw}(F))=\operatorname {Tw}(F).  \tag{241.2}
\]

Combining (241.2) with the Cycle 200 finite-twisted-complex theorem proves the
frozen gate

\[
 E\in\mathcal C,\quad [E]=\xi
 \quad\Longrightarrow\quad
 \exists v\in T_0S:\ o_v(E)\ne0.                                  \tag{KI240}
\]

Thus `KI240 PASS` holds.  This is a theorem about the specified support
category.  It does not prove the Hodge conjecture.

## Abstract finite theorem

The normal form used here is the following finite algebraic statement.

**Theorem 241.A (finite connective splitting).**  Let `A` be a strictly unital
minimal `A_infinity` category over a field, with finitely many objects `X_i`,
such that

\[
 H^q\operatorname {hom}(X_i,X_j)=0\quad(q<0),\qquad
 H^0\operatorname {hom}(X_i,X_j)=
 \begin{cases}k,&i=j,\\0,&i\ne j.\end{cases}                       \tag{241.3}
\]

Then the category of finite twisted complexes `Tw(A)` is idempotent complete.
For every finite twisted complex `C` and every idempotent in
`H^0 End(C)`, its image and complement have finite minimal twisted-complex
models.  Every such cohomological idempotent acquires, in the finite dg
realization constructed below and after restoring the canceled contractible
pairs, a strict representative and the stable strict normal form (241.1).

Only finiteness of the particular packet is used.  The dimensions of the
positive-degree Hom spaces need not be uniformly bounded across a family of
packets, and the projector need not preserve a previously chosen vertex
ordering.

### Proof

We first isolate the strictification step.  This is needed because an
idempotent of `H^0` is not, in general, represented by an idempotent cocycle.

**Finite filtered strictification lemma.**  Let `B` be a unital dg algebra and
let

\[
 B=F^0B\supset F^1B\supset\cdots\supset F^LB=0                 \tag{241.4a}
\]

be a multiplicative filtration preserved by the differential.  Suppose that
the differential on `B/F^1B` is zero.  If `a in Z^0(B)` and `[a]^2=[a]` in
`H^0(B)`, and if the image of `a` in `B/F^1B` is idempotent, then `[a]` has a
strict closed idempotent representative.  More explicitly, choose
`h_0 in B^{-1}` with

\[
 \delta _0=a_0^2-a_0=d h_0,\qquad a_0=a,
\]

and recursively put

\[
 \begin{split}
 a_{r+1}&=a_r+(1-2a_r)\delta_r,\\
 \delta_{r+1}&=a_{r+1}^2-a_{r+1}
              =-3\delta_r^2+4\delta_r^3,\\
 h_{r+1}&=(-3\delta_r+4\delta_r^2)h_r .                         \tag{241.4b}
 \end{split}
\]

Then `d a_r=0`, `d h_r=delta_r`, and

\[
 a_{r+1}-a_r=d((1-2a_r)h_r).                                    \tag{241.4c}
\]

Since `delta_0` maps to zero in `B/F^1B`, multiplicativity gives
`delta_r in F^{2^r}B`.  Thus `e=a_r` is a strict idempotent as soon as
`2^r>=L`, and (241.4c) gives an explicit degree-minus-one homotopy from `a` to
`e`.  These formulas are all the coherences required: each new idempotency
defect and its primitive are printed in (241.4b), and the process has at most
`ceil(log_2 L)` stages.

For completeness, inside `Z^0(B)` the boundaries `d(B^{-1})` form a two-sided
ideal: for closed degree-zero `z`, one has
`z d(h)=d(zh)` and `d(h)z=d(hz)`.  In the present situation that ideal is
contained in `F^1B`, because the quotient differential is zero.  Formula
(241.4b) is the idempotent lift modulo that ideal, here given as a finite
polynomial calculation rather than an appeal to a lifting theorem.

Replace the finite dg subcategory used by the packet by its minimal
`A_infinity` Ext model.  Homological perturbation is finite on a finite twisted
complex, so this replacement and its inverse use finite matrices and preserve
the represented retract and its `K_0` class.

First take the scalar part of the differential.  It is a bounded complex in
the semisimple category `add{X_i}`.  Split it, equivariantly for the scalar part
of the projector, into its homology and finitely many contractible two-cell
complexes.  The finite homological perturbation lemma transfers the remaining
positive-degree terms and the projector to the homology summand.  Its series
terminates because every non-scalar term raises the finite bar filtration.
Thus the packet is the direct sum, up to finite contractible stabilization, of
a minimal packet and a contractible packet; no infinite completion is used.

Filter the minimal packet by shift and bar length.  For the fixed packet this
is a finite multiplicative filtration: a non-scalar entry strictly raises the
ordered pair (shift, bar length), so a product of `L` such entries is zero for
some packet-dependent `L`.  Use the finite bar dg realization of the packet.
To make "finite" explicit, number its `n` cells so that every twisting entry
goes from a smaller to a larger cell.  Retain precisely the bar summands indexed
by chains `i_0<...<i_m`; there are no chains with `m>=n`.  The bar differential
replaces consecutive blocks by the corresponding `m_s`, and the
Maurer--Cartan equation makes its square zero.  Deconcatenation gives strictly
associative composition.  Thus its degree-zero endomorphisms form an
associative dg algebra `B`; no completed product or infinite word is present.
Word length, together with shift increase, gives (241.4a).  Its quotient
`B/F^1B` is the endomorphism algebra of the scalar minimal packet and has zero
differential.  In the convention

\[
 \operatorname {hom}^n(X_i[r],X_j[s])
 =H^{n-r+s}\operatorname {hom}(X_i,X_j),                            \tag{241.4}
\]

a degree-zero map has `s-r=q>=0`.  Its shift-preserving symbol has `q=0` and,
by (241.3), is a tuple of ordinary matrices, one matrix for each vertex.  The
underlying symbol algebra is therefore a finite product of matrix algebras.
The closed symbols are the matrices commuting with the symbol differential;
an idempotent among them still splits the symbol complex into its image and
kernel.  The ideal of maps with zero symbol is nilpotent.

Let `p` be the symbol of the projector.  Ordinary Gaussian elimination
conjugates each matrix of `p` to `diag(1,0)`; because `p` commutes with the
symbol differential, that differential is block diagonal in the same basis.
Lift the basis change to the underlying finite graded packet, conjugating both
the full differential and the projector.  Induct over the finite filtration
length.  At one induction step the unknown correction lies in the next
quotient `N^a/N^(a+1)` of the zero-symbol ideal.  Expanding `e^2=e` says that
its off-diagonal components lie in

\[
 p(N^a/N^{a+1})(1-p)\oplus(1-p)(N^a/N^{a+1})p,                     \tag{241.5}
\]

and conjugation by `1+x`, with `x` in the same quotient, removes those two
components.  The diagonal components vanish by the same idempotent equation.
Because `N` is nilpotent, this process stops.  Conjugate the differential along
with the projector.  The identity `de=ed` then forces the final differential
to be block diagonal when the final projector is `diag(1,0)`.  Its two blocks
separately satisfy the Maurer--Cartan equation and hence are finite twisted
complexes.

Now start with an idempotent class and choose a closed representative `a`.
Its scalar symbol is an idempotent: the defect is a boundary, while the
minimal scalar quotient has zero differential.  Apply (241.4b) in `B`.  It
produces, after finitely many displayed polynomial operations, a closed strict
idempotent `e` with `[e]=[a]`.  In particular no unspecified higher homotopies,
coherent homotopy-idempotent datum, or mapping telescope is being assumed.

Here is also an explicit replacement for the triangular conjugation.  After a
scalar basis change, let `p=diag(1,0)` be the chosen lift of the symbol of `e`.
Then `e-p` lies in `N=F^1B`.  Set

\[
 u=ep+(1-e)(1-p).                                                  \tag{241.6}
\]

One has `eu=up` and `u=1+n` for `n in N`; hence
`u^{-1}=1-n+n^2-...+(-n)^{L-1}`.  Therefore `e=upu^{-1}` by a
finite, printed graded conjugator.  If `Q` is the total twisting operator, set
`Q'=u^{-1}Qu`.  Closedness `d_Be=0` is exactly `[Q,e]=0`, so
`[Q',p]=u^{-1}[Q,e]u=0`; hence `Q'` is block diagonal.  Also
`(Q')^2=u^{-1}Q^2u=0`.  Its two blocks are therefore finite twisted complexes.
The map `u:(C,Q')->(C,Q)` is now a closed isomorphism.  This also proves
directly that no preservation of the old vertex ordering is required.

Transfer back across the scalar contraction.  Every transfer sum terminates in
the same filtration `F`; the homotopy between the original representative and
the strict projector is explicitly `H=sum_r (1-2a_r)h_r`, by telescoping
(241.4c).  Adjoin
the finitely many two-cell scalar complexes removed during cancellation and
apply (241.6) to the resulting filtered dg endomorphism algebra.  This gives
the strict stable decomposition (241.1), rather than merely a homotopy block
decomposition.  Removing the contractible blocks leaves finite twisted
complexes representing the image and complement.  This proves Theorem 241.A.

This argument is also the finite-cell proof of the familiar statement that a
connective dg or `A_infinity` category with idempotent-complete semisimple
degree-zero heart has an idempotent-complete finite pretriangulated hull.  The
proof above records the filtration and termination needed for the literal
finite-packet quantifier.

## Verification of the hypotheses for `F_0,...,F_6`

Cycle 199 computes, for `i!=j`,

\[
 \operatorname {Ext}^q(F_i,F_j)=0\ (q\ne3),\qquad
\operatorname {Ext}^3(F_i,F_j)
=H^0(\Gamma_i\cap\Gamma_j,O),                                    \tag{241.7}
\]

and, on a vertex,

\[
 \dim\operatorname {Ext}^q(F_i,F_i)=(1,6,15,20,15,6,1)_q.          \tag{241.8}
\]

There are no negative Ext groups.  Equations (241.7)--(241.8) give

\[
 \operatorname {Hom}^0(F_i,F_j)=0\ (i\ne j),\qquad
 \operatorname {End}^0(F_i)=\mathbb C.                            \tag{241.9}
\]

Hence (241.3) holds.  Notice that the very large, nonzero groups in (241.7)
do not interfere: they have positive degree three and enter only nilpotent
triangular terms after shifts.  They prevent a central vertex decomposition,
as Cycle 201 observed, but they do not prevent objectwise finite idempotent
splitting.

The distinction resolves the earlier concern.  An arbitrary projector need
not preserve Cycle 200's chosen topological ordering on the original packet.
The theorem does not claim that it does.  It replaces the packet by a finite
minimal one and uses the intrinsic shift filtration, whose degree-zero symbol
is semisimple.  The image itself is then another finite twisted complex, to
which Cycle 200 applies directly.

## Grothendieck coordinates and obstruction corner

For completeness, the seven coefficients are detected independently of the
chosen packet.  Localizing at the generic point of `Gamma_k` defines the generic
Euler-multiplicity homomorphism

\[
 \nu_k:K_0(\mathcal C)\longrightarrow\mathbb Z,
 \qquad \nu_k([F_j])=\delta_{kj}.                                  \tag{241.10}
\]

Pairwise graph intersections are zero-dimensional, so no other generator
survives at that generic point.  Thus the seven classes are independent in the
coordinates relevant here.  If `[E]=xi`, then

\[
 (\nu_0(E),\ldots,\nu_6(E))=(c_0,\ldots,c_6),                      \tag{241.11}
\]

and every coordinate is nonzero.  Equation (241.10) is used only to certify the
`K_0` equality; no local restriction of the global Atiyah obstruction is made.

Let `D` be the finite twisted-complex image supplied by Theorem 241.A.  Cycle
200 applies to `D` and gives a vertex `k` and a PEL basis vector `v_j` for which
the diagonal class detected by

\[
 c_k\rho_k(v_j),\qquad
 \rho_k(B)=Q^{-1}B^t-N(u^k)B,                                     \tag{241.12}
\]

is nonzero.  Therefore `o_(v_j)(D)` is not a boundary.  Under the splitting
maps `D -> C -> D`, Atiyah naturality identifies this class with

\[
 [e[2]o_{v_j}(C)e]\in H^2(e\operatorname {End}(C)e).               \tag{241.13}
\]

This is the required nonzero one of the nine exact corners.  The same argument
with a one-cell packet reproduces the known nonzero diagonal obstruction of
each generator `F_k`.

## Coverage of finite packets

The quantifiers are literal:

1. arbitrary finite multiplicities and shifts are allowed;
2. arbitrary differentials satisfying the Maurer--Cartan equation are allowed;
3. arbitrary strict noncentral chain idempotents are allowed;
4. scalar contractible pairs, self-Ext arrows, cross-Ext degree-three arrows,
   and all higher `A_infinity` products are allowed;
5. no genericity, coefficient-height bound, packet-size bound, or enumeration
   is used.

Termination comes from two integers attached to each input packet: the number
of cells decreases during scalar cancellation, and the finite shift-filtration
length decreases during triangular splitting.  Therefore every finite packet
is covered exactly, although no uniform packet-size bound is asserted.

## Scope

This closes the Cycle 200--201 Karoubi boundary and proves `KI240` for the
declared graph-generated category.  It rules out this category as a source of
an object of class `xi` deforming in all nine PEL directions.  It neither rules
out objects with genuinely new support nor produces an algebraic cycle on a
very general fiber.  No Hodge or other Millennium Prize Problem is claimed
solved.
