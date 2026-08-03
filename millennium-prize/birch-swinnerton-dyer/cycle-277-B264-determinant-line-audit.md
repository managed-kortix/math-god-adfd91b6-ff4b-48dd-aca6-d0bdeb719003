# Cycle 277: `B264-DL-AUDIT`

## Verdict

`B264-DL-WALL`.

The one theorem/class pair is:

- D. Jetchev, C. Skinner, and X. Wan, *The Birch and
  Swinnerton--Dyer formula for elliptic curves of analytic rank one*,
  Cambridge Journal of Mathematics 5 (2017), no. 3, 369--434,
  DOI `10.4310/CJM.2017.v5.n3.a2`, Main Theorem; and
- the already committed two-member twist class
  \[
  \mathcal C=\{433\mathrm a1^{(-1499)},433\mathrm a1^{(-29023)}\}.
  \]

The first mismatched hypothesis is **semistability**. The published theorem
starts with a semistable elliptic curve of square-free conductor. The two
dossier members have respective conductors

\[
433\cdot1499^2,\qquad 433\cdot29023^2,
\]

and additive reduction at the twist prime. Neither member is semistable, so
the theorem does not apply to this class.

## Source statement and normalization

For a semistable `E/Q` of analytic rank one and a prime `p>=5` of good
reduction for which `E[p]` is irreducible, the published Main Theorem proves

\[
\operatorname{ord}_p\!\left(
 \frac{L'(E,1)}{\operatorname{Reg}(E/\mathbf Q)\Omega_E}
\right)
=
\operatorname{ord}_p\!\left(
 \#\Sha(E/\mathbf Q)\prod_{\ell<\infty}c_\ell(E/\mathbf Q)
\right).
\]

The source defines `Reg(E/Q)` as the discriminant of the Neron--Tate height
pairing on the free Mordell--Weil lattice and

\[
\Omega_E=\int_{E(\mathbf R)}|\omega_E|
\]

for a Neron differential. These agree with the dossier's regulator and full
real Neron-period conventions. The source's conjectural full formula contains
the standard factor `#E(Q)_tors^(-2)`; its theorem suppresses that factor at
the level of `p`-adic valuation because residual irreducibility makes it a
`p`-unit. Both members of `mathcal C` have trivial rational torsion, so no
normalization discrepancy arises here. Their finite Tamagawa product is `2`.

At `p=7`, the remaining visible hypotheses do pass for both members: `7>=5`,
both have good ordinary reduction with `a_7=3`, their residual representations
are irreducible (indeed the dossier certifies full image), and their analytic
rank is exactly one by the directed derivative certificates. These checks do
not repair the failed global semistability hypothesis.

## Exact stopping point

The theorem is also only a prime-part equality of `p`-adic valuations. It does
not assert the exact signed complex leading-term identity

\[
\frac{L'(E,1)}{\Omega_E\operatorname{Reg}(E/\mathbf Q)}
=
\frac{\#\Sha(E/\mathbf Q)\prod_\ell c_\ell(E/\mathbf Q)}
     {\#E(\mathbf Q)_{\rm tors}^{2}}.
\]

Thus even a hypothetical repair of semistability would not turn this named
theorem into the exact complex bridge requested by `B264-DL-AUDIT`; it would
give only one prime valuation at a time. No BSD equality is assumed in the
deduction above. This audit introduces no curve or field computation, does not
reopen `43a1`, and makes no general BSD claim.

Primary-source locations: abstract and Main Theorem, especially the source's
displayed hypotheses and formulas; the normalization definitions immediately
precede the Main Theorem. Dossier inputs are recorded in
`bstw-p7-rank-one-twist-applicability.md`,
`cycle-193-rigorous-derivative-certificate.md`, and
`cycle-194-D-29023-rigorous-derivative-certificate.md`.
