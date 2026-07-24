# The four-fifths theorem in the two short-base theta channels

Write `Theta(a,b,c)` for the simple graph formed by three internally disjoint
paths of edge lengths `a,b,c` with common endpoints.  It has

`n=a+b+c-1`, `m=a+b+c=n+1`.

For a graph with adjacency eigenvalues `lambda_i`, write

`s^+(G)=sum_(lambda_i>0) lambda_i^2`.

This note assembles the exact limit certificate, exact pointwise
`c -> c+4` monotonicity certificate, and exact finite Sturm gates for the two
short-base channels `Theta(2,3,c)` and `Theta(1,4,c)`.  The result is:

**Theorem.** Every simple graph in these two channels satisfies

`s^+(G)>|V(G)|+4/5`,

except precisely

`Theta(2,3,2)=Theta(2,2,3)`, `Theta(2,3,3)`, and `Theta(1,4,4)`,

for each of which `s^+(G)<|V(G)|+4/5`.

The equality in the first display merely permutes the three path lengths.
No isomorphism between `Theta(2,3,3)` and `Theta(1,4,4)` is asserted or used.
They are different graphs and even have different orders, seven and eight.
Their surpluses happen to agree, as explained below; that numerical or
algebraic coincidence must not be confused with graph isomorphism.

## Phase formula and limit

The checked-in derivation in `experiments/theta-imaginary-phase.md` associates
to each theta a canonical phase `alpha_c(z)` on `0<z<1` and proves

`s^+(Theta)-n = 1-I_c/pi`,

`I_c=int_0^1 (z^(-2)-1) alpha_c(z) dz`.                         (1)

The phase has the required endpoint decay, so the integral is proper in the
sense established there.  Thus larger pointwise phase means smaller surplus.

The exact limits in `experiments/theta-short-base-limits.md` are

`alpha_23(z)=atan(2z^(5/2)/(1+2z-z^2))`,

`alpha_14(z)=atan(2z^(5/2)/(1+2z-z^2+z^3-z^4))`.

Both denominator comparisons are polynomial identities with nonnegative
remainders on `[0,1]`.  Using `atan(t)<t`, exact integration gives

`I_inf < int_0^1 2sqrt(z)(1-z) dz = 8/15 < 3/5 < pi/5`.        (2)

Consequently both limiting surpluses are strictly greater than `4/5`.
The algebra and the exact value `8/15` are checked independently by
`experiments/theta_phase_sign_certificate.py`.

## Pointwise monotonicity

The exact certificate `experiments/theta_phase_monotonicity_certificate.py`
proves the following directions.  They concern the phase itself; by (1), the
surplus moves in the opposite direction.

| channel | `c mod 4` | phase as `c -> c+4` | consequence |
|---|---:|---|---|
| `(2,3,c)` | 0 | strictly increasing | every finite phase is below the safe limit |
| `(2,3,c)` | 1 | strictly increasing | every finite phase is below the safe limit |
| `(2,3,c)` | 2 | strictly decreasing | check the first required finite gate |
| `(2,3,c)` | 3 | strictly decreasing | check the first required finite gate |
| `(1,4,c)` | 0 | strictly decreasing | check the first required finite gate |
| `(1,4,c)` | 1 | strictly decreasing | check the first required finite gate |
| `(1,4,c)` | 2 | strictly increasing | every finite phase is below the safe limit |
| `(1,4,c)` | 3 | strictly increasing | every finite phase is below the safe limit |

This is not a sampled or floating-point assertion.  The certificate constructs
the finite phase carrier, factors the exact cross product for `c` and `c+4`,
and proves positivity of every residual on `[0,1]^2` by exact tensor-product
Bernstein coefficients.  It also reconstructs concrete integer-length cases
as an independent bookkeeping check.

For an increasing residue class, strict increase plus convergence to (2)
implies `alpha_c(z)<alpha_inf(z)` pointwise.  Therefore `I_c<I_inf<pi/5`, and
the whole class is safe without a finite spectral gate.  For a decreasing
class, every later phase is below its first checked safe phase, so one safe
finite gate propagates to the entire tail.

