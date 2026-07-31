# Cycle 182: explicit cross-splice orders and an OBDD lower bound

## Target and definition

Let the variables be two copies of the affine plane over `F_q`, where `q` is a
prime power:

\[
 X=\{x_{a,b}:(a,b)\in F_q^2\},\qquad
 Y=\{y_{a,b}:(a,b)\in F_q^2\}.
\]

For an order `pi` of `X union Y`, write `P_pi(t)` for its first `t` variables.
The combinatorial cross-splice property sought here is that balanced prefixes
from two orders have all four Venn cells large. The matching property needed
for an OBDD lower bound is different: at one cut of one order, many fixed pairs
`{x_v,y_v}` must have exactly one endpoint in the prefix. Fixing all other
variables then leaves equality or disequality on independent pairs. Keeping
these notions separate prevents a pair-of-orders statement from being silently
used as a one-order OBDD theorem.

The unrestricted all-cuts version is impossible. In any order, the cuts at
`t=0` and `t=2q^2` have no crossing pair. More generally, a cut with only `d`
variables on its smaller side has matching capacity at most `d`. Any valid
definition must therefore restrict to balanced cuts or state a bound depending
on the cut depth.

## Exact candidate

Fix an explicit representation of `F_q`. For every `m in F_q^*` and `c in
F_q`, first define a point order `sigma_(m,c)` by lexicographically sorting
`(ma+b+c,a)`. Its blocks are the affine lines `ma+b+c=i`. Define the lifted
variable order `pi_(m,c)` by the rank map

\[
 R_{m,c}(x_{a,b})=(a,0,b),\qquad
 R_{m,c}(y_{a,b})=(ma+b+c,1,a),
\]

ordered lexicographically using the fixed representation. Thus the `X` copy is
grouped by vertical lines and the `Y` copy by affine lines of slope `-m`; the
bit in the middle interleaves the two copies. The family has exactly `q(q-1)`
orders, seed length at most `2 log q`, and every rank is computable using
`O(log q)`-bit field operations. Excluding `m=0` makes every `Y` partition
transverse to the fixed vertical `X` partition.

For two distinct slopes `m != m'`, every block in `sigma_(m,c)` meets every
block in `sigma_(m',c')` in exactly one point. This is the strongest available
pairwise incidence statement:

\[
 |\{(a,b):ma+b+c=i,\ m'a+b+c'=j\}|=1.
\]

Consequently, if `A` is a union of `alpha q` complete `m`-blocks and `B` is a
union of `beta q` complete `m'`-blocks, then

\[
 |A\cap B|=\alpha\beta q^2
\]

exactly. Point prefixes in the two `sigma` orders differ from such block unions
by at most one block, so all four cells of their Venn diagram have product
densities up to additive `O(q)`. In particular, for `delta`-balanced point
prefixes and fixed `delta>0`, every cell has size at least

\[
 \delta^2q^2-O(q).
\]

This is an explicit orthogonal-array / pairwise-independent construction; an
extractor or small-bias generator is unnecessary for the two-order statement.
For a larger seed space or simultaneous tests against many prescribed cuts, a
linear small-bias space only controls parity tests and does not imply these
rectangle-cell lower bounds. The relevant pseudorandom object would instead be
a seeded two-source disperser or lossless condenser for the cut classes.

## Exact OBDD lower bound on the designated orders

Define the equality function on `2q^2` variables

\[
 EQ_q(X,Y)=1 \quad\Longleftrightarrow\quad
 x_{a,b}=y_{a,b}\ \text{for every }(a,b)\in F_q^2.
\]

First fix an arbitrary variable order `pi`, and cut it after exactly `q^2`
variables. Let `a` be the number of indices whose two variables are both before
the cut, `b` the number split by the cut, and `c` the number both after it.
Counting variables and indices gives

\[
 2a+b=q^2,\qquad a+b+c=q^2,
\]

so `b=q^2-2a` and `c=a`. This does not force `b` to be large: the paired order
`x_v,y_v,x_w,y_w,...` has `b=0`. Thus equality is easy in a favorable order and
cannot prove an order-independent OBDD bound.

There is nevertheless a sharp exact lower bound for every member of the affine
family. Under `pi_(m,c)`, cut after `h` complete outer blocks, hence after
`2hq` variables. The prefix contains the `hq` indices on `h` vertical lines on
the `X` side and the `hq` indices on `h` slope-`-m` lines on the `Y` side.
Transversality gives exactly `h^2` indices present on both sides. Therefore the
number of equality pairs split by the cut is

\[
 k=2(hq-h^2)=2h(q-h).
\]

The `2^k` assignments to the prefix endpoints of these pairs induce pairwise
distinct residual functions: for two assignments, complete the suffix by
copying one assignment across every split pair. Thus every deterministic OBDD
for `EQ_q` in order `pi_(m,c)` has width and size at least `2^k`. Taking
`h=floor(q/2)` proves the explicit bound

\[
 \operatorname{width}_{pi_{m,c}}(EQ_q)
 \ge 2^{2\lfloor q/2\rfloor(q-\lfloor q/2\rfloor)}
 \ge 2^{(q^2-1)/2}.
\]

With `2q^2` input variables, this is `2^{Omega(N)}` for every one of the
`q(q-1)` designated orders. It is not uniform over all variable orders: the
paired order computes equality with width two.

## Barrier verdict

The affine-plane family exactly has pairwise cross-splice for block-aligned,
balanced prefixes of distinct slopes: it has optimal one-point block
intersections, explicit rank/unrank, and no probabilistic existence step. The
same geometry gives an exponential equality OBDD lower bound for every
designated affine order. It does not yield a Millennium-relevant lower bound.

There are three independent barriers.

1. Pairwise order pseudorandomness is weaker than adversarial-order OBDD
   hardness. An OBDD chooses one favorable order; hardness on a selected family
   of orders does not exclude it.
2. Matching crossings alone prove width only for a function whose restrictions
   preserve independent equality/disequality bits. Such a function generally
   exposes the matching and may have a different easy order. Hiding all the
   matchings in one polynomial-time function is the actual order-oblivious
   branching-program problem.
3. Even an explicit exponential OBDD lower bound is a lower bound for read-once
   oblivious branching programs. There is no known resource-preserving reverse
   simulation from unrestricted circuits, RAMs, or exact relational
   `search-MCSP^SAT` to OBDDs. Therefore it does not trigger the MMW implication.

The precise next combinatorial target, if this scout continues, is stronger:
construct one polynomial-time Boolean function and an explicit polynomial-size
set of matchings such that every variable order has a balanced cut on which one
matching survives with `Omega(N)` independent restricted bits. Extractors may
help select a matching after the order is fixed, but a selector encoded in the
input gives the OBDD advance knowledge and can restore an easy order. Preventing
that quantifier reversal is the central barrier.

No unrestricted circuit lower bound or `P != NP` result is claimed.
