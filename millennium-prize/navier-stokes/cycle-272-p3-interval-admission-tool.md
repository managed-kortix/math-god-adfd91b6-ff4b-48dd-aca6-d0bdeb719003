# Cycle 272: rigorous P3 admission certificate with zeros and Fourier tails

## Result

For normalized Haar measure on `T^3=[0,2 pi]^3`, the script
`certify_p3_admission.py` rigorously encloses

\[
 {\cal P}_3(u)=3\int p\,u\cdot\nabla |u|,
 \qquad -\Delta p=\partial_i\partial_j(u_i u_j).
\]

It uses exact rational Fourier algebra and Arb outward-rounded balls. It offers
three treatments of zeros: direct box partition, the regularized denominator
`( |u|^2+epsilon^2 )^(1/2)`, and the nonsingular identity

\[
 {\cal P}_3(u)=-3\int |u|\,u\cdot\nabla p.              \tag{272.1}
\]

The last form is the preferred certificate. It is Lipschitz even at `u=0` and
therefore avoids an illegitimate interval division by a speed interval
containing zero. The direct and regularized values remain diagnostic breakers.
A diagnostic is printed as `null` rather than admitted if dependency
overestimation prevents a finite Arb enclosure.

## Finite Fourier construction

The input prints rational real trigonometric modes `a cos(k.x)` or
`a sin(k.x)`. The verifier checks `k.a=0`, constructs conjugate complex Fourier
coefficients, and solves pressure exactly by

\[
 \widehat p_k=-{k_i k_j\over |k|^2}
     \sum_{r+s=k}\widehat u_{i,r}\widehat u_{j,s},\quad k\ne0. \tag{272.2}
\]

On every Cartesian box, Arb evaluates all trigonometric functions with outward
rounding. Boxes whose speed-squared interval excludes zero evaluate the original
quotient. Other boxes receive the integrable absolute bound

\[
  |3p\,u\cdot\nabla|u||\le3|p|\,|u|\,|\nabla u|_F.       \tag{272.3}
\]

The regularized functional differs from the original by at most

\[
 3\epsilon\,\|p\|_\infty\|\nabla u\|_\infty,           \tag{272.4}
\]

using `|1-sqrt(s/(s+epsilon^2))| sqrt(s)<=epsilon`.

For efficient proof on a datum bounded away from zero, the tool may instead
expand `sqrt(S0(1+x))` by the binomial polynomial. It verifies
`||x||_infinity <= rho < 1` from the exact Fourier `l1` norm, computes the
integral of every polynomial term exactly as its zero Fourier coefficient, and
bounds the remainder conservatively by

\[
 3\sqrt{S_0}\,\|u\|_\infty\|\nabla p\|_\infty
 {\rho^{d+1}\over1-\rho}.                              \tag{272.5}
\]

## Analytic Fourier tail

An infinite-support caller supplies proved bounds
`R0=sum |rhat_k|` and `R1=sum |k|_1 |rhat_k|`. If `u=v+r`, the script uses

\[
 \|p(u)-p(v)\|_\infty\le3(2V_0R_0+R_0^2)
\]

and a product estimate for (272.1). Writing
`G_v=||grad p(v)||_infinity` and
`G_r=6(V1 R0+V0 R1+R0 R1)`, the printed fail-closed radius is

\[
 3\{(2V_0+R_0)R_0G_v+(V_0+R_0)^2G_r\}.               \tag{272.6}
\]

This deliberately coarse bound is reusable for any independently proved
analytic tail majorant. A zero tail is valid for the local functional at a
trigonometric initial datum; it is not a claim that the Euler trajectory keeps
finite support. The full generated tail is controlled separately by the
shrinking Wiener majorant in
`cycle-272-p3-finite-support-admission-audit.md`.

## Proof datum

`cycle-272-p3-example.json` is a genuine three-dimensional rational
trigonometric field. Its support contains `(0,0,1)`, `(1,1,0)`, and `(1,1,1)`,
which span `R^3`. Every printed polarization is perpendicular to its wave
vector. A circular shear of amplitude `256` keeps speed away from zero, while
five interacting 3D waves produce a nonzero derivative. The exact speed-square
Fourier norm verifies `||x||_infinity <= 0.11111 < 19/125`.

Run:

```text
uv run --with python-flint python certify_p3_admission.py \
  --input cycle-272-p3-example.json --subdivisions 1 --precision 96 \
  --output cycle-272-p3-certificate.json
```

The degree-six exact Fourier polynomial and its rigorous remainder give a
strictly positive lower endpoint. The box, regularization, tail, and polynomial
error radii are all printed. This certifies a nonzero initial complete-velocity
`L3^3` derivative only; it is not a trajectory or factor-two certificate.

All certificate Arb fields are decimal balls re-parsed and checked to contain
the in-memory ball before JSON is written. Non-finite values, negative tail
bounds, malformed polynomial bounds, and insufficient precision fail closed.
