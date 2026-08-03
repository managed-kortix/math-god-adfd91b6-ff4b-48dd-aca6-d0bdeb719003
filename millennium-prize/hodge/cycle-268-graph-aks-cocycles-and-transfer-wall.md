# Cycle 268: graph AKS cocycles and the two-cell transfer wall

## Exact vertex cocycles

Put `K=Q(i)`, `u=2+i`, `F_k=O_(Gamma_(u^k))`, and
`Q=diag(1,1,3)`. Choose

\[
 h_1,h_2,h_3\in H^1(O_{\Gamma_k}),\qquad
 n_1,n_2,n_3\in H^0(N_{\Gamma_k/A_0})
\]

as the degree-one generators in the translation-invariant Koszul/Dolbeault
splitting. Then

\[
 Ext^*(F_k,F_k)=\Lambda_K(h_1,h_2,h_3,n_1,n_2,n_3).
\]

For the row-major PEL tangent basis `B_pq`, `1<=p,q<=3`, Cycles 152, 169,
197, and 200 give

\[
 \rho_k(B)=Q^{-1}B^t-5^kB.
\]

Embedding `H^1(N)=H^1(O) tensor H^0(N)` in `Ext^2` gives the nine actual
geometric Atiyah--Kodaira--Spencer classes

\[
 \boxed{o_{k,pq}=Q_{qq}^{-1}h_p\wedge n_q-5^kh_q\wedge n_p.}       \tag{268.1}
\]

Thus the three diagonal columns are

\[
 o_{k,11}=(1-5^k)h_1n_1,\quad
 o_{k,22}=(1-5^k)h_2n_2,\quad
 o_{k,33}=(1/3-5^k)h_3n_3,
\]

and each off-diagonal column has the two terms displayed in (268.1). At
`k=0`, the first two diagonal columns vanish and the remaining seven columns
span a rank-six space; for `k=1,...,6`, the nine columns are independent.
These are the previously printed `rho_k` maps, now placed explicitly in the
15-dimensional exterior basis of `Ext^2`.

The complete exact sparse `9 x 9` normal matrices, `15 x 9` exterior matrices,
and all 63 column forms are in `cycle268_aks_cocycles.json`. Rational complex
scalars use numerator/denominator pairs for both real and imaginary parts.

## Sufficiency audit

This closes the missing vertex-coordinate issue but does not supply the full
input demanded by `H268-MIN2-AKS`. The retained Cycles 150--201 determine the
cohomology classes (268.1), self- and cross-Ext groups, and the binary Yoneda
products used later in Cycle 241. They do not determine:

1. representatives of (268.1) in one fixed dg enhancement or as cocycles in a
   transferred minimal `A_infinity` module;
2. the higher multiplications `m_r`, `r>=3`, on the seven-graph category;
3. the higher components of the Atiyah natural transformation and the
   homotopies transferring it to a twisted two-cell object.

Those data can contribute even with only two cells because a higher operation
may contain one obstruction insertion together with repeated copies of the
single Maurer--Cartan arrow. The strict compressed calculation is usable only
after a formality-and-transfer theorem showing that all such terms vanish or
after printing them from a common resolution. Neither theorem nor those
structure constants occurs in Cycles 150--201 (or in the later compressed Ext
artifact).

Therefore the exact disposition is:

`MIN2-AKS-WALL: vertex AKS Ext^2 classes are now explicit, but the transferred
Atiyah A_infinity-module operations for a two-cell twist are not determined by
the retained data.`

This is a missing-structure wall, not survival or cancellation, and it makes no
Hodge-conjecture or `KI240` claim.

Reproduce with

```sh
python3 millennium-prize/hodge/verify_cycle268_aks_cocycles.py --check
```
