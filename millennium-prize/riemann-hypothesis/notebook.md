# Notebook

## Tick 1 — exact finite enclosure lemma

Fix integers `N >= 3` and `Q >= N`, and set `epsilon=1/Q`. Define `c_a` and
`F_N` as in `routes.md`, and

\[
A_N=\sum_{a\le N}c_a/a,\qquad M_N=1+\sum_{a\le N}|c_a|.
\]

Let the sorted breakpoint set be

\[
\mathcal B=\{1/Q,1\}\cup
\{1/(ak):1\le a\le N,\ 1\le k\le\lfloor Q/a\rfloor\}.
\]

### Lemma 1 (finite exact enclosure)

If consecutive distinct points of `B` are `l<r`, choose any rational
`m in (l,r)` and put

\[
n_a(l,r)=\lfloor1/(am)\rfloor,
\quad B_{l,r}=1-\sum_{a\le N}c_an_a(l,r).
\]

Then

\[
S_{N,Q}\le\|F_N\|_2^2\le S_{N,Q}+M_N^2/Q,
\]

where

\[
S_{N,Q}=A_N^2+\sum_{(l,r)}\left[
A_N^2(1/l-1/r)+2A_NB_{l,r}\log(r/l)+B_{l,r}^2(r-l)
\right].
\]

### Proof

Every discontinuity of `floor(1/(ax))` in `[1/Q,1]` is `1/(ak)` with
`k <= floor(Q/a)`. Hence on `(l,r)`,

\[
F_N(x)=A_N/x+B_{l,r},
\]

and direct integration gives the summand. For `x>1`, all floors vanish and
`F_N(x)=A_N/x`, whose squared integral is `A_N^2`. On `(0,1/Q)`, each
fractional part lies in `[0,1)`, so `|F_N| <= M_N`; integration gives the
stated omitted-origin bound. Endpoints have measure zero. QED.

This is an exact reduction to rational arithmetic and certified logarithms;
it is not an asymptotic theorem. The crude origin error grows with the
coefficient `l1` norm and must never be replaced by `1/Q`.

## Tick 2 — periodic tail lemma proved

After `t=1/x`, the omitted part is

\[
\int_Q^\infty |1+\sum_{a\le N}c_a\{t/a\}|^2\,dt/t^2.
\]

The numerator is periodic with period `L=lcm(1,...,N)`.

### Lemma 2 (period-average tail enclosure)

Put

\[
g_N(t)=1+\sum_{a\le N}c_a\{t/a\},\qquad
\mathcal A_N=\frac1L\int_0^L g_N(t)^2dt.
\]

For every real `Q > 0`,

\[
\boxed{
 \frac{\mathcal A_N}{Q+L}
 \le \int_Q^\infty\frac{g_N(t)^2}{t^2}dt
 \le \mathcal A_N\left(\frac1Q+\frac L{Q^2}\right).}
\]

Moreover the period average has the finite closed form

\[
\boxed{
\mathcal A_N=
\left(1+\frac12\sum_{a\le N}c_a\right)^2+
\frac1{12}\sum_{a,b\le N}c_ac_b
\frac{\gcd(a,b)^2}{ab}.}
\]

### Proof

Write `h=g_N^2`. It is nonnegative and `L`-periodic. On the block
`[Q+jL,Q+(j+1)L]`, monotonicity of `t^-2` and invariance of the integral of
`h` under a phase shift give

\[
\frac{L\mathcal A_N}{(Q+(j+1)L)^2}
\le \int_{Q+jL}^{Q+(j+1)L}\frac{h(t)}{t^2}dt
\le\frac{L\mathcal A_N}{(Q+jL)^2}.
\]

For the decreasing function `x -> (Q+Lx)^-2`, integral comparison gives

\[
\sum_{j\ge0}\frac1{(Q+(j+1)L)^2}\ge\frac1{L(Q+L)},
\]

and

\[
\sum_{j\ge0}\frac1{(Q+jL)^2}
\le\frac1{Q^2}+\frac1{LQ}.
\]

Summing proves the enclosure.

For the closed form, over any common period,

\[
\operatorname{avg}\{t/a\}=\frac12,
\quad
\operatorname{avg}\left[
(\{t/a\}-\tfrac12)(\{t/b\}-\tfrac12)
\right]=\frac{\gcd(a,b)^2}{12ab}.
\]

The second identity follows by reducing to the common period
`lcm(a,b)` and summing the elementary integrals between its integer
breakpoints (equivalently, the first periodic Bernoulli polynomial
correlation). The convention for the centered sawtooth at its jump points is
irrelevant to these integrals. Expanding `g_N^2` yields the formula. QED.

### Assessment

This replaces the coefficient-`l1` error by the exact mean square, but its
relative slack is controlled by `L/Q`. Since `lcm(1,...,N)` grows
exponentially, taking `Q >> L` is unsuitable for an efficient large-`N`
certificate. The lemma is nevertheless an exact theorem and a useful audit:
it exposes that bare periodicity alone cannot supply a polynomial-cost tail
bound.

## Tick 3 — pair-period discrepancy and strategic falsification

The queued request for merely *some* polynomial incomplete-period discrepancy
bound is too weak: pairwise expansion gives one immediately.

Put

\[
\beta_a(t)=\{t/a\}-\tfrac12,\qquad
C_N=1+\tfrac12\sum_{a\le N}c_a,
\]

so that `g_N=C_N+sum c_a beta_a` almost everywhere. For `d=(a,b)`, put

\[
\mu_{a,b}=\frac{d^2}{12ab},\qquad
L_{a,b}=\operatorname{lcm}(a,b)=\frac{ab}{d}.
\]

### Lemma 3 (elementary pair-period discrepancy)

For all real `T` and `H >= 0`,

