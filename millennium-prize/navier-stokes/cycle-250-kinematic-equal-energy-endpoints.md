# Cycle 250: exact kinematic equal-energy endpoints with an `L^3` gap

## Status: KINEMATIC ONLY

This cycle constructs two real-analytic, equimeasurable, mean-zero vorticities
on the two-torus whose homogeneous `dot H^-1` energies agree exactly while the
associated Biot--Savart velocities have a directed `L^3` ratio strictly greater
than two. This passes only the static endpoint screen in Cycle 247.

No Euler orbit, self-induced Lagrangian path, Navier--Stokes solution, inviscid
limit, or three-dimensional transfer is constructed. In fact, the explicit
toral automorphism used below is not isotopic to the identity when `N>0`, so it
cannot itself be a finite-time flow map. No Millennium problem is claimed
solved.

## Normalization and profiles

Work on

\[
 \mathbb T^2=(\mathbb R/2\pi\mathbb Z)^2
\]

with normalized Haar measure. Let `Delta=partial_x^2+partial_y^2` and
`grad^perp=(-partial_y,partial_x)`. For mean-zero vorticity set

\[
 K\omega=\nabla^\perp\Delta^{-1}\omega,
 \qquad
 \|\omega\|_{\dot H^{-1}}^2=\|K\omega\|_2^2.       \tag{250.1}
\]

For `epsilon>0`, define the periodic heat-kernel profile and a reference
profile by

\[
 P_\varepsilon(s)=\sum_{m\in\mathbb Z}e^{-\varepsilon m^2}e^{ims},
 \qquad F_\varepsilon=P_\varepsilon-1,
 \qquad G(s)=\sin s.                                  \tag{250.2}
\]

These are real analytic, real valued, and mean zero. Put

\[
 a=\|F_\varepsilon\|_2,\quad A=\|F_\varepsilon\|_3,
 \qquad b=\|G\|_2=2^{-1/2},\quad
 B=\|G\|_3=\left(\frac4{3\pi}\right)^{1/3}.          \tag{250.3}
\]

Poisson summation and localization to the heat-kernel peak give for each fixed
`p>1`

\[
 \|F_\varepsilon\|_p
 \sim \pi^{(p-1)/(2p)}p^{-1/(2p)}
       \varepsilon^{-(p-1)/(2p)}
 \quad(\varepsilon\downarrow0).                       \tag{250.4}
\]

Subtracting `1` does not alter the leading term because that term diverges in
`L^p`. In particular,

\[
 R_\varepsilon:=\frac{A/a}{B/b}\longrightarrow\infty. \tag{250.5}
\]

Fix any `epsilon>0` sufficiently small that

\[
 R:=R_\varepsilon>2.                                  \tag{250.6}
\]

This is the sole concentration choice. Equation (250.4) proves analytically
that the set of such choices contains an interval `(0,epsilon_0)` for some
`epsilon_0>0`; no numerical quadrature is part of the existence proof.

## Exact endpoint pair

Choose an integer `N>=1`, set `L=sqrt(1+N^2)`, and introduce

\[
 B_N=\begin{pmatrix}1&N\\N&N^2+1\end{pmatrix}.
                                                               \tag{250.7}
\]

For the continuous amplitude parameter `t>0`, define

\[
 \begin{aligned}
 \omega_0^t(x,y)
   &=F_\varepsilon'(x)+tG'(-Nx+y),\\
 \omega_1^t(x,y)
   &=F_\varepsilon'(x+Ny)+tG'(y).
 \end{aligned}                                                \tag{250.8}
\]

Both vorticities are real analytic and mean zero. The endpoint theorem uses

\[
 t=t_*:=\frac ab.                                             \tag{250.9}
\]

The heat-kernel component is coherent at unit scale in `omega_0` and lies on
the direction `(1,N)` in `omega_1`; the sinusoidal component makes the opposite
move, from `(-N,1)` to `(0,1)`. Thus the construction combines concentration
with a reciprocal multiscale placement rather than changing the vorticity
distribution.

## Hostile check 1: pullback and orientation

The determinant is

\[
 \det B_N=(N^2+1)-N^2=1.                               \tag{250.10}
\]

Hence `B_N` induces a smooth orientation-preserving Haar-measure-preserving
automorphism of `T^2`. Direct substitution, including the sign in the second
profile, gives

\[
 \begin{aligned}
 \omega_0^t(B_N(x,y))
 &=F_\varepsilon'(x+Ny)
   +tG'\bigl(-N(x+Ny)+Nx+(N^2+1)y\bigr)\\
 &=F_\varepsilon'(x+Ny)+tG'(y)=\omega_1^t(x,y).
 \end{aligned}                                                \tag{250.11}
\]

Therefore `omega_1^t=omega_0^t o B_N`. If transported-vorticity notation is
written as `omega_1=omega_0 o eta^{-1}`, the corresponding endpoint map is
`eta=B_N^{-1}`, not `B_N`. Since either toral automorphism preserves Haar
measure, for every Borel function `Phi` for which the integral exists,

\[
 \int_{\mathbb T^2}\Phi(\omega_1^t)
 =\int_{\mathbb T^2}\Phi(\omega_0^t).                  \tag{250.12}
\]

Thus the endpoints are exactly equimeasurable, including equality of every
distribution function and every vorticity Casimir.

## Hostile check 2: derivative signs and Biot--Savart formula

