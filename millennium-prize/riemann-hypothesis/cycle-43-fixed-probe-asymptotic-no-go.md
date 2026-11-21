# Cycle 43: asymptotic no-go for every fixed finite old-probe family

## Scope and verdict

This note concerns only the direct projection architecture introduced in the
Cycle 43 finite multiprobe census.  Fix

\[
 0<\theta<\frac12
\]

and use the dyadic block \([a,2a)\).  Let \(S\) be any fixed nonempty finite family
chosen from the affine probe and distinct fixed squarefree old-divisor probes.
Then, unconditionally,

\[
 \boxed{
 \Pi_S(a,2a;\theta)
 =\frac{2(1-\theta)\log 2}{(\log a)^3}
   \delta_S^T V_S^{-1}\delta_S
  +o_{S,\theta}((\log a)^{-3}), }
 \tag{43.29}
\]

where \(V_S\) is the fixed spatial Gram matrix and \(\delta_S\) is defined
below.  In contrast, the negative budget satisfies

\[
 \boxed{
 \liminf_{a\to\infty}(\log a)^2N_\theta(a,2a)
 \geq \frac{C_{\rm B}\log2}{2(1-\theta)}>0. }
 \tag{43.30}
\]

Consequently,

\[
 \boxed{\frac{\Pi_S(a,2a;\theta)}{N_\theta(a,2a)}
 =O_{S,\theta}((\log a)^{-1})\longrightarrow0.}
 \tag{43.31}
\]

Thus every such fixed finite family eventually fails the sufficient direct
projection condition \(\Pi_S\geq N_\theta\).  This does **not** determine the
sign of the full compensated residual: it says only that a fixed finite span
captures asymptotically too little of its positive square.

The proof uses only the classical de la Vallée Poussin zero-free-region error,
a fixed-test Abel lemma proved here, and Burnol's unconditional lower bound for
the optimal Nyman--Beurling distance.  It assumes neither RH nor any
RH-strength Mertens estimate.  It does not cover moving divisors, growing rank,
current-admission/triangular families, moving \(\theta\), or \(\theta=1/2\).

## 1. Exact block and probe identities

Put

\[
 L_n=\log n,\qquad
 w_n=1-\frac{L_n}{L_{n+1}},\qquad
 \tau=1-2\theta,
\]

\[
 \mathsf A_n=1+\frac{L_n}{L_{n+1}}-2\theta
 =2(1-\theta)-w_n,
 \qquad
 \eta_n=\frac{\tau}{\mathsf A_n},
\]

and

\[
 B_n=2\theta+\frac{\tau^2}{\mathsf A_n}.
\]

Retain the restricted-space vectors

\[
 U_n=\chi+\sum_{d\leq n}\mu(d)\rho_d,
 \qquad
 D_n=\sum_{d\leq n}\mu(d)(\log d)\rho_d,
\]

and set

\[
 Z_n=\frac{D_n}{L_n}-\eta_nU_n,
 \qquad
 X=\bigl(\sqrt{w_n\mathsf A_n}\,Z_n\bigr)_{a\leq n<2a}.
\]

The exact Cycle 43 completed-square identity is

\[
 \mathcal R_\theta(a,2a)=\|X\|^2-N_\theta(a,2a),
 \tag{43.32}
\]

where

\[
 N_\theta(a,2a)
 =\sum_{a\leq n<2a}w_nB_n\|U_n\|_{L^2(0,1)}^2.
 \tag{43.33}
\]

For the affine label put

\[
 v_0=\chi,\qquad \varepsilon_0=1,\qquad \ell_0=0.
\]

For a fixed squarefree divisor \(q\), put

\[
 v_q=\rho_q,\qquad \varepsilon_q=\mu(q),\qquad \ell_q=\log q.
\]

Once \(a>q\), the divisor is old throughout the block, and both types of probe
have the common formula

\[
 \phi_i(n)=\varepsilon_i\left(\frac{\ell_i}{L_n}-\eta_n\right),
 \qquad
 p_i=\bigl(\sqrt{w_n\mathsf A_n}\,\phi_i(n)v_i\bigr)_{a\leq n<2a}.
 \tag{43.34}
\]

In particular, \(p_0\) is exactly the affine probe.  The exact finite Gram and
correlation entries are

\[
 G_{ij}(a)=\langle v_i,v_j\rangle
 \sum_{a\leq n<2a}w_n\mathsf A_n\phi_i(n)\phi_j(n),
 \tag{43.35}
\]

