# Cycle 53: the old-`D` reserve and probe hierarchy

## Corrected reserve identity

Fix `M<B<=M+12`, put `L=log M`, and use the incoming convention

\[
U=U_{M-1},\qquad D=D_{M-1},\qquad
F_M=U-{D\over L}.
\]

Let

\[
Z=\operatorname{span}\{U,\rho_M,\ldots,\rho_{B-1}\},
\qquad Q_Z=I-\Pi_Z.
\]

The weighted new packet `bar T` lies in `Z`, so the Cycle 52 omitted square is
entirely old-state:

\[
\boxed{
A\|Q_Z(D+\bar T)\|^2=A\|Q_ZD\|^2
=A(\log M)^2\|Q_ZF_M\|^2,}                       \tag{53.1}
\]

where `A=sum_[M,B) beta_n`. This is the exact source of the recovery missed by
the local projection.

If `Gamma` is the restricted Gram matrix of the probes and
`b_D=(<D,z>)_(z in Z)`, then

\[
\boxed{
\|Q_ZD\|^2=\|D\|^2-b_D^*\Gamma^+b_D.}           \tag{53.2}
\]

Equivalently, opening the old squarefree coefficient vector `d_a=mu(a)log a`,
this is the generalized Schur contraction

\[
d^*(G^- -K^*\Gamma^+K)d.                         \tag{53.3}
\]

The matrix is positive semidefinite, but positivity supplies no nonzero lower
bound. The reserve depends on the complete old/new restricted Vasyunin
correlations.

## Exact projection telescope

For fixed `M`, define

\[
Z_q=\operatorname{span}\{U,\rho_M,\ldots,\rho_{q-1}\},
\quad r_q=(I-\Pi_{Z_q})D,
\quad s_q=(I-\Pi_{Z_q})\rho_q.
\]

Whenever `s_q!=0`, adjoining one row gives

\[
r_{q+1}=r_q-{\langle r_q,s_q\rangle\over\|s_q\|^2}s_q,
\]

and

\[
\boxed{
\|r_{q+1}\|^2=\|r_q\|^2
-{|\langle r_q,s_q\rangle|^2\over\|s_q\|^2}.}   \tag{53.4}
\]

Thus the reserve has a finite Pythagorean telescope. It is not an arithmetic
telescope: every residualized row depends on the entire preceding Gram system,
and sliding the left endpoint changes all normal equations.

The equivalent endpoint formulation requires a coefficient correction. If

\[
\Pi_ZF_M=\lambda_0U+\sum_j\lambda_{j+1}\rho_{M+j},
\]

then

\[
\Pi_Z(D+\bar T)=L(1-\lambda_0)U
+\sum_j(t_j-L\lambda_{j+1})\rho_{M+j}.            \tag{53.5}
\]

The `U` coefficient is `L(1-lambda_0)`, not `-L lambda_0`.

## Finite older-probe phenomenon

At 256-bit Arb precision, adjoining the single old probe `D_(M-2)` to the
Cycle 52 span gives a positive projection lower bound at every one of the eleven
historically delayed first-success windows. The weakest is `[222,226)` with
lower bound `2.4814980673e-6`; `[219,231)` is certified at
`3.4816972890e-6` against the exact surplus `4.4763896498e-6`.

This statement needs a crucial audit. Since

\[
D_{M-1}=D_{M-2}+\mu(M-1)\log(M-1)\rho_{M-1},
\]

the probe is exactly tautological when `mu(M-1)=0`. This occurs for four of the
eleven starts: `99,100,221,226`. The other seven certificates are nontrivial
finite inequalities, but `D_(M-2)` still imports essentially the entire global
old state. They do not establish a uniform hierarchy theorem.

The nested Schur gain from adjoining any residualized probe `z_perp` is exactly

\[
\boxed{
A{|\langle D+\bar T,z_\perp\rangle|^2\over\|z_\perp\|^2}.} \tag{53.6}
\]

Every fixed incomplete hierarchy is generically defeatable by placing the
unseen old-`D` component orthogonally to its probes. Including `D_(M-1)` makes
the formula exact and tautological.

## Quantitative finite audit and generic no-go

On all eleven delayed windows, the amount of old-`D` reserve needed to repair
the failed local projection is positive and much larger than the final surplus.
For `[219,231)`, the needed payment is
`0.00080094034174...`, about `178.9` times the surviving budget. Across the
eleven windows, the ratio of needed payment to the negative `U` packet lies
between `0.4319...` and `0.7698...`; this is finite evidence only.

Exact rational Hilbert models preserving a twelve-step nested Möbius pattern,
zero nonsquarefree updates, `Delta D=L Delta U`, positive Gram geometry, and
negative per-cell `U` cost can make the reserve/LocalBudget ratio arbitrarily
small or arbitrarily large. Hence nested kinematics, local Möbius symbols, and
Gram positivity cannot control (53.1). The indispensable input is the fixed
fractional-part/Vasyunin coupling of the entire old prefix to the new rows.

The active target is therefore an arithmetic upper bound on the Schur capture
in (53.2), or a direct comparison of the terminal residual with `N_U-V_D`.
No additive-12 theorem or RH result is claimed.
