# Notebook

## Cycle 166 arbitrary split-prime chains

One Cycle 163 split adapted kernel and its complementary isogeny produce an
arbitrarily long carried `eta=1` chain. If `Lambda_1` is the quotient
over-lattice at a good split prime `p`, take
`Lambda_(2r)=p^-r Lambda_0` and `Lambda_(2r+1)=p^-r Lambda_1`, with forms
`p^n E_0`. Every lattice index is `p^6`, every diagonal-lattice index is
`p^3`, and a length-`N` composite has level `m=p^N`, kernel order `m^6`,
restricted degree `m^3`, and `eta_m=1`. Localizing this construction at
finitely many split primes gives mixed composite levels and arbitrary words of
prime arrows. The one-prime chain is periodic up to polarized isomorphism and
all such carried chains stay in the bounded Hilbert locus, so existence gives
no generic Hodge transport.

## Cycle 164 split-quotient descent

Every Cycle 163 split adapted kernel has the form `K=D+JD` with `D` inside the
diagonal.  The factor-swap involution `t` acts by `+1` on `D` and `-1` on
`JD`, hence preserves `K` and descends integrally to a K-antilinear involution
`tbar` of the quotient.  Its exact graph is
`[Gamma_tbar]=p^-6(f times f)_*[Gamma_t]`, and
`(Delta+Gamma_tbar)/2` projects onto the descended diagonal threefold
`Y=f(Gamma)`.  Since `deg(f|Gamma)=p^3`, the normalized class is exactly
`p^-3 f_*[Gamma]=[Y]`.  Thus all `2(p+1)(p^2+1)` adapted quotients remain on
the proper extra-endomorphism/decomposition locus; split eta one does not
yield generic transport.

## Cycle 163 PEL follow-up

For the Cycle 151 K-antilinear graph at every good prime, a PEL-stable kernel
intersection `D` is simultaneously isotropic for the graph symplectic form and
the symmetric cross-form `e(x,Jy)`.  The latter has a four-dimensional radical
and residual plane `X^2+Y^2`.  At inert primes anisotropy forces `dim D<=2`, so
`eta>=p`; exactly `(p+1)^2(p^2+1)` kernels attain equality and none has eta one.
At split primes the eta-one kernels are exactly `O(L+ell_+)` and
`O(L+ell_-)`, for `L` Lagrangian in the radical, and number
`2(p+1)(p^2+1)`.  Thus PEL stability forces large eta on inert support but
does not remove the adapted split-prime escape.

## Cycle 163

A finite-group referee proof now validates the Cycle 162 kernel formulas over
arbitrary `Z/p^e Z`-modules, including nonfree isotropic intersections.  If
`K=K^perp` in `G perp H`, its projections are exactly
`(K cap G)^perp` and `(K cap H)^perp`; the residual quotient is the graph of an
anti-isometry between the resulting quotient pairings.  Equal factor orders
are essential: only then do the intersection orders agree.  For rank-six equal
factors, `|A_K|=|B_K|=delta` and the residual order is exactly
`(p^(3e)/delta)^2=eta^2`.  Explicit nonfree examples over `Z/p^2` and `Z/p^3`
pass, while unequal factors give a counterexample to the unqualified equality.

## Cycle 111

Hostile applicability audit corrected Cycle 110: Bring's curve rigorously has
the two pencils and norm-one `Q(sqrt(5))` unit, but its Jacobian is isogenous to
an elliptic fourth power, so it is neither simple nor RM-only.  Markman's
generic secant-space/nonzero-projection proof cannot be imported.  The uniform
rank-`20`, nullity-`8` contraction theorem remains valid independently and its
verifier survives corrected sign/parameter audits.  Symmetry does not force the
eight-dimensional kernel to be Atiyah-unobstructed.  The production route was
retired.

## Cycle 110

