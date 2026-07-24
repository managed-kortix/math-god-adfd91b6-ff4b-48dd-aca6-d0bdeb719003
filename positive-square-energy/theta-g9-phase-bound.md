# Whole-rectangle phase bound for theta graphs of odd girth at least nine

This note records the exact finite certificate proving

`I=int_0^1 (z^(-2)-1) alpha(z) dz < pi/5`                       (1)

for every positive-phase theta whose shortest odd cycle has length `g>=9`.
Unlike the earlier corner-only draft, the argument maximizes the phase on the
entire cap rectangle.  Repeated carrier corners are used only after this
whole-rectangle theorem has been established.

## Normalized carrier

For an odd length `l` and an even length `m`, set

`A_l=z^((l-1)/2)/(1+z^l)`,  `C_l=(1-z^(l-1))/(1+z^l)`,

`B_m=z^(m/2-1)/(1-z^m)`,    `G_m=(1+z^(m-1))/(1-z^m)`.          (2)

For the three path lengths, let `r` be the number of odd paths and `s=3-r`
the number of even paths.  In a positive-phase class all odd terms have one
sign and all even terms the other required sign.  Write their positive
magnitudes as

`Abar=sum_(l odd) A_l`, `Bbar=sum_(m even) B_m`,

and use the sharpened, cap-dependent real term

`D=1-z+z sum_(l odd) C_l+z sum_(m even) G_m`.                   (3)

With `c=z(1+z)^2`, direct normalization of the reconstructed carrier gives

`R/F^2=D^2+c Abar^2-zc Bbar^2`, `S/F^2=2c Abar Bbar`.          (4)

Thus, if `Phi=S/R`,

`Phi(Abar,Bbar)=2c Abar Bbar/(D^2+c Abar^2-zc Bbar^2)`,

`alpha=atan(sqrt(z) Phi)`.                                     (5)

The script constructs (2)-(5), reconstructs `F,N,P,Q,R,S` directly for every
cap, and checks all normalized identities symbolically.  It also checks

`C_l+(1+z)z^((l-1)/2)A_l=1`,

`G_m-(1+z)z^(m/2)B_m=1`,                                      (6)

which is the relation that makes the dependence of `D` on the rectangle
coordinates exact rather than an independent coarse bound.

## Exact rectangle maximizer

Fix a cap with odd endpoint `o`, even endpoint `e`, and multiplicities `r,s`.
Put

`A_0=A_o`, `B_0=B_e`, `A_*=r A_0`, `B_*=s B_0`,

`D_*=1-z+zr C_o+zs G_e`,

`a=D_*^2-zc B_*^2`.                                           (7)

Using (6), differentiation of (5) over the admissible rectangle reduces to a
one-variable linear-fractional calculation.  The maximum lies at the endpoint
unless

`B_branch=a-c A_*^2<0`.                                       (8)

On the endpoint branch its exact value is

`Y_endpoint=2c A_* B_*/(a+c A_*^2)`.                           (9)

If (8) is negative, the exact interior value is

`Phi_interior=sqrt(c) B_*/sqrt(a)`.                            (10)

Indeed, after the other rectangle direction has been maximized, the remaining
function is `2cAB_*/(a+cA^2)`, whose exact derivative is
`2cB_*(a-cA^2)/(a+cA^2)^2`.  Its critical point is `A=sqrt(a/c)`,
and substitution gives (10).  The script checks both identities symbolically.

These are formulas for the maximum on the whole rectangle, not values merely
sampled at a repeated-length theta.  The certificate reconstructs `D_*`, `a`,
`B_branch`, (9), and the squared inequality for (10) from (2); none of the
decisive polynomials are entered as stand-alone conclusions.

## Reduction from arbitrary `g>=9`

Let `o` and `e` be the shortest odd and even paths.  Then `g=o+e>=9`.  For
fixed parity, (2) and the exact difference identities

