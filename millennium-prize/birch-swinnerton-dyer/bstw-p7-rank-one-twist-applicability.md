# BSTW ordinary `p=7` applicability for two rank-one twists

## Scope and verdict

Let

\[
 E_0=433\mathrm a1:\quad y^2+xy=x^3+1
\]

and let `A_D=E_0^(D)` for `D=-1499,-29023`.  The hypotheses of the ordinary
rank-one `p`-part BSD statement in Burungale--Skinner--Tian--Wan (BSTW),
arXiv:2409.01350v2, Theorem `corA'` in the source, apply to each `A_D` at
`p=7`, subject to the status and trust boundaries stated below.  Therefore the
theorem gives, separately for each twist,

\[
 \left|\frac{L'(1,A_D)}{\Omega_{A_D}R(A_D/\mathbf Q)}\right|_7^{-1}
 =
 \left|\#\Sha(A_D/\mathbf Q)
          \prod_{\ell\mid N_D}c_\ell(A_D)\right|_7^{-1}.       \tag{1}
\]

Both curves have trivial rational torsion, so there is no torsion-factor
ambiguity in matching BSTW's displayed rank-one formula.  Here the Tamagawa
product is `2`, so (1) reduces to the valuation identity for the normalized
algebraic leading-term quotient

\[
 v_7\!\left(\frac{L'(1,A_D)}{\Omega_{A_D}R(A_D/\mathbf Q)}\right)
 =v_7\!\left(\#\Sha(A_D/\mathbf Q)\right).                    \tag{2}
\]

No value for either side of (2) is computed here.  In particular, this report
does **not** claim `Sha(A_D)[7^infty]=0`, `Sha(A_D)[7]=0`, or triviality of the
full Tate--Shafarevich group for either twist.

## The theorem hypotheses

BSTW's ordinary rank-one theorem is stated for an elliptic curve `A/Q` of
conductor `N` and an ordinary prime `p` satisfying:

1. `p` does not divide `2N`;
2. the residual representation on `A[p]` is absolutely irreducible;
3. there is a prime `ell || N` at which that residual representation is
   ramified; and
4. `ord_(s=1)L(s,A)=1`.

The theorem concludes the equality of `p`-adic absolute values in (1).  It is a
prime-part statement about the normalized algebraic leading term, not an
equality of signed real numbers and not, by itself, a computation of the common
valuation.

## Hypothesis audit for both twists

| hypothesis or datum | `D=-1499` | `D=-29023` | justification |
|---|---:|---:|---|
| minimal model | `[1,0,1,-46813,-3372156843]` | `[1,1,1,-17548636,-24475377572834]` | exact PARI replay |
| conductor `N_D` | `433*1499^2` | `433*29023^2` | exact PARI replay |
| `7` does not divide `2N_D` | yes | yes | integer factorization |
| `a_7(A_D)` | `3` | `3` | exact point count; hence good ordinary |
| `#A_D(F_7)` | `5` | `5` | exact point count |
| residual absolute irreducibility | yes | yes | inherited from the certified full image for `E_0[7]` under quadratic scalar twist |
| prime `ell || N_D` | `433` | `433` | conductor exponent one |
| residual ramification at `433` | yes | yes | multiplicative `I_1` reduction and `v_433(Delta_min)=1`, so mod-seven tame inertia contains a nontrivial transvection |
| root number | `-1` | `-1` | exact local computation |
| `L'(1,A_D)` | rigorously positive | rigorously positive | directed-rational AFE certificates in Cycles 193 and 194 |
| analytic rank | `1` | `1` | sign `-1` plus certified `L'(1) != 0` |
| rational torsion order | `1` | `1` | exact PARI replay |
| local Tamagawa numbers | `c_433=1`, `c_1499=2` | `c_433=1`, `c_29023=2` | exact local reduction |
| Tamagawa product | `2` | `2` | exact local/global reduction |

The residual argument needs no new image computation for each twist.  Cycle
185 certifies `rho_(E_0,7)(G_Q)=GL_2(F_7)`.  A quadratic twist replaces every
matrix by a scalar quadratic character times that matrix, which leaves its
invariant subspaces unchanged; absolute irreducibility follows.  At `433`, the
twisting characters are unramified because `433` divides neither fundamental
discriminant.  More directly, each displayed minimal twist has multiplicative
reduction and minimal-discriminant valuation one at `433`.  Since `7` does not
divide that valuation, the standard Tate-curve inertia matrix is a nonidentity
transvection modulo seven.  This verifies BSTW's `(ram)` hypothesis with
`ell=433`; the additive twist prime is not used for that hypothesis.

Cycles 193 and 194 prove analytic rank one with pinned coefficient tables and
directed rational enclosures.  Gross--Zagier--Kolyvagin consequently gives
algebraic rank one and finiteness of the full `Sha` for both curves.  That
qualitative finiteness result does not determine any primary order.

## What remains uncomputed

Applicability of BSTW converts a calculation of the left side of (2) into a
calculation of `v_7(#Sha)`, but no such calculation is present in the committed
artifacts.

- For `D=-1499`, Cycle 195 gives a directed real interval for the
  point-normalized BSD quotient and a generator claim with an explicitly
  retained eclib non-directed-`bigfloat` trust boundary.  A real interval near
  one is not a computation of a `7`-adic valuation and cannot be rounded into a
  seven-part BSD conclusion.
- For `D=-29023`, no rational generator, regulator, normalized Heegner index,
  or rank-one BSD quotient has been computed.  The analytic-rank certificate
  and qualitative Kolyvagin theorem do not supply these data.
- For either twist, the present report does not evaluate the rational algebraic
  leading-term quotient in (2), prove that it is a `7`-adic unit, or compute a
  normalized Heegner/Kolyvagin index.  Thus the common valuation in (2) remains
  unknown from these artifacts.

In particular, the fact that `7` divides neither the torsion order nor the
Tamagawa product removes those local factors from (2); it does not force the
remaining `Sha` valuation to vanish.

## Preprint and theorem trust boundary

The source audited is arXiv:2409.01350v2, submitted in September 2024.  As of
this audit it is cited here as a **preprint**, not as a published theorem.  The
arXiv source states Theorem `corA'` exactly with ordinary reduction, residual
absolute irreducibility, ramification at some `ell || N`, and analytic rank one.
This report checks specialization of those displayed hypotheses; it does not
independently referee the proof of BSTW, certify that no later version changes
the statement, or replace the normal scholarly trust placed in the preprint.
Accordingly, (1)--(2) are conditional on the correctness of that preprint
theorem, while the local and analytic-rank inputs have the separate certificate
boundaries already documented in this repository.

## Reproduction and sources

Run the exact local-data replay with PARI/GP:

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/verify_bstw_p7_rank_one_twists.gp
```

The script checks both minimal models, conductors, root numbers, `a_7`, point
counts over `F_7`, reduction and discriminant valuation at `433`, reduction at
the twist prime, Tamagawa products, and rational torsion orders.

Primary and repository sources:

- A. Burungale, C. Skinner, Y. Tian, and X. Wan, *Zeta elements for elliptic
  curves and applications*, arXiv:2409.01350v2, especially Theorem `corA'`.
- `cycle-185-actual-433a1-kummer-group.md` for the exact residual-image
  certificate.
- `cycle-193-rigorous-derivative-certificate.md` and
  `cycle-194-D-29023-rigorous-derivative-certificate.md` for analytic rank one.
- `cycle-195-D-1499-exact-interval-bsd-quotient.md` for the real quotient,
  generator scope, and the warning that no odd-primary valuation was computed.

This is a bounded applicability report for two curves.  It is not a family
theorem, a proof of refined BSD, or progress toward the full Millennium
quantifier.
