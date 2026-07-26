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

## Tick 12 — cancellation-aware tail theorem and certification frontier

Let

\[
g_u(t)=m_u+\sum_a u_a\beta_a(t),
\qquad \beta_a(t)=\{t/a\}-\tfrac12,
\]

and similarly `g_v`. Their exact period mean is

\[
\boxed{\mathcal A(u,v)=m_um_v+\frac1{12}
\sum_{a,b}u_av_b\frac{(a,b)^2}{ab}.}
\]

Using `(a,b)^2=sum_(d|a,d|b)J_2(d)`, this is computable in
`O(M log M)` divisor-transform operations:

\[
\sum_{a,b}u_av_b\frac{(a,b)^2}{ab}
=\sum_{d\le M}\frac{J_2(d)}{d^2}
\left(\sum_{j\le M/d}\frac{u_{dj}}j\right)
\left(\sum_{j\le M/d}\frac{v_{dj}}j\right).
\]

### Lemma 8 (signed periodic tail enclosure)

Suppose `K` is a bounded primitive of
`g_u g_v-mathcal A(u,v)` and `||K||_infinity<=D`. Then, for every `Q>0`,

\[
\boxed{
\int_Q^\infty\frac{g_u(t)g_v(t)}{t^2}dt
=\frac{\mathcal A(u,v)}Q-\frac{K(Q)}{Q^2}+\varepsilon_Q,
\qquad |\varepsilon_Q|\le D/Q^2.}
\]

### Proof

Integrate `K'(t)/t^2` by parts. Boundedness kills the endpoint at infinity,
and `2 int_Q^infinity |K(t)|t^-3 dt<=D/Q^2`. QED.

This handles signed cross-Gram entries and gains one power of `Q` over a
pointwise coefficient-`l1` tail. A rigorous pairwise primitive certificate is
polynomial-cost because every pair period is `lcm(a,b)<=M^2`; exact pair
extrema or the cheaper oscillation bound can be used. Symmetrizing the two
orientations preserves some coefficient cancellation before absolute values.

For the two-vector endpoint field, the nonnegative periodic-tail lemma also
has a matrix form. If `M` is the exact period-mean Gram matrix and `T_Q` the
tail Gram matrix, then

\[
\boxed{\frac1{Q+L}M\preceq T_Q\preceq
\left(\frac1Q+\frac L{Q^2}\right)M.}
\]

This couples all three entry errors in Loewner order, but its common period
`L=lcm(1,...,2N)` is exponential. It is structurally correct and
computationally useless at `N=8192` unless replaced by a matrix short-block
discrepancy.

### Quantitative verdict at `N=8192`

The exact gcd means for `(F,H)` are moderate, but the absolute pair-lcm
primitive bound is dominated by the `H,H` entry. It improves the old `l1`
enclosure by roughly one order of magnitude for `H,H` and much more for
`F,F`, yet at cutoff near `64` million its `H,H` uncertainty remains around
`10^-1`. A cutoff of several hundred million is predicted to give a useful
full Schur certificate. This is polynomial and reproducible, but still a large
finite computation, not an asymptotic advance.

Reduced-frequency Fourier aggregation is the only identified route likely to
close the remaining orders of magnitude at the existing cutoff: combine the
divisor sums

\[
U_s=\sum_{j\le M/s}u_{sj}/j
\]

at each reduced rational frequency before taking absolute values. A rigorous
implementation needs a finite-frequency truncation and an analytic remainder;
gcd grouping alone does not align primitive phases and is not a certificate.

An alternative exact finite certificate is a streamed Vasyunin Gram
contraction through index `2N=16384`. Direct cotangent summation per pair is
infeasible; a certified continued-fraction/period-function reciprocity engine
or multiplicative-unit-group transform is required. Such an artifact would
settle only the finite `8192 -> 16384` endpoint.

### Analytic projected-correlation audit

The signed term satisfies exactly

\[
PU-AC_f=P\langle D^\perp,B_{fresh}^\perp\rangle.
\]

Thus improving Cauchy is literally a nontrivial angle theorem for these two
specific Möbius vectors. Generic support separation, gcd sign, conditional
negative type, and Fourier orthogonality all fail. Even individual projected
old/fresh dictionary entries have both signs. Any valid improvement must use
the full Möbius logarithmic vectors and cannot be a dictionary-wide kernel
inequality.

## Next queued main-funnel step

Implement the reduced-frequency primitive certificate first on moderate `N`
and compare it against exact Vasyunin Gram values and breakpoint tails. The
exact target is a certified bound for the matrix functional

\[
2(P-C)-\alpha(P+B-2C),
\]

which equals `(P_N-P_(2N))/alpha` and avoids separately dividing to form
`q,Theta`. Once validated, scale the certificate to `N=8192`. In parallel,
formulate the projected old/fresh angle as a reduced-frequency bilinear form
and isolate the near-diagonal positive kernel from the off-diagonal remainder.

## Tick 13 — reduced-frequency theorem, validation, and scalability obstruction

For

\[
g_u(t)=m_u+\sum_{a\le M}u_a\beta_a(t),
\qquad U_q=\sum_{j\le M/q}u_{qj}/j,
\]

the Fourier coefficient at a nonzero reduced rational frequency `p/q` is

\[
\boxed{\widehat g_u(p/q)=-U_q/(2\pi i p).}
\]

This is the exact aggregation point: all divisibility representations of one
rational frequency are combined before any absolute value. If `L` is a common
period and `c_u(k)` are the coefficients on `k/L`, then the product coefficient

\[
\boxed{H(k)=\sum_jc_u(j)c_v(k-j)}
\]

is absolutely convergent for each fixed output `k` by `ell^2` Cauchy--Schwarz.
The zero output is removed as the exact gcd/divisor mean. For nonzero outputs,
the mean-zero product primitive has coefficients `L H(k)/(2 pi i k)`.

The script `verify_reduced_mean.py` checks with exact rational arithmetic:

1. the pair correlation `(a,b)^2/(12ab)` by direct piecewise integration;
2. equality of the gcd and Jordan-totient divisor forms for arbitrary rational
   coefficient vectors;
3. the direct endpoint-functional mean
   `2mn-alpha n^2 + (1/12) sum rho(s)(2U_sD_s-alpha D_s^2)`.

### Rigorous finite truncation

For a periodic product of bounded variation, output coefficients satisfy
`|H(k)|<=Var/(2 pi |k|)`. Hence the primitive output tail after `K` is at most

\[
\boxed{L\,Var/(2\pi^2K).}
\]

Finite input convolution can also be enclosed: for retained outputs
`|k|<=K`, truncate the input index at `J>K` and bound the omitted Diophantine
fiber using the `1/|j|` variation bounds. This is a mathematically complete
certificate after duplicate-frequency aggregation. It correctly handles the
fact that arbitrarily high input harmonics contribute to a fixed low output.

However, its common-period factor `L=lcm(1,...,M)` is exponential and destroys
scalability. The theorem validates the method but does not yield the desired
polynomial `N=8192` certificate.

### Direct endpoint cancellation

The direct endpoint integrand is

\[
q_N(t)=2f(t)d(t)-\alpha d(t)^2,
\qquad d=f-h.
\]

Its quadratic coefficient matrix in the sawtooth coefficients is rank at most
two, and its exact reduced-frequency mean is

\[
\boxed{\mathcal A_N=2mn-\alpha n^2+
\frac1{12}\sum_s\frac{J_2(s)}{s^2}
[2U_sD_s-\alpha D_s^2].}
\]

There is no `U_s^2` term: the large common endpoint mass cancels before
certification. A moderate-`N` prototype independently matched exact Vasyunin,
breakpoint, and periodic-tail evaluations and showed growing cancellation over
pairwise primitive bounds. This validates the algebraic direction.

### Decisive computational obstruction

An Abel-smoothed finite realization has controlled smoothing error of order
approximately `(log K)^2/K`, but at `N=8192` a useful harmonic cutoff produces
tens of millions of reduced modes. The finite weighted-tail kernel couples
essentially every pair of modes, leading to an infeasible dense bilinear sum.
Ordinary FFT binning is unsafe because near-diagonal rational spacings can be
`1/M^2`, precisely where the kernel is largest.

Thus reduced-frequency aggregation is mathematically sound and validated at
moderate `N`, but it is not yet a practical `8192` certificate. The missing
ingredient is a rigorous fast treatment of the weighted near-diagonal kernel,
not a Fourier convergence theorem.

## Next queued main-funnel step

Derive a near/far decomposition of the exact weighted kernel

\[
C_Q(2\pi|\lambda-\mu|)-C_Q(2\pi(\lambda+\mu))
\]

for reduced rational frequencies. Treat near pairs exactly by Farey-neighbor
enumeration and bound far pairs collectively by summation by parts or a
certified low-rank expansion. The goal is a subquadratic interval algorithm for
the direct endpoint bilinear form. Simultaneously construct hostile rational
frequency sets to test every proposed far-kernel low-rank bound. Without this
kernel theorem, scaling the validated Fourier route is computationally blocked.

## Tick 14 — interval-ready kernel theorem and failure of neighbor-only splitting

Define

\[
C_Q(\omega)=\int_Q^\infty\cos(\omega t)t^{-2}dt
=Q^{-1}F(Q|\omega|),
\]

where

\[
F(x)=\cos x-\frac{\pi x}{2}+x\operatorname{Si}(x).
\]

### Lemma 9 (certified near/far expansions)

For `x>=0`,

\[
\boxed{F(x)=1-\frac{\pi x}{2}+
\sum_{m\ge1}\frac{(-1)^{m+1}x^{2m}}{(2m-1)(2m)!}.}
\]

On a bounded near interval, truncation is enclosed by the first omitted term
once successive magnitudes decrease. For every far `x>0` and integer `M>=1`,

\[
\boxed{F(x)=-\sum_{k=1}^M
\frac{k!\cos(x-k\pi/2)}{x^k}+R_M(x),
\qquad |R_M(x)|\le\frac{2(M+1)!}{x^{M+1}}.}
\]

### Proof

The near series follows from the Taylor series for cosine and sine integral.
Repeated integration by parts in `int_x^infinity sin(u)/u du` gives the far
series and Dirichlet remainder. QED.

For sine frequencies `a,b>=0`,