Bring's curve supplies rigorous elementary genus-four RM data: its
smooth canonical quadric gives two trigonal pencils, and the five-cycle
endomorphism yields exact Rosati-compatible `Q(sqrt(5))` RM with integral
norm-one unit `f=(r+r^-1)^2`, satisfying `f^2-3f+1=0`.  Its extra endomorphisms
prevent it from being a full generic Markman seed.  The rank
verifier was corrected to include `q`, standard bivector contraction order,
and sparse cancellation.  A symbolic block proof upgrades rank `20`, nullity
`8` from one specialization to a uniform characteristic-zero theorem.

## Cycle 109

Added a dependency-free exact exterior-algebra verifier for the full
`28`-column Chern-contraction matrix.  It reproduces rank `20`, nullity `8` for
real-quadratic `(2,2)` multiplicities and rank `24`, nullity `4` for four
distinct eigenvalues.  The kernel decomposes into two trace-free endomorphism
summands and two matched `B`/Poisson lines, none automatically killed by the
Atiyah obstruction.  A direct algebraic correspondence on the explicit curve,
not finite point-count matching, is the clean RM certificate.  No such
correspondence or Ext matrix was produced.

## Cycle 108

An explicit genus-four quadric-cubic candidate with smooth quadric and modular
`Q(sqrt(5))` RM data was isolated, but its Jacobian/modular identification is
only heuristic in the source.  Exact exterior-algebra computation corrects the
quartic-CM Chern-contraction rank: real-quadratic `(2,2)` multiplicities force
rank `20` and nullity `8`, not the provisional `24/4`.  Semiregularity requires
the Atiyah obstruction map to have exactly the same eight-dimensional kernel.
Simplicity, RR, and gluing incidence do not imply this; off-diagonal gluing
Atiyah terms remain essential.  The route was not promoted.

## Cycle 107

Primary-source audit of Markman arXiv:2509.23079 confirms an algebraic normalized
Chern class with nonzero quartic-CM Weil projection on a special abelian
eightfold `J(C) x J(C)^`.  The unresolved family step is exactly injectivity of
the Buchweitz--Flenner semiregularity map on the Atiyah obstruction image.  This
reduces to equality of kernels of two maps from a `28`-dimensional deformation
space.  The cohomological matrix is explicit, but the preprint does not specify
enough sheaf/resolution data to compute the Ext/Atiyah matrix reproducibly.
The target remains the leading Hodge scout but is not promoted.

## Cycle 105

Polarization changes, `K`-linear isogenies, nonprincipal duals, and twisted
Fourier--Mukai transports preserve Markman's split Hermitian norm class: the
determinant remains `-N(alpha)`, never `-3 N(alpha)`.  Nonzero unitary special
cycles live over proper special loci, while dominating contraction-generated
cycles have zero determinant projection.  In full `A_6`, the nine-dimensional
Weil component has codimension twelve; rank nine refers only to dominance onto
that chosen base.  No nonmetabolic determinant-bearing seed was found, so the
mechanism was retired.

## Cycle 104

Primary-source audit confirms a clean bounded open target: the rank-two Weil
space of a very general `Q(i)` abelian sixfold of signature `(3,3)` and nonsplit
Hermitian determinant class `-3`.  Split-discriminant secant/Prym constructions
do not cross the norm-class boundary.  An exact eigenspace projector tests any
candidate cycle; one nonzero Weil projection suffices after applying `1+i`.
Promotion requires a nonzero seed on a formally unobstructed relative Chow
component dominating the nine-dimensional Shimura base.  None was found.

## Bounded calibration cycle 84

The all-degree Fermat-plane semiregularity multiplication has a symbolic private-
pivot proof and a dependency-free finite auditor. Literature review shows the
tangent equality and injectivity are known in substance for linear complete-
intersection cycles. The bounded-complexity dense-specialization lemma is also a
standard finite-Hilbert/Chow properness argument; producing the uniform bound is
the unresolved content. These are retained as calibrations, not new Hodge cases.

Bounded scout is queued to formalize the two rank computations in the Fermat
cubic calibration and then check obstruction/smoothness data; equality of
Zariski tangent dimensions alone is not actual dominance.

## Bounded scout tick 2

