# Cycle 276: critical-excursion one-split audit

## Verdict

`CEB-SPLIT-WALL`.

The first unchargeable term is

\[
 {X(\tau)^{1/3}\over4\nu}
 \int_0^\tau \|u(s)\|_4^4\,ds.                       \tag{276.2}
\]

Charging (276.2) to the entire permitted remainder would require the
unavailable scale-sensitive estimate

\[
 \int_0^\tau\|u(s)\|_4^4\,ds
 \le {7\nu\over6}X(\tau)^{2/3}.                       \tag{276.3}
\]

No second amplitude split, data, or frequency decomposition is used below.

## Frozen chain to the wall

Set

\[
 A=X(\tau)^{1/3},\qquad
 E_<(s)=\{x:|u(s,x)|\le A\}.
\]

The strict `CEB` statement must exclude `A=0`: the zero solution would give
`0<0`, not a true inequality. That solution is regular and is handled
separately, so this audit assumes `A>0`. Periodic integration by parts gives the
exact dissipation identity

\[
 \mathcal D(u)=\int_{\mathbb T^3}|u||\nabla u|^2
   +\int_{\mathbb T^3}|u||\nabla|u||^2.              \tag{276.4}
\]

Normalize the pressure to have zero mean. From
`-Delta p=partial_i partial_j(u_i u_j)`, its nonzero Fourier coefficients
satisfy

\[
 \widehat p(k)=-{k_i k_j\over |k|^2}\widehat{u_i u_j}(k).
\]

The matrix `(k_i k_j/|k|^2)_{ij}` has Frobenius norm one. Parseval and
Cauchy--Schwarz therefore retain the explicit constant one:

\[
 \|p\|_2^2
 \le \sum_{i,j}\|u_i u_j\|_2^2
 =\int_{\mathbb T^3}|u|^4
 =\|u\|_4^4.                                           \tag{276.5}
\]

For the low-amplitude part of the pressure work, Young's inequality in the
exact form `ab <= nu a^2+b^2/(4 nu)` yields

\[
\begin{aligned}
 \mathcal P_<(u)
 &=\int_{E_<}p\,u\mathbin\cdot\nabla|u|\\
 &\le \int_{E_<}|p|\sqrt{|u|}
                    \sqrt{|u|}|\nabla|u||\\
 &\le \nu\int_{E_<}|u||\nabla|u||^2
       +{1\over4\nu}\int_{E_<}|p|^2|u|\\
 &\le \nu\mathcal D_<(u)+{A\over4\nu}\|p\|_2^2\\
 &\le \nu\mathcal D_<(u)+{A\over4\nu}\|u\|_4^4 .   \tag{276.6}
\end{aligned}
\]

Here `D_<` denotes the restriction to `E_<` of the two nonnegative
integrands in (276.4). Integrating (276.6) in time produces exactly (276.2).
Even if the full allowance `7X(tau)/24` is assigned to this low-amplitude
term and nothing is reserved for the high-amplitude region, the required
bound is (276.3).

The frozen maximum normalization supplies only
`||u(s)||_3^3 <= X(tau)`. It does not control `||u(s)||_4`: concentration at
fixed `L^3` makes the latter arbitrarily large. The pressure equation gives
the critical estimate `p in L^(3/2)` from `u in L^3`, whereas the weighted
Young remainder in (276.6) requires `p` in weighted `L^2`; (276.5) exposes
the resulting `L^4` demand. Any attempt to recover it from (276.4) introduces
a dissipation-dependent interpolation term and then needs an additional
scale-sensitive spacetime estimate not present among the frozen inputs.

This is a wall rather than a no-go: the chain does not prove that every
possible one-split estimate misses `7/8`. Per the first-failure rule, the
high-amplitude region is not estimated.
