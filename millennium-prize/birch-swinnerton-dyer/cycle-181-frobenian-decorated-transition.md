# Cycle 181: conditional Frobenian decorated transitions

## Scope

This note isolates what Chebotarev proves if the decorated one-prime state of
Cycle 178 is governed by a finite extension.  The conclusion is conditional.
In particular, saying only that the decoration is Frobenian does not imply
that its values are uniform.  Uniformity is an additional finite-group fiber
statement, and proving finite governance of the derived modular-symbol
coordinate remains the missing arithmetic hypothesis.

Fix `p=7`, a finite residual Selmer space `S` of dimension `r`, and a
decoration `z in F_7`.  After choosing compatible determinant-line
trivializations, the proposed update is

\[
 T_{\lambda,c}(S,z)=
 \begin{cases}
  (\ker\lambda,z+c),&\lambda\ne0,\\
  (S\oplus\mathbf F_7,z+c),&\lambda=0.
 \end{cases}
 \tag{181.1}
\]

The arithmetic assertion that (181.1) describes the local condition of the
quadratic twist is not proved here.

## Conditional theorem

Let `L/Q` be a finite Galois extension with group `G`, let `Sigma` contain the
ramified primes and all fixed bad primes, and let `A subset G` be a nonempty
union of conjugacy classes encoding the admissible prime packet.  Suppose the
following hypotheses hold for one fixed input state `(S,z)`.

1. **Local comparison.** For every prime `q notin Sigma` with
   `Frob_q subset A`, twisting at `q` changes the residual Selmer condition by
   exactly (181.1).
2. **Decorated finite governance.** There is a conjugacy-invariant map

   \[
     \Phi:A\longrightarrow S^*\times\mathbf F_7,
     \qquad \Phi(\operatorname{Frob}_q)=(\lambda_q,c_q),
     \tag{181.2}
   \]

   where the target coordinates are defined in common determinant lines.  It
   is enough to assume that the inverse images of all transition events below
   are unions of conjugacy classes; literal coordinates are not intrinsic if
   a change of local basis rescales them.
3. **Balanced fibers.** For every `(lambda,a) in S^* x F_7`,

   \[
     |\Phi^{-1}(\lambda,a)|=\frac{|A|}{7^{r+1}}.
     \tag{181.3}
   \]

Then, relative to admissible primes, the natural transition densities exist
and, for every `a in F_7`, are

\[
 \Pr((r,z)\longmapsto(r-1,z+a))
   =\frac{7^r-1}{7^{r+1}}
   =\frac{1-7^{-r}}7,
 \tag{181.4}
\]

and

\[
 \Pr((r,z)\longmapsto(r+1,z+a))
   =\frac1{7^{r+1}}=7^{-r-1}.
 \tag{181.5}
\]

For `r=2` and `z=0`, the relative density of a rank drop with nonzero new
decoration is

\[
 \Pr(\lambda_q\ne0,\ c_q\ne0)
 =\frac{(7^2-1)(7-1)}{7^3}
 =\boxed{\frac{288}{343}}.
 \tag{181.6}
\]

The corresponding absolute prime density is

\[
 \frac{|A|}{|G|}\frac{288}{343},
 \tag{181.7}
\]

not `288/343` unless the ambient family has already been conditioned on `A`.

### Proof

Chebotarev gives, for every union `B` of conjugacy classes in `G`,

\[
 \#\{q\le X:q\notin\Sigma,\ \operatorname{Frob}_q\subset B\}
 \sim \frac{|B|}{|G|}\operatorname{Li}(X).
 \tag{181.8}
\]

Apply this to `A` and to each fiber in (181.3), then divide the latter
asymptotic by the former.  For a fixed increment `a`, there are `7^r-1`
nonzero functionals and one zero functional.  This gives (181.4) and (181.5).
There are `(7^r-1)6` pairs with both coordinates nonzero, so setting `r=2`
gives (181.6).  Multiplication by the density `|A|/|G|` gives (181.7).

