# Cycle 225: exact quadratic leakage cancellation gate

## Decision

On the fixed eight Fibonacci rails from Cycle 224, a nonzero packet with six
designated instantaneous isolated triads **can** satisfy the finite admission inequality
`mathcal L^2 <= mathcal I^2/16`.  An exact rational packet is given below.  In
contrast, exact cancellation of every first-order exterior mode is impossible
as soon as the sixth directed triad is required to be nonzero.  A saturated
five-variable Groebner calculation returns the unit ideal, with a one-line
Bezout certificate.

This decides only the instantaneous quadratic leakage gate.  The frozen orbit
test below subsequently fails item 4. Neither calculation is a PDE claim, a
factor-two crossing, or a statement about Navier--Stokes regularity.

## Polynomial formulation

Use the frozen Cycle 212 convention `k^perp=(k_2,-k_1)`, so the ordered Euler
coefficient is `-det(p,q)/|p|^2`. Let `k_j=(F_(j+1),F_j)`, `1<=j<=8`, and write the independent positive-mode
vorticities as

\[
 z_j=x_j+i y_j=A_j e^{i\theta_j},\qquad
 z_{-k_j}=\overline {z_j}.
\]

For every output `m`, collect all ordered convolution terms before imposing a
norm:

\[
 B_m(x,y)=\sum_{p+q=m}{-p\wedge q\over |p|^2}z_pz_q.
 \tag{225.1}
\]

Equivalently, after pairing `(p,q)` and `(q,p)`, each unordered pair contributes

\[
  -(p\wedge q)(|p|^{-2}-|q|^{-2})z_pz_q.
 \tag{225.2}
\]

Thus `B_m=P_m+iQ_m` with exact quadratic polynomials `P_m,Q_m` over `Q`.
The complete cancellation equations are

\[
 P_m=Q_m=0\quad(m\notin S),                         \tag{225.3}
\]

and the two forcing budgets are the quartics

\[
 \mathcal L^2=\sum_{m\notin S}{P_m^2+Q_m^2\over|m|^2},
 \qquad
 \mathcal I^2=\sum_{m\in S}{P_m^2+Q_m^2\over|m|^2}. \tag{225.4}
\]

The exact semialgebraic admission equation is obtained with a slack `s`:

\[
 \mathcal I^2-16\mathcal L^2-s^2=0.               \tag{225.5}
\]

For the directed chain `k_j+k_(j+1)=k_(j+2)`, the lower-receiver rate is

\[
 R_j=-4(k_j\wedge k_{j+1})
 (|k_{j+1}|^{-2}-|k_{j+2}|^{-2})
 A_jA_{j+1}A_{j+2}
 \cos(\theta_j+\theta_{j+1}-\theta_{j+2}).          \tag{225.6}
\]

The designated isolated-triad conditions are `R_j>0`, `1<=j<=6`. In Cartesian
variables the phase-amplitude factor in (225.6) is exactly
`Re(z_j z_(j+1) conjugate(z_(j+2)))`, a cubic polynomial, so no trigonometric
approximation enters the decision.

## Exact admitted packet

Set `epsilon=1/1000`, use phases `(pi,pi,0,0,0,pi,pi,pi)`, and take signed real
amplitudes

\[
 (a_1,\ldots,a_8)=
 (-\epsilon,-\epsilon,1,1,1,-\epsilon,-\epsilon,-\epsilon). \tag{225.7}
\]

All six values in (225.6) are strictly positive.  Full exact convolution gives
the rational values stored in `cycle225-quadratic-leakage-certificate.json` and

\[
 {\mathcal L^2\over\mathcal I^2}
 ={221566150214377794643486738050958086496690696332305977982
 \over
 5394620087876012357406842563085445747466566163719048937505}
 \approx0.04107168746<\frac1{16}.                   \tag{225.8}
\]

The verifier checks the stronger exact integer/rational sign statement
`mathcal I^2-16 mathcal L^2>0`.  This packet is nonzero at every rail, although
some transfer rates are small.  Cycle 224's admission rule imposes nonzero
rather than a uniform lower bound after normalization, so (225.7) meets its
items 1--3. It fails the frozen orbit condition in item 4 as recorded next.

