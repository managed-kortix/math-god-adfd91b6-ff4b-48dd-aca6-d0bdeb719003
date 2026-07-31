# Cycle 177: invariant cubic-flux many-edge baseline

Raw bilinear output is not energy flux. Once the receiver is included, the
correct algebraic relaxation is a three-uniform geometric program. It gives an
exact constrained AM--GM baseline, including every saving caused by shared
modes. A useful many-edge theorem must exceed this baseline through a genuine
polarization, phase, collision, or dynamical incompatibility.

## Physical orbit flux

Let `V` be a finite set of nonzero real frequency orbits `[j]={j,-j}` and put

\[
 x_{[j]}=2|j|\,|u_j|^2,
 \qquad E_c(u)=\sum_{v\in V}x_v.
\]

For an oriented triad `e=([p],[q]\to[k])`, with representatives `p+q=k`,
define the receiver flux magnitude

\[
 \Phi_e(u)=2\left|\operatorname{Re}\left(
 \overline{u_k}\mathbin\cdot[-iP_k\big((u_p\mathbin\cdot q)u_q
 +(u_q\mathbin\cdot p)u_p\big)]\right)\right|.       \tag{1}
\]

The factor two combines the conjugate output. It does not count `[k]` twice.
Replacing the absolute value by a prescribed sign gives a directed transfer
constraint and only strengthens the conclusions below. Formula (1) is
independent of polarization coordinates and translation phase, is quadratic
in the two senders and linear in the receiver, and coherently sums the two
ordered interactions. If several input pairs hit the same receiver and the
hypothesis concerns total receiver flux, their vectors must first be summed in
(1); they cannot be declared separate edges afterward.

Let `gamma_e` be any valid orbit-level trilinear bound

\[
 \Phi_e(u)\le\gamma_e(x_px_qx_k)^{1/2}.              \tag{2}
\]

The sharp choice is the norm of the Leray trilinear tensor between the three
divergence-free planes with the displayed critical weights. Set
`d_e=gamma_e^{-2}`. Unit flux forces

\[
 x_px_qx_k\ge d_e.                                  \tag{3}
\]

Under the frequency dilation `(p,q,k)\mapsto N(p,q,k)`, (1) scales by `N`
at fixed Fourier amplitudes, each `x_v` scales by `N`, `gamma_e` scales by
`N^{-1/2}`, and `d_e` scales by `N`. If all edge data are dilated together,
the optimized baseline scales by `N^{1/3}`, as cubic homogeneity requires.
Thus (2)--(3) do not hide the raw-output normalization error from Cycle 175.

## Exact constrained AM--GM theorem

Let `H=(V,\mathcal E)` be the three-uniform incidence hypergraph of designated
physical triads, including all shared sender and receiver modes. Define

\[
 C_{\rm AM}(H,d)=\inf\left\{\sum_{v\in V}x_v:
 x_v>0,\ \prod_{v\in e}x_v\ge d_e\quad(e\in\mathcal E)\right\}.       \tag{4}
\]

For nonnegative multipliers `lambda_e`, not all zero, put

\[
 a_v=\sum_{e\ni v}\lambda_e,
 \qquad A=\sum_va_v=3\sum_e\lambda_e.
\]

Then

\[
 \boxed{
 C_{\rm AM}(H,d)=
 \sup_{\lambda\ge0}
 A\left(
 {\prod_e d_e^{\lambda_e}\over\prod_v a_v^{a_v}}
 \right)^{1/A}}
                                                               \tag{5}
\]

with `0^0=1`. Consequently every field satisfying `Phi_e>=1` obeys

\[
 E_c(u)\ge C_{\rm AM}(H,d).                           \tag{6}
\]

