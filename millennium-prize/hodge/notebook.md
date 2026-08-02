# Notebook

## Cycle 241 connective Karoubi normal form

The Karoubi boundary from Cycles 200--201 closes for these seven generators.
Their minimal Ext category is connective, with `Hom^0(F_i,F_j)=0` for `i!=j`
and `End^0(F_i)=C`.  In every finite projector packet, canceling scalar
contractible pairs terminates; on the resulting minimal packet, degree-zero
maps preserve the finite shift filtration and have a product-of-matrix-algebras
symbol.  Splitting that symbol and removing successive strictly triangular
terms through its nilpotent ideal gives a finite stable normal form
`1_D direct-sum 0`, even for arbitrary noncentral projectors.  Thus the finite
twisted-complex category is already idempotent complete.  Generic Euler
multiplicities recover the seven coefficients of `xi`, and Cycle 200 applied to
the finite image `D`, followed by Atiyah naturality, produces a nonzero one of
the nine corners.  This proves `KI240` for the graph-generated support category,
not the Hodge conjecture.

The homotopy-idempotent step is literal.  For a closed representative `a` with
`delta=a^2-a=dh`, replace `a` by `a+(1-2a)delta`; the new defect is
`-3delta^2+4delta^3`, with primitive `(-3delta+4delta^2)h`.  Repetition doubles
the nilpotent filtration order and terminates.  If `p` is the diagonal scalar
symbol, `u=ep+(1-e)(1-p)` conjugates the resulting strict idempotent to `p`, and
`u^{-1}` is a finite geometric series.  This removes the strictification gap
identified by the hostile audit without invoking a telescope.

## Cycle 223 conics on Chow varieties

For a Chow-degree-two map from `P^1` with geometrically integral, generically
reduced general `r`-cycle, the universal incidence pushes forward to twice the
linear `(r+1)`-plane class. If `S` is its swept carrier and `delta` the generic
incidence degree, then `delta deg(S)=2`. The two cases are a birational sweep of
an integral quadric `Q^(r+1) subset P^(r+2)` and a degree-two sweep of a linear
`P^(r+1)`. For three-cycles these are `Q^4` and `P^4`; both contain lines and
therefore cannot lie in an abelian variety. Hence the integral-general conic
mechanism is empty on `A_0`. As the second consecutive support failure after
Cycle 222, it triggers the stop rule and returns the funnel to portfolio
discovery. No Hodge result is claimed.

## Cycle 222 lines on Chow varieties

A nonconstant line in `Chow_(r,d)(X subset P^N)` with integral, generically
reduced general member forces a linear `P^(r+1) subset X`. Indeed, the universal
incidence sweep has dimension `r+1`; intersecting it with a general codimension
`r+1` linear space counts both the single intersection with a Chow hyperplane
on the parameter line and `delta deg(S)`, so `delta deg(S)=1`. Projective-space
hypersurface pencils show that reducible endpoints with no common summand can
have integral general member: `x_0x_1` and
`x_2(x_0+x_1+x_2)` give the divisor example and, in a fixed plane, the curve
example. Zero-cycles admit no such example because an integral reduced
zero-cycle has degree one. Since an abelian variety contains no `P^4`, Cycle
218's integral-general secant open is empty. This retires Chow degree one only;
higher-degree rational curves and chains remain open. No Hodge result is
claimed.

## Cycle 221 Chow-pencil UFD scout

For `P=F_(Y^+)F_(C_0^-)` and `Q=F_(Y^-)F_(C_0^+)`, write
`g=gcd(P,Q)`. In the polynomial UFD the universal pencil has the exact
factorization `sP+tQ=g(sp+tq)`, with `sp+tq` irreducible after removing `g`.
Distinct scalar members therefore have gcd exactly `g`. Since Cycle 218 asks
the general member to be geometrically integral, `g=1`, giving four explicit
cross-coprimality conditions between the two unknown and two reference Chow
forms. No stronger common-factor conclusion follows: the line `sxy+tzw` in
the Chow space of quadric divisors on `P^3` has reduced reducible endpoints
`xy` and `zw`, gcd one, and geometrically integral rank-four general member.
Hence UFD/resultant geometry supplies useful open witnesses but does not retire
the frozen higher-codimension Chow secant. No Hodge result is claimed.

