# Routes

## Active gate: fixed-degree relative Chow production

For the Cycle 151 seed `alpha_0=P_Weil[Gamma]` on
`A_0=E_i^3 x E_i^3`, use `D_0=930187500000000000`.  Since
`deg(Gamma_(u^k))=(1+5^k)^2(1+3*5^k)`, freeze the two polarization degrees to
the exact degrees of the Cycle 169 pair:
`d_+=6072151396206990896` and `d_-=2315779370123038256`.  The product of the
resulting relative Chow spaces is a finite-type ambient pair space over the
nine-dimensional PEL base.  Produce an effective pair `(Y^+,Y^-)` such that

1. `[Y^+]-[Y^-]=D_0 alpha_0` in `CH^3(A_0)`, with an explicit rational
   equivalence;
2. its relative Chow germ maps onto all nine PEL tangent directions; and
3. a rank-nine first-order lift extends through second order.

The rational-equivalence condition is not itself known to be finite type at
fixed endpoint degrees.  It is the countable union of finite-type incidences
`R_(e,n,h)` parametrizing an auxiliary effective cycle and a chain of rational
curves in the degree-`d_++d_-+e` Chow scheme.  Thus a positive certificate must
give one explicit incidence witness.  A negative certificate must either give
explicit uniform bounds on `(e,n,h)`, reducing to a finite union, or obstruct
every incidence stratum uniformly; connected components detect only algebraic
equivalence and do not suffice.  The transformed-graph pair has rank zero, and
no single effective cycle can represent the signed class, so a positive
certificate must introduce genuinely new support.  This is a production gate,
not the Hodge conjecture.

The Cycle 196 divisor-cube decomposition does not supply that support. Cycle
197's Appell--Humbert calculation shows that the only integral divisor classes
remaining `(1,1)` over the full PEL germ are multiples of the polarization
`P`. Full-base triple intersections therefore span only `P^3`, which has zero
exceptional Weil projection. The particular graph-divisor triples have common
base dimensions `3,0,0,0,0,0,0`. Thus smooth effective replacements in the
same line bundles cannot yield the required rank-nine pair; the active search
must leave the fixed-line-bundle complete-intersection architecture.

## Cycle 198 vector-bundle classification

An unpinned request for a bundle on the geometric generic fiber with nonzero
exceptional `c_3` projection is not a new gate. It is equivalent to algebraicity
of the Weil classes: `c_3` is already algebraic, while rational Chern character
identifies algebraic `K_0` with rational Chow. For the converse, lift a pure
codimension-three Chow class to `[E]-[F]`; equality of rank, `c_1`, and `c_2`
gives `ch_3(E)-ch_3(F)=(c_3(E)-c_3(F))/2`.

The non-equivalent bounded replacement is to pin one independently constructed
special-fiber object `E_0` and compute the nine-column Atiyah obstruction map
`T_0S -> Ext^2(E_0,E_0)`. Rank zero is necessary for all-direction deformation
but is neither implied by Hodge algebraicity nor sufficient for generic
algebraicity; nonzero rank rejects only the chosen object. The next candidate
must be a non-split, nontransverse extension with an explicit locally free
resolution, since transverse graph extensions
cannot alter the degree-two obstruction.

Cycles 199--200 upgrade the last statement from ordinary extensions to every
finite twisted complex on the seven transformed graph vertices. Cross-Ext is
concentrated in degree three, so the degree-one cross-arrow quiver is acyclic;
no cross-path or higher `A_infinity` product can return to cancel a diagonal
degree-two obstruction. The nonzero projector coefficients then force a
nonzero graph obstruction. This does not yet close arbitrary retracts in the
idempotent-complete thick category: generic-open localization can kill the
global `H^1(N)` class, and K-additivity sees only the already-cancelled
semiregularity image. Finite-cone candidates must add new or nontransverse
support; closing the Karoubi boundary requires a new categorical theorem.

