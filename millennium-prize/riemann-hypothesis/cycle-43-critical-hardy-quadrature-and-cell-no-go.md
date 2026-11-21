# Cycle 43: critical Hardy quadrature and exact cell no-go results

## Scope

This note sharpens the active logarithmic Nyman--Beurling renewal route.  It
contains exact scalar identities and abstract counterexamples, not a sign
estimate for the physical Möbius--Vasyunin sequence.  In particular it proves
no instance of the Riemann hypothesis.

Throughout, for `n>=2`, put

\[
 L_n=\log n,\qquad x_n=L_n^{-1},\qquad
 h_n=x_n-x_{n+1},\qquad w_n=L_nh_n=1-{L_n\over L_{n+1}}.
\]

Let `P_n>=0` satisfy

\[
 \sum_{n\ge2}w_nP_n<\infty,
\]

and set

\[
 A_n=L_nP_n={P_n\over x_n},\qquad
 T_a=\sum_{n\ge a}w_nP_n.
\]

Thus every scale tail below converges.  The finite-block identities use no
infinite tail in the scale index `n`; the established absolutely convergent
unit-cell decompositions in the index `k` are still understood.

## 1. The critical residual is an exact future Hardy average

Since `w_nP_n=h_nA_n` and `sum_(n>=a)h_n=x_a`, the numbers

\[
 \pi_{a,n}={h_n\over x_a}=L_ah_n\qquad(n\ge a)
\]

form a probability distribution.  Therefore, for `c=2 kappa`,

\[
 \boxed{P_a-cT_a=x_a\left(A_a-c\sum_{n\ge a}\pi_{a,n}A_n\right).}
 \tag{43.1}
\]

At the critical value `kappa=1/2`, this is

\[
 \boxed{P_a-T_a=x_a(A_a-\mathbb E_{\pi_a}A).}
 \tag{43.2}
\]

Thus critical tail-budget positivity is a nonlocal superharmonicity condition
for the scaled energy `A_n=L_nP_n`.

Fix a constant `C` and define the effective second coefficient

\[
 \Delta_n={P_n-Cx_n\over x_n^2}=L_n^2P_n-CL_n.
 \tag{43.3}
\]

The elementary identity

\[
 2h_nx_n=x_n^2-x_{n+1}^2+h_n^2
\]

gives

\[
 \sum_{n\ge a}h_nx_n={1\over2}\left(x_a^2+\sum_{n\ge a}h_n^2\right).
 \tag{43.4}
\]

Define

\[
 \nu_{a,n}={h_nx_n\over x_a^2},\qquad
 \theta_a=\sum_{n\ge a}\nu_{a,n}
 ={1\over2}\left(1+{\sum_{n\ge a}h_n^2\over x_a^2}\right).
 \tag{43.5}
\]

Because `x_n` is decreasing and convex, `h_n` decreases, and hence

\[
 0<{\sum_{n\ge a}h_n^2\over x_a^2}
 \le {h_a\over x_a}=w_a\longrightarrow0.
 \tag{43.6}
\]

Substitution of `P_n=Cx_n+x_n^2Delta_n` into (43.1) proves the exact
quadrature formula

\[
 \boxed{
 P_a-cT_a=(1-c)Cx_a+x_a^2\left(
 \Delta_a-c\sum_{n\ge a}\nu_{a,n}\Delta_n\right).}
 \tag{43.7}
\]

In particular,

\[
 \boxed{P_a-T_a=x_a^2\left(
 \Delta_a-\sum_{n\ge a}\nu_{a,n}\Delta_n\right).}
 \tag{43.8}
\]

The future operator in (43.8) has total mass `theta_a -> 1/2`, not one.
This is the exact origin of the formal `D/(2 log^2 a)` critical reserve.

### Exact two-term consequence

Suppose

\[
 P_n=Cx_n+(D+r_n)x_n^2,\qquad r_n\to0.
 \tag{43.9}
\]

Then

\[
 \boxed{\begin{aligned}
 P_a-cT_a={}&(1-c)Cx_a\\
 &+D\left[\left(1-{c\over2}\right)x_a^2
 -{c\over2}\sum_{n\ge a}h_n^2\right]\\
 &+r_ax_a^2-c\sum_{n\ge a}h_nx_nr_n .
 \end{aligned}}
 \tag{43.10}
\]