\[
\boxed{K_Q(a,b)=\int_Q^\infty\sin(at)\sin(bt)t^{-2}dt
=\tfrac12[C_Q(a-b)-C_Q(a+b)].}
\]

The direct near expansion begins

\[
K_Q(a,b)=\frac\pi2\min(a,b)-Qab+
\frac{Q^3ab(a^2+b^2)}{18}+\cdots,
\]

with an explicit sum of first-omitted-term remainders. The cusp at `a=b` is
real: `C_Q` is not differentiable at zero. Away from the diagonal, integration
by parts factors the oscillation `exp(iQ(a-b))` exactly and leaves inverse
powers of `a-b`, which admit certified Chebyshev or exponential-sum
approximations. This yields blockwise low rank independent of `Q times range`
once `Q times separation` is sufficiently large.

### Hostile cluster obstruction

Exact Farey neighbors are not the full near field. There are `K` reduced
fractions of denominator at most `M`, clustered in an interval of diameter
`O(K/M^2)`, with `Theta(K^2)` mutually near pairs but only `K-1` Farey-neighbor
edges. Signed coefficients can make those `Theta(K^2)` terms cancel to
`Theta(K)`. A neighbor-only exact treatment plus fixed-accuracy far
approximation can therefore give the wrong leading value. The approximation
error must scale with the signed cluster, not merely entrywise kernel accuracy.

Thus geometric cluster separation, not Farey adjacency, is the valid notion of
near/far.

### Prototype verdict

A moderate-size hierarchical prototype sorted the reduced rational frequencies,
kept overlapping blocks dense, and compressed separated blocks. Ranks `4--8`
gave high numerical accuracy, while a single global low-rank approximation and
an exact Farey-neighbor band plus one global far approximation both failed.
This identifies an H-matrix-type structure, but the prototype used ordinary
floating point and SVD and is not a certificate.

A positive quadrature representation also gives a global Gram factorization

\[
K_Q(\omega,\nu)\approx\sum_{j=1}^r w_j
\sin(\omega t_j)\sin(\nu t_j),\qquad w_j>0,
\]

with explicit uniform error. Its rank scales with time-bandwidth, so it is
useful for blocks but not as one global approximation at the required accuracy.

## Next queued main-funnel step

Replace empirical SVD blocks by a certified analytic H-matrix expansion. For
each separated pair of frequency intervals, use the integration-by-parts
oscillatory factor and a Chebyshev or exponential-sum approximation to inverse
powers, with outward-rounded remainder. Prove a blockwise bilinear error bound
using local coefficient norms rather than global `l1` mass. Then validate the
certified hierarchy against dense moderate-size kernels and the hostile
rational clusters before scaling. The unresolved theorem is now certification
of hierarchical compression, not identification of kernel structure.

## Tick 15 — coefficient-aware hierarchical error theorem

The rigorous error propagation for a symmetric H-matrix leaf partition is now
formulated in `hierarchical-error-propagation.md`. If `P_+` stores each
off-diagonal block once and `E_AB=K_AB-Ktilde_AB`, then exactly

\[
Q-\widetilde Q=\sum_{(A,B)\in P_+}\kappa_{AB}c_A^TE_{AB}c_B,
\qquad \kappa_{AA}=1,\quad\kappa_{AB}=2\ (A<B).
\]

For a residual with certified entrywise and spectral errors, the local bound is

\[
|c_A^TR_{AB}c_B|\le
\min\{\epsilon_{AB}^{(\infty)}\|c_A\|_1\|c_B\|_1,
\epsilon_{AB}^{(2)}\|c_A\|_2\|c_B\|_2\}.
\]

Certified maximum row-`l2` and column-`l2` errors additionally give the mixed
local alternatives `epsilon^(1,2)||c_A||_1||c_B||_2` and
`epsilon^(2,1)||c_A||_2||c_B||_1`; the minimum of all available enclosures is
valid.

Certified separated error terms are evaluated through signed local moments
before taking absolute values. If a block enclosure is
`[m_AB-r_AB,m_AB+r_AB]`, the global error is enclosed by

\[
M\pm R,
\qquad M=\sum\kappa_{AB}m_{AB},
\quad R=\sum\kappa_{AB}r_{AB}.
\]

Thus known centers cancel globally, while unknown radii do not. This also
settles the symmetry bookkeeping: diagonal blocks occur once, their internal
off-diagonal entries are already doubled by the quadratic form, and stored
off-diagonal rectangles occur twice.

For reduced frequencies `p/q`, the local coefficient masses are computed from
the aggregates

\[
U_q=\sum_{j\le N/q}u_{qj}/j,
\qquad a_{p,q}=-w_{p,q}U_q/(\pi p).
\]

For the logarithmic Mobius taper, `U_q=0` for nonsquarefree `q`, while for
squarefree `q` it is the finite coprime Mobius sum displayed in the dedicated
note. The direct endpoint functional is treated as one two-channel symmetric
quadratic form, so its `2UD-alpha D^2` cancellation is retained rather than
bounded term by term.

This proves the certification theorem but not an affordable rank bound for all
separated blocks at `N=8192`. The remaining task is to instantiate each far
block with a certified analytic separated expansion and measure its
theorem-weighted local radius on dense and hostile rational data.

## Tick 16 — certified phase-extracted separated-block theorem

The analytic instantiation is proved in `certified-separated-kernel.md`.
Repeated integration by parts gives a complex endpoint expansion with the
sharp uniform residual

\[
|R_n(d)|\le (n+1)!/(Q^{n+2}|d|^{n+1})
\]

after `n+1` retained terms. Centering the residual at half the next asymptotic
term gives a disk of half that next term's magnitude. A hostile indexing audit
caught the important distinction: this is not uniformly half the preceding
uncentered bound.

On a separated block with difference center `d_0`, sum center `s_0`, and total
half-width `H<d_0`, Taylor compression of every inverse power has the explicit
remainder (3.1) of that note. After exact extraction of the phases
`exp(iQ(a-b))` and `exp(iQ(a+b))`, the combined difference/sum kernel has real
separated rank at most `2(p+1)`, independent of `Q` and the number of retained
inverse powers. Explicit absolute block radii are given by (4.2)--(4.3).

The qualification is essential: affordable rank requires fixed geometric
admissibility and a useful lower bound on `Q(d_0-H)`. Overlapping blocks retain
the Brownian `min(a,b)` cusp and cannot be uniformly compressed. Positive
global quadrature is certifiable but costs rank proportional to inverse target
accuracy near this cusp, so it does not replace the hierarchy.

An audit of the coefficient note also corrected two scope errors. A multiplier
can be pulled through `U_q` only if it depends on the reduced mode rather than
the original harmonic, and the sine-kernel quadratic form covers only the
oscillatory--oscillatory tail; constant-mode pieces must be certified
separately. No asymptotic Mobius cancellation or RH conclusion is asserted.

## Next queued main-funnel step

Implement the theorem as an outward-rounded block certificate and measure the
global theorem-weighted radius on moderate exact rational frequency sets.
Dense near leaves must use exact kernel intervals, while admissible leaves use
the phase-extracted expansion and signed local moments. Test first against the
two-point cusp adversary, alternating Farey clusters, and rational grids before
assessing `N=8192` complexity.

## Tick 17 — outward-rounded block certificate and full tail completion

Added `verify_separated_kernel.py`, an Arb verifier independent of the endpoint
expansion through direct `Si`/`Ci` evaluation. It certifies the complex endpoint
remainder, half-next-term disk, inverse-power Taylor bound, every entry of a
compressed rational block, and the corresponding local-`l1` bilinear radius.
At 192 bits, deterministic `19 by 19` alternating Farey and `7 by 7` rational
grid blocks pass; an overlapping two-point cusp is correctly rejected. These
are finite implementation tests, not asymptotic evidence.

A second audit improved the amplitude theorem. The direct Lagrange radius was
valid but could grow with degree on wide admissible blocks. Summing the
negative-binomial absolute tail proves

\[
|R_{m,p}|\le \binom{m+p}{p+1}
H^{p+1}/[z_0^{p+1}(z_0-H)^m],
\]

which decreases to zero for every fixed `H/z_0<1`. The separated-block radius
and verifier now use this strictly stronger formula.

The missing constant modes are completed exactly. The full endpoint tail is
the constant term `(2mn-alpha n^2)/Q`, a linear constant--sine sum with

\[
S_Q(\omega)=\sin(Q\omega)/Q-\omega\operatorname{Ci}(Q\omega),
\]

and the existing two-channel sine-kernel quadratic form. This recovers the
exact period mean and closes a scope gap in the prospective finite certificate.

A cluster-tree complexity audit found that rationality alone permits quadratic
hostile near clusters. With denominator cap `M`, however, distinct reduced
fractions are separated by at least `1/[M(M-1)]`. At the approximately
64-million harmonic cutoff and fixed order-one far threshold, this gives only
`O(1)` forced-dense neighbors per frequency for `M<=16384`. It rules out that
specific quadratic near-field obstruction but not excessive far-leaf count,
rank, or accumulated radius.

## Next queued main-funnel step

Build the full one-dimensional cluster tree for a finite reduced-frequency
realization, allocate a global radius using exact local coefficient masses, and
include the constant and linear terms. Measure leaf count, selected orders,
signed center, and accumulated radius at increasing moderate cutoffs. The next
decisive test is whether far-field radii, rather than dense-neighbor count,
destroy the endpoint contraction margin.

## Tick 18 — full finite cluster tree and radius-growth obstruction

Added `verify_cluster_tree.py` and `test_cluster_tree.py`. The implementation
builds a binary tree on sorted rational frequencies, stores only canonical
upper-triangle leaves, evaluates near leaves by direct Arb `Si`/`Ci`, and uses
the certified phase-extracted expansion on admissible far leaves. It checks
that leaf multiplicities cover exactly all `N^2` ordered entries and encloses an
independent dense Arb evaluation.

The two-channel path certifies the shared-kernel expression

\[
2u^TKd-\alpha d^TKd
\]

without splitting its three terms. On a block its unstructured residual weight
is the exact finite sum of

\[
|u_i d_j+d_i u_j-\alpha d_i d_j|,
\]

which is never worse than separate local-`l1` products. Hand-computed
multiplicity, mixed dense/compressed, all-dense, rational-input, and exact
isotropic-null tests pass. In particular `alpha=2,u=d` is detected before tree
construction and has exactly zero center, radius, and rank.