Cycle 201 shows exactly what that theorem cannot be. For a retract
`E --i--> C --p--> E`, Atiyah naturality gives
`o_v(E)=p[2]o_v(C)i`, but a nonzero ambient obstruction can lie on the
complementary summand. Trace and ordinary Hochschild semiregularity factor
through the Chern character and vanish on the horizontal class `xi`. The
graph-generated category has no vertex-separating central idempotents because
all pairwise `Ext^3` groups are nonzero. Thus only projector-sensitive,
untraced information could close the boundary, and that information is
presently just the unknown raw Atiyah corner itself.

Cycle 202A shows that Fourier--Mukai transport changes presentation, not this
gate. Untwisted graph sheaves transform to shifted sheaves on annihilator
threefolds. After tensoring by a relative ample line bundle they transform to
full-support vector bundles, and the projector object becomes a bounded bundle
complex whose `ch_3` is the cohomological Fourier transform of the same nonzero
exceptional class. But a relative Fourier--Mukai equivalence conjugates the
raw Atiyah obstruction in `Ext^2`; its kernel and rank are unchanged in every
PEL direction. Thus a dense-branch obstruction becomes a full-support
endomorphism-valued bundle obstruction, not a cancelable one. The Karoubi gap
is likewise transported rather than closed.

Cycle 201B closes reduced clean-union smoothings as the immediate geometric
escape. For `Z=union G_a`, restriction to each dense branch open forces the PEL
tangent into `intersection ker(rho_a)`; clean smoothing and gluing modules are
supported on the multiple locus. This holds even if the general support is
smooth and geometrically irreducible. Any endpoint retaining a nonunit
transformed graph has zero PEL image, while the smallest nontransverse pair has
image dimension at most one. Signed endpoint equality cancels semiregularity
images, not the separate endpoint deformation conditions. The search must use
support already generically irreducible at the special fiber, a generically
linked/nonreduced object, or genuinely non-graph support.

Cycle 203 closes the first Ferrand-double version of the nonreduced escape. For
each fixed Hilbert polynomial these doubles form the locally-free open in
`Quot(O_G^3,P_L)`. Local universal equations give a canonical Atiyah block
`(A_r tensor I_3)rho_G` with `det A_r=+/-2`; its rank-zero equations eliminate
to the unit ideal for both `Gamma_I` and `Gamma_diag(3,1,1)`, separately and as
a pair. Extra quotient-line obstruction rows cannot restore rank zero. More
complicated non-Ferrand generic support or a genuinely Chow-only tangent is
still required.

Cycle 202 tests the generically linked escape in its strongest common-envelope
form. Link each graph `Gamma_k` inside three general divisors of class `mP` and
write the connected residual as `R_k`; then the exact Chow identity is
`[R_k]=m^3P^3-[Gamma_k]`. This gives effective residual endpoints with new
support and an explicit rational equivalence, but both endpoint degrees rise by
the same positive auxiliary degree. More decisively, `P^3` is horizontal, so
the residual semiregularity condition is exactly the graph condition with the
opposite sign. Its PEL tangent potential has dimensions `(3,0,0,0,0,0,0)`,
and each endpoint contains a nonunit residual, forcing the explicit
decomposition-preserving liaison germ to have pair tangent image zero. This
does not exclude extra branches of the ambient Chow germ that destroy the
residual decomposition. Common ample linkage changes support but does not
improve the tangent gate in its natural incidence.

Cycle 203 tests the smallest non-complete-intersection refinement: homogeneous
height-three Gorenstein centers defined by the five Pfaffians of a `5 x 5`
alternating matrix with entries in one fixed system `|mP|`. Containment of
`Gamma_I` or `Gamma_diag(3,1,1)` is the quadratic rank-at-most-two condition on
the restricted alternating matrix; ten pivot charts give explicit local
parameters and residual colon ideals. The canonical liaison sheaf has
`[E_G]=[O_W]-[O_G]` and `ch_3(E_G)=5m^3P^3-[G]`, so it is rank zero with nonzero
exceptional projection. But `P^3` is horizontal, and its first semiregularity
obstruction is exactly the negative graph map, of rank `6` for `Gamma_I` and
`8` for `Gamma_D`. These ranks are independent of every Pfaffian parameter;
the rank-zero ideal, even after saturation by the proper-link open conditions,
is the unit ideal. Weighted Pfaffian systems with nonhorizontal center class
remain outside this bounded no-go.
