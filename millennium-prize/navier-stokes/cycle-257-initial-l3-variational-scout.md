# Cycle 257: exact initial velocity-L3 variation and constrained Fourier scout

## Verdict

For smooth mean-zero two-dimensional Euler data on the square torus, the exact
initial cubic velocity variation is

\[
 {d\over dt}\|u\|_3^3\bigg|_{t=0}
 =3\int_{\mathbb T^2}|u|u\cdot
 K[-u\cdot\nabla\omega] \,dx,                         \tag{257.1}
\]

where `omega=curl u` and `K=grad^perp Delta^-1` in the convention
`u=(-partial_y psi,partial_x psi)`. Equivalently, if

\[
 \omega(x)=\sum_{k\ne0}\widehat\omega_k e^{ik\cdot x},\qquad
 \widehat u_k={i k^\perp\over |k|^2}\widehat\omega_k,
\]

then

\[
 \widehat{\omega_t}_k
 =\sum_{p+q=k}{p^\perp\cdot q\over |p|^2}
   \widehat\omega_p\widehat\omega_q,                  \tag{257.2}
\]

and (257.1), with `K omega_t` reconstructed from these coefficients, is an
exact finite formula whenever the initial Fourier support is finite. The
integral is generally not a finite polynomial in the coefficients because of
the factor `|u|`; its spatial form is the exact formula, not a cubature claim.

A deterministic constrained screen over every real streamfunction mode in the
box `|kx|,|ky|<=5` finds positive scale-invariant logarithmic derivatives but
no structural route to a factor two. On energy-one shells with enstrophy
`rho=4,8,12,16,20`, the best sampled values of

\[
 \mathcal J(\psi)
 ={(d/dt)\log\|u\|_3|_{0}\over\|u\|_2}
 ={\int |u|u\cdot u_t\over
   \int |u|^3\,\|u\|_2}                               \tag{257.3}
\]

are respectively `0.13759`, `0.21542`, `0.27084`, `0.30010`, and `0.30545`.
These are floating lower candidates, not upper bounds or PDE certificates.

## Derivation

The Euler vorticity equation is

\[
 \omega_t+u\cdot\nabla\omega=0,\qquad u=K\omega.
\]

Since `z -> |z|^3` is continuously differentiable, smoothness gives

\[
 {d\over dt}\int |u|^3=3\int |u|u\cdot u_t,
 \qquad u_t=K\omega_t=-K(u\cdot\nabla\omega),
\]

which proves (257.1), including points where `u=0`. Formula (257.2) follows by
inserting the Fourier series. The pressure form is also useful:

\[
 {d\over dt}\|u\|_3^3
 =-3\int |u|u\cdot(u\cdot\nabla u+\nabla p).
\]

The transport term is not separately zero: integration by parts gives
`-3 integral |u| u dot (u dot grad u)=0`, but only because it equals
`-integral u dot grad(|u|^3)=0`. Thus

\[
 {d\over dt}\|u\|_3^3=3\int p\,\operatorname{div}(|u|u),               \tag{257.4}
\]

with `-Delta p=sum_(i,j) partial_i u_j partial_j u_i`. This is equivalent to
(257.1) and provides an independent sign check.

The logarithmic derivative follows without an erroneous factor three:

\[
 {d\over dt}\log\|u\|_3
 ={\int |u|u\cdot u_t\over\int|u|^3}.                 \tag{257.5}
\]

Under Euler amplitude scaling `u -> lambda u(lambda t)`, (257.5) scales by
`lambda`. Therefore (257.3), dividing by the conserved `L2` norm, is invariant
under amplitude scaling. Spatial frequency scaling on a fixed torus is not a
symmetry of a fixed finite box and is controlled separately by enstrophy.

## Exact coefficient gradient

Write the real streamfunction as `psi=sum_j x_j phi_j`, set
`v_j=grad^perp phi_j`, `eta_j=Delta phi_j`,

\[
 u=\sum_jx_jv_j,\quad \omega=\sum_jx_j\eta_j,\quad
 f=-u\cdot\nabla\omega,\quad b=Kf,
\]

and define `F=integral |u|^3`, `N=integral |u|u dot b`, and
`E=integral |u|^2`. For each coefficient,

