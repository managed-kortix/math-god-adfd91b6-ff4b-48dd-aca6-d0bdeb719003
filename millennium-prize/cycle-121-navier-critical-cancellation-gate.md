# Cycle 121: Navier critical-passage cancellation gate

The proposed completed-passage tax is not promoted.  A full Fourier packet can
simultaneously transfer energy from low shells upward and from high shells
downward while canceling the signed critical quadratic derivative exactly.

Use positive representatives and rational divergence-free polarizations

\[
\begin{array}{c|c}
k=(3,0,0)&u_k=(0,-2,-2)\\
p=(0,4,0)&u_p=(-2,0,-2)\\
q=(3,4,0)&u_q=i(4,-3,-2)\\
h=(-6,4,12)&u_h=(-6,-9,0)/252\\
j=(9,0,-12)&u_j=(4,-3,3).
\end{array}
\]

The active triads are `k+p=q` and `h+j=q`, with radii `3,4,5` and `14,15,5`.
For conjugate-pair energies, their exact nonlinear initial rates combine to

\[
(\dot E_k,\dot E_p,\dot E_q,\dot E_h,\dot E_j)
=(-48,-64,898/7,-20/7,-94/7).
\]

Ordinary energy cancels.  The forward triad contributes `+160` to the signed
`H^(1/2)` derivative and the high-to-middle triad contributes `-160`; hence

\[
 \left.\frac d{dt}\|u\|_{\dot H^{1/2}}^2\right|_{NL,t=0}=0.
\]

Other full-equation Fourier modes are launched but begin with zero energy, so
they do not alter this first derivative.  This gives exact dynamic first-order
realization of the cross-scale cancellation that a local tagged no-return
condition misses.  It does not prove persistence of no return.

More abstractly, the exact shell identity

\[
 \int\sum_j2^j\Pi_j
 =H^{dyad}_{1/2}(b)-H^{dyad}_{1/2}(a)
 +\nu\int\sum_j2^jD_j
\]

telescopes but is signed.  Its positive variation charges passages but has no
known finite budget.  Exact shell-balance trajectories can undergo infinitely
many fixed critical increments in finite time with geometrically summable
kinetic dissipation and no backscatter.  Therefore energy balance, shell
localization, and a retained/dissipated/returned trichotomy cannot prove an
additive obstruction without a new Navier-specific coercive fact.

The alternative associahedral tree proposal also fails promotion.  Explicit
low-order Leray products have surviving Catalan bracketings, no associative or
pre-Lie cancellation, and balanced trees receive only exponential rather than
factorial damping in known Duhamel estimates.  The resulting series retains the
standard small-critical-data radius.

No regularity or Millennium result is claimed.