For the Fermat cubic plane, the normal sequence is
`0 -> N_(P/X) -> O_P(1)^3 -> O_P(3) -> 0`, with map `(u^2,v^2,w^2)`.
Thus `H^0(N)=0` and `H^1(N)=C[uvw]`. The fixed-fiber Hilbert point is isolated
and reduced despite the nonzero ambient obstruction space. The incidence of
cubics containing a plane is a smooth dimension-54 projective bundle over
`Gr(3,6)` and maps unramifiedly to the 55-dimensional cubic parameter space,
so its image is locally a genuine divisor. This validates the calibration but
does not identify arbitrary Hodge components with incidence images.

## Bounded scout cycle 36

The plane calibration also fixes the primitive intersection form exactly.  If
`h` is the hyperplane class and `P` is a plane in a smooth cubic fourfold, then
`h^4=3`, `P.h^2=1`, and the normal sequence gives

`c(N_(P/X))=(1+h)^3/(1+3h)`, hence `P^2=c_2(N_(P/X))=3`.

Therefore the integral primitive class `gamma=3[P]-h^2` satisfies
`gamma.h^2=0` and `gamma^2=24`.  Equivalently,
`([P]-h^2/3)^2=8/3`.  This identifies the exact lattice vector carried by the
plane-incidence divisor; tangent-space dominance alone still says nothing
about Hodge components carrying other primitive lattices.

## Bounded scout cycle 39

The plane self-intersection calibration extends exactly to every smooth
degree-`d` hypersurface fourfold `X_d` in `P^5` containing a plane.  The normal
sequence gives

`c(N_(P/X_d))=(1+h)^3/(1+d h)`

and hence `P^2=d^2-3d+3`.  Because `h^4=d` and `P.h^2=1`, the primitive rational
class `P-h^2/d` has square `d^2-3d+3-1/d`.  At `d=3` this is `8/3`, so
`3[P]-h^2` has square `24` as before.  This fixes the entire normal-sequence
lattice calculation; it supplies no dominance statement for other Hodge
components.

## Bounded scout cycle 41

For the Fermat-type degree-`d` plane calibration, `d>=3`, the map on global
sections induced by the normal sequence is

`H^0(O_P(1)^3) -> H^0(O_P(d))`,
`(l_1,l_2,l_3) |-> l_1u^(d-1)+l_2v^(d-1)+l_3w^(d-1)`.

Its nine monomials are distinct, so it is injective and
`h^0(N_(P/X_d))=0`, while
`h^1(N_(P/X_d))=binom(d+2,2)-9`.  The latter is exactly the expected
codimension of the plane-incidence image: a fixed plane imposes
`binom(d+2,2)` conditions and `Gr(3,6)` has dimension nine.  At `d=3` this
recovers a one-dimensional obstruction space beside a reduced isolated plane
and a smooth incidence divisor.  Nonzero `H^1(N)` therefore cannot by itself
be used as a failure-of-dominance certificate.

## Bounded scout cycle 42

The cubic calibration gives an exact local counterexample to treating
`H^1(N)` as a nonreducedness test. The normal map has cokernel `C[uvw]`, so
`H^1(N_(P/X))` is one-dimensional, but the Hilbert tangent space is
`H^0(N_(P/X))=0`. For the local Hilbert ring `(A,m)` this says `m/m^2=0`;
Nakayama gives `m=0`. Hence the plane is a reduced isolated Hilbert point even
though its standard obstruction space is nonzero. No conclusion follows for
other Hodge-locus components.

## Bounded scout cycle 43

Reduced isolated fibers and tangent equality still do not prove component
dominance. In `S=Spec C[x,y]`, let `W=V(y)`, `V=V(y-x^2)`, and immerse
`Z=W` into `S`. The fiber over the origin is one reduced point, the
differential is injective, and `T_0 W=T_0 V=V(y)`. Nevertheless the image is
`W`, not `V`; indeed `W intersect V=V(y,x^2)` is supported only at the origin.
First-order data cannot distinguish the tangent branches `(y)` and
`(y-x^2)`. Thus the Fermat cubic plane calibration still needs branch
identification plus equal dimension inside a specified irreducible Hodge
component. This is a local logical obstruction, not a claim about the actual
cubic Hodge locus or a Hodge result.

## Bounded scout cycle 50

