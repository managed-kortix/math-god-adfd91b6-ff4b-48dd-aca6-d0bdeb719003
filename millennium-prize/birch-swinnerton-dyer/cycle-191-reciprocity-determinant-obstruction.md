# Cycle 191: fixed-`L_0` reciprocity/determinant obstruction

## Question isolated by the collision

Retain the objects and packet `A` of Cycle 190:

\[
 E=433\mathrm a1,\quad p=7,\quad P=(0,1),\quad Q=(-1,1),
 \quad \ell=29,
\]

\[
 L_0=\mathbf Q(E[7],7^{-1}P,7^{-1}Q).
\]

The collision is

\[
 q_0=29023,\qquad q_1=1499,
\]

\[
 \operatorname{Frob}_{q_0}(L_0)
 =\operatorname{Frob}_{q_1}(L_0)\quad\text{in }G_0^\#,
 \qquad \mathfrak c(q_0,29)=0,
 \qquad \mathfrak c(q_1,29)\ne0.                 \tag{191.1}
\]

Both Frobenius classes have the same nonidentity-unipotent linear part and the
same ordered projective Kummer row `[1:5]`. Thus (191.1) is not merely a
collision after forgetting the affine Kummer coordinates: it is a collision in
the full two-point Kummer field.

Consider a proposed explicit-reciprocity identity of the form

\[
 \iota_q\bigl(\mathfrak c(q,29)\bigr)=u_q D_q,                \tag{191.2}
\]

where `iota_q` compares the varying modular-symbol line with a fixed
determinant line, `u_q` is a nonzero normalization factor, and `D_q` is a
Selmer/Kummer localization determinant. Formula (191.2) is incompatible with
(191.1) whenever the vanishing of `D_q` is determined by
`Frob_q(L_0)`. This remains true if the units `u_q` and the line
trivializations vary arbitrarily: units preserve zero.

In particular, the collision rules out all of the following on the whole
packet `A`:

1. a scalar formula in which `D_q` is a class function of `G_0`;
2. a line-valued version whose determinant section has `L_0`-Frobenian
   vanishing;
3. a formula using only the residual matrix and the localizations of the fixed
   points `P,Q`, since these comprise precisely the full `L_0` conjugacy datum
   in the present nonidentity-unipotent fibre;
4. a repair by a nowhere-zero period, Manin, orientation, or local-torsion
   factor.

The collision does not contradict an explicit reciprocity theorem whose
determinant is built from an additional varying-twist global class. It says
that this extra class cannot itself be recoverable, even at the level of its
vanishing contribution, from the named field `L_0`.

## Minimal missing Galois datum

Let `xi(q)` be any extra finite datum proposed to supplement the `L_0`
Frobenius class. If the vanishing of `mathfrak c(q,29)` factors through

\[
 \bigl(\operatorname{Frob}_q(L_0),\xi(q)\bigr),              \tag{191.3}
\]

then (191.1) forces

\[
 \boxed{\xi(q_0)\ne\xi(q_1).}                               \tag{191.4}
\]

Thus the logically minimal missing datum is one binary separator on the
colliding `L_0` fibre. This is a lower bound on information, not a canonical
choice and not a sufficient governing datum.

There is a particularly small arithmetic realization. Put

\[
 \epsilon_5(q)=\left(\frac5q\right).
\]

Quadratic reciprocity and reduction modulo 5 give

\[
 \epsilon_5(29023)=-1,\qquad \epsilon_5(1499)=+1.            \tag{191.5}
\]

Consequently

\[
 L_1=L_0\mathbf Q(\sqrt5)                                   \tag{191.6}
\]

separates the certified pair. The two-point Kummer extension `L_0` is
unramified away from `7*433`, while `Q(sqrt5)` ramifies at 5, so
`Q(sqrt5)` is not contained in `L_0` and `[L_1:L_0]=2`. Hence (191.6) realizes
the information-theoretic minimum of one additional bit. Nothing here shows
that `L_1` governs any other value of `mathfrak c`, much less the whole packet.

## Obstruction lemma

**Lemma 191.1 (collision obstruction to fixed-field determinant
reciprocity).** Let `L/Q` be finite Galois, let `B` be a set of primes
unramified in `L`, and for each `q in B` let `C_q` be a one-dimensional vector
space over a field `k` with an element `c_q in C_q`. Suppose there are primes
`q_0,q_1 in B` such that

\[
 \operatorname{Frob}_{q_0}(L)=\operatorname{Frob}_{q_1}(L)
 \quad\text{in }\operatorname{Gal}(L/\mathbf Q)^\#,
 \qquad c_{q_0}=0,\quad c_{q_1}\ne0.                         \tag{191.7}
\]

Then there do not exist a fixed line `Delta`, isomorphisms
`iota_q:C_q -> Delta`, nonzero scalars `u_q in k^x`, and elements
`D_q in Delta` satisfying

\[
 \iota_q(c_q)=u_qD_q                                         \tag{191.8}
\]

for all `q in B`, if the predicate `D_q=0` factors through the Frobenius
conjugacy class in `L`. More generally, if (191.8) is governed by an enlarged
finite Galois extension `K` containing `L`, then the Frobenius classes of
`q_0,q_1` in `Gal(K/Q)` must be distinct. In particular, the fibre of
`Gal(K/Q)^# -> Gal(L/Q)^#` over their common class must contain at least two
classes met by `B`.

**Proof.** Isomorphisms and multiplication by nonzero scalars preserve
vanishing, so (191.8) gives

\[
 c_q=0\quad\Longleftrightarrow\quad D_q=0.
\]

If the right side factors through the Frobenius class in `L`, it has the same
truth value at `q_0` and `q_1`, contradicting (191.7). The same argument over
`K` shows that a governing `K` must separate the pair. QED.

## Consequence for the proposed route

The earlier determinant mechanism remains valid for fixed-curve two-prime
Kurihara nonvanishing: there global Tate reciprocity, core-vertex rigidity, and
pointwise explicit reciprocity prove an implication of vanishing loci without
asserting a termwise determinant identity. It cannot be transplanted to the
prime-twist coordinate by declaring the varying twist determinant to be the
fixed `L_0` Kummer determinant. Any valid prime-twist formula must introduce a
genuinely new Galois/automorphic input that separates (191.1), together with
comparison maps and uniform integrality and primitivity hypotheses.

The quadratic bit (191.5) is the smallest explicit separator, but the collision
does not privilege it conceptually and supplies no evidence that it is the
missing reciprocity variable. It only proves that zero additional bits are
impossible and one bit is enough to separate this one certified collision.

No finite-governance theorem, explicit reciprocity formula, density theorem, or
BSD case is claimed.
