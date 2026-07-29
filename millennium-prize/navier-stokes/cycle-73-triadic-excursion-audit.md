# Cycle 73: three-dimensional triads and excursion no-go

## Exact helical stretching formula

On the `2pi`-periodic torus, expand a real divergence-free velocity in helical
modes `h_s(k)` satisfying

\[
ik\times h_s(k)=s|k|h_s(k).
\]

For

\[
S=\int(\omega\cdot\nabla)u\cdot\omega\,dx,
\]

the exact ordered-triad formula is

\[
\boxed{
S=(2\pi)^3\sum_{k+p+q=0}\sum_{a,b,c=\pm1}
iac|k||q|u_a(k)u_b(p)u_c(q)
[p\cdot h_a(k)][h_b(p)\cdot h_c(q)].}              \tag{73.1}
\]

Opposite triads are conjugate, making the total real. Neither homochiral nor
heterochiral triads have a fixed sign. Local frequency interactions have
coefficient scale `N^3`; separated interactions are necessarily high--high--low
and have natural scale `H^2L`.

## Explicit hostile integer triad

There is exact divergence-free periodic data supported on the triad

\[
(1,0,0),\quad(0,1,1),\quad(-1,-1,-1)
\]

with integer amplitudes `(12,6,3)` such that, in normalized-torus convention,

\[
\boxed{Y=\|\omega\|_2^2=540,\qquad
Z=\|\nabla\omega\|_2^2=900,
\qquad S=864.}                                      \tag{73.2}
\]

Amplitude scaling makes `S/(nu Z)` arbitrarily large. Integer Navier--Stokes
scaling on the fixed torus also rules out absolute scale-independent excursion
caps or persistence times independent of frequency.

## Separated estimate and structural failure

Paraproduct estimates give, uniformly in cutoff,

\[
|S_{sep}|\lesssim Y^{3/4}Z^{3/4}.                  \tag{73.3}
\]

On a first enstrophy-doubling interval, energy dissipation and Young's inequality
yield a remainder of order

\[
{K_0Y_*^2\over\nu^4}.                               \tag{73.4}
\]

This grows quadratically with the starting enstrophy, while a doubling requires
only linear payment. It becomes weaker at high enstrophy and cannot contradict
a cascade.

The standard differential inequality

\[
Y'\lesssim\nu^{-3}Y^3
\]

forces only a passage time of order `nu^3/Y^2`. The kinetic-energy cost of
successive dyadic passages is then of order `nu^3/Y`; these costs form a
convergent geometric series. A Zeno cascade can therefore reach unbounded
enstrophy in finite total time without contradicting this excursion accounting.

The enstrophy-excursion tactic is consequently retired. Retuning constants does
not fix either the superlinear remainder or summable cascade times.

## Corrected Navier bottleneck

The official periodic regularity alternative follows from

\[
\sup_{t<T_*}\|u(t)\|_{L^3}<\infty,                  \tag{73.5}
\]

by the endpoint `L^infinity_t L^3_x` continuation theorem. A viable frequency
route must therefore be scaling-critical and cancellation-preserving across all
shells, with summable control of high--high backscatter and leakage. Isolated
triad or enstrophy budgets are insufficient.

This cycle supplies an exact three-dimensional formula and decisive tactic
falsification, not a Navier--Stokes regularity result.