\[
\left|\int_T^{T+H}\beta_a(t)dt\right|\le \frac a8
\]

and

\[
\left|\int_T^{T+H}
[\beta_a(t)\beta_b(t)-\mu_{a,b}]dt\right|
\le \frac{L_{a,b}}3.
\]

Consequently, if

\[
\mathcal A_N=C_N^2+\sum_{a,b\le N}c_ac_b\mu_{a,b},
\]

then

\[
\boxed{
\left|\int_T^{T+H}g_N(t)^2dt-H\mathcal A_N\right|
\le \frac{|C_N|}{4}\sum_{a\le N}a|c_a|
+\frac13\sum_{a,b\le N}|c_ac_b|L_{a,b}.}
\]

For the route coefficients `|c_a| <= 1`, this is `O(N^4)` uniformly in
`T,H`, with an absolute effective constant.

### Proof

The periodic primitive

\[
\frac a2 B_2(\{t/a\}),\qquad B_2(x)=x^2-x+\tfrac16,
\]

has derivative `beta_a` away from jumps. The oscillation of `B_2` on
`[0,1]` is `1/4`, proving the first bound. The function
`beta_a beta_b-mu_(a,b)` has period `L_(a,b)` and mean zero by Lemma 2.
Delete all complete pair periods from `[T,T+H]`. The remaining interval has
length below `L_(a,b)`, while

\[
|\beta_a\beta_b-\mu_{a,b}|\le\tfrac14+\tfrac1{12}=\tfrac13.
\]

This proves the pair bound. Expanding `g_N^2`, subtracting its mean, and
applying the triangle inequality gives the boxed estimate. Finally,
`L_(a,b)<=ab`, `|C_N|<=1+N/2`, and elementary sums give `O(N^4)`. QED.

### Strategic consequence

This proves the literal polynomial-discrepancy target but does **not** advance
the RH-strength estimate. Indeed the even simpler pointwise bound
`|g_N|<=N+1` already makes the weighted tail below `O(1/log N)` by taking a
polynomial cutoff `Q >> N^2 log N`. The hard part is the norm on the retained
range, not certification of the far tail. Pairwise absolute values erase the
Möbius cancellation.

This is a decisive falsification of the short-block route *at the strength
previously queued*. No rotation of the main RH funnel is warranted; the
bottleneck is sharpened instead.

## Tick 3 arithmetic audit — the period variance is elementary

The gcd quadratic form in `A_N` has the exact positive decomposition

\[
E_N:=\sum_{a,b\le N}c_ac_b\frac{(a,b)^2}{ab}
=\sum_{d\le N}\rho(d)
\left(\sum_{m\le N/d}\frac{c_{dm}}m\right)^2,
\quad
\rho(d)=\frac{J_2(d)}{d^2}\in(0,1].
\]

This follows from `(a,b)^2=sum_(d|a,d|b) J_2(d)` and finite rearrangement.
For the route coefficients, an absolute estimate already gives

\[
\boxed{0\le E_N\le\frac{14N}{(\log N)^2}\qquad(N\ge2).}
\]

To verify the constant, set `X=N/d`. Squareful `d` contribute zero. For
squarefree `d`, `mu(dm)=mu(d)mu(m)` when `(d,m)=1` and is zero otherwise, so

\[
\left|\sum_{m\le X}\frac{c_{dm}}m\right|
\le\frac{\log X+\frac12\log^2X}{\log N}.
\]

The summand is bounded by
`Phi(log(N/d))/log^2 N`, where
`Phi(t)=(t+t^2/2)^2`. Monotone integral comparison and `x=N exp(-t)` give

\[
\sum_{d\le N}\Phi(\log(N/d))
\le N\int_0^\infty(t^2+t^3+t^4/4)e^{-t}dt=14N.
\]

Thus neither the gcd variance nor the far tail is, by itself, the hidden
RH obstruction. At cutoff `Q=N`, however, a Fourier-tail argument does not
show that the constant mode dominates: distinct reduced frequencies can be
only `1/N^2` apart, so their products are effectively nonoscillatory on a
length-`N` scale.

## Next queued main-funnel step

Replace cutoff analysis by the known exact rational autocorrelation formula
for the complete Gram entry

\[
\langle\rho_a,\rho_b\rangle
=\int_0^\infty\{t/a\}\{t/b\}\,dt/t^2,
\]

which is expressible for rational `a/b` through finite Vasyunin cotangent
sums (Báez-Duarte--Balazard--Landreau--Saias, arXiv:math/0306251). Independently
derive and verify every normalization, then expand the route coefficients.
The next exact lemma must isolate the signed Möbius--Vasyunin bilinear sum and
state a quantitatively sufficient cancellation bound. It must not replace
that signed sum by pairwise absolute values or claim that the constant Fourier
mode dominates.

## Tick 4 — exact full Gram reduction and domain audit

The rational autocorrelation formula supplies a cutoff-free finite expression.
An initial audit incorrectly appended the correction appropriate to a
restricted `(0,1)` Gram matrix. A second independent domain audit caught this:
the route uses the full Hilbert space `L^2((0,infinity),dx)`, so no subtraction
is present. The corrected full-space derivation follows.
Set

\[
\rho_a(x)=\{1/(ax)\},\quad \chi=1_{(0,1)},\quad
C_0=\log(2\pi)-\gamma.
\]

For coprime positive integers `p,q`, use the convention

\[
V(p,q)=\sum_{k=1}^{q-1}\{kp/q\}\cot(\pi k/q),\qquad V(p,1)=0.
\]

For `d=(a,b)`, `p=a/d`, `q=b/d`, and `l=lcm(a,b)`, the published rational
autocorrelation formula and the change of variables `t=1/x` give

