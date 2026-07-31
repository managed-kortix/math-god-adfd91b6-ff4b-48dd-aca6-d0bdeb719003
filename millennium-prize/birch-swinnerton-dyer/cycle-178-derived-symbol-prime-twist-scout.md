# Cycle 178: a decorated one-prime twist transition candidate

## Verdict

The bare target "a positive density of rank-one quadratic twists" is not a
safe novelty target.  Results of Gross--Zagier--Kolyvagin, Ono--Skinner and
later work already prove positive-proportion rank-one statements in broad
twist families, while modern 2-Selmer distribution theorems prove still
stronger algebraic-rank distribution statements in many cases.  A potentially
new, sharply testable target is instead a **certificate-density theorem** in a
fixed prime-twist subfamily: positive density of twists for which one specified
residual derived modular symbol is nonzero and hence certifies rank one.

This note gives an exact finite-state transition candidate for that target. It
does not assert that the transition law or its equidistribution has been
proved.

## Concrete family

Fix

\[
 E=433\mathrm{a}1:\quad y^2+xy=x^3+1,
 \qquad p=7.
\]

Cycles 136 and 173 give two independent rational points modulo seven, and the
existing Kurihara calculation gives the relevant residual Selmer upper bound
for the base curve.  Thus this curve has a completely explicit residual
starting packet.  Consider

\[
 \mathcal F_C=\{E^{(q)}:q\text{ prime},\ \operatorname{Frob}_q\in C\},
\]

where `C` is to be one conjugacy class in a finite governing extension chosen
so that all of the following are fixed:

1. `q` is prime to `2*7*433`;
2. the local quadratic-twist conditions at `2,7,433,infinity` are constant;
3. `w(E^(q))=-1`;
4. the residual local condition at `q` is a single transverse switch; and
5. the normalized local torsion and dual-exponential factors are 7-units.

Items 1--5 are finite Frobenius or congruence conditions.  The first
computation is to exhibit one nonempty class `C`; no density claim should be
made before that calculation.

For each member choose the least auxiliary genuine Kolyvagin prime `ell` in a
second fixed Frobenius class and form Kim's normalized one-prime Kurihara
number

\[
 z(q)=\widetilde\delta^{(1)}_{\ell}(E^{(q)})\in\mathbf F_7.
\]

Using the least such `ell` makes this a definite certificate, but it is poor
for proving equidistribution.  A theorem should instead count pairs `(q,ell)`
first and remove `ell` by a bounded-multiplicity or second-moment argument.

## Exact decorated transition candidate

Let `S` be the residual self-dual Selmer space immediately before the switch,
let `r=dim_F7 S`, and let `lambda_q:S->F_7` be localization at the new
one-dimensional local quotient.  Attach a derived-symbol coordinate
`z in F_7`.  The proposed local update is

\[
 T_{\lambda,c}(S,z)=
 \begin{cases}
   (\ker\lambda,z+c),&\lambda\ne0,\\
   (S\oplus\mathbf F_7,z+c),&\lambda=0,
 \end{cases}
 \tag{178.1}
\]

where `c in F_7` is the normalized residual explicit-reciprocity coordinate of
the new Kato/Kurihara component.  Formula (178.1), once the two coordinates
are defined in common determinant lines, is the exact finite linear-algebra
candidate; there is no asymptotic approximation in it.

If `(lambda,c)` is uniform in `S^* x F_7`, its transition probabilities are

\[
 \Pr((r,z)\mapsto(r-1,z+a))=(1-7^{-r})/7
 \tag{178.2}
\]

for every `a in F_7`, and

\[
 \Pr((r,z)\mapsto(r+1,z+a))=7^{-r-1}.
 \tag{178.3}
\]

For a one-prime family only the starting layer and its two output layers are
visited.  It is therefore genuinely finite-state even though the iterated
Klagsbrun--Mazur--Rubin rank chain is infinite.  For the base packet `r=2`, the
state set is

\[
 \{2\}\times\mathbf F_7\ \sqcup\
 \{1\}\times\mathbf F_7\ \sqcup\
 \{3\}\times\mathbf F_7,
\]

Make the two output layers absorbing; then (178.2)--(178.3) specify a 21-by-21
stochastic matrix.  In particular the rank-drop branch has mass `48/49`, and
from `z=0` the candidate mass of rank drop with nonzero symbol is
`(48/49)(6/7)=288/343`.  The root-number restriction makes rank one the desired
output, but nonvanishing of `z` must still be connected to the full residual
Selmer bound for the **twisted** curve.

## The production lemma actually needed

The useful theorem is not merely Selmer-rank equidistribution.  It is the
following decorated governing-field statement.

> There are finite Galois extensions `K subset L` and a nonempty conjugacy
> packet `D subset Gal(L/Q)` above `C` such that, for all admissible pairs
> `(q,ell)`, the pair `(lambda_q,c(q,ell))` is the image of Frobenius in
> `S^* x F_7`, and every element with `lambda_q != 0` and `c(q,ell) != 0`
> occurs in `D`.

Chebotarev would then give a positive density of rank-drop, nonzero-certificate
pairs.  Core-vertex rigidity plus the pointwise explicit reciprocity law would
turn `c!=0` into Kurihara nonvanishing.  A verified rank-one `p`-converse, with
all hypotheses checked for `E^(q)`, would then give analytic and algebraic rank
one and finite 7-primary Tate--Shafarevich group.

## Hostile audit

There are four independent failure points.

- A quadratic twist at its ramified prime is not automatically the same local
  modification as adjoining a Kolyvagin prime.  The cartesian local-condition
  comparison must be written, not inferred from the KMR analogy.
- The usual governing field controls `lambda_q`; it does not automatically
  control the modular-symbol coordinate `c`.  Proving that `c` is Frobenian in
  one finite extension is the central new lemma, not notation.
- Kurihara nonvanishing for `E` does not transport to `E^(q)`.  Every
  primitivity, Tamagawa, residual-image, ordinarity and local-torsion hypothesis
  must be uniform on `C`.
- Rank-one positive density by itself is likely duplicated.  Novelty must be
  claimed, if at all, for the explicit nonzero derived-symbol certificate in a
  specified prime Frobenius packet.

## Next bounded test

Compute the first 200 admissible prime twists and 20 auxiliary primes per
twist.  Record `(local Selmer rank change,z(q,ell))`, test whether the
conditional `z` histogram is compatible with uniformity, and search for two
primes with identical Frobenius data in every proposed governing field but
different `z`.  Such a collision would decisively falsify the finite-extension
version of the candidate.  Passing the experiment would remain evidence, not
a theorem.

No BSD case, rank-one density theorem, or novelty claim is made here.