\[
 \partial_j f=-v_j\cdot\nabla\omega-u\cdot\nabla\eta_j,                \tag{257.6}
\]

\[
 \partial_jF=3\int |u|u\cdot v_j,                                     \tag{257.7}
\]

\[
 \partial_jN=\int\left[
 |u|v_j\cdot b+{(u\cdot v_j)(u\cdot b)\over|u|}
 +(K^*(|u|u))\partial_jf\right].                                      \tag{257.8}
\]

The quotient in (257.8) is assigned its continuous value zero at `u=0`.
Consequently

\[
 \partial_j\mathcal J={\partial_jN\over F\sqrt E}
 -\mathcal J\left({\partial_jF\over F}+{\partial_jE\over2E}\right).   \tag{257.9}
\]

The implementation evaluates (257.6)--(257.9), rather than finite-differencing
the objective. Directional finite differences are retained only as a breaker;
the recorded relative errors are between `5.5e-12` and `1.8e-9`.

## Energy and enstrophy constraints

The screen uses normalized Haar measure and constrains

\[
 E(x)=\sum_k |k|^2|\widehat\psi_k|^2=1,\qquad
 Z(x)=\sum_k |k|^4|\widehat\psi_k|^2=\rho.             \tag{257.10}
\]

Every gradient is projected onto the intersection of the tangent hyperplanes
`grad E dot h=grad Z dot h=0`. A deterministic exponential spectral tilt
`x_k -> exp(beta(|k|^2-rho))x_k`, with `beta` found by bisection, restores
`Z/E=rho`; scalar normalization then restores `E=1`. The tilt ratio is strictly
increasing unless the state lies on one shell, so each retraction is uniquely
defined for an interior `rho`.

This is an equality-constrained exploration. For the interval shell
`rho in [rho_-,rho_+]`, exact candidate handling is finite: inspect stationary
KKT boxes in the interior and constrained boxes on both boundary shells. A
rigorous upper bound would interval-evaluate (257.1), (257.6)--(257.10) on all
boxes after branch-and-bound. The JSON field `coefficient_box_radius` merely
declares seed boxes for such a pass; it is not an interval proof.

## Structural bound

Energy and enstrophy give a direct scale-aware upper estimate for the same
instantaneous objective. Let `C_B` satisfy
`||K g||_3<=C_B||g||_(3/2)` and let `C_GN` satisfy
`||u||_3<=C_GN||u||_2^(2/3)||grad u||_2^(1/3)`. Then

\[
 |N|\le\||u|u\|_{3/2}\|K(u\cdot\nabla\omega)\|_3
 \le C_B\|u\|_3^2\|u\|_3\|\nabla\omega\|_3.          \tag{257.11}
\]

For data supported in `|k|<=K`, Gagliardo--Nirenberg and Parseval give
`||grad omega||_3<=C_GN K^(4/3) Z^(1/2)`. Combining this with
`||u||_3>=||u||_2=E^(1/2)` yields the coarse finite-family bound

\[
 |\mathcal J|\le C_B C_GN K^{4/3}(Z/E)^{1/2}.           \tag{257.12}
\]

It is explicit once torus constants are fixed, but far too weak to exclude the
numerical candidates or prove a factor-two accumulation. More importantly, a
positive initial derivative alone has no duration lower bound. Even an exact
value `mathcal J=c` proves only local growth; reaching two would require control
of the logarithmic derivative along the orbit for integrated area `log 2`.
The observed `c about 0.305` at energy one suggests a formal constant-rate time
near `log(2)/c about 2.27`, but no such persistence is established.

## Reproduction and scope

```bash
g++ -O3 -std=c++20 -Wall -Wextra -pedantic \
  cycle257_initial_l3_optimizer.cpp -o cycle257_initial_l3_optimizer
./cycle257_initial_l3_optimizer --max-wave 5 --grid 48 \
  --starts 12 --iterations 120 --output cycle257-initial-l3-candidates.json
python -m unittest -q test_cycle257_initial_l3_optimizer.py
```

The optimization is deterministic, and each candidate is reevaluated on a
doubled spatial grid. The largest doubled-grid value is `0.3052711112` at
`rho=20`. The run is floating candidate generation only: it gives neither a
global optimum over the finite family, an interval upper bound, a finite-time
Euler ratio, nor a Navier--Stokes or Millennium result.