\[
\boxed{
\langle\rho_a,\rho_b\rangle=
\frac{(q-p)\log(p/q)+(p+q)C_0
-\pi[V(p,q)+V(q,p)]}{2l}.}
\]

Indeed `t=1/x` maps the complete half-line to itself and gives exactly the
published autocorrelation. The restricted Gram entry over `x in (0,1)` is the
one equal to the displayed full entry minus `1/(ab)`, because its omitted
`x>1` tail is `integral_1^infinity dx/(abx^2)=1/(ab)`. Checks include

\[
\langle\rho_a,\rho_a\rangle=C_0/a
\]

and

\[
\langle\chi,\rho_a\rangle=(\log a+1-\gamma)/a.
\]

Primary sources: Báez-Duarte, arXiv:math/0202141, for the raw functions on
`L^2(0,infinity)`; and Báez-Duarte--Balazard--Landreau--Saias,
arXiv:math/0306251, for the rational multiplicative autocorrelation formula.
Raw functions restricted to `(0,1)` require the rank-one subtraction, but that
is not this route's Hilbert space.

### Exact route identity

Write `L=log N`,

\[
w_a=\mu(a)(L-\log a),\qquad c_a=w_a/L,
\]

and define

\[
M_0=\sum_{a\le N}w_a,\quad M_1=\sum_{a\le N}w_a/a,
\]

\[
L_0=\sum_{a\le N}w_a\log a,\quad
L_1=\sum_{a\le N}w_a\log a/a.
\]

Finally put

\[
\mathcal V_N=\frac\pi2\sum_{a,b\le N}w_aw_b\frac{(a,b)}{ab}
\left[V\left(\frac a{(a,b)},\frac b{(a,b)}\right)
+V\left(\frac b{(a,b)},\frac a{(a,b)}\right)\right].
\]

Finite expansion of the Gram form gives the exact identity

\[
\boxed{
\begin{aligned}
\|F_N\|_2^2={}&1+\frac2L[L_1+(1-\gamma)M_1]\\
&+\frac1{L^2}[C_0M_0M_1+M_0L_1-M_1L_0
-\mathcal V_N].
\end{aligned}}
\]

Here the elementary kernel factorizations are

\[
\sum_{a,b}w_aw_b\frac{a+b}{2ab}=M_0M_1,
\]

\[
\sum_{a,b}w_aw_b\frac{b-a}{2ab}\log(a/b)=M_0L_1-M_1L_0,
\]

All sums are finite, so no convergence interchange occurs.

Define the combined signed quantity

\[
\mathcal W_N=\mathcal V_N-M_0L_1+M_1L_0.
\]

Then, for any fixed `C*>0`, the desired estimate at this `N` is exactly

\[
\boxed{
\|F_N\|_2^2\le C_*/L
\iff
\mathcal W_N\ge
L^2+2L[L_1+(1-\gamma)M_1]+C_0M_0M_1-C_*L.}
\]

This is an equivalent finite reformulation, not progress on the inequality.
Cotangent reciprocity does not annihilate the symmetric Vasyunin sum, and
termwise bounds `|V(p,q)| << q log q` are far too large after absolute
summation.

### Audit incident and invariant

The erroneous `-1/(ab)` survived one adversarial pass because that pass
silently changed the inner-product domain to `(0,1)`. It was committed briefly
and is corrected here explicitly. Future Gram audits must begin by writing the
integration domain before applying `t=1/x`. The invariant is

\[
G^{(0,\infty)}_{ab}=G^{(0,1)}_{ab}+1/(ab),
\]

a positive rank-one tail correction. The target cross term is unchanged
because `chi` vanishes for `x>1`.

## Next queued main-funnel step

Derive exact small-`N` values of `mathcal W_N` in a symbolic field generated
by logarithms, `pi`, cotangents, and `gamma`, independently checking the Gram
identity against breakpoint integration. Use the data only to test structural
decompositions. In parallel, rewrite `mathcal V_N` through Estermann values
and Bettin--Conrey reciprocity and seek a signed bilinear transform that
preserves the Möbius coefficients. The next candidate lemma must give the
displayed lower bound for `mathcal W_N` uniformly; any use of RH-level Mertens
cancellation or unqualified cotangent cancellation is circular or false.

## Tick 5 — exact small cases and the Estermann operator obstruction

The script `verify_small_gram.py` checks the following identities symbolically.
For `N=2`, the endpoint coefficient at `a=2` vanishes and

\[
\boxed{\|F_2\|_2^2=3+\log(2\pi)-3\gamma.}
\]

For `N=3`, put

\[
r=\frac{\log(3/2)}{\log3},\qquad a=1-r/2.
\]

Then `F_3=chi+rho_1-r rho_2` and

\[
\boxed{
\|F_3\|_2^2=1-\log2+a(2-\log\pi-\gamma)
+2a^2(\log(2\pi)-\gamma).}
\]

These follow both from the full Gram entries

\[
G_{11}=C_0,\quad G_{22}=C_0/2,\quad
G_{12}=(3C_0-\log2)/4
\]

and from splitting the transformed integral into alternating unit intervals.
In the latter computation the interval `0<t<1` contributes the full-space
tail and independently detects the forbidden restricted-domain subtraction.

### Exact Estermann reindexing

Let

\[
D_{\sin}(s,x)=\sum_{n\ge1}\tau(n)\sin(2\pi nx)n^{-s}
\]

by analytic continuation (or Abel limiting) at `s=1`. With our convention,

\[
V(p,q)=-\frac{2q}{\pi^2}D_{\sin}(1,p/q).
\]

Writing `a=dp`, `b=dq`, `(p,q)=1`, gives the sign-preserving identity

