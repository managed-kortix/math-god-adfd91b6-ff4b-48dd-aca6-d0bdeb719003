# Cycle 47: initial-tail geometry and complete-prefix diagnostics

## Status and scope

This note records exact finite identities, an unconditional additive endpoint
expansion, one narrow zero-mode obstruction, and two fail-closed finite Arb
censuses for the Cycle 45 moving Möbius--Vasyunin frontier.  It does **not**
prove

\[
 D_a(I)\gg (\log a)^{-3},
 \qquad
 \liminf_{a\to\infty}\log(a)\frac{D_a(I)}{\Delta_a(I)}>0,
\]

a moving-projection theorem, completed-square budget closure, or the Riemann
hypothesis.  The projection estimates below are stronger sufficient
checkpoints, not equivalent reformulations of the surviving dispersion target.

No claim of bibliographic priority is made for an elementary finite identity.
The new durable content is the exact assembly, correction ledger, hostile
scope audit, and reproducible finite certificates.

Throughout, fix

\[
 a\in\mathbb Z,\qquad a\ge2,\qquad
 0<\theta<\frac12,\qquad C=2(1-\theta),\qquad \tau=1-2\theta=C-1,
\]

put \(M=2a-1\), \(L=\log a\), \(L_n=\log n\), and write

\[
 \delta_n=\log\frac{n+1}{n},\qquad
 w_n=1-\frac{L_n}{L_{n+1}},\qquad
 A_n=C-w_n,\qquad
 \eta_n=\frac{\tau}{A_n}.
\]

Work in

\[
 H=L^2\!\left([1,\infty),\frac{dt}{t^2}\right),\qquad
 \chi(t)=1,\qquad \rho_d(t)=\left\{\frac td\right\}.
\]

Define

\[
 b_d(n)=\frac{\log d}{L_n}-\eta_n,
\]

\[
 U_n=\chi+\sum_{d\le n}\mu(d)\rho_d,
 \qquad
 \mathscr D_n=\sum_{d\le n}\mu(d)(\log d)\rho_d,
\]

and

\[
 Z_n=\frac{\mathscr D_n}{L_n}-\eta_nU_n
 =-\eta_n\chi+\sum_{d\le n}\mu(d)b_d(n)\rho_d.
 \tag{1.1}
\]

The affine vector \(\chi\) is essential.  For a compact
\(I\Subset(0,2)\), let

\[
 S_a(I)=\{q<2a:\mu(q)^2=1,\ q/a\in I\},
 \qquad N_q=\max(a,q).
\]

On a physical squarefree row, put
\(\widehat c_a(q)=\mu(q)c_a(q)\).  No extra outer Möbius sign occurs below.
Finally set

\[
 \alpha_{q,n}=w_nA_nb_q(n),
 \qquad
 \mathcal K_{q,n}=\langle\rho_q,Z_n\rangle_H.
\]

## 1. Exact temporal contraction

For every physical \(q<2a\), Cycle 46's coefficient-index identity may be
reordered, with all sums finite, to give

\[
 \boxed{
 \widehat c_a(q)=
 \sum_{n=N_q}^{M}\alpha_{q,n}\mathcal K_{q,n}.}
 \tag{1.2}
\]

There is no \(n=2a\) term.  Writing

\[
 g_q=\langle\chi,\rho_q\rangle_H
 =\frac{\log q+1-\gamma_E}{q},
 \qquad
 G(q,d)=\langle\rho_q,\rho_d\rangle_H,
\]

and

\[
 m_n=\sum_{d\le n}\frac{\mu(d)}d,
 \qquad
 \ell_n=\sum_{d\le n}\frac{\mu(d)\log d}{d},
 \qquad
 s_n=\frac{\ell_n}{L_n}-\eta_nm_n,
 \tag{1.3}
\]

one has

\[
 \mathcal K_{q,n}
 =\frac1{L_n}\sum_{d\le n}\mu(d)(\log d)G(q,d)
 -\eta_n\left(g_q+\sum_{d\le n}\mu(d)G(q,d)\right).
 \tag{1.4}
\]

