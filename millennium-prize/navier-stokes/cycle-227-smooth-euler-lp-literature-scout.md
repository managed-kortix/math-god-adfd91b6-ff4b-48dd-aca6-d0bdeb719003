# Cycle 227: smooth Euler velocity `L^p` literature scout

## Verdict

The literature checked through 2026-08-02 supplies no theorem of the form needed
by the Cycle 211 breaker:

\[
 u\in C^\infty([0,T]\times\mathbb T^d),\quad d=2\text{ or }3,
 \qquad \|u(T)\|_{L^3}>2\|u(0)\|_{L^3}.                 \tag{227.1}
\]

The closest rigorous smooth-data results inflate a derivative norm of the
velocity or vorticity. They do not inflate the undifferentiated velocity in the
same `L^3` norm. The strongest recent two-dimensional result found, Cordoba--
Martinez-Zoroa--Ozanski, gives arbitrary `H^{beta'}` growth of vorticity from
smooth compactly supported data with bounded initial `H^beta`, where
`0<beta<1` and

\[
 \beta'>\frac{(2-\beta)\beta}{2-\beta^2}.               \tag{227.2}
\]

Since velocity is one derivative smoother, this is growth of a positive-order
velocity norm `H^{1+beta'}`, not of velocity `L^3`. There is no norm embedding
or interpolation argument that turns the theorem's lower bound into a lower
bound for `||u(T)||_3/||u(0)||_3`. Thus no published theorem located here
supplies the required factor-greater-than-two Euler seed.

## Exact target and necessary endpoint information

For a mean-zero two-dimensional periodic Euler flow,

\[
 u=\nabla^\perp\Delta^{-1}\omega,
 \qquad \|u\|_{L^3}\asymp\|\omega\|_{W^{-1,3}}.         \tag{227.3}
\]

Consequently a usable theorem must compare the same negative-order vorticity
norm at two times. A statement that only makes `||omega(T)||_{H^s}` large for
`s>=0`, `||nabla omega(T)||_p` large, or the flow-map derivative large does not
control (227.3) from below. High-frequency creation can make every such
positive-order norm large while making `W^{-1,3}` small.

The endpoint denominator is equally essential. A theorem of the form
`||u(T)||_X>K` together with `||u(0)||_Y<=1`, for `X!=Y`, does not give any
same-norm ratio. One needs either (227.1) directly or quantitative bounds

\[
 \|u(0)\|_3\le A,\qquad \|u(T)\|_3>2A.                 \tag{227.4}
\]

Smoothness must hold on the closed transfer interval. Weak, Yudovich, or
point-singular initial data cannot be inserted into the classical inviscid-limit
step without a separate smoothing and stability theorem preserving a strict
ratio margin.

## Theorem-by-theorem audit

### Cordoba--Martinez-Zoroa--Ozanski (newest direct smooth-data candidate)

Diego Cordoba, Luis Martinez-Zoroa, and Wojciech S. Ozanski,
*Instantaneous gap loss of Sobolev regularity for the 2D incompressible Euler
equations*, Duke Math. J. 173 (2024), DOI
`10.1215/00127094-2023-0052`, arXiv:`2210.17458`.

Their Theorem 1 states: for `T,K>0`, `beta in (0,1)`, and `beta'` satisfying
(227.2), there is finite-energy `omega_0 in C_c^infinity(R^2)` with
`||omega_0||_{H^beta}<=1` whose unique global classical 2D Euler solution obeys