In a complete Noetherian local ring, equality of two branch ideals modulo
`m^(n+1)` for every `n` implies equality because ideals are `m`-adically
closed. Faithful flatness then identifies the local algebraic germs. A bounded
jet suffices only with an independent finite-determinacy theorem; Noetherianity
alone provides no uniform order. The Fermat calibration still lacks equality
of completed incidence and Hodge-branch ideals, or an applicable determinacy
bound. This proves no Hodge case.

## Bounded scout cycle 46

The branch obstruction persists through arbitrary fixed jet order. In
`C[[x,y]]`, the smooth branches `W=V(y)` and `V=V(y-x^3)` have identical
quadratic jets, reduced points, and injective tangent maps, but
`C[[x,y]]/(y,y-x^3)=C[[x]]/(x^3)`: they meet only at the origin with contact
length three and first differ at the cubic jet. Replacing `x^3` by
`x^(N+1)` defeats every prescribed finite jet order. Thus component dominance
needs formal ideal containment/equality or an independent finite-determinacy
theorem, not a bounded deformation jet. This is a local obstruction only and
proves no Hodge statement.

## Bounded scout cycle 59

Formal inclusion in a smooth irreducible germ plus equal Krull dimension forces
formal equality: a nonzero quotient ideal in the regular local domain strictly
lowers dimension. Reduced equidimensionality alone fails for a component of
`Spf C[[x,y]]/(xy)`. The Hodge route still lacks the required branch inclusion
and dimension equality. No Hodge case is proved.

## Bounded scout cycle 70; promoted calibration

For the Fermat quartic fourfold and a correctly rooted contained plane, the
Jacobian-ring multiplication `R_4 -> R_10` by the primitive plane class has
exact rank six. The plane-incidence normal map has rank nine, so its image is a
smooth codimension-six germ. The relative plane gives scheme-theoretic inclusion
in the selected Hodge germ, whose period Jacobian also has codimension six;
hence the two selected formal germs agree. An exact rational verifier preserves
the rank certificates. This is a local branch theorem for an already algebraic
class, not a Hodge-conjecture case.

## Main-funnel cycle 71

A proper irreducible relative cycle component dominates a reduced irreducible
marked Hodge component once the cycle gives scheme-theoretic inclusion and the
incidence differential has full rank at one pair of smooth points. Bloch's
factorization `beta=sigma alpha` identifies the exact normal-space discrepancy
as `im(alpha) intersect ker(sigma)`. Injectivity on the actual relative
obstruction image gives tangent equality; a complete Artin lifting argument is
still required in singular settings.

For Fermat degree-`d` plane families, the normal obstruction space has dimension
`binom(d+2,2)-9`, and pair multigrading proves the semiregularity multiplication
map injective for every `d>=3`. This propagates the supplied plane cycle but
does not create cycles for arbitrary Hodge components. Details are in
`cycle-71-component-domination-criterion.md`. No full Hodge result is claimed.

## Main-funnel cycle 72: seed equivalence and retirement

A relative cycle component dominates a marked Hodge component exactly when the
marked class is algebraic on the geometric generic fiber, after finite base
change. Properness and spread then propagate a generic cycle to every fiber but
cannot provide the generic seed. CDK algebraicity, countability, degeneration,
K-theory, and normal functions do not bypass this primary obstruction. Broad
complete-intersection and linear-cycle seeded cases are prior art. The tactic is
therefore retired at a precise target-equivalence boundary. No Hodge result is
claimed.

## Bounded scout cycle 63

For the cubic-fourfold plane class, the universal relative plane gives a
scheme-theoretic inclusion of the incidence branch into its Hodge germ. Since
the incidence branch is a smooth divisor, equality is equivalent to nonzero
normal infinitesimal-period functional
`v -> Q(gamma,theta_v(omega))`. The Jacobian-ring multiplication and perfect
Macaulay pairing make this functional nonzero for every nonzero primitive
class; `gamma=3[P]-h^2` has square `24`. Thus the selected formal plane branch
equals its selected Hodge germ. This says nothing about arbitrary Hodge
components and proves no Hodge-conjecture case.
