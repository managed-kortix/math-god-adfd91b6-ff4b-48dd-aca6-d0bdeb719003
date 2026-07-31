# Cycle 150: coherent heat resonance still has vanishing scale charge

Navier--Stokes has no linear dispersive phase.  Viscosity and pressure do not
rotate a triad forcing: all interaction-frame phase motion comes from
neighboring nonlinear interactions.  Nevertheless, absence of dispersion does
not produce a scale-uniform heat-filtered cascade charge.

For each integer `N`, take

\[
q_0=N(1,0,0),\quad p_0=N(0,1,0),\quad q_1=N(1,1,0),
\]

\[
p_1=N(0,0,1),\quad q_2=N(1,1,1),
\]

with divergence-free polarizations

\[
a=(0,1,1),\qquad b=(1,0,1),\qquad c=(1,-1,0).
\]

For the symmetrized Leray symbol,

\[
\mathcal S_{q_0,p_0}(a,b)=N(0,0,2)=Nf,
\]

and

\[
\mathcal S_{q_1,p_1}(f,c)=N(2,-2,0)=Nh.
\]

The output-frequency-normalized edge symbols are `1/sqrt(2)` and
`1/sqrt(3)`, independently of `N`.  The two alternative positive-source
bracketings vanish exactly after Leray projection, and signed source modes
cannot sum to `q_2`; hence this is the complete real full convolution at the
relevant Picard order.

All three source modes decay at rate `nu N^2`.  The first generated parent is
exactly heat-resonant:

\[
u_{q_1}^{(2)}(t)=-iNt e^{-2\nu N^2t}f.
\]

The exact terminal second-generation term is

\[
\boxed{
u_{q_2}^{(3)}(t)=-N^2t^2e^{-3\nu N^2t}(1,-1,0).
}
\]

There is no oscillatory or vector cancellation.  Over one parent viscous
lifetime

\[
T_N=\frac1{2\nu N^2},
\]

the terminal heat-budget charge is

\[
\boxed{
\int_0^{T_N}\nu|q_2|^2|u_{q_2}^{(3)}(t)|^2dt
=\frac{1}{54\nu^4N^4}
\left(1-\frac{131}{8}e^{-3}\right).
}
\]

It is positive for every `N` but tends to zero like `N^-4`.  Thus two coherent,
exactly heat-resonant, uniformly nondegenerate symbol edges do not force a
scale-uniform Duhamel payment.  The failure is amplitude/critical normalization,
not temporal phase cancellation.

The exact phase equation confirms the structural scope.  For one triad forcing
`F=B_k(u_p,u_q)`,

\[
\dot{\arg}F=
\frac{\operatorname{Im}\left[F^*\cdot
(B_k(N_p,u_q)+B_k(u_p,N_q))\right]}{|F|^2}.
\]

The viscous contribution is a real multiple of `F` and drops out.  There is no
systematic linear `N^2` phase rotation, but the nonlinear ratio has no energy-
level bound near modal or interaction zeros.  A conditional coherence estimate
requires control of source relative derivatives, which is precisely the
uncontrolled temporal-action quantity from Cycle 149.

This bounded counterexample closes nondispersive temporal coherence based only
on nonzero normalized edge symbols.  Any surviving mechanism must incorporate
an intrinsic critical-throughput amplitude lower bound; obtaining such a bound
uniformly is already at the regularity frontier.  The Navier cascade funnel is
therefore rotated after this checkpoint.

Reproduce the algebra with

```sh
python3 millennium-prize/navier-stokes/verify_cycle150_two_stage_heat_cascade.py
```

This is a two-stage Picard no-go, not a Navier--Stokes regularity theorem or
blowup construction.