\[
\boxed{
\mathcal V_N=-\frac2\pi\sum_{d\le N}\frac1d
\sum_{\substack{p,q\le N/d\\(p,q)=1}}
\frac{w_{dp}w_{dq}}pD_{\sin}(1,p/q).}
\]

The Abel limit is essential if the defining sine series is inserted; an
unqualified interchange with the finite arithmetic sums is not permitted.

Combining the elementary logarithmic kernel, define for `1<=p,q<=X`

\[
\begin{aligned}
\mathsf H_X(p,q)=1_{(p,q)=1}\bigg[&-\frac1\pi\left(
\frac{D_{\sin}(1,p/q)}p+\frac{D_{\sin}(1,q/p)}q\right)\\
&+\frac{p-q}{2pq}\log(p/q)\bigg].
\end{aligned}
\]

Then, with `w^(d)_p=w_(dp)`,

\[
\boxed{
\mathcal W_N=\sum_{d\le N}\frac1d
\langle w^{(d)},\mathsf H_{\lfloor N/d\rfloor}w^{(d)}\rangle.}
\]

This is exact and preserves every Möbius sign.

### Decisive positivity failure

The operator is indefinite already on indices `{1,2}`. Since the relevant
Estermann sine values vanish there,

\[
\mathsf H_2|_{\{1,2\}}=
\begin{pmatrix}0&\log2/4\\\log2/4&0\end{pmatrix},
\]

whose eigenvalues are `+-log(2)/4`. Thus no generic PSD argument can prove the
required lower bound. More intrinsically, the symmetric Vasyunin kernel is an
elementary rank-four kernel minus a positive fractional-part Gram kernel; it
is nonpositive only after imposing two moment constraints, neither of which
the route vectors satisfy identically.

Sign-blind large-sieve bounds naturally lose a factor of order `N` and control
absolute size rather than the required positive lower main term. Bettin--Conrey
reciprocity also does not telescope after Möbius reindexing: the descendant
pair is governed by a modular inverse, changing the Möbius factors, logarithmic
weights, cutoff, and leaving a nonzero period-function remainder.

### Candidate-strength audit

The coarse `O(1/log N)` estimate for these particular approximants implies RH,
but is not known to follow from RH alone. The sharp asymptotic is known under
RH plus a reciprocal-derivative moment. Multiple zeros create higher
principal parts in the contour formula, but current lower bounds do not prove
that the coarse big-O estimate forces simplicity. The route must therefore
describe its candidate honestly as an RH-implying explicit-rate conjecture,
not as a theorem known equivalent to RH.

## Next queued main-funnel step

The exact operator reformulation is now complete and generic positivity is
falsified. The next target is a **Möbius-vector-specific** identity: apply the
Mellin representation of `w_(dp)` before Estermann reciprocity and derive a
double-contour formula for `mathcal W_N` in which all poles and diagonal terms
are explicit. Simultaneously seek a frequency-isolating lower bound for the
multiple-zero residue contribution. A useful result must either (i) reveal a
new positive main term for these exact vectors, or (ii) prove that the chosen
`O(1/log N)` approximant conjecture is strictly stronger than RH.

## Tick 6 — double Mellin formula and a weaker positive RH certificate

For `w_N(n)=mu(n) log(N/n) 1_(n<=N)` and every `c>0`,

\[
\boxed{w_N(n)=\frac{\mu(n)}{2\pi i}\int_{(c)}
\left(\frac Nn\right)^u\frac{du}{u^2}.}
\]

The integral is absolute and the endpoint `n=N` is exactly zero. Let

\[
H(p,q)=\frac{(p-q)\log(p/q)+\pi[V(p,q)+V(q,p)]}{2pq}
\quad((p,q)=1).
\]

The full Gram identity gives `H(p,q)=C_0(p^-1+q^-1)/2-G(p,q)`, where

\[
G(p,q)=\frac1{2\pi i}\int_{(c)}
\frac{\zeta(s)\zeta(1-s)}{s(1-s)}p^{-s}q^{s-1}ds,
\quad 0<c<1.
\]

For `Re(u),Re(v)>1`, define

\[
\begin{aligned}
\Phi(u,v)={}&\frac{C_0}{2}\left[
\frac1{\zeta(u+1)\zeta(v)}+
\frac1{\zeta(u)\zeta(v+1)}\right]\\
&-\frac1{2\pi i}\int_{(c)}
\frac{\zeta(s)\zeta(1-s)}
{s(1-s)\zeta(u+s)\zeta(v+1-s)}ds.
\end{aligned}
\]

Then

\[
\boxed{\mathcal W_N=\frac1{(2\pi i)^2}\int_{(c_u)}\int_{(c_v)}
\Phi(u,v)\frac{N^{u+v}}{u^2v^2}\,dv\,du,
\qquad c_u,c_v>1.}
\]

All operations are absolute initially. The Euler-product collapse uses
`1-l^-A-l^-B+l^-(A+B)=(1-l^-A)(1-l^-B)` and depends on including the gcd
variable. The coprime diagonal is only `p=q=1`, and `H(1,1)=0`; hence there is
no positive diagonal main term. Contour shifts meet reciprocal-zeta poles from
the complete zero set, and diagonal vanishing does not imply axis vanishing of
`Phi`.

### A weaker positive certificate

Put

\[
A_N=V_N(1)=\sum_{a\le N}c_a/a,
\qquad P_N=\int_0^1|F_N(x)|^2dx.
\]

Since `F_N(x)=A_N/x` for `x>1`,

\[
\boxed{\|F_N\|_{L^2(0,\infty)}^2=P_N+A_N^2.}
\]

The Vinogradov--Korobov zero-free region gives unconditionally

\[
\boxed{A_N=\frac1{\log N}+O\left(\frac{e^{-c(\log N)^{3/5}
(\log\log N)^{-1/5}}}{\log N}\right)}
\]

