# Direct-breakpoint complete endpoint certificates

For a dyadic `N`, write the exact `N -> 2N` endpoint channels as

\[
 f(t)=1+\sum_{a\le2N}u_a\{t/a\},\qquad
 d(t)=\sum_{a\le2N}d_a\{t/a\},\qquad
 \alpha_N=\frac{\log 2}{\log(2N)}.
\]

The target is the complete, untruncated functional

\[
 \mathcal E_N=\int_1^\infty
 [2f(t)d(t)-\alpha_Nd(t)^2]\,\frac{dt}{t^2}.
\]

No Fourier series or common period is used. On each open unit interval
`(k,k+1)`, every breakpoint function is exactly
`{t/a}=t/a-floor(k/a)`. Hence `f=A t+B_k`, `d=D t+E_k`, and the numerator is
`c_2 t^2+c_1 t+c_0`. Its interval contribution is evaluated by Arb as

\[
 c_2+c_1\log((k+1)/k)+c_0/[k(k+1)].
\]

Summing these outward-rounded expressions certifies `[1,T]`. For the omitted
tail, the pointwise bounds

\[
 |f|\le1+\sum|u_a|=:F,\qquad |d|\le\sum|d_a|=:D
\]

give the elementary enclosure

\[
 \left|\int_T^\infty(2fd-\alpha_Nd^2)t^{-2}dt\right|
 \le (2FD+\alpha_ND^2)/T.
\]

The script also performs an independent normalization audit. It constructs
`F_N` and `F_2N` separately from their Mobius-logarithmic coefficients and
integrates `F_N^2-F_2N^2` breakpoint by breakpoint. The exact affine identity
`F_2N=F_N-alpha_N d` gives

\[
 P_N-P_{2N}=\alpha_N\mathcal E_N.
\]

The two computations share only the elementary integration routine; the
coefficient construction and quadratic numerators are independent. Both
omitted tails receive pointwise absolute enclosures. Run

```
uv run --with python-flint python certify_endpoint_tail.py --bits 192 --cutoff 4096 --N 2 4 8 16
```

from this directory. `test_endpoint_tail.py` checks the affine coefficients,
finite-prefix additivity, remainder bounds, the alpha-normalized independent
identity, and positivity of both complete enclosures for all four values.

At 192-bit precision with `T=4096`, the certified complete intervals are

\[
\begin{array}{c|c|c}
N&\mathcal E_N&P_N-P_{2N}\\ \hline
2 &[1.9491262021,1.9523787976]&[0.9726099760,0.9781425238]\\
4 &[1.5986773125,1.6065762431]&[0.5293130147,0.5391048372]\\
8 &[0.9896370511,1.0112272914]&[0.2411968631,0.2590192225]\\
16&[0.5701852472,0.6343383735]&[0.1024270898,0.1384776344]
\end{array}
\]

Every endpoint functional and every independent energy difference is strictly
positive. The scaled endpoint enclosure overlaps the direct difference
enclosure in every row. These are finite small-`N` certificates, not an
asymptotic result; they also reinforce that the negative oscillatory component
of the `N=4 -> 8`, `R=3` Fourier surrogate does not determine the complete
sign.