The complete restricted Gram entry is the full Vasyunin entry minus
\(1/(qd)\).  Deleting that correction or the affine term changes (1.2).

## 2. Initial block and intrinsic one-generator projection

For \(n\ge q\), define the initial non-wrapped contraction

\[
 \mathcal F_{q,n}=
 \int_1^q\rho_q(t)Z_n(t)\frac{dt}{t^2}.
\]

Let

\[
 C_q=\sum_{r<q}\Lambda(r)\log\frac qr,
 \qquad E_q=C_q-(q-1),
 \qquad R_n=s_n+\frac1{L_n}.
\]

On each complete cell \([k,k+1)\), \(1\le k<q\le n\), the finite
convolution identities

\[
 \sum_{d\le n}\mu(d)\left\lfloor\frac kd\right\rfloor=1,
 \qquad
 -\sum_{d\le n}\mu(d)\log d
       \left\lfloor\frac kd\right\rfloor=\psi(k)
\]

give

\[
 \boxed{
 \mathcal F_{q,n}
 =\frac{q-1}{q}s_n+\frac{C_q}{qL_n}
 =\frac{q-1}{q}R_n+\frac{E_q}{qL_n}.}
 \tag{2.1}
\]

Define row vectors

\[
 P_a(q)=\sum_{n=N_q}^{M}\alpha_{q,n}\mathcal F_{q,n},
 \qquad
 T_a(q)=\sum_{n=N_q}^{M}\alpha_{q,n}
                 (\mathcal K_{q,n}-\mathcal F_{q,n}).
 \tag{2.2}
\]

Then exactly

\[
 \widehat{\mathbf c}_a=P_a+T_a,
 \qquad
 D_a(I)=\|P_a\|^2+2\langle P_a,T_a\rangle+\|T_a\|^2.
 \tag{2.3}
\]

The source functions on \([1,q)\) and \([q,\infty)\) are orthogonal before
the common row contraction, but their scalar row vectors are not orthogonal.
The cross term in (2.3) cannot be discarded.

When \(P_a\ne0\), put

\[
 \gamma_a=
 \frac{\langle P_a,\widehat{\mathbf c}_a\rangle}{\|P_a\|^2}
 =1+\frac{\langle P_a,T_a\rangle}{\|P_a\|^2},
\]

\[
 \mathcal Q_a(I)=
 \frac{|\langle P_a,\widehat{\mathbf c}_a\rangle|^2}{\|P_a\|^2}
 =\gamma_a^2\|P_a\|^2.
 \tag{2.4}
\]

Set \(\mathcal Q_a=0\) when \(P_a=0\).  Orthogonal projection onto
\(\operatorname{span}\{P_a\}\) gives

\[
 \boxed{
 D_a(I)=\mathcal Q_a(I)
 +\|\widehat{\mathbf c}_a-\gamma_aP_a\|^2
 \ge \mathcal Q_a(I).}
 \tag{2.5}
\]

Consequently, fixed constants \(c_0,\varepsilon>0\) satisfying

\[
 \|P_a\|^2\ge c_0L^{-3},
 \qquad |\gamma_a|\ge\varepsilon
 \tag{2.6}
\]

would imply

\[
 D_a(I)\ge\varepsilon^2c_0L^{-3}.
 \tag{2.7}
\]

The square on \(\varepsilon\) is mandatory.  The earlier one-sided condition
\(\langle P_a,T_a\rangle\ge-(1-\varepsilon)\|P_a\|^2\) is sufficient but
stronger than necessary.  Neither (2.6) nor the intrinsic stronger checkpoint
\(\mathcal Q_a(I)\gg L^{-3}\) is proved.

This is not an equivalence: with \(P=e_1\) and
\(T=-e_1+e_2\), one has \(\gamma=\mathcal Q=0\) but
\(\|P+T\|^2=1\).

