# Cycle 257: deterministic multiscale self-strain Euler scout

## Verdict and scope

The prescribed stop condition fires. A deterministic family of 5,184 smooth
two-dimensional Euler initial data was ranked at `N=64` and `N=128`; the 16
largest initial absolute logarithmic velocity-`L^3` derivatives at each
resolution were evolved in both time directions through `|t|=1/2`. The largest
max/min variation was

| resolution | cutoff | time step | largest variation |
|---:|---:|---:|---:|
| 64 | 21 | `2^-10` | `1.017422050416628` |
| 128 | 42 | `2^-11` | `1.0174778325106282` |

Both are below the frozen promotion threshold `1.05`, and the resolutions
agree on the maximizing symmetry class. The search therefore stops without a
longer-time or broader parameter expansion. This is numerical Galerkin
candidate generation only. It is not an Euler PDE certificate, an exhaustive
family exclusion, a Navier--Stokes transfer, or a Millennium result.

## Exact deterministic family

Work on the normalized-Haar torus `(R/2 pi Z)^2`. Let

\[
 \omega_{\rm low}(x,y)
 =\cos x+\alpha\cos y+\rho\cos(x+y),                   \tag{257.1}
\]

where

\[
 \alpha\in\{1/2,1,2\},\qquad
 \rho\in\{-1/2,0,1/2\}.                              \tag{257.2}
\]

This low-frequency field is part of the vorticity and evolves under the same
Biot--Savart law as every other mode. Thus its deformation of the fine packet
is self-induced; no background strain or prescribed transport is used. The
diagonal mode also breaks the equal-radius cancellation of the two axial modes.

Let `R(x,y)=(-y,x)`. There are three base direction/weight packets:

\[
\begin{array}{c|c|c}
 p&(q_{p,0},q_{p,1},q_{p,2})&(w_{p,0},w_{p,1},w_{p,2})\\ \hline
0&((2,1),(5,2),(9,4))&(1,1/2,1/4)\\
1&((2,1),(5,2),(9,4))&(1,-1/2,1/4)\\
2&((2,1),(5,-2),(9,4))&(1,1/2,-1/4).
\end{array}                                             \tag{257.3}
\]

For `r in {0,1,2,3}`, put `q'_{p,j}=R^r q_{p,j}`. For a phase seed
`s in {0,...,7}`, define

\[
 \phi_{s,j}={2\pi\over16}
     \bigl(s(2j+1)+j^2\bmod16\bigr).                   \tag{257.4}
\]

The analytic multiscale packet is

\[
 \omega_{\rm fine}(x,y)=
 -2\beta\sum_{j=0}^2w_{p,j}|q'_{p,j}|
 \sum_{m=1}^{\infty}m e^{-\varepsilon m^2}
 \sin\bigl(m(q'_{p,j}\cdot(x,y)+\phi_{s,j})\bigr),     \tag{257.5}
\]

with

\[
 \varepsilon\in\{1/16,1/8\},\qquad
 \beta\in\{1/16,1/8,1/4\}.                           \tag{257.6}
\]

Finally,

\[
 \boxed{\omega_0=\omega_{\rm low}+\omega_{\rm fine}}. \tag{257.7}
\]

The Gaussian Fourier tail makes every member real analytic. Equations
(257.2)--(257.6) specify
`3*3*2*3*3*4*8=5,184` members, in Python `itertools.product` order. Relative to
Cycle 250, (257.5) retains concentrated one-dimensional derivative profiles
but uses three separated directions and phase/sign variants, while (257.1)
replaces externally imposed kinematics by active low modes.

## Numerical protocol

The scout solves vorticity Euler

\[
 \partial_t\omega+u\cdot\nabla\omega=0,\qquad
 u=\nabla^\perp\Delta^{-1}\omega,                      \tag{257.8}
\]

with a Fourier pseudospectral method, square two-thirds mask, and classical
RK4. Formula (257.5) is truncated only by the mask. Velocity `L^3` is normalized
grid cubature. Every member is first ranked by

\[
 \left|{d\over dt}\log\|u(t)\|_3\right|_{t=0},         \tag{257.9}
\]

computed from the full dealiased Euler right-hand side. The top 16 are evolved
forward and backward, sampled every `1/64`, and scored by

\[
 {\max_{|t|\le1/2}\|u(t)\|_3
  \over\min_{|t|\le1/2}\|u(t)\|_3}.                   \tag{257.10}
\]

This derivative shortlist is deterministic but is not an exhaustive
integration of all 5,184 members; a member with small initial derivative and
large later excursion could be missed.

At both resolutions the maximizing class is

```text
alpha=1, rho=1/2, epsilon=1/16, beta=1/4,
packet=2, rotation=1 or 3, phase_seed=0.
```

At `N=128`, the representative with rotation 1 has minimum
`1.258176858947227` at `t=-1/2` and maximum `1.280167063356655` at `t=1/2`.
Its relative endpoint energy drift is `4.90e-13`; relative endpoint enstrophy
drift is `1.79e-10`. The corresponding `N=64` drifts are `5.05e-12` and
`1.89e-10`. The small, resolution-stable 1.75 percent excursion is nonzero but
negligible for the factor-two objective and below the stated 5 percent
promotion gate.

## Reproduction and artifacts

```text
uv run --with numpy python -m unittest -v test_cycle257_multiscale_strain.py
uv run --with numpy python scout_cycle257_multiscale_strain.py --n 64 --shortlist 16 --dt 0.0009765625 --time 0.5 --sample-dt 0.015625 --output cycle257-multiscale-strain-N64.json
uv run --with numpy python scout_cycle257_multiscale_strain.py --n 128 --shortlist 16 --dt 0.00048828125 --time 0.5 --sample-dt 0.015625 --output cycle257-multiscale-strain-N128.json
```

```text
scout_cycle257_multiscale_strain.py
  sha256 e3da93b239873cf62018750c060fe339820dfe05053c4987f5097904f7161c27
cycle257-multiscale-strain-N64.json
  sha256 746d9babc458a3e319da3481e667b3f64471b56c08b7e55acab8ed5fca7496a0
cycle257-multiscale-strain-N128.json
  sha256 dab593637d9960799ebd18a23eb3361aa9736cbb9c703432cff358f854730c25
```
