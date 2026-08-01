# Cycle 213: explicit dissipative shell comparison

## Normalization and shell inequality

Use exactly the Cycle 212 normalization on the normalized `2 pi` torus:

\[
 \dot\omega_k=-\mu |k|_2^2\omega_k+
 \sum_{p+q=k}{p^\perp\cdot q\over |p|_2^2}\omega_p\omega_q,
 \qquad \omega_0=0.
 \tag{213.1}
\]

Put `S_n={k:|k|_infinity=n}` and
`z_n=sum_(k in S_n)|omega_k|`.  The upper right Dini derivative obeys

\[
 D^+z_n\leq-\mu n^2z_n+
 2\sum_{\substack{a,b\geq1\\|a-b|\leq n\leq a+b}}
 {b\over a}z_az_b.                                      \tag{213.2}
\]

Indeed `|k|_2^2>=n^2`, shell addition gives the two triangle inequalities,
and the entirely rational estimate

\[
 {|p^\perp\cdot q|\over|p|_2^2}
 \leq {2|p|_\infty|q|_\infty\over |p|_\infty^2}
 =2{b\over a}                                           \tag{213.3}
\]

applies before summing the nonnegative products.  No lattice-point count is
needed because each `z_a z_b` already sums every ordered pair in the two
shells.  This is deliberately less sharp than Euclidean `sqrt(2)b/a`, but it
has the rational constant `2` and no directed-square-root dependency.

## Finite head and geometric cap

Fix an integer `L>=1`, rational `rho>1`, rational `C>0`, and bounds

\[
 z_a\leq H_a\quad(1\leq a<L),\qquad z_a\leq Cx^a
 \quad(a\geq L),\qquad x={1\over\rho}.                 \tag{213.4}
\]

For a target shell `n`, define the following published majorant `Q_n`.
The head-head part is the exact ordered shell sum from (213.2).  For each head
index `h`, shell geometry confines a capped partner to

\[
 I_{n,h}=[\max(L,|n-h|),n+h]\cap\mathbb Z,
\]

and the two orderings are bounded by

\[
 2H_hC\left({1\over h}\sum_{a\in I_{n,h}}a x^a
       +{h\over L}\sum_{a\in I_{n,h}}x^a\right).       \tag{213.5}
\]

For two capped shells, discard the reverse triangle inequality and use
`1/a<=1/L`.  With `m=max(0,n-2L)`, this gives

\[
 {2C^2\over L}x^{2L}\sum_{s=m}^\infty
       {(s+1)(s+2L)\over2}x^s.                         \tag{213.6}
\]

All sums are rational geometric moments.  Equations (213.2), (213.5), and
(213.6) prove `D^+z_n<=-mu n^2 z_n+Q_n` throughout the box (213.4).

## Inward theorem

**Lemma 213.A.** Suppose the initial shell masses satisfy (213.4).  If

\[
 Q_n\leq\mu n^2 Cx^n\qquad(n\geq L),                  \tag{213.7}
\]

then every cap face points inward and `z_n(t)<=Cx^n` persists for as long as
the head bounds used in `Q_n` persist.

For finite replay, check (213.7) directly for `L<=n<2L`.  For `n>=2L`, the
head-head term vanishes and `Q_n/(Cx^n)` is a quadratic polynomial in `n`:
(213.5) becomes linear after writing `a=n+d`, and the shifted moments in
(213.6) are quadratic.  At `n_0=2L`, recover that polynomial from three exact
rational evaluations.  Writing the normalized dissipative margin as

\[
 A t^2+B t+D,\qquad t=n-n_0,
\]

it is nonnegative on the whole ray if

\[
 A\geq0,\quad D\geq0,\quad
 [B\geq0\ \hbox{or}\ (A>0\ \hbox{and}\ 4AD\geq B^2)]. \tag{213.8}
\]

These are inward, non-strict rational inequalities.  Equality is accepted;
strict amplification remains a separate final certificate condition.
The first-exit comparison proof applies to finite truncations, and the common
summable cap permits passage to the full convolution by dominated convergence.

## Verifier primitive

`validate_cycle212.py` now provides:

* `shell_convolution_bound`, implementing (213.5)-(213.6) with `Fraction`;
* `check_dissipative_shell_cap`, checking initial domination, every finite
  face, and the complete quadratic ray criterion (213.8);
* `low_mode_tail_remainder_bound`, deleting retained-retained pairs from the
  same ordered majorant and returning a modulus bound for each omitted
  low-mode convolution.  The complex interval `[-R,R]+i[-R,R]` is therefore
  a valid, slightly conservative remainder box.

This closes the missing mathematical primitive in item 3 of Theorem 212.A.  It
does not by itself upgrade the component manifest to `PASS FULL`: a production
certificate must still supply slab-specific head masses, initial tail
domination, low-mode remainder boxes, and successful Picard inclusions.
