# Cycle 71: component domination and semiregularity

## Generic domination theorem

Let `S` be a smooth finite-type scheme in characteristic zero, let
`f:H->S` be a proper relative Hilbert/Chow space, let `Z` be a reduced
irreducible component of `H`, and let `V` be a reduced irreducible marked Hodge
component. Assume the relative cycle gives a factorization

\[
Z\longrightarrow V\hookrightarrow S.                              \tag{71.1}
\]

Suppose there are smooth points `z in Z`, `s=f(z) in V` such that

\[
df_z:T_zZ\longrightarrow T_sV
\]

is surjective. Then

\[
\boxed{f(Z)=V.}                                                    \tag{71.2}
\]

Indeed, the map is smooth at `z`, hence open near `z`. Its image contains a
nonempty open subset of `V`. Properness makes the image closed, and
irreducibility forces equality. The reduced scheme-theoretic image is `V`; the
map of completed local rings is formally smooth and faithfully flat at the
chosen points.

Properness is needed only to upgrade dense domination to a closed/surjective
image. The substantive hypothesis is full differential rank, or an equivalent
generic fiber-dimension estimate. Equal source/target dimensions without fiber
control is insufficient.

## Relative obstruction criterion

For a smooth lci surface `Z subset X`, the normal sequence supplies the relative
embedded obstruction map

\[
\alpha_Z:T_{S,[X]}\longrightarrow H^1(N_{Z/X}).                   \tag{71.3}
\]

The incidence tangent image is

\[
\operatorname{im}(df)=\ker\alpha_Z.                               \tag{71.4}
\]

Bloch's semiregularity map is

\[
\sigma_Z:H^1(N_{Z/X})\longrightarrow H^3(\Omega_X^1),             \tag{71.5}
\]

and compatibility with infinitesimal variation of Hodge structure gives

\[
\beta_{[Z]}=\sigma_Z\alpha_Z.                                     \tag{71.6}
\]

Hence

\[
\ker\alpha_Z\subseteq\ker\beta_{[Z]}=T_{V,[X]},                  \tag{71.7}
\]

and the discrepancy of incidence and Hodge normal spaces is exactly

\[
\operatorname{im}(\alpha_Z)\cap\ker(\sigma_Z).                    \tag{71.8}
\]

If `sigma_Z` is injective on the actual relative obstruction image, then

\[
\ker\alpha_Z=\ker\beta_{[Z]},                                    \tag{71.9}
\]

so the incidence map has full differential rank onto the Hodge tangent space.
To pass from (71.9) to formal smoothness in singular settings, one still needs
the full Artin lifting statement: first-order exactness alone is not enough.

This isolates the active main-funnel lemma:

> Construct, on a dense open subset of a relative cycle component, a complete
> relative obstruction theory whose semiregularity map is injective on every
> actual obstruction, and prove the selected Hodge component generically
> smooth. Then the cycle component dominates that Hodge component.

The difficult input is existence of such a relative cycle component for an
arbitrary marked Hodge component. Semiregularity propagates a supplied cycle; it
does not manufacture one.

## Fermat degree-`d` plane calibration

For the Fermat degree-`d` fourfold and a correctly rooted plane, the normal
sequence is

\[
0\to N_{P/X_d}\to\mathcal O_P(1)^3
\xrightarrow{(u_0^{d-1},u_1^{d-1},u_2^{d-1})}
\mathcal O_P(d)\to0.                                                \tag{71.10}
\]

Therefore

\[
H^1(N_{P/X_d})\cong
{\mathbf C[u_0,u_1,u_2]_d\over
\sum_i u_i^{d-1}\mathbf C[u_0,u_1,u_2]_1},
\]

with dimension

\[
\boxed{h^1(N_{P/X_d})={d+2\choose2}-9.}                            \tag{71.11}
\]

In the Fermat Jacobian ring, the plane class is

\[
p_{P,d}=\prod_{i=0}^2
\left(\sum_{j=0}^{d-2}\alpha^jx_i^{d-2-j}y_i^j\right).            \tag{71.12}
\]

The semiregularity map is multiplication

\[
[q]\longmapsto[q p_{P,d}]\in R_{4d-6}.                            \tag{71.13}
\]

Pair multigrading proves injectivity for every `d>=3`. It identifies the Hilbert
obstruction space with the Hodge-normal image relevant to the plane, not with
all of `H^(1,3)`. At `d=4`, both relevant normal spaces have dimension six,
recovering Cycle 70.

## Hostile boundaries

None of the following separately implies domination:

- equality of tangent dimensions at a nonreduced point;
- injectivity or surjectivity of an auxiliary semiregularity map without a
  complete relative obstruction comparison;
- properness;
- equal source and target dimensions.

A constant map between smooth formal disks defeats unobstructedness without
differential rank; a thickened point defeats first-order tangent equality.

Cycle 71 supplies an exact promotion criterion and verifies it for the Fermat
plane family. It does not show that arbitrary Hodge components possess cycle
components, and therefore proves no case of the full Hodge conjecture.
