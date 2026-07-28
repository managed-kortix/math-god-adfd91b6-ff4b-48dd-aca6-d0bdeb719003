# Cycle 69: RH-conditional audit of the exact logarithmic taper

## Exact family and Mellin representation

Let

\[
V_N(s)=\sum_{a\le N}\mu(a)
\left(1-\frac{\log a}{\log N}\right)a^{-s},
\]

where the `a=N` coefficient is zero, and

\[
F_N(x)=\mathbf1_{(0,1)}(x)+
\sum_{a\le N}\mu(a)
\left(1-\frac{\log a}{\log N}\right)
\left\{\frac1{ax}\right\}.
\]

The complete Nyman--Beurling energy is

\[
\boxed{
\mathcal P_N={1\over2\pi}\int_{-\infty}^{\infty}
\left|1-\zeta(\tfrac12+it)V_N(\tfrac12+it)\right|^2
{dt\over\tfrac14+t^2}.}                            \tag{69.1}
\]

For the repository restricted energy `P_N=integral_(0,1)|F_N|^2`, put

\[
A_N=V_N(1).
\]

Since `F_N(x)=A_N/x` for `x>1`,

\[
\boxed{\mathcal P_N=P_N+A_N^2.}                    \tag{69.2}
\]

Classically,

\[
A_N={1\over\log N}+o(1/\log N),
\]

so full and restricted energies have the same first-order `1/log N` behavior,
but their second-order coefficients differ by one.

On `(0,1)`, the exact Mellin transform contains the tail correction

\[
\int_0^1F_N(x)x^{s-1}dx
={1-\zeta(s)V_N(s)\over s}+{V_N(1)\over s-1};        \tag{69.3}
\]

the apparent pole at `s=1` cancels. Equation (69.1) corresponds to the complete
`(0,infinity)` convention.

## Published conditional theorem

Bettin--Conrey--Farmer prove for this exact taper that

\[
\boxed{
\mathrm{RH}+J_{-1}(T)\ll T^{3/2-\delta}
\Longrightarrow
\mathcal P_N\sim {C_0\over\log N},}                 \tag{69.4}
\]

where

\[
J_{-1}(T)=\sum_{|\Im\rho|\le T}{1\over|\zeta'(\rho)|^2},
\qquad
C_0=2+\gamma-\log(4\pi).
\]

The reciprocal-derivative hypothesis implies simplicity and adds substantial
information not supplied by RH. By (69.2), the same first-order asymptotic holds
for `P_N`.

Primary source: S. Bettin, J. B. Conrey, and D. W. Farmer, *An optimal choice of
Dirichlet polynomials for the Nyman--Beurling criterion*, Theorem 1,
arXiv:1211.5191; Proc. Steklov Inst. Math. 280 Suppl. 2 (2013), 30--36.

## What RH alone does and does not give

No theorem is currently known that RH alone implies

\[
P_N\to0
\quad\text{or}\quad
P_N=O(1/\log N)                                     \tag{69.5}
\]

for this fixed logarithmic taper. RH is equivalent to convergence of suitable
integer-dilation approximants and gives bounds for the optimal distance or for
other dampings, but does not select this exact coefficient family.

The optimal-distance lower bound of Báez-Duarte--Balazard--Landreau--Saias and
Burnol implies, for every particular admissible approximant,

\[
\boxed{
\liminf_{N\to\infty}P_N\log N
\ge C_B:=\sum_{\rho\ distinct}{m(\rho)^2\over|\rho|^2}}           \tag{69.6}
\]

under RH, up to the lower-order full/restricted tail. Thus, if this taper
converges, it cannot generally beat the `1/log N` energy scale. Under simplicity
`C_B=C_0`.

## Exact contour obstruction

The triangular weight has the Perron representation

\[
\boxed{
V_N(s)={1\over2\pi i\log N}
\int_{c-i\infty}^{c+i\infty}
{N^w\over w^2\zeta(s+w)}dw.}                       \tag{69.7}
\]

Shifting left crosses `w=rho-s`. At a simple zero the residue is

\[
{N^{\rho-s}\over\log N\,(\rho-s)^2\zeta'(\rho)}.  \tag{69.8}
\]

Multiple zeros produce higher principal parts and polynomials in `log N`.
RH controls the real parts of these poles, not reciprocal derivatives, zero
multiplicities, or the resulting quadratic zero correlations. Ordinary shifted-
line bounds for `1/zeta` do not control the critical-line residue channel.

Consequently the proposed calibration

\[
\mathrm{RH}\Longrightarrow P_N\to0
\]

is itself an open fixed-approximant problem. This means the previous
additive-12 target was not merely technically difficult; it attempted a strong
property of a taper whose RH-conditional convergence is not known.

## Strategic conclusion

The exact logarithmic-taper funnel is retired as the main RH route pending new
control of reciprocal-zeta derivative moments or an independent fixed-family
convergence theorem. Its finite certificates and exact identities remain useful
calibrations.

The Millennium main funnel should now rotate to a different problem/route under
the program gate, rather than continuing to repackage this unresolved
zero-correlation input. No RH result is claimed.
