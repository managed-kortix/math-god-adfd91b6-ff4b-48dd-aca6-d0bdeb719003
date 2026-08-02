# Cycle 243: structural reduction before the F242 enumeration

## Scope and fixed input

Write

\[
 \mathcal B=\{0,1,-1,i,-i\},\qquad
 \mathcal L=M_{6\times3}(\mathcal B),\qquad n=|\mathcal L|=5^{18}.
\]

Cycle 248 now prints the three elliptic quotient maps, the degree-eight
isogeny to `E_i^3`, the resulting map `phi`, its differential, and the integral
curve class

\[
 \gamma=2(\eta_2\eta_3+\eta_1\eta_3+\eta_1\eta_2).
\]

The statements below are the choice-independent reductions that precede the
enumeration.  The remaining uninstantiated fixed geometric input is the
projective difference scheme in the chosen charts.

## Exact classification of the maps

For `L=(L_1,L_2,L_3)` put

\[
 M_L=[L_1\ L_2\ L_3]:E_i^9\longrightarrow E_i^6,
 \qquad \Phi=\phi^3:C^3\longrightarrow E_i^9.
\]

Then `f_L=M_L Phi`. Thus labelled maps are classified by the 54 entries of
`M_L`, together with the fixed ordered decomposition of its nine columns into
three blocks. Let

\[
 \delta_\phi:C\times C\longrightarrow E_i^3,
 \qquad (p,q)\longmapsto\phi(p)-\phi(q),
\]

and let `D_phi` be its scheme-theoretic image. There is an exact
closed-immersion test:

1. the inverse image of `ker(M_L)` under `delta_phi^3` has exactly the diagonal
   `Delta_(C^3)` as its geometric points; and
2. for every `(p_1,p_2,p_3)`, the map

   \[
    \bigoplus_r T_{p_r}C\longrightarrow T_0E_i^6,
    \quad(v_1,v_2,v_3)\longmapsto
    \sum_r L_r d\phi_{p_r}(v_r)
   \]

   is injective.

The first condition is geometric injectivity and the second is unramifiedness.
Over the fixed characteristic-zero number field, a proper injective unramified
morphism is a closed immersion. Equivalently, one may replace both conditions
by the single scheme-theoretic assertion that the fiber product
`C^3 x_(A_0) C^3` is its diagonal. This replaces a Groebner calculation on a
large graph ideal by one fixed difference scheme and a family of linear
sections.

Assume, as the intended Abel--Jacobi isogeny map does, that `phi(C)` is not an
elliptic curve. Then `dim D_phi=2`. The dimension theorem gives two universal
necessary conditions:

\[
 \boxed{\operatorname {rank}_{\mathbb Q(i)}M_L=6},\qquad
 \boxed{\operatorname {rank}_{\mathbb Q(i)}L_r\ge2\quad(r=1,2,3)}.
\]

For the first, if `rank(M_L)=s<6`, the identity component of its kernel has
dimension at least `9-s`, and its intersection with `D_phi^3` has dimension at
least `6-s>0`; hence it contains nonzero differences and `f_L` is not
injective. Applying the same argument to one factor proves the block-rank
condition. These rank tests use only Gaussian elimination over `Q(i)` and must
be the first enumeration filters.

When `rank(M_L)=6`, the kernel has dimension three and its intersection with
`D_phi^3` is expected to be zero-dimensional. Closed immersion is then the
sharp condition that all of this finite intersection is concentrated on the
diagonal, with the correct scheme structure, followed by the displayed tangent
test. Merely checking full rank is not sufficient.

## Irregularity and the cohomology test

If the closed-immersion test passes, `Y_L` is isomorphic to `C^3`; therefore

\[
 q(Y_L)=h^1(C^3,\mathcal O_{C^3})=3g(C)=9.
\]

This distinguishes `Y_L` from a smooth abelian graph threefold, whose
irregularity is three. It does not, by itself, classify arbitrary reducible
graph unions or nonreduced graph thickenings. The separate test that `[Y_L]`
lies outside the seven-dimensional graph span is therefore essential and
cannot be inferred from irregularity.

For every labelled triple, whether or not it embeds, functoriality of proper
pushforward and addition gives

\[
 z_L=(L_1)_*\gamma*(L_2)_*\gamma*(L_3)_*\gamma=(f_L)_*[C^3].
\]

