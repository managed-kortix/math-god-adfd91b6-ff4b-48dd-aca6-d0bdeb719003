# Adversarial audit of the candidate weighted-pair theorem

## Verdict

There are three materially different statements hiding under the phrase
"weighted pair theorem."

1. A theorem for only the zero-zero block is **weaker than, and in general
   incomparable with, shell contraction**.  It does not control the affine
   zero term, the trivial-zero and half-jump terms, the odd interpolation
   square, or the finite-cutoff correction.
2. A theorem for the augmented affine Gram form, with the exact signed
   cutoff correction retained, is **exactly shell contraction written in zero
   coordinates**.  Expanding it by the explicit formula recovers the original
   weighted prime shell square term by term.
3. A theorem that replaces the signed cutoff correction by an absolute error
   majorant and asks for enough margin to beat that majorant is **strictly
   stronger than shell contraction as a formal finite statement**.  The loss
   comes from the triangle inequality, not from arithmetic information.

Thus the candidate becomes sufficient only at the point where it is either an
exact reformulation of the target or a stronger error-buffered version of it.
No known pair-correlation theorem supplies the missing implication.

## 1. Exact objects and sign

Let

\[
 n=N/2,\qquad m=N-1,\qquad
 w_k={N\over k(k+1)},
\]

and use the definitions from `finite-zero-shell-gram.md`.  In particular,

\[
 D_N=\|p-x\|_W^2-\|p+h-y\|_W^2-R_{\rm jump}
     =E_N-E_{2N}.
\tag{1}
\]

The shell contracts exactly when

\[
 \boxed{D_N\geq0.}
\tag{2}
\]

For one common finite zero cutoff `T`, write

\[
 Q_{N,T}=\sum_{\rho,\sigma\in Z(T)}K^{(N)}_{\rho\sigma},\qquad
 L_{N,T}=2\Re\sum_{\rho\in Z(T)}q^{(N)}_\rho.
\]

Then the finite affine Gram value and exact cutoff correction are

\[
 D_{N,T}=c_N+L_{N,T}+Q_{N,T},
\tag{3}
\]

\[
 \mathcal R_{N,T}:=D_N-D_{N,T}
 =2\Re\langle g_{0,T},\epsilon_{0,T}\rangle_W+\|\epsilon_{0,T}\|_W^2
 -2\Re\langle g_{1,T},\epsilon_{1,T}\rangle_W-\|\epsilon_{1,T}\|_W^2.
\tag{4}
\]

Consequently the exact candidate weighted-pair inequality is

\[
 \boxed{
 Q_{N,T}\geq-c_N-L_{N,T}-\mathcal R_{N,T}.}
\tag{WP}
\]

By (3)--(4), `(WP)` is equivalent, with no asymptotics or omitted terms, to
`D_N>=0`.  Calling `(WP)` a pair-correlation theorem does not make it an
intermediate theorem: its right side contains precisely all the non-pair and
cutoff data needed to turn the pair block back into the full target.

If only a certified bound `|mathcal R_(N,T)|<=B_(N,T)` is used, the convenient
sufficient statement

\[
 Q_{N,T}\geq-c_N-L_{N,T}+B_{N,T}
\tag{WP+}
\]

implies contraction, but is stronger.  For example, contraction can hold with
`mathcal R_(N,T)>0` while `(WP+)` fails by almost `2B_(N,T)`.  There is no
reverse implication without signed remainder information.

## 2. Explicit-formula expansion of the pair block

Put

\[
 E_k=\psi(k)-k,\qquad E_{2k}=\psi(2k)-2k,
\]

and recall the exact finite formula

\[
 Z_T(q)=B(q)+r_T(q)-(\psi(q)-q).
\tag{5}
\]

Since

\[
 \sum_{\rho\in Z(T)}\phi_\rho(k)={Z_T(k)\over\log N},\qquad
 \sum_{\rho\in Z(T)}\chi_\rho(k)={Z_T(2k)\over\log(2N)},
\]

the allegedly spectral pair statistic expands exactly as