For the deterministic scalar surrogate at `Q=64`, fixed rank bound `12`, the
certified results were:

| modes | dense leaves | compressed leaves | theorem radius | dense value |
|---:|---:|---:|---:|---:|
| 48 | 31 | 22 | 0.0001541 | 0.0122698 |
| 96 | 63 | 52 | 0.0008010 | 0.0231688 |
| 192 | 127 | 114 | 0.0064671 | 0.0141767 |

These are synthetic rational coefficients, not the Möbius endpoint channels,
so they imply no RH behavior. They do expose a decisive certification danger:
fixed per-block orders plus absolute unstructured radii can become comparable
to the signed center even while leaf count is nearly linear. Global adaptive
tolerance allocation and stronger residual structure are necessary.

The exact finite-realization audit also fixes the scope. A harmonic-first cutoff
must retain its weight inside each duplicate-frequency aggregate. The cluster
tree currently certifies exactly the supplied finite surrogate; it does not yet
certify the omitted harmonic limit, the retained interval `[1,Q]`, or the full
endpoint decrement.

### Stronger near-field route

The identity

\[
K_Q(\omega,\nu)=\frac\pi2\min(\omega,\nu)-G_Q(\omega,\nu),
\quad
G_Q=\int_0^Q\frac{\sin(\omega t)}t\frac{\sin(\nu t)}t\,dt
\]

suggests a one-sided replacement for dense cusp leaves. The cusp form is
evaluated in linear time by suffix sums. If `G_0` is the Gram matrix of an
orthogonal projection and `E=G_Q-G_0` is positive semidefinite, then with
`z=d-u/alpha`,

\[
2u^TK_Qd-\alpha d^TK_Qd
\le \mathcal L_{\pi\min/2}-\mathcal L_{G_0}+\alpha z^TEz.
\]

Only the projection error of the cancellation vector remains adverse; the
large `u` residual has favorable sign. This is structurally stronger than any
entrywise residual norm and is the next near-field attack.

## Next queued main-funnel step

Implement exact cusp suffix sums and a piecewise-polynomial orthogonal
projection certificate for `G_Q`, with a Poincare or Legendre remainder on
`z=d-u/alpha`. Compare its one-sided radius against dense leaves and the
existing local-`l1` hierarchy on hostile finite-difference clusters and actual
small Möbius endpoint channels. In parallel, add adaptive far-block order
allocation. The decisive question is whether PSD residual structure prevents
the observed radius blow-up.

## Tick 19 — certified PSD cusp/projection bound

Added `certified-cusp-projection.md`, `verify_cusp_projection.py`, and tests.
For `alpha>0`, one common orthogonal projection gives `G_Q=G_0+E` with
`E` positive semidefinite. With `z=d-u/alpha`, the exact completion is

\[
\mathcal L_{K_Q}=\mathcal L_{\pi\min/2}-\mathcal L_{G_0}
+\alpha z^TEz-\alpha^{-1}u^TEu.
\]

Dropping only the final favorable term yields a rigorous one-sided bound. The
assumption `alpha>0` and use of one common projection are essential.

The cusp form is evaluated exactly in one suffix pass. The prototype projects
onto constants on uniform cells, uses Arb `Si` cell means, and bounds the
residual by the sharp Neumann Poincare inequality. Defining

\[
A_z(s)=\sum_{\omega_i\ge s}z_i,
\qquad \mathfrak C(z)=\int s|A_z(s)|\,ds,
\]

one has `||Phi_z'||_infinity <= mathfrak C(z)`. For rational frequencies this
is an exact suffix sum and is much tighter than taking coefficientwise absolute
values first.

At `N=32,Q=8,alpha=3/2`, the certified results were:

| cells | adverse residual | upper-bound gap |
|---:|---:|---:|
| 16 | `3.32e-4` | `5.19e-4` |
| 32 | `8.29e-5` | `1.30e-4` |
| 64 | `2.07e-5` | `3.25e-5` |
| 128 | `5.18e-6` | `8.11e-6` |

Both decay by four under cell doubling, as proved. These are finite synthetic
tests only.

A hostile narrow pair with coefficients proportional to inverse gap converges
to a carrier cosine. Thus zero total mass and shrinking bandwidth do not force
a small residual; piecewise constants can require `Omega(Q times carrier)`
cells. The correct complexity parameter is the suffix profile or derivative
energy, not bandwidth alone.

Higher-order piecewise Legendre projection preserves the PSD completion and
has explicit weighted derivative constant

\[
\Lambda_{p,m}=(p+1+m)!/(p+1-m)!.
\]

## Next queued main-funnel step

Implement piecewise Legendre projection with exact feature moments and an
origin-safe Taylor--Legendre remainder. Test the harmonic-first `N=4 -> 8`,
`R=3` Möbius endpoint surrogate with `alpha=1/3`, then compare degrees `0--3`
at equal total rank. Retain the favorable `-u^TEu/alpha` term whenever a lower
bound can be certified; otherwise record exactly the loss from dropping it.

## Tick 20 — higher-order projection and exact small Mobius surrogate

Extended the PSD projection certificate to piecewise Legendre degrees `0--3`.
Projection features are exact finite combinations of Arb `Si`, sine, and cosine
endpoint values; the origin cell never evaluates `sin(omega t)/t`. For degree
`p`, comparison with the midpoint Taylor polynomial and the exact suffix bound

\[
B_{p+1}(z)=\int s^{p+1}|A_z(s)|\,ds
\]

gives a residual of order `h^(2p+2)`. All four degrees are compared at equal
total projection rank.

On the synthetic finite test, equal rank `192` gave certified gaps

\[
8.12\cdot10^{-6},\quad2.26\cdot10^{-9},\quad
1.46\cdot10^{-12},\quad1.23\cdot10^{-15}
\]

for degrees `0,1,2,3`. This confirms that the time-carrier obstruction of
piecewise constants is not intrinsic to the PSD projection route.

Added `mobius_endpoint_surrogate.py`. It constructs the harmonic-first
`N=4 -> 8`, `R=3` endpoint channels, aggregates duplicates only after applying
the original harmonic cutoff, and obtains 14 active reduced angular
frequencies with exact `alpha=1/3`. At `Q=8`, the dense Arb oscillatory form is

\[
-0.0040628365567544479045\ldots.
\]

At equal rank `768`, the degree-three certificate has adverse residual
`1.75677e-6`, upper bound `-0.0040622509662`, and gap `5.85591e-7`. It therefore
certifies that this finite oscillatory surrogate is negative. This is not the
full endpoint decrement: omitted harmonics, constant and linear pieces, and the
retained interval remain outside this finite claim.

An audit of the sharper weighted Legendre inequality confirms

\[
\|(I-P_p)F\|^2\le\Lambda_{p,m}^{-1}
\int_I[(t-a)(b-t)]^m|F^{(m)}|^2,
\quad \Lambda_{p,m}=\frac{(p+1+m)!}{(p+1-m)!}.
\]

The reciprocal, admissible range `1<=m<=p+1`, and affine scaling are essential.
The current code uses the simpler valid Taylor constant; weighted Legendre can
improve degree three by about a factor `19` at the same derivative order.

The favorable residual `-u^TE_pu/alpha` can also be recovered without a matrix
eigenvalue bound. Extra Legendre shadow modes give a Bessel lower bound on
`u^TE_pu`; equivalently, the shell from degree `p+1` through `r` can be retained
with its exact two-channel sign before bounding only the residual beyond `r`.

## Next queued main-funnel step

Implement the weighted Legendre residual and signed shadow-shell completion.
Measure how much of the favorable `u` residual is recovered on the `N=4 -> 8`
surrogate and whether the certified negative oscillatory margin persists at
substantially lower rank. Then include the exact constant--constant and
constant--sine terms of the same finite surrogate before confronting the
harmonic truncation remainder.

## Tick 21 — weighted shells and the full-tail sign obstruction

Implemented the weighted Legendre backend and signed shadow-shell completion.
For degree `p` and derivative order `m`, the exact uniform-cell constant is

\[
C_{p,m}=\frac{m!^2(p+1-m)!}{(2m+1)!(p+1+m)!}.
\]

The implementation checks every `1<=m<=p+1` and selects the smallest certified
radius. It also evaluates shell modes `p+1,...,r` with their exact signed
endpoint contribution, bounding only the PSD residual beyond `r`. On the finite
Möbius oscillatory surrogate, weighted degree three lowers the first negative
certificate from rank `256` to `176`; a degree-three primary projection with
shadow degree `12` certifies negativity at completed rank `104`.

The full finite `R=3` tail was then completed. At `Q=8`, its certified pieces
are

\[
\begin{array}{lr}
\text{constant--constant}&+0.2186425862643,\\
\text{constant--sine}&+0.0007373649329,\\
\text{oscillatory--oscillatory}&-0.0040628365568.
\end{array}
\]

Hence the complete finite tail is

\[
\boxed{0.21531711464047\ldots>0.}
\]

The negative oscillatory certificate was therefore not the sign of the direct
endpoint functional; the constant mode dominates it by more than a factor of
fifty. This is a decisive route correction.

The harmonic truncation issue is also eliminated for this fixed checkpoint by
`certify_endpoint_tail.py`. On each unit interval, every original sawtooth is
affine, so the direct integrand is a quadratic divided by `t^2` and integrates
exactly using one logarithm. A finite prefix to `T=1024` plus the elementary
`1/T` pointwise remainder gives

\[
\boxed{0.2004969520996<\mathcal T_8<0.2320926742316.}
\]

Thus the full untruncated `N=4 -> 8` tail on `[8,infinity)` is rigorously
positive without Fourier truncation or a common period. This is a finite
checkpoint, not an RH implication. It shows that the next useful target cannot
be oscillatory-tail negativity; it must control the complete endpoint
functional, including constants and the retained interval.

## Next queued main-funnel step

Certify the direct complete endpoint decrement on `[1,infinity)` for small
dyadic `N`, splitting `[1,Q]` exactly at all sawtooth breakpoints and using the
new tail certificate beyond `Q`. Compare its sign with the already certified
`P_N-P_(2N)` breakpoint calculations as an independent normalization audit.
Then search for a complete-functional block or averaged inequality that scales
with `N`; abandon oscillatory-only sign targets.

