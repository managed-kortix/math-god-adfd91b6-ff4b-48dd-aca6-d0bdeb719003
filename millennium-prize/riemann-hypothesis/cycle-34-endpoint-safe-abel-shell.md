# Cycle 34: endpoint-safe Abel formula for the full shell decrement

Let `N` be even, put

\[
 n=N/2,\qquad m=N-1,\qquad L_X=\log X,
\]

and retain the affine constants `A_X` from the completed shell construction.
The coarse and fine cumulative vectors are

\[
 U_k=kA_N-\frac{\psi(k)}{L_N}\quad(n\leq k<N),
 \qquad
 Y_r=rA_{2N}-\frac{\psi(r)}{L_{2N}}\quad(N\leq r<2N).
\]

Thus `U=u`.  If

\[
 v_k=Y_{2k},\qquad
 j_k=A_{2N}-\frac{\Lambda(2k+1)}{L_{2N}},
\]

then `Y_(2k+1)=v_k+j_k`, and the pair average is

\[
 Z_k=v_k+\frac{k}{2k+1}j_k=z_k.
\]

All formulas below are in the normalized shell convention used in
`shell-first-difference-report.md`.

## Endpoint-safe Abel lemma

For an arbitrary finite sequence `T_a,...,T_b`,

\[
 \boxed{
 \sum_{r=a}^{b}\frac{C}{r(r+1)}T_r^2
 =\frac{C}{a}T_a^2-\frac{C}{b+1}T_b^2
 +C\sum_{r=a+1}^{b}\frac{(T_r-T_{r-1})(T_r+T_{r-1})}{r}.}
 \tag{34.1}
\]

This is just summation by parts with
`1/[r(r+1)]=1/r-1/(r+1)`.  Both boundary squares are essential.  In
particular, the right boundary has a minus sign and denominator `b+1`, not
`b`.

The arithmetic increments of the two cumulative vectors are exactly

\[
 \boxed{
 U_k-U_{k-1}=A_N-\frac{\Lambda(k)}{L_N},\qquad
 Y_r-Y_{r-1}=A_{2N}-\frac{\Lambda(r)}{L_{2N}}.}
 \tag{34.2}
\]

Consequently Abel summation never requires opening a product of two Chebyshev
errors.  The arithmetic input is a constant background increment plus a
sparse prime-power impulse.

## Full decrement as two Abel-summed fine squares

The pair-average/variance identity gives

\[
 \|Y\|_{W_+}^2
 =\sum_{k=n}^{m}\left\{
 \frac{N}{k(2k+1)}v_k^2
 +\frac{N}{(2k+1)(k+1)}(v_k+j_k)^2\right\}
 =\|Z\|_{W_-}^2+R_{\rm jump},
\]

where

\[
 R_{\rm jump}=\sum_{k=n}^{m}\frac{N}{(2k+1)^2}j_k^2.
\]

Since the two terms in braces are precisely the `r=2k` and `r=2k+1`
terms of

\[
 \sum_{r=N}^{2N-1}\frac{2N}{r(r+1)}Y_r^2,
\]

the full decrement is

\[
 E_N-E_{2N}
 =\sum_{k=n}^{m}\frac{N}{k(k+1)}U_k^2
 -\sum_{r=N}^{2N-1}\frac{2N}{r(r+1)}Y_r^2.
\]

Applying (34.1) at the two scales and using (34.2) gives the compact exact
formula

\[
\boxed{\begin{aligned}
 E_N-E_{2N}={}&
 2\bigl(U_n^2-Y_N^2\bigr)
 +\bigl(Y_{2N-1}^2-U_m^2\bigr)\\
 &+N\sum_{k=n+1}^{m}\frac1k
 \left(A_N-\frac{\Lambda(k)}{L_N}\right)
 (U_k+U_{k-1})\\
 &-2N\sum_{r=N+1}^{2N-1}\frac1r
 \left(A_{2N}-\frac{\Lambda(r)}{L_{2N}}\right)
 (Y_r+Y_{r-1}).
\end{aligned}}
\tag{34.3}
\]

Formula (34.3) is endpoint-safe and contains no raw prime-pair expansion.  It
also absorbs the odd jump square automatically: the odd increment
`Y_(2k+1)-Y_(2k)=j_k` is one of the ordinary fine increments in the last sum.
The even increment has the equally simple form

