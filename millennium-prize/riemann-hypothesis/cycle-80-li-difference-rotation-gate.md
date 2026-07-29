# Cycle 80: Li-difference rotation gate

The finite theorem

\[
\lambda_{n+1}-\lambda_n>0\qquad(1\le n\le10000)
\]

has been certified by outward-rounded Arb computation. It remains finite.

The exact Laplace transform of the prime-error kernel is

\[
\int_0^\infty e^{-st}[L_n(t)-L_n'(t)]dt
=1-\left({s-1\over s}\right)^{n+1}.
\]

Its real part is a square on `Re(s)=1/2`, but the original prime-error pairing
lives on the wrong spectral line. First differencing leaves the phase-indefinite
kernel `((s-1)/s)^n/s`. Thus the square does not sign the Li differences.

Laguerre recurrence gives an exact forced discrete wave equation, but each
attempt to control its forcing introduces the next signed prime moment. No
finite moment energy closes. Selberg symmetry also leaves a signed adjoint
kernel; separating its positive convolution destroys convergence, and the
elementary `O(x)` remainder is not absolutely transformable.

Therefore the positive-square, recurrence, and Selberg mechanisms are retired.
Strict Li monotonicity remains a stronger RH-sufficient conjecture, but no
independent uniform lemma survives. No RH result is claimed.