## Retired Cycle 218 frozen Chow-secant candidate

Freeze `(e,n,h)=(0,1,(1))` again, now without imposing the already obstructed
split determinantal endpoints. Unknown endpoints of the exact Cycle 169
degrees lie in a declared integral, generically reduced non-graph open.
Cross-add the reference pair and require the projective secant between the two
Chow forms to lie in `Chow_(3,D)` coefficient by coefficient. This line is the
explicit `P^1` rational-equivalence chain. It selects the special-fiber point;
the rank-nine Jacobian and 45 Hessian lifts are correctly computed in the
ambient relative Chow product because the reference graphs do not extend over
the PEL base. Cycle 222 subsequently proves that no such line can have integral
general member on an abelian variety, so the declared open is empty before
these equations are reached. No Hodge result is claimed.

## Cycle 217 split determinantal degree obstruction

Freeze `R_(0,1,(1))`: one degree-one rational curve in
`Chow_(3,d_++d_-)` joins `Y^++C_0^-` to `Y^-+C_0^+`, with no auxiliary cycle.
Take the endpoints to be the expected codimension-three maximal-minor loci of
`4 x 2` matrices of sections of `O(161557P)` and `O(117159P)`, saturated by the
1-generic, pure, integral support open. Thom--Porteous forces the endpoint
classes to be `4m^3P^3` and their degrees to be `1440m^3`.
The frozen degrees are respectively `296` and `56` modulo `360`, so the
incidence is empty before tangent or second-order equations. Even without the
degree mismatch, a difference of these classes has zero exceptional Weil
projection. This retires split-polarization maximal-minor supports, not
determinantal loci from independently constructed nonsplit exceptional
bundles. No Hodge result is claimed.

## Cycle 205 clean weighted-Pfaffian no-go

For free nonnegative coordinate weights, requiring every `5 x 5` Pfaffian
entry class to be effective and the complete center cubic to equal `kXYZ`
has no solution for any nonzero `k`. After sorting one coordinate vector,
effectivity and parity give `x=q+2r+z+2u`; its pure-cubic coefficient expands
as a polynomial with positive coefficients in every variable except the single
free gap `p`. Hence a zero pure cube is exactly a multiple of a permutation of
`(0,1,1,1,1)`. Two distinct such rays create positive `X^2Y` and `XY^2`
contamination, while three coordinates on one ray have zero `XYZ` coefficient.
This is an unbounded arithmetic no-go in the free coordinate cone, not for
effective divisor cones with relations. No Hodge result is claimed.

## Cycle 241 additive-motive wall and punctured-support gate

The universal additive motive proves a strict wall: every natural objectwise
additive characteristic class, with arbitrary coefficients and including all
standard cyclic variants, sees an object only through `K_0`. It therefore has
the same value on all objects of class `xi`, and cannot distinguish the known
raw-obstructed, trace-zero split object. Geometric restriction is stronger:
removing the other graphs finitely punctures `G_k`, and depth preserves its
normal `H^1`; supported/topological K-theory retains multiplicity `c_k`.
Completion by this route reduces exactly to `PSC`: for every perfect complex supported on
the punctured regular branch, `o_v(P)=0` must imply `m rho_G(v)=0`. This is
known for the filtered graph complexes but is not formal for arbitrary Karoubi
images, because their support may move and ordinary semiregularity has a
coarser target. Additive motives are `WALL`; this route does not decide
`KI240`, independently of the connective normal-form argument recorded first.

## Cycle 203 first Ferrand doubles

For either `G=Gamma_I` or `Gamma_diag(3,1,1)`, fixed-polynomial first Ferrand
doubles are the locally-free quotients `O_G^3 -> L` in a bounded Quot scheme;
the embedded square-zero algebra is uniquely determined by the quotient. On a
local chart `q(z_r)=1`, its equations are
`(z_j-a_j z_r, z_r^2)`, and differentiation gives an invertible normal matrix
`A_r(a)` with determinant `+/-2`. Thus the full Atiyah matrix contains the
canonical block `(A_r tensor I_3)rho_M`. Its ranks are `6` for the identity
graph and `8` for the `(3,1,1)` graph; the paired block has rank `8` and common
kernel dimension one. Eliminating rank-zero equations to all quotient and
extension parameters gives `(1)` on every chart. Quotient-dependent trace-free
rows may only increase rank. Hence every bounded first-double rank-zero locus
is empty; no Hodge result is claimed.

