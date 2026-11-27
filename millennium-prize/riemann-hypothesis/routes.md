# Routes

## Active route: explicit discrete Nyman--Beurling approximants

For `N >= 3`, put

\[
c_a=\mu(a)\frac{\log(N/a)}{\log N},\qquad
F_N(x)=1_{(0,1)}(x)+\sum_{a\le N}c_a\{1/(ax)\}.
\]

Candidate lemma: there are absolute `C,N0` such that

\[
 \|F_N\|_{L^2(0,\infty)}^2\le C/\log N\quad(N\ge N_0).
\]

By Báez-Duarte's discrete Nyman--Beurling criterion this implies RH. The route
is knowingly RH-strength. The proof may not use critical-line convergence of
`sum mu(n)n^-s`, an RH-level Mertens bound, or an RH-conditional mollifier
estimate.

Primary route references: Báez-Duarte, arXiv:math/0202141 and
arXiv:math/0205003; Burnol, arXiv:math/0103058; Bettin--Conrey--Farmer,
arXiv:1211.5191.

## Current Cycle 45 gate: physical Möbius anti-cancellation

Fix a nondegenerate compact interval `I` with \(I\Subset(0,2)\), and put

\[
 \mathcal D_a=\{1\le d<2a:\mu(d)^2=1\},\qquad
 S_a(I)=\{q\in\mathcal D_a:q/a\in I\}.
\]

For \(q\in S_a(I)\), define the rectangular unsigned matrix and its normal
trace by

\[
 (M_a)_{q0}=\beta_a(q),\qquad
 (M_a)_{qd}=W_a(q,d)\quad(d\in\mathcal D_a),\qquad
 \Delta_a(I)=\|M_a\|_F^2.
\]

The accepted dossier `moving-gram-kernel-audit-2026-11-25.md` establishes the
following bulk sign-stripped geometry. It proves the locally uniform bulk kernel

\[
 a\log(a)W_a(q,r)\longrightarrow
 K_\theta(q/a,r/a),
 \qquad K_\theta(u,v)=
 \frac{\log(2/\max(1,u,v))}{2(1-\theta)}J(u,v),
\]

the squarefree-measure bulk trace, the normal-diagonal normalization
`log(a)^2 Delta_a(I) -> A_(theta,I)>0`, and an explicit continuum lower
spectral tail. None of these statements controls the selected Möbius vector.

The exact remaining quantity is

\[
 D_a(I)=\|M_ax_a\|_2^2,\qquad
 x_a=(1,(\mu(d))_{d\in\mathcal D_a}),
\]

and the next theorem sought is

\[
 \liminf_{a\to\infty}
 \log(a)\frac{D_a(I)}{\Delta_a(I)}>0.
\]

Equivalently, with

\[
 A_{de}^{(a,I)}=\sum_{q\in S_a(I)}W_a(q,d)W_a(q,e),\qquad
 r_d^{(a,I)}=\sum_{q\in S_a(I)}\beta_a(q)W_a(q,d),
\]

one must prove, for some `kappa>0` and all sufficiently large `a`,

\[
 2\sum_{d\in\mathcal D_a}\mu(d)r_d^{(a,I)}
 +\sum_{\substack{d,e\in\mathcal D_a\\d\ne e}}
  \mu(d)\mu(e)A_{de}^{(a,I)}
 \ge-\Delta_a(I)+\frac{\kappa}{\log^3a}.
\]

Generic positivity, positive entries, continuum spectral noncompression, and
normal-diagonal mass alone do not imply this estimate. Literal self-pairs are
`o(log^-3 a)`, while the canonical gcd factorization merely leaves an
uncontrolled four-factor Möbius sign. Cycle 46 proves exact finite-prime
inclusion-exclusion grouping and a grouped continuum normalizer, but the
physical vector is unchanged, a certified finite grouped diagonal is
nonmonotone under adjoining primes, and an extreme primorial moves all
unresolved cancellation into one column. It also isolates the initial
non-wrapped interval of every temporal row as an exact
Chebyshev/reciprocal-Möbius expression. For a certified physical row at
`a=512,q=742`, only `0.0265234%` of the initial-block energy remains, with
ratio `hat_c(q)^2/P(q)^2=0.0002652341...`. Therefore no universal finite
pointwise rule can retain a grouped diagonal, initial-block square, or
initial-plus-tail diagonal without its signed cross term. See
`cycle-46-finite-prime-grouping-and-initial-block-audit.md`.

Every fixed finite old family, and only the explicit endpoint layers

\[
 d\le a^{1/2-\varepsilon},\qquad
 2a-a^{3/4-\varepsilon}\le d<2a
 \quad(0<\varepsilon<1/2),
\]

are removed at `o(log^-3/2 a)` in norm; no `o(log^-3 a)` energy removal follows
without an independent upper bound. The estimate above remains open.

Cycle 47 gives two stronger sufficient projection checkpoints.  With the exact
Cycle 46 split `hat_c=P_a+T_a`, define

\[
 \mathcal Q_a(I)=
 \frac{|\langle P_a,\widehat{\mathbf c}_a\rangle|^2}{\|P_a\|^2}
\]