## 3. Endpoint Möbius packet

Define

\[
 \mathfrak h_n=1+\ell_n-L_nm_n.
 \tag{3.1}
\]

Finite Abel summation gives

\[
 \ell_n=L_nm_n-\sum_{j=1}^{n-1}\delta_jm_j,
 \qquad
 \mathfrak h_n=1-\sum_{j=1}^{n-1}\delta_jm_j,
 \tag{3.2}
\]

and hence

\[
 \boxed{\mathfrak h_n-\mathfrak h_{n+1}=\delta_nm_n.}
 \tag{3.3}
\]

Quantitative PNT estimates imply \(L_nm_n\to0\), \(\ell_n\to-1\), and
absolute convergence of the last series.  Therefore

\[
 \sum_{j\ge1}\delta_jm_j=1,
 \qquad
 \mathfrak h_n=\sum_{j\ge n}\delta_jm_j,
 \tag{3.4}
\]

and

\[
 \sum_{n=N_q}^{M}\delta_nm_n
 =\mathfrak h_{N_q}-\mathfrak h_{2a}.
 \tag{3.5}
\]

The endpoint \(\mathfrak h_{2a}\) is created by telescoping; it is not an
omitted \(n=2a\) summand.  One also has the exact smoothed PNT error identity

\[
 E_q=\int_1^q\frac{\psi(t)-t}{t}\,dt.
 \tag{3.6}
\]

Since \(1-\eta_n=(1-w_n)/A_n\), substituting (3.1) into (2.1) yields the exact
three-packet formula

\[
 \boxed{
 \begin{aligned}
 P_a(q)={}&\frac{q-1}{q}
 \sum_{n=N_q}^{M}w_n(1-w_n)b_q(n)m_n\\
 &+\frac{q-1}{q}
 \sum_{n=N_q}^{M}\frac{w_nA_nb_q(n)}{L_n}\mathfrak h_n\\
 &+\frac{E_q}{q}
 \sum_{n=N_q}^{M}\frac{w_nA_nb_q(n)}{L_n}.
 \end{aligned}}
 \tag{3.7}
\]

All displayed signs are plus; the three arithmetic packets remain signed.

Uniformly when \(q/a\) remains in a fixed compact subset of \((0,2)\), put

\[
 \lambda_{a,q}=\log\frac{2a}{N_q}.
\]

Elementary expansion of the exact coefficients gives

\[
 \begin{aligned}
 P_a(q)={}&
 \frac{q-1}{q}\frac{\mathfrak h_{N_q}-\mathfrak h_{2a}}{CL}\\
 &+\frac{q-1}{q}\frac1{L^2}
   \sum_{n=N_q}^{M}\delta_n\mathfrak h_n
 +\frac{E_q}{q}\frac{\lambda_{a,q}}{L^2}
 +\mathcal E_a(q),
 \end{aligned}
 \tag{3.8}
\]

where

\[
 \begin{aligned}
 |\mathcal E_a(q)|\ll_{\theta,I}{}&
 \frac1{L^2}\sum_{n=N_q}^{M}\delta_n|m_n|
 +\frac1{L^3}\sum_{n=N_q}^{M}\delta_n|\mathfrak h_n|\\
 &+\frac{|E_q|}{q}\frac{\lambda_{a,q}}{L^3}.
 \end{aligned}
 \tag{3.9}
\]

A standard quantitative PNT estimate, after reducing its constant, implies

\[
 |m_x|+|1+\ell_x|+|\mathfrak h_x|
 \ll e^{-c\sqrt{\log x}},
 \qquad
 |E_x|/x\ll e^{-c\sqrt{\log x}},
\]

so

\[
 P_a(q)=
 \frac{q-1}{q}\frac{\mathfrak h_{N_q}-\mathfrak h_{2a}}{CL}
 +O_{\theta,I}\!\left(
 \frac{\lambda_{a,q}e^{-c\sqrt L}}{L^2}\right).
 \tag{3.10}
\]