## Tick 22 — complete small dyadic decrements and local-positivity failure

Generalized `certify_endpoint_tail.py` to arbitrary dyadic `N`. It independently
constructs `F_N` and `F_(2N)` and checks

\[
P_N-P_{2N}=\alpha_N\mathcal E_N,
\qquad
\mathcal E_N=\int_1^\infty(2f_Nd_N-\alpha_Nd_N^2)t^{-2}dt.
\]

At cutoff `4096`, both independent enclosures are strictly positive for
`N=2,4,8,16`; the endpoint-functional intervals are respectively

\[
[1.9491,1.9524],\ [1.5987,1.6066],\ [0.9896,1.0113],\ [0.5702,0.6344].
\]

The two normalizations overlap after multiplication by `alpha_N`. These are
finite certificates only.

The unit-cell structure is recorded in `unit-cell-endpoint-bounds.md`. Each
cell integral has one logarithm, while floor intercepts update by sparse divisor
impulses, giving an `O(T log N)` certificate. Three Bernstein products of
one-sided endpoint values provide elementary bounds. However, cellwise
positivity is false: for `N=8 -> 16`, cell `k=35` contributes

\[
-0.0001179347729698\ldots.
\]

The cell discriminant is always the exact square `4(Db_k-e_kA)^2`; it gives
root geometry but no Möbius positivity. A successful elementary proof must
group cells or control cumulative divisor impulses.

The scalable candidate is complete-functional contraction

\[
\mathcal E_N\ge\eta P_N,
\]

equivalently `P_(2N)<=(1-eta alpha_N)P_N`. A weaker fixed-length dyadic block
inequality permits individual increases:

\[
P_N-P_{2^LN}\ge
2\kappa\sum_{r=0}^{L-1}W_{2^rN}P_{2^rN}.
\]

Either target forces `liminf P_N=0` and hence RH in this funnel. The missing
lemma is a cancellation-aware bound for the aggregated complete numerator or
its cumulative divisor-impulse primitive.

## Next queued main-funnel step

Form exact divisor-impulse sequences for a fixed dyadic scale block and derive
Abel/summation-by-parts identities for grouped cell sums before any absolute
value. Search for a short deterministic pairing or block lower bound absorbing
every negative cell through moderate `N`; state the weakest pattern that would
imply fixed-length block contraction.

## Tick 23 — exact Abel primitives and failure of local pairings

The grouped unit-cell sum is now reduced exactly in
`abel-divisor-impulses.md`. Abel summation writes it as `c_2(T-K)` plus positive
weights applied to two cumulative primitives `Z_m,H_m`. The latter retains the
signed quadratic correlation

\[
H_m=\sum_{k=K}^m(2b_ke_k-\alpha e_k^2).
\]

Thus a lower-envelope theorem for aggregated `Z_m,H_m` is precisely sufficient;
termwise absolute bounds are precisely the wrong operation.

Added `analyze_unit_cells.py` and tests. At horizon `1024`, the first universally
nonnegative sliding-window lengths are `3` for `N=8` and `12` for `N=16`, but
no length through `256` works for `N=32,64`. A deeper hostile audit finds a
negative length-512 block for `N=32` and a negative length-4096 block for
`N=64`. Fixed nearby pairings fail by `N=16`, and a greedy divisor-event pairing
fails by `N=128`. Therefore fixed spatial windows and local pairings are
decisively abandoned.

The natural cross-scale alpha weights telescope pointwise to
`F_N^2-F_(2^LN)^2`; this removes intermediate scales but gives no new positivity.
General weights leave mixed-sign intermediate energy squares. The useful target
remains a lower envelope for cross-scale aggregated Abel primitives, not a
longer telescope.

One exact favorable initial-range identity was found. For `1<=k<=N`, classical
Möbius convolution gives

\[
b_k=e_k=-\psi(k)/\log N,
\]

so the quadratic primitive summand is nonnegative there. Beyond `N`, the
truncated Möbius tail reappears. Existing Farey and Franel--Landau identities do
not bound the required mixed logarithmic floor correlation without importing
RH-strength cancellation.

## Next queued main-funnel step

Exploit the exact `b_k=e_k=-psi(k)/log N` reserve on `[1,N]`. Quantify it
against the worst possible loss on `[N,T]` using the cumulative Abel weights,
first with exact finite optimization and then with unconditional Chebyshev-type
bounds. Search for an anchored reserve inequality rather than translated-window
positivity; test whether a fixed number of dyadic scales improves the reserve
to defect ratio after aggregating primitives.

## Tick 24 — reserve cancellation and drift-free cells

Added `analyze_endpoint_prefix.py` and certified tests. The exact Chebyshev
identity produces a large positive `psi^2` term, but
`drift-free-endpoint-cells.md` proves that this is mostly bookkeeping drift. The
complete initial reserve is

\[
(2-\alpha)[V_N+N(D-m_N)(G-m_N)],
\]

where `V_N>=0` is a weighted variance. Constant, logarithmic, and quadratic
pieces each have size `N/log^2 N` and cancel at leading order. Coarse explicit
Chebyshev bounds cannot control the slope-position term. The large-reserve
domination strategy is therefore abandoned.

Recentring each cell gives

\[
J_k=c_2R_k+\widehat z_kV_k+g_kw_k
\]

with three positive `O(k^-2)` weights. A certified run through
`N=8192,T=16N` found initial reserve `0.0691463`, later loss `0.0035216`, and
complete prefix `0.0656248`. All three drift-free component sums were positive
on that finite prefix. However, the absolute tail radius was about `80`, over a
thousand times the prefix, and grows with `N` at fixed `T/N`.

The later contribution stabilizes numerically near a negative few `10^-3`,
dominated by `g_kw_k`, while the positive `c_2R_k` channel decays. No
componentwise late-tail inequality survives. Exact endpoint formulas identify
the obstruction after `k=N` as a truncated Möbius transform `T_N(k)` entering
`r_k,s_k` with different scaling.

Cross-scale aggregation gives only modest, nonuniform finite improvement, and
`W` weights behave almost identically to alpha weights. Separate primitive
bounds remain unusable because large drifts cancel only in the complete form.

## Next queued main-funnel step

Expand the drift-free `g_k` tail through `T_N(k)` and sum over `k` before taking
absolute values. Seek a positive gcd/divisor kernel or a cancellation-aware
bilinear identity at the required `1/log^2 N` scale. Uniform endpoint bounds
cannot attain this scale.

## Tick 25 — exact weighted Mobius kernel

`drift-free-mobius-kernel.md` carries out the requested expansion before any
bounding. On `N<k<=2N`, with `p_k=kA-psi(k)/log N`, the exact cancellation is

\[
g_k=g_k^{(0)}+\alpha^{-1}(2p_kT_N(k)+T_N(k)^2).
\]

After summing with `w_k=1/[k(k+1)]`, the quadratic kernel telescopes to

\[
K(n,m)={1\over\max(n,m)}-{1\over2N+1}.
\]

It is positive definite, since its form is the weighted sum of squares of
cumulative sums. The linear kernel is also exact and can be written using a
harmonic term and a single von Mangoldt sum. Its sign is uncontrolled; this is
the entire fresh-transform obstruction on the first dyadic block. The max
kernel has no gcd dependence, and splitting it into gcd classes destroys its
Gram structure.

Beyond `2N`, exact floor transforms at scales `N` and `2N` give a difference of
two PSD floor Gram forms, not a positive gcd form. The separate floor pieces
must be recombined before an infinite-horizon bound, because each contains
large growth canceled only in the endpoint difference.

Added `analyze_weighted_g_tail.py` and exact tests. Through `N=8192`, the fresh
linear term is certified negative and the quadratic max-kernel term nonnegative,
but the complete first post-reserve block is usually negative and highly
nonmonotone. At `N=8192`, on `[N,2N)`,

\[
\text{baseline}=0.0008528322,
\quad \text{linear}=-0.0024768828,
\quad \text{quadratic}=0.0004437379,
\]

so the total is `-0.0011803128`. The baseline itself is another cancellation of
three terms near `194,-389,195`; componentwise estimates are unusable.

Completing the square gives a sharper interpretation:

\[
g_k=\alpha^{-1}(T_N(k)-\tau_k)^2-\alpha^{-1}\Delta_k^2,
\]

where `tau_k=psi(k)/log N-kA` and
`Delta_k=k(A-alpha D)-(1-alpha)psi(k)/log N`. Thus the problem is weighted
tracking of a deterministic center by the cumulative Möbius transform. The
actual transform correlates enough with the center to make this shell negative,
but no unconditional tracking theorem is known.

The positive max kernel alone cannot yield the required scale. An
`O(1/log^2 N)` estimate for its Möbius quadratic form is equivalent to an
average square-root cancellation statement for partial Möbius sums on the
dyadic block. Generic PSD, spectral, random-sign, or gcd arguments would hide
an RH-strength input. The leading eigenvalues remain bounded away from zero.

## Next queued main-funnel step

Target the complete tracking difference, not the positive quadratic term.
Derive a Perron/Mellin or Dirichlet-polynomial representation for

\[
\sum_{N\le k<2N}w_k[(T_N(k)-\tau_k)^2-\Delta_k^2]
\]

that keeps the linear--quadratic cancellation. Identify whether its main term
vanishes or has a favorable sign before any contour shift encounters
`1/zeta(s)`. In parallel, test low-eigenmode projections of the exact Möbius
vector to isolate the minimum finite family of smooth moments that must cancel.

## Cycle 24: complete tracking representation and low modes

The first-block completed square admits a cancellation-preserving cumulative
coefficient representation.  In the half-open convention `M=2N-1`, set

\[
c_n=A-\Lambda(n)/\log N+
\mathbf1_{N<n\le M}\mu(n)\log(N/n)/\log N,
\]

\[
e_n=A-\alpha D-(1-\alpha)\Lambda(n)/\log N.
\]

Then the complete tracking difference is exactly

\[
\sum_{k=N}^M{(\sum_{n\le k}c_n)^2-(\sum_{n\le k}e_n)^2\over k(k+1)}.
\]

