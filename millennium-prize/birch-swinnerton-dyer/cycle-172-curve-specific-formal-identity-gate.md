# Cycle 172: the curve-specific formal-identity gate for `433a1` at seven

The Cycle 171 congruence strongly suggests the good-ordinary `p`-adic BSD
leading-term formula.  This cycle asks a narrower literature question: does a
published theorem, with hypotheses that can be checked for this curve, already
turn that congruence into an exact equality in `Q_7`?

The answer is **no among the theorem routes audited here**.  Two exact bridges
are available, but they meet on the arithmetic side only.  The remaining
analytic-to-arithmetic bridge in rank two is still a conjectural higher-rank
leading-term statement (or is proved only up to a `7`-adic unit), not an
unconditional curve-specific theorem.

## The exact identity that would be needed

Let

\[
 E: y^2+xy=x^3+1,
 \qquad p=7,
 \qquad \alpha^2+3\alpha+7=0,
 \quad \alpha\equiv4\pmod7.
\]

Let `mu_alpha` be the Neron-period-normalized ordinary modular-symbol measure
of Cycle 171, let `<x>=8^ell(x)`, and put

\[
 M_2=\int_{\mathbf Z_7^\times}\ell(x)^2\,d\mu_\alpha(x).
\]

Let `Reg_7(P,Q)` be the determinant of the Mazur--Tate cyclotomic height on the
saturated basis

\[
 P=(0,1),\qquad Q=(-1,1).
\]

Since `433a1` has trivial rational torsion, Tamagawa product one, and
`Sha(E)[7^infty]=0` from Cycles 135--136, the desired specialization of the
good-ordinary `p`-adic BSD formula is

\[
 \boxed{
 \frac{M_2}{2}
 = (1-\alpha^{-1})^2
   \frac{\operatorname{Reg}_7(P,Q)}{\log_7(8)^2}
 }
 \qquad\text{in }\mathbf Q_7. \tag{1}
\]

Equivalently, using the analytic cyclotomic variable of Cycle 171,

\[
 \boxed{
 \frac{(L^E_{7,\alpha})''(0)}{2}
 = (1-\alpha^{-1})^2\operatorname{Reg}_7(P,Q)
 }. \tag{2}
\]

The measure already includes the ordinary Euler factor, so it must not be
inserted a second time on the left.  The factor `1/2` belongs to the quadratic
Taylor coefficient.  Formula (1) is exactly the equality whose reduction
modulo `7^6` was verified in Cycle 171.

## What Coleman integration proves exactly

Balakrishnan--Besser, *Coleman--Gross height pairings and the p-adic sigma
function*, proves a direct comparison for an ordinary elliptic curve:

1. with the global logarithm whose component at `p` is the standard branch
   `log_p(p)=0`;
2. with the unit-root complement to the Hodge filtration; and
3. with the invariant differential attached to the chosen minimal
   Weierstrass equation,

the Coleman--Gross height equals the Mazur--Tate height.  Locally at `p`, their
Corollary 4.2 identifies the self-height Coleman function with
`-2 log(sigma_p)`; Corollary 4.3 then identifies the global height with the
Mazur--Tate sigma formula.

All these hypotheses are directly satisfied here: `7` is good ordinary
because `a_7=-3`, the Cycle 145 sigma function uses the unit-root splitting and
the Neron differential of the minimal equation, and the global cyclotomic
logarithm has `log_7(7)=0`.  Hence the Cycle 145 matrix is not merely a
numerical analogue of the Coleman--Gross or Nekovar height: after aligning the
global logarithm, splitting, and sign convention, it is that height exactly.

This closes the **height-comparison** bridge

\[
 \text{sigma height}=\text{Mazur--Tate height}
 =\text{Coleman--Gross height}
 =\text{Nekovar cyclotomic height}, \tag{3}
\]

up to the explicitly chosen common convention.  It does **not** relate this
height determinant to the modular-symbol moment `M_2`.

