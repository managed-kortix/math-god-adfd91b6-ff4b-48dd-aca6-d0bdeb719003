# Cycle 194: loose rigorous derivative certificate for `D=-29023`

## Result

For the quadratic twist of `433a1` by `D=-29023`, the conductor and root
number are

\[
 N=364730851057=433\cdot29023^2,\qquad w=-1.
\]

The same exact odd-sign approximate functional equation used in Cycle 193 is

\[
 L'(E^{(-29023)},1)=2\sum_{n\geq1}\frac{a_n}{n}
 E_1\!\left(\frac{2\pi n}{\sqrt N}\right).                 \tag{194.1}
\]

An intentionally crude directed-rational calculation proves

\[
 \boxed{9.776577544974464\leq L'(E^{(-29023)},1)
                     \leq141.618654480665006}.                \tag{194.2}
\]

The lower bound is much looser than the actual value but is already strictly
positive. Together with `w=-1`, it certifies analytic rank one for this
individual twist. It does not prove any general BSD case.

## Deliberately low precision and coarse quadrature

The verifier uses only

\[
 M=650000,\qquad K=1,\qquad S=10^{15}.
\]

Here `M` is the coefficient cutoff, `K` is the number of midpoint/trapezoid
subintervals in each unit cell, and `S` is the fixed-point denominator. Thus
there is just one midpoint and one trapezoid per cell, and about 50 binary bits
of directed fixed-point precision. This is substantially less stringent than
Cycle 193's `K=16`, `S=10^50` certificate.

Machin-series rational bounds enclose

\[
 \alpha=\frac{2\pi}{\sqrt N}
 =0.000010403838892284317869514074224245190037638796397\ldots.
\]

For `f(u)=exp(-alpha*u)/u`, positivity and convexity make the one-panel
midpoint rule a lower bound and the one-panel trapezoid rule an upper bound on
each `[n,n+1]`. Directed integer arithmetic propagates the exponential grid.
At `M+1`, the remaining `E1` integral is bounded by

\[
 \frac{e^{-x}}{x+1}\leq E_1(x)\leq\frac{e^{-x}}x.
\]

Using the first `650000` exact integer coefficients, the finite sum lies in

\[
 [75.518458081702825,\ 75.876773943936645].                  \tag{194.3}
\]

The CSV is pinned by SHA-256

```text
cc7f4e63833e33728233bc8b69a60b6a0609a84cabaafb3c2919b4d79b0992b1
```

## Crude infinite tail

Deligne and `d(n)<=2*sqrt(n)` give `|a_n|<=2n`. Therefore

\[
 \left|2\sum_{n>M}\frac{a_n}{n}E_1(\alpha n)\right|
 \leq \frac{4e^{-\alpha(M+1)}}
 {\alpha(M+1)(1-e^{-\alpha})}
 <65.741880536728361.                                      \tag{194.4}
\]

No cancellation is used after `M`. Subtracting and adding (194.4) to (194.3)
gives (194.2). The tail, rather than arithmetic precision or quadrature error,
dominates the interval width.

## Validation and resource estimate

The previously reported PARI value

\[
 75.657891889970836850511571591763350569\ldots
\]

lies strictly inside (194.2), and also inside the much tighter finite-sum
interval (194.3). This numerical agreement is a validation only; positivity
uses the rational lower endpoint in (194.2).

The coefficient generator completed locally in about two seconds at
`M=10^6`; the final `M=650000` table is about 9 MB. The Python verifier takes
about six seconds and stores four integer arrays of length `M+1`, so a
conservative resource budget is under 15 seconds and under 250 MB. PARI grew
its working stack to 32 MB while generating coefficients. A practical minimum
for this exact crude-tail strategy is near `M=650000`: at `M=600000` the same
elementary tail bound is about `119.82`, too large for a positive lower bound,
whereas at `M=650000` it is `65.74`. Choosing `M=700000` raises the certified
lower bound to about `39.25`; `M=10^6` gives a tail near `1.12` and a lower
bound near `74.43`, but neither is needed for nonvanishing.

## Reproduction

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/cycle194_generate_D29023_coefficients.gp
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle194_D29023_afe.py
```

The verifier uses only Python's exact integers and `Fraction`; no binary
floating-point value participates in a certification decision.