## Cycle 202A Fourier--Mukai obstruction transport

An untwisted graph sheaf transforms to a shifted sheaf on its annihilator, but
tensoring first by a relative ample line bundle gives an IT0 Fourier--Mukai
transform that is a full-support vector bundle. The projector object therefore
becomes a bounded complex of such bundles, and its degree-six Chern character
is the cohomological Fourier transform of the same nonzero exceptional Weil
class. This does not improve deformation: the relative equivalence conjugates
`At(E) contraction kappa(v)` in `Ext^2`, preserving the kernel and rank of the
nine-column obstruction map. Dense-branch obstruction is merely encoded as a
full-support bundle obstruction; semiregularity cancellation remains traced
rather than raw. The unknown Karoubi corner is transported unchanged. No Hodge
result is claimed.

## Cycle 202 multiplicity Chow tangent gate

At a generic multiplicity-`m` codimension-three branch, the transverse Chow
germ is `Sym^m(A^3)` and has tangent dimension `binom(m+3,3)-1`, with
multisymmetric generators of degrees one through `m`. The degree-at-least-two
generators are genuine singular Chow directions missed by the ordered reduced-
branch cover. On embedded or split branches the traced obstruction equation is
`m_k rho_k(B)=0`, and point-supported edges cannot change it. But an
arbitrary relative Chow branch can have linear base coupling to higher
multisymmetric generators, so the absolute tangent calculation does not extend
the dense-open obstruction to all Chow tangents. No full base direction is yet
constructed. Its endpoint cycle classes must be horizontal separately; the
next finite tests are the common positive/negative semiregularity rank and the
differential of an explicit rational-equivalence incidence.

## Cycle 202 generically nonreduced graph-support obstruction

For every `m>0`, the automorphism `(x,y) -> (x,y-ax)` pulls
`X x V(z_1^m,z_2,z_3)` back to an explicit codimension-three lci
`Z_(a,m)` supported on `Gamma_a`, with generic length `m` and fundamental cycle
`m[Gamma_a]`.  Applying this construction with lengths `|c_k|` realizes both
Cycle 169 projector endpoints as generically nonreduced scheme unions. For an
arbitrary generic graph thickening of length `m`, semiregularity sends its
embedded KS obstruction to `m` times the graph cycle-class obstruction. Cycle
152 identifies the latter with the same rank map and kernel as `rho_a`; hence
in characteristic zero a lift forces `rho_a(B)=0`. Componentwise restriction gives exactly the
same common-kernel bound as for reduced support. Both explicit endpoints have
zero PEL image because each contains a nonunit graph. Nilpotents enlarge only
the vertical Hilbert tangent; no Hodge result is claimed.

## Cycle 201B clean-union smoothing gate

For any connected reduced clean union `Z=union G_a` of codimension-three
graphs, restriction to the dense branch opens gives
`im(T_[Z] Hilb(A/S) -> T_0S) subset intersection_a ker(rho_a)`. The clean
smoothing module and gluing terms are supported on the multiple locus, so they
cannot cancel a normal Kodaira--Spencer class on a dense graph open. This stays
true when the general support is smooth and geometrically irreducible. Every
endpoint union retaining a nonunit transformed graph therefore has zero PEL
tangent image; `Gamma_I union Gamma_diag(3,1,1)` has image dimension at most
one. Signed endpoint equality cancels only after semiregularity, while the pair
space imposes both endpoint conditions separately. A common graph bridge only
adds kernel conditions. The next support must already be generically
irreducible at the special fiber, be generically linked/nonreduced, or be
genuinely non-graph. This is an embedded-smoothing statement; an arbitrary
Chow tangent not induced by a Hilbert family is not identified with it.

## Cycle 201 retract-natural obstruction audit

The exact retract formula is `o_v(E)=p[2]o_v(C)i`; it shows that retracts of
unobstructed objects are unobstructed, but a nonzero ambient obstruction may
live wholly on the complementary summand.  Categorical trace and Hochschild
semiregularity factor through `ch(E)` and vanish in the relevant degree for
every object of projector class `xi`, including the known obstructed split
object.  Projector-inserted trace has the same failure, while retaining the
untraced corner merely recovers the unknown raw obstruction.  Central
idempotents cannot separate vertices: `End^0(F_k)=C` and every pair has nonzero
`Ext^3`, forcing all central idempotent scalars to agree.  Deformation-category
base change repackages raw liftability but does not make it K-theoretic.  Thus
the four proposed categorical devices cannot close the Karoubi boundary; a
classification of noncentral splitting projectors would be new required input.

