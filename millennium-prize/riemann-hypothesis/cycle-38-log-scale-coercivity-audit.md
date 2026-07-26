# Cycle 38: log-scale coercivity audit for complete endpoint paths

## 1. Exact path on one integer cell

Let `H` be the real Hilbert space in which the complete approximants live and
put

\[
 L_n=\log n,\qquad L_{n+1}=\log(n+1),\qquad
 h_n=L_n^{-1}-L_{n+1}^{-1}.
\]

On `L_n<=t<=L_(n+1)`, the exact complete interpolation is

\[
 F_{e^t}=U_n-{D_n\over t}
 =F_n+\left({1\over L_n}-{1\over t}\right)D_n.       \tag{38.1}
\]

Consequently

\[
 {d\over dt}F_{e^t}={D_n\over t^2},\qquad
 F_{n+1}-F_n=h_nD_n.                                  \tag{38.2}
\]

The exact `t=log X` path energy is

\[
 K_n:=\int_{L_n}^{L_{n+1}}
 \left\|{d\over dt}F_{e^t}\right\|^2dt
 ={\|D_n\|^2\over3}
 \left(L_n^{-3}-L_{n+1}^{-3}\right).                 \tag{38.3}
\]

Writing `delta_n=L_(n+1)-L_n`, this can also be compared with the least
energy of any path joining the same endpoints:

\[
 {K_n\over \|F_{n+1}-F_n\|^2/\delta_n}
 ={L_{n+1}^2+L_nL_{n+1}+L_n^2\over3L_nL_{n+1}}
 \geq1.                                                \tag{38.4}
\]

Thus the interpolation is asymptotically a constant-speed chord in logarithmic
scale. This gives an unsigned metric fact, not a dissipative sign.

The scale matching the block weight is instead

\[
 s=\log t=\log\log X.
\]

On one cell,

\[
 {dF\over ds}={D_n\over t},\qquad
 J_n:=\int_{\log L_n}^{\log L_{n+1}}
 \left\|{dF\over ds}\right\|^2ds
 ={\|D_n\|^2\over2}
 \left(L_n^{-2}-L_{n+1}^{-2}\right).                 \tag{38.5}
\]

Moreover, if `Delta s_n=log(L_(n+1)/L_n)`, then the exact RH weight is

\[
 w_n=h_nL_n=1-{L_n\over L_{n+1}}=1-e^{-\Delta s_n}
 \sim\Delta s_n.                                      \tag{38.6}
\]

Hence `sum w_nP_n` is the discrete counterpart of path mass
`int ||F(s)||^2 ds` on log-log scale. This identifies the natural functional-
analytic formulation, but does not establish its coercivity.

## 2. What Poincare and Hardy actually control

For an `H`-valued Sobolev path on a finite `t`-interval, Neumann Poincare gives

\[
 \int_A^B\|F-\overline F\|^2dt
 \leq{(B-A)^2\over\pi^2}\int_A^B\|F'\|^2dt.          \tag{38.7}
\]

It controls only the oscillatory component in scale. The constant scale mode
`overline F` is invisible. A Hardy inequality controls `F` itself only after a
boundary condition such as `F(A)=0` or `F(infinity)=0`, or after subtracting a
boundary value. No such condition is available for the complete approximants.
In particular, imposing `F(infinity)=0` would already insert the desired
Nyman--Beurling conclusion into the hypothesis.

There is a second, independent obstruction. Differentiating the squared norm
gives

\[
 P_n-P_{n+1}
 =-2h_n\langle F_n,D_n\rangle-h_n^2\|D_n\|^2
 =2h_nE_n.                                             \tag{38.8}
\]

Path energy sees only `||D_n||^2`. Dissipation also needs the orientation of
`D_n` relative to `F_n`. Cauchy--Schwarz yields only the two-sided estimate

\[
 |P(B)-P(A)|
 \leq2\left(\int_A^B\|F\|^2\right)^{1/2}
       \left(\int_A^B\|F'\|^2\right)^{1/2},           \tag{38.9}
\]

with compatible measures. It gives no favorable lower bound. Large path
energy may be tangential or outward, and therefore may produce zero or negative
endpoint dissipation.

## 3. Explicit counterexamples

### Constant-mode obstruction

Take any nonzero `v in H` and set, on every cell,

\[
 F_X=v,\qquad D_n=0,\qquad U_n=v.
\]

This has exactly the form (38.1). Every path energy vanishes while
`P_n=||v||^2>0`, so no inequality of the form

\[
 \sum_{a\leq n<b}w_nP_n
 \leq C\int_{\log\log a}^{\log\log b}\|F'(s)\|^2ds  \tag{38.10}
\]

can follow from complete endpoint interpolation alone. The failure is exactly
the uncontrolled constant mode in (38.7).

### Nonzero-energy, zero-dissipation obstruction

The failure is not repaired by excluding constant paths. Let `H=R^2`, let
`e_1,e_2` be its standard orthonormal basis, and for `n>=3` set

\[
 v_n=\begin{cases}e_1,&n\text{ even},\\e_2,&n\text{ odd},\end{cases}
 \qquad
 D_n={v_{n+1}-v_n\over h_n},
 \qquad U_n=v_n+{D_n\over L_n}.                        \tag{38.11}
\]

Define `F_(e^t)=U_n-D_n/t` on the `n`th cell. Then

\[
 F_n=v_n,\qquad F_{n+1}=v_{n+1},\qquad P_n=1,         \tag{38.12}
\]

and adjacent cell definitions agree at every endpoint. Nevertheless,

\[
 P_a-P_b=0                                             \tag{38.13}
\]

for every pair of integer endpoints, whereas every cell has strictly positive
path energy

\[
 K_n={2\over3h_n^2}
 \left(L_n^{-3}-L_{n+1}^{-3}\right)>0.                \tag{38.14}
\]

Also, for every nonempty block,

\[
 \sum_{a\leq n<b}w_nP_n=\sum_{a\leq n<b}w_n>0,
\]

and this mass diverges over the tail. Thus neither positive nor arbitrarily
large endpoint path energy implies the required block inequality

\[
 P_a-P_b\geq2\kappa\sum_{a\leq n<b}w_nP_n.
\]

This counterexample obeys the exact reciprocal-log interpolation and endpoint
continuity. It violates only the arithmetic relation tying `D_n` to the Mobius
coefficients. Therefore it rules out a generic Hilbert-space Hardy/Poincare
route, not a genuinely Mobius-specific correlation theorem.

## 4. Route verdict

The complete interpolation supplies useful exact kinematics:

1. `log log X` is the scale whose measure matches the divergent weight
   `w_n`.
2. Path energy controls scale oscillation and endpoint distance.
3. It does not control the constant scale mode or the radial orientation of an
   endpoint increment.

Any successful coercive inequality must therefore add arithmetic information
that forces the compensated alignment

\[
 -\langle F_n,D_n\rangle-{h_n\over2}\|D_n\|^2
\]

to dominate weighted `P_n` on complete chained blocks. That is precisely the
existing `E_n` block target in another language. A scale-only Hardy or Poincare
argument cannot supply it. The generic functional-analytic route is closed;
the remaining route must exploit the actual Mobius coefficient path, or a new
boundary/orthogonality condition proved from that arithmetic rather than
assumed.