## Why the modular parametrization does not close the bridge

The strong-Weil parametrization

\[
 \pi:X_0(433)\longrightarrow E
\]

has modular degree `28` and Manin constant one.  It therefore explains exactly
why PARI's plus modular symbol is normalized by the Neron period used in Cycle
171, and functoriality transports Coleman integrals and heights of divisors
through `pi`.

That is not a rank-two leading-term theorem.  The modular symbol defines the
ordinary measure and hence the analytic scalar `M_2`; a rational point on `E`
does not acquire a canonical modular-divisor representative whose pairwise
Coleman integrals have determinant equal to this second moment.  Establishing
such an equality would itself be an explicit-reciprocity or `p`-adic BSD
leading-term theorem.  The degree `28` is a `7`-adic unit, and the Manin
constant is one, but these facts remove normalization ambiguity rather than
prove (1).

## Why p-adic Gross--Zagier does not apply directly

Published `p`-adic Gross--Zagier formulas identify a **first cyclotomic
derivative of a Rankin--Selberg p-adic L-function** with the height of a
Heegner point over an imaginary quadratic field.  Disegni's theorem, for
example, is of this form.  It is not a formula for the determinant of a
two-dimensional height pairing on `E(Q)` and the second derivative of the
one-variable cyclotomic `L_p(E)`.

One could try to choose two auxiliary quadratic fields or factor a base-change
`L`-function and then isolate the two rational generators.  To recover (2),
that argument would require, in addition to separate rank-one Gross--Zagier
formulas, an exact determinant/factorization identity with all periods, Euler
factors, indices, and cross-height terms controlled.  No such rank-two theorem
was found in the audited sources.  Disegni's proved cyclotomic theorem over
`Q` is explicitly stated for analytic rank at most one, so `433a1`, of
analytic rank two, lies outside its theorem.

The 2024 theorem of Burungale--Skinner--Tian--Wan does not enlarge this range:
its ordinary `p`-part BSD theorem is for analytic rank one, while its
supersingular result is for analytic rank at most one.  It therefore cannot be
specialized to (1).

## The closest arbitrary-rank formalism is conditional or only up to a unit

Burns--Kurihara--Sano construct an arbitrary-rank cyclotomic Bockstein
regulator and prove an exact generalized Rubin formula.  For good reduction,
their formula pairs the derived Kato class `kappa_infty` with a rational point
and expresses the result through the `r`-th derivative of the `p`-adic
`L`-function.  They also prove that their Bockstein regulator pairs with a
rational point as its formal logarithm times the classical `p`-adic regulator.

This is precisely the formal shape needed in rank two, and (3) identifies the
classical regulator with the sigma regulator after conventions are aligned.
However, the theorem that would identify `kappa_infty` with the complex
leading term times the Bockstein regulator is their **Generalized Perrin--Riou
Conjecture**.  Their arbitrary-rank `p`-adic BSD consequence of the Iwasawa main
conjecture is only up to an unspecified element of `Z_7^times`; their exact
classical `7`-part BSD conclusion additionally assumes the generalized
Perrin--Riou conjecture.  Neither statement yields the exact scalar (1).

The related Burns--Kurihara--Sano Mazur--Tate theorem has the same gate: in
positive rank its leading-term result assumes classical BSD and the
Generalized Perrin--Riou Conjecture.  Sano's derived-Bockstein descent theorem
is a formal implication and gives several anticyclotomic formulas only up to a
`p`-adic unit; its general cyclotomic leading-term equality remains a
conjecture.  These results explain the observed congruence but do not promote
it to equality in `Q_7`.

## Hypothesis audit for `433a1,p=7`

The elementary and local hypotheses that usually surround the desired theorem
are verifiable and favorable:

| datum | value | status |
|---|---:|---|
| conductor | `433` | square-free; semistable |
| reduction at `7` | good ordinary, `a_7=-3` | verified |
| exceptional zero | none, since `alpha != 1` | verified |
| residual image | `GL_2(F_7)` | verified in Cycles 135--136 |
| rational rank | `2` | certified by the displayed basis and Kim upper bound |
| saturated `7`-adic lattice | `P,Q`, index prime to `7` | verified in Cycle 136 |
| rational torsion | `1` | exact |
| Tamagawa product | `1` | exact (`I_1` at `433`) |
| `Sha[7^infty]` | `0` | Cycle 135 consequence |
| Manin constant | `1` | audited for the optimal curve |
| cyclotomic height | nondegenerate | Cycle 143; `v_7(Reg_7)=2` |

What is not supplied by these checks is a theorem proving the generalized
Perrin--Riou/`p`-adic BSD leading-term equality in algebraic rank two.  Using
the database value `ord_{s=1}L(E,s)=2` as a hypothesis would also be only a
numerical analytic-rank assertion unless separately certified; even granting
it does not move the published rank-at-most-one theorems into rank two.

## Decision

There is a clean exact chain on each side:

\[
 \text{modular symbols}\Longrightarrow M_2
 \Longleftrightarrow (L^E_{7,\alpha})''(0),
\]

and

\[
 \text{sigma}\Longleftrightarrow
 \text{Coleman--Gross/Nekovar height}
 \Longrightarrow \operatorname{Reg}_7(P,Q).
\]

No audited established theorem joins these chains **exactly** for this
non-CM, good-ordinary, rank-two curve.  Formula (1) remains the curve-specific
specialization of the `p`-adic BSD/generalized Perrin--Riou leading-term
conjecture.  The congruence modulo `7^6` is strong calibration evidence, not a
proof in `Q_7`.

The next legitimate exact target is therefore not more finite precision.  It
is either (a) a proof of the rank-two generalized Perrin--Riou identity for the
derived Kato class of `433a1`, with constants fixed, or (b) a genuinely
rank-two explicit-reciprocity theorem that identifies the modular-symbol
second moment directly with the determinant of the cyclotomic height.

## Primary references audited

- J. S. Balakrishnan and A. Besser, *Coleman--Gross height pairings and the
  p-adic sigma function*, J. Reine Angew. Math. 698 (2015), 89--104,
  arXiv:1201.6016; especially Corollaries 4.2--4.3.
- D. Disegni, *On the p-adic Birch and Swinnerton-Dyer conjecture for elliptic
  curves over number fields*, Kyoto J. Math. 60 (2020), 473--510,
  arXiv:1609.02528; Theorem A has analytic rank at most one.
- D. Disegni, *The p-adic Gross--Zagier formula on Shimura curves*, Compos.
  Math. 153 (2017), 1987--2074, arXiv:1510.02114; a Heegner-point height/first
  Rankin derivative formula, with the published factor-of-two erratum noted by
  the author.
- D. Burns, M. Kurihara, and T. Sano, *On derivatives of Kato's Euler system
  for elliptic curves*, arXiv:1910.07404; generalized Rubin formula and
  arbitrary-rank Bockstein regulator, with the leading Kato identity
  conjectural and main-conjecture descent up to a unit.
- D. Burns, M. Kurihara, and T. Sano, *On derivatives of Kato's Euler system
  and the Mazur--Tate conjecture*, arXiv:2103.11535; the positive-rank
  Mazur--Tate implication assumes BSD and the Generalized Perrin--Riou
  Conjecture, while its unconditional leading-term evidence is rank one.
- T. Sano, *Derived Bockstein regulators and anticyclotomic p-adic Birch and
  Swinnerton-Dyer conjectures*, arXiv:2308.08875.
- A. Burungale, C. Skinner, Y. Tian, and X. Wan, *Zeta elements for elliptic
  curves and applications*, arXiv:2409.01350; ordinary BSD application in
  analytic rank one and supersingular application in rank at most one.