## Cycle 200 graph triangulated-envelope hostile audit

The Cycle 199 cross-Ext computation closes the finite twisted-complex envelope.
Every cross group lies in degree three; after shifts, a directed cycle of
degree-one arrows would force `3m=m`. Hence each finite graph-sheaf twisted
complex has an acyclic vertex filtration, and no cross-path or higher
`A_infinity` operation can return to alter a diagonal degree-two obstruction.
The nonzero projector coefficients retain nonzero multiples of the individual
normal obstructions. A stronger thick-category argument remains unproved:
generic-open restriction can kill the global `H^1(N)` class, and an arbitrary
Karoubi summand need not preserve the vertex filtration. K-additivity and
cohomological cancellation alone decide neither raw Atiyah vanishing nor this
retract boundary.

## Cycle 199 nontransverse graph extensions

For `F_0=O_(Gamma_I)` and `F_1=O_(Gamma_diag(3,1,1))`, the clean intersection
is four copies of `E_i^2`, with excess rank two and one transverse normal line.
The cross algebra on each component is
`tau Lambda(h_1,h_2,e_1,e_2)`, giving global dimensions
`4(1,4,6,4,1)` and `Ext^2=C^16`. A nonzero `Ext^1` class gives the smallest
ordinary nonsplit extension; an `Ext^2` class gives the smallest shifted cone
using the requested group. Their `K_0` classes are respectively
`[F_0]+[F_1]` and `[F_0]-[F_1]`, so their pure Weil coefficients are fixed at
`4` and `-2`. The opposite degree-one product is zero
because it squares the unique transverse generator. Independently of this
product, cross corrections vanish away from the double locus. Restriction to
the two dense graph opens forces both graph equations; their common PEL kernel
is one-dimensional. Every such extension/cone therefore has Atiyah rank at
least eight and cannot pass the rank-zero deformation gate.

## Cycle 197 Appell--Humbert complete-intersection no-go

For a divisor class with Hermitian matrix `R`, the PEL Beltrami tangent
`mu_B=[[0,B],[Q^-1 B^t,0]]` preserves type `(1,1)` exactly when `mu_B^t R` is
symmetric. Requiring this for all nine complex PEL directions has real rank 35
on `Herm_6(C)`, leaving only the polarization line generated integrally by
`P=diag(1,1,1,1,1,3)`. None of the rank-one Cycle 196 graph-divisor classes
lies on this line. Changing to smooth effective sections in the same line
bundles cannot alter the obstruction. Simultaneous preservation of the three
divisors for `Gamma_(u^k)` has base dimensions `3,0,0,0,0,0,0`; hence either
signed Cycle 196 collection has common base zero. More generally, every triple
intersection of full-base relative divisor classes is a multiple of `P^3`,
whose Weil projection is zero, so no rank-nine signed smooth
complete-intersection pair can represent `D_0 alpha_0`.

## Cycle 196 finite-type rational-equivalence correction

Fixing `d_+` and `d_-` makes the ambient product of effective Chow spaces
finite type, but does not make the locus `[Y^+]-[Y^-]=D_0 alpha_0` finite type.
After cross-adding the fixed pair, the endpoints have common degree
`D=d_++d_-=8387930766330029152`.  Rational equivalence is parametrized by a
countable union of finite-type endpoint incidences `R_(e,n,h)`, with auxiliary
effective degree `e` and a chain of `P^1` maps of degrees `h` in
`Chow_(D+e)`.  Fixed endpoint degree gives no known uniform bound on these
data.  Chow connected components yield algebraic, not rational, equivalence.
Accordingly, production requires one explicit witness stratum; a universal
negative result requires explicit complexity bounds or a uniform obstruction
over every stratum.

## Cycle 170 Pontryagin connected-representative obstruction

