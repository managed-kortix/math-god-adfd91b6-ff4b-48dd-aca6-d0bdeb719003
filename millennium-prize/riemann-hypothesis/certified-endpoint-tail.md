# Direct-breakpoint endpoint-tail certificate

For the exact `N=4 -> 8` endpoint channels, write

\[
 f(t)=1+\sum_{a\le8}u_a\{t/a\},\qquad
 d(t)=\sum_{a\le8}d_a\{t/a\},\qquad \alpha=1/3.
\]

The target is the full, untruncated tail

\[
 \int_8^\infty [2f(t)d(t)-\alpha d(t)^2]\,\frac{dt}{t^2}.
\]

No Fourier series or common period is used. On each open unit interval
`(k,k+1)`, every breakpoint function is exactly
`{t/a}=t/a-floor(k/a)`. Hence `f=A t+B_k`, `d=D t+E_k`, and the numerator is
`c_2 t^2+c_1 t+c_0`. Its interval contribution is evaluated by Arb as

\[
 c_2+c_1\log((k+1)/k)+c_0/[k(k+1)].
\]

Summing these outward-rounded expressions certifies `[8,T]`. For the omitted
tail, the pointwise bounds

\[
 |f|\le1+\sum|u_a|=:F,\qquad |d|\le\sum|d_a|=:D
\]

give the elementary enclosure

\[
 \left|\int_T^\infty(2fd-\alpha d^2)t^{-2}dt\right|
 \le (2FD+\alpha D^2)/T.
\]

Thus the script proves positivity of the complete integral, not a harmonic
surrogate. Run

```
uv run --with python-flint python certify_endpoint_tail.py --bits 192 --cutoff 1024
```

from this directory. `test_endpoint_tail.py` independently checks the affine
and quadratic coefficients, finite-prefix additivity, the elementary remainder
constant, and strict positivity of the final enclosure.

At 192-bit precision with `T=1024`, the certificate is

\[
\boxed{0.2004969520996<\mathcal T_8<0.2320926742316.}
\]

Thus the full untruncated endpoint tail is strictly positive. This directly
falsifies any attempt to infer the complete-tail sign from the negative
oscillatory component of the `R=3` Fourier surrogate.
