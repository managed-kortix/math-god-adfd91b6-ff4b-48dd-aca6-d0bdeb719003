# Cycle 202: generic graph thickenings retain the support obstruction

## Explicit endpoint schemes

Put

\[
 X=E_i^3,\qquad A=X\times X,\qquad u=2+i,
\]

and let `Gamma_k=Gamma_(u^k)`.  For an endomorphism `a` of `X`, the map

\[
 \phi_a:A\longrightarrow X\times X,
 \qquad (x,y)\longmapsto (x,y-ax)
\]

is an automorphism taking `Gamma_a` to `X x {0}`.

For every positive integer `m`, let `J_j` be the ideal of the origin in the
`j`-th elliptic factor and let

\[
 T_m=V(J_1^m,J_2,J_3)\subset X.
\]

Thus its ideal in product parameters at the origin is
`(z_1^m,z_2,z_3)`. It is the product of the length-`m` infinitesimal divisor at
the origin of the first elliptic factor with the origins of the other two
factors. Define

\[
 Z_{a,m}:=\phi_a^{-1}(X\times T_m)\subset A.                 \tag{202.1}
\]

This is an explicit codimension-three local complete intersection, finite flat
of degree `m` over `Gamma_a`, generically nonreduced when `m>1`, and

\[
 [Z_{a,m}]_{
 \rm cyc}=m[\Gamma_a].                                      \tag{202.2}
\]

Using the Cycle 169 coefficients

\[
(c_0,\ldots,c_6)=
(317131927490234375,-2073948378906250,12564289203125,
-56707735500,27598945,3626326,-68381),
\]

take the scheme-theoretic unions

\[
 \mathcal Z^+=\bigcup_{c_k>0}Z_{u^k,c_k},\qquad
 \mathcal Z^-=\bigcup_{c_k<0}Z_{u^k,-c_k}.                  \tag{202.3}
\]

Here union means intersection of the component ideals. Their generic
components have precisely the requested multiplicities, and
their fundamental cycles are the two projector endpoints `C_0^+` and `C_0^-`.
Intersections between distinct graphs can add lower-dimensional scheme
structure but do not alter these generic multiplicities.

## Conormal nilpotent layers

On the dense generic open of `Gamma_a`, write `R_m=O[epsilon]/(epsilon^m)`.
The nilradical filtration is

\[
 R_m\supset (\epsilon)\supset\cdots\supset(\epsilon^{m-1})
 \supset0,
 \qquad
 (\epsilon^j)/(\epsilon^{j+1})\simeq O_{\Gamma_a}.           \tag{202.4}
\]

Thus the reduced graph-normal contribution occurs once on each of the `m`
associated-graded sheets. The two other transverse equations and `epsilon^m`
make (202.1) a codimension-three complete intersection. If
`s=(s_1,s_2,s_3)` is the reduced normal KS value, its image in the lci normal
module is explicitly

\[
 L_m(s)=(m\epsilon^{m-1}s_1,s_2,s_3).                       \tag{202.5}
\]

This map is injective in characteristic zero. Hence these explicit
thickenings have exactly the reduced-support kernel. They add many vertical
embedded Hilbert directions but do not supply a negative copy of the scalar
support contribution.

For comparison, the isotropic thickening `V(I_G^r)` has

\[
 \operatorname {gr}O_{V(I_G^r)}
 =\bigoplus_{j=0}^{r-1}\operatorname {Sym}^jN_G^*,
 \qquad
 m=\binom{r+2}{3}.                                          \tag{202.6}
\]

Its first normal equation is the polarization map

\[
 D_r(s)(v_1\cdots v_r)
 =\sum_{j=1}^rv_1\cdots s(v_j)\cdots v_r.                  \tag{202.7}
\]

In characteristic zero `D_r` is injective (evaluate on `v^r`), recovering the
first-thickening calculation of Cycle 170.  The trace argument below applies
to arbitrary finite generic graph thickenings, not just powers of the graph
ideal or the curvilinear models (202.1).

## Exact traced Kodaira--Spencer obstruction

Let `Z` be a codimension-three subscheme whose only generic reduced support is
a smooth graph `G` and whose generic length along `G` is `m>0`. Its fundamental
cycle is `m[G]`. The trace (semiregularity) of the embedded KS obstruction is
the infinitesimal Hodge obstruction of that cycle, hence

\[
 \boxed{\sigma_Z(o_B(Z))=m\,\sigma_G(\rho_G(B)).}            \tag{202.8}
\]

For these graph embeddings, Cycle 152 identifies the contraction of the graph
class with the same rank map and kernel as the normal KS map. Thus
`sigma_G` is injective on `im(rho_G)`, and (202.8) gives the exact necessary
condition

\[
 \boxed{o_B(Z)=0\quad\Longrightarrow\quad m\rho_G(B)=0.}    \tag{202.9}
\]

Equivalently, (202.8) is the cycle-class trace of the Hilbert--Chow
differential. Nilpotent deformations can alter the trace-free embedded
obstruction, but not the fundamental cycle seen by this trace. Since the
ground field has characteristic zero, (202.9) implies

\[
 o_B(Z)=0\quad\Longrightarrow\quad\rho_G(B)=0.              \tag{202.10}
\]

The formula makes precise why nilpotent layers cannot cancel the obstruction.
They can enlarge the vertical Hilbert tangent, but every extension between the
conormal layers has the same cycle-class trace `m[G]`.

For several generically distinct graphs, restriction to their disjoint dense
opens and application of (202.9) component by component gives

\[
 \boxed{
 \operatorname {im}\bigl(T_{[Z]}\operatorname {Hilb}(\mathcal A/S)
 \longrightarrow T_0S\bigr)
 \subseteq\bigcap_a\ker\rho_a.}                             \tag{202.11}
\]

This does not require the total scheme to be reduced, clean at graph
intersections, finite flat over its reduction, or locally a power of a graph
ideal: the fundamental cycle and its semiregularity trace depend only on the
generic lengths. Lower-dimensional embedded defects are invisible to that
trace.

## PEL consequence

For the transformed scalar graphs,

\[
 \rho_k(B)=Q^{-1}B^t-5^kB,
 \qquad Q=\operatorname {diag}(1,1,3).
\]

Cycle 169 gives `dim ker rho_0=3` and `ker rho_k=0` for `1<=k<=6`.
Every endpoint in (202.3) contains a nonunit graph thickening.  Therefore

\[
 \boxed{\operatorname {im}(d p_{\mathcal Z^+})
 =\operatorname {im}(d p_{\mathcal Z^-})=0.}                \tag{202.12}
\]

More generally, a generically nonreduced scheme supported on one graph has no
larger PEL image than its reduced support, and a scheme supported generically
on several graphs is bounded by their common kernel.  Multiplicity signs do
not interact: positive and negative endpoints are separate effective Hilbert
conditions, while trace on either endpoint uses positive generic lengths.

Thus the explicit nilpotent candidates match all projector coefficients but
fail the rank-nine gate.  The support obstruction persists for every finite
generic thickening of graph support.  A viable continuation must have genuinely
new generic reduced support (or concern a Chow tangent not induced by an
embedded Hilbert family); lower-dimensional embedded nilpotents and graph
thickenings cannot suffice.  No Hodge-conjecture result is claimed.
