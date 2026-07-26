# Cycle 39: half-strength adaptive blocks and the exact tail budget

## 1. Half-strength algebra

Put

\[
 L_n=\log n,\qquad h_n={1\over L_n}-{1\over L_{n+1}},\qquad
 w_n=h_nL_n=1-{L_n\over L_{n+1}},
\]

and let `P_n>=0`. At `kappa=1/2`, the complete-block inequality is

\[
 P_a-P_b\geq\sum_{n=a}^{b-1}w_nP_n.                 \tag{39.1}
\]

Define the logarithmically normalized energy

\[
 A_n=L_nP_n.
\]

Discrete summation by parts gives the exact identity

\[
 \boxed{P_a-P_b-\sum_{n=a}^{b-1}w_nP_n
 =\sum_{n=a}^{b-1}{A_n-A_{n+1}\over L_{n+1}}.}      \tag{39.2}
\]

Indeed, the summand on the right is

\[
 {L_nP_n-L_{n+1}P_{n+1}\over L_{n+1}}
 ={L_n\over L_{n+1}}P_n-P_{n+1},
\]

and summing leaves `P_a-P_b-sum (1-L_n/L_(n+1))P_n`.
Consequently (39.1) is exactly

\[
 \boxed{\sum_{n=a}^{b-1}{A_n-A_{n+1}\over L_{n+1}}\geq0.} \tag{39.3}
\]

This is the special algebra at `kappa=1/2`. It is not ordinary endpoint
monotonicity of `A_n`, because the differences have changing positive weights.
For a singleton block it does reduce to

\[
 P_n-P_{n+1}\geq w_nP_n
 \quad\Longleftrightarrow\quad A_{n+1}\leq A_n.      \tag{39.4}
\]

Thus adaptive longer blocks can compensate upward steps of `A_n`, but only
through the weighted signed variation in (39.3).

## 2. Tail budget and exact characterization

When the weighted tail is finite, set

\[
 T_a=\sum_{n=a}^{\infty}w_nP_n,\qquad
 \boxed{Q_a=P_a-T_a.}                                \tag{39.5}
\]

The half-strength normalization yields the local identity

\[
 \boxed{Q_a-Q_{a+1}
 ={L_a\over L_{a+1}}P_a-P_{a+1}
 ={A_a-A_{a+1}\over L_{a+1}}.}                       \tag{39.6}
\]

Therefore, for every finite `b>a`,

\[
 \boxed{Q_a-Q_b
 =P_a-P_b-\sum_{n=a}^{b-1}w_nP_n.}                 \tag{39.7}
\]

The block condition is precisely `Q_b<=Q_a`: an adaptive endpoint is a later
non-increase of the residual tail budget. Since `sum w_n=infinity`, finiteness
of `sum w_nP_n` implies `liminf P_n=0`. Also `T_n->0`, `Q_n>=-T_n`, and along a
subsequence with `P_n->0` one has `Q_n->0`; hence

\[
 \liminf_{n\to\infty}Q_n=0.                           \tag{39.8}
\]

The general tail-Hardy characterization at `c=2 kappa=1` now says that a
finite block endpoint exists from every start if and only if

1. `sum_n w_nP_n<infinity`;
2. `Q_a>=0`, equivalently `P_a>=T_a`, for every `a`;
3. every zero of `Q` has a later zero, with no condition when the zero set is
   empty.

If `Q_a>0`, (39.8) produces a later `b` with `Q_b<Q_a`. If `Q_a=0`, a block is
possible exactly when a later zero occurs. This also shows that the strict tail
inequalities `P_a>T_a` automatically give all finite stopping times.

## 3. Integral and Gram forms

For the exact RH lane, write `P_n=||F_n||_H^2` in
`H=L^2((0,1),dx)`. Whenever `T_a<infinity`, Tonelli gives

\[
 \boxed{Q_a=\int_0^1\left(F_a(x)^2-
 \sum_{n=a}^{\infty}w_nF_n(x)^2\right)dx.}            \tag{39.9}
\]

This is an exact integral representation, but its integrand has no fixed sign.
If `u_n` is the augmented coefficient vector of `F_n` and `G` is the fixed
fractional-part Gram matrix, then at a finite cutoff `B` equivalently

\[
 P_a-\sum_{n=a}^{B}w_nP_n=\left\langle G,
 u_au_a^T-\sum_{n=a}^{B}w_nu_nu_n^T\right\rangle.     \tag{39.10}
\]

