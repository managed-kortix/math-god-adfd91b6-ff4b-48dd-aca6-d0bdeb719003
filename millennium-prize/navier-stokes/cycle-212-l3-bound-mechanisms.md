# Cycle 212: mechanisms for and against the universal `L^3` factor

## Frozen question

Let `u` be a smooth mean-zero periodic solution of

\[
 \partial_tu+u\mathbin\cdot\nabla u+\nabla p=\nu\Delta u,
 \qquad \nabla\mathbin\cdot u=0.                         \tag{212.1}
\]

Cycle 210 asks whether every such three-dimensional solution satisfies

\[
 \sup_{t<T_*}\|u(t)\|_3\leq 2\|u(0)\|_3.              \tag{212.2}
\]

The same estimate for embedded two-dimensional solutions is a necessary
special case. This note tests three standard routes. None proves (212.2), and
none supplies a counterexample, but the tests sharply separate a finite-time
theorem from the global claim.

## Exact velocity identity

Put

\[
 F(t)=\int_{\mathbb T^d}|u|^3,
 \qquad
 D(t)=\int_{\mathbb T^d}|u|
   \bigl(|\nabla u|^2+|\nabla|u||^2\bigr).
\]

Multiplication of (212.1) by `|u|u` gives

\[
 {1\over3}F'(t)+\nu D(t)
   =I(t):=\int_{\mathbb T^d}p\,u\mathbin\cdot\nabla|u|. \tag{212.3}
\]

Transport cancels, but pressure has no sign. If `C_CZ(5/2)` denotes the
periodic Calderon--Zygmund constant in
`||p||_(5/2)<=C_CZ(5/2)||u||_5^2`, then

\[
\begin{split}
 |I|
 &\leq \|p\|_{5/2}\|u\nabla|u|\|_{5/3}\\
 &\leq C_{CZ}(5/2)D^{1/2}
       \left(\int|u|^5\right)^{1/2}.
\end{split}                                                   \tag{212.4}
\]

Consequently

\[
 {1\over3}F'+{\nu\over2}D
 \leq {C_{CZ}(5/2)^2\over2\nu}\int|u|^5.              \tag{212.5}
\]

This is a valid differential inequality, but it is not a critical `L^3`
closure. With `w=|u|^(3/2)`, one has
`||grad w||_2^2=(9/4)int |u||grad|u||^2`. In three dimensions the homogeneous
Gagliardo--Nirenberg estimate has the critical form

\[
 \int|u|^5=\|w\|_{10/3}^{10/3}
 \leq C_{GN}\|\nabla w\|_2^2\|w\|_2^{4/3}
 =C_{GN}\|\nabla w\|_2^2 F^{2/3}.                    \tag{212.6}
\]

Thus dissipation absorbs pressure only under a smallness condition of the form
`||u||_3<=c nu`; it gives no estimate for arbitrary critical data. On the
torus (212.6) also has a lower-order `C F^(5/3)` term, which does not repair the
critical coefficient.

In two dimensions the corresponding estimate is

\[
 \int|u|^5\leq C_{GN,2}\|\nabla w\|_2^{4/3}F
                 +C_{0,2}F^{5/3}.                    \tag{212.7}
\]

Young's inequality therefore yields a local ODE of the schematic, fully
constant-trackable form

\[
 F'\leq C_1\nu^{-5}F^3+C_2\nu^{-1}F^{5/3}.            \tag{212.8}
\]

It controls a finite interval depending on `nu`, the initial norm, and the
torus normalization, but it cannot control all time or force the numerical
factor two.

## Vorticity and Biot--Savart

For a two-dimensional solution,

\[
 \partial_t\omega+u\mathbin\cdot\nabla\omega=\nu\Delta\omega
\]

is contractive in every `L^p`, `1<=p<=infinity`. Periodic Biot--Savart and
Hardy--Littlewood--Sobolev give

\[
 \|u(t)\|_3\leq C_{BS,2}\|\omega(t)\|_{6/5}
 \leq C_{BS,2}\|\omega_0\|_{6/5}.                    \tag{212.9}
\]

This proves a global data-dependent bound. It does not imply (212.2), because
`C_BS,2||omega_0||_(6/5)/||u_0||_3` has no universal upper bound. High-frequency
data already make this ratio arbitrarily large, while vorticity rearrangement
can change the negative-order Biot--Savart norm. Vorticity contraction is
therefore compatible both with a factor-two crossing and with global 2D
regularity.

In three dimensions the matching endpoint is

