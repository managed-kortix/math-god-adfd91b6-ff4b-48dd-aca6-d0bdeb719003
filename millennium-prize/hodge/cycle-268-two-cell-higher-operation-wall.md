# Cycle 268: two-cell higher-operation theorem and AKS wall

## Verdict

The proposed blanket assertion is false.  For a one-arrow two-cell packet,
higher products cannot change the Maurer--Cartan equation, but they can change
both the twisted endomorphism differential and the transferred
Atiyah--Kodaira--Spencer representative.  The retained geometry determines the
graded Ext groups and `m_2`, but not the first products which can make those
changes.  The terminal output is therefore

`MIN2-AKS-WALL`.

This is a missing-structure wall, not a survival or cancellation result.

## The two-cell truncation theorem

Fix a minimal `A_infinity` model, use the unsuspended convention
`deg(m_n)=2-n`, and let

\[
 A=F_i[0],\qquad B=F_j[s],\qquad
 q\in\operatorname {Hom}^1(A,B).
\]

Thus the unshifted Ext degree of `q` is `p=s+1`.  Regard `q` as the only
strictly upper-triangular entry of the twisting matrix.

**Theorem 268.A.**

1. The complete Maurer--Cartan sum is zero in every minimal model:
   `m_1(q)=0`, and every `m_n(q,...,q)` for `n>=2` is zero because two
   consecutive copies of `q:A->B` are not composable.
2. For a homogeneous endomorphism `f`, the twisted differential has only
   `m_1`, the two binary terms, and possibly

   \[
   m_3(q,f,q),\qquad f:B\longrightarrow A.                 \tag{268.1}
   \]

   No `m_n` with `n>=4` can occur: with only one distinguished input `f`, such
   a word necessarily contains two consecutive copies of `q`.
3. On the boundary map `End^1(T_q)->End^2(T_q)`, (268.1) can occur only for a
   self-arrow with `p=1` or `p=2`.  Indeed a reverse degree-one map has
   unshifted degree

   \[
   \deg_{Ext}(f)=1-s=2-p.
   \]

   Negative Ext groups vanish.  In a strictly unital model the `p=2` case is
   also zero, because its reverse space is `Ext^0=K1` and every higher product
   containing a unit vanishes.  Hence only the self `Ext^1` stratum can have a
   genuine ternary correction to this boundary map.  The self `Ext^2` through
   `Ext^6` strata and every cross stratum (`p=3`) cannot.  This does not remove
   their independent Atiyah-transfer problem.

The theorem proves the maximal higher-product truncation; it does not prove
that the surviving `m_3` is zero.

For the mandatory Cycle 266 packet

\[
 q=\alpha=a_1a_2:F_0[0]\longrightarrow F_0[1],
 \qquad G=1:F_0[1]\longrightarrow F_0[0],
\]

the only shape-allowed ternary term is

\[
 \mu_\alpha:=m_3(\alpha,1,\alpha)
 \in\operatorname {Ext}^3(F_0,F_0),                         \tag{268.2}
\]

viewed as the total-degree-two `A->B` corner.  Thus the strict identity becomes

\[
 d_\alpha(G)=
 \alpha|_A+\alpha|_B+\mu_\alpha                           \tag{268.3}
\]

up to the fixed convention signs.  Binary geometry computes the first two
terms.  Moreover, `G` is the shifted strict unit, so strict unitality gives
`\mu_\alpha=0`.  Consequently higher multiplications do **not** alter the
Cycle 266 boundary identity.  What remains unknown for that packet is whether
the actual geometric obstruction is the displayed diagonal class: the
one-`q` transfer term below need not vanish by strict unitality.

## One `q` plus the deformation insertion

Let `\Theta_v` denote a coherent Hochschild/`A_infinity` representative of the
Atiyah--Kodaira--Spencer natural transformation for a PEL tangent vector `v`.
Twisting the transformation by the packet gives

\[
 \Theta_v^q=
 \Theta_{v,0}|_A+\Theta_{v,0}|_B+\Theta_{v,1}(q).           \tag{268.4}
\]

