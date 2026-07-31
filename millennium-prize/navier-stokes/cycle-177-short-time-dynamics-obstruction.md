# Cycle 177: terminal seeding is not a dynamically preserved filter

The simultaneous Laurent identity from Cycle 176 is an exact statement about
the quadratic vector field at one instant. Its terminal outputs do become real
receiver amplitudes under Euler or Navier--Stokes evolution. However, the same
Taylor calculation shows that the cancellation manifold is not invariant:
viscosity reweights colliding representations differently, and the newly
created terminal modes interact with the pumps. Thus the filter seeds modes,
but it does not execute a clean next stage while retaining its cancellations.

## Exact invariant shear equation

Write the Cycle 176 field in physical variables as

\[
 u=(0,V(x,t),W(x,y,t)).
\]

This infinite-dimensional shear class is invariant, has constant pressure, and
obeys

\[
 \partial_tV=\nu\partial_x^2V,
 \qquad
 \partial_tW+V\partial_yW=\nu(\partial_x^2+\partial_y^2)W.
 \tag{1}
\]

Consequently the same calculation is valid in every finite Galerkin system
that retains the modes displayed below. Let `D=z d/dz`, let `G` be the pump
Laurent polynomial, and let `F(t)` denote the coefficient polynomial of the
`+Y` Fourier layer of `W`. Equation (1) becomes exactly

\[
 \dot G=-\nu D^2G,
 \qquad
 \dot F=-\nu(D^2+Y^2)F-iYG F.
 \tag{2}
\]

At `t=0`, Cycle 176 gives

\[
 F(0)G(0)=A_T=z^{-T}-z^T,
 \qquad T=R_D.
 \tag{3}
\]

The exact Duhamel formula for every rail coefficient is

\[
 F_r(t)=e^{-\nu(r^2+Y^2)t}F_r(0)
 -iY\int_0^t e^{-\nu(r^2+Y^2)(t-s)}[G(s)F(s)]_r\,ds.
 \tag{4}
\]

In particular, if the terminal modes are absent initially, then

\[
 F_{-T}(t)=-iYt+O(t^2),
 \qquad
 F_T(t)=iYt+O(t^2).
 \tag{5}
\]

Thus the algebraic outputs really do seed receiver amplitudes; they are not
merely formal convolution labels.

## Tangency obstruction

Put `C(t)=G(t)F(t)`, the polynomial whose coefficients are the instantaneous
quadratic rail forcing before the common factor `-iY`. Differentiating (2)
gives the exact identity

\[
 \boxed{
 \dot C=-\nu\{(D^2G)F+G(D^2F)+Y^2C\}-iYG C
 }
 \tag{6}
\]

or, using the Laurent product rule,

\[
 \dot C=-\nu(D^2+Y^2)C
       +2\nu(DG)(DF)-iYGC.
 \tag{7}
\]

For every interior exponent `r` with `[A_T]_r=0`, (7) reduces at time zero to

\[
 \boxed{
 [\dot C(0)]_r=2\nu[(DG)(DF)]_r-iY[GA_T]_r.
 }
 \tag{8}

The first term is the viscous obstruction. Two representations `x+s=r` that
cancel in `FG` acquire different heat weights
`x^2+Y^2+s^2`; cancellation survives only under an additional equal-weight
coincidence. The second term is the dynamical obstruction. It is the
interaction of the newly generated terminal pair with the already present
pumps. It remains when `nu=0`.

The two mechanisms are independent and cannot be removed by saying that
Navier--Stokes has no dispersive phase. Diagonal heat damping changes collision
weights, while nonlinear evolution multiplies the terminal boundary by `G`.

## Small exact example

Take `R=Y=nu=1`, multipliers `(2,4)`, and put the first factor on the rail and
the second on the pump. Then

\[
 F=A_1H_0=A_2=z^{-2}-z^2,
 \qquad
 G=H_1=z^{-6}+z^{-2}+z^2+z^6,
\]

so `FG=A_8`. Formula (8) gives

\[
 [\dot C(0)]_4=-32,
 \qquad
 [\dot C(0)]_6=i.
 \tag{9}
\]

The exponent `4` is pure viscous leakage and exponent `6` is pure nonlinear
terminal--pump leakage. Applying (4) once more yields the exact Taylor data

\[
 F_4(t)=16it^2+O(t^3),
 \qquad
 F_6(t)=\frac12t^2+O(t^3).
 \tag{10}
\]

At the same time `F_{-8}(t)=-it+O(t^2)` and
`F_8(t)=it+O(t^2)`. Hence terminal receivers turn on at order `t`, but unwanted
rails turn on already at order `t^2`.

There are exceptional first-order coincidences: for example, if each family is
supported on one `x`-shell, the viscous term in (8) can vanish. This does not
repair the construction, because `GA_T` generally remains. Projecting all of
these outputs away can make a specially chosen Galerkin truncation look closed,
but it also removes genuine Navier--Stokes interactions and cannot certify the
PDE cascade.

If a prospective next pump factor is included from time zero, the full initial
product telescopes directly to the final boundary and the intermediate
receiver has zero first derivative. If it is not included, (5) seeds the
intermediate receiver but (8) simultaneously creates uncancelled channels.
This is the obstruction: simultaneous cancellation and sequential dynamic
promotion are not compatible in this scalar two-shear filter without a new
invariant-manifold or error-control mechanism.

This is an exact short-time no-go for the proposed Laurent-filter dynamics,
not a Navier--Stokes regularity theorem or blowup construction. Verify the
Laurent and Taylor coefficients with

```sh
python3 millennium-prize/navier-stokes/verify_cycle177_short_time_filter.py
```
