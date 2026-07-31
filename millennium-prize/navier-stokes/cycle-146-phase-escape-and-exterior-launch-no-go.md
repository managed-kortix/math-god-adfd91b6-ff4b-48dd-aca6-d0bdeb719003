# Cycle 146: positive critical production does not coerce exterior launch

The proposed phase-escape mechanism is false even on one fixed ten-mode
support.  Positive order-one critical production can coexist with arbitrarily
small nonlinear output outside the occupied support, while the active triad
phase remains exactly locked.

For a finite symmetric support `S`, define

\[
E_S=\sum_{n\in S}|n||u_n|^2,
\qquad
\Phi_S=2\sum_{n\in S}|n|\operatorname{Re}
(\overline{u_n}\cdot B_n(u,u)),
\]

and

\[
I_S=\sum_{n\in S}|n||B_n(u,u)|^2,
\qquad
\Lambda_S=\sum_{n\notin S}|n||B_n(u,u)|^2.
\]

The exact real-Hilbert-space identity is

\[
4E_SI_S-\Phi_S^2
=4E_S\left\|\mathbf1_SB(u,u)-\frac{\Phi_S}{2E_S}u
\right\|_{\dot H^{1/2},\mathbf R}^2.
\]

Hence the sharp unconditional estimate is

\[
\boxed{\Phi_S^2\le4E_SI_S}.
\]

It controls the internal nonlinear output, not exterior launch.  There is no
general comparison of `I_S` with `Lambda_S`.

For the Cycle 113 six-mode packet, adjoin its four exact first-generation
launch modes with amplitude `epsilon`; call the resulting fixed ten-mode field
`U^epsilon`.  Exact convolution gives

\[
E_S(U^\epsilon)=8+6\sqrt2+\frac{44\sqrt5}{5}\epsilon^2,
\]

\[
\Phi_S(U^\epsilon)=8(\sqrt2-1)
+\frac{-16-72\sqrt2+88\sqrt5}{5}\epsilon,
\]

and

\[
\Lambda_S(U^\epsilon)=A\epsilon^2+B\epsilon^4,
\]

where

\[
A=\frac{416}{5}+\frac{1728\sqrt2}{25}
+\frac{1252\sqrt{10}}{125}+\frac{2168\sqrt{13}}{325}>0,
\qquad B=\frac{288\sqrt2}{25}>0.
\]

After exact critical-energy normalization, one still has

\[
E_S=1,
\qquad \Phi_S\longrightarrow
\frac{8(\sqrt2-1)}{(8+6\sqrt2)^{3/2}}>0,
\qquad \Lambda_S\longrightarrow0.
\]

Therefore, on the same fixed support,

\[
\boxed{
\frac{\Phi_S^2}{E_S\Lambda_S}\longrightarrow\infty.
}
\]

No universal constant can satisfy

\[
\Phi_S^2\le C E_S\Lambda_S.
\]

The packet remains in the invariant parity class in which Fourier coefficients
are real when `n_1+n_2` is odd and imaginary when it is even.  Its active triad
scalar remains purely imaginary, with maximizing phase exactly `pi/2`.
Consequently small exterior launch does not force phase escape.

Recursive completion strengthens the obstruction.  For every fixed depth `r`,
one can adjoin the first `r` generated shells with amplitudes
`1,epsilon,...,epsilon^r`; after normalization,

\[
E_S=1,
\qquad\Phi_S\to c_*>0,
\qquad\Lambda_S=O_r(\epsilon^{2r}).
\]

Thus every finite-depth leakage or phase tax can be defeated to arbitrarily
high prescribed algebraic order.

There is also a clean support classification.  A finite symmetric nonzero
Fourier support is universally closed under the divergence-free Euler
bilinear map if and only if all its frequencies are collinear.  On such a
support the nonlinearity vanishes, so positive production excludes universal
closure.  This qualitative statement gives no quantitative leakage: a
particular polarization can approach the exterior-zero algebraic variety to
arbitrarily high order.

The surviving theorem-scale target is therefore not local phase escape.  It is
an all-depth obstruction to a scale-uniform cascade circuit for the exact
unaveraged Leray symbol: a proof that sufficiently many consecutive efficient
transfers force comparable backscatter, irreversible off-circuit output, or a
viscosity-sized dwell-time payment.  Such a result must survive recursive
completion and fail for Tao's averaged bilinear operator.  No such theorem is
currently established.

The exact packet and recursive calculations are reproduced by

```sh
python3 millennium-prize/navier-stokes/verify_cycle125_completed_star.py
python3 millennium-prize/navier-stokes/verify_cycle129_recursive_completion.py
```

This is a finite-Fourier no-go for exterior-launch and local phase-escape
coercivity.  It is not a Navier--Stokes regularity theorem or a blowup result.
