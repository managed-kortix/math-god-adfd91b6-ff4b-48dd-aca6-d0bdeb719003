# Cycle 40: dyadic norm-defect averages and the exact renewal mass

## 1. The norm defect and its first telescope

Put

\[
 L_n=\log n,\qquad h_n={1\over L_n}-{1\over L_{n+1}},\qquad
 w_n=h_nL_n=1-{L_n\over L_{n+1}},
\]

and retain the reciprocal-log Mobius path from Cycle 39,

\[
 F_n=U_n-{D_n\over L_n},\qquad P_n=\|F_n\|^2,
 \qquad A_n=L_nP_n.
\]

Define the singleton norm defect

\[
 \boxed{H_n:=\|D_n\|^2-L_nL_{n+1}\|U_n\|^2.}             \tag{40.1}
\]

The mixed-term cancellation in the exact coefficient update gives

\[
 A_{n+1}-A_n=(L_{n+1}-L_n)
 \left(\|U_n\|^2-{\|D_n\|^2\over L_nL_{n+1}}\right).
\]

Since `h_n=(L_(n+1)-L_n)/(L_nL_(n+1))`, this is exactly

\[
 \boxed{h_nH_n=A_n-A_{n+1}.}                              \tag{40.2}
\]

Therefore, for every pair of integers `2<=a<b`, and in particular for a
dyadic interval `[X,2X)`,

\[
 \boxed{\sum_{n=a}^{b-1}h_nH_n=A_a-A_b
       =L_aP_a-L_bP_b,}                                   \tag{40.3}
\]

\[
 \boxed{\sum_{X\le n<2X}h_nH_n
       =(\log X)P_X-(\log(2X))P_{2X}.}                    \tag{40.4}
\]

The normalizing mass also telescopes exactly:

\[
 \sum_{X\le n<2X}h_n={1\over\log X}-{1\over\log(2X)}.
\tag{40.5}
\]

Thus the `h`-weighted mean is known without any interior sum:

\[
 {\sum_{X\le n<2X}h_nH_n\over\sum_{X\le n<2X}h_n}
 ={(\log X)P_X-(\log(2X))P_{2X}
   \over1/\log X-1/\log(2X)}.                             \tag{40.6}
\]

This identity is useful but is not yet the critical renewal inequality.
Positivity in (40.4) says only that the log-scaled endpoint energy does not
increase across the block.

## 2. The renewal-weighted telescope

At the critical value `kappa=1/2`, the block residual is

\[
 \mathcal R(a,b):=P_a-P_b-\sum_{n=a}^{b-1}w_nP_n.
\tag{40.7}
\]

Combining the Cycle 39 summation-by-parts identity with (40.2) gives the exact
norm-defect average

\[
 \boxed{\mathcal R(a,b)
 =\sum_{n=a}^{b-1}{h_n\over L_{n+1}}H_n.}                 \tag{40.8}
\]

Equivalently, a second summation by parts gives

\[
 \boxed{\sum_{n=a}^{b-1}{h_n\over L_{n+1}}H_n
 ={A_a\over L_{a+1}}-{A_b\over L_b}
  -\sum_{n=a+1}^{b-1}h_nA_n.}                            \tag{40.9}
\]

The right side is precisely
`P_a-P_b-sum_(a<=n<b)w_nP_n`. Hence the extra factor
`1/L_(n+1)` cannot be discarded. Because the defects may change sign,

\[
 \sum_{a\le n<b}h_nH_n\ge0
 \quad\not\Longrightarrow\quad
 \sum_{a\le n<b}{h_n\over L_{n+1}}H_n\ge0.              \tag{40.10}
\]

For example, a negative defect near the left endpoint and a compensating
positive defect near the right endpoint can make the first sum nonnegative
while the decreasing factor `1/L_(n+1)` makes the second negative. Thus plain
log-scaled endpoint monotonicity is strictly weaker than block renewal.

## 3. Weakest averaged positivity for a chained dyadic renewal

Fix `X_j=2^jX_0` and let `I_j=[X_j,X_(j+1))`. The weakest sign assertion on
the complete defect average that gives the critical renewal inequality on this
particular chain is exactly

\[
 \boxed{\sum_{n\in I_j}{h_n\over L_{n+1}}H_n\ge0
 \qquad(j\ge0).}                                         \tag{40.11}
\]

No pointwise positivity of `H_n`, no positivity of the `h`-weighted mean, and
no renewal from every possible start is needed. By (40.8), (40.11) is
equivalent to

\[
 P_{X_j}-P_{X_{j+1}}\ge\sum_{n\in I_j}w_nP_n.            \tag{40.12}
\]