for some `c>0`; the sign check is `sum mu(n)log(n)/n=-1`.

If `rho=sigma+i gamma` is a nontrivial zero with `1/2<sigma<1`, then

\[
\int_0^1F_N(x)x^{\rho-1}dx=\frac1\rho-\frac{A_N}{1-\rho}.
\]

Cauchy--Schwarz and minimization over real `A` prove

\[
\boxed{P_N\ge
\frac{(2\sigma-1)\gamma^2}{|\rho|^4|1-\rho|^2}>0.}
\]

The Hilbert-space test vector is `x^(conjugate(rho)-1)`. A left-half zero is
first reflected to a right-half zero. Therefore

\[
\boxed{\liminf_{N\to\infty}P_N=0\quad\Longrightarrow\quad RH.}
\]

Because `A_N->0`, this supplies a convergent subsequence in the full criterion.
The converse is **not known for this fixed logarithmic taper**: RH gives
existence of approximants and convergence of a differently damped explicit
family, but the cited literature does not prove convergence of this exact
family under RH alone.

For finitely many right-half zeros, projection onto their power functions
gives a stronger positive floor through the Cauchy Gram matrix
`G_ij=1/(rho_i+conjugate(rho_j)-1)`.

### Multiple-zero route closed at the proposed strength

A formally large residue assigned to a multiple zero has no norm lower bound
until its remainder is controlled. Burnol's rigorous bound puts multiplicity
into the constant `sum m(rho)^2/|rho|^2` while retaining the `1/log N` scale.
Thus an unspecified `O(1/log N)` upper constant is compatible with multiple
zeros. Frequency isolation cannot prove strict strength over RH from
multiplicity alone and is abandoned at that strength.

## Next queued main-funnel step

Pivot to the positive restricted energy `P_N`. Derive its finite-zero
Hardy/Cauchy Gram obstruction for symmetric hypothetical zero sets and optimize
the determinant to obtain the strongest explicit certificate. In parallel,
seek an unconditional contraction, recurrence, or monotonic subsequence
mechanism forcing `liminf P_N=0`; any such result would prove RH. Do not claim
that RH implies convergence of this fixed taper.

## Tick 7 — finite-zero certificate and recurrence obstruction

The following is classical finite-dimensional Hardy-space interpolation,
specialized to the restricted energy. It is recorded because it gives the
exact hostile certificate generated by any hypothetical finite set of
right-half zeros; no novelty is claimed for the RKHS mechanism.

### Lemma 4 (finite-zero Cauchy Gram floor)

Let `rho_1,...,rho_m` be distinct nontrivial zeros with
`Re(rho_j)>1/2`. Define

\[
u_j=1/\rho_j,\qquad v_j=1/(1-\rho_j),
\qquad G_{ij}=1/(\rho_i+\overline{\rho_j}-1).
\]

Then `G` is Hermitian positive definite. With `H=G^-1`, every `N` satisfies

\[
\boxed{P_N\ge(u-A_Nv)^*H(u-A_Nv).}
\]

Discarding the known value of the real number `A_N` and optimizing over all
real `A` gives the uniform floor

\[
\boxed{P_N\ge\mathcal L_R:=
u^*Hu-\frac{[\Re(v^*Hu)]^2}{v^*Hv}>0.}
\]

The Cauchy determinant is

\[
\boxed{\det G=
\frac{\prod_{i<j}|\rho_i-\rho_j|^2}
{\prod_i(2\Re\rho_i-1)
\prod_{i<j}|\rho_i+\overline{\rho_j}-1|^2}>0.}
\]

### Proof

Put `h_j(x)=x^(conjugate(rho_j)-1)` in `L^2(0,1)`. Its Gram matrix is
exactly `G`. Distinct exponentials are linearly independent after `x=e^-t`,
so `G>0`. At a zero,

\[
\langle h_j,F_N\rangle=1/\rho_j-A_N/(1-\rho_j).
\]

The squared norm of the orthogonal projection of `F_N` onto the span of the
`h_j` is `(u-A_Nv)^*G^-1(u-A_Nv)`, proving the first claim. Completing the
real quadratic in `A` proves the optimized formula. Equality in its
Cauchy--Schwarz proof would require `u=Av` for a real `A`, but
`(1-rho_j)/rho_j` is nonreal for a nontrivial zero. The determinant is the
standard Cauchy determinant. QED.

Because `A_N->0`, the sharper asymptotic consequence is

\[
\boxed{\liminf_{N\to\infty}P_N\ge u^*G^{-1}u.}
\]

For one zero this is `(2 sigma-1)/|rho|^2`, stronger than the uniform
real-tail floor. More generally the Cauchy bordered-determinant identity gives

\[
\boxed{u^*G^{-1}u=1-
\prod_{j=1}^m\frac{|1-\rho_j|^2}{|\rho_j|^2}.}
\]

For a conjugate pair `rho=beta+i gamma`, `conjugate(rho)`, set
`d=2 beta-1`. The optimized uniform restricted floor is

\[
\boxed{\mathcal L_{\rho,\bar\rho}=
\frac{2d(d^2+4\gamma^2)}
{|\rho|^4(d^2+4\gamma^2+1)}>0.}
\]

The script `verify_zero_gram.py` checks this identity symbolically.

### Exact scale recurrence

At integer scales, the endpoint coefficient is zero and all previous
coefficients move. Put

\[
h_N=1/\log N-1/\log(N+1),\qquad
D_N=\sum_{a\le N}\mu(a)\log a\,\rho_a.
\]

Then exactly

\[
F_{N+1}=F_N+h_ND_N
\]

on `(0,1)`, and

\[
\boxed{P_{N+1}-P_N=
2h_N\langle F_N,D_N\rangle+h_N^2\|D_N\|^2.}
\]