There are no components whose ordinary morphism inputs contain two consecutive
copies of `q`.  The one-arrow term `\Theta_{v,1}(q)` is nevertheless allowed
and records deformation of the morphism, rather than only deformation of its
endpoints.

If the AKS class is represented as the product of an Atiyah insertion `At` and
a Kodaira--Spencer insertion `\kappa_v`, the same missing Taylor coefficient is
resolved into the composable ternary products with exactly one `q`, namely the
source-compatible members of

\[
 m_3(q,At,\kappa_v),\qquad
 m_3(At,q,\kappa_v),\qquad
 m_3(At,\kappa_v,q),                                      \tag{268.5}
\]

together with the endpoint binary products `m_2(At,\kappa_v)`.  Formula
(268.5), with object labels and shifts inserted, is the precise ``one `q` plus
deformation insertion'' datum.  Different transfer gauges redistribute these
terms between `\Theta_{v,1}` and the higher products, so they must be
transferred coherently; setting one part to zero while retaining the other is
not invariant.

Equivalently, in a first-order family of dg or `A_infinity` categories, the
linearized closedness equation for a lift of `q` contains the variation of the
structure maps applied to `q`.  This is the same one-`q` Taylor information as
(268.4), expressed without splitting the AKS class into `At` and `\kappa_v`.

## What geometry computes

The retained graph geometry gives

\[
 \operatorname {Ext}^*(F_k,F_k)=\Lambda(a_1,\ldots,a_6),
\]

the transverse cross groups concentrated in `Ext^3`, and all binary Yoneda
products.  It also gives the endpoint normal obstruction maps and, in the
translation-invariant exterior basis
`(h_1,h_2,h_3,n_1,n_2,n_3)`, the nine vertex classes

\[
 \rho_k(B)=Q^{-1}B^t-N(u^k)B.
\]

For the row-major tangent matrix `B_pq` these are

\[
 o_{k,pq}=Q_{qq}^{-1}h_p\wedge n_q-5^k h_q\wedge n_p,
 \qquad Q=\operatorname {diag}(1,1,3),                         \tag{268.6}
\]

with exact ranks `6,9,9,9,9,9,9` for `k=0,...,6`.

Therefore the endpoint `m_2` products and raw graph obstruction classes are in
principle fixed.  Strict unitality determines (268.2) to be zero, but these data
do not determine the nine one-arrow coefficients (268.4)/(268.5).  Higher
Massey products are not determined by the cohomology algebra, and `rho_k`
contains no deformation or homotopy data for the chosen chain representative
of `q`.

The exact indispensable input is consequently:

1. `m_3(q,f,q)` for the self `Ext^1` two-cell stratum; strict unitality kills
   this term on the self `Ext^2` stratum, including (268.2), and degree kills it
   on all remaining strata;
2. `\Theta_{v,1}(q)` for all nine PEL basis vectors and every `q` stratum, or
   equivalently all source-compatible products (268.5) in one declared dg
   enhancement;
3. the zero-input endpoint representatives `\Theta_{v,0}|_{F_k}` in the same
   transfer gauge, so that the resulting classes can be compared with
   `\rho_k`.

No explicit resolutions, contraction homotopy, chain-level AKS maps, or
formality-and-naturality theorem supplying these tensors occurs in the retained
dossier.  The binary exterior-algebra calculation cannot recover them.

## Terminal statement

**WALL 268.B (`MIN2-AKS-WALL`).**  Two-cell shape proves that all higher terms
in the Maurer--Cartan equation vanish and truncates the endomorphism differential
to at most the single ternary operation (268.1); degree and strict unitality
leave it only on the self `Ext^1` stratum.  They do not kill the one-`q` Taylor
coefficient of the transferred AKS transformation.  In particular, the
mandatory `q=a_1a_2` packet retains the strict Cycle 266 boundary identity, but
its actual nine obstruction representatives still require (268.4),
equivalently (268.5).  Until a concrete dg enhancement and transfer or an exact
compatible formality theorem supplies them, no
`MIN2-AKS-SURVIVAL`, `CANCELLATION`, or `MIXED` conclusion is admissible.