Equation (3.10) is additive, not relative.  The endpoint difference may vanish
or be smaller than the error.  Pointwise PNT decay also does not give the
needed vector lower bound over \(O(a)\) rows.

If

\[
 X_a(q)=\frac{q-1}{q}(\mathfrak h_{N_q}-\mathfrak h_{2a}),
 \qquad \mathcal H_a(I)=\sum_{q\in S_a(I)}|X_a(q)|^2,
\]

and \(\mathscr R_a=P_a-X_a/(CL)\), then exactly

\[
 \|P_a\|^2=
 \frac{\mathcal H_a(I)}{C^2L^2}
 +\frac2{CL}\langle X_a,\mathscr R_a\rangle
 +\|\mathscr R_a\|^2.
 \tag{3.11}
\]

Thus \(\mathcal H_a(I)\gg L^{-1}\) would imply
\(\|P_a\|^2\gg L^{-3}\) only together with a strict remainder estimate such
as

\[
 \|\mathscr R_a\|
 \le\kappa\frac{\sqrt{\mathcal H_a(I)}}{CL},
 \qquad 0\le\kappa<1.
 \tag{3.12}
\]

Neither premise is proved.  A formal reciprocal-zeta expansion for
\(\mathfrak h_x\) requires simplicity, controlled symmetric summation,
truncation bounds, reciprocal-derivative estimates, and moving-endpoint
uniformity.  It is not a consequence of RH alone, and a positive logarithmic
mean would not imply the every-scale liminf.

## 4. Exact complete-prefix theorem

Now fix

\[
 I_0=[1,3/2].
\]

For \(q\in S_a(I_0)\) and \(q\le n<2a\), one has \(n<2q\).  Define

\[
 \mathcal B_{q,n}=
 \int_1^{n+1}\rho_q(t)Z_n(t)\frac{dt}{t^2}.
 \tag{4.1}
\]

Put

\[
 \mathfrak a_{q,n}=\frac nq-\log\frac{n+1}{q},
 \qquad
 \mathfrak j_{q,n}=\log\frac{n+1}{q}
 -\sum_{k=q}^{n}\frac{\psi(k)}{k(k+1)}.
 \tag{4.2}
\]

Then

\[
 \boxed{
 \mathcal B_{q,n}=
 \mathfrak a_{q,n}R_n
 +\frac{E_{n+1}}{qL_n}
 +\frac{\mathfrak j_{q,n}}{L_n}.}
 \tag{4.3}
\]

Indeed, on each half-open complete cell \([k,k+1)\), \(1\le k\le n\),
finite convolution gives

\[
 U_n(t)=m_nt,
 \qquad
 \mathscr D_n(t)=\ell_nt+\psi(k),
 \qquad
 Z_n(t)=s_nt+\frac{\psi(k)}{L_n}.
\]

Because \(n<2q\), the row function is \(t/q\) before \(q\) and
\(t/q-1\) from \(q\) through the final cell.  Cellwise integration gives
(4.3).  Finite Abel summation also gives the endpoint-safe form

\[
 \boxed{
 \mathfrak j_{q,n}=
 \log\frac{n+1}{q}
 -\frac{\psi(q-1)}q
 -\sum_{m=q}^{n}\frac{\Lambda(m)}m
 +\frac{\psi(n)}{n+1}.}
 \tag{4.4}
\]

There is no half-weight, \(n=2a\) summand, \(\psi(n+1)\), or
\(\Lambda(n+1)\) term.  The final cell is \([n,n+1)\).  If
\(q=a,n=2a-1\), the reset at \(t=2q\) is a measure-zero singleton.  Omitting
the affine vector changes (4.3) by

\[
 \eta_n\left(\frac{\log(n+1)-1}{q}+\frac1{n+1}\right),
\]

so it cannot be dropped.

Define canonical row vectors on \(S_a(I_0)\):

\[
 Y_a(q)=\sum_{n=q}^{M}\alpha_{q,n}\frac{E_{n+1}}{qL_n},
 \tag{4.5}
\]