This yields both an exact finite max-kernel form and a double Perron formula in
finite entire Dirichlet polynomials.  The finite formula has only the two
Perron poles.  Replacing its Mobius polynomial by `1/zeta` creates poles at all
zeta zeros; the maximal standard unconditional shift stays in the classical
zero-free region and gives only PNT-strength control, far above the required
scale.  Thus routine contour shifting is now ruled out as the missing lemma.

The formal deterministic continuum profile vanishes: replacing `psi(k)` by
`k`, `log(N)A` by `1`, and `A-D` by `0` makes both completed-square centers
zero.  The positive Mobius diagonal nevertheless has the nonzero limit

\[
{6\over\pi^2}\left({\log^3 2\over3}-\log^2 2+2\log2-1\right).
\]

Hence an improved complete estimate requires constant-precision cancellation
of this diagonal by the off-diagonal, mixed Mobius--von-Mangoldt, and
deterministic error channels.

The continuum max-kernel operator has exact eigenfunctions

\[
x^{-1/2}\left(\cos(\beta\log x)+{\sin(\beta\log x)\over2\beta}\right),
\quad \tan(\beta\log2)=-2\beta,
\]

and eigenvalues `1/(beta^2+1/4)`.  Thus the low modes are localized Mellin
moments near the critical exponent `1/2-i beta`; their eigenvalues do not
vanish with `N`.  Added a tridiagonal inverse eigensolver and small Arb modal
certificates.  Reconnaissance through `N=8192` shows the observed tracking sign
is often fixed by the first few modes, although accurate magnitude recovery
needs a growing spectral tail.  This is diagnostic, not an asymptotic theorem.

An exact inverse audit corrected the max-kernel energy boundary: it lies at the
terminal index `M`, as forced by `max(n,m)`, rather than at the initial index.

### Next queued main-funnel step

Construct the explicit finite harmonic completion of the first few low Mellin
modes using `mu*1=epsilon`, `mu*log=Lambda`, and their quadratic analogues.
Test whether the prime residual already present in the deterministic center
cancels these completed modes before estimation.  In parallel, seek a
cancellation-aware high-mode bound; a fixed number of moments alone is
insufficient because the raw Mobius source norm grows with `N`.

## Cycle 25: exact harmonic completion and fixed-mode obstruction

For every complex `z`, divisor convolution gives the entire identity

\[
\sum_{N<r\le2N}\mu(r)(r/N)^z
=-\sum_{d\le N}\mu(d)(d/N)^z
\sum_{N/d<m\le2N/d}m^z.
\]

This is an exact completion of the continuum Mellin weights, including
`z=-1/2+i beta_j`.  Differentiation yields all polynomial logarithmic moments.
The degree-one divisor-side residual is exactly
`-(psi(2N)-psi(N))`; it includes prime powers and all endpoints.

More importantly, opening the floor transform

\[
Z_X(k)=\sum_{d\le X}\mu(d)\log(X/d)\lfloor k/d\rfloor
\]

cancels the explicit von Mangoldt channel before squaring.  On the first block,
the complete tracking difference becomes exactly

\[
\sum_{k=N}^{2N-1}{1\over k(k+1)}\left[
\left(kA+1-{Z_N(k)\over\log N}\right)^2-
\left(k(A-\alpha D)+1-{Z_{2N}(k)\over\log(2N)}\right)^2
\right].
\]

This is the strongest algebraic completion found.  It does not collapse to
boundary terms: expansion leaves a difference of dense floor Gram forms at the
two scales.  Composite squarefree fresh indices also show that the positive
Mobius diagonal cannot cancel locally against a same-index Lambda term; any
cancellation is global.

Degree two is not completed by the existing Lambda channel.  Its exact source
mismatch is

\[
(\mu*\log^2)(n)-2\log(n)\Lambda(n),
\]

whose jump at a prime `p` is `-log^2 p`.  This is an explicit certificate
against a naive quadratic extension of the degree-one cancellation.

Added `verify_harmonic_completions.py`, exact formal-prime-log tests through
degree three, and a separate noncertifying comparison with discrete and
continuum low modes.  The exact layer uses rational sparse polynomials only.

A hostile spectral audit also rules out fixed-mode closure.  For the first `J`
eigenmodes removed, completed-square projection gives only

\[
|\mathcal T_{>J}|\le\lambda_{J+1}
(\|u-v\|_2^2+\|v\|_2^2),
\]

and generic bounded source size yields `O(N/J^2)`.  A bounded rescaling of the
`(J+1)`-st eigenvector annihilates all first `J` modal moments but retains this
order of energy.  Hence fixed `J`, bounded increments, and smoothness alone are
insufficient.  Without new arithmetic cancellation, even `o(1)` requires
roughly `J` larger than `sqrt(N)`.

The finite Jacobi problem is exact: inverse eigenvalues are roots of an integer
continuant for the tridiagonal conductances `n(n+1)`.  A direct kernel comparison
gives operator error less than `5/(4N)`, enough for continuum eigenvalue control
through `J=o(sqrt(N))` and individual eigenvector control through
`J=o(N^(1/3))`.  This helps certify growing-mode approximations but supplies no
Mobius cancellation.

### Next queued main-funnel step

Analyze the exact two-scale completed square `Z_N` versus `Z_(2N)` without
expanding the scales separately.  Seek a cross-scale floor-kernel identity or
martingale decomposition whose high-frequency remainder is charged to the
difference of transforms rather than either raw source.  In parallel, derive
and certify the continuant/quasimode comparison for growing `J` so any proposed
arithmetic moment estimate has a rigorous discrete tail.

## Cycle 26: common-source cross-scale geometry

The two completed scales admit the exact common-source relation

\[
\eta=(1-\alpha)\lambda+\alpha\rho,
\]

where `lambda` and `eta` are the normalized scale-`N` and scale-`2N` tapers,
and `rho_d=1` for `d<=N`, while
`rho_d=log(2N/d)/log2` on the fresh block.  If

\[
P_k=kA+1-Z_N(k)/\log N,
\]

\[
Q_k=k(A-D)+1-(Z_{2N}(k)-Z_N(k))/\log2,
\]

then the second center is

\[
\widetilde P_k=(1-\alpha)P_k+\alpha Q_k.
\]

Thus

\[
P_k^2-\widetilde P_k^2
=\alpha(2-\alpha)
\left(P_k-{1-\alpha\over2-\alpha}Q_k\right)^2
-{\alpha\over2-\alpha}Q_k^2.
\]

The `2 by 2` determinant is `-alpha^2`, so this compression is exactly
indefinite.  On the common Mobius source the quadratic kernel is

\[
\mathcal H_N=D_\lambda K_ND_\lambda-D_\eta K_ND_\eta,
\qquad K_N=F^TWF.
\]

It is indefinite at every scale: its `1,1` entry is zero and every active
`1,e` entry is negative, producing a negative `2 by 2` principal determinant.
The correction has rank of order `N`, not fixed rank.

The normalized weight `2N/[k(k+1)]` is the exact reciprocal-integer law on the
dyadic shell.  The fresh transform is adapted under this law but is neither
mean zero nor orthogonal to the old transform.  Variance differences have both
signs, closing the natural martingale-contraction route.

A minimal exact arbitrary-source certificate occurs at `N=2`:

\[
w=(1/6,1/12),\quad b=(2,3),\quad c=(1/2,1/2),
\]

with old-minus-fine homogeneous matrix

\[
\begin{pmatrix}0&-7/24\\-7/24&-1/16\end{pmatrix},
\qquad \det=-49/576.
\]

The source vectors `(1,1)` and `(1,-1)` give opposite signs.  Hence floor
geometry alone supplies no Loewner order, contraction, sign, or martingale
orthogonality.

Added an exact/Arb two-scale analyzer.  It verifies the actual completed-square
identity cellwise against the independent drift-free implementation and
certifies ambient two-channel floor ranks and nullspaces through `N=32`.  Its
ambient signed-Gram inertia is explicitly distinguished from the linked
common-source restriction.

Parity gives `mu(2d)=-1_(d odd)mu(d)`, so even fine-scale coefficients
anti-dilate odd coarse coefficients.  At floor level the residual is the full
odd-multiple transform, not a sparse boundary term.

### Next queued main-funnel step

Use the canonical dyadic embedding of coarse floor columns into even fine-scale
columns.  Compute the exact positive Schur complement of odd fine columns after
projection onto the embedded coarse space, then express the actual Mobius
coefficient pair in this orthogonalized basis.  Target an arithmetic estimate
for the odd residual and its signed affine correlation.

### Weighted parity Schur audit through N=64

Implemented the queued finite audit in `analyze_parity_schur.py`, with details
in `parity-schur-report.md`.  Under the exact weights `1/(k(k+1))`, the embedded
even/coarse rank is `N/2`, the odd and full fine ranks are `N`, and the exact
odd-against-coarse Schur rank is `N/2` for every dyadic `2 <= N <= 64`.

The analyzer applies this exact rational projection to the actual Arb Mobius-log
coefficient pair.  The projected/residual cross terms rigorously contain zero,
and the Schur energy agrees with an independent direct fine-image energy
calculation.  At `N=64`, the direct normalized fine energy is approximately
`2.9043992041`, while the orthogonal odd residual contributes approximately
`0.00071103223`.  The even/odd cross term is approximately `-5.7631556664`, so
the arithmetic cancellation is large even though the positive Schur residual
is small in these finite cases.

## Cycle 27: exact odd-column projection and affine Schur residual

The canonical embedding is most transparent with normalized shell weights.  On
the coarse and fine shells put

\[
 w_k^-={N\over k(k+1)}\quad(N/2\le k<N),\qquad
 w_j^+={2N\over j(j+1)}\quad(N\le j<2N),
\]

and define

\[
 (Ju)_{2k}=(Ju)_{2k+1}=u_k.
\]

The telescoping identity

\[
 w_{2k}^++w_{2k+1}^+=w_k^-
\]

makes `J` an exact isometry.  If

\[
 C_{kd}=\left\lfloor{k\over d}\right\rfloor,
 \qquad E_{j d}=\left\lfloor{j\over 2d}\right\rfloor,
\]

then `E=JC`: the even fine columns are exactly the embedded coarse columns,
including on the odd fine rows.  This is the canonical dyadic embedding; no
interpolation or asymptotic approximation is involved.

These weights are `2N` times the ordinary fine-shell matrix
`diag(1/[j(j+1)])`; thus every formula below converts to the original completed
energy by division by `2N`.  The normalization changes no projection or sign.

