# Cycle 148: simultaneous-chain cross output and the normalization gate

The mirror-free designated chain of Cycle 147 is not remotely closed when all
rails and pumps are populated simultaneously.  In one exact amplitude gauge,
the complete off-circuit convolution grows exponentially.  This does not yet
give an intrinsic cascade obstruction because that gauge has exponentially
growing critical energy and the complete output has collision and phase
cancellation channels.

For depth `L`, populate

\[
S_L=\{\pm q_0,\ldots,\pm q_L,
\pm p_0,\ldots,\pm p_{L-1}\}.
\]

Fix every rail scalar amplitude to one and choose each pump scalar so that its
designated edge produces exactly the next raw polarization vector.  Exact full
convolution gives the following unweighted exterior squared norms:

\[
\begin{array}{c|c|c}
L&\#\operatorname{supp}B_{S_L^c}&
\sum_{k\notin S_L}|B_k|^2\\ \hline
1&4&8.4378750\cdot10^5\\
2&20&4.8302743\cdot10^7\\
3&52&7.2952052\cdot10^8\\
4&96&9.7784133\cdot10^9\\
5&156&1.4727010\cdot10^{11}\\
6&232&2.4263946\cdot10^{12}\\
7&320&4.0503715\cdot10^{13}\\
8&424&6.6595419\cdot10^{14}
\end{array}
\]

The exterior support count in this range is `6L^2+2L-8`, while the squared
norm is empirically of order `16^L`.  Rail--rail cross interactions contribute
more than `99.96%` at depth eight.  Thus killing every designated mirror does
not suppress nonadjacent high-shell sidebands.

There is exact arithmetic structure behind the cross outputs.  Writing

\[
q_n=2^{n+1}(1,1,1)+w_n,
\qquad p_n=2^{n+1}(1,1,1)+w_{n+2},
\]

the correction `w_n` is six-periodic.  This classifies all frequency
collisions.  In particular, gaps congruent to zero or three modulo six create
some same-frequency channels, and three binary-carry identities create further
sum/difference collisions.  All other outputs are arithmetically unique up to
sign.  Exact cancellation must therefore be assessed after coherently summing
vectors at each output frequency; pairwise norm counting is invalid.

The prescribed normalized-polarization symbol has intrinsic edge gain

\[
\kappa_0^2=\frac43,
\qquad
\kappa_n^2=\frac{9(Q_n-2)}{2Q_n-3},
\qquad Q_n=|q_n|^2=12\cdot4^n+2.
\]

Although `kappa_n^2 -> 9/2`, its derivative-scale normalization decays:

\[
\frac{\kappa_n^2}{|q_n|^2}\longrightarrow0.
\]

For critical-energy charges, the intended bilinear gain decays like
`|q_n|^(-1/2)`.  Therefore a unit-critical-energy field cannot maintain a
positive depth-independent intended charge along this particular chain.  The
raw unit-output gauge above pays an increasing energy cost and cannot be used
as a scale-invariant regularity obstruction.

Amplitude hierarchies also face a real but not yet fully certified obstruction:
for two stages,

\[
(x_i y_j)(x_j y_i)=(x_i y_i)(x_j y_j).
\]

Thus reciprocal rescaling can suppress one cross orientation only by amplifying
the reverse orientation.  A complete theorem would need selected output
frequencies that are unique in the full signed convolution and normalized
cross-symbol coefficients uniformly bounded below.  The present work has not
closed those arbitrary-depth uniqueness and coercivity gates, so no exponential
lower bound is claimed.

Recursive completion supplies the decisive warning.  At every fixed chain
length and completion depth, tiny populated correction modes can push output
outside the enlarged support to arbitrarily high order without changing the
designated gains at leading order.  But the forcing on those tiny populated
modes remains order one.  Hence completion defeats exterior-support costs, not
the dynamical relative-rate condition

\[
|\partial_tu_k|\lesssim |u_k|.
\]

The surviving gate is therefore time dependent: prove or refute that a
simultaneous efficient cascade must pay a scale-uniform dwell-time cost because
some small correction mode experiences order-one exact forcing.  Such a cost
must be integrated against viscosity or another finite global budget.  Purely
instantaneous support and cross-output norms are no longer sufficient.

This is a normalization and mechanism gate, not a Navier--Stokes regularity
theorem or blowup construction.
