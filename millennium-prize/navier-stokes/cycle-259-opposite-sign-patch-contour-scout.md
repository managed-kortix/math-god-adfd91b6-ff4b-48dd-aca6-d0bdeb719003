# Cycle 259: bounded opposite-sign patch contour scout

## Verdict and scope

The prescribed weak-signal stop fires. A deterministic 24-member geometry grid
of equal-area, opposite-sign periodic patch pairs was evolved under a numerical
full-contour discretization in both time directions through `|t|=1/2`. At 32
nodes per contour, the largest sampled complete-velocity `L^3` max/min ratio is

\[
 1.008192826706615<1.2.
\]

The leading geometry was repeated at 64 nodes per contour and gave
`1.0044771166846347`. It exhibits a nonzero non-relative shape diagnostic, but
the norm signal is weak and decreases under this refinement. The search stops:
no longer-time run, geometry tuning, or interval enclosure is attempted.

This is numerical candidate generation only. It is not a contour-dynamics
convergence proof, a rigorous Euler patch certificate, a smooth Euler orbit, a
Navier--Stokes transfer, or a Millennium result.

## Frozen geometry grid

Work on `(R/2 pi Z)^2` with normalized Haar measure and patch strength one. For

\[
 a\in\{0.45,0.65\},\quad b/a\in\{0.45,0.70\},\quad
 g\in\{0.15,0.30\},\quad \theta\in\{0,\pi/4,\pi/2\},
\]

put `d=a+g/2` and initialize

\[
 D_+^0=(d,0)+E(a,b),\qquad
 D_-^0=(-d,0)+R_\theta E(a,b),\qquad
 \omega_0=1_{D_+^0}-1_{D_-^0}.
\]

Thus the two patches have exactly opposite circulation in the continuum model.
The Cartesian product has 24 members in Python `itertools.product` order. This
is a bounded scout of the honest two-contour architecture from Cycle 254, not an
ellipse moment closure.

## Numerical protocol

Each boundary is represented by counterclockwise equal-arclength nodes. The
periodic zero-mean Green function is tabulated on a `512^2` grid from Fourier
modes `|k_x|,|k_y|<=96`; bilinear interpolation and midpoint panels evaluate
the contour integral. Classical RK4 uses `dt=2^-7` at 32 nodes and `dt=2^-8`
at 64 nodes, with equal-arclength redistribution after each step. Velocity
`L^3` is evaluated independently from boundary-derived Fourier coefficients on
a `64^2` spatial grid. Samples occur every `1/16`.

The 32-node full-grid result is:

| quantity | value |
|---|---:|
| promotions above `1.2` | `0/24` |
| largest max/min ratio | `1.008192826706615` |
| leading `(a,b/a,g,theta)` | `(0.65,0.45,0.15,pi/4)` |
| minimum node separation | `0.36904758227116524` |
| maximum chord--arc ratio | `2.7140042923579686` |
| maximum relative polygon-area drift | `0.010414842172553729` |
| non-relative shape change | `0.0369692485343065` |

For the leading geometry, the 64-node replay gives ratio
`1.0044771166846347`, minimum node separation `0.3629302648926953`, maximum
chord--arc ratio `2.720195392947783`, relative polygon-area drift
`0.004665520049633498`, and non-relative shape change
`0.03628892039449583`.

The shape diagnostic is the maximum change, after normalization by area, in
either the isoperimetric ratio or the absolute third complex boundary Fourier
mode. Translation and rotation leave both components unchanged. Its nonzero
value therefore rules out merely reporting rigid motion at the discrete level,
but it is not a rigorous lower bound for the continuum patch orbit.

Separation stays positive and the sampled chord--arc ratio stays bounded in
these runs. They are monitors, not a posteriori enclosures. Polygon-area drift
at 32 nodes is about one percent, and the `L^3` variation changes materially at
64 nodes, so the data would be inadequate for promotion even if the ratio were
closer to the threshold.

## Reproduction and artifacts

```text
uv run --with numpy python -m unittest -v test_cycle259_patch_contours.py
uv run --with numpy python scout_cycle259_patch_contours.py --points 32 --dt 0.0078125 --time 0.5 --sample-dt 0.0625 --output cycle259-patch-contours-P32.json
uv run --with numpy python scout_cycle259_patch_contours.py --points 64 --dt 0.00390625 --time 0.5 --sample-dt 0.0625 --indices 13 14 --output cycle259-patch-contours-P64-top.json
```

Record:

`CYCLE259 PATCH CONTOUR SCOUT STOPPED: 0/24 ABOVE 1.2; MAX 1.008192826706615; NUMERICAL ONLY.`