Summing consecutive blocks telescopes the endpoints:

\[
 \sum_{X_0\le n<X_J}w_nP_n
 \le P_{X_0}-P_{X_J}\le P_{X_0}.                         \tag{40.13}
\]

Since the intervals cover the full tail and `sum w_n=infinity`, (40.13)
forces `liminf P_n=0`. For the arithmetic energies this is RH-sufficient by
the previously established off-critical-zero floor. Condition (40.11) is not
claimed proved.

There is a sharp lossy version. Let `0<=c_j<=1` and assume only

\[
 \boxed{\sum_{n\in I_j}{h_n\over L_{n+1}}H_n
 \ge -(1-c_j)\sum_{n\in I_j}w_nP_n.}                     \tag{40.14}
\]

Using (40.8), this is exactly the weakened block renewal

\[
 P_{X_j}-P_{X_{j+1}}
 \ge c_j\sum_{n\in I_j}w_nP_n.                           \tag{40.15}
\]

The abstract liminf argument works if and only if the surviving effective
coefficient mass is divergent in every tail:

\[
 \boxed{\sum_{j\ge J}c_jW_j=\infty\quad\hbox{for every }J,
 \qquad W_j:=\sum_{n\in I_j}w_n.}                        \tag{40.16}
\]

Indeed, summing (40.15) shows
`sum_j c_j sum_(n in I_j)w_nP_n<=P_(X_0)`. If `P_n` had a
positive tail lower bound, (40.16) would contradict this bound. Conversely,
if `sum c_jW_j<infinity`, finite effective energy is compatible with a
positive lower bound, so this telescope alone cannot force zero liminf. For
example, define a positive block-constant sequence recursively by
`p_(j+1)=p_j(1-c_jW_j)` after deleting finitely many blocks so that
`c_jW_j<1`; then (40.15) holds with equality and `p_j` tends to a positive
limit whenever `sum c_jW_j<infinity`. This establishes sharpness for arbitrary
nonnegative sequences.

For the liminf conclusion alone, even blockwise positivity can be weakened.
It is enough that (40.15) hold with errors `-e_j` on the right, provided the
cumulative positive error is bounded:

\[
 P_{X_j}-P_{X_{j+1}}
 \ge c_j\sum_{n\in I_j}w_nP_n-e_j,
 \qquad e_j\ge0,\qquad \sum_je_j<\infty.                 \tag{40.17}
\]

Then partial summation over blocks bounds the effective weighted energy by
`P_(X_0)+sum e_j`, and the same divergent-mass contradiction applies. More
generally, it suffices that the partial sums of the signed errors be uniformly
bounded above. Exact renewal on every listed block, however, is specifically
the zero-error condition (40.11).

## 4. Exact size of the dyadic mass

Although `W_j` does not itself telescope, it has the elementary comparison

\[
 L_{X_j}
 \left({1\over L_{X_j}}-{1\over L_{X_{j+1}}}\right)
 \le W_j\le
 L_{X_{j+1}}
 \left({1\over L_{X_j}}-{1\over L_{X_{j+1}}}\right),     \tag{40.18}
\]

obtained by bounding `L_n` in `W_j=sum_(n in I_j)h_nL_n`.
Writing `ell_j=log X_j` and `d=log 2`, this becomes

\[
 {d\over\ell_j+d}\le W_j\le {d\over\ell_j},
 \qquad W_j\sim{\log2\over\log X_j}\asymp{1\over j}.   \tag{40.19}
\]

Consequently the exact divergent-mass threshold for dyadic losses is

\[
 \boxed{\sum_j{c_j\over j}=\infty,}                      \tag{40.20}
\]

up to deletion of finitely many blocks. A fixed positive `c_j` works. A loss
`c_j` comparable to `1/log X_j` does not: it leaves mass comparable to
`sum 1/j^2`, which converges. More generally `c_j` may tend to zero arbitrarily
slowly provided the harmonic-weighted series in (40.20) still diverges.

## 5. Verdict

The natural `h_n`-weighted sum of `H_n` telescopes exactly to the difference of
the log-scaled endpoint energies. Renewal uses the slightly different natural
weight `h_n/L_(n+1)`, and its nonnegative block average is exactly, rather than
merely sufficiently, the critical block inequality. For a single consecutive
dyadic chain, this averaged positivity is enough; every-start reverse Hardy
positivity is unnecessary for the liminf implication. After block-dependent
losses, the surviving mass must satisfy `sum c_j/j=infinity`. The previously
proposed `1/log X` strength lies just below that threshold by one harmonic
factor.