\[
 c_i(a)=\sum_{a\leq n<2a}w_n\mathsf A_n\phi_i(n)
 \left(
  \frac{\langle D_n,v_i\rangle}{L_n}
  -\eta_n\langle U_n,v_i\rangle
 \right).
 \tag{43.36}
\]

When \(G_S\) is nonsingular,

\[
 \Pi_S=c_S^TG_S^{-1}c_S
 =\|\operatorname{Proj}_{\operatorname{span}\{p_i:i\in S\}}X\|^2,
 \tag{43.37}
\]

and hence

\[
 \mathcal R_\theta(a,2a)\geq \Pi_S-N_\theta(a,2a).
 \tag{43.38}
\]

## 2. Fixed spatial functions and their Gram matrix

Under the reciprocal substitution \(t=1/x\), the restricted space becomes

\[
 L^2\!\left([1,\infty),\frac{dt}{t^2}\right),
 \qquad
 \chi(t)=1,\qquad \rho_q(t)=\{t/q\}.
 \tag{43.39}
\]

The entries needed later include

\[
 \langle\chi,\rho_q\rangle
 =\frac{\log q+1-\gamma}{q},
 \tag{43.40}
\]

\[
 \|\rho_q\|^2
 =\frac{\log(2\pi)-\gamma}{q}-\frac1{q^2}.
 \tag{43.41}
\]

The affine function together with any distinct finite list of divisor
functions is linearly independent.  Indeed, suppose

\[
 c_0+\sum_{q\in S}c_q\{t/q\}=0
 \tag{43.42}
\]

in the Hilbert space.  Equality almost everywhere implies equality on every
common continuity interval.  For a label \(q\), choose a prime \(P\) larger
than every label and take the jump at \(t=qP\).  A divisor function
\(\{t/r\}\) jumps at an integer \(t_0\) exactly when \(r\mid t_0\).
Moreover, \(r<P\) implies \(\gcd(r,P)=1\), so
\(r\mid qP\) is equivalent to \(r\mid q\).  Thus

\[
 \sum_{\substack{r\in S\\r\mid q}}c_r=0.
 \tag{43.43}
\]

Induction through the labels in increasing order gives \(c_q=0\) for every
\(q\), and then \(c_0=0\).  Therefore the fixed spatial Gram matrix

\[
 V_S=(\langle v_i,v_j\rangle)_{i,j\in S}
 \tag{43.44}
\]

is positive definite.  In particular, there is no degeneracy between the
affine probe and the divisor \(q=1\): their scale profiles agree, but their
spatial vectors do not.

## 3. A fixed-divisor Gram asymptotic

For fixed \(q\), write

\[
 K_q(d)=\langle\rho_d,\rho_q\rangle
 =\int_1^\infty\{t/d\}\{t/q\}\frac{dt}{t^2}.
\]

Splitting at \(t=d\), and then putting \(t=du\) in the second part, gives the
exact formula

\[
 K_q(d)=\frac1d\int_1^d\frac{\{t/q\}}t\,dt
 +\frac1d\int_1^\infty\frac{\{u\}\{du/q\}}{u^2}\,du.
 \tag{43.45}
\]

The periodic function \(\{t/q\}-1/2\) has a bounded primitive.  Integration
by parts therefore gives

\[
 \int_1^d\frac{\{t/q\}}t\,dt
 =\frac12\log d+\kappa_q^{(1)}+O_q(d^{-1}).
 \tag{43.46}
\]

The function \(h(u)=\{u\}/u^2\) is integrable and has finite total variation.
The function \(\{du/q\}-1/2\) has a primitive bounded by \(O(q/d)\), so a
second integration by parts gives

\[
 \int_1^\infty h(u)\{du/q\}\,du
 =\frac12\int_1^\infty h(u)\,du+O_q(d^{-1}).
 \tag{43.47}
\]

Consequently, for a constant \(\kappa_q\),

\[
 \boxed{
 K_q(d)=\frac{\log d}{2d}+\frac{\kappa_q}{d}+R_q(d),
 \qquad R_q(d)=O_q(d^{-2}).}
 \tag{43.48}
\]

The remainder is retained throughout.  More precisely, with the periodically
extended Bernoulli polynomial \(B_2(x)=x^2-x+1/6\), a second integration by
parts gives