\[
 V_a(q)=\sum_{n=q}^{M}\alpha_{q,n}
 \left(\mathfrak a_{q,n}R_n+
       \frac{\mathfrak j_{q,n}}{L_n}\right),
 \tag{4.6}
\]

\[
 H_a(q)=\sum_{n=q}^{M}\alpha_{q,n}
       (\mathcal K_{q,n}-\mathcal B_{q,n}).
 \tag{4.7}
\]

Then exactly

\[
 \boxed{\widehat{\mathbf c}_a=Y_a+V_a+H_a.}
 \tag{4.8}
\]

Moreover,

\[
 \mathcal K_{q,n}-\mathcal B_{q,n}
 =\int_{n+1}^{\infty}\rho_q(t)Z_n(t)\frac{dt}{t^2},
\]

so \(H_a\) retains the complete remaining tail, including the affine term,
restricted correction, exact gcd condition, every Möbius sign, and the full
Vasyunin kernel.

## 5. Rank-at-most-two geometry

Let

\[
 \mathcal L_a(x_1,x_2)=x_1Y_a+x_2V_a,
\]

\[
 \mathsf G_a=\mathcal L_a^*\mathcal L_a
 =\begin{pmatrix}
 \langle Y_a,Y_a\rangle&\langle Y_a,V_a\rangle\\
 \langle Y_a,V_a\rangle&\langle V_a,V_a\rangle
 \end{pmatrix},
\]

and

\[
 z_a=\mathcal L_a^*\widehat{\mathbf c}_a
 =\binom{\langle Y_a,\widehat{\mathbf c}_a\rangle}
              {\langle V_a,\widehat{\mathbf c}_a\rangle}.
\]

Since \(\ker\mathsf G_a=\ker\mathcal L_a\), one has
\(z_a\in\operatorname{Ran}\mathsf G_a\).  Therefore, in ranks zero, one, or
two,

\[
 \boxed{
 Q_a^{(2)}=z_a^T\mathsf G_a^+z_a
 =\|\operatorname{Proj}_{\operatorname{span}(Y_a,V_a)}
      \widehat{\mathbf c}_a\|^2
 \le D_a(I_0).}
 \tag{5.1}
\]

The superscript denotes two generators.  It does not assert actual rank two.
A rank-safe formula is

\[
 Q_a^{(2)}=
 \begin{cases}
 0,&\operatorname{tr}\mathsf G_a=0,\\[3pt]
 \displaystyle\sup_{x^T\mathsf G_ax>0}
 \dfrac{(x^Tz_a)^2}{x^T\mathsf G_ax},
 &\operatorname{tr}\mathsf G_a>0.
 \end{cases}
 \tag{5.2}
\]

Only after certifying \(\det\mathsf G_a>0\) may an ordinary inverse be used.
Also,

\[
 Q_a^{(2)}\ge\frac{\|z_a\|_2^2}{\operatorname{tr}\mathsf G_a}
 \tag{5.3}
\]

when the trace is positive.  Hence the canonical sufficient pair

\[
 \operatorname{tr}\mathsf G_a\ll L^{-3},
 \qquad \|z_a\|_2^2\gg L^{-6}
 \tag{5.4}
\]

would imply \(Q_a^{(2)}\gg L^{-3}\).  Neither estimate is proved, and the two
coordinates depend on the canonical generators.  Only \(Q_a^{(2)}\) is basis
invariant.

Generic full rank and trace control are insufficient.  For \(L>1\), set

\[
 Y=L^{-3/2}e_1,
 \qquad V=L^{-3/2}e_2,
 \qquad H=-Y-V+L^{-2}e_3.
\]

Then \(\det\mathsf G=L^{-6}>0\) and
\(\operatorname{tr}\mathsf G=2L^{-3}\), but
\(z=0\), \(Q^{(2)}=0\), and
\(\|Y+V+H\|^2=L^{-4}\).  The unresolved arithmetic is exactly the retained
correlation with the physical vector.

