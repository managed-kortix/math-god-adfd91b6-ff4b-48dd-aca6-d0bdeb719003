# Cycle 183: every-order Reed--Muller splice audit

Let `C=RM(d,n)`, let `N=2^n`, and identify a balanced midpoint cut
`A subseteq F_2^n` with its Boolean indicator `a=1_A`.  Write `E=E_{n,s}`
for the truth tables having circuits of size at most `s`.  The random-order
splice theorem cannot be strengthened to every order by using the same
Reed--Muller packing.  A coordinate-hyperplane cut makes every such splice
easy.

## Exact characterization at a fixed cut

For `f,g in C`, put `q=f+g`.  The oriented splice that uses `f` on `A` and
`g` off `A` is

\[
 f\star_A g=g+a(f+g)=g+aq.                                      \tag{183.1}
\]

Consequently the exact number of hard ordered off-diagonal splices is

\[
 H_A=\sum_{0\ne q\in C}
 \left(|C|-\left|(C+aq)\cap E\right|\right).                    \tag{183.2}
\]

Thus many Reed--Muller pairs yield hard splices precisely when many of the
affine translates `C+aq` have small intersection with `E`.  Distance, balance,
and generalized Hamming weights alone do not control the intersections in
(183.2), because membership in `E` is a circuit-complexity property.

Two useful sufficient tests point in opposite directions:

* If `C+aC subseteq E`, then `H_A=0`.
* If for a set `Q subseteq C\{0}` one has
  `|(C+aq) cap E| <= rho|C|` for every `q in Q`, then
  `H_A >= (1-rho)|Q||C|`.

The second statement is only a reformulation of the needed hardness input; it
is not supplied by the weight hierarchy.

## Explicit bad order

Take

\[
 A=\{x\in F_2^n:x_1=0\},\qquad a(x)=1+x_1,
\]

and order all coordinates of `A` before all coordinates of its complement.
This is a balanced cut.  Equation (183.1) gives

\[
 f\star_A g=(1+x_1)f+x_1g.
\]

After multilinear reduction this polynomial has degree at most `d+1`.
Therefore

\[
 f\star_A g\in RM(d+1,n)
\]

for every ordered pair `f,g in RM(d,n)`, in both orientations.  If

\[
 s\ge (d+1)\sum_{j=0}^{d+1}{n\choose j},                         \tag{183.3}
\]

the usual monomial-by-monomial construction puts all of `RM(d+1,n)` inside
`E_{n,s}`.  Hence `H_A=0`: not merely few, but no Reed--Muller codeword pairs
give hard midpoint splices in this order.

For the concrete Cycle 182 choice `d=2` and
`s=floor(2^n/(64n))`, condition (183.3) holds for every `n>=24` (and then
continues to hold by the elementary ratio comparison).  The random-order
theorem's parameter regime therefore already contains this explicit bad
family of orders.

More generally, if the balanced indicator `a` has algebraic degree `t`, then

\[
 C+aC\subseteq RM(d+t,n).
\]

Every low-ANF-degree balanced cut is consequently bad whenever the circuit
threshold includes that larger Reed--Muller code.  Affine hyperplanes give the
sharpest instance with `t=1`.

## What generalized Hamming weights do show

At the hyperplane cut, the subcode

\[
 x_1 RM(d-1,n-1)\subseteq RM(d,n)
\]

has dimension

\[
 \sum_{j=0}^{d-1}{n-1\choose j}
\]

and is supported entirely on the half `x_1=1`.  Equivalently, the restriction
of `RM(d,n)` to `x_1=0` has dimension
`sum_(j=0)^d binom(n-1,j)`.  This is exactly the kind of large half-supported
subcode detected by generalized Hamming weights.  It explains why an
adversarial half-set can destroy random-cut restriction behavior, but it does
not turn any splice into a hard truth table.  In the same example the explicit
degree calculation proves that all splices are easy.

The conclusion is therefore negative only for the proposed strengthening and
its Reed--Muller splice witness.  It does not prove that MCSP has a small OBDD
in this order; a different family of easy inputs or a different lower-bound
method could still separate midpoint states.
