# Cycle 191: the natural mod-49 Kummer extension separates the collision

Let

\[
 E:y^2+xy=x^3+1,\qquad P=(0,1),\qquad Q=(-1,1),
\]

and recall

\[
 L_0=\mathbf Q(E[7],7^{-1}P,7^{-1}Q).
\]

The next natural finite extension carrying one more 7-adic layer of both the
linear representation and the two Kummer classes is

\[
 \boxed{L_1^{\rm Kum}=\mathbf Q(E[49],49^{-1}P,49^{-1}Q).}
 \tag{191.1}
\]

It contains `L_0`: multiplying a chosen 49-division point of `P` or `Q` by
seven gives a 7-division point, and `E[7]` is contained in `E[49]`. This is the
minimal natural simultaneous mod-49 lift. Adjoining division points for a
larger Selmer basis would give a Selmer-saturated variant, but is unnecessary
for testing the Cycle 190 pair. The superscript distinguishes this canonical
Kummer lift from the unrelated minimal quadratic separator denoted `L_1` in the
Cycle 191 reciprocity-obstruction note.

## Computable Frobenius signature

Choose a basis of `E[49]` and compatible division points of `P,Q`. For every
good prime `q` away from `7*433`, Frobenius in `L_1^{Kum}` is represented by

\[
 g_q=(\kappa_P(q),\kappa_Q(q),A_q)
 \in E[49]^2\rtimes\operatorname{GL}_2(\mathbf Z/49\mathbf Z).
 \tag{191.2}
\]

The intrinsic signature is the conjugacy class

\[
 \boxed{\Sigma_{49}(q)=[g_q]_{\rm conj}.}                 \tag{191.3}
\]

It is finite and computable: compute the action on the roots of the 49-division
polynomial and on the two 49-division torsors, then apply the semidirect-product
criterion

\[
 A'=BAB^{-1},\qquad
 (\kappa'_P,\kappa'_Q)\equiv
 B(\kappa_P,\kappa_Q)\pmod{(I-A')E[49]^2}.
 \tag{191.4}
\]

A cheaper fail-fast shadow, sufficient here, is

\[
 \sigma_{49}(q)=
 \left(q\bmod49,\,a_q\bmod49,\,
 E(\mathbf F_q)/49E(\mathbf F_q),\,[P],[Q]\right).       \tag{191.5}
\]

The first two entries are the determinant and trace of `A_q`. The last three
are obtained without constructing `L_1`, using the canonical finite-field
Kummer identification

\[
 \operatorname{coker}(A_q-I\mid E[49])
 \simeq E(\mathbf F_q)/49E(\mathbf F_q).
\]

Equality of (191.5) is necessary, not generally sufficient, for equality of
the full conjugacy classes (191.3). A mismatch in either trace or determinant
is a rigorous separation certificate.

## The Cycle 190 primes separate

Exact point counts give

| `q` | `q mod 49` | `#E(F_q)` | `a_q` | `a_q mod 49` | `v_7(#E(F_q))` |
|---:|---:|---:|---:|---:|---:|
| 1499 | 29 | 1526 | -26 | 23 | 1 |
| 29023 | 15 | 29050 | -26 | 23 | 1 |

For an elliptic curve, the determinant of the mod-49 Frobenius action is the
mod-49 cyclotomic character:

\[
 \det A_q=q\pmod {49}.
\]

Therefore

\[
 \det A_{1499}=29\ne15=\det A_{29023}\pmod {49}.
\]

Determinant is invariant under conjugacy. Hence

\[
 \boxed{\operatorname{Frob}_{1499}\not\sim
 \operatorname{Frob}_{29023}\text{ in }
 \operatorname{Gal}(L_1^{\rm Kum}/\mathbf Q).}
 \tag{191.6}
\]

In fact they are already nonconjugate in the subextension `Q(E[49])`; no
maximal-image assertion for the full mod-49 Kummer group is needed. Thus the
Cycle 190 collision is specific to the residual field `L_0` and does not survive
the first natural 7-adic lift.

## Exact local mod-49 divisibility

At both primes `v_7(#E(F_q))=1`. Consequently

\[
 E(\mathbf F_q)/49E(\mathbf F_q)\simeq\mathbf Z/7\mathbf Z,
\]

not `Z/49`; the local group has no second 7-primary layer. The class of `P`
is nonzero and hence generates, while the following exact witnesses prove
`Q-5P` is 49-divisible:

| `q` | `Q-5P` | `R_q` | checked identity |
|---:|:---:|:---:|:---:|
| 1499 | `(1249,657)` | `(805,1292)` | `49 R_q=Q-5P` |
| 29023 | `(16289,21235)` | `(433,28654)` | `49 R_q=Q-5P` |

Thus the exact ordered local Kummer row remains `[1:5]` at both primes, and
for integers `a,b`,

\[
 aP+bQ\in49E(\mathbf F_q)
 \iff a+5b\equiv0\pmod7.                                  \tag{191.7}
\]

The local Kummer coordinates therefore do not separate this pair; the mod-49
cyclotomic determinant does. This distinction is useful: lifting only the
translation row would retain the collision locally, whereas lifting the full
Selmer representation necessarily includes `E[49]` and separates it.

Reproduce the finite arithmetic with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle191_mod49_extension.py
```