Thus monotonicity is equivalent to the new Möbius-specific negative-correlation
inequality

\[
\langle F_N,D_N\rangle\le-h_N\|D_N\|^2/2.
\]

Positivity of the restricted Gram matrix controls only the final quadratic
term and gives no sign for the mixed term.

For real `X` between successive integers, write `t=log X` and

\[
U_n=\chi+\sum_{a\le n}\mu(a)\rho_a,
\qquad D_n=\sum_{a\le n}\mu(a)\log a\,\rho_a.
\]

Then

\[
F_X=U_n-D_n/t,\qquad
P_X=\|U_n\|^2-2\langle U_n,D_n\rangle/t+\|D_n\|^2/t^2.
\]

This is a convex quadratic in `1/t`, not a contraction toward zero. Its target
`U_n` jumps at squarefree integers. Global convexity already fails at `X=2`:
the derivative jump is

\[
\frac{2\mu(2)}{\log2}\langle F_2,\rho_2\rangle<0.
\]

Exact calculations give `P_2>P_3>P_4>P_5`, but the scaled sequence
`(log N)P_N` increases from `N=2` to `N=3`; hence scaled monotonicity is
falsified at the first nontrivial step. These facts are audits, not evidence
for global decrease. Even global decrease alone would not identify the limit
as zero.

## Next queued main-funnel step

The only viable recurrence target exposed here is the mixed-correlation
inequality for `D_N`, but proving it alone is insufficient unless accompanied
by a quantitative decrement whose sum forces zero. Derive a lower bound for
`-<F_N,D_N>` in terms of `P_N` and explicit Möbius moments, and search exact
moderate `N` for sign failures using certified Gram entries. In parallel,
investigate logarithmic averaging of `P_X`: an unconditional averaged value
tending to zero would imply `liminf P_N=0` and hence RH, while any argument
that imports critical-line Möbius cancellation must be rejected as circular.

## Tick 8 — sharp decrement scale and logarithmic averaging

Put

\[
Q_N=-\langle F_N,D_N\rangle,\qquad R_N=\|D_N\|^2,
\qquad h_N=1/\log N-1/\log(N+1).
\]

The exact recurrence is

\[
\boxed{P_N-P_{N+1}=2h_NE_N,\qquad
E_N:=Q_N-\frac{h_N}{2}R_N.}
\]

This identifies the correct quantity: a lower bound for `Q_N` alone is
incomplete because the quadratic cost can erase it.

### Lemma 5 (sufficient effective decrement)

If there are constants `kappa>0,N_0` such that

\[
\boxed{E_N\ge\kappa P_N\log N\qquad(N\ge N_0),}
\]

then `P_N->0`, hence RH.

### Proof

The recurrence gives

\[
P_{N+1}\le P_N(1-2\kappa h_N\log N).
\]

Now `h_N log N ~ 1/(N log N)`, whose sum diverges, while its square is
summable. The standard infinite-product argument forces `P_N->0`. QED.

The scale is sharp. If the expected law `P_N~C/log N` is locally regular, then

\[
E_N\sim C/2\sim P_N\log N/2.
\]

Thus an eventual coefficient above `1/2` would conflict with the expected
law, while any fixed positive coefficient suffices for RH. By contrast,
`Q_N >= c P_N` is strategically useless because `sum h_N<infinity`.

At `N=2`, exact formulas disprove an all-`N` coefficient `1/2`. A separate
rigorous Arb search certified

\[
\langle F_N,D_N\rangle<0,\qquad P_{N+1}<P_N
\]

for every `2<=N<=250`; the closest correlation occurred at `N=221`. This is
only a bounded certificate and supplies no asymptotic inference.

### Exact logarithmic averages

For `L_n=log n`, and on `L_n<=t<=L_(n+1)`, write

\[
F_{e^t}=U_n-D_n/t,
\quad A_n=\|U_n\|^2,
\quad B_n=\langle U_n,D_n\rangle,
\quad C_n=\|D_n\|^2.
\]

Then the exact cell integral is

\[
\boxed{
\begin{aligned}
I_n:=\int_{L_n}^{L_{n+1}}P_{e^t}dt
={}&(L_{n+1}-L_n)A_n
-2\log(L_{n+1}/L_n)B_n\\
&+(L_n^{-1}-L_{n+1}^{-1})C_n.
\end{aligned}}
\]

Summing the cells gives the complete logarithmic average with only an explicit
incomplete final cell. Integration by parts telescopes endpoints but leaves
the same mixed correlation:

\[
\boxed{
\int_{\log2}^{T}P_{e^t}dt
=TP_{e^T}-(\log2)P_2
-2\int_{\log2}^{T}\frac{\langle F_{e^t},D_{\lfloor e^t\rfloor}\rangle}{t}dt.}
\]

Thus averaging does not algebraically remove the obstruction.

There is also the exact Cesaro identity

\[
\boxed{F_X=\frac1{\log X}\int_1^XU_y\frac{dy}{y}.}
\]

Jensen yields

\[
P_X\le\frac1{\log X}\int_1^X\|U_y\|^2\frac{dy}{y},
\]

with exact nonnegative defect equal to half the weighted double average of
`||U_s-U_t||^2`. This is not contraction toward the latest approximant:
already `P_3>||U_2||^2`. Hence Cesaro smoothing merely moves the missing
Möbius cancellation into averaged sharp-truncation energies.

Finally, any normalized positive logarithmic average of `P_X` tending to zero
forces `liminf P_N=0`: within each logarithmic cell,
`||F_X-F_n||=o(1)` uniformly by the elementary bound on `h_n||D_n||`.
But the critical-line Mellin expansion of the average contains a nonnegative
covariance term and remains a fixed-mollifier reciprocal-zeta estimate. Its
decay is RH-implying, not elementary smoothing.

