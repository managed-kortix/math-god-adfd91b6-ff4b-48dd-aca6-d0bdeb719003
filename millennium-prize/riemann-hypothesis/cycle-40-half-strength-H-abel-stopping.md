# Cycle 40: exact half-strength residual in H form

## 1. Direct one-cell calculation

For `n>=2`, write

\[
 L_n=\log n,\qquad \delta_n=L_{n+1}-L_n,
 \qquad h_n={\delta_n\over L_nL_{n+1}},
 \qquad w_n={\delta_n\over L_{n+1}}.
\]

On the complete reciprocal-log coefficient cell, put

\[
 U_n=1+\sum_{q\le n}\mu(q)\phi_q,
 \qquad D_n=\sum_{q\le n}\mu(q)(\log q)\phi_q.
\]

The two endpoint vectors are

\[
 F_n=U_n-{D_n\over L_n},\qquad
 F_{n+1}=U_n-{D_n\over L_{n+1}},
 \qquad P_j=\|F_j\|^2.
\]

Define the signed radial gap

\[
 \boxed{\mathcal H_n=\|D_n\|^2-L_nL_{n+1}\|U_n\|^2}                 \tag{40.1}
\]

and its positive weight

\[
 \boxed{\beta_n={h_n\over L_{n+1}}
 ={\delta_n\over L_nL_{n+1}^2}.}                                  \tag{40.2}
\]

At `kappa=1/2`, the one-cell residual is exactly

\[
 \boxed{P_n-P_{n+1}-w_nP_n=\beta_n\mathcal H_n.}                    \tag{40.3}
\]

This can be checked without invoking the earlier logarithmic-energy identity.
Since `1-w_n=L_n/L_(n+1)`, the left side is

\[
 {L_n\over L_{n+1}}\left\|U_n-{D_n\over L_n}\right\|^2
 -\left\|U_n-{D_n\over L_{n+1}}\right\|^2.
\]

The coefficient of `2<U_n,D_n>` is

\[
 -{1\over L_{n+1}}+{1\over L_{n+1}}=0.
\]

The coefficient of `||U_n||^2` is `-delta_n/L_(n+1)`, while that of
`||D_n||^2` is

\[
 {1\over L_nL_{n+1}}-{1\over L_{n+1}^2}
 ={\delta_n\over L_nL_{n+1}^2}.
\]

Thus the signs in (40.1)--(40.3) are forced: the `D_n` norm is favorable, the
`U_n` norm is unfavorable, and the mixed term vanishes. In particular,
`mathcal H_n>=0` is exactly the half-strength singleton inequality.

Summing (40.3) over a complete block gives the requested exact residual:

\[
 \boxed{\mathfrak R_{1/2}(a,b)
 :=P_a-P_b-\sum_{n=a}^{b-1}w_nP_n
 =\sum_{n=a}^{b-1}\beta_n\mathcal H_n.}                            \tag{40.4}
\]

There is no factor `1/2` in (40.4). If one instead uses the Cycle 38 surplus
`mathfrak S_(1/2)=(P_a-P_b)/2-(1/2)sum w_nP_n`, then
`mathfrak S_(1/2)=mathfrak R_(1/2)/2`.

## 2. Abel reduction to cumulative H

For a fixed start `a`, define the unweighted cumulative gaps

\[
 \boxed{\mathcal C_a(m)=\sum_{n=a}^m\mathcal H_n\qquad(m\ge a).}    \tag{40.5}
\]

The sequence `beta_n` is positive and strictly decreasing. Indeed,
`1/log x` is decreasing and strictly convex on `(1,infinity)`, so its forward
drops `h_n` decrease; `1/L_(n+1)` also decreases, and
`beta_n=h_n/L_(n+1)`.

Finite Abel summation now gives

\[
 \boxed{\begin{aligned}
 \mathfrak R_{1/2}(a,b)
 ={}&\beta_{b-1}\mathcal C_a(b-1)\\
 &+\sum_{m=a}^{b-2}(\beta_m-\beta_{m+1})\mathcal C_a(m).
 \end{aligned}}                                                   \tag{40.6}
\]

Every coefficient in (40.6) is positive, and their sum is `beta_a`. Hence

\[
 \beta_a\min_{a\le m<b}\mathcal C_a(m)
 \le \mathfrak R_{1/2}(a,b)
 \le \beta_a\max_{a\le m<b}\mathcal C_a(m).                       \tag{40.7}
\]

Thus nonnegative cumulative gaps throughout a candidate block are sufficient,
but not necessary, for a stop. The exact criterion is the positive Abel average
in (40.6), not the sign of the terminal cumulative gap alone.

## 3. Exact stopping theorem in H terms

Define

\[
 \mathcal B_a(m)=\sum_{n=a}^m\beta_n\mathcal H_n.
\]

By (40.6), `mathcal B_a(m)` is determined only by the cumulative values
`mathcal C_a(j)`:

\[
 \mathcal B_a(m)=\beta_m\mathcal C_a(m)
 +\sum_{j=a}^{m-1}(\beta_j-\beta_{j+1})\mathcal C_a(j).             \tag{40.8}
\]

**Finite H-stopping theorem.** For every `a>=2`, the first half-strength
complete-block stop is

\[
 \boxed{\tau(a)=1+\min\{m\ge a:\mathcal B_a(m)\ge0\},}             \tag{40.9}
\]

with `tau(a)=infinity` if the set is empty. Equivalently, a finite stop exists
if and only if

\[
 \sup_{m\ge a}\mathcal B_a(m)>0,
 \quad\hbox{or}\quad
 \sup_{m\ge a}\mathcal B_a(m)=0
 \text{ and the supremum is attained}.                            \tag{40.10}
\]

This is an exact reformulation, not a positivity theorem.

There is also a tail version matching the residual-budget theorem. Assume

\[
 \sum_{n\ge2}w_nP_n<\infty,
 \qquad T_a=\sum_{n=a}^\infty w_nP_n,
 \qquad Q_a=P_a-T_a.
\]

Then (40.3) gives

\[
 \mathcal B_a(m)=Q_a-Q_{m+1}.                                     \tag{40.11}
\]

Finite weighted energy implies `liminf Q_m=0`; consequently

\[
 \boxed{Q_a=\limsup_{m\to\infty}\mathcal B_a(m).}                 \tag{40.12}
\]

Therefore the following are equivalent:

1. every start `a>=2` has a finite half-strength complete-block stop;
2. for every `a`, `limsup_m mathcal B_a(m)>=0`, and whenever this limsup is
   zero, `mathcal B_a(m)=0` for some finite `m>=a`;
3. `Q_a>=0` for every `a`, and every zero of `Q` has a later zero.

Condition 2 is the stopping theorem entirely in signed-gap language; inserting
(40.8) makes it a theorem entirely about cumulative `mathcal H`. The attained
zero clause is essential: convergence of negative Abel averages to zero does
not produce a finite endpoint.

## 4. Scope

Equations (40.4) and (40.6) isolate the exact arithmetic target. They do not
show that the actual Mobius--fractional-part gaps or their cumulative Abel
averages have the required signs. A proof that condition 2 holds for the
physical vectors would recover the RH-sufficient renewal theorem, so no RH
result is claimed here.