\[
 R_q(d)=\frac{\beta_q(d)}{d^2}+O_q(d^{-3}),
 \qquad
 \beta_q(d)=\frac q2\sum_{k\geq1}
 \frac{B_2(\{dk/q\})}{k^2}.
\]

Thus \(\beta_q\) is bounded and \(q\)-periodic in the integer \(d\), and is
generally nonconstant.  This oscillatory coefficient is not being replaced by
a constant multiple of \(d^{-2}\).  Absolute summability of \(R_q\), together
with conditional convergence of the two leading Möbius moment series supplied
by the classical zero-free-region estimate, proves natural-order convergence
of both

\[
 \langle U_n,\rho_q\rangle
 =\langle\chi,\rho_q\rangle+
   \sum_{d\leq n}\mu(d)K_q(d)
 \tag{43.49}
\]

and

\[
 \langle D_n,\rho_q\rangle
 =\sum_{d\leq n}\mu(d)(\log d)K_q(d).
 \tag{43.50}
\]

It does not by itself identify their limits.  That conditional-convergence
step is supplied next rather than hidden inside a Fubini assertion.

## 4. Fixed-test Abel lemma

### Lemma 43.1

For each fixed positive integer \(q\), there is \(c_q>0\) such that, in natural
Möbius order,

\[
 \boxed{\langle U_n,\rho_q\rangle
 =O_q(e^{-c_q\sqrt{\log n}}),}
 \tag{43.51}
\]

and

\[
 \boxed{\langle D_n,\rho_q\rangle
 =\delta_q+O_q(e^{-c_q\sqrt{\log n}}),}
 \tag{43.52}
\]

where

\[
 \boxed{
 \delta_q=\int_1^\infty
 (\psi(\lfloor t\rfloor)-t)\{t/q\}\frac{dt}{t^2}.}
 \tag{43.53}
\]

The integral is absolutely convergent.

### Proof

Let

\[
 H(s)=\frac1{\zeta(s)}.
\]

For real \(z>0\), define

\[
 \mathcal U_z(t)=1+\sum_{d\geq1}\mu(d)d^{-z}\{t/d\},
 \tag{43.54}
\]

\[
 \mathcal D_z(t)=\sum_{d\geq1}\mu(d)(\log d)d^{-z}\{t/d\}.
 \tag{43.55}
\]

Their pairings with the fixed function \(\{t/q\}\) converge absolutely by
(43.48).  Explicitly,
\(K_q(d)\ll_q\log(2d)/d\), so for every \(z>0\) the series
\(\sum_{d\geq1}d^{-z}(\log d)^jK_q(d)\) converges absolutely for every fixed
\(j\) (only \(j\leq2\) is used below).  This also justifies the required first
\(z\)-derivatives of the scalar series.

For nonintegral \(t\), put

\[
 a_z(m)=\sum_{d\mid m}\mu(d)d^{-z}
 =\prod_{p\mid m}(1-p^{-z}),
 \qquad c_z=H(1+z).
 \tag{43.56}
\]

Splitting the sum in (43.54) at \(d=t\), and using
\(\{t/d\}=t/d-\lfloor t/d\rfloor\), gives exactly

\[
 \mathcal U_z(t)=1-\sum_{m\leq t}a_z(m)+c_zt.
 \tag{43.57}
\]

Here \(0\leq a_z(m)\leq1\), \(c_z\to0\), \(a_z(1)=1\), and
\(a_z(m)\to0\) for every \(m>1\).  It follows pointwise that
\(\mathcal U_z(t)\to0\).

Set \(K_z(t)=\mathcal U_z(t)/t^2\).  Between integers,

\[
 K_z'(t)=\frac{c_z}{t^2}-\frac{2\mathcal U_z(t)}{t^3},
\]

while the jump at \(m\geq2\) has magnitude \(a_z(m)/m^2\).  Fix a small
\(z_0>0\).  Uniformly for \(0<z\leq z_0\), \(c_z\) is bounded and
\(|\mathcal U_z(t)|\ll t\).  More explicitly,

\[
 \operatorname{Var}_{[1,\infty)}K_z
 \leq |c_z|\int_1^\infty\frac{dt}{t^2}
 +2\int_1^\infty\frac{|\mathcal U_z(t)|}{t^3}\,dt
 +\sum_{m\geq2}\frac{a_z(m)}{m^2}.
\]

