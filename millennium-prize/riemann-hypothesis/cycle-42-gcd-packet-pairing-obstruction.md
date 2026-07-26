# Cycle 42: finite obstruction to gcd-packet injection

## Question tested

For a half-open block `[A,B)`, assign to each diagonal packet its positive
magnitude

\[
 d_a=R_{a,a}G_{a,a},
\]

and to each reduced pair `(p,q)` the positive magnitude

\[
 w_{p,q}=2\mathop{\sum_{d<B/q}}_{\mu(dp)\mu(dq)\ne0}
 R_{dp,dq}G_{dp,dq}.
\]

The signed contribution is `-d_a` on the diagonal and
`-mu(p)mu(q) w_(p,q)` off the diagonal. The proposed packet-only strategy asks
for an injection from all diagonal and equal-sign packets into opposite-sign
packets, with every image weight at least its source weight.

The script `cycle42_gcd_packet_pairing.py` evaluates these definitions directly.
It uses suffix sums for the exact block coefficient

\[
 R_{a,b}=\sum_{\max(A,a,b)\le n<B}\beta_n
 (L_nL_{n+1}-L_aL_b)
\]

and certified Arb enclosures of the complete restricted Vasyunin Gram entry.
No elementary/cotangent split and no absolute-value estimate is used.

## Certified finite blocks

At 192-bit precision the exact-formula census gives:

| block | diagonal | equal sign | unfavorable | opposite sign | unfavorable mass | favorable mass |
|---|---:|---:|---:|---:|---:|---:|
| `[2,8)` | 6 | 7 | 13 | 6 | 0.983220... | 1.003579... |
| `[2,16)` | 11 | 20 | 31 | 22 | 2.086492... | 1.952033... |
| `[2,32)` | 20 | 76 | 96 | 75 | 3.836890... | 3.541436... |

The first row already obstructs an injection by cardinality: thirteen distinct
unfavorable packets cannot inject into six favorable packets. This conclusion
does not depend on numerical ordering of the weights.

The block `[2,16)` gives the stronger obstruction

\[
 \sum_{\rm diagonal}d_a+
 \sum_{\mu(p)\mu(q)=1}w_{p,q}
 -\sum_{\mu(p)\mu(q)=-1}w_{p,q}
 =0.134460\ldots>0.
\]

Thus even if injectivity is dropped and favorable weights may be split or used
as arbitrary capacities, their total mass is insufficient. In particular, no
weight-preserving or weight-dominating pairing based only on packet sign can
work on every exact finite block.

## Scope

This is an obstruction to the stated packet-only mechanism, not to positivity
of the full weighted `H` block. Formula (41.4) also contains `-Q_1` and the
linear contraction `-2 sum mu(a)g_aQ_a`; that linear channel can compensate a
packet deficit. A viable continuation must therefore couple the pairing to the
linear term, aggregate several source packets through an identity that changes
the available budget, or restrict to specially chosen blocks and prove that
those blocks avoid the mass obstruction. Mobius signs and positive packet
weights alone are insufficient.

Reproduce with:

```sh
uv run --with python-flint python cycle42_gcd_packet_pairing.py 2:8 2:16 2:32
uv run --with python-flint python -m unittest -v test_cycle42_gcd_packet_pairing.py
```
