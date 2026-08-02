# Cycle 245: global punctured-support repair of the finite obstruction

## Post-audit status

The shift or cell spectral sequence alone does not prove the finite
twisted-complex obstruction. The exact return

\[
 F_i[0]\longrightarrow F_j[2]\longrightarrow F_i[4]
\]

survives every such reindexing as a possible later-page contribution. There is,
however, a proposed independent proof: restrict to the global punctured branch
before taking the leading supported semiregularity class. This kills every
cross return and retains the complete graph's normal `H^1`, but the printed
argument does not construct the required chain-level trace-and-edge map on the
raw Atiyah obstruction. Consequently the claimed repair is not established.

**Proposed Theorem 245.A (not established).** Let `D` be a finite twisted
complex formed from finite sums of shifts of

\[
 F_k=\mathcal O_{G_k},\qquad G_k=\Gamma_{u^k},\quad 0\leq k\leq6.
\]

If

\[
 [D]=\xi=\sum_{k=0}^6c_k[F_k]
\]

in the Grothendieck group of the graph-generated finite category, then some PEL
tangent vector `v` has `o_v(D) != 0` in `Ext^2(D,D)`.

The argument below does not currently prove this statement, so it cannot
restore `KI240 PASS`. This is not a Hodge-conjecture result.

## Why weight alone stops short

With

\[
 \operatorname {Hom}^d(F_i[r],F_j[s])
 =\operatorname {Ext}^{d-r+s}(F_i,F_j),
\]

a degree-one cross arrow has `s-r=2`. Hence opposite cross arrows can return to
the same vertex four shifts later, and their nonzero unshifted `Ext^6` product
has total degree two. A shift, cell, or bar filtration records positive weight,
but it supplies neither a vanishing differential nor a permanent-cycle
theorem. No corrected proof below relies on such a claim.

## The global punctured branch

Fix `k` and set

\[
 V_k=A_0\setminus\bigcup_{\ell\ne k}G_\ell,
 \qquad G_k^\circ=G_k\cap V_k.
\]

Distinct graphs meet in finite sets. The deleted subset of the smooth
threefold `G_k` therefore has codimension three. Since the normal bundle is
locally free, local-cohomology depth gives

\[
 H^q_{G_k\setminus G_k^\circ}(G_k,N_{G_k/A_0})=0\quad(q<3)
\]

and in particular

\[
 H^1(G_k,N_{G_k/A_0})
 \xrightarrow{\sim}
 H^1(G_k^\circ,N_{G_k^\circ/V_k}).                              \tag{245.1}
\]

This is the point of using the entire punctured branch rather than a small
affine generic open. The latter can kill `H^1`; (245.1) does not.

Restriction of `D` to `V_k` kills every cell supported on `G_ell` for
`ell != k`, and therefore kills every cross map and every shifted cross-return
product. The restricted object `D_k` is a finite twisted complex of shifts of
`O_(G_k^circ)`. Its supported Grothendieck class is

\[
 [D_k]=c_k[\mathcal O_{G_k^\circ}],                               \tag{245.2}
\]

because generic Euler multiplicity at `G_k` sends `[F_ell]` to
`delta_(k ell)`.

## Finite-cell leading-support lemma

The required comparison is narrower than the arbitrary-perfect-complex `PSC`
statement isolated in Cycle 241.

**Proposed Lemma 245.B.** Let `i:G -> X` be a smooth regular immersion, and let `P` be a
finite twisted complex of finite sums of shifts of `O_G`. If
`[P]=m[O_G]` in supported `K_0`, then

\[
 o_v(P)=0\quad\Longrightarrow\quad
 m\rho_G(v)=0\text{ in }H^1(G,N_{G/X}).                           \tag{245.3}
\]

**Incomplete proof attempt.** Use the Koszul resolution for the regular immersion and filter its
endomorphism complex by conormal degree. The leading normal edge of the
Atiyah--Kodaira--Spencer class of `O_G` is the usual normal deformation class
`rho_G(v)`. On a finite direct sum of shifted cells, the same edge applied to
the categorical supertrace is

\[
 \sum_a(-1)^{r_a}\rho_G(v)=m\rho_G(v).                            \tag{245.4}
\]

Passing from the direct sum to a twisted complex is claimed to add only
commutators with the twisting differential, whose supertrace is zero. But no
chain map from the raw endomorphism-valued obstruction complex to the punctured
normal `H^1` target is constructed, and no compatibility of its conormal edge
with the twisting differential is checked. Invoking naturality and additivity
of a supported Atiyah Chern character does not fill this gap: those are traced
invariants, while (245.3) requires a specific map sending the raw obstruction
class to `m rho_G(v)`. Thus (245.3) remains unproved.

The attempted proof uses an actual finite `O_G`-cell presentation. It does not assert
that an arbitrary perfect complex specified only by generic multiplicity has
such a filtration, and therefore does not assume the full `PSC` lemma.

## Conditional deduction

If Lemma 245.B were proved, suppose `o_v(D)=0`. Atiyah and Kodaira--Spencer classes commute with open
restriction, so `o_v(D_k)=0`. Applying Lemma 245.B to (245.2) gives

\[
 c_k\rho_k(v)=0
 \quad\text{in }H^1(G_k^\circ,N_{G_k^\circ/V_k}).                 \tag{245.5}
\]

By (245.1), this is equivalent to vanishing of the same class on the complete
graph. Every coefficient `c_k` is nonzero, and the previously computed normal
map

\[
 \rho_k(B)=Q^{-1}B^t-N(u^k)B
\]

is nonzero. Choose `k` and a PEL basis vector `v` with `rho_k(v) != 0`.
Characteristic zero and (245.1) would imply `c_k rho_k(v) != 0`, contradicting
(245.5). This deduction is conditional on the missing chain-level lemma and
does not establish `KI240`.

## Boundary

The proposed route would repair the finite graph-cell theorem retracted after
Cycle 244 if Lemma 245.B were supplied. It is designed to remove shifted cross
returns by restriction before applying the leading-support map, but that map is
the unproved step. It does not prove
the full arbitrary-perfect-complex `PSC` statement, does not cover genuinely
new generic support, and does not make the obstruction a function of ambient
`K_0` alone.