Every integrand or summand tends pointwise to zero and is dominated by an
integrable or summable majorant independent of \(z\).  Also
\(K_z(1+)=c_z\).  (At \(1<t<2\), (43.57) reads
\(\mathcal U_z(t)=c_zt\).)  Dominated convergence therefore gives

\[
 |K_z(1+)|+\operatorname{Var}_{[1,\infty)}K_z\longrightarrow0.
 \tag{43.58}
\]

Now decompose

\[
 \{t/q\}=\frac12+g_q(t),
\]

where \(g_q\) is periodic of mean zero and has a bounded primitive.  Stieltjes integration by parts, first on \([1,R]\) using the right-continuous
BV representative and then with \(R\to\infty\), against that primitive and
(43.58) gives

\[
 \int_1^\infty \mathcal U_z(t)g_q(t)\frac{dt}{t^2}\longrightarrow0.
 \tag{43.59}
\]

The mean part is explicit.  Using (43.40),

\[
 \int_1^\infty\mathcal U_z(t)\frac{dt}{t^2}
 =1-H'(1+z)+(1-\gamma)H(1+z)\longrightarrow0.
 \tag{43.60}
\]

Therefore

\[
 \langle\mathcal U_z,\rho_q\rangle\longrightarrow0.
 \tag{43.61}
\]

For the logarithmic sum, differentiate (43.56).  Put

\[
 b_z(m)=a_z'(m),\qquad c_z'=H'(1+z).
\]

Then (43.57) gives

\[
 \mathcal D_z(t)=\sum_{m\leq t}b_z(m)-c_z't.
 \tag{43.62}
\]

For \(0<z\leq z_0\),

\[
 0\leq b_z(m)\leq\sum_{p\mid m}\log p\leq\log m.
 \tag{43.63}
\]

Moreover,

\[
 b_z(m)\longrightarrow\Lambda(m),\qquad c_z'\longrightarrow1.
 \tag{43.64}
\]

Thus \(\mathcal D_z(t)\to E(t):=\psi(\lfloor t\rfloor)-t\) pointwise.  For
\(J_z(t)=\mathcal D_z(t)/t^2\), the derivative between jumps is

\[
 J_z'(t)=-\frac{c_z'}{t^2}-\frac{2\mathcal D_z(t)}{t^3},
\]

and the jump at \(m\) is \(b_z(m)/m^2\).  Put \(J_0(t)=E(t)/t^2\).
The total-variation passage is not a formal interchange: using
\(|\mathcal D_z(t)|+|E(t)|\ll t\log(2t)\), one has the explicit bound

\[
 \begin{aligned}
 \operatorname{Var}_{[1,\infty)}(J_z-J_0)
 \leq{}& |c_z'-1|\int_1^\infty\frac{dt}{t^2}
 +2\int_1^\infty
       \frac{|\mathcal D_z(t)-E(t)|}{t^3}\,dt\\
 &+\sum_{m\geq2}\frac{|b_z(m)-\Lambda(m)|}{m^2}.
 \end{aligned}
\]