## Exact finite gates

The new certificate `experiments/theta_short_base_gates.py` constructs each
adjacency matrix directly from the three paths and computes its characteristic
polynomial independently.  SymPy then isolates every real root in a rational
interval.  Every interval is checked by an exact Sturm count, exact rational
roots and multiplicities are checked separately, the intervals are checked
disjoint and separated from zero, and total multiplicity is checked against
the characteristic-polynomial degree.  Hence no root can be omitted or
assigned the wrong sign.

If a positive root lies in the checked rational interval `(l,u)`, then
`l^2<lambda^2<u^2`.  Summing these exact rational bounds with multiplicity
gives rigorous enclosures for `s^+`; no prelisted decimal interval is trusted.
The certificate obtains:

| graph | `n` | role | rigorous conclusion | decimal enclosure for orientation only |
|---|---:|---|---|---|
| `Theta(2,3,6)` | 10 | safe gate, residue 2 | `s^+>10+4/5` | `[10.8172499868,10.8178015704]` |
| `Theta(2,3,7)` | 11 | safe gate, residue 3 | `s^+>11+4/5` | `[11.8189138338,11.8197679841]` |
| `Theta(1,4,5)` | 9 | safe gate, residue 1 | `s^+>9+4/5` | `[9.82436211901,9.82506523130]` |
| `Theta(1,4,8)` | 12 | safe gate, residue 0 after the exception | `s^+>12+4/5` | `[12.8222738314,12.8232470859]` |
| `Theta(2,3,2)` | 6 | exception | `s^+<6+4/5` | `[6.69754738619,6.69810540506]` |
| `Theta(2,3,3)` | 7 | exception | `s^+<7+4/5` | `[7.71043287903,7.71091144567]` |
| `Theta(1,4,4)` | 8 | exception | `s^+<8+4/5` | `[8.71039786625,8.71111552731]` |

The script prints the actual rational enclosures and their positive rational
margins from the threshold.  The decimals in the last column are generated
only after those exact comparisons pass and play no role in the proof.

There is a useful explanation for the equal surplus of the last two
exceptions.  Their checked characteristic polynomials factor as

`chi_233=(x-1)^2(x+1)(x+2)(x^3-x^2-4x+2)`,

`chi_144=x(x-1)(x+2)(x^2-2)(x^3-x^2-4x+2)`.

The common cubic and common negative root `-2` contribute equally.  Replacing
the two positive roots `1,1` in the first graph by the positive roots
`1,sqrt(2)` and a zero in the second increases `s^+` by exactly one, while the
vertex count also increases by one.  Thus the surpluses agree.  The full
spectra, characteristic polynomials, and vertex counts do not agree.

## Assembly by residue class

For `Theta(2,3,c)`, residues 0 and 1 are safe directly from the increasing
phase and the safe limit.  In residue 2, `c=2` is an exception, `c=6` is the
safe gate, and monotonicity propagates safety to `c=10,14,...`.  In residue 3,
`c=3` is an exception, `c=7` is the safe gate, and monotonicity propagates
safety to `c=11,15,...`.

For `Theta(1,4,c)`, residues 2 and 3 are safe directly from the increasing
phase and the safe limit.  In residue 0, `c=4` is an exception, `c=8` is the
safe gate, and all later members are safer.  In residue 1, the first simple
member is `c=5`: `c=1` would repeat the direct endpoint edge and is not a
simple theta under the definition used here.  The `c=5` safe gate therefore
propagates to `c=9,13,...`.

These eight residue-class arguments exhaust the two channels and prove the
theorem.

## Reproduction

Run from `positive-square-energy/`:

```text
python3 experiments/theta_phase_sign_certificate.py
python3 experiments/theta_phase_monotonicity_certificate.py
python3 experiments/theta_short_base_gates.py
```

The expected final lines are respectively
`theta phase sign/limit certificate: PASS`,
`theta phase monotonicity certificate: PASS`, and
`theta short-base gates: PASS (7/7 graphs; all roots exhausted by exact rational Sturm counts)`.