## 6. Narrow fixed-local zero-isolation obstruction

Let \(\lambda=\log2\), and let \(\Gamma\) be the ordinates of simple zeta zeros
on the critical line.  For \(\gamma\in\Gamma\), set

\[
 v_\gamma(t)=\int_t^\lambda e^{(-1/2+i\gamma)y}\,dy,
 \qquad 0<t<\lambda.
\]

For every fixed \(\gamma_0\in\Gamma\),

\[
 v_{\gamma_0}\in
 \overline{\operatorname{span}}
 \{v_\gamma:\gamma\in\Gamma,\ \gamma\ne\gamma_0\}
\]

in \(L^2((0,\lambda),e^t\,dt)\).  Indeed, an orthogonal vector would produce,
by Fubini, a Cartwright-class entire function of exponential type at most
\(\lambda\) vanishing at all but one of the simple critical-line ordinates.
Conrey's positive-proportion theorem supplies \(\gg R\log R\) distinct such
ordinates, whereas a nonzero entire function of fixed exponential type has
only \(O(R)\) zeros.  Fourier uniqueness then forces the orthogonal vector to
vanish.

Thus no bounded fixed local functional can exactly select one fixed simple
critical zero while annihilating all the others.  This does **not** rule out
an \(a\)-dependent or growing-support test, finite cutoff, approximate
isolation, unbounded dual, meromorphic transform, ordinary projection, or a
direct inequality for the whole zero packet.

## 7. Finite certificate results

### 7.1 Initial-tail census

The current working-tree pair

- `cycle47_initial_tail_vector_census.py`, and
- `cycle47-initial-tail-vector-census.out`

has current hashes

```text
source  26c3f1a33bf68d1fe2d759e607f28246661fa1ac934af93bb11a6bd24072e7aa
output  03f9d1b2e3b016dc84fa7ea400565ab796d85ecae125f75a1bc86e6dbebf2663
```

and certifies twelve outward 192-bit Arb rows at

```text
a = 32, 64, 128, 256, 512, 1024
I = [1,2] and [1,3/2].
```

It checks three paths to \(P_a\), two paths to \(\widehat c_a\), two paths to
\(T_a\), rowwise recombination, energy recombination, the rank-one projection,
and all twelve Cycle 45 values of \(D_a\).  Its independent reciprocal-cell
Gram brackets use the fail-closed endpoint tests

```python
prefix.upper() <= value.lower()
value.upper() <= (prefix + tail).lower()
```

and the canonical run reproduces byte for byte in the pinned versioned
runtime.  A hostile final replay accepted the corrected pair.

At these finite scales every aggregate \(\langle P_a,T_a\rangle\) is positive,
with

\[
 1.05749\ldots\le\gamma_a\le1.14333\ldots,
\]

while \(L^3\|P_a\|^2\) is finite and nonmonotone.  The separate physical row
\((a,q)=(512,742)\) still has

\[
 \gamma=-0.0162860\ldots,
 \qquad
 \widehat c_a(q)^2/P_a(q)^2=0.0002652341\ldots.
\]

This refutes a universal finite pointwise one-sided rule, not an eventual
aggregate theorem.

### 7.2 Complete-prefix census

The committed pair

- `cycle47_complete_prefix_census.py`, and
- `cycle47-complete-prefix-census.out`

has hashes

```text
source   49f128e0e411f03e6d646ddbee5e4b2a13a4da2bc11bc5e6705e356404625928
closure  5880034899a532b7ee0ef742fd2964081fad48c4241ade78657582b2e7f6c635
output   d15e404fd584b62a778156eea00e66d2cbb1b7eb7770028228dff6be2f6001ef
```

and, at \(\theta=2/5\), certifies six 192-bit summaries on
\(I_0=[1,3/2]\), containing 613 physical rows.  It checks 54 direct-cell and
Abel evaluations of
\(\mathcal B_{q,n}\), every-row (4.8), temporal versus coefficient-index
contractions, six positive determinants before inversion, and six Cycle 45
values of \(D_a\).  Its reciprocal-cell predicates are also fail closed.