## Next queued main-funnel step

The active exact lemma is now the effective decrement inequality for `E_N`.
Decompose `E_N` into its finite mixed Vasyunin term and elementary Möbius
moments, and seek an averaged inequality

\[
\sum_{N\le n<2N}h_nE_n\ge
\kappa\sum_{N\le n<2N}h_nP_n\log n
\]

for some absolute `kappa>0`. This dyadic/logarithmic version is sufficient if
iterated and may tolerate the observed local oscillations. Simultaneously seek
a certified sign failure beyond `N=250`; either outcome is structurally
decisive. Any proof replacing finite Möbius polynomials by `1/zeta` on the
critical line is circular.

## Tick 9 — dyadic telescope, quantifier correction, and extended certificates

The proposed dyadic numerator contains no new interior structure. Exactly,

\[
\boxed{\sum_{N\le n<2N}h_nE_n=\frac{P_N-P_{2N}}2.}
\]

Hence the dyadic target is equivalent to

\[
\boxed{P_N-P_{2N}\ge
2\kappa\sum_{N\le n<2N}w_nP_n,
\qquad w_n=h_n\log n.}
\]

The block weight satisfies

\[
\frac{\log2}{\log(2N)}\le
W_N:=\sum_{N\le n<2N}w_n
\le\frac{\log2}{\log N}.
\]

### Lemma 6 (correct dyadic implication)

If one fixed `kappa>0` satisfies the boxed block inequality on every block in
an eventual dyadic partition `[N_j,2N_j)`, `N_(j+1)=2N_j`, then

\[
\boxed{\liminf_{n\to\infty}P_n=0,}
\]

and therefore RH.

### Proof

Summing block inequalities telescopes the endpoints and gives

\[
2\kappa\sum_{n\ge N_0}w_nP_n\le P_{N_0}<\infty.
\]

But `sum w_n=infinity`. If `liminf P_n>0`, the left side diverges. QED.

This does **not** prove `P_n->0` or even decay of dyadic endpoints. An abstract
sequence can put small values in block interiors while retaining positive
endpoint values. The stronger endpoint condition

\[
\sum_{N\le n<2N}h_nE_n\ge\kappa W_NP_N
\]

does force dyadic endpoint decay, since `sum_j W_(2^jN_0)=infinity`. The
weaker weighted-interior condition is nevertheless sufficient for RH because
our established criterion needs only a zero liminf.

Expanding the weighted denominator gives an exact positive variance kernel,
but no comparison with the endpoint drop. Its only genuinely non-elementary
term remains a Möbius-weighted Vasyunin sum with an explicit max-tail
coefficient. Thus dyadic averaging reorganizes but does not remove the same
arithmetic obstruction.

### Finite certificates

Arb calculations certify positive dyadic ratios through `[512,1024)`; the
tested power-of-two block ratios range from about `0.444` to `0.997`. These are
finite facts only. A separate reconnaissance through `N=2000` found no sign
failure. Rigorous breakpoint certificates for the structurally weak candidates
give

\[
\langle F_{592},D_{592}\rangle<0,\quad P_{593}-P_{592}<0,
\]

and

\[
\langle F_{1418},D_{1418}\rangle<0,\quad P_{1419}-P_{1418}<0.
\]

The reproducible script `certify_restricted_jump.py` performs this exact
breakpoint/Arb certification with a conservative omitted-origin enclosure.
No finite range supports an asymptotic claim.

## Next queued main-funnel step

The dyadic inequality is now known to be exactly an endpoint-drop comparison.
Attack the stronger endpoint form

\[
P_N-P_{2N}\ge2\kappa W_NP_N,
\]

which has a clean multiplicative consequence and avoids uncontrolled interior
spikes. Derive `P_(2N)` directly from `P_N` by comparing the two coefficient
vectors in the restricted Gram space; seek a positive-square decomposition of
their difference plus one signed remainder. In parallel, certify endpoint
ratios on larger dyadic blocks. Any uniform `kappa>0` proves RH; generic Hilbert
convexity alone cannot establish it.

## Tick 10 — exact endpoint geometry and the transverse obstruction

Put

\[
\alpha_N=\frac{\log2}{\log(2N)},
\]

and define the normalized fresh-block vector

\[
H_N=\chi+\sum_{a\le N}\mu(a)\rho_a
+\sum_{N<a\le2N}\mu(a)\frac{\log(2N/a)}{\log2}\rho_a.
\]

Coefficient comparison gives the exact affine relation

\[
\boxed{F_{2N}=(1-\alpha_N)F_N+\alpha_NH_N.}
\]

The shell in `H_N` is essential; replacing `H_N` by the sharp truncation at
`N` makes the formula false.

### Lemma 7 (endpoint polarization)

For every `N>=2`,

\[
\boxed{
P_N-P_{2N}=\alpha_N(P_N-\|H_N\|^2)
+\alpha_N(1-\alpha_N)\|F_N-H_N\|^2.}
\]

Equivalently, put `Delta_N=F_N-H_N` and decompose

\[
\Delta_N=q_NF_N+Z_N,
\qquad Z_N\perp F_N.
\]

Then

\[
\boxed{
P_N-P_{2N}=(2\alpha_Nq_N-\alpha_N^2q_N^2)P_N
-\alpha_N^2\|Z_N\|^2.}
\]

### Proof

The first identity is the Hilbert-space variance identity for a convex
combination. The second follows from
`F_(2N)=(1-alpha_N q_N)F_N-alpha_N Z_N` and orthogonality. QED.

This hostile sign audit is decisive: the convexity formula contains a positive
square, but after projection the transverse remainder enters the endpoint
drop with a **negative** coefficient. Generic Hilbert geometry cannot prove
contraction. The exact endpoint target is equivalent to