To prove the lower bound in (5), multiply (3) to the powers `lambda_e` and
apply weighted AM--GM to `sum_v x_v` with weights `a_v/A`. Equality in (5)
follows by writing `x_v=e^{y_v}`: (4) is a convex program with linear
constraints in `y`, and its Lagrange dual is precisely the optimized weighted
AM--GM expression. Isolated vertices are omitted. For one edge (5) is the
familiar `3d_e^{1/3}`; for disjoint edges it is the sum of these one-edge
costs. For shared modes it is generally much smaller, and summing one-edge
AM--GM inequalities is invalid because it repeatedly charges the same energy.

Define the invariant physical minimum and its excess by

\[
 C_{\rm phys}=\inf\{E_c(u):\Phi_e(u)\ge1\ \hbox{for every }e\},
 \qquad \Delta_H=C_{\rm phys}-C_{\rm AM}(H,d)\ge0.     \tag{7}
\]

Here the infimum includes phases, polarizations, coherent collisions, reality,
and every reciprocal-amplitude symmetry. A substantive many-edge result must
prove `Delta_H` grows, or prove an invariant off-circuit or time-integrated
charge at near-minimizers. Growth of `C_AM` alone is compulsory normalization
cost, not cascade depletion.

## Shared-pump hostile test and stability excess

Consider `L` edges `e_i={P,R_i,K_i}` sharing only the pump `P`. Write
`d_i=d_{e_i}` and

\[
 D=\sum_{i=1}^L\sqrt{d_i}.
\]

For fixed pump energy `x_P=P`, each constraint gives
`x_{R_i}x_{K_i}>=d_i/P`. Therefore

\[
 \boxed{C_{\rm AM}=\min_{P>0}\left(P+{2D\over\sqrt P}\right)
 =3D^{2/3}.}                                           \tag{8}
\]

For equal `d_i=d`, this is `3L^{2/3}d^{1/3}`, not the false decoupled value
`3Ld^{1/3}`. Moreover every feasible scalar profile has the quantitative
excess bound

\[
 \begin{aligned}
 E_c-3D^{2/3}
 &\ge D^{2/3}{(t-1)^2(t+2)\over t}
   +\sum_i(\sqrt{x_{R_i}}-\sqrt{x_{K_i}})^2,\\
 t&={\sqrt P\over D^{1/3}}.                            \tag{9}
 \end{aligned}
\]

This follows from
`x_R+x_K=2sqrt(x_R x_K)+(sqrt(x_R)-sqrt(x_K))^2` and
`t^2+2/t-3=(t-1)^2(t+2)/t`. Thus pump imbalance or sender/receiver imbalance
does produce an excess. But the bound is sharp: take

\[
 P=D^{2/3},\qquad x_{R_i}=x_{K_i}=\sqrt{d_i/P}.         \tag{10}
\]

An actual Leray realization uses a common pump
`p=(N,0,0), u_p\parallel e_2`, rails with `|Y_i|>=N`,
`q_i=(0,Y_i,0), u_{q_i}\parallel e_3`, and receivers
`k_i=(N,Y_i,0), u_{k_i}\parallel e_3`. The symmetrized symbol is
`Y_i e_3`. Decomposing arbitrary sender polarizations into the in-plane and
`e_3` directions shows that the critical trilinear norm is attained by these
polarizations when `|Y_i|>=N`, and (1) gives

\[
 \gamma_i={|Y_i|\over\sqrt{2|p||q_i||k_i|}},
 \qquad d_i={2|p||q_i||k_i|\over Y_i^2}.               \tag{11}
\]

Choose real positive pump and rail coefficients and receiver coefficients with
relative phase `i`; reality fixes the negative modes. Choosing their magnitudes
from (10) attains unit designated cubic flux on every triad and equality in
(8). Hence shared use of one physical pump does not by
itself force positive excess. Constraints on coherently summed total flux can
only be inferred after all other pairs at each receiver are included; the
star test establishes no closed Euler subsystem or dynamical cascade.

Reproduce the symbol, unit-flux normalization, dual value, and equality case
with

```sh
python3 millennium-prize/navier-stokes/verify_cycle177_cubic_flux_baseline.py
```

This is an invariant proof architecture and a hostile normalization test, not
a Navier--Stokes regularity theorem.