No analytic independence assumption is hidden in this proof: all required
independence is exactly the finite statement (181.3).  Conversely,
Chebotarev cannot prove (181.3); it only converts already computed fiber sizes
into prime densities.

## Pair-governed decoration and the squarefree sieve

Cycle 178 naturally writes the derived coordinate as `c(q,ell)`, where `ell`
is an auxiliary Kolyvagin prime.  In that setting (181.2) must be replaced by
a genuinely joint statement.  Let `A_2 subset G_q x G_ell` be a union of
products of conjugacy classes encoding all admissibility conditions, and
suppose

\[
 \Phi_2:A_2\longrightarrow S^*\times\mathbf F_7,
 \qquad
 \Phi_2(\operatorname{Frob}_q,\operatorname{Frob}_\ell)
   =(\lambda_q,c(q,\ell))
 \tag{181.9}
\]

has balanced fibers of size `|A_2|/7^(r+1)`.  Here `G_q x G_ell` may be
replaced by the actual image of the two Frobenius coordinates in one governing
extension; the denominator is always the size of that actual finite packet.
Two-variable Chebotarev, obtained by applying (181.8) to the two prime sums,
then gives (181.4)--(181.6) as relative densities of ordered admissible pairs.

The squarefree restriction introduces no new factor for a fixed two-prime
family.  Indeed, among pairs `q,ell <= X`, the nonsquarefree products are
exactly the diagonal `q=ell`.  The diagonal contributes `O(pi(X))`, whereas a
positive-density admissible pair packet contributes order `pi(X)^2`.
Consequently

\[
 \frac{\#\{(q,\ell)\in A_2(X):q\ne\ell,\ \lambda_q\ne0,
                    c(q,\ell)\ne0\}}
      {\#\{(q,\ell)\in A_2(X):q\ne\ell\}}
 \longrightarrow \frac{288}{343}.
 \tag{181.10}
\]

Thus the elementary squarefree sieve merely removes a zero-relative-density
diagonal and preserves the conditional constant.  The same argument works in
fixed unequal prime ranges.  If one forgets the ordering and the event is
symmetric, numerator and denominator are both divided by two.

This does **not** prove density `288/343` among all squarefree integers.  For
squarefree twists with an unbounded number of prime factors one needs a
uniform Frobenian/Selberg--Delange sieve, control of every history-dependent
state transition, and local Euler factors.  Fixed-length Chebotarev does not
supply those assertions.  Nor does a pair density automatically give a prime
twist density after choosing the least auxiliary `ell`; that projection needs
uniform bounded multiplicity, a second-moment argument, or another explicit
selection theorem.

## What remains unproved

The conditional theorem above is finite-group bookkeeping plus Chebotarev.
For the proposed `433a1`, `p=7` certificate family, the following arithmetic
inputs are still missing.

- Construct one finite Galois extension governing `c(q,ell)` jointly with
  `lambda_q`; ordinary Kummer governance of `lambda_q` does not govern `c`.
- Prove the balanced-fiber identity (181.3) or its joint version for the actual
  Galois image.  Frobenianity alone permits arbitrarily biased fibers.
- Prove the twist-at-`q` cartesian local comparison giving (181.1), uniformly
  on the admissible packet.
- Verify uniform residual image, primitivity, ordinarity, Tamagawa, local
  torsion, and root-number hypotheses for the twisted curves.
- Prove the pointwise explicit-reciprocity and rank-one converse implications
  that turn `c(q,ell) != 0` into the claimed Kurihara and BSD certificates.
- Remove the auxiliary prime if the final theorem is stated for prime twists
  rather than decorated ordered pairs.

Accordingly `288/343` is rigorously derived only as the conditional relative
density in (181.6) and (181.10).  No rank-one twist-density theorem and no BSD
case is claimed.
