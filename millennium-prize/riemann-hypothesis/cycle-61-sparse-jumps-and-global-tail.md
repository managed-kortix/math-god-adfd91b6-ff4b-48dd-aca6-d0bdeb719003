# Cycle 61: sparse floor jumps and the global-tail operator

## Sparse jump search

Retain the Cycle 59 quotient and matched shell. Candidate surplus cells were
chosen at floor-signature changes

\[
j=nq+e,\qquad M\le q<B,\quad2\le n\le16,\quad e\in\{-1,0,1\}.
\]

For every candidate, the floor constraints and null directions were solved
exactly over the rationals. Search ranking used floating arithmetic, but every
reported optimum was recomputed from the exact directions with 256-bit Arb
logarithms and a positive-definite solve.

The strongest single, pair, and triple scores were:

| window | best single | best pair | best triple |
|---|---:|---:|---:|
| `[98,99)` | `2.39906078968e-4` | `6.43440345187e-4` | `8.08558680289e-4` |
| `[219,231)` | `3.10951523021e-5` | `1.48084354967e-4` | `1.90074278953e-4` |
| `[220,231)` | `3.24394602943e-5` | `1.44230395866e-4` | `1.89861823880e-4` |
| `[222,226)` | `2.83261352636e-5` | `1.29062743943e-4` | `2.00969573532e-4` |

The best pairs were `{196,1273}`, `{459,661}`, `{459,661}`, and `{446,1576}`
in row order. Greedy selection of sixteen sparse cells gave:

| window | `Omega_K` | approximate fraction of required payment |
|---|---:|---:|
| `[98,99)` | `0.00119331139226760423` | `1.47%` |
| `[219,231)` | `0.000683132772414039000` | `1.42%` |
| `[220,231)` | `0.000648117113221465364` | `3.48%` |
| `[222,226)` | `0.000520708695051379691` | `1.31%` |

Thus sparse jump cells are more efficient individually than generic cells, but
the tested bounded families are even weaker cumulatively than the 24-cell
consecutive shells of Cycle 60. No tested family approaches the target.

## A rigorous fixed-sparse upper bound

Let `K` consist of the matched shell and fixed surplus cells `j_i`, and let
`x_i=B_(j_i)`. Exact triangular elimination gives

\[
m_{B-1}A+\theta\cdot x=0,
\qquad
\ell A+\sum_{k\in K}v_kB_k=\alpha A+\eta\cdot x.  \tag{61.1}
\]

If `gamma=eta-alpha theta/m_(B-1)`, the Cycle 60 energy immediately yields

\[
\boxed{\Omega_K\le\sum_i{\gamma_i^2\over j_i(j_i+1)}.}           \tag{61.2}
\]

The apparent inverse power of `m_(B-1)` is not intrinsic. Retaining `A` in the
energy and writing `N=|K|` gives the uniform estimate

\[
\boxed{\Omega_K\le2\left(N\alpha^2+{\|\eta\|_2^2\over M^2}\right).} \tag{61.3}
\]

Floor jumps only change the bounded integer coefficients defining `alpha` and
`eta`. Neither (61.2) nor (61.3) has polynomial decay from elementary Möbius
bounds: such decay is exactly a cancellation theorem for the compensated
divisor-floor quantities `alpha` and `eta`. Fixed sparse dimension and floor
geometry do not provide it.

## Infinite-tail dual and innovations

Let `X_M` be the completion of finitely supported tail moment sequences under
the Cycle 59 cell metric, and let `C:X_M->R^(B-M+1)` be the old-`U` and new-row
constraint operator. Let `S` be the old-`D` score and `sigma` its Riesz vector.
Infinite sums are interpreted as Hilbert-space inner products; separating a
generally divergent `sum A_k` from the compensating floor terms is forbidden.

The best witness supported on the complete tail is exactly

\[
\boxed{\Omega_\infty=
\|\Pi_{\ker C}\sigma\|_{X_M}^2
=\|\sigma\|^2-
\langle C\sigma,(CC^*)^+C\sigma\rangle.}           \tag{61.4}
\]

It remains only a lower bound for the full residual `R`, because `R` can retain
the one boundary/below-`M` channel identified in Cycle 56.

If `N_n` denotes constrained moments supported on cells `M,...,n` and

\[
J_n=N_n\ominus N_{n-1},
\]

then finite-dimensional constraint correction proves density of their union in
`ker C`, and Parseval gives

\[
\boxed{\Omega_\infty=
\sum_{n\ge M}\|\Pi_{J_n}\sigma\|^2
=\lim_{n\to\infty}\Omega_{[M,n]}.}                \tag{61.5}
\]

Hence constant-scale global accumulation is possible even though every bounded
local family is weak. But only the orthogonal innovations—the differences of
nested cumulative scores—may be summed. Arbitrary local witness scores overlap
and cannot be added.

The unresolved statement is now sharply global: prove a positive arithmetic
angle between the Möbius score vector and the closed divisor-floor row space,
or show that the innovation sum pays the additive-window deficit. Rank growth,
local jump placement, and frame completeness do not imply such an angle. No
additive-12 theorem or RH result is claimed.