For a mean-zero periodic `H` and a nonzero integer vector `q`, Fourier series
with the conventions above give

\[
 K[H'(q\mathbin\cdot z)]
 =\frac{q^\perp}{|q|^2}H(q\mathbin\cdot z),
 \qquad q^\perp=(-q_2,q_1).                            \tag{250.13}
\]

Indeed, the derivative contributes `im`, `Delta^-1` contributes
`-1/(m^2|q|^2)`, and `grad^perp` contributes `im q^perp`; the two minus signs
cancel. A different simultaneous convention for `Delta^-1` or `grad^perp`
changes only the global velocity sign and none of the norms below.

Applying (250.13) without dropping the negative entry in `q=(-N,1)` yields

\[
 \begin{aligned}
 u_0^t
 &= (0,1)F_\varepsilon(x)
    +t\frac{(-1,-N)}{L^2}G(-Nx+y),\\
 u_1^t
 &= \frac{(-N,1)}{L^2}F_\varepsilon(x+Ny)
    +t(-1,0)G(y).
 \end{aligned}                                                \tag{250.14}
\]

In particular, the magnitudes of the two primitive contributions are
respectively `(1,L^-1)` at endpoint zero and `(L^-1,1)` at endpoint one.

## Hostile check 3: cross-term orthogonality and exact energy

The phase maps

\[
 (x,y)\mapsto(x,-Nx+y),\qquad
 (x,y)\mapsto(x+Ny,y)                                  \tag{250.15}
\]

are unimodular toral automorphisms. Since both `F_epsilon` and `G` have zero
mean, change of variables gives

\[
 \int F_\varepsilon(x)G(-Nx+y)=0,
 \qquad
 \int F_\varepsilon(x+Ny)G(y)=0.                       \tag{250.16}
\]

The velocity vectors in (250.14) need not be perpendicular; it is the scalar
profile integrals (250.16), not pointwise vector orthogonality, that kill the
`L^2` cross terms. Consequently

\[
 \begin{aligned}
 \|\omega_0^t\|_{\dot H^{-1}}^2
   &=a^2+\frac{t^2b^2}{L^2},\\
 \|\omega_1^t\|_{\dot H^{-1}}^2
   &=\frac{a^2}{L^2}+t^2b^2.
 \end{aligned}                                                \tag{250.17}
\]

Their signed difference is

\[
 D(t)=\left(1-L^{-2}\right)(a^2-t^2b^2).               \tag{250.18}
\]

This continuous function is positive at zero and negative for `t>a/b`. Its
unique positive zero is exactly `t_*=a/b`, proving

\[
 \boxed{
 \|\omega_0^{t_*}\|_{\dot H^{-1}}^2
 =\|\omega_1^{t_*}\|_{\dot H^{-1}}^2
 =a^2(1+L^{-2}).}                                      \tag{250.19}
\]

Thus the continuous tuning is exact, not approximate.

## Hostile check 4: directed `L^3` ratio

At `t=t_*`, define `C=t_*B`. Then

\[
 \frac AC=\frac{A/a}{B/b}=R>2.                         \tag{250.20}
\]

The reverse triangle inequality at endpoint zero and the triangle inequality
at endpoint one, together with Haar invariance of each primitive profile, give

\[
 \|u_0^{t_*}\|_3\ge A-\frac CL,
 \qquad
 \|u_1^{t_*}\|_3\le C+\frac AL.                       \tag{250.21}
\]

Therefore the high-concentration endpoint is `u_0`, and the ratio is directed
as

\[
 \frac{\|u_0^{t_*}\|_3}{\|u_1^{t_*}\|_3}
 \ge \frac{R-L^{-1}}{1+R/L}.                           \tag{250.22}
\]

Choose any integer `N` satisfying the exact symbolic condition

\[
 \sqrt{1+N^2}>\frac{1+2R}{R-2}.                        \tag{250.23}
\]

The right side is finite because `R>2`, and arbitrarily large integers exist.
Multiplying positive denominators in (250.22) shows that (250.23) is precisely
sufficient for

\[
 \boxed{
 \frac{\|K\omega_0^{t_*}\|_{L^3}}
      {\|K\omega_1^{t_*}\|_{L^3}}>2.}                 \tag{250.24}
\]

The reverse quotient is not claimed. The strictness comes from the strict
choices `R>2` and (250.23), even though (250.21) itself uses non-strict norm
inequalities.

## Symbolic existence theorem

For every sufficiently small `epsilon>0`, calculate the exact profile norms in
(250.3), set `t_*=a/b`, and take any integer `N` obeying (250.23). Equations
(250.8) then give a completely specified real-analytic endpoint pair with all
of the following properties:

1. `omega_1=omega_0 o B_N`, with `B_N in SL(2,Z)` orientation preserving;
2. `omega_0` and `omega_1` are exactly equimeasurable and mean zero;
3. their homogeneous `dot H^-1` energies are exactly equal;
4. the directed velocity ratio `||K omega_0||_3/||K omega_1||_3` is strictly
   greater than two.

Here "calculate" means evaluate the norms defined by their convergent analytic
Fourier series or normalized integrals; no closed elementary form is required
for `a` or `A`. This is an analytic symbolic existence theorem with one
continuously tuned parameter and one integer scale choice. Its output remains
**KINEMATIC ONLY**:
equal energy and equimeasurability are necessary Euler endpoint conditions,
not sufficient dynamical-accessibility conditions.
