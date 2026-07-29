# Cycle 85: prime-local sum-of-squares audit

Each Euler factor has an exact causal delay realization. For `a=log p`,
`r=p^(-1/2)`, and the bilateral translation `U_a`, the Poisson operator

\[
K_p=\sum_{n\in\mathbf Z}r^{|n|}U_a^n
\]

is positive, with Fourier multiplier

\[
P_r(a t)={1-r^2\over1-2r\cos(at)+r^2}.
\]

The Weil-sign prime packet is nevertheless

\[
Q_p(f)=\log p\,\langle f,(I-K_p)f\rangle,
\]

and is indefinite. The nonconstant zero-mean multiplier `1-P_r` takes both
signs. Hence no additive prime-local positive-square factorization exists.

The sharp local diagonal needed to repair one packet is

\[
c_p={2\over\sqrt p-1},
\]

for which

\[
c_p\log p\,\|f\|_2^2+Q_p(f)
\]

has an exact translation-resolvent square. But these local repair coefficients
are not summable over the primes and cannot be paid by the fixed archimedean and
pole channels.

Long modulated packets make the obstruction extensive: a negative symbol phase
produces negative energy of order packet length, while local boundary or compact
remainders are subextensive. A viable construction would therefore need
intrinsically cross-prime correlations. If arbitrary single-prime channel tests
are admitted, even cross-prime Gram factors cannot repair the negative diagonal
restriction of a globally positive form.

Adelic conductor/scattering and semi-local Sonin realizations of these local
factors are already known in work of Burnol and Connes--Consani. They produce
positive traces plus sign-indefinite supertrace or compact remainders. Proving
the global remainder positive is the Weil criterion itself.

Thus prime-local SOS is retired: locally it is false, and globally its required
coupled positivity is RH-equivalent. No RH result is claimed.