For `c=2 kappa>=0`, if `epsilon_a=sup_(n>=a)|r_n|`, the last line has
absolute value at most `(1+c)epsilon_a x_a^2`.  Hence, at `c=1`,

\[
 P_a-T_a=\left({D\over2}+o(1)\right){1\over\log^2a}.
 \tag{43.11}
\]

For the exact profile `P_n=Cx_n+Dx_n^2`, there is no error:

\[
 \boxed{P_a-T_a
 ={D\over2}\left(x_a^2-\sum_{n\ge a}h_n^2\right)
 =D\sum_{n\ge a}h_nx_{n+1}.}
 \tag{43.12}
\]

Its sign is exactly the sign of `D` for every start.

## 2. Exact bridge to the complete Möbius--Chebyshev packets

For the physical sequence, retain the notation of Cycles 40--41:

\[
 \beta_n={h_n\over L_{n+1}}=h_nx_{n+1},\qquad
 H_n=\|D_n\|^2-L_nL_{n+1}\|U_n\|^2.
\]

The established singleton identity is

\[
 P_n-P_{n+1}-w_nP_n=\beta_nH_n.
 \tag{43.13}
\]

Since `1-w_n=x_(n+1)/x_n`, its left side is also

\[
 x_{n+1}(A_n-A_{n+1}).
\]

Using `A_n=C+x_nDelta_n` gives the exact coefficient bridge

\[
 \boxed{H_n={x_n\Delta_n-x_{n+1}\Delta_{n+1}\over h_n}.}
 \tag{43.14}
\]

Let `mathcal D_(n,k),mathcal U_(n,k)` be the complete nonnegative cell packets
of Cycle 41.  Then

\[
 \boxed{\sum_{k\ge1}
 (\beta_n\mathcal D_{n,k}-w_n\mathcal U_{n,k})
 =x_{n+1}(x_n\Delta_n-x_{n+1}\Delta_{n+1}).}
 \tag{43.15}
\]

Only on `1<=k<=n` may one substitute
`u_(n,k)=0, v_(n,k)=psi(k)`.  On those cells the summand is

\[
 \beta_n[(\ell_n+\lambda_k\psi(k))^2+q_k\psi(k)^2]-w_nm_n^2.
 \tag{43.16}
\]

The complete tail `k>n` still requires the divisor-floor formula.  Thus
positivity of the complete fixed-`n` compensated packet sum is exactly

\[
 x_n\Delta_n\ge x_{n+1}\Delta_{n+1}.
 \tag{43.17}
\]

If (43.17) holds for every `n>=a`, then the successive critical residuals are
nonnegative.  Under finite weighted energy this implies the nonlocal budget
inequality (43.8) at `a`.  It does not assert termwise positivity of every
individual `k`-cell.

For a finite block `a<b`, summing (43.15) gives

\[
 \boxed{\begin{aligned}
 &\sum_{n=a}^{b-1}\sum_{k\ge1}
 (\beta_n\mathcal D_{n,k}-w_n\mathcal U_{n,k})\\
 &\qquad=x_a^2\Delta_a-x_b^2\Delta_b
 -\sum_{n=a}^{b-1}h_nx_n\Delta_n.
 \end{aligned}}
 \tag{43.18}
\]

This is finite algebra, with no tail assumption.

## 3. Bounded second-scale control does not imply critical budgets

Define

\[
 \boxed{P_n=x_n+{(-1)^n\over2}x_n^2.}
 \tag{43.19}
\]

This is positive for all `n>=2`, tends to zero, and has finite weighted energy.
Its effective coefficient is `Delta_n=(-1)^n/2`.  Put `t_n=h_nx_n`; this is
strictly decreasing.  The alternating-series theorem gives

\[
 0<(-1)^a\sum_{n\ge a}(-1)^nt_n<t_a.
 \tag{43.20}
\]

Consequently, for `Q_a=P_a-T_a`,

\[
 \boxed{2(-1)^aQ_a>x_a^2-t_a=x_ax_{a+1}>0.}
 \tag{43.21}
\]

So `sgn(Q_a)=(-1)^a`.  To compare different odd starts, observe that