\[
\boxed{
q_N-\frac{\alpha_N}{2}
\left(q_N^2+\frac{\|Z_N\|^2}{P_N}\right)
\ge\frac{\kappa W_N}{\alpha_N}.}
\]

Thus both sufficiently positive parallel correlation and control of the
transverse shell are required.

The same comparison in coefficient coordinates cancels the common old--old
quadratic form. All elementary pieces factor into finite Möbius moments; the
only non-elementary remainder is one signed old/new Vasyunin bilinear sum.
The new-index part has the exact gcd decomposition over coprime `p,q` with
`max(p,q)>N/d`. It has no known sign.

An abstract one-dimensional dictionary respecting the exact taper
coefficients can make `||F_(2N)||>||F_N||`; hence no coefficient-only convexity
argument is possible. The arithmetic fractional-part dictionary is essential.

### Extended finite endpoint certificates

Rigorous breakpoint/Arb enclosures certify positive endpoint contraction
ratios through the block `4096 -> 8192`. The conservative enclosure for
`8192 -> 16384` overlaps zero and is inconclusive, not a counterexample.
Reconnaissance centers remain positive. These are finite audits only.

## Next queued main-funnel step

The active exact obstruction is the transverse ratio

\[
\Theta_N=\alpha_N\|Z_N\|^2/(P_Nq_N)
\]

when `q_N>0`. Derive it directly as a Schur complement of the restricted Gram
matrix for the old vector and fresh block. Seek a Möbius-specific upper bound
`Theta_N<=2-delta` together with `q_N >> W_N/alpha_N`; these two statements
were the queued proposal at this tick, but Tick 11 shows they are insufficient
without also controlling `alpha_N q_N`. Simultaneously compute certified enclosures for
`q_N` and `Theta_N` on weak dyadic blocks to identify which factor actually
degenerates. Any argument dropping `Z_N` is invalid.

## Tick 11 — Schur complement and corrected contraction conditions

Write

\[
P=\|F_N\|^2,\qquad B=\|H_N\|^2,
\qquad C=\langle F_N,H_N\rangle,
\qquad \alpha=\alpha_N.
\]

The `2 by 2` restricted Gram determinant is

\[
\mathcal D=PB-C^2\ge0.
\]

For `Delta=F_N-H_N=qF_N+Z`, `Z perpendicular F_N`, one has

\[
\boxed{q=1-C/P,\qquad \|Z\|^2=\mathcal D/P.}
\]

When `q>0`, the transverse ratio has the exact Schur form

\[
\boxed{
\Theta=\frac{\alpha\|Z\|^2}{Pq}
=\alpha\frac{PB-C^2}{P(P-C)}.}
\]

The endpoint ratio factors as

\[
\boxed{
\frac{P_{2N}}{P_N}=1-\alpha q(2-\alpha q-\Theta).}
\]

Therefore strict contraction is equivalent to

\[
\boxed{q>0\quad\hbox{and}\quad \Theta+\alpha q<2.}
\]

This corrects the previously queued sufficient pair. A bound
`Theta<=2-delta` plus only a lower bound on `q` is insufficient: the
longitudinal penalty `alpha q^2` also requires an upper bound. A valid
separated sufficient condition is

\[
\Theta+\alpha q\le2-\delta,
\qquad q\ge cW_N/\alpha,
\]

which gives endpoint contraction with `kappa=c delta/2`.

### Old/fresh Schur decomposition

Let

\[
D=\sum_{a\le N}\mu(a)\log a\,\rho_a,
\]

and let `B_fresh` be the normalized fresh shell in `H_N`. Then
`H_N=F_N+D/log N+B_fresh`. Writing

\[
A=\langle F_N,D\rangle,\quad C_f=\langle F_N,B_{fresh}\rangle,
\]

\[
R=\|D\|^2,\quad U=\langle D,B_{fresh}\rangle,
\quad W=\|B_{fresh}\|^2,
\]

the determinant simplifies exactly to

\[
\boxed{
PB-C^2=\frac{PR-A^2}{(\log N)^2}
+(PW-C_f^2)+\frac2{\log N}(PU-AC_f).}
\]

The first two terms are nonnegative Gram minors. The sole signed obstruction is
the projected old/fresh correlation `PU-AC_f`. Its exact expansion retains
uncancelled Möbius--Vasyunin terms. Cauchy--Schwarz merely proves total Schur
positivity and gives no useful upper bound.

### Numerical factor audit

Reconnaissance through powers of two up to `8192` gives `q` near one and
`Theta` between roughly `0.02` and `0.06`; the dangerous threshold remains far
away. Retained-range Arb values at `8192` are very stable, but the current
absolute omitted-origin enclosure lets the full interval for the parallel
inner product cross zero. Thus these are not full certificates. The failure is
in the tail bound, not in the observed geometry.

The stronger norm condition `||H_N||<=||F_N||` is unnecessary and likely false
for the restricted dictionary at larger scales according to reconnaissance.
Endpoint contraction can persist because the correlation and transverse
Schur loss, not norm domination alone, control the convex combination.

## Next queued main-funnel step

Replace the coefficient-`l1` omitted-origin error by a cancellation-aware tail
certificate for the **three** Gram quantities `P,B,C`. Use the exact periodic
mean/gcd kernel for each coefficient vector and a short-block discrepancy bound
to certify `q` and `Theta` at `N=8192` without exponentially large cutoff. This
is a finite but structurally necessary test of whether the Schur formulation is
computationally certifiable. In parallel, attack the signed projected
old/fresh term `PU-AC_f` analytically; any bound must improve on bare
Cauchy--Schwarz and preserve Möbius signs.