\[
 Y_{2k}-Y_{2k-1}=A_{2N}-\frac{\Lambda(2k)}{L_{2N}}.
\]

Thus the apparently exceptional odd endpoint fan becomes the same one-point
von Mangoldt increment as every other fine index.

## Equivalent pair-average formula

For a representation that leaves the jump reserve visible, put

\[
 q_k=U_k^2-Z_k^2,
 \qquad a_k=U_k-U_{k-1},
 \qquad b_k=Z_k-Z_{k-1}.
\]

Then

\[
 \boxed{
 E_N-E_{2N}
 =2q_n-q_m+N\sum_{k=n+1}^{m}\frac{q_k-q_{k-1}}{k}
 -R_{\rm jump}.}
 \tag{34.4}
\]

Here `a_k=A_N-Lambda(k)/L_N`, while direct first differencing of the pair
average gives the local sparse formula

\[
\boxed{\begin{aligned}
 b_k={}&A_{2N}\left(2+\frac1{(2k-1)(2k+1)}\right)\\
 &-\frac1{L_{2N}}\left[
 \Lambda(2k)
 +\frac{k}{2k-1}\Lambda(2k-1)
 +\frac{k}{2k+1}\Lambda(2k+1)\right].
\end{aligned}}
\tag{34.5}
\]

The increment in (34.4) should be retained in either of the following
equivalent cancellation-preserving forms:

\[
 q_k-q_{k-1}
 =a_k(U_k+U_{k-1})-b_k(Z_k+Z_{k-1}),
 \tag{34.6}
\]

or, more symmetrically,

\[
\boxed{\begin{aligned}
 q_k-q_{k-1}={1\over2}(a_k-b_k)
 &(U_k+U_{k-1}+Z_k+Z_{k-1})\\
 +{1\over2}(a_k+b_k)
 &(U_k+U_{k-1}-Z_k-Z_{k-1}).
\end{aligned}}
\tag{34.7}
\]

The second line of (34.7) keeps the small cross-scale cumulative difference
intact.  Expanding `U`, `Z`, or their products into separate slope,
Chebyshev-square, and mixed channels would recreate the artificial prime-pair
terms eliminated in Cycle 33.

## Exact sign localization

Define the Abel packets

\[
 \begin{aligned}
 B_N&=2(U_n^2-Y_N^2)+(Y_{2N-1}^2-U_m^2),\\
 C_k&={N\over k}\left(A_N-\frac{\Lambda(k)}{L_N}\right)
       (U_k+U_{k-1}),\\
 F_r&=-{2N\over r}\left(A_{2N}-\frac{\Lambda(r)}{L_{2N}}\right)
       (Y_r+Y_{r-1}).
 \end{aligned}
\]

Then

\[
 \boxed{E_N-E_{2N}=B_N+\sum_{k=n+1}^{m}C_k
 +\sum_{r=N+1}^{2N-1}F_r.}
 \tag{34.8}
\]

This localizes every possible sign change:

* `B_N` contains the four unavoidable endpoint squares.
* `C_k` has the sign of
  `(A_N-Lambda(k)/L_N)(U_k+U_(k-1))`.
* `F_r` has the opposite sign of
  `(A_(2N)-Lambda(r)/L_(2N))(Y_r+Y_(r-1))`.
* Away from prime powers the von Mangoldt impulse vanishes exactly; at a prime
  power it changes only the packet at that index.
* In the pair-average form, every jump packet is explicitly nonpositive:
  `-N j_k^2/(2k+1)^2`.

No unconditional common sign follows from this identity alone.  The boundary
packet is indefinite, and neither the cumulative adjacent sums nor the affine
minus-von-Mangoldt increments have a fixed sign supplied by positivity.  The
gain is structural: all cancellation is retained inside complete local
increment-times-cumulative packets, and the only arithmetic impulses are
one-point `Lambda` values rather than opened prime pairs.

## Conclusion

The two-fine-square formula (34.3) is the shortest endpoint-safe Abel form.
The pair formula (34.4)--(34.7) is preferable when the negative odd jump reserve
must remain explicit.  They are exactly equivalent.  Any subsequent estimate
should act on the complete packets in (34.3) or (34.7), not separately on their
affine and von Mangoldt pieces; such a separation would again destroy the
cancellation that motivated the recombination.
