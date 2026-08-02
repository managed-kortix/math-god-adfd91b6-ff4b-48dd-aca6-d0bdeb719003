# Cycle 265: genuine 3D Euler amplification pivot architecture

## Strategic decision

Pivot `ND251` candidate generation from weak two-dimensional velocity-`L3`
families to genuinely three-dimensional smooth periodic Euler flow. Preserve
the exact target and transfer logic:

\[
 \|v(T)\|_{L^3(\mathbb T^3)}>(2+\eta)\|v(0)\|_{L^3(\mathbb T^3)},
 \qquad \eta>0,                                         \tag{265.1}
\]

on one rigorously enclosed finite smooth interval. The pivot is justified by
the repeated two-dimensional screens: `C258-V1` promoted `0/4`, and the fresh
structure-preserving `C264-DE1` screen promoted `0/3`, with best directed
endpoint ratio only `1.004458192981`. Those outcomes do not exclude 2D Euler,
but they provide no evidence that another nearby 2D low-mode search will cross
two. Three dimensions add the absent production mechanism, vortex stretching,
while retaining a finite analytic-tail/Picard certificate and an explicit
inviscid transfer.

This document freezes the mathematics of interface `C265-3D-ATI1` and
identifies the first deterministic family. It is not a trajectory-compute
freeze. No family member is run, ranked, tuned, or promoted here. Compute is
authorized only after a separate manifest fixes every coefficient, horizon,
resolution, integrator, endpoint score, and stop rule listed in Section 7.

## 1. Equation, normalization, and genuine three-dimensionality

Use normalized Haar measure on `T^3=(R/2pi Z)^3`. Write

\[
 v(x)=\sum_{k\in\mathbb Z^3\setminus\{0\}}v_k e^{ik\cdot x},
 \qquad k\cdot v_k=0,\qquad v_{-k}=\overline{v_k}.       \tag{265.2}
\]

For `P_k=I-k\otimes k/|k|_2^2`, the Euler equation is

\[
 \dot v_k=F(v)_k=-iP_k\sum_{p+r=k}(v_p\cdot r)v_r.       \tag{265.3}
\]

The retained cube is `S_N={k:0<|k|_infinity<=N}` and
`F_N=P_N F P_N`. All convolutions are ordered. A padded FFT is an
implementation replay of (265.3), not the definition of the vector field.

A family member is genuinely 3D only if its exact Fourier support is not
contained, after any orthogonal lattice change of variables, in a plane and
the exact initial stretching field

\[
 (\omega\cdot\nabla)v,
 \qquad \omega=\nabla\times v,                          \tag{265.4}
\]

is not identically zero. The verifier checks both facts from exact
coefficients. Merely depending on `x_3`, or adding a passive third component to
a 2D carrier, is insufficient.

## 2. Dimension-independent analytic Euler tail

For `q>1`, define the vector Wiener norms

\[
 A_q(v)=\sum_{k\ne0}q^{|k|_1}|v_k|_2,
 \qquad
 D_q(v)=\sum_{k\ne0}|k|_1q^{|k|_1}|v_k|_2.              \tag{265.5}
\]

Because `P_k` has Euclidean operator norm one,

\[
 |v_p\cdot r|\,|v_r|_2
 \le |v_p|_2|r|_1|v_r|_2,
 \qquad q^{|p+r|_1}\le q^{|p|_1}q^{|r|_1}.
\]

Termwise differentiation, with upper Dini derivatives at zero coefficients,
therefore gives exactly

