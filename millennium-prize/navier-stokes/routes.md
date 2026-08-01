# Routes

Cycle 210 promotes the universal factor-two amplification bound for the
mean-zero `L^3` norm of every maximal smooth periodic solution. Together with
endpoint `L^infinity_t L^3_x` continuation, it would imply the periodic
existence alternative. Cycle 211 sharpens the breaker: first certify one smooth
2D Euler orbit with `L^3` amplification greater than two, then transfer it by an
explicit fixed-time inviscid-limit estimate and amplitude scaling to any fixed
positive viscosity. Time reversal permits searching for either growth or decay,
but reversibility or vorticity rearrangement alone is not a counterexample. One
full-PDE certificate refutes the universal lemma; a Galerkin trajectory,
passive-scalar mixer, or floating ratio does not. Exhaustion without a crossing
retires only the tested finite family. See
`../cycle-210-strategic-rotation.md` and
`cycle-211-euler-reversal-breaker.md`. A separate hostile literature audit
finds no known same-norm `L^3` falsifier or scaling contradiction; weaker
critical-space norm inflation does not transfer. See
`cycle-211-hostile-l3-literature-audit.md`.

Cycle 212 audits the standard analytic mechanisms. The velocity `L^3`
differential inequality is critical in 3D, the 3D endpoint Duhamel kernel is
nonintegrable, and 2D vorticity contraction gives only a data-dependent
Biot--Savart constant. In 2D the heat--Duhamel estimate does certify a local
factor-two interval of size `nu^5/(24 K_2||u_0||_3)^6`, after fixing a periodic
heat--Leray constant. The Cycle 211 Euler inverse-transfer breaker remains the
preferred falsifier route. See `cycle-212-l3-bound-mechanisms.md`.

Cycle 213 replaces the proxy-only finite-family shortlist by reduced-resolution
integration of all 152586 nonlinear canonical rows. Its declared floating
pipeline has maximum `1.0132639341307961`; this is explicitly not an interval
claim. See `cycle-213-finite-family-screen.md`.

Cycle 214 replaces the frozen integer family by continuous optimization of a
low-mode Fourier box and terminal time. A discrete automatic-gradient midpoint
solver screens random seeds at `N=32`, promotes endpoint ratios above `1.2` to
`N=64`, and records any floating ratio above two. This remains candidate
generation only. See `cycle-214-gradient-screen.md`.

Cycle 216 gives the hostile bound for a finite sequential inverse cascade.
Conserved energy `E` and enstrophy `Z`, together with two-dimensional
Gagliardo--Nirenberg, imply the orbitwise ratio bound
`||u(t)||_3/||u(0)||_3<=C_T(Z/(kappa_0^2E))^(1/6)`. Initial Fourier support
below `K_+` therefore gives `C_T(K_+/kappa_0)^(1/3)`, with a stable
enstrophy-leakage version. This rules out unbounded amplification at a fixed
launch band and rules out a factor-two crossing whenever the displayed constant
is at most two. It does not give a launch-scale-independent factor two, so a
coupled high-enstrophy Euler crossing remains open. See
`cycle-216-sequential-inverse-cascade-no-go.md`.

Cycle 224 freezes a deterministic eight-frequency Fibonacci packet with six
exact phase-aligned inverse-transfer triads. Exact full-convolution bookkeeping
finds 60 exterior modes and a squared velocity-forcing leakage/intended ratio
about `771.56`, so the packet fails the declared `1/16` structural admission
gate before numerical integration. The reusable output is the finite
admission/failure criterion, not an `L^3` crossing. See
`cycle-224-deterministic-fibonacci-packet.md`.