`A_u-A_(u+2k)=z^((u-1)/2)(1-z^k)(1-z^(u+k))`

`                 /((1+z^u)(1+z^(u+2k)))`,

`B_v-B_(v+2k)=z^(v/2-1)(1-z^k)(1+z^(v+k))`

`                 /((1-z^v)(1-z^(v+2k)))`                     (11)

show that every path contribution lies in the cap rectangle

`0<=Abar<=r A_o`, `0<=Bbar<=s B_e`.                            (12)

The `D` remainders must also be retained.  For `l=o+2k` and `m=e+2k`, direct
subtraction gives

`C_l-C_o=z^(o-1)(1+z)(1-z^(2k))`

`            /((1+z^o)(1+z^l)) >=0`,

`G_e-G_m=z^(e-1)(1+z)(1-z^(2k))`

`            /((1-z^e)(1-z^m)) >=0`.                          (13)

Consequently the actual denominator term is exactly

`D=D_*+z U-z V`,                                               (14)

where `U` is the sum of the odd differences and `V` the sum of the even
differences in (13).  The script checks both rational difference identities
symbolically.  Equations (12)-(14) are precisely the admissible set used in
the rectangle maximization.  Dropping `U,V`, or treating `D` as fixed while varying
`Abar,Bbar`, would recover the invalid corner-only argument.

For `g>=9`, choose the odd cap endpoint

`o_0=min(o,7)` with the same odd parity progression, and `e_0=9-o_0`.

If `o<=7`, then `e>=9-o=e_0`; if `o>=9`, all odd contributions are contained
in the `o_0=7` odd interval and every even path has length at least `2=e_0`.
The monotonicities (11), with the signed remainders (13)-(14), therefore give
set inclusion into one of the eight cap rectangles

`(1,8;r,s)`, `(3,6;r,s)`, `(5,4;r,s)`, `(7,2;r,s)`, `r=1,2`.   (15)

Thus the eight-cap certificate below applies to every `g>=9` theta whose
same-parity paths share a residue modulo four.  When two same-parity paths
differ by `2 mod 4`, their signed contributions can have opposite signs;
in that case the unsigned rectangle maximization does not directly bound
the signed carrier, because `D=N/F` is coupled to each individual path
through (6).  A complete proof for arbitrary paths requires a 16-case
parameterized certificate preserving all sign correlations; see the
Status section below.  The eight-cap calculation is exact and verified for
its stated scope.

## Seven endpoint caps

Set `z=3x/4`, `0<=x<=1`.  For every cap except `(1,8;2,1)`, the script first
clears the positive denominator of `B_branch` and proves its numerator
nonnegative by exact Bernstein coefficients.  Hence (9) is the exact rectangle
maximum.  It then forms

`4z^4-Y_endpoint=z^k L(z)/(positive denominator)`              (16)

from the formulas above and proves `L>=0` on `[0,3/4]` by a second exact
Bernstein conversion.  Every expansion is inverted back to the source
polynomial as a check on the conversion itself.

The seven endpoint polynomials all have degree eight.  Their exact minimum
Bernstein coefficients are:

| cap | minimum coefficient of `L(3x/4)` |
|---|---:|
| `(1,8;1,2)` | `83927/16384` |
| `(3,6;1,2)` | `76439/16384` |
| `(3,6;2,1)` | `83927/16384` |
| `(5,4;1,2)` | `69527/16384` |
| `(5,4;2,1)` | `76439/16384` |
| `(7,2;1,2)` | `60839/16384` |
| `(7,2;2,1)` | `69527/16384` |

Therefore `Phi<=4z^4` throughout each of these seven whole rectangles.

## Split exceptional cap

For `(1,8;2,1)`, the endpoint branch is valid on `[0,1/4]`.  Exact Bernstein
coefficients prove both `B_branch>=0` and the degree-eight endpoint polynomial
`L>=0` there; the minimum coefficient of `L(x/4)` is `157283/16384`.

