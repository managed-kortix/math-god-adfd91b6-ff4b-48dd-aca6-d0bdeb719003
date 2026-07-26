# Cycle 39: extended complete-Gram adaptive scan

## Scope

This cycle is finite only. It optimizes the exact finite Arb evaluation of the
restricted energies

\[
 P_N=\left\|\chi+\sum_{a\leq N}\mu(a)
 {\log(N/a)\over\log N}\rho_a\right\|_{L^2(0,1)}^2
\]

from the complete Vasyunin Gram formula of Cycle 38, and scans complete block
ratios

\[
 \mathcal R(a,b)={P_a-P_b\over
 2\sum_{a\leq n<b}(1/\log n-1/\log(n+1))(\log n)P_n}.
\tag{39.1}
\]

There is no integration cutoff and no omitted-origin tail. All logarithms,
cotangents, Gram contractions, prefix sums, and ratios remain outward-rounded
Arb balls.

## Optimizations and diagnostics

`certify_complete_gram.py` now caches each denominator's complete cotangent
row, rather than reevaluating the same transcendental cotangents for every
Vasyunin numerator. It also uses

\[
 V(q-p,q)=-V(p,q)
\tag{39.2}
\]

to store only the reflected numerator class. The existing incremental three-
scalar Gram contraction still computes all `P_N` without repeating dense
quadratic forms.

For block work, define the certified prefix

\[
 W_m=2\sum_{2\leq n<m}
 \left(1-\frac{\log n}{\log(n+1)}\right)P_n.
\tag{39.3}
\]

Then the denominator in (39.1) is `W_b-W_a`. First passage and arbitrary block
queries are therefore constant-time after one linear prefix pass.

The new every-start scan encloses

\[
 K_a(B)=\max_{a<b\leq B}\mathcal R(a,b)
\tag{39.4}
\]

for every `2<=a<B`. The lower endpoint is the largest lower endpoint among all
candidate ratios, and the upper endpoint is the largest upper endpoint. Thus
the reported ball rigorously contains the finite maximum even if two candidate
balls overlap. It also reports a witness endpoint attaining the displayed
lower bound. Finally it encloses the finite common threshold

\[
 K_*(B)=\min_{2\leq a<B}K_a(B).
\tag{39.5}
\]

## Certified finite result through 2048

At 192-bit precision with `B=2048`:

| diagnostic | certified finite result |
|:--|:--|
| first-passage threshold | `R(a,b)>1/2` |
| chained range | `2` through `2048` |
| blocks | `2023` |
| longest block | `[219,231)`, length `12` |
| largest dilation | `[2,6)`, `b/a=3` |
| every-start scan | every `a=2,...,2047` has a witness `b<=2048` |
| common maximal threshold `K_*(2048)` | `[0.58975733076014293927179930704648092412643104090915 +/- 6.57e-51]` |
| weakest start | `a=2`, lower-bound witness `b=2048` |

In particular, there is **no failure of `kappa=1/2` through starting index
`2047` when endpoints up to `2048` are allowed**. This is stronger finite
coverage than following just one chain: every starting index in the range was
scanned against every later available endpoint.

The command was

```text
uv run --with python-flint python certify_complete_gram.py \
  --max-N 2048 --bits 192 --kappa 0.5 --scan-maximal --summary-only
```

The six focused tests pass, including symbolic `N=2,3`, Vasyunin reflection, the full/restricted
rank-one correction, incremental-versus-dense Gram contraction, prefix-versus-
direct block ratios, first passage, and exhaustive small-range maximal scans:

```text
uv run --with python-flint python -m unittest -v test_complete_gram.py
```

## Finite-only boundary

The scan proves only the displayed finite Arb inequalities. The value
`K_*(2048)>1/2`, the short observed waits, and the absence of a finite failure
do not imply that `K_a(B)>1/2` for later starts, that every stopping time is
finite, that a chain continues indefinitely, or that RH follows. A first
failure beyond the computed boundary may exist. Locating it requires extending
the exact finite computation; excluding it asymptotically requires the missing
Mobius-specific arithmetic theorem.