\[
 D^+A_{q(t)}(v(t))
 \le\left(A_{q(t)}(v(t))+{q'(t)\over q(t)}\right)
 D_{q(t)}(v(t)).                                        \tag{265.6}
\]

There is no dimension factor, Leray-projector loss, or hidden vorticity
estimate in (265.6). Choose rational `q0,M,alpha,T` with

\[
 q(t)=q_0(1-\alpha t),\qquad
 A_{q_0}(v_0)\le M,\qquad \alpha\ge M,\qquad q(T)>1.    \tag{265.7}
\]

Here `q'/q=-alpha/(1-alpha t)<=-alpha`, so on the closed face
`A_q(v)=M` the coefficient in (265.6) is nonpositive. The certificate must
check `T>0`, `q0>1`, `M>0`, `alpha>=M`, the initial norm bound, and the strict
gate `q0(1-alpha T)>1` in exact arithmetic. Incompatible radius and slope gates
fail rather than being relaxed. The same closed-face comparison used in Cycle
255 then yields

\[
 A_{q(t)}(v(t))\le M,
 \qquad
 s_n(t):=\sum_{|k|_\infty=n}|v_k(t)|_2
 \le Mq(t)^{-n}.                                       \tag{265.8}
\]

At finite Galerkin cutoff the comparison is elementary. Uniform control at
the smaller fixed weight `q(T)` gives compactness and convergence of the
quadratic convolution at every still smaller weight. Standard analytic-Wiener
local well-posedness and uniqueness then identify the limit and continue it
through time `T`. A certificate may invoke this conclusion only after all
(265.7) gates pass. This proves only finite-time smoothness of the selected
orbit; it assumes nothing about global 3D regularity.

The initial datum may have finite Fourier support. Genuine infinite initial
support is not a mathematical requirement: (265.8) controls every mode created
by the full Euler evolution. If an infinite analytic perturbation is later
included, its contribution to `A_q` must be an exact summed rational bound, not
a sampled truncation.

## 3. Full-PDE retained interface

On a rational slab `I_j=[t_j,t_j+h_j]`, let `c_j(s)` be an exact rational
Fourier-real, divergence-free reference path in `S_N`; the preferred path is
piecewise affine through rationalized implicit-midpoint nodes. Put

\[
 C_j=c_j([0,h_j]),\quad W_j=C_j+E_j,\quad
 e=P_Nv-c_j.                                            \tag{265.9}
\]

The full retained equation is

\[
 \dot x=F_N(x)+r,
 \qquad r=P_NF(v)-F_N(P_Nv).                           \tag{265.10}
\]

At the smaller slab-end weight `q_{j+1}=q(t_j+h_j)`, (265.8) bounds all
unresolved shells. For each retained `k`, the verifier encloses the complete
omitted convolution

\[
 R_{j,k}\supset
 -iP_k\!\sum_{\substack{p+r=k\\p\notin S_N\ \text{or}\ r\notin S_N}}
 (v_p\cdot r)v_r.                                      \tag{265.11}
\]

The enclosure splits into retained--tail and tail--tail terms. Retained
coefficients come from `W_j`; unresolved shells use
`s_n<=Mq_{j+1}^{-n}`. Every infinite remainder is reduced to exact geometric
sums with the three-dimensional shell count
`#{k:|k|_infinity=n}=(2n+1)^3-(2n-1)^3=24n^2+2`.
Using a global convolution radius for every component is valid but likely too
coarse; production should retain directional dot products and exact `P_k`
entries before taking interval absolute values.

Define

\[
 D_j=F_N(W_j)+R_j-\dot c_j.                             \tag{265.12}
\]

The exact recentered Picard gates are

\[
 E_j^{in}+[0,h_j]D_j\subseteq\operatorname{int}E_j,
 \qquad
 E_j^{in}+h_jD_j\subseteq E_j^{out}.                   \tag{265.13}
\]

Entry boxes chain between slabs, and the first contains
`P_Nv_0-c_0(0)`. Equations (265.7), (265.11), and (265.13), not a Galerkin
convergence plot, prove the full-PDE enclosure.

For the exact symmetric Galerkin field, kinetic energy and helicity

\[
 E(v)={1\over2}\int|v|^2,
 \qquad H(v)=\int v\cdot(\nabla\times v)                \tag{265.14}
\]

are quadratic invariants. Implicit midpoint preserves both at zero solve
residual, and their finite-residual defect identities are mandatory integrity
replays. Three-dimensional enstrophy is not invariant and must never be used
as a conservation gate. Retained energy and helicity also exchange with the
unresolved tail, so nominal Galerkin invariance cannot replace (265.13).

## 4. Directed endpoint certification

At both endpoints, interval Fourier evaluation plus three-dimensional
cubature encloses

\[
 C_0=\int_{\mathbb T^3}|v(0,x)|^3\,dx,
 \qquad C_T=\int_{\mathbb T^3}|v(T,x)|^3\,dx.           \tag{265.15}
\]

The cubature remainder uses retained derivative boxes and the complete
analytic tail from (265.8). A forward certificate with rational bounds
`C_0<=U_0` and `C_T>=L_T` proves a directed factor `gamma>2` by

\[
 L_T>\gamma^3U_0.                                      \tag{265.16}
\]

The production objective is the endpoint ratio at the predeclared `T`, not an
interior max/min excursion. Euler time reversal is allowed only after one
complete smooth segment is enclosed; all endpoint boxes and signs then reverse
together. For useful transfer margin, the numerical promotion threshold should
be at least `2.20`, while the final theorem accepts any exact rational
`gamma=2+eta>2`.

## 5. Exact three-dimensional inviscid transfer

The 2D vorticity transfer from Cycle 256 does not apply verbatim in 3D because
vorticity is stretched. Use a second shrinking velocity Wiener norm instead.
Suppose the Euler certificate gives the fixed bound

\[
 A_Q(v(t))\le M\quad(0\le t\le T),\qquad Q=q(T)>1.      \tag{265.17}
\]

Choose exact rational `rho0,beta,epsilon` such that

\[
 1<\rho(t)=\rho_0(1-\beta t)\le\rho_0<Q,
 \qquad \rho(T)>1,\qquad \beta\ge M+\epsilon.          \tag{265.18}
\]

All inequalities in (265.18) are replay gates. In particular, the simultaneous
requirements `beta>=M+epsilon` and `rho0(1-beta T)>1` must be checked exactly;
if they are incompatible, this transfer route supplies no viscosity threshold.

Let `w_nu` solve 3D Navier--Stokes with viscosity `nu>0` and initial datum
`v(0)`, on its maximal smooth interval, and put `z=w_nu-v`. Define

\[
 Z(t)=A_{\rho(t)}(z(t)),
\]

and the exact finite maxima

\[
 \kappa_j=\max_{n\ge1}n^j(\rho_0/Q)^n,\qquad
 G=M\kappa_1,\qquad H=M\kappa_2,\qquad
 B=H\Phi(G,T),                                         \tag{265.19}
\]

where `Phi(G,T)=(exp(GT)-1)/G`, with value `T` at `G=0`.
The maximizing integer is found by comparing consecutive rational terms, so
only the outward exponential bound in `Phi` is non-rational.

Write

\[
 \mathcal B(a,b)_k=-iP_k\sum_{p+r=k}(a_p\mathbin\cdot r)b_r.
\]

The ordered difference is exactly
`B(v,z)+B(z,v)+B(z,z)`: the derivative falls on `z`, `v`, and `z`,
respectively. Subtracting the Fourier equations, retaining the favorable
viscous term, and using the norm-one Leray projector gives

\[
 D^+Z+\nu E_\rho^{(2)}(z)\le D_\rho(v)Z+
 \left(A_\rho(v)+Z+{\rho'\over\rho}\right)D_\rho(z)
 +\nu D_\rho^{(2)}(v).                                 \tag{265.20}
\]

Here
`E_rho^(2)(z)=sum |k|_2^2 rho^{|k|_1}|z_k|_2` is the exact
Laplacian dissipation and
`D_rho^(2)(v)=sum |k|_1^2 rho^{|k|_1}|v_k|_2` is its declared upper
majorant for the viscosity forcing, using `|k|_2^2<=|k|_1^2`.
Thus the coefficient of `D_rho(v)Z` is one, not two; the other mixed
bilinear term contributes `A_rho(v)D_rho(z)`. Dropping the nonnegative
`nu E_rho^(2)(z)` is valid but must not be described as an equality.
Equations (265.17)--(265.19) imply
`D_rho(v)<=G`, `D_rho^(2)(v)<=H`, and
`A_rho(v)<=M`. While `Z<=epsilon`, the coefficient of `D_rho(z)` is
nonpositive because
`rho'/rho=-beta/(1-beta t)<=-beta` and
`A_rho(v)+Z<=M+epsilon<=beta`. Therefore

\[
 Z(t)\le\nu H\Phi(G,t)\le\nu B.                       \tag{265.21}
\]

For certification, replace `B` by a strictly positive rational outward upper
bound `B_up>=B`. If `nu B_up<epsilon`, a first-exit argument makes the
bootstrap strict. If the maximal smooth Navier--Stokes time were at most `T`,
then `A_rho(w_nu)<=A_rho(v)+Z<=M+nu B_up` with
`rho>=rho(T)>1` would give a uniform analytic Wiener, hence Lipschitz, bound up
to that time and the standard local theory would continue the solution. Thus
the maximal time is greater than `T`, and (265.21) holds on `[0,T]`. Since
normalized Haar measure has mass one and
`|z(x)|_2<=A_1(z)<=Z`,

\[
 \sup_{0\le t\le T}\|w_\nu(t)-v(t)\|_3\le\nu B.       \tag{265.22}
\]

This is the analytic-tail/inviscid interface. It is dimension-three specific
in purpose but avoids any unproved 3D vorticity estimate.

For exact endpoint replay, supply rationals `a>0` and `delta>0` with

\[
 a^3\ge U_0,\qquad (2a+\delta)^3<L_T.                  \tag{265.23}
\]

Let `B_up` be the same rigorously replayed positive rational upper bound for
`B` used in the continuation gate. Then every

\[
 0<\nu<\nu_0^{rat}:={\min(\epsilon,\delta)\over B_{up}} \tag{265.24}
\]

satisfies

\[
 \|w_\nu(T)\|_3>2\|w_\nu(0)\|_3.                     \tag{265.25}
\]

There is only one endpoint perturbation because the Euler and viscous initial
data agree exactly. For fixed physical viscosity `nu_phys>0`, the exact scaling

\[
 u_\lambda(t,x)=\lambda w_{\nu_{phys}/\lambda}(\lambda t,x),\qquad
 p_\lambda(t,x)=\lambda^2p_{\nu_{phys}/\lambda}(\lambda t,x)
\]

produces a 3D periodic Navier--Stokes solution at viscosity `nu_phys` whenever
`lambda>nu_phys/nu_0^{rat}`, with the same strict ratio at time `T/lambda`.
Unlike the old route, no two-dimensional lift is used: both the Euler seed and
the transferred Navier--Stokes solution are genuinely 3D.

### Hostile transfer replay

No rigorous transfer certification is emitted unless all of the following
pass exactly:

1. `T,M,Q,rho0,beta,epsilon,a,delta,B_up` are finite in their declared
   exact domains, with `T,M,epsilon,a,delta,B_up>0` and `Q>rho0>1`;
2. both radius gates `rho0(1-beta T)>1` and `beta>=M+epsilon` pass;
3. `kappa_1,kappa_2`, then `G,H`, are recomputed from `rho0/Q` by exact
   consecutive-term comparisons rather than trusted as certificate fields;
4. an outward exponential replay proves the positive rational bound
   `B_up>=H Phi(G,T)`; a rounded exponential value fails;
5. the directed endpoint witnesses satisfy `a^3>=U_0` and the strict gate
   `(2a+delta)^3<L_T`; equality, reversed endpoints, or floating cube roots
   fail; and
6. the emitted effective viscosity obeys the exact strict inequalities
   `0<nu<min(epsilon,delta)/B_up`. For physical viscosity, the emitted
   amplitude obeys `lambda>nu_phys B_up/min(epsilon,delta)` and the terminal
   time is exactly `T/lambda`.

Failure of any gate sets the viscosity threshold to `UNAVAILABLE`; it must not
be weakened, repaired from floating data, or reported as zero/positive. The
amplitude scaling preserves a certified ratio but cannot create the missing
Euler endpoint crossing or cure a failed radius/continuation gate.

## 6. Deterministic vortex-stretching family

Use the Kida--Pelz symmetry class as the primary seed, not as an asserted
singularity scenario. Define the exact trigonometric field `K=(K1,K2,K3)` by

\[
\begin{aligned}
 K_1&=\sin x(\cos3y\cos z-\cos y\cos3z),\\
 K_2&=\sin y(\cos3z\cos x-\cos z\cos3x),\\
 K_3&=\sin z(\cos3x\cos y-\cos x\cos3y).
\end{aligned}                                           \tag{265.26}
\]

The divergence cancels term by term. Let

\[
 \mathcal F(K)=-\mathbb P((K\cdot\nabla)K),             \tag{265.27}
\]

whose Fourier coefficients are exact Gaussian rationals, and let
`K_{2,theta}(x)=K(2x+theta)` for common coordinate phases
`theta_j in {0,pi/2}`. The proposed finite family is

\[
 v_0^{a,b,\theta}=K+{a\over64}\mathcal F(K)
                    +bK_{2,\theta},                    \tag{265.28}
\]

with

\[
 a\in\{-2,-1,1,2\},\qquad
 b\in\{-1/4,-1/8,0,1/8,1/4\},\qquad
 \theta\in\{0,\pi/2\}^3,                              \tag{265.29}
\]

where `theta=(0,0,0)` is the sole phase used when `b=0`. This gives exactly
`4(4*8+1)=132` distinct coefficient-defined profiles before horizons and sign
orientation. Overall amplitude duplicates are not added. The tangent term in
(265.28) breaks special time symmetry and chooses a direction along the Euler
vector field; the doubled translated packet supplies a deterministic
multiscale perturbation without random phases. Every member remains real,
mean-zero, divergence-free, analytic, and finite Fourier at time zero.

This family is plausible rather than proven to cross two. Its advantages are
specific:

1. `K` has nonzero self-induced vortex stretching and three active velocity
   components, so it evades all 2D and passive-2D3C no-go mechanisms.
2. The Kida--Pelz geometry is a standard deterministic setting for strong
   strain/vorticity interaction; the second scale permits localized alignment
   rather than only a single symmetric stretching episode.
3. `mathcal F(K)` supplies an exact directed perturbation rather than selecting
   the favorable sign after seeing a trajectory.
4. All coefficients and the initial analytic norm are finite exact algebraic
   calculations, making (265.7) and the family digest independently replayable.

Vortex stretching alone does not imply velocity-`L3` growth. It raises a
positive-order vorticity quantity, whereas (265.1) requires concentration of
the undifferentiated velocity at fixed energy. Promotion therefore depends
only on the directed endpoint score and not on peak vorticity, enstrophy
growth, spectral slope, or visual tube formation.

## 7. Required pre-compute freeze and stop rules

Before any trajectory is generated, a separate `C265-3DDE1` manifest must fix:

1. the exact Fourier generator for (265.26)--(265.29), coefficient ordering,
   algebraic-number encoding, profile order, and source digest;
2. a rational horizon grid, one forward orientation per enumerated profile,
   and a policy that treats reversal only after full endpoint enclosure;
3. cubic Galerkin cutoffs, dealiased convolution sizes, implicit-midpoint step
   sizes, nonlinear residual gates, and exact energy/helicity defect replays;
4. three-dimensional endpoint cubature grids and a doubled-grid discrepancy
   gate, with no interior-extremum promotion;
5. a numerical lead threshold at least `2.20`, cross-resolution tolerances,
   the maximum number of promotions, and a fixed no-expansion stop;
6. exact analytic-feasibility filtering for (265.7), followed by the maximum
   number of attempted Picard/tail certificates; and
7. the certificate schema for (265.11)--(265.16) and transfer fields
   (265.17)--(265.24), with strict parsing and fail-closed arithmetic.

No adaptive horizon extension, phase insertion, coefficient optimization, or
threshold relaxation is allowed after output is viewed. A failed bounded
screen excludes only (265.28)--(265.29) under its frozen horizons and numerical
gates. A Galerkin crossing is only a lead. The only acceptance path is

```text
exact genuine-3D datum
  -> shrinking full-Euler analytic tail
  -> complete 3D omitted-convolution boxes
  -> recentered retained Picard chain
  -> full-tail directed endpoint cubature above 2+eta
  -> shrinking-Wiener inviscid bound
  -> explicit positive viscosity and amplitude thresholds.
```

## Disposition

Adopt this as the next `ND251` architecture. Retain Cycles 263--264 as reusable
midpoint/Picard infrastructure, replacing 2D vorticity, enstrophy, and the 2D
Biot--Savart transfer by 3D velocity, helicity diagnostics, and
(265.17)--(265.24). Do not run the family until `C265-3DDE1` is separately
frozen. No Euler crossing, Navier--Stokes result, breakdown result, or
Millennium result is claimed.