Let the odd fine indices be `q=1,3,...,2N-1`, and write

\[
 O_{jq}=\left\lfloor{j\over q}\right\rfloor,
 \qquad G=C^TW_-C,
 \qquad P_C=CG^+C^TW_-.
\]

Here `G^+` is the Moore--Penrose inverse on `ran(G)`.  It is essential because
the coarse floor columns need not be independent.  For `m_k=2k+1`, define

\[
 H_{kq}=\left\lfloor{2k\over q}\right\rfloor
       +{k\over2k+1}\mathbf1_{q\mid 2k+1},
 \qquad D_{kq}=\mathbf1_{q\mid2k+1}.
\]

The weighted adjoint of `J` gives the exact pair average

\[
 J^*O=H.
\]

Consequently the orthogonal projection and residual of every odd column are

\[
 \boxed{\Pi_EO=JP_CH,\qquad R_O=(I-\Pi_E)O=O-JP_CH,}
\]

where `Pi_E=JP_CJ^*`.  Equivalently, for a single odd `q`, its projected
coarse coefficient vector can be chosen canonically as

\[
 \boxed{\gamma_q=G^+C^TW_-h_q,\qquad \Pi_Eo_q=JC\gamma_q.}
\]

There is also a useful orthogonal splitting of the residual.  The pairwise
fluctuation `O-JH` is perpendicular to the whole range of `J`, while
`J(I-P_C)H` is pair-constant.  Therefore

\[
 R_O=(O-JH)+J(I-P_C)H
\]

is an orthogonal sum.  Its Gram matrix, the positive odd-column Schur
complement, is

\[
 \boxed{
 S=O^TW_+(I-\Pi_E)O
  =H^TW_-(I-P_C)H+T,}
\]

with the completely explicit arithmetic matrix

\[
 \boxed{
 T_{qr}=\sum_{k=N/2}^{N-1}{N\over(2k+1)^2}
       \mathbf1_{q\mid2k+1}\mathbf1_{r\mid2k+1}.}
\]

Thus `S` is positive semidefinite without any assumption on the source.  In
ordinary unnormalized weights `1/[j(j+1)]`, the coefficient in `T` is
`1/[2(2k+1)^2]`.  The formula is exactly the generalized Schur complement

\[
 S=O^TW_+O-(E^TW_+O)^T(E^TW_+E)^+(E^TW_+O),
\]

so it remains valid across every coarse rank defect.

Now insert the actual normalized scale-`2N` Mobius source.  Put

\[
 e_d={\mu(2d)\log(N/d)\over\log(2N)},\qquad
 x_q={\mu(q)\log(2N/q)\over\log(2N)},
\]

for `1<=d<=N` and odd `q<2N`.  The exact parity formula is

\[
 \boxed{\mu(2d)=-\mathbf1_{\{d\text{ odd}\}}\mu(d),}
\]

and hence, if `a_d=mu(d)log(N/d)/log N` and
`alpha=log 2/log(2N)`, then

\[
 \boxed{e_d=-(1-\alpha)\mathbf1_{\{d\text{ odd}\}}a_d.}
\]

This is the exact even-source coefficient formula; in particular, it is not a
copy of the full coarse Mobius source.

To retain the affine center rather than silently homogenizing it, set

\[
 A=A_{2N}=\sum_{n\le2N}{\mu(n)\over n}
                 {\log(2N/n)\over\log(2N)},
 \qquad c_j=jA+1,
\]

and let `y=c-Ee-Ox` be the actual completed scale-`2N` vector on the fine
shell.  Its weighted pair average and pair jump are

\[
 \bar c_k=1+A\left(2k+{k\over2k+1}\right),
 \qquad y_{2k+1}-y_{2k}=A-(Dx)_k,
\]

so

\[
 J^*y=\bar c-Ce-Hx.
\]

Define the canonical effective coarse coefficient

\[
 \boxed{
 \gamma=G^+C^TW_-(\bar c-Hx)-e.}
\]

Then the exact orthogonal decomposition of the actual normalized fine energy is

\[
 \boxed{
 \|y\|_{W_+}^2
 =\|C\gamma\|_{W_-}^2+\mathcal R_{\rm odd},}
\]

(The original unscaled scale-`2N` completed energy is the right-hand side
divided by `2N`.)

where

\[
 \boxed{
 \mathcal R_{\rm odd}
 =\|(I-P_C)(\bar c-Hx)\|_{W_-}^2
  +\sum_{k=N/2}^{N-1}{N\over(2k+1)^2}
       \left(A-\sum_{q\mid2k+1}x_q\right)^2.}
\]

Both terms are positive, but the second displays the arithmetic cancellation
that an absolute-value argument would destroy.  Notice also that the affine
center contributes to both residual terms.  Calling `x^TSx` the whole residual
would be incorrect for the actual completed vector.

For the signed completed-square needed in the endpoint comparison, define

\[
 r_0=(I-P_C)\bar c,\qquad
 \ell=H^TW_-r_0+D^TV(A\mathbf1),\qquad
 V=\operatorname{diag}\left({N\over(2k+1)^2}\right).
\]

Then the affine residual has the exact signed expansion

\[
 \boxed{
 \mathcal R_{\rm odd}=x^TSx-2\ell^Tx+C_0,\qquad
 C_0=\|r_0\|_{W_-}^2+A^2\mathbf1^TV\mathbf1.}
\]

Because `ell` lies in `ran(S)`, its completed-square form is

\[
 \boxed{
 \mathcal R_{\rm odd}
 =(x-S^+\ell)^TS(x-S^+\ell)
  +C_0-\ell^TS^+\ell.}
\]

The last constant is nonnegative, since it is the squared distance of the
affine residual from the odd residual range.  If `u` denotes the corresponding
coarse completed vector on `N/2<=k<N`, the signed shell-energy comparison is
therefore

\[
 \boxed{
 \|u\|_{W_-}^2-\|y\|_{W_+}^2
 =\|u\|_{W_-}^2-\|C\gamma\|_{W_-}^2
  -(x-S^+\ell)^TS(x-S^+\ell)
  -(C_0-\ell^TS^+\ell).}
\]

This preserves the affine centers and the sign of every completed square.  It
also shows the limitation of the geometric step: the Schur residual is
positive, but it is subtracted in the desired coarse-minus-fine comparison.
The remaining arithmetic target is a joint estimate for the effective coarse
term and the centered odd divisor-incidence residual; positivity of `S` alone
cannot prove contraction.

### Next queued main-funnel step

Exploit the explicit odd incidence form.  First rewrite
`A-(Dx)_k` using `mu(2d)` and divisor convolution at the odd integer `2k+1`;
then test whether its affine correlation with `(I-P_C)(bar c-Hx)` has an exact
von-Mangoldt completion.  Any bound must retain the signed center `ell`: a
source-only estimate for `x^TSx` does not control the actual residual.

## Cycle 28: odd Schur complement collapses to the prime diagonal

The even fine columns span the full pair-constant space.  Consequently the odd
Schur complement has the exact incidence formula

\[
\boxed{S_{d,e}=\sum_{\substack{N<r<2N\\r\text{ odd}\\d\mid r,\ e\mid r}}
{1\over2r^2}.}
\]

This is stronger than the earlier abstract projection formula.  The residual
of an odd column `d` is a sum over its odd multiples `r` in the shell, supported
on the pair `(r-1,r)`.  On that pair its values are

\[
-{r-1\over2r},\qquad {r+1\over2r},
\]

and its exact weighted energy is `1/(2r^2)`.  Hence the Schur rank is exactly
`N/2`: the shell columns `d=r` give an identity incidence block.  The complement
is not low rank.

For the actual normalized odd source

\[
x_d=\mu(d){\log(2N/d)\over\log(2N)},
\]

divisor convolution gives, for every odd shell integer `r>1`,

\[
\sum_{d\mid r}x_d={\Lambda(r)\over\log(2N)}.
\]

Therefore

\[
\boxed{x^TSx={1\over2\log^2(2N)}
\sum_{\substack{N<r<2N\\r\text{ odd}}}{\Lambda(r)^2\over r^2}.}
\]

The Mobius signs disappear completely after orthogonalization.  Weighted PNT
asymptotics yield

\[
x^TSx\sim {1\over4N\log N}.
\]

Thus the positive odd residual shrinks, but only at its natural prime-diagonal
rate.  At the critical normalization `N log N x^TSx -> 1/4`; it is not an
unexpected cancellation and cannot simply be discarded.

The affine jump in the actual completed vector is

\[
A-{\Lambda(r)\over\log(2N)}.
\]

For prime `r` this is order one, not order `1/log N`; earlier speculation that
the affine correction might be uniformly lower order is false.  The exact
affine square must remain intact.  Schur positivity enters the desired
coarse-minus-fine comparison with a minus sign and still does not imply
contraction.

The analyzer now verifies the incidence formula entrywise over the rationals
and independently certifies the prime-power energy identity with Arb through
`N=64`.

### Next queued main-funnel step

Compute the pair-constant null correction `(I-P_C)(bar c-Hx)` in the sparse
left-null basis of the coarse floor matrix.  Its basis vectors arise from
collisions of truncated divisor-incidence rows.  Derive the exact Lambda-valued
coordinates of the affine vector on these collisions, and determine whether
their energy cancels or reinforces the explicit odd prime diagonal.

## Cycle 29: the pair-constant left-null residual vanishes

The exact analyzer `analyze_pair_constant_residual.py` computes the left kernel
of the coarse matrix

\[
 C_{k,d}=\lfloor k/d\rfloor,
 \qquad N/2\leq k<N,\quad 1\leq d\leq N,
\]

over the rationals.  Contrary to the anticipated sparse collision correction,
`C` has full row rank `N/2` for every dyadic `2<=N<=128`.  Hence its columns
span the entire pair-constant space and

\[
 \boxed{(I-P_C)(\bar c-Hx)=0}
\]

for the actual affine vector, indeed for every vector.  The exact left-null
basis is empty, so its Arb coordinate tuple, coordinate supports, residual
support, and weighted projection energy are all empty or zero.  A general
exact implementation using the Gram `L^T W_-^{-1}L` was retained and tested on
a nontrivial sparse left kernel.

At 192-bit precision the independently evaluated scaled odd prime-power
diagonal

