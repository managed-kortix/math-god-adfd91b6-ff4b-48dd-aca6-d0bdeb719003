# Cycle 129: every finite-depth leakage completion fails coercivity

The Cycle 125 completed-star construction extends to arbitrary fixed finite
depth.  One can absorb successive coefficients of the exterior Euler
convolution while retaining the original order-one critical production.  Thus
no universal estimate can control critical flux solely by leakage outside any
fixed finite coefficient-completed support.

Let `B` be the full ordered-pair Euler convolution.  Start from the six-mode
Cycle 113 packet `V_0`, with support `S_0`.  Recursively define

\[
Q_j=\sum_{a+b=j}B(V_a,V_b),
\]

\[
V_{j+1}=\mathbf1_{S_j^c}Q_j,
\qquad
S_{j+1}=S_j\cup\operatorname{supp}V_{j+1}.
\]

For fixed `r`, put

\[
U_r^\epsilon=\sum_{j=0}^r\epsilon^jV_j.
\]

Every generation has finite support, is divergence-free, satisfies Fourier
reality, and is disjoint from all earlier generations.  Expanding,

\[
B(U_r^\epsilon,U_r^\epsilon)
=\sum_{m=0}^{2r}\epsilon^m
\sum_{\substack{a+b=m\\0\le a,b\le r}}B(V_a,V_b).
\]

For every `m<r`, the coefficient is supported in `S_(m+1)`, hence in `S_r`.
Therefore

\[
\mathbf1_{S_r^c}B(U_r^\epsilon,U_r^\epsilon)
=\epsilon^rV_{r+1}+O(\epsilon^{r+1}).
\]

Consequently the exterior weighted leakage obeys

\[
\Lambda_{1/2,r}(U_r^\epsilon)=O_r(\epsilon^{2r}).
\]

If `V_(r+1)` is nonzero, its leading coefficient is exactly

\[
\epsilon^{2r}\|V_{r+1}\|_{\dot H^{1/2}}^2.
\]

Disjoint supports also give

\[
E_{1/2}(U_r^\epsilon)
=E_{1/2}(V_0)+O_r(\epsilon^2)
=8+6\sqrt2+O_r(\epsilon^2),
\]

while the critical production satisfies

\[
\Phi_{1/2}(U_r^\epsilon)
=\Phi_{1/2}(V_0)+O_r(\epsilon)
=8(\sqrt2-1)+O_r(\epsilon).
\]

Hence, for every fixed finite `r`,

\[
\frac{\Phi_{1/2}(U_r^\epsilon)^2}
{E_{1/2}(U_r^\epsilon)\Lambda_{1/2,r}(U_r^\epsilon)}
\gtrsim_r\epsilon^{-2r}\longrightarrow\infty
\]

whenever the leakage is nonzero; identically zero leakage would be an even
stronger obstruction.

The exact verifier recursively computes through depth three.  It finds

```text
generation sizes: 6, 4, 14, 24
cumulative sizes: 6, 10, 24, 48
first exterior order after S_3: epsilon^3
leading leak support size: 28
```

and checks all convolution coefficients, reality, incompressibility, support
disjointness, and exact rational radial norm groups.

This is an instantaneous finite-Fourier theorem.  It does not describe an
invariant subsystem or long-time solution, and it does not rule out infinite-
generation, time-integrated, viscous, or support-geometry-dependent mechanisms.
It rules out leakage outside a fixed finite completed support as a universal
coercive defect.

Reproduce with

```sh
python3 millennium-prize/navier-stokes/verify_cycle129_recursive_completion.py
```

No Navier--Stokes or Millennium solution is claimed.