Here \(c_z'\to1\), the middle integrand is dominated by
\(O(\log(2t)/t^2)\), and the jump summands are dominated by
\(2\log(m)/m^2\).  Moreover \(J_z(1+)=-c_z'\) and \(J_0(1+)=-1\).
Pointwise convergence and dominated convergence therefore imply

\[
 \left|J_z(1+)-J_0(1+)\right|
 +\operatorname{Var}_{[1,\infty)}(J_z-J_0)\longrightarrow0.
 \tag{43.65}
\]

If \(G_q(t)=\int_1^t g_q(s)\,ds\), then \(G_q\) is bounded.  Stieltjes
integration by parts first on \([1,R]\), using the right-continuous BV
representative, followed by \(R\to\infty\), has vanishing endpoint terms and
bounds each centered pairing by
\(\|G_q\|_\infty\) times the relevant total variation.  Applied to (43.65),
this yields

\[
 \int_1^\infty \mathcal D_z(t)g_q(t)\frac{dt}{t^2}
 \longrightarrow
 \int_1^\infty E(t)g_q(t)\frac{dt}{t^2}.
 \tag{43.66}
\]

The mean part is again explicit:

\[
 \int_1^\infty\mathcal D_z(t)\frac{dt}{t^2}
 =H''(1+z)-(1-\gamma)H'(1+z)
 \longrightarrow-(1+\gamma),
 \tag{43.67}
\]

because

\[
 H(1+z)=z-\gamma z^2+O(z^3).
\]

On the other hand, the classical PNT error gives

\[
 E(t)\ll t e^{-c\sqrt{\log t}}+1,
 \tag{43.68}
\]

so \(E(t)/t^2\) is absolutely integrable.  Direct summation over unit
intervals, together with

\[
 \sum_{m\leq x}\frac{\Lambda(m)}m=\log x-\gamma+o(1),
 \qquad \frac{\psi(x)}x\to1,
\]

also gives

\[
 \int_1^\infty E(t)\frac{dt}{t^2}=-(1+\gamma).
 \tag{43.69}
\]

Combining (43.66)--(43.69) proves

\[
 \langle\mathcal D_z,\rho_q\rangle\longrightarrow
 \int_1^\infty E(t)\{t/q\}\frac{dt}{t^2}.
 \tag{43.70}
\]

Finally, write (43.48) as its two displayed leading terms plus the retained
remainder \(R_q(d)\).  Partial summation from the classical bound

\[
 \sum_{d\leq x}\mu(d)\ll x e^{-c\sqrt{\log x}}
 \tag{43.71}
\]

gives, for each fixed \(r\geq0\),

\[
 \sum_{d>x}\frac{\mu(d)(\log d)^r}{d}
 =O_r\!\left(e^{-c_r\sqrt{\log x}}\right),
\]

where the tail is interpreted in natural order.  Meanwhile

\[
 \sum_{d>x}|R_q(d)|=O_q(x^{-1}),
 \qquad
 \sum_{d>x}(\log d)|R_q(d)|=O_q((\log x)/x).
\]

Thus the two scalar series in (43.49)--(43.50) converge in natural order with
the errors asserted in (43.51)--(43.52), after reducing \(c_q\) if necessary.
The absolutely summable remainder can contribute a nonzero constant; no value
has been discarded.  Finally, summation by parts for the convergent generalized
Dirichlet series \(\sum a_dd^{-z}\) gives the ordinary-to-Abel theorem
\(\lim_{z\downarrow0}\sum a_dd^{-z}=\sum a_d\).  Applying it to the complete
scalar series, remainder included, identifies the ordinary sums with the
limits (43.61) and (43.70).  This proves the lemma. \(\square\)

The role of the two-cutoff/Abel argument is essential: the pointwise Möbius
identities are conditionally convergent and cannot simply be integrated by
Tonelli.

## 5. The affine coordinate

Define

\[
 M(x)=\sum_{d\leq x}\frac{\mu(d)}d,
 \quad
 J(x)=\sum_{d\leq x}\frac{\mu(d)\log d}{d},
 \quad
 K(x)=\sum_{d\leq x}\frac{\mu(d)(\log d)^2}{d}.
 \tag{43.72}
\]

Using (43.40), one has exactly

\[
 \langle U_n,\chi\rangle
 =1+J(n)+(1-\gamma)M(n),
 \tag{43.73}
\]

\[
 \langle D_n,\chi\rangle
 =K(n)+(1-\gamma)J(n).
 \tag{43.74}
\]

The zero-free-region estimate (43.71) gives ordinary convergence with an
exponentially small square-root-log error.  Since

\[
 \frac1{\zeta(1+z)}=z-\gamma z^2+O(z^3),
\]

Abel's theorem gives the corrected limits

\[
 \boxed{M(n)\to0,\qquad J(n)\to-1,\qquad K(n)\to-2\gamma.}
 \tag{43.75}
\]

Therefore

\[
 \langle U_n,\chi\rangle=O(e^{-c\sqrt{\log n}}),
 \qquad
 \langle D_n,\chi\rangle=-(1+\gamma)
 +O(e^{-c\sqrt{\log n}}).
 \tag{43.76}
\]

Set

\[
 \delta_0=-(1+\gamma),
 \qquad
 \delta_q=\text{the value in (43.53)}.
 \tag{43.77}
\]

Lemma 43.1 and (43.76) can then be written uniformly for every fixed label in
\(S\) as

\[
 \langle U_n,v_i\rangle=O_S(e^{-c_S\sqrt{\log n}}),
 \qquad
 \langle D_n,v_i\rangle=\delta_i+
 O_S(e^{-c_S\sqrt{\log n}}).
 \tag{43.78}
\]

## 6. Asymptotics of the fixed-family projection

Let

\[
 L=\log a,\qquad \lambda=\log2,
 \qquad E_S=\operatorname{diag}(\varepsilon_i)_{i\in S}.
\]

The elementary block sums are

\[
 \sum_{a\leq n<2a}w_n
 =\frac{\lambda}{L}+O(L^{-2}),
 \tag{43.79}
\]

and, exactly,

\[
 \sum_{a\leq n<2a}\frac{w_n}{L_n}
 =\sum_{a\leq n<2a}
 \left(\frac1{L_n}-\frac1{L_{n+1}}\right)
 =\frac1L-\frac1{L+\lambda}
 =\frac{\lambda}{L(L+\lambda)}.
 \tag{43.80}
\]

Since \(\mathsf A_n\to2(1-\theta)\), the exact expression (43.35) gives

\[
 \boxed{
 G_S(a)=
 \frac{\tau^2\lambda}{2(1-\theta)L}
 E_SV_SE_S+O_{S,\theta}(L^{-2}).}
 \tag{43.81}
\]

The sign matrix is required at the matrix level.  From (43.36), (43.78), and
(43.80),

\[
 \boxed{
 c_S(a)=-\frac{\tau\lambda}{L^2}E_S\delta_S
 +O_{S,\theta}(L^{-3}).}
 \tag{43.82}
\]

Since \(V_S>0\), (43.81) is positive definite for all sufficiently large
\(a\), and

\[
 G_S(a)^{-1}
 =\frac{2(1-\theta)L}{\tau^2\lambda}
 E_SV_S^{-1}E_S+O_{S,\theta}(1).
 \tag{43.83}
\]

Substitution in (43.37) proves (43.29).  Both \(\tau\) and all Möbius signs
cancel from the leading coefficient.

For the affine singleton this specializes to

\[
 \boxed{
 \Pi_{\rm aff}(a,2a;\theta)
 =\frac{2(1-\theta)(1+\gamma)^2\log2}{(\log a)^3}
 +o_\theta((\log a)^{-3}).}
 \tag{43.84}
\]

For a divisor singleton,

\[
 \boxed{
 \Pi_q(a,2a;\theta)
 =\frac{2(1-\theta)\delta_q^2\log2}
 {\|\rho_q\|^2(\log a)^3}
 +o_{q,\theta}((\log a)^{-3}).}
 \tag{43.85}
\]

If \(\delta_q=0\), the leading coefficient vanishes; this is not a Gram
degeneracy and only makes the projection smaller.

## 7. Burnol's lower bound and the restricted negative budget

Define the discrete optimal distance explicitly by

\[
 d_n^2=\inf_{A}
 \frac1{2\pi}\int_{-\infty}^{\infty}
 \left|1-\zeta\!\left(\tfrac12+it\right)
 A\!\left(\tfrac12+it\right)\right|^2
 \frac{dt}{\tfrac14+t^2},
 \tag{43.86a}
\]

where the infimum is over all Dirichlet polynomials
\(A(s)=\sum_{d\leq n}a_dd^{-s}\) with complex coefficients; no condition
\(A(1)=0\) is imposed.

Burnol's Theorem 1.3 is stated for the continuous Nyman--Beurling distance
\(D(\lambda)\).  Under the Mellin unitary normalization corresponding to
(43.86a), the discrete span with labels \(1\leq d\leq n\) is a subspace of
the continuous span with parameters \(\lambda\leq\theta\leq1\), for
\(\lambda=1/n\).  Hence

\[
 d_n\geq D(1/n).
\]

Combining this inclusion with Burnol's continuous theorem (equivalently, with
the discrete statement recorded explicitly by Bettin--Conrey--Farmer) gives

\[
 \liminf_{n\to\infty}(\log n)d_n^2\geq C_{\rm B},
 \qquad
 C_{\rm B}=\sum_{\substack{\rho:\Re\rho=1/2\\
                    \rho\ \mathrm{distinct}}}
 \frac{m(\rho)^2}{|\rho|^2}>0.
 \tag{43.86}
\]

This is conventionally unconditional.  More precisely, Burnol states that if
RH fails then
\(\liminf_{\lambda\downarrow0}D(\lambda)
\sqrt{\log(1/\lambda)}=+\infty\); the inclusion therefore makes the discrete
left side in (43.86) infinite as well.  The sum on the right uses only
critical-line zeros.

The Dirichlet polynomial

\[
 Q_n(s)=\sum_{d\leq n}\mu(d)d^{-s}
\]

is an admissible competitor.  In the repository Mellin convention,
\(\mathcal M\rho_d(s)=-\zeta(s)d^{-s}/s\), so its full-space residual is
precisely \(U_n=\chi+\sum_{d\leq n}\mu(d)\rho_d\).  Burnol's inequality
applies to this full residual, not directly to the restricted norm in
(43.33).  On \(x>1\), \(\chi(x)=0\) and \(\rho_d(x)=1/(dx)\), whence

\[
 U_n(x)=\frac{M(n)}x.
\]

Therefore the full and restricted norms satisfy the exact relation

\[
 \|U_n\|_{L^2(0,\infty)}^2
 =\|U_n\|_{L^2(0,1)}^2+M(n)^2.
 \tag{43.87}
\]

Since the full norm is at least \(d_n^2\), while
\((\log n)M(n)^2\to0\), (43.86) implies

\[
 \boxed{
 \liminf_{n\to\infty}(\log n)
 \|U_n\|_{L^2(0,1)}^2\geq C_{\rm B}.}
 \tag{43.88}
\]

Also

\[
 B_n\longrightarrow
 2\theta+\frac{\tau^2}{2(1-\theta)}
 =\frac1{2(1-\theta)}.
 \tag{43.89}
\]

Fix \(\epsilon_1,\epsilon_2>0\).  The definition of liminf gives, for
**every** sufficiently large \(n\),

\[
 \|U_n\|^2\geq\frac{C_{\rm B}-\epsilon_1}{L_n},
 \qquad
 B_n\geq\frac1{2(1-\theta)}-\epsilon_2.
\]

There is therefore no subsequence-to-block gap.  Using (43.80),

\[
 N_\theta(a,2a)
 \geq
 \left(\frac1{2(1-\theta)}-\epsilon_2\right)
 (C_{\rm B}-\epsilon_1)
 \frac{\lambda}{L(L+\lambda)}
\]

for every sufficiently large \(a\).  Letting
\(\epsilon_1,\epsilon_2\downarrow0\) proves
(43.30), and (43.29)--(43.30) prove (43.31).

## 8. Strategic consequence and exclusions

The cap-256 finite census found that one or two old columns often capture the
budget, with the moving label \(215\) repairing the last four affine failures.
The theorem above explains why that phenomenon cannot stabilize with one
prescribed finite old family at fixed \(\theta\): a fixed family contributes
only order \((\log a)^{-3}\), while the budget is at least order
\((\log a)^{-2}\).

The viable projection search must therefore leave at least one hypothesis of
this theorem.  Possibilities include:

1. a divisor \(q=q(a)\) moving with the scale;
2. rank growing with \(a\);
3. triangular/current-admission support rather than old full-block support;
4. a different probe class whose fixed-test correlation does not decay as in
   (43.78);
5. a moving \(\theta\), although the pilot choice \(\theta\asymp1/\log a\)
   has only summable effective renewal mass on polynomial chains and is not by
   itself an RH mechanism.

In any regime where an analogue of (43.29) remains uniform, overcoming the
budget requires the effective quadratic leverage
\(\delta_S^TV_S^{-1}\delta_S\) to grow at least on the order of \(\log a\).
This is a necessary scale heuristic, not a theorem for labels comparable to
\(a\), where the fixed-test asymptotics cease to be uniform.

The theorem does not include:

- \(\theta=1/2\), where \(\tau=0\) and the leading probe Gram degenerates;
- nonsquarefree labels, whose declared divisor probes vanish because
  \(\mu(q)=0\);
- repeated labels;
- moving \(q\), growing rank, or arbitrary fixed Hilbert-space probes outside
  the declared affine/old-divisor architecture;
- any conclusion that \(\mathcal R_\theta(a,2a)<0\).

No Riemann-hypothesis result is claimed.

## References

- J.-F. Burnol, *A lower bound in an approximation problem involving the zeros
  of the Riemann zeta function*, Advances in Mathematics **170** (2002),
  56--70, DOI 10.1006/aima.2001.2066, arXiv:math/0103058.
- L. Báez-Duarte, M. Balazard, B. Landreau, and E. Saias, *Notes sur la
  fonction zêta de Riemann, 3*, Advances in Mathematics **149** (2000),
  130--144, DOI 10.1006/aima.1999.1861.
- The Cycle 39--40 notes in this dossier for the exact full/restricted
  normalization and the literature audit of Burnol's constant.