\[
\boxed{\begin{aligned}
Q_{N,T}=\sum_{k=n}^{m}w_k\bigg[&
 {\bigl(B(k)+r_T(k)-E_k\bigr)^2\over\log^2N}\\
 &-{\bigl(B(2k)+r_T(2k)-E_{2k}\bigr)^2\over\log^2(2N)}
 \bigg].
\end{aligned}}
\tag{6}
\]

This is already a difference of two weighted prime-power square energies.  It
has no positivity: each square sum is positive, but their difference is not.
The odd value `Lambda(2k+1)` is absent from (6) because it belongs to the
affine vector `d_1` and to `R_jump`, not to the zero-zero kernel.

Now add the linear and constant terms.  From

\[
 g_{0,T}(k)=p_k-{B(k)\over\log N}+{Z_T(k)\over\log N}
            =p_k-{E_k\over\log N}+{r_T(k)\over\log N},
\]

and

\[
\begin{aligned}
g_{1,T}(k)
 &=(p+h)_k-{B(2k)+\vartheta_k\Lambda(2k+1)\over\log(2N)}
                +{Z_T(2k)\over\log(2N)}\\
 &=(p+h)_k-{E_{2k}+\vartheta_k\Lambda(2k+1)\over\log(2N)}
                +{r_T(2k)\over\log(2N)},
\end{aligned}
\]

the correction vectors

\[
 \epsilon_{0,T}(k)=-{r_T(k)\over\log N},\qquad
 \epsilon_{1,T}(k)=-{r_T(2k)\over\log(2N)}
\]

give

\[
 g_{0,T}+\epsilon_{0,T}=p-x,
 \qquad
 g_{1,T}+\epsilon_{1,T}=p+h-y.
\tag{7}
\]

Substitution of (7) into `(WP)` cancels every `B`, `r_T`, and zero-sum term
and leaves

\[
 \|p-x\|_W^2-\|p+h-y\|_W^2-R_{\rm jump}\geq0,
\tag{8}
\]

which is exactly (2).  On opening `x` and `y`, (8) is

\[
\begin{aligned}
0\leq D_N={}&\sum_{k=n}^{m}{N\over k(k+1)}
 \left(kA_N-{\psi(k)\over\log N}\right)^2\\
&-\sum_{r=N}^{2N-1}{2N\over r(r+1)}
 \left(rA_{2N}-{\psi(r)\over\log(2N)}\right)^2.
\end{aligned}
\tag{9}
\]

Formula (9) is the original shell contraction inequality.  This explicit
expansion is the decisive circularity test.

## 3. Classification of common variants

### Pure pair-block positivity

The statement `Q_(N,T)>=0` is neither shell contraction nor a sufficient
condition for it.  Even if true, the affine quantity `c_(N)+L_(N,T)`, the jump
square, and the correction (4) can overturn its sign.  Conversely, contraction
can hold while `Q_(N,T)<0`, because favorable affine cross terms may dominate.
The kernel itself is a difference of two Gram matrices, so abstract positivity
has no basis.

### Diagonal dominance or a Montgomery asymptotic

Controlling only `rho=sigma`, or replacing the off-diagonal measure by a
limiting pair-density law, is weaker.  The target is a cancellation-scale
difference of two bulk energies.  An `o(1)` error in a conventionally
normalized pair statistic need not be `o(D_N)`, need not be uniform in `N`, and
does not retain the affine and endpoint packets.  Such a theorem can be true
while (2) has either sign.

### Full augmented affine theorem

The assertion `a^* mathcal K^(N) a + mathcal R_(N,T)>=0`, where the affine
index, all endpoint terms, and the exact signed correction are included, is
exactly (2).  It is not weaker and not stronger.  It is a coordinate change.

### Uniform coefficient or matrix positivity

Asserting positivity for every coefficient vector, or positive semidefiniteness
of the augmented kernel matrix, is stronger than the needed assertion for the
single zeta coefficient vector `a=(1,1,...)`.  It is also false in the natural
ambient setting: the underlying coarse-minus-fine form already has an
indefinite rational certificate at `N=2`.  Restricting to the actual zeta
vector avoids that counterexample but returns to the exact target.

### Prime-pair reformulation