\[
 \|u\|_3\leq C_{BS,3}\|\omega\|_{3/2},                \tag{212.10}
\]

but

\[
 \partial_t\omega+u\mathbin\cdot\nabla\omega
 =\omega\mathbin\cdot\nabla u+\nu\Delta\omega.       \tag{212.11}
\]

The stretching pairing has no sign and does not close in `L^(3/2)`, since
Calderon--Zygmund controls `grad u` in `L^(3/2)`, not in `L^infinity`. The 2D
contraction mechanism does not extend to the Clay dimension.

## Heat contraction and Duhamel

The mild formula is

\[
 u(t)=e^{\nu t\Delta}u_0-
 \int_0^t e^{\nu(t-s)\Delta}{\mathbb P}\nabla\mathbin\cdot
 (u\otimes u)(s)\,ds.                                 \tag{212.12}
\]

The linear term is an `L^3` contraction. Let `K_d` be a valid periodic heat--
Leray constant such that, on the short-time range under consideration,

\[
 \|e^{\nu\tau\Delta}{\mathbb P}\nabla\mathbin\cdot f\|_3
 \leq K_d(\nu\tau)^{-1/2-d/6}\|f\|_{3/2}.             \tag{212.13}
\]

For `d=2` the exponent is `5/6`, hence, with
`Y(t)=||u(t)||_3`,

\[
 Y(t)\leq Y_0+K_2\nu^{-5/6}
 \int_0^t(t-s)^{-5/6}Y(s)^2\,ds.                      \tag{212.14}
\]

A direct bootstrap `sup_[0,t]Y<=2Y_0` closes whenever

\[
 24K_2\nu^{-5/6}t^{1/6}Y_0\leq1,
 \quad\hbox{or equivalently}\quad
 t\leq {\nu^5\over(24K_2Y_0)^6}.                     \tag{212.15}
\]

If (212.13) is recorded only for `tau<=tau_0`, take the minimum of the right
side and `tau_0`. This is an explicit finite-time factor-two theorem once one
fixes the torus and a certified value of `K_2`. Its severe sixth power is the
same scaling seen in (212.8). It has no iteration mechanism: restarting
(212.15) uses the current norm and permits repeated growth.

For `d=3`, (212.13) has exponent one. The resulting integral is logarithmically
nonintegrable at `s=t`, so `sup_(s<=t)||u(s)||_3` alone cannot close the mild
estimate. Kato's endpoint construction introduces some `q>3` and the
profile-dependent quantity

\[
 \eta_q(T)=\sup_{0<t<T}
 t^{(1-3/q)/2}\|e^{\nu t\Delta}u_0\|_q.               \tag{212.16}
\]

For each fixed `u_0 in L^3`, `eta_q(T)` tends to zero with `T`, but not
uniformly on an `L^3` ball. Critical concentration preserves the `L^3` norm
while compressing the required time. Thus standard local theory supplies a
data-profile-dependent factor-two interval, not a constant depending only on
`nu` and `||u_0||_3`.

## Plausibility and falsifier mechanism

The three routes agree on the following conclusions.

1. There is no sign, maximum principle, or heat-kernel contraction known here
   that selects the global numerical constant two.
2. The two-dimensional case is globally regular yet only data-dependent bounds
   emerge. It remains the cleanest place to refute (212.2); a counterexample
   there would not concern singularity.
3. The most plausible finite falsifier mechanism is inviscid low-frequency
   transfer. Find a smooth 2D Euler trajectory with
   `||u^E(T)||_3>(2+delta)||u^E(0)||_3`, then use a quantitative inviscid-limit
   enclosure to choose positive effective viscosity `mu` so that
   `||u^mu(T)-u^E(T)||_3<delta||u^E(0)||_3`. This produces the required strict
   Navier--Stokes crossing.
4. Positive instantaneous `L^3` derivative is insufficient. Amplitude scaling
   replaces viscosity by an effective viscosity and compresses time, but the
   relative amplification converges to the finite Euler amplification on a
   fixed rescaled interval.
5. Conversely, proving (212.2) requires a genuinely global critical-flux
   principle beyond these estimates. The differential inequality is critical
   in 3D, the endpoint Duhamel kernel is nonintegrable, and Biot--Savart is only
   data-dependent in 2D.

Accordingly, the universal factor-two assertion currently looks structurally
unsupported and plausibly false, but no counterexample is claimed. The Cycle
210 interval-certified embedded-2D campaign remains logically appropriate; its
screen should favor trajectories exhibiting inverse transfer and should use
(212.15) only as a local validation scale, not as evidence for the universal
bound.