when `P_a` is nonzero, and zero otherwise.  Then
`D_a(I)>=mathcal Q_a(I)`.  Thus `||P_a||^2>>log(a)^-3` and

\[
 \left|1+\frac{\langle P_a,T_a\rangle}{\|P_a\|^2}\right|
 \ge\varepsilon
\]

give the lower bound with constant `epsilon^2`, not `epsilon`.  On the fixed
interval `I0=[1,3/2]`, the exact complete-prefix identity further decomposes
`hat_c=Y_a+V_a+H_a`; projection onto `span(Y_a,V_a)` gives a rank-safe
quantity `Q_a^(2)<=D_a(I0)`.

Cycle 48 replaces the coordinate-dependent split of the complete prefix by the
canonical vector

\[
 B_a=Y_a+V_a=\sum_{n=q}^{2a-1}\alpha_{q,n}\mathcal B_{q,n},
 \qquad \widehat{\mathbf c}_a=B_a+H_a.
\]

Its intrinsic one-generator projection is

\[
 \mathcal Q_a^{\rm cp}
 =\frac{|\langle B_a,\widehat{\mathbf c}_a\rangle|^2}{\|B_a\|^2}
 \le Q_a^{(2)}\le D_a(I_0),
\]

with value zero when `B_a=0`.  Orthogonalizing the remaining contrast gives an
exact two-channel formula for `Q_a^(2)`, while temporal Abel summation gives
endpoint-safe finite formulas for `B_a` in the Chebyshev and reciprocal-Mobius
packets.  The coordinate rewrite isolates the following stronger, still-open
sufficient target for the physical checkpoint:

\[
 \mathcal Q_a^{\rm cp}\gg(\log a)^{-3}.
\]

One sufficient, but not necessary, way to prove it is to find fixed
\(c_0,\varepsilon>0\) such that, for every sufficiently large \(a\),

\[
 \|B_a\|^2\ge c_0(\log a)^{-3},
 \qquad
 \left|1+\frac{\langle B_a,H_a\rangle}{\|B_a\|^2}\right|
 \ge\varepsilon.
\]

These inequalities would give
\(\mathcal Q_a^{\rm cp}\ge\varepsilon^2c_0(\log a)^{-3}\).
Neither the projection target nor either factor estimate is established.  At
\(\theta=2/5\), the six finite two-generator censuses capture more than
`99.7%` of `D_a`, and the reconstructed complete-prefix line captures between
about `95.8%` and `99.9%`, but both statements are finite only.  The scaled
projection values, generator angles, mixed signs, and coefficients are
nonmonotone and imply no asymptotic estimate, eventual rank, or interscale
theorem.  See
`cycle-47-initial-tail-and-complete-prefix-audit.md` and
`cycle-48-canonical-complete-prefix-and-abel-audit.md`.

Cycle 49 proves a sharper no-go inside this route.  The exact prefix splits as

\[
 B_a=P_a^++S_a^\mu,
\]

where `P_a^+` is strictly row-positive at every permitted finite scale.  Yet,
uniformly for `q/a in [1,3/2]`,

\[
 (\log a)^2P_a^+(q)\to F(q/a),\qquad
 (\log a)^2S_a^\mu(q)\to-F(q/a),
\]

with

\[
 F(u)=\frac{2-u}{u}-\frac12\log^2\frac2u>0.
\]

Hence the positive packet and signed reciprocal-Mobius partner annihilate at
leading order.  A separate lower bound for the positive packet, even with its
sharp norm asymptotic `asymp a/log(a)^4`, cannot prove the prefix target.  The
surviving exact row residual is

\[
 B_a(q)=\sum_{n=q}^{2a-1}\frac{\alpha_{q,n}}{\log n}
 \left[
 \frac{E_{n+1}}q+\mathfrak j_{q,n}
 +\mathfrak a_{q,n}(1+\ell_n-\eta_n(\log n)m_n)
 \right].
\]

The next lemma must control the square of this complete correlated residual
before absolute values, and must separately retain its signed correlation with
`H_a`.  The exact coefficient-kernel rewrite shows that this is a moving
selected-Mobius quadratic-form theorem, not a consequence of sign-stripped
operator spectrum or normal diagonal mass.  See
`cycle-49-leading-prefix-annihilation-and-coefficient-kernel.md`.

If the original packet estimate is proved, it gives only a trace-based
moving-projection lower bound of order `log^-2 a`; Burnol's cited result is a
budget lower bound, not the upper bound needed to close the completed square.
No RH consequence is presently proved.

## Earlier route context through Cycle 44

The pre-Cycle-45 projection gate was
`cycle-44-boundary-envelope-no-go.md`. At fixed `theta=2/5`, complete
restricted-Gram certificates show that the entire current-admission span fails
at dyadic starts `128,256,512`; adding every squarefree old label in a window
of width `ceil(a/log a)` still fails at `256,512`. The least passing
affine-free historical widths are exactly `19,53,361` there. This kills those
finite local architectures, not an eventual theorem. The Cycle 45 kernel
analysis supersedes the former instruction to derive the moving kernel and
leaves the signed arithmetic inequality above.