If `f_L` is a closed immersion this equals `[Y_L]`. A regular codimension-three
immersion has `ch_1(O_Y)=ch_2(O_Y)=0` and leading Chern character
`ch_3(O_Y)=[Y]`; hence

\[
 c_3(O_{Y_L})=2[Y_L],\qquad P_Wc_3(O_{Y_L})=2P_Wz_L.
\]

The exceptional test is consequently an exact exterior-algebra calculation.
Cycle 248 supplies `gamma` and the sharper 27-term abelian-image expansion
(245.12), so this part can now be instantiated.
Full rank is also necessary for a nonzero determinant-sector coordinate, so a
rank failure may be recorded before the 924-coordinate expansion.

## First-order deformation constraints

For a regular closed immersion, an embedded first-order lift in a PEL direction
produces a flat lift of its structure sheaf. Therefore vanishing of the
embedded-normal boundary in all nine directions implies vanishing of the
nine-column Atiyah obstruction of `O_(Y_L)`. The two matrices remain useful as
independent computations and as a check on conventions, but they are not two
independent necessary conditions for a passing embedded deformation.

Conversely, Atiyah vanishing alone need not produce an embedded lift. It is
the weaker derived-object condition. Neither first-order vanishing implies the
45 quadratic Maurer--Cartan equations, and the quadratic equations do not imply
an all-order algebraic family.

## A universal finite symmetry reduction

There is a choice-independent action

\[
 G=C_4\times S_3,
\]

where `S_3` permutes the three source factors and `C_4={1,-1,i,-i}` multiplies
all three matrices by the same unit. Source permutation leaves the image
unchanged. Global unit multiplication is a polarization-preserving ambient
automorphism commuting with the `Q(i)` action; it preserves closed immersion,
irregularity, graph-span nonmembership, nonvanishing of the Weil projection,
and the ranks and solvability of all deformation systems. Hence every F242
gate is constant on `G`-orbits.

Burnside's lemma gives the exact number of labelled-triple orbits:

\[
 \boxed{N_G=\frac{n^3+3n^2+5n+15}{24}},\qquad n=5^{18}.
\]

For `(u,sigma)`, each cycle of length `ell` in `sigma` contributes `n` choices
when `u^ell=1` and only the zero matrix otherwise. This proves the formula and
also gives every stabilizer test. An implementation can canonicalize a triple
among its 24 transforms and print its stabilizer; orbit sizes then sum exactly
to `5^54`. This is only a factor-24 reduction, but it is rigorous and free.

There is also a larger universal monomial action
`(C_4 wr S_3) x S_3`: signed permutation matrices on the six ambient
coordinates act on the left of every `L_r`, while the last factor permutes the
three sources. It preserves the coefficient box, closed immersion, and the
unprojected cohomology class up to ambient automorphism. It may be used for the
full F242 gate only after the fixed polarization and `P_W` are checked to be
equivariant under each retained row operation. With weights
`(1,1,1;1,1,3)`, arbitrary row permutations do not preserve the PEL datum, so
using the whole wreath product without this stabilizer check would be invalid.

Further reduction by `Aut(C)^3` is allowed only after `phi` is explicit. One
must print the affine identities

\[
 \phi\circ a=T_a\phi+t_a
\]

and retain only automorphisms for which right multiplication by `T_a`
preserves the norm-one matrix box. The translations merely translate `Y_L`,
but omitting them would make the asserted action incorrect.

## Outcome

There is no choice-independent universal obstruction that rejects every
full-rank triple: at rank six the difference intersection is zero-dimensional
and depends on the explicit Cycle 248 map `phi`. The cheap rigorous
preprocessing is:

1. use the certified Cycle 248 `phi`, `dphi`, and `gamma`, and construct its
   projective difference scheme `D_phi`;
2. quotient by `C_4 times S_3` (and only then by any certified curve symmetry);
3. reject total rank below six or a block rank below two;
4. perform the finite difference-scheme and tangent closed-immersion tests;
5. only for survivors expand the graph-span and exceptional coordinates, then
   compute the embedded-normal/Atiyah and quadratic systems.

The quotient-map defect is closed by Cycle 248.  F242 remains computationally
`INCOMPLETE`, not `FAIL`, until `D_phi` and the finite enumeration and
deformation calculations are completed.
