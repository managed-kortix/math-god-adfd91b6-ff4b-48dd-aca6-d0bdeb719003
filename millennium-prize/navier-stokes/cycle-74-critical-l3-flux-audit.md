# Cycle 74: critical `L^3` frequency-flux audit

Let `u_j=Delta_j u` and `a_j=||u_j||_3`. A localized mild estimate has the
scaling-critical form

\[
a_j(t)\lesssim e^{-c\nu2^{2j}t}a_j(0)
+\int_0^t2^{2j}e^{-c\nu2^{2j}(t-s)}
[a_j^*L_j(a)+Q_j(a)](s)\,ds,
\]

where

\[
L_j(a)=\sum_{k\le j-C}2^{k-j}a_k,
\qquad Q_j(a)=\sum_{k\ge j-C}(a_k^*)^2.
\]

The kernel has `L^1` norm comparable to `1/nu`, uniformly in shell location.
Smooth periodic initial data belongs to `ell^2_jL^3_x`, but `Q` does not map
`ell^2` uniformly to `ell^2`: one nonzero shell at index `N` makes `Q_j`
constant on every lower shell and creates a `sqrt(N)` loss.

For output `xi=eta+zeta`, divergence-free input gives

\[
\widehat{\mathbb P(u\cdot\nabla v)}(\xi)
=iP(\xi)[\widehat u(\eta)\cdot\xi]\widehat v(\zeta).
\]

For high--high to low interactions this has size `2^j`, an exact gain
`2^(j-k)` relative to the raw input derivative. The gain is fully consumed in
replacing the derivative by the low output frequency. Opposing high waves
saturate it, and many shells can add coherently into one fixed low mode.

Low-frequency transport cancels in the shellwise `L^3` pairing, but pressure is
exactly a Leray commutator:

\[
\int\mathbb P(a\cdot\nabla v)\cdot|v|v
=\int[\mathbb P,a\cdot\nabla]v\cdot|v|v.
\]

Literal pressure cancellation fails because `|v|v` is not divergence-free.
High--high pressure remains part of projected backscatter.

The proposed envelope is a `B^0_(3,2)` condition stronger than `L^3`; its
propagation is exactly the unresolved flux problem. This tactic is retired. A
viable route needs new depletion or spacetime cancellation for coherent
high--high backscatter. No Navier--Stokes result is claimed.