The coefficient kernel is one positive rank-one term minus a positive scale
kernel. It has explicit negative directions and is not positive semidefinite.
Moreover, because `sum w_n=infinity`, its constant coefficient entries diverge
as `B` tends to infinity. Thus (39.9) has a valid limit under finite tail
energy, but one may not take the infinite coefficient matrix entry by entry.
On the balanced finite-support domain the limiting coefficient quadratic form
exists, yet explicit two-coordinate squarefree vectors still make it strictly
negative. This rules out a generic coefficient-space PSD argument without
ruling out favorable contraction with the specific physical Gram matrix.

There is also a normalized path interpretation. Set

\[
 V_n=\sqrt{L_n}\,F_n,
 \qquad ||V_n||^2=A_n.
\]

Then the exact block residual is

\[
 \boxed{\sum_{n=a}^{b-1}{
 \langle V_n-V_{n+1},V_n+V_{n+1}\rangle\over L_{n+1}}.} \tag{39.11}
\]

This makes the obstruction explicit: the estimate needs favorable radial
orientation of normalized endpoint motion. Hilbert-space or Gram positivity
alone controls neither sign in (39.11).

For the actual reciprocal-log Mobius coefficient path there is a further exact
one-step cancellation. With

\[
 U_n=1+\sum_{q\le n}\mu(q)\phi_q,
 \qquad D_n=\sum_{q\le n}\mu(q)(\log q)\phi_q,
\]

one has `F_n=U_n-D_n/L_n` and `F_(n+1)=U_n-D_n/L_(n+1)`. Hence

\[
 \boxed{A_{n+1}-A_n=(L_{n+1}-L_n)
 \left(\|U_n\|^2-{\|D_n\|^2\over L_nL_{n+1}}\right).} \tag{39.12}
\]

The mixed inner product cancels exactly. Therefore the singleton inequality at
half strength is also exactly

\[
 \boxed{\|D_n\|^2\ge L_nL_{n+1}\|U_n\|^2.}            \tag{39.13}
\]

This is a genuinely special normalization identity, but it is a comparison of
two positive norms, not an automatic inequality.

## 4. The special normalization identity

The profile

\[
 \boxed{P_n={C\over\log n}\quad(C>=0)}                \tag{39.14}
\]

lies exactly on the half-strength boundary. Indeed,

\[
 w_nP_n=C\left({1\over L_n}-{1\over L_{n+1}}\right),
\]

so

\[
 T_a={C\over L_a}=P_a,\qquad Q_a=0,                  \tag{39.15}
\]

and every finite block satisfies (39.1) with equality. Equivalently, `A_n=C`
is constant. Conversely, equality in every singleton block forces
`A_(n+1)=A_n`, so (39.12) is the unique nonnegative profile, up to its constant,
with equality at every step. Likewise, `Q_a=0` at every index forces the same
recursion.

Thus `kappa=1/2` is algebraically distinguished: its critical equality profile
is exactly reciprocal logarithmic decay, and the residual budget increments
are exactly weighted differences of `L_nP_n`. This identity does not assert
that the actual Mobius energies follow the critical profile.

## 5. Universal claims: falsifications and surviving statement

No universal positivity follows from the normalization.

* Taking `P_n=1` gives infinite weighted energy and no favorable block, since
  every endpoint decrement is zero while every block cost is positive.
* Even finite weighted energy does not imply `Q_a>=0`. Fix `a`, take `P_a=1`,
  `P_(a+1)=M`, and all later terms zero. Then
  \[
  Q_a={L_a\over L_{a+1}}-w_{a+1}M<0
  \]
  for sufficiently large `M`.
* The normalized Gram expression is not universally positive. In an arbitrary
  Hilbert space one may take `F_n=sqrt(P_n)e` for a fixed unit vector `e`; the
  preceding scalar counterexamples are already Gram counterexamples.
* Monotonicity of `A_n=L_nP_n` is sufficient for every block, by (39.2), but is
  not necessary for adaptive blocks. For example, prescribe
  `A_a=1`, `A_(a+1)=2`, and `A_(a+2)=0`. Then `A` first increases, but the
  residual on `[a,a+2)` is
  \[
  -{1\over L_{a+1}}+{2\over L_{a+2}}>0,
  \]
  since `a+2<(a+1)^2`. A later weighted decrease compensates the increase.

What survives universally is only the exact equivalence: at half strength,
adaptive complete blocks are later non-increases of `Q`, or equivalently
nonnegative weighted signed variation of `L_nP_n`. For the specific finite
Mobius--fractional-part energies, proving `Q_a>=0` for every sufficiently large
`a` (plus recurrence at equality) remains an RH-sufficient arithmetic theorem.
The algebra, integral form, and critical profile neither prove nor falsify that
Mobius-specific assertion.