Opening the squares in (9) produces diagonal `Lambda(a)^2` terms and weighted
off-diagonal correlations `Lambda(a)Lambda(b)` across the two moving windows.
A prime-pair theorem with exactly the one-sided remainder needed to prove (9)
is equivalent arithmetic content.  It is noncircular only if proved from an
input that does not already contain this cross-window quadratic bound.

## 4. A genuinely intermediate statement

There is a noncircular weaker target on the prime side.  Let `u` be the coarse
completed vector, `z` the weighted fine-pair average, and `delta=z-u`.  The
exact image-space identity is

\[
 D_N=-2\langle u,\delta\rangle_{W_-}
       -\|\delta\|_{W_-}^2-R_{\rm jump}.
\tag{10}
\]

Define the compensated covariance gain

\[
 \boxed{G_N=-\langle u,\delta\rangle_{W_-}-{1\over2}R_{\rm jump}.}
\tag{11}
\]

Then

\[
 D_N=2G_N-\|\delta\|_{W_-}^2.
\tag{12}
\]

For a fixed constant `0<c<1/2`, consider

\[
 \boxed{G_N\geq c\|\delta\|_{W_-}^2.}
\tag{IC_c}
\]

This statement is genuinely weaker than contraction: contraction is exactly
`(IC_c)` with `c=1/2`, while any `c<1/2` leaves the possible deficit
`D_N>=-(1-2c)||delta||^2`.  It is not obtained by merely dropping positive
terms from `(WP)`; it asserts a scale-free favorable correlation between the
coarse completed error and the cross-scale discrepancy after paying half of
the explicit prime-power jump variance.

It also has independent plausibility:

* the jump term has the unconditional leading size
  `1/[2 log(2N)]`, so (11) asks whether the mixed correlation systematically
  absorbs that explicit variance;
* finite certified data through the audited scales show a favorable mixed
  correlation even where complete shell contraction fails;
* `c<1/2` separates a robust correlation phenomenon from the sharp threshold
  required for monotonicity.

Using the certified values already reported in
`shell-first-difference-report.md`, the finite ratios are

\[
\begin{array}{c|ccccc}
N&32&128&512&2048&8192\\ \hline
G_N/\|\delta\|_{W_-}^2
&0.541&0.433&0.367&0.412&0.318.
\end{array}
\]

Thus `(IC_c)` holds at those five scales with `c=0.3`, including the four
displayed scales `N>=128` where contraction (`c=1/2`) fails.  This does not
support a uniform asymptotic claim, but it proves that the intermediate has
finite content distinct from the target rather than being a verbal weakening.

It remains a serious arithmetic statement, not a consequence of standard pair
correlation.  It may also be false uniformly.  Its value is diagnostic: a
proof for some explicit `c>0` would establish independently meaningful
cross-scale alignment without claiming RH-strength shell contraction, while a
counterexample sequence with `G_N/||delta||^2 -> 0` would kill the entire
correlation route.

A still safer averaged version is

\[
 \sum_{N\in[ X,2X)\cap2\mathbb Z}{G_N\over N}
 \geq c\sum_{N\in[ X,2X)\cap2\mathbb Z}{\|\delta_N\|_{W_-}^2\over N}.
\tag{AIC_c}
\]

This is plausibly approachable by mean-value methods, but it is substantially
weaker: averaging permits exceptional noncontracting scales and therefore
cannot imply pointwise shell contraction.

## 5. Adversarial requirements for any claimed proof

Any future weighted-pair claim should be rejected unless it states:

1. whether it controls only `Q_(N,T)` or the full augmented affine form;
2. one common zero cutoff, zero multiplicities, conjugate closure, and the
   exact half-jump convention;
3. a signed finite-cutoff correction, or an explicit declaration that an
   absolute majorant makes the theorem stronger;
4. an error measured against the shell cancellation residual, not against
   either bulk Gram norm;
5. uniformity in the moving Mellin kernel and dyadic scale `N`;
6. the result of expansion by (5), showing which new prime-side estimate is
   actually being asserted.

Without these items, "weighted pair theorem" is too ambiguous to have a
logical strength.  With all of them and the sharp sign, it is exactly shell
contraction.