\[
 Q_n-Q_{n+1}=(-1)^n\gamma_n,\qquad
 \gamma_n={1\over2}x_{n+1}(x_n+x_{n+1}).
\]

The positive sequence `gamma_n` strictly decreases.  Hence, for odd `n`,

\[
 Q_{n+2}-Q_n=\gamma_n-\gamma_{n+1}>0.
\]

Every later odd residual therefore exceeds `Q_n`, while every even residual is
positive.  No critical renewal can start at an odd `a>=3`: for every `b>a`,

\[
 P_a-P_b-\sum_{n=a}^{b-1}w_nP_n=Q_a-Q_b<0.
 \tag{43.22}
\]

Therefore positivity, convergence to zero, finite weighted energy, and even

\[
 \left|P_n-{1\over\log n}\right|={1\over2\log^2n}
\]

do not imply critical tail-budget positivity.  This is an abstract scalar
counterexample, not a counterexample to the physical sequence.

## 4. Positive critical budgets do not imply abstract singleton positivity

Define

\[
 \boxed{P_n=x_n+\left(1+{(-1)^n\over n}\right)x_n^2.}
 \tag{43.23}
\]

Here `Delta_n=1+r_n`, where `r_n=(-1)^n/n`.  The sequence is positive,
tends to zero, and has finite weighted energy because

\[
 0<P_n\le x_n+{3\over2}x_n^2.
\]

From (43.5), `theta_a<=(1+w_a)/2`, while `w_a<1/a`.  Also

\[
 \left|r_a-\sum_{n\ge a}\nu_{a,n}r_n\right|<{2\over a}.
\]

Therefore

\[
 \boxed{Q_a>{a-5\over2a}x_a^2>0\qquad(a\ge6).}
 \tag{43.24}
\]

Moreover `|Delta_n|<=3/2` and `theta_b<1`, so (43.8) gives
`|Q_b|<3x_b^2->0`.  Thus every start `a>=6` has some finite critical renewal:
eventually `Q_b<Q_a`.

For an arbitrary scalar profile define the formal singleton defect

\[
 \widetilde H_n={A_n-A_{n+1}\over h_n}
 ={x_n\Delta_n-x_{n+1}\Delta_{n+1}\over h_n}.
\]

It satisfies the scalar identity

\[
 P_n-P_{n+1}-w_nP_n=\beta_n\widetilde H_n.
\]

For (43.23), direct substitution gives

\[
 \widetilde H_n=1+(-1)^n{x_n/n+x_{n+1}/(n+1)\over h_n}.
 \tag{43.25}
\]

Since `w_n<1/n`, one has `h_n=x_nw_n<x_n/n`; hence

\[
 \boxed{\widetilde H_n<0\quad\hbox{for every odd }n\ge3.}
 \tag{43.26}
\]

So a positive convergent second coefficient controls the nonlocal budgets but
need not imply eventual positivity of the abstract scalar singleton residual.
This scalar profile is not asserted to arise from the physical
Möbius--Vasyunin vectors or their cell packets.  To deduce
`widetilde H_n->D` from `Delta_n=D+r_n`, the exact necessary and sufficient
condition is the stronger difference regularity

\[
 x_nr_n-x_{n+1}r_{n+1}=o(h_n),
 \tag{43.27}
\]

not merely `r_n->0`.

## 5. Strategic consequence

The exact next target should not be eventual singleton positivity.  The
critical tail-budget inequality is instead the killed-Hardy estimate

\[
 \boxed{\Delta_a\ge\sum_{n\ge a}{h_nx_n\over x_a^2}\Delta_n,}
 \tag{43.28}
\]

or a finite chained block version of (43.18), proved using the complete
Möbius--Vasyunin/divisor-floor structure.  For finite renewal from every start,
non-strict (43.28) must be supplemented by the established equality-boundary
condition: every zero `Q_a=0` must have a later zero, unless strict positivity
is proved instead.  Boundedness of the effective coefficient alone is
insufficient to force critical budget positivity by Section 3, although it
still yields useful size control.  A one-sided arithmetic Hardy estimate or a
controlled positive limiting second coefficient are examples of sufficient
additional information.  Any unconditional physical estimate strong enough
to force a zero liminf remains RH-sufficient and must be audited as such.