\[
 {N\over\log^2(2N)}
 \sum_{\substack{N<r<2N\\r\text{ odd}}}{\Lambda(r)^2\over r^2}
\]

is respectively `0.139561452, 0.167331409, 0.105472584, 0.135777594,
0.089908252, 0.091012125, 0.080296855` for
`N=2,4,8,16,32,64,128`.  Thus the pair-constant residual neither cancels nor
reinforces the odd diagonal; only the separate affine jump square remains.
This is a finite exact/Arb audit, not a contraction result.

The rank statement is in fact exact for every even `N`, not merely the tested
range.  The columns `N/2<=d<N` form the unit lower-triangular block

\[
C_{k,d}=\mathbf1_{d\le k}\qquad(N/2\le k,d<N),
\]

because `k<2d`.  Hence `P_C=I` for every positive shell weight and the queued
collision premise is decisively false.  Four-row relations belong only to a
column-deleted surrogate and cannot contribute to the actual decomposition.

The full affine residual is therefore exactly

\[
\boxed{
\mathcal R_{\rm odd}
=\sum_{k=N/2}^{N-1}{N\over(2k+1)^2}
\left(A-{\Lambda(2k+1)\over\log(2N)}\right)^2.}
\]

### Next queued main-funnel step

Use the explicit triangular representation of the pair-average to write the
effective coarse coefficient `gamma` by first differences.  Compare that exact
 coefficient vector with the preceding-scale Mobius taper, retaining the affine
 prime jump square.  Determine whether the discrepancy has a convolution
 collapse or whether its control is again equivalent to a Mertens-strength
 correlation.

## Cycle 30: exact shell first differences and local convolution collapse

Write `n=N/2`, `L=log(2N)`, and let

\[
 \chi(m)=\sum_{\substack{q\mid m\\q\text{ odd}}}
 \mu(q)\log(2N/q).
\]

If `m_o` is the odd part of `m`, divisor convolution gives

\[
 \chi(m)=L\mathbf1_{m_o=1}+\Lambda(m_o)\mathbf1_{m_o>1}.
\]

For `z=bar c-Hx`, the unique shell-supported coefficient `gamma^sh` with
`z_k=sum_(d=n)^k gamma_d^sh` has the essential boundary value

\[
 \gamma_n^{\rm sh}=1+A\left(2n+{n\over2n+1}\right)
 -{1\over L}\left(\sum_{m\le2n}\chi(m)
 +{n\over2n+1}\Lambda(2n+1)\right),
\]

and, for `n<d<N`, the exact local formula

\[
 \boxed{\gamma_d^{\rm sh}=A\left(2+{1\over(2d-1)(2d+1)}\right)
 -{\chi(2d)+{d\over2d-1}\Lambda(2d-1)
 +{d\over2d+1}\Lambda(2d+1)\over L}.}
\]

Thus the interior first differences collapse to the odd part of `d` and its
two adjacent odd integers; only the single boundary coordinate retains a
cumulative convolution.

With the preceding taper

\[
 a_d=\mu(d){\log(N/d)\over\log N}.
\]

its exact discrepancy `Delta=gamma^sh-a` is

\[
 \boxed{\Delta_d=\gamma_d^{\rm sh}
 -\mu(d){\log(N/d)\over\log N}.}
\]

The full energy identity is

\[
 \boxed{\|\widetilde y\|_{W_+}^2=\|U(a+\Delta)\|_{W_-}^2
 +\sum_{k=n}^{N-1}{N\over(2k+1)^2}
 \left(A-{\Lambda(2k+1)\over L}\right)^2,}
\]

for the odd-source vector `tilde y=c-Ox`, where `U_(k,d)=1_(d<=k)`.
Expanding the first square leaves the mixed term
`2< Ua,U Delta >`; the local convolution collapse gives no sign for this
correlation.  For the actual completed vector `y=tilde y-Ee`, the shell
coefficient is `gamma^sh-p`, where

\[
 p_n=-{1\over L}\sum_{m\le n}\xi(m),\quad
 p_d=-{\xi(d)\over L}\ (d>n),\quad
 \xi(m)=\log N\mathbf1_{m_o=1}+\Lambda(m_o)\mathbf1_{m_o>1}.
\]

Hence its first energy term is `||U(a+Delta-p)||^2`; the affine odd
prime-power square remains intact.  Full details are in
`shell-first-difference-report.md`.

The accompanying `analyze_effective_shell.py` implements the actual
coefficient `gamma^sh-p` with divisor-sum prefixes and no dense matrices.  At
192-bit Arb precision it certifies pair-average reconstruction and
`E_fine=E_effective+E_jump` through `N=8192`.  At that endpoint the normalized
energies are respectively `6.260278071359`, `6.218714150019`, and
`0.041563921340`.  The preceding taper image and discrepancy image energies are
`414295.614215` and `414235.669294`; their large cancellation shows why
separate norm bounds do not control the effective term.

The preceding raw taper image in that sentence is not the preceding completed
vector and is not the invariant contraction comparator.  The corrected direct
recurrence uses

\[
u_k=kA_N-\psi(k)/\log N
\]

and the exact pair average

\[
z_k=2kA_{2N}-\psi(2k)/\log(2N)
+{k\over2k+1}\left(A_{2N}-{
\Lambda(2k+1)\over\log(2N)}\right).
\]

Putting `delta=z-u`, polarization gives

\[
\boxed{E_N-E_{2N}
=-2\langle u,\delta\rangle_{W_-}
-\|\delta\|_{W_-}^2-R_{\rm jump}.}
\]

Thus the exact necessary and sufficient nonexpansion condition is

\[
\boxed{\langle u,\delta\rangle_{W_-}
\le-{1\over2}(\|\delta\|_{W_-}^2+R_{\rm jump}).}
\]

The analyzer now checks this identity independently.  The normalized shell
decrements at `N=32,128,512,2048,8192` are respectively
`+0.0155868,-0.0867393,-0.371475,-1.02298,-3.86119`.  Hence this shell
recurrence is not generically or empirically monotone at the tested larger
scales.  This does not decide the complete endpoint functional, which includes
the other ranges.

The first-difference coefficient is only a shell-supported gauge: the full
coarse dictionary has a right kernel.  Coefficient signs, Euclidean norms, and
coefficientwise correlations are not invariant.  Only the image-space vectors
`u,z,delta` and their weighted energies may be used for contraction claims.

The jump term has the unconditional asymptotic

\[
R_{\rm jump}={1\over2\log(2N)}
-{1/4+\log2\over\log^2(2N)}+o(\log^{-2}N).
\]

The affine terms affect only the secondary coefficient; they do not remove the
leading prime-square mass.

### Next queued main-funnel step

Analyze the invariant correlation `sum w_k u_k delta_k` directly using the
explicit two-scale Chebyshev formula for `delta_k`.  Sum before bounding and
separate the deterministic PNT cancellation from the single remaining odd
logarithmically weighted Mertens transform.  Audit whether any useful sign
would be equivalent to an RH-strength Mertens correlation.

## Cycle 32: centered Chebyshev correlation

Put

\[
a=A_N-1/\log N,
\qquad b=2(A_{2N}-1/\log(2N))-a,
\]

\[
E_k=\psi(k)-k,
\qquad
F_k=\psi(2k)+{k\over2k+1}\Lambda(2k+1)-2k.
\]

Then exactly

\[
u_k=ka-E_k/\log N,
\]

\[
\delta_k=kb+{k\over2k+1}A_{2N}
+E_k/\log N-F_k/\log(2N).
\]

The complete deterministic PNT slope has canceled. The weighted correlation
expands into two elementary slope sums, three linear centered-Chebyshev sums,
and the quadratic channel

\[
-{1\over\log^2N}\sum{E_k^2\over k(k+1)}
+{1\over\log N\log(2N)}
\sum{E_kF_k\over k(k+1)}.
\]

Endpoint-preserving Abel formulas reduce each linear term to finite weighted
Lambda sums. The mixed quadratic term remains the decisive signed channel.

Parity does not isolate one odd Mertens block. The exact identity

\[
\log X A_X=\mathcal L_o(X)-\tfrac12\mathcal L_o(X/2)
\]

leaves centered odd blocks at `N/2,N,2N`, while the quadratic Chebyshev product
is independent of that linear reduction. RH-strength odd-Mertens magnitude
bounds make the slope defects small but do not provide the required sign.

Pair averaging and the jump square combine exactly into

\[
E_{2N}=\sum_k\left[
{N\over k(2k+1)}v_k^2
+{N\over(2k+1)(k+1)}(v_k+j_k)^2\right],
\]

where `v_k=2kA_(2N)-psi(2k)/log(2N)` and
`j_k=A_(2N)-Lambda(2k+1)/log(2N)`. Their prime diagonals reinforce rather than
cancel, producing order `1/log N` in the fine energy.

At `N=8192`, the analyzer's four exact uncentered correlation components are
approximately `+39.86999,+44.10513,-87.35993,-0.008114`, summing to
`-3.39293`. This is large finite cancellation, not evidence for an asymptotic
sign law.

A hostile aggregate audit confirms structurally that PNT-sized linear
information cannot determine this quadratic local sign. The identity
`mu*1=epsilon` is indispensable for the local collapse; retaining only
`Lambda=-mu*log` leaves arbitrary surrogate freedom. Numerical perturbation
examples are recorded only as diagnostics, not rigorous certificates.

### Next queued main-funnel step

Rewrite the joint quadratic expression in `E_k,F_k` as a finite bilinear form
in Lambda increments. Separate diagonal, fixed-shift, and genuinely
off-diagonal pieces. Determine whether its needed favorable contribution is a
known sieve-scale estimate, an RH consequence, or a stronger prime-pair/Mobius
statement.

## Cycle 33: increment audit and recombination

The centered increment expansion is exact but not canonical.  With
`x_r=Lambda(r)-1`, the `E^2` kernel is the usual max/prefix kernel, while the
`EF` kernel has a dyadic prefix rectangle and a separate odd endpoint fan.
Endpoints below `N/2`, the bulk endpoint `2N-2`, and the odd endpoint `2N-1`
must all be retained.

An Arb analyzer decomposes the isolated quadratic channel into literal
diagonal, same-prefix fixed-shift, structured odd-dilation endpoint, and generic
off-diagonal rectangle.  At `N=8192` the pieces are approximately

