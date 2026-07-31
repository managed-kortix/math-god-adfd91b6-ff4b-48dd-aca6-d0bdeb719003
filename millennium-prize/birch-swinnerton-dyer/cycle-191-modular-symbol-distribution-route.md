# Cycle 191: exact distribution route for infinitely many fixed-class values

## Question and conclusion

Fix the objects and packet `A` of Cycle 190.  The desired strengthening is to
find one conjugacy class `C` in

\[
 G_0=\operatorname{Gal}(L_0/\mathbf Q)
\]

for which infinitely many primes `q in A` with `Frob_q(L_0) in C` have
`c(q,29)=0`, and infinitely many have `c(q,29) != 0`.

No theorem located in the modular-symbol distribution literature gives this
statement after specialization.  The existing theorems distribute individual
fixed-level modular symbols while averaging over all reduced rational cusps of
bounded denominator (sometimes with an interval restriction).  Here the sample
is prime denominators in one nonabelian Chebotarev class, and the random
variable is the quadratic-character-weighted sum of `12(q-1)` mutually
correlated symbols.  Neither the prime restriction nor this grouped transform
is a formal consequence of individual-symbol equidistribution.

There is, however, an exact and reasonably sharp analytic target which would
imply the requested infinitude.  It is recorded below so that a future argument
has no hidden probabilistic or Chebotarev step.

## Exact coordinate

For `q in A`, write

\[
 c(q)=\overline{\sum_{a=1}^{14}w_a\sum_{u=1}^{q-1}
 \left(\frac uq\right)
 \left[\frac{aq+29u}{29q}\right]^{\epsilon_q}_E}\in\mathbf F_7,
 \tag{191.1}
\]

where

\[
 (w_1,\ldots,w_{14})=(0,2,3,4,2,5,3,6,6,4,1,0,1,5),
 \qquad \epsilon_q=\left(\frac{-1}{q}\right).
\]

Cycle 188 proves that the period factor in this formula is exactly one.  Thus
there is no varying unit to remove before asking for distribution of the
zero/nonzero predicate.

## The known theorem routes, with their exact scope

1. **Petridis--Risager.**  Petridis and Risager, *Arithmetic statistics of
   modular symbols*, Invent. Math. 212 (2018), 997--1053,
   DOI `10.1007/s00222-017-0784-7`, prove refined archimedean Gaussian laws for
   modular symbols ordered by denominator, including restrictions on the
   location of the cusp.  Their theorem concerns individual symbols and an
   all-denominator average; it is not a residual theorem for (191.1), nor a
   prime-denominator Chebotarev theorem.

2. **Constantinescu--Nordentoft.**  Constantinescu and Nordentoft, *Residual
   equidistribution of modular symbols and cohomology classes for quotients of
   hyperbolic n-space*, Trans. Amer. Math. Soc. 375 (2022), 7001--7034,
   DOI `10.1090/tran/8646`, Theorem 1.1, prove joint mod-`p` equidistribution for
   a Hecke basis on

   \[
   \Omega_{Q,N}=\{a/d:0<a<d\leq Q,(a,d)=1,N\mid d\},
   \]

   with an interval restriction on `a/d`.  In particular, the theorem averages
   over both numerator and denominator.  It does not retain prime denominators,
   prescribe Frobenius in `L_0`, or evaluate a Legendre-weighted sum over all
   numerators belonging to one denominator.

3. **Lee--Sun.**  Lee and Sun, *Dynamics of continued fractions and
   distribution of modular symbols*, J. Eur. Math. Soc. 27 (2025), 3527--3582,
   DOI `10.4171/JEMS/1665`, prove residual equidistribution with a power-saving
   error for modular partition functions on rationals of denominator at most
   `M`.  Their Theorem E gives, under residual irreducibility and good ordinary
   reduction, equidistribution of an individual normalized elliptic modular
   symbol modulo `p^e` on that all-rational sample.  The curve `433a1` at `p=7`
   meets the familiar good-ordinary condition (`a_7=-3`), but the theorem's
   sample and random variable still differ from (191.1).  Its power saving does
   not by itself survive restriction to prime denominators, which have density
   zero in the rational sample.

4. **Normal-distribution and moment theorems.**  Petridis--Risager's earlier
   Gaussian theorem and the additive-twist/moment results of Nordentoft and of
   Blomer--Fouvry--Kowalski--Michel--Milicevic--Sawin concern real-valued
   individual additive twists or families of Dirichlet twists.  An
   archimedean Gaussian law does not imply distribution after reduction modulo
   7, and those family parameters do not identify the prime-twist derivative
   (191.1).

Consequently, citing "modular symbols are equidistributed" is insufficient at
three separate gates: grouped correlations, prime support, and the fixed
nonabelian Frobenius condition.

## The finite-field Fourier criterion

Let `C` be a conjugacy class of `G_0`, and put