On `[1/4,3/4]`, use the interior maximizer (10).  After squaring
`Phi_interior<=4z^4`, clearing its positive denominator, and removing the
positive origin power, the script reconstructs the following `J`.  It also
certifies the numerator and denominator of `a` strictly positive on this
interval, so the square root and the cleared inequality are legitimate:

`J(z)=16z^17-32z^16+48z^15-64z^14+80z^13-96z^12+112z^11`

`     -128z^10+128z^9-128z^8+112z^7-96z^6+80z^5-64z^4`

`     +48z^3-32z^2+16z-1`.                                    (17)

Under `z=(1+2x)/4`, all 18 exact Bernstein coefficients of `J` are positive,
and their exact minimum is

`1674992681/1073741824`.                                       (18)

This proves the same `Phi<=4z^4` bound on the interior part.  Combining the
two pieces certifies the whole exceptional rectangle.

## Exact area budget

By (5), `atan(t)<t`, and all eight rectangle certificates,

`alpha(z)<4z^(9/2)`, for `0<z<=3/4`.                           (19)

Hence

`int_0^(3/4) (z^-2-1)alpha(z) dz`

` < int_0^(3/4) 4(z^(5/2)-z^(9/2)) dz`

` =3051 sqrt(3)/19712`.                                       (20)

On `[3/4,1]`, the right-half-plane carrier gives `alpha<=pi/2`, while

`int_(3/4)^1 (z^-2-1) dz=1/12`.                               (21)

Thus the retained exact budget is

`I<3051 sqrt(3)/19712+pi/24`.                                 (22)

Finally, the script verifies `pi>3` using the eight-term alternating lower sum
for `atan(1)`, and `sqrt(3)<2` by squaring.  Therefore

`pi/5-I>19pi/120-3051sqrt(3)/19712`

`       >19/40-6102/19712=8153/49280>0`.                       (23)

This proves (1) for every theta covered by the eight-cap reduction.

## Status: remaining gate for arbitrary paths

The eight cap certificates are exact for repeated-length carriers.  For
arbitrary actual paths, `P/F` and `Q/F` are alternating signed sums whose
terms can have opposite signs when two same-parity paths differ by
`2 mod 4`.  The unsigned rectangle maximization does not directly bound
the signed carrier in that case.

A complete proof is supplied by the 16-case parameterized certificate
`experiments/theta_g9_signed_certificate.py`:

- split by shortest residue pair `(1,4)` or `(3,2)`;
- split by mandatory `+4` allocation (odd or even);
- split by doubled parity (odd or even);
- split by companion displacement (`+4k` or `+2+4k`).

Each case introduces power variables `X,Y,W` for the longer paths,
constructs `K=4z^4R-S` as a polynomial in `z,X,Y,W`, and certifies
`K>=0` on `[0,3/4]x[0,1]^3` by exact tensor Bernstein coefficients with
subdivision.  This preserves all sign correlations and the shared
dependence of `N,P,Q,R,S` on every path power.  The 16-case list is
exhaustive as a cover (some thetas map to multiple cases, which is
harmless).  All 16 cases pass with zero adaptive subdivisions needed.
Combined with the already-proved `R>0` and `S>0` in the positive-phase
class (from `theta-imaginary-phase.md` and `theta-phase-sign-theorem.md`),
`K>=0` gives `S/R<=4z^4`, hence `alpha<4z^(9/2)` for `0<z<=3/4`.
The area budget (22)-(23) then proves (1) for every `g>=9` theta.


## Reproduction

Run from `positive-square-energy/`:

```text
python3 experiments/theta_g9_phase_certificate.py
python3 -m py_compile experiments/theta_g9_phase_certificate.py
```

The expected final certificate line is

```text
theta g>=9 whole-rectangle phase certificate: PASS (8/8 caps)
```