\[
-0.0040256251,
\quad +0.0040046379,
\quad -0.0000015132,
\quad -0.0003930616,
\]

recombining to `-0.0004155620`.  This split diagnoses cancellation but cannot
support separate estimates: bounded nonnegative surrogate increments with
summatory function `x+O(1)` can force either sign, and even a PSD prefix energy
can have diagonal and one fixed shift individually of order `N` while their
complete sum is bounded.

More importantly, the apparent `E_kF_k` prime-pair channel cancels exactly when
the correlation is recombined with the discrepancy square.  If

\[
x_k=E_k/\log N,
\qquad y_k=F_k/\log(2N),
\]

then

\[
\langle x,y-x\rangle
=\tfrac12(\|y\|^2-\|x\|^2-\|y-x\|^2).
\]

In the full decrement, writing `u=p-x` and `u+delta=p+h-y`, one gets

\[
\boxed{-2\langle u,\delta\rangle-\|\delta\|^2
=\|p-x\|^2-\|p+h-y\|^2.}
\]

Thus a separate Hardy--Littlewood estimate for the mixed `EF` term is not
intrinsically required; expanding it prematurely manufactures prime-pair
subproblems.  The safe obstruction is again a signed comparison of two complete
cumulative-square energies plus the negative jump square.  There is no generic
Loewner or martingale order between them.

Under RH, the explicit formula turns `E_k` and `F_k` into oscillatory zero waves
sampled a logarithmic distance `log 2` apart.  RH fixes their amplitudes but not
the phase of this lagged correlation.  Therefore RH alone is not presently a
known source of the required sign.

### Next queued main-funnel step

Derive an endpoint-safe Abel decomposition of the recombined square difference
`||p-x||^2-||p+h-y||^2-R_jump` without opening it into raw prime pairs.  Search
for a finite zero-Gram or dyadic-transfer representation whose only indefinite
part is a sharply identified lag-`log 2` zero phase statistic.

## Cycle 33: exact Lambda-pair split of the quadratic channel

Put `h_r=Lambda(r)-1`, so `E_k=sum_(r<=k) h_r` and
`psi(2k)-2k=sum_(r<=2k)h_r`.  The centered quadratic channel divided by `N`
now splits exactly into four pieces: the `h_r^2` diagonal; the remaining
same-prefix pairs, grouped as a fixed-shift family; the structured endpoint
pairing with `Lambda(2k+1)`; and the generic rectangle `r<=k<s<=2k`.

`analyze_effective_shell.py` computes the direct centered-Chebyshev expression
and the four Lambda-pair pieces independently with Arb.  Entrywise divisor
convolutions supply exact Lambda balls, and recombination is certified for
every dyadic `2<=N<=8192`.  At `N=8192`, in the correlation-divided-by-`N`
normalization, the pieces are

\[
-0.00402562513630,
\quad +0.00400463793787,
\quad -0.00000151317961104,
\quad -0.000393061613528,
\]

which recombine to `-0.000415561991575`.  The exact centered diagonal and the
fixed-shift family nearly cancel; the generic off-diagonal rectangle is the
largest residual piece at this endpoint.  This is a finite exact/Arb
classification, not a sign theorem.

### Next queued main-funnel step

Analyze the generic cross-window form
`sum_k w_k sum_(r<=k<s<=2k) h_r h_s`.  Determine whether its required bound or
sign follows from a known Selberg/sieve variance estimate, requires a uniform
prime-pair estimate over the moving ratio window, or is stronger than RH.

## Cycle 34: abstract lag-`log 2` zero-wave audit

The finite zero-wave statistic

\[
 \mathcal C_h={\sum_j a_j^2\cos(h\gamma_j)\over\sum_j a_j^2},
 \qquad h=\log2,
\]

is the long-average correlation of conjugate-paired waves sampled at lag `h`.
Critical-line pairs at ordinates `2pi/h` and `pi/h` give signs `+1` and `-1`,
respectively.  This freedom survives rough zeta-zero density: concentrate a
continuous density `3M'(t)dt` in the one-third phase arcs where `cos(ht)>=1/2`,
or in the opposite arcs where `cos(ht)<=-1/2`, and quantize cumulative mass to
simple ordinates.  Both constructions satisfy

\[
 N(T)=M(T)+O(\log T),
 \qquad M(T)={T\over2\pi}\log{T\over2\pi}-{T\over2\pi},
\]

after an arbitrary finite initial completion, while every positive weighted
truncation has the selected strict sign.  Reflection gives exact conjugation
and all abstract zeros lie on `Re s=1/2`.

Therefore RH location plus rough density cannot by themselves determine the
lag sign.  This is not a model of zeta's Euler product or full explicit formula,
so it does not show that RH together with those extra structures is
insufficient.  The full construction and scope are recorded in
`lag-log2-zero-model-audit.md`.

## Cycle 34: endpoint-safe Abel formula for the recombined decrement

Put `n=N/2`, `m=N-1` and define the complete cumulative vectors

\[
 U_k=kA_N-\psi(k)/\log N,
 \qquad
 Y_r=rA_{2N}-\psi(r)/\log(2N).
\]

The exact increments are sparse:

\[
 U_k-U_{k-1}=A_N-\Lambda(k)/\log N,
 \qquad
 Y_r-Y_{r-1}=A_{2N}-\Lambda(r)/\log(2N).
\]

The two members of each fine pair are `Y_(2k)=v_k` and
`Y_(2k+1)=v_k+j_k`.  Hence the pair-average identity
`||Y||^2=||z||^2+R_jump` converts the full decrement into a difference of two
complete cumulative-square energies.  Applying

\[
 \sum_{r=a}^b{C T_r^2\over r(r+1)}
 ={C\over a}T_a^2-{C\over b+1}T_b^2
 +C\sum_{r=a+1}^b{(T_r-T_{r-1})(T_r+T_{r-1})\over r}
\]

at the two scales gives

\[
\boxed{\begin{aligned}
 E_N-E_{2N}={}&2(U_n^2-Y_N^2)+(Y_{2N-1}^2-U_m^2)\\
 &+N\sum_{k=n+1}^m {A_N-\Lambda(k)/\log N\over k}
 (U_k+U_{k-1})\\
 &-2N\sum_{r=N+1}^{2N-1}
 {A_{2N}-\Lambda(r)/\log(2N)\over r}(Y_r+Y_{r-1}).
\end{aligned}}
\]

This is endpoint-safe: it retains both left squares, both right squares, and
all lower-shell history through the cumulative vectors.  It is also
cancellation-preserving: no `E_kF_k` or raw prime-pair channel is opened.  The
odd jump is absorbed as the ordinary increment
`Y_(2k+1)-Y_(2k)=A_(2N)-Lambda(2k+1)/log(2N)`.

Equivalently, with `q_k=U_k^2-z_k^2`,

\[
 E_N-E_{2N}=2q_n-q_m+N\sum_{k=n+1}^m{q_k-q_{k-1}\over k}-R_{\rm jump}.
\]

Writing `a_k=Delta U_k`, `b_k=Delta z_k`, its interior packet is exactly

\[
 q_k-q_{k-1}={1\over2}(a_k-b_k)(U_k+U_{k-1}+z_k+z_{k-1})
 +{1\over2}(a_k+b_k)(U_k+U_{k-1}-z_k-z_{k-1}),
\]

which preserves the cross-scale cancellation.  The first difference `b_k` is
local and uses only `Lambda(2k-1),Lambda(2k),Lambda(2k+1)` with the exact
rational endpoint weights.  Every interior sign is therefore localized to one
increment-times-adjacent-cumulative packet; the four-square boundary remains
indefinite, and no global sign follows from positivity alone.  Full details are
in `cycle-34-endpoint-safe-abel-shell.md`.

The Arb analyzer independently verifies this Abel decomposition through
`N=8192`. At that endpoint its boundary, diagonal-increment, and
cumulative-increment packets are approximately

\[
+2.17136021372,
\qquad +133.173825870,
\qquad -139.206371610,
\]

recombining to the shell decrement `-3.86118552583`. The packet sizes again
show that separate absolute estimates are unusable.

## Cycle 34: finite-zero shell Gram

An endpoint-correct finite explicit formula gives a finite affine Gram
representation of the recombined shell-square difference. For a symmetric,
complete finite zero multiset `Z(T)`, counted with multiplicity, define

\[
S_N(s)=\sum_{k=N/2}^{N-1}{Nk^s\over k(k+1)}.
\]

The zero-by-zero block is

\[
\boxed{K^{(N)}_{\rho\sigma}=
{S_N(\bar\rho+\sigma)\over\bar\rho\sigma}
\left({1\over\log^2N}-{2^{\bar\rho+\sigma}\over\log^2(2N)}\right).}
\]

The affine row and constant retain the trivial-zero term, the half-`Lambda`
correction converting symmetric `psi_0` to right-continuous `psi`, the odd
interpolation endpoint, and the complete jump square. The matrix is a
difference of two PSD Gram matrices, not a PSD matrix.

Under RH, its off-diagonal entries contain the exact phase

\[
e^{i(\eta-\gamma)\log2}
\]

times the finite Mellin shell factor `S_N(1+i(eta-gamma))`. The diagonal is
explicit but does not determine the sign of the full Gram difference.

The representation includes an exact truncation correction in terms of the
finite explicit-formula remainders at every shell integer. A valid certificate
must use one common cutoff, exact half-jumps, zero completeness and
multiplicities, directed rounding, and a cancellation-preserving remainder
bound. Finite-zero computation alone proves only bounded-`N` statements unless
supplemented by a uniform tail and phase theorem.

Abstract critical-line zero models with conjugation and
`N(T)=M(T)+O(log T)` can force either sign of the lag statistic by placing
ordinates in opposite phase arcs. Hence RH location and rough zero density do
not control the sign; additional zeta-specific Euler-product or explicit-formula
phase information is indispensable. See `finite-zero-shell-gram.md` and
`lag-log2-zero-model-audit.md`.

### Next queued main-funnel step

Sum the endpoint-safe Abel packets over consecutive dyadic scales and inspect
whether their four-square boundaries telescope against the next shell. In
parallel, apply Landau-type explicit formulas to the **weighted** lag kernel to
test whether the Euler product supplies a sign-sensitive main term absent from
abstract zero-density models.