\[
 \mathcal P_C(X)=\{q\leq X:q\in A,\ \operatorname{Frob}_q(L_0)=C\},
 \qquad \pi_C(X)=\#\mathcal P_C(X).
\]

Let `e_7(t)=\exp(2\pi i t/7)`.  For `h in F_7`, define

\[
 S_{C,h}(X)=\sum_{q\in\mathcal P_C(X)}e_7(hc(q)).             \tag{191.2}
\]

**Proposition 191.1 (tractable sufficient statement).**  Suppose
`pi_C(X) -> infinity` and, for every `h=1,...,6`,

\[
 S_{C,h}(X)=o(\pi_C(X)).                                    \tag{191.3}
\]

Then, for every `r in F_7`,

\[
 \#\{q\in\mathcal P_C(X):c(q)=r\}
 =\frac{\pi_C(X)}7+o(\pi_C(X)).                             \tag{191.4}
\]

In particular, the class `C` contains infinitely many zero values and
infinitely many nonzero values of `c(q,29)`.

**Proof.**  Finite Fourier inversion gives the exact identity

\[
 1_{c(q)=r}=\frac17\sum_{h=0}^6 e_7(h(c(q)-r)).
\]

Sum over `q in P_C(X)`.  The `h=0` term is `pi_C(X)/7`; (191.3)
controls the other six terms.  This proves (191.4).

The power-saving version

\[
 S_{C,h}(X)\ll_C X^{1-\delta}\quad(1\leq h\leq6),           \tag{191.5}
\]

together with `pi_C(X) asymp_C X/log X`, is more than enough.  A dyadic form of
(191.5), uniform for the finitely many nonzero `h`, is an especially concrete
analytic target.

## Why the prime set itself is not the obstruction

Every condition defining `A` is finite-level Frobenius data after adjoining a
fixed finite extension:

- `(q/29)=1` and the twist root number are fixed quadratic/Dirichlet character
  conditions;
- `q=1 mod 7` and `a_q(E)=2 mod 7` are cyclotomic and `E[7]` data;
- `v_7(#E(F_q))=1` is detected by the action on `E[49]`, since
  `#E(F_q)=det(1-Frob_q)`.

Thus, after forming a fixed finite Galois compositum `K` containing `L_0`, the
set `P_C` is a union of conjugacy classes of `Gal(K/Q)`.  If one of those
classes is nonempty, Chebotarev gives `pi_C(X) asymp X/log X`.  The already
observed primes in the Cycle 190 class `[1:5]` witness nonemptiness for the
corresponding finite local packet.  Chebotarev therefore supplies infinitely
many admissible primes in that same `L_0` class; it says nothing about their
values of `c(q,29)`.

## Expanded analytic target

The class and local-packet indicator can be expanded as a finite linear
combination of irreducible characters of `Gal(K/Q)`.  Therefore (191.3) would
follow from cancellation in the finitely many sums

\[
 \sum_{\substack{q\leq X\\q\ \text{ prime}}}(\log q)\,
 \chi(\operatorname{Frob}_q(K))
 e_7\!\left(h\sum_{a=1}^{14}w_a\sum_{u=1}^{q-1}
 \left(\frac uq\right)
 \left[\frac{aq+29u}{29q}\right]^{\epsilon_q}_E\right)
 =o(X)                                                       \tag{191.6}
\]

for every relevant Artin character `chi` and `h != 0`.  Partial summation then
yields (191.3).  Formula (191.6), not ordinary one-cusp equidistribution, is the
exact missing estimate.

A plausible proof program would need a transfer-operator or automorphic
generating series that simultaneously records:

1. the mod-7 fixed-level symbol along each continued-fraction path;
2. the complete Legendre-weighted aggregate over `u mod q`;
3. von Mangoldt support in the denominator `q`; and
4. a finite-state label for Frobenius in `K`.

Known transfer-operator theorems provide versions of items 1 and 4 for
individual rational cusps and all denominators.  The coupled aggregate in item
2 and prime extraction in item 3 are the genuinely new analytic work.  Treating
the `q-1` symbols as independent would bypass precisely the unproved step.

## Honest endpoint

The strongest unconditional conclusion available from this route is:

- each witnessed fixed `L_0` class in the finite packet contains infinitely
  many admissible primes, by Chebotarev in a fixed finite compositum;
- existing residual-distribution theorems imply infinitely many values of each
  residue for individual base modular symbols in broad all-rational samples;
- no verified theorem transfers that distribution to `c(q,29)` on prime twists
  in one fixed `L_0` class.

Proposition 191.1 isolates a tractable sufficient theorem.  Proving (191.3), or
even (191.5), would produce the requested infinitely many same-class zero and
nonzero values.  At present it remains a new prime-denominator correlation
estimate, not a corollary of the cited literature and not a BSD result.
