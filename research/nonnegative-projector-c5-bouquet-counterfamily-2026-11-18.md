# A nonsingular fixed-rank counterfamily for the nonnegative-projector bound

Date: 2026-11-18.  Scope: standalone exact note; no sharp universal lower
bound is claimed.

For a real symmetric matrix `A`, write `Pi_+(A)` and `Pi_(>=0)(A)` for the
orthogonal spectral projectors on the positive and nonnegative eigenspaces,
respectively.  This note refutes

`(Pi_(>=0)(A(G)))_(uu) >= 1/(beta(G)+2)`                         (1)

for every nonisolated vertex `u` of every finite simple graph `G`.  Here
`beta(G)=|E(G)|-|V(G)|+c(G)` is the cyclomatic rank.  The counterexamples are
connected, are nonsingular, and use only `C5` blocks and one bridge.  Thus the
failure is not caused by a zero eigenspace, and throughout the family
`Pi_(>=0)=Pi_+`.

## 1. The graph family

For `r>=1`, let `B_r` be obtained from `r` copies of `C5` by identifying one
chosen vertex from every copy to a single vertex `c`, and then adjoining one
new pendant vertex `u` adjacent to `c`.  It has

`|V(B_r)|=4r+2`, `|E(B_r)|=5r+1`, and `beta(B_r)=r`.             (2)

In particular, (1) predicts a lower bound `1/(r+2)` at `u`.

## 2. Exact spectrum and absence of zero modes

Partition the vertices into the center `c`, the `2r` cycle vertices adjacent
to `c`, the other `2r` cycle vertices, and the leaf `u`.  The corresponding
equitable divisor is

`D_r=[[0,2r,0,1],[1,0,1,0],[0,1,1,0],[1,0,0,0]]`,

and

`det(xI-D_r)=(x-1) f_r(x)`,
`f_r(x)=x^3-(2r+2)x-1`.                                        (3)

The remaining petal-difference and within-cell directions give

`chi_(B_r)(x)`
` =(x-1)(x^2-x-1)^(r-1)(x^2+x-1)^r f_r(x)`.                   (4)

One direct derivation of the exponents is as follows.  On each petal, reflection
about `c` splits the four noncentral coordinates into an antisymmetric
2-space and a symmetric 2-space.  The antisymmetric block has polynomial
`x^2+x-1`, once per petal.  In the symmetric sector, differences between
petals have polynomial `x^2-x-1`, giving multiplicity `r-1`; the common
symmetric mode, `c`, and `u` give (3).

All displayed factors have nonzero constant term, so `B_r` is nonsingular
(`det A(B_r)=-1`).  Consequently

`Pi_(>=0)(A(B_r))=Pi_+(A(B_r))`.                               (5)

The cubic has exactly one positive root.  Indeed its coefficient signs have
one variation, while `f_r(0)=-1` and `f_r(x)->+infinity`.  Denote this root by
`lambda_r`.  Moreover

`f_r(sqrt(2r+2))=-1<0`,
`f_r(sqrt(2r+3))=sqrt(2r+3)-1>0`,                              (6)

so

`sqrt(2r+2)<lambda_r<sqrt(2r+3)`.                              (7)

In particular `lambda_r>2`.

## 3. Exact leaf spectral measure

Deleting the leaf row and column from `D_r` gives characteristic polynomial

`g_r(x)=x^3-x^2-(2r+1)x+2r`.                                  (8)

Because the leaf vector lies in the equitable subspace, its diagonal
resolvent is exactly

`<e_u,(xI-A(B_r))^(-1)e_u>`
` =g_r(x)/((x-1)f_r(x))`
` =1/[2(r+1)(x-1)] + N_r(x)/f_r(x)`,                           (9)

where

`N_r(x)=((2r+1)x^2-x-(2r+1)^2)/[2(r+1)]`.                     (10)

The only positive eigenvalues seen from `u` are `1` and `lambda_r`: all
petal-difference eigenvectors are orthogonal to `e_u`.  Taking residues in
(9) therefore gives the exact nonnegative-projector diagonal

`p_r := (Pi_(>=0)(A(B_r)))_(uu)`
` =1/[2(r+1)] + N_r(lambda_r)/(3lambda_r^2-2r-2)`.              (11)

Eliminating `r` via `lambda_r^3=(2r+2)lambda_r+1` gives the useful single-root
form

`p_r=(3lambda_r^3+3lambda_r^2+2lambda_r+1)`
`    /[(2lambda_r^3+1)(lambda_r^2+lambda_r+1)].`                (12)

No numerical eigenvector calculation enters (11)--(12).

## 4. Strict refutation for every rank

Subtracting the conjectured bound from (12), again using
`2r+2=(lambda_r^3-1)/lambda_r`, factors exactly as

`p_r-1/(r+2)`
` =- (lambda_r-1)(lambda_r^2-lambda_r-1)`
`      (lambda_r^3+3lambda_r^2+2lambda_r+1)`
`   /[(2lambda_r^3+1)(lambda_r^2+lambda_r+1)`
`      (lambda_r^3+2lambda_r-1)].`                             (13)

Every denominator factor is positive.  By (7), `lambda_r>2`, so every
numerator factor shown after the minus sign is also positive.  Hence

`(Pi_(>=0)(A(B_r)))_(uu)=p_r<1/(r+2)` for every `r>=1`.         (14)

Thus (1) already fails for a unicyclic graph: `B_1` is `C5` with one pendant
leaf.  The first values (printed only for orientation, not used as proof) are

`p_1=0.3111454521... < 1/3`,
`p_3=0.1729360407... < 1/5`,
`p_6=0.1028463085... < 1/8`,
`p_7=0.09053997870... < 1/9`.                                 (15)

For comparison, `K4` has rank `3` and projector diagonal `1/4`, while `K5`
has rank `6` and projector diagonal `1/5`.  Neither is sharp for (1): the
corresponding members `B_3,B_6` are strictly smaller.

The family also locates its scale.  Exact subtraction gives

`p_r-1/(2r+2)`
` =(lambda_r^2-lambda_r-1)/[(lambda_r-1)(2lambda_r^3+1)]>0,`    (16)

while (7) and (12), or direct division, give

`lim_(r->infinity) r p_r=3/4`.                                (17)

Consequently this family rules out the proposed constant but does not
establish the sharp fixed-rank infimum.  In particular, the following remain
separate open questions:

* whether every nonisolated vertex of every rank-`r` graph satisfies some
  smaller positive bound, such as a bound on the order `1/r`;
* whether `B_r` is extremal at any fixed `r`; and
* whether a packet-specific product bound suffices in the heptacyclic bridge
  application.

## 5. Consequence for one-bridge corrections

The exact variational bridge inequality from
`fixed-rank-bridge-projector-obstruction-2026-11-14.md` contains the product

`(Pi_(>=0)(A(H)))_(uu) (Pi_(>=0)(A(K)))_(vv)`.                 (18)

If the sides have ranks `a,b>=1`, choosing `H=B_a`, `K=B_b`, and their pendant
vertices as bridge endpoints gives the exact factor `p_a p_b`, with

`p_a p_b < 1/[(a+2)(b+2)].`                                   (19)

For the heptacyclic splits this yields, for example,

`(a,b)=(1,6): p_1 p_6 = 0.032000... < 1/24`,
`(a,b)=(3,4): p_3 p_4 = 0.024391... < 1/30`.                   (20)

These decimals are diagnostics only; each strict comparison in (19) follows
from (13).  Equation (19) refutes the correction product obtained by
multiplying (1).  It does **not** show that the true full bridge gain is this
small, nor does it close or refute any square-energy theorem.
