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
theorem gives, separately for each twist, the equality exactly displayed in
`corA'`:

\[
 \left|\frac{L'(1,A_D)}{\Omega_{A_D}R(A_D/\mathbf Q)}\right|_7^{-1}
 =
 \left|\#\Sha(A_D/\mathbf Q)
          \prod_{\ell\mid N_D}c_\ell(A_D)\right|_7^{-1}.       \tag{1}
\]

BSTW suppresses the standard denominator `#A_D(Q)_tor^2` in this display.
This is harmless at `p`: absolute irreducibility of `A_D[p]` implies
`A_D(Q)[p]=0`, hence the omitted torsion order is a `p`-adic unit.  Thus the
valuation-faithful BSD form is

\[
 \left|\frac{L'(1,A_D)}{\Omega_{A_D}R(A_D/\mathbf Q)}\right|_7^{-1}
 =
 \left|\frac{\#\Sha(A_D/\mathbf Q)
          \prod_{\ell\mid N_D}c_\ell(A_D)}
         {\#A_D(\mathbf Q)_{\rm tor}^{\,2}}\right|_7^{-1}.     \tag{1'}
\]

For the two curves here the stronger exact fact `#A_D(Q)_tor=1` is
independently checked.  Their Tamagawa product is `2`, so (1') reduces to the
valuation identity for the normalized algebraic leading-term quotient

\[
 v_7\!\left(\frac{L'(1,A_D)}{\Omega_{A_D}R(A_D/\mathbf Q)}\right)
 =v_7\!\left(\#\Sha(A_D/\mathbf Q)\right).                    \tag{2}
\]

The separate Cycle 209 exact Kurihara certificate now computes the
`D=-1499` side: `Sha(A_-1499)[7^infty]=0`, so both sides of (2) have valuation
zero.  No value is computed for `D=-29023`, and full Tate--Shafarevich
triviality is not claimed for either twist.

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
valuation.  Here `|p|_p=p^{-1}`.  The period convention is the positive real
Neron period

\[
 \Omega_A=\int_{A(\mathbf R)}|\omega_A|,
\]

for a global minimal Neron differential (so all real components are included),
and the regulator is formed from the Neron--Tate pairing on a `Z`-basis of the
free Mordell--Weil group.  This is the BSD convention referred to in the
paper's introduction; `corA'` itself abbreviates it as "the period".  Replacing
either by a quantity known only up to an unspecified rational factor is not
legitimate before taking a valuation.

No Manin constant occurs in the final statement.  In the proof, BSTW first
obtain (in the proof of Proposition `p-BSD-prop`)

\[
 \left|\frac{L^{(d)}(1,A_g)}
 {d!\,\Omega_g R(A_g)}\right|_\lambda^{-1}
 =\left|\#\Sha(A_g)[\lambda^\infty]c_g^{-2}
 \prod_{\ell\mid N}c_\ell(A_g)\right|_\lambda^{-1},             \tag{3}
\]

where `Omega_g` is the product of congruence periods and `c_g` is the Manin
constant.  They then invoke the `p`-indivisibility of `c_g` and compare the
optimal/congruence periods with the Neron-period lattice up to a `p`-adic unit.
Consequently `c_g^{-2}` disappears only at the level of `p`-adic absolute
values.  The theorem needs only the cited `p`-indivisibility, not a separately
assumed equality `c_g=1`; this report does not promote the base curve's audited
Manin constant to an unproved exact Manin-constant assertion for both twists.

Before rewriting (1') as (2), one must therefore fix the Neron period and
Neron--Tate regulator conventions, view the algebraic leading-term quotient in
`Q_7`, know the relevant finiteness of `Sha`, and verify that every torsion,
Tamagawa, Manin, and period-comparison factor being discarded is a 7-adic unit.
Analytic rank one supplies Mordell--Weil rank one and finiteness of the full
`Sha` here by Gross--Zagier--Kolyvagin; the local and unit checks are recorded
below.  Omitting these steps would make (2) an unjustified strengthening of the
displayed theorem.

## Hypothesis audit for both twists

| hypothesis or datum | `D=-1499` | `D=-29023` | justification |
|---|---:|---:|---|
| minimal model | `[1,0,1,-46813,-3372156843]` | `[1,1,1,-17548636,-24475377572834]` | exact PARI replay |
| conductor `N_D` | `433*1499^2` | `433*29023^2` | exact PARI replay |
| `7` does not divide `2N_D` | yes | yes | integer factorization |
| `7` divides minimal discriminant | no | no | good reduction at `7` |
| `a_7(A_D)` | `3` | `3` | exact point count; hence good ordinary |
| `#A_D(F_7)` | `5` | `5` | exact point count |
| residual absolute irreducibility | yes | yes | inherited from the certified full image for `E_0[7]` under quadratic scalar twist |
| prime `ell || N_D` | `433` | `433` | conductor exponent one |
| residual ramification at `433` | yes | yes | multiplicative `I_1` reduction and `v_433(Delta_min)=1`, so mod-seven tame inertia contains a nontrivial transvection |
| root number | `-1` | `-1` | exact local computation |
| `L'(1,A_D)` | rigorously positive | rigorously positive | directed-rational AFE certificates in Cycles 193 and 194 |
| analytic rank | `1` | `1` | sign `-1` plus certified `L'(1) != 0` |
| rational torsion order | `1` | `1` | exact PARI replay |
| Manin factor in BSTW proof | 7-adic unit | 7-adic unit | cited `p`-indivisibility; exact twist Manin constants are not asserted |
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

The condition `p \nmid 2N` is a good-reduction condition and is not permission
for `p` to divide the minimal discriminant.  For a global minimal equation,
good reduction at `p` forces `v_p(Delta_min)=0`.  The statement of `corA'` has
no separate condition involving a quadratic-twist discriminant because it is
stated for the curve `E` itself: after specialization to `A_D`, its requirement
is simply `7 \nmid 2N_D`.  Thus a twist ramified at `7`, which ordinarily has
bad reduction and `7 | N_D`, is outside this theorem.  A nonminimal equation
may have an equation discriminant divisible by `7`; that does not alter the
criterion, which uses the conductor/good reduction of the elliptic curve.

This should not be confused with Theorem `KaMC_r(c)` later in the paper, whose
twist clause allows an auxiliary quadratic field `K` with `p | disc(K)` under
`(ram_K)`.  That is an internal Kato-main-conjecture statement, not the
ordinary rank-one BSD statement `corA'`, and it does not license dropping
`p \nmid 2N_D` when applying `corA'` to the twisted curve.

## Seven-part status

Applicability of BSTW converts a calculation of either side of (2) into the
other.  The committed status is:

- For `D=-1499`, Cycle 209 computes the exact one-prime Kurihara value
  `delta_tilde_29=-150=4 mod 7` and an exact nonzero local Kummer image of the
  displayed rational point.  Kim's Selmer-structure theorem gives
  `Sel(Q,A[7^infty])=Q_7/Z_7` and `Sha[7^infty]=0`.  BSTW then gives
  `v_7(L'(1,A)/(Omega_A R(A/Q)))=0`.  This uses no real rounding and does not
  depend on the Cycle 195 generator trust boundary.
- For `D=-29023`, Cycle 215 combines Cycle 211's exact nonzero Kurihara value
  at `113` with rank one and trivial torsion. The rank-one Kummer space and
  Kim's residual Selmer group are both one-dimensional, so the Kummer
  injection is surjective and `Sha[7^infty]=0`. BSTW then proves that the
  normalized leading-term quotient in (2) is a `7`-adic unit. No rational
  generator, regulator value, or normalized Heegner index is needed for this
  valuation.

The fact that `7` divides neither the torsion order nor the Tamagawa product
only removes local factors from (2).  For `D=-1499`, vanishing comes from the
separate exact Selmer certificate, not from those unit checks alone.

## Preprint and theorem trust boundary

The source audited is arXiv:2409.01350v2, submitted in September 2024.  As of
this audit it is cited here as a **preprint**, not as a published theorem.  The
arXiv source states Theorem `corA'` exactly with `p \nmid 2N`, ordinary
reduction, residual absolute irreducibility, ramification at some `ell || N`,
and analytic rank one.  Its display omits rational torsion and Manin factors:
torsion is automatically a `p`-unit under residual irreducibility, and the
Manin/period factors are removed in the proof only up to `p`-adic units as
described above.
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
- `cycle-209-D-1499-seven-adic-leading-term.md` for the exact Kurihara/Selmer
  computation that now supplies the seven-primary valuation.

This is a bounded applicability report for two curves.  It is not a family
theorem, a proof of refined BSD, or progress toward the full Millennium
quantifier.
