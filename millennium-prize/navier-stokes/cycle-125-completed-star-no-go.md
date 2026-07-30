# Cycle 125: completed triad-star leakage no-go

A complete first-generation Fourier star can carry order-one critical
production while its remaining exterior leakage tends to zero.  Therefore no
universal coercive inequality can bound critical flux by completed-star leakage.

Start with the exact Cycle 113 core

\[
k=(1,0,0),\quad p=(0,1,0),\quad q=(1,1,0),
\]

\[
u_k=(0,1,1),\quad u_p=(1,0,1),\quad
u_q=-i(1,-1,1),
\]

and their conjugates.  Add its four first-generation launch modes to the
support, with coefficient `epsilon` times their exact launch vectors:

\[
v_{(1,2,0)}=(-2/5,1/5,0),\qquad
v_{(2,1,0)}=(-1/5,2/5,-2),
\]

and `v_(-n)=v_n`.  Leakage is measured outside this completed ten-mode support.

For the full ordered-pair Euler convolution, define

\[
E_{1/2}=\sum_n|n||u_n|^2,
\]

\[
\Phi_{1/2}=2\sum_n|n|\operatorname{Re}
 (\overline{u_n}\cdot B_n(u,u)),
\]

and

\[
\Lambda_{1/2}=\sum_{n\notin S}|n||B_n(u,u)|^2.
\]

Exact reconstruction gives

\[
E_{1/2}(\epsilon)
=8+6\sqrt2+\frac{44\sqrt5}{5}\epsilon^2,
\]

\[
\Phi_{1/2}(\epsilon)
=8(\sqrt2-1)
+\frac{-16-72\sqrt2+88\sqrt5}{5}\epsilon,
\]

and

\[
\Lambda_{1/2}(\epsilon)=A\epsilon^2+B\epsilon^4,
\]

where

\[
A=\frac{416}{5}+\frac{1728\sqrt2}{25}
+\frac{1252\sqrt{10}}{125}+\frac{2168\sqrt{13}}{325}>0,
\qquad
B=\frac{288\sqrt2}{25}>0.
\]

Consequently

\[
\frac{\Phi_{1/2}(\epsilon)^2}
{E_{1/2}(\epsilon)\Lambda_{1/2}(\epsilon)}
\sim
\frac{64(\sqrt2-1)^2}{(8+6\sqrt2)A}\epsilon^{-2}
\longrightarrow\infty.
\]

Thus no finite universal constant `C` can satisfy

\[
\Phi_{1/2}^2\le C E_{1/2}\Lambda_{1/2}
\]

for all complete rational Fourier stars.  Replacing the signed quantity by a
positive star flux only strengthens the failed inference on this family.

The support additions are not dynamically inert: they alter internal nonlinear
velocities at order `epsilon`.  The verifier includes these corrections.  The
family is not a closed invariant subsystem, and the result does not establish
long-time phase locking, singularity formation, or failure of regularity.  It
only retires leakage-by-itself as a universal coercive mechanism.

Reproduce with

```sh
python3 millennium-prize/navier-stokes/verify_cycle125_completed_star.py
```

No Navier--Stokes or Millennium solution is claimed.