For scalar graphs in `A=E_i^3 x E_i^3`, the group law gives the exact Chow
identity `Gamma_a*Gamma_b=N(a-b)^3[A]` for `a!=b`, while
`Gamma_a*Gamma_a=0`.  Applying this to the denominator-cleared Cycle 169 class
`Z=sum_k c_k Gamma_(u^k)` gives
`Z*Z=-104188231402289079266552000000000000[A]`.  The Pontryagin square of any
effective three-cycle is a nonnegative multiple of `[A]`, so no effective,
hence no connected effective, cycle is rationally equivalent to `Z`.  The
seven graph classes are also cohomologically independent by the seven-sector
Vandermonde matrix, so theorem-of-cube manipulations cannot create a graph-only
relation.  New connected positive/negative representatives remain logically
possible, but adding a common bridge does not improve their componentwise
relative Chow obstruction.

## Cycle 168 full prime-Hecke trace

For all PEL maximal-isotropic prime-Hecke kernels, the exact sheet count is
`(p+1)(p^3+1)(p^5+1)` at inert primes and `sum_r [6 choose r]_p` at split
primes, both asymptotic to `p^9`. Every raw diagonal pushforward has normalized
degree `16p^3`, so the integral effective trace has degree `16p^3 N_p`,
asymptotic to `16p^12`. Weight normalization has degree `16N_p` and exact
denominator `p^3`; Hecke averaging has degree 16 but exact denominator
`N_p p^3` on the fine disjoint correspondence. The Weil projector commutes
with every PEL isogeny, so the exceptional projection is the direct sum of the
nonzero transported seed projection; under sheetwise middle-weight
identifications it is `N_p alpha`, or `alpha` after averaging. Thus full trace
creates no cancellation and no bounded integral Chow complexity.

## Cycle 168 full-Hecke normalization gate

For any transported diagonal image `Y`, with `eta=m^3/deg(f|Gamma)`, one has
`chi(M|Y)=16 eta` and `m^-3 f_*[Gamma]=eta^-1[Y]`; primitivity makes the latter
denominator exact. If a fixed `D` clears any positive rescaling and
`D Z=k[Y]`, then `deg(D Z)=16 k eta>=16 eta`. Thus unbounded inert primes,
where every PEL kernel has `eta>=p`, forbid simultaneous bounded degree and
uniform denominator. Full-correspondence averaging only adds its branch-count
denominator. The surviving candidate is not a Hecke saturation but a fixed-
degree product of two relative Chow spaces through an effective pair whose
difference is a fixed multiple of the projected seed and whose component has
rank-nine tangent image with vanishing obstructions; the obvious projector
pair does not acquire this property from cohomological cancellation.

## Cycle 167 hostile arbitrary-chain audit

The Cycle 166 chain survives, but its definition of `widetilde K` was not
literally well typed: `K` lies in `p^-1 Lambda_0/Lambda_0`, not in
`Lambda_0/pLambda_0`, until multiplication by `p` identifies the two.  The
clean definition is `Lambda_1=q^-1(K)` for the quotient map from
`p^-1 Lambda_0`.  Maximal isotropy proves integrality and preserves the exact
ambient type locally; it also preserves the carried type `(2,2,4)`.  Finite
local data globalize by adelic lattice intersection, while an infinite-support
word means a chain of finite prefixes, not one global finite-index lattice.
Multiplication by `p^r` explicitly proves the claimed two-class polarized
periodicity.  Thus the flaw is notation/domain ambiguity, not a counterexample
to the chain or its degree formulas.

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

## Main-funnel cycle 167

Polarization volume 16 gives exactly four threefold types: `(1,1,16)`,
`(1,2,8)`, `(1,4,4)`, and `(2,2,4)`.  The complete abstract prime-two
maximal-isotropic transition matrix is computed in
`cycle-167-volume-16-types-and-idempotents.md`; good odd-prime completely
adapted steps preserve exact type.  Poincare reducibility shows that one
threefold already forces a complementary projector, so an unqualified second
factor need not cut `Z_16` further.  A smaller special locus requires projector
algebra strictly larger than the single-decomposition algebra, measured by its
Peirce components or repeated-isotypic matrix block.  Fixed integral Peirce
data give a proper ambient locus; an unspecified extra Hom condition is only a
countable union until bounded.  Ambient properness follows from generic
endomorphism field `Q(i)`, but strictness inside every component of `Z_16`
remains unproved.  No Hodge-conjecture result is claimed.
