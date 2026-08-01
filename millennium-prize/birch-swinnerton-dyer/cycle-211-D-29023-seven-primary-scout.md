# Cycle 211: `D=-29023`, `p=7` Kurihara scout

Let

\[
 A=433\mathrm a1^{(-29023)}:
 y^2+xy+y=x^3+x^2-17548636x-24475377572834.
\]

## Verdict

The first genuine Kolyvagin prime after the known zero at `ell=29` is

\[
 \boxed{\ell=113}.
\]

With primitive root `eta=3 mod 113`, the exact one-prime Kurihara value is

\[
 \boxed{\widetilde\delta^{(1)}_{113}(A)=-17186\equiv6\pmod7.}
\]

Thus the bounded scout succeeds; there is no bounded obstruction at this
stage. The value at the smaller Kolyvagin prime `ell=29` remains the exact zero
`77/2=0 mod 7` from Cycle 190.

## Exact base-twist computation

Cycle 187's base-twist identity applies with `q=29023`, `D=-29023`, and the
base minus symbols of `433a1`. The exact minimal-model change is
`[1,2419,1,1210]`, so the differential scale and period factor are
`kappa_29023=1`. For `1<=a<=112`, put

\[
 U_a=\sum_{u=1}^{29022}\left(\frac{u}{29023}\right)
 \left[\frac{29023a+113u}{113\cdot29023}\right]^-_{433\mathrm a1}.
\]

The verifier computes all `112*29022` modular symbols exactly with PARI
`msfromell`, checks that every completed `U_a` has denominator prime to seven,
and forms

\[
 \sum_{a=1}^{112}\log_3(a)U_a=-17186.
\]

No decimal period or floating modular-symbol value enters the calculation.
The orientation is the same endpoint and minus-period convention fixed in
Cycle 187. Changing the primitive root rescales the residue by a unit and does
not affect nonvanishing.

Exact point counting gives

\[
 a_{113}(A)=2,\qquad \#A(\mathbf F_{113})=112.
\]

Hence `113=1 mod 7` and `a_113=113+1 mod 7`, so `113` is a genuine one-prime
Kolyvagin prime at `p=7`.

## Localization witness

Exact finite-field arithmetic gives

\[
 A(\mathbf F_{113})\simeq \mathbf Z/112\mathbf Z.
\]

The point

\[
 G=(85,7)
\]

has exact order `112`. Its class generates
`A(F_113)/7A(F_113)`, and the explicit seven-torsion detector is

\[
 16G=(53,42),\qquad \operatorname{ord}(16G)=7.
\]

This is an exact nonzero local quotient witness. It is not yet the localization
of a displayed rational Mordell--Weil point: no exact rational coordinates for
a generator of `A(Q)` are presently available. Consequently this scout proves
Kurihara nonvanishing and identifies the one-dimensional local target, but by
itself does not prove that a rational Kummer class spans that target.

Under Kim's Cycle 209 theorem packet, the nonzero value gives the same
one-dimensional residual Selmer conclusion for `A` after the curve-specific
hypotheses are imported: the mod-seven representation is surjective, seven is
good ordinary and nonanomalous (`#A(F_7)=5`), and the Tamagawa factors are
seven-units. Since Cycle 194 certifies analytic rank one, Gross--Zagier--
Kolyvagin supplies algebraic rank one and finite `Sha`. To conclude
`Sha(A/Q)[7]=0` by the Cycle 209 localization argument, one still needs an
exact global Kummer localization witness, or an equivalent theorem identifying
the rational line with the displayed nonzero local line.

## Reproduction

Run

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/cycle211_D29023_p7_kurihara.gp
```

The exact producer takes several minutes. Its output must report
`delta_tilde_113=-17186=6 mod 7`, the cyclic group of order `112`, and the
order-seven point `(53,42)`.

This is a successful bounded re-entry certificate for the Kurihara coordinate,
not a full BSD result and not yet a complete seven-primary `Sha` certificate.