## Frozen item 4 orbit failure

The deterministic continuation uses the real packet (225.7) without changing
any frequency, phase, amplitude, normalization, checkpoint, or stopping time.
It applies the square `2/3`-dealiased Fourier--Galerkin vorticity system, the
same pseudospectral convolution at both resolutions, AB2 after one Euler start,
and velocity `L^3` cubature on the collocation grid. Ratios are sampled at the
frozen `1/16` checkpoints through `T=8`. The two prescribed runs are exactly

| floating label | endpoint and checkpoint maximum | energy drift | enstrophy drift |
|---|---:|---:|---:|
| `N128 dt1/1024 T8` | `1.0006370099010511` | `3.330670805823388e-08` | `1.0158541052796011e-07` |
| `N256 dt1/2048 T8` | `1.0006370044160084` | `8.326847655837355e-09` | `2.5396648117848031e-08` |

In both runs the maximum sampled ratio occurs at `T=8`. The ratio discrepancy
is `5.485042642528804e-09`; both invariant drifts are below `2^-20`. Thus the
convergence and drift checks pass, but the common ratio is only about
`1.000637`, far below the required `9/4`. Item 4 therefore fails. Under the
frozen Cycle 224 stop rule there is no amplitude, phase, time, method, or nearby
packet tuning and no post hoc budget extension.

These are ordinary floating Galerkin outputs, not directed intervals or a
full-Euler tail enclosure. They make no PDE claim. Passing the numerical
agreement and drift subchecks does not promote the packet after the endpoint
threshold fails.

## Zero-leakage unit ideal

The exterior mode

\[
 m=k_7+k_8=(55,34)
\]

has only the contributing pair `{k_7,k_8}`.  Equation (225.2) gives

\[
 B_m={987\over974170}z_7z_8.                        \tag{225.9}
\]

Put

\[
 f=x_7x_8-y_7y_8,\quad
 g=x_7y_8+y_7x_8,
\]

and saturate away `z_7z_8=0` by adjoining

\[
 h=t(x_7^2+y_7^2)(x_8^2+y_8^2)-1.
\]

Over `Q`, grevlex Groebner reduction of `(f,g,h)` is `[1]`.  The exact
certificate is already visible without trusting software output:

\[
 t f^2+t g^2-h=1,                                   \tag{225.10}
\]

because `f^2+g^2=(x_7^2+y_7^2)(x_8^2+y_8^2)`.  Hence
zero first-order exterior leakage forces `z_7z_8=0`, while a nonzero sixth
isolated-triad rate requires `z_7z_8z_6!=0`. The full cancellation ideal is therefore
also the unit ideal after directed-transfer saturation.

## Reproduction

Using the repository's pinned SymPy 1.13.3 installation, run

```sh
PYTHONPATH=.cycle206-sympy python3 \
  millennium-prize/navier-stokes/verify_cycle225_quadratic_leakage.py
```

The command regenerates `cycle225-quadratic-leakage-certificate.json`, checks
the admitted packet over exact rationals, computes the Groebner basis, and
expands the Bezout identity to `1`.

Compile and replay the two frozen floating runs with

```sh
g++ -O3 -march=native -std=c++20 \
  millennium-prize/navier-stokes/cycle225_orbit_screen.cpp \
  -o cycle225_orbit_screen
./cycle225_orbit_screen --n 128 --steps-per-unit 1024 --final-time 8 \
  --output millennium-prize/navier-stokes/cycle225-orbit-N128.json
./cycle225_orbit_screen --n 256 --steps-per-unit 2048 --final-time 8 \
  --output millennium-prize/navier-stokes/cycle225-orbit-N256.json
python3 -m unittest -q \
  millennium-prize/navier-stokes/test_cycle225_orbit_screen.py
```

The committed JSON files preserve the exact floating labels and outputs. The
unit test is a deterministic, reduced-duration harness smoke test; it does not
replace either frozen `T=8` run.