\[
 \|\omega(t)\|_{H^{\beta'}}>K,
 \qquad t\in[1/T,T].                                   \tag{227.5}
\]

(The printed interval is nonempty when `T>=1`; this harmless parameter detail
does not affect the mismatch.)

This is genuinely rigorous, has smooth initial data, and gives arbitrary finite
growth. It nevertheless misses (227.1) in three independent ways.

1. The domain is `R^2`, not the fixed torus needed by the present breaker.
2. The inflated quantity is vorticity `H^{beta'}`, equivalently a
   positive-order velocity Sobolev norm, not velocity `L^3`.
3. The initial and final norms differ (`H^beta` versus `H^{beta'}`), so it is
   not a ratio theorem even in the stated Sobolev scale.

The second mismatch is decisive. On a fixed torus, take a smooth Fourier mode
with vorticity amplitude one and frequency `N`. Its vorticity `H^{beta'}` norm
is comparable to `N^{beta'}`, while the induced velocity `L^3` norm is
comparable to `N^{-1}`. Therefore no universal implication
`||omega||_{H^{beta'}}>K => ||u||_3>F(K)` with `F(K)` tending to infinity is
possible. Localization on `R^2` gives the same scaling obstruction.

Their Theorem 2 glues infinitely many packets and obtains instantaneous
infinite `H^{beta'}` norm, but its initial datum is low regularity and the
authors use a special definition of classical solution. It is even farther
from the smooth closed-interval seed.

### Bourgain--Li critical Sobolev inflation

Jean Bourgain and Dong Li, *Strong ill-posedness of the incompressible Euler
equation in borderline Sobolev spaces*, Invent. Math. 201 (2015), DOI
`10.1007/s00222-014-0548-6`, arXiv:`1307.7090`.

The paper treats dimensions two and three and critical velocity spaces
`W^{d/p+1,p}`. Its smooth 2D noncompact construction (Theorem 1.2) starts with
an initial velocity that is `C^infinity`, although its Lipschitz norm is
unbounded, and gives a unique classical solution whose vorticity `H^1` norm is
unbounded in every interval immediately after zero. The compact 2D theorem
(Theorem 1.6) uses a continuous compactly supported perturbation and a Yudovich-
type solution, smooth only away from one point. The 3D noncompact theorem
(Theorem 1.8) gives a `C^infinity` classical solution on a positive interval
with vorticity `H^{3/2}` inflation; the compact 3D theorem (Theorem 1.10) again
has only continuous initial perturbation and local smoothness away from one
point. The informal Besov and Sobolev formulations are Theorems 1.12--1.13.

All of these inflate the critical differentiated norm
`W^{d/p+1,p}` of velocity (or the corresponding vorticity norm). Taking `p=3`
does not select velocity `L^3`; it selects `W^{5/3,3}` in 2D and `W^{2,3}` in
3D. Their lower bounds therefore do not imply a lower bound for velocity
`L^3`. The same high-frequency example used above proves the missing reverse
embedding. Moreover, most compact versions are not globally smooth initial
data. These theorems do not supply (227.1).

### Misiolek--Yoneda weak Besov inflation

Gerard Misiolek and Tsuyoshi Yoneda, *Continuity of the solution map of the
Euler equations in Holder spaces and weak norm inflation in Besov spaces*,
Trans. Amer. Math. Soc. 370 (2018), DOI `10.1090/tran/7101`,
arXiv:`1601.01024`.

The norm inflation concerns critical Besov regularity and the continuity
properties of the Euler solution map. It is not an undifferentiated velocity
`L^p` theorem. In particular, neither the theorem's initial control nor its
inflated endpoint is velocity `L^3`, and no quantitative factor-two endpoint
comparison follows.

### Jeong continuous loss of regularity

In-Jee Jeong, *Loss of regularity for the 2D Euler equations*, arXiv:`2108.09928`.
Theorem 1.1 constructs bounded periodic vorticity

\[
 \omega_0\in L^\infty\cap\bigcap_{p<p_0}W^{1,p}(\mathbb T^2),
 \qquad p_*<p_0<2,
\]

whose unique Yudovich solution has infinite `W^{1,q(t)}` norm, with

\[
 q(t)=1+\frac{1}{1/(p_0-1)+c_0t},\qquad 0\le t\le T_*(p_0).
\]

In velocity variables this is loss of `W^{2,p}` regularity. The initial
vorticity is singular at one point rather than smooth, and the inflated norm is
differentiated. It supplies neither hypothesis required by (227.1).

### Mixing, gradient growth, and damping results

Rigorous 2D Euler constructions of vorticity-gradient growth, small-scale
creation, or inviscid damping control quantities such as
`||nabla omega||_p`, high Sobolev norms, or decay of nonzero velocity modes.
These effects point in the wrong logical direction for (227.3): mixing moves
vorticity toward high frequencies and tends to reduce a negative-order norm.
Time reversal is relevant only after a theorem gives quantitative decay of the
full velocity `L^3` norm relative to its initial value. The surveyed results do
not state such a same-norm bound, and vorticity rearrangement alone does not
provide it.

### Three-dimensional rough or singular constructions

The 3D literature also contains loss-of-smoothness shear flows, critical-space
ill-posedness, weak convex-integration solutions, and finite-time singularity
results with boundaries or sub-Lipschitz data. None is a smooth periodic Euler
trajectory on a closed regular interval with a finite endpoint velocity `L^3`
ratio. Energy conservation for smooth 3D Euler controls `L^2`, not `L^3`, but
does not manufacture the missing endpoint estimate.

## Why arbitrary Sobolev inflation cannot be converted

The mismatch is structural rather than a missing constant. On `T^2`, let

\[
 \omega_N(x)=a_N\sin(Nx_1),\qquad
 u_N=\nabla^\perp\Delta^{-1}\omega_N.
\]

Then, up to constants independent of `N`,

\[
 \|\omega_N\|_{H^s}\sim |a_N|N^s,
 \qquad \|u_N\|_3\sim |a_N|N^{-1}.                     \tag{227.6}
\]

Choosing `a_N=N^{-s}` keeps `||omega_N||_{H^s}` bounded while
`||u_N||_3` tends to zero; choosing `a_N=1` makes the Sobolev norm diverge while
the velocity norm again tends to zero. Thus positive-order norm inflation gives
no lower bound at all for the required velocity norm. Interpolation with
conserved energy gives upper bounds for intermediate norms, not a lower bound
for `L^3`, and therefore cannot repair the implication.

The phrase "norm inflation" is consequently insufficient. For the Cycle 211
application, the theorem must name velocity `L^3` at both endpoints, or name
vorticity `W^{-1,3}` at both endpoints, with a strict quantitative ratio.

## Newest-literature check and disposition

Searches through 2026-08-02 of recent records for incompressible Euler norm
inflation, velocity `L^p` growth, transient growth, and loss of regularity found
no 2025--2026 theorem closing this gap. The new records returned by broad norm-
inflation searches concern hypodissipative Navier--Stokes, Boussinesq, SQG,
MHD, quantum Euler, or Einstein--Euler, not the classical incompressible Euler
seed (227.1). Recent classical Euler papers returned by the searches concern
well-posedness classes, singularity formation, or measure-valued solutions,
again without the same-norm endpoint statement.

This is a literature non-supply result, not a proof that a smooth Euler seed
does not exist. The rigorous conclusion is narrower:

> None of the identified norm-inflation, loss-of-regularity, mixing, damping,
> or 3D rough-solution theorems implies (227.1) under its printed hypotheses.

The Cycle 211 breaker therefore remains a new construction/certification task.
A qualifying future theorem should be screened against four non-negotiable
fields: fixed domain, smoothness on `[0,T]`, the same velocity `L^3` norm at
both endpoints, and a strict ratio greater than two. No Navier--Stokes or
Millennium result is claimed.

## Primary sources

1. Cordoba--Martinez-Zoroa--Ozanski, DOI
   `10.1215/00127094-2023-0052`, arXiv:`2210.17458`, especially Theorems 1--2.
2. Bourgain--Li, DOI `10.1007/s00222-014-0548-6`, arXiv:`1307.7090`,
   especially Theorems 1.2, 1.6, 1.8, 1.10, and 1.12--1.13.
3. Misiolek--Yoneda, DOI `10.1090/tran/7101`, arXiv:`1601.01024`.
4. Jeong, arXiv:`2108.09928`, especially Theorem 1.1 and Remark 1.2.
