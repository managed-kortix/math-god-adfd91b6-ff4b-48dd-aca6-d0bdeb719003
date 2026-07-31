# Cycle 170: Pontryagin products obstruct an effective connected projector representative

Cycle 169 leaves open whether rational equivalences from the abelian group law
can turn the signed transformed-graph pair into one connected cycle with a
better deformation theory.  For the most direct interpretation--one effective
codimension-three cycle representing the signed class--there is an exact
obstruction.  In fact, the obstruction already appears in the Pontryagin
square.

## Exact graph product

Put `X=E_i^3`, `A=X x X`, and, for a Gaussian integer `a`, let

\[
 \Gamma_a=\{(x,ax):x\in X\}\subset A.
\]

Write `*` for the Pontryagin product on `CH_*(A)`.  For `a != b`, addition
restricts on `Gamma_a x Gamma_b` to the isogeny

\[
 X\times X\longrightarrow A,
 \qquad (x,y)\longmapsto (x+y,ax+by).
\]

Its matrix has determinant `b-a`.  Since multiplication by a Gaussian integer
`z` on `E_i^3` has degree `N(z)^3`, proper pushforward gives the exact Chow
identity

\[
 \boxed{\Gamma_a*\Gamma_b=N(a-b)^3[A]\quad(a\ne b).}
\]

For `a=b`, the addition map has three-dimensional image, so its pushforward as
a six-dimensional cycle is zero:

\[
 \boxed{\Gamma_a*\Gamma_a=0\quad\text{in }CH_6(A).}
\]

These formulas use rational equivalence, not merely cohomology.

## The projector square is negative

Let `u=2+i`, let `Gamma_k=Gamma_(u^k)`, and use the Cycle 169 coefficients

\[
(c_0,\ldots,c_6)=
(317131927490234375,-2073948378906250,12564289203125,
-56707735500,27598945,3626326,-68381).
\]

Thus

\[
 Z:=D_0\alpha_0=\sum_{k=0}^6c_k\Gamma_k=C_0^+-C_0^-.
\]

The graph-product formula gives

\[
 Z*Z=
 2\sum_{0\le i<j\le6}c_ic_jN(u^i-u^j)^3[A].
\]

Exact integer evaluation yields

\[
 \boxed{
 Z*Z=-104188231402289079266552000000000000[A].
 }
\]

Now let `Y` be any effective pure three-cycle on `A`.  The map
`Y x Y -> A` induced by addition either has image of dimension less than six,
in which case `Y*Y=0`, or is generically finite on each dominating pair of
components, in which case

\[
 Y*Y=m[A]\qquad(m\in\mathbf Z_{\ge0}).
\]

The same nonnegativity holds for a reducible effective cycle because all
multiplicities and all generically finite degrees are nonnegative.  Pontryagin
products respect rational equivalence.  Consequently

\[
 \boxed{
 Z\not\sim_{\rm rat}Y
 \quad\text{for every effective codimension-three cycle }Y.
 }
\]

In particular, the signed projector pair cannot be replaced by one effective
connected cycle, regardless of its singularities or deformation theory.

There is also a simpler degree obstruction.  The projector kills every
balanced Kunneth sector, including the polarization-cube direction.  Hence
`Z` has zero degree against any PEL polarization cube, whereas every nonzero
effective three-cycle has positive polarization degree.  The negative
Pontryagin square is stronger in that it is an explicit group-law identity in
the Chow ring.

## No graph-only rational recombination

There is no hidden rational equivalence among the seven transformed graphs.
On the sector

\[
 \bigwedge^pW\otimes\bigwedge^{6-p}\bar W,
\]

`u^*` has the seven distinct eigenvalues

\[
 \lambda_p=(2+i)^p(2-i)^{6-p},\qquad 0\le p\le6.
\]

The diagonal class has a nonzero component in every sector.  Therefore the
cohomology classes of `Gamma_0,...,Gamma_6` have a Vandermonde matrix
`(lambda_p^k)`.  It is invertible, so

\[
 \sum_{k=0}^6r_k\Gamma_k\sim_{\rm rat}0
 \quad\Longrightarrow\quad r_0=\cdots=r_6=0.
\]

Thus group-law manipulations cannot produce a nontrivial graph-only relation.
Their first Pontryagin products instead leave middle dimension and collapse to
multiples of `[A]` by the displayed identity.

The theorem of the cube does not alter this conclusion.  It gives cubical
rational equivalences for pullbacks and tensor products of line bundles, hence
relations in `CH^1(A)`.  Intersecting such relations can create decomposable
codimension-three cycles, but it cannot give a relation involving only these
seven graph classes: the Vandermonde cohomology test would contradict it.  Any
useful cubical construction must therefore introduce genuinely new
middle-dimensional supports.

## Remaining scope

The obstruction rules out a single effective representative of `Z`; it does
not rule out every new effective pair `(Y^+,Y^-)` with

\[
 [Y^+]-[Y^-]=Z.
\]

Adding the same bridge cycle to both sides can make their supports connected,
but it leaves the difference unchanged and supplies no cancellation in the
product of effective Chow spaces.  A useful replacement would still have to be
a genuinely new pair whose two relative Chow germs dominate the PEL base.
Neither the group-law identity, the theorem of the cube, nor graph-only
rational equivalence constructs such a pair.

Reproduce the integer Pontryagin coefficient with

```sh
python3 millennium-prize/hodge/verify_cycle170_pontryagin_obstruction.py
```

This is an exact no-go for the proposed single connected effective
representative, not a no-go for all rationally equivalent effective pairs and
not a generic Hodge-conjecture result.

## Nilpotent-thickening check

The first infinitesimal thickening of the diagonal does not evade the tangent
obstruction either.  If `I` is the diagonal ideal and `V=I/I^2`, then

\[
I^2/I^4\simeq\operatorname{Sym}^2V\oplus\operatorname{Sym}^3V,
\qquad
\mathcal N_{V(I^2)/A}\simeq
\mathcal Hom(\operatorname{Sym}^2V,V),
\]

so it has eighteen fixed-fiber Hilbert tangent directions.  For a normal
ambient obstruction `r`, however, the thickened obstruction is obtained from

\[
D(r)(uv)=u(r)v+v(r)u.
\]

The map `D` is injective in characteristic zero.  Therefore the PEL-base
obstruction is `D circ rho_Gamma`, with the same rank six and the same
three-dimensional kernel as the reduced diagonal.  Nonunit Gaussian graph
thickenings remain injectively obstructed.  Nilpotents add vertical embedded
directions but no new PEL-base directions.

Moreover `V(I^2)` has fundamental cycle `4[Gamma]`; Chow theory forgets its
nilpotent structure but retains this generic multiplicity.  Embedded
nilpotents of smaller-dimensional support cannot alter an obstruction visible
on the dense open of a graph component.