The finite capture ratios are

\[
 Q_a^{(2)}/D_a=
 0.999925\ldots,\ 0.999938\ldots,\ 0.999776\ldots,
 0.999626\ldots,\ 0.997459\ldots,\ 0.997895\ldots.
\]

But \(L^3Q_a^{(2)}\) is nonmonotone and falls from
\(0.013519\ldots\) to values near \(0.001\).  The near-exhaustion says only
that the six finite physical vectors lie close to their respective canonical
two-generator spans.  It proves no positive liminf, eventual rank, all-dyadic
bound, or all-integer theorem.

Both certificates pin CPython 3.12.13, python-flint 0.9.0, and FLINT 3.6.0 and
bind their declared local source/input closure.  The interpreter, wheel,
native-library binaries, operating system, hardware, and `uv` launcher are not
binary-attested; this is the explicit trusted-runtime boundary.

## 8. Hostile correction and no-go ledger

Any continuation must preserve all of the following.

1. Temporal sums end at \(2a-1\), and their lower endpoint is
   \(N_q=\max(a,q)\).
2. The affine vector \(\chi\), restricted correction \(-1/(qd)\), every
   Möbius sign, and the full Vasyunin kernel remain present.
3. In gcd grouping the reduced condition is \((r,q)=1\), not merely
   \((r,q/h)=1\).
4. The initial/tail retention factor is \(\varepsilon^2\), not
   \(\varepsilon\), and \(|\gamma_a|\) is the intrinsic condition.
5. Initial, tail, Chebyshev, endpoint, or normal-diagonal squares are not
   lower bounds without all signed cross terms.
6. The endpoint expansion is additive.  PNT upper bounds do not supply the
   required lower bound or every-window energy.
7. In (3.8), the factor \(1/C\) multiplies the endpoint-difference packet only.
8. The complete-prefix Abel formula has \(-\psi(q-1)/q\) and
   \(+\psi(n)/(n+1)\), with no next-index term.
9. “Two-generator” means rank at most two.  An ordinary inverse is permitted
   only after a certified positive determinant.
10. Trace, positive entries, continuum spectral tails, and finite projection
    capture do not control the selected Möbius vector generically.
11. A fixed compactly supported bounded local dual cannot exactly isolate one
    fixed simple critical zero, but the theorem has none of the stronger
    implications explicitly excluded in Section 6.
12. Six dyadic scales, or even infinitely many dyadic scales, do not yield the
    all-integer liminf without a separate interscale theorem.

## 9. Surviving frontier

For one fixed nondegenerate \(I\Subset(0,2)\), the unresolved theorem remains

\[
 \boxed{
 \exists\kappa>0,\ a_0:\quad
 D_a(I)\ge\frac{\kappa}{(\log a)^3}
 \quad\text{for every integer }a\ge a_0.}
 \tag{9.1}
\]

Since \((\log a)^2\Delta_a(I)\to A_{\theta,I}>0\), this is equivalent to

\[
 \boxed{
 \liminf_{a\to\infty}
 \log(a)\frac{D_a(I)}{\Delta_a(I)}>0.}
 \tag{9.2}
\]

Three available sufficient attack surfaces are:

1. the original weighted two-point Möbius packet inequality from Cycle 45;
2. the stronger one-generator projection bound
   \(\mathcal Q_a(I)\gg L^{-3}\); or
3. on \(I_0=[1,3/2]\), the stronger two-generator bound
   \(Q_a^{(2)}\gg L^{-3}\).

None is proved.  Even (9.1) would reach only the trace-based moving-retention
checkpoint.  Completed-square closure still requires a budget upper bound with
explicit constants and a strict comparison.  Burnol's cited theorem gives a
lower budget bound, which has the wrong direction for that final step.  No RH
conclusion is established.
