# Notebook

## Cycle 208

The exact selector-free MCSP target is the asymmetric template: at every
balanced truth-table cut there must be `2^m` consistent prefix rows and `m`
consistent suffix queries whose completed tables have circuit size at most `s`
exactly when `z_j=1`. This immediately embeds `INDEX_m`; a sufficient
direct-sum lemma needs only a uniform easy-side upper bound and hard-side lower
bound separated by one gate, but the gap must survive every unqueried bit. The
easy-template entropy window is `m<=O(r log(n+r))`. The simplest disjoint-
subcube multiplexer has no additive rigidity: identical components share all
gates, and even distinct `f_i=H XOR x_i` share `H`, giving total size
`C(H)+O(t)` versus nominal component sum `t(C(H)-1)`. Thus restriction proves
only a maximum, not a sum. No MCSP or unrestricted lower bound follows.

## Cycle 207

Hostile audit confirms the `HWB_(8m)` construction under the one-based
convention `[8m]={1,...,8m}`. Prefix assignments are rows and suffix queries
are columns, giving `K(z,j)=z_j`, the transpose of the other common `INDEX_m`
orientation. Data and compensator sets are disjoint prefix coordinates; every
query is confined to the suffix and therefore leaves all data positions
untouched. Distinct data indices require distinct suffix weights, excluding
duplicate columns. A dependency-free verifier exhaustively evaluates every cut
through `m=3` (`N=24`, `2717096` cuts) and checks structural identities on
representative cuts through `m=64`. No flaw or counterpartition survives.
Mixing zero-based labels with `x_(|x|)` would be erroneous, but is not the
convention used. This remains an OBDD theorem, not an MCSP transfer or
unrestricted lower bound.

The constant audit shows that the midpoint is wasteful. Cutting `HWB_(6m)`
after `4m` variables and using `[m,3m]` and `[3m,5m]` gives the same exact
`INDEX_m` minor, improving the exponent from `1/8` to `1/6`. This is optimal
for the fixed-weight complementary-pair/suffix-weight prescribed-cut interval
mechanism:
after putting `2k+O(1)` prefix positions outside all accessible windows, a
near-uniform central placement makes every window contain at most
`(N-2k)/4+o(N)` prefix coordinates. Hence universal `INDEX_k` extraction by
this method requires `k/N<=1/6+o(1)` and cannot recover the known `HWB`
exponent `1/5`. The exact-minor certificate is structurally clean but does not
improve the known asymptotic HWB lower bound.

## Cycle 206

`HWB_(8m)` gives an exact selector-free all-order benchmark. At the midpoint of
any order, one of `[m,5m]` and `[3m,7m]` contains `m` prefix indices. Store an
arbitrary `m`-bit word there, pair each data bit with its complement to freeze
the prefix weight at `m` or `3m`, and use the suffix weight to select the
address. This embeds the exact `INDEX_m` matrix and forces width `2^m` in every
order. The direct quadratic-code transfer fails exactly: the order with
`u_1=0` first sends every `RM(2,n)` cross-splice into `RM(3,n)`, all easy above
the explicit cubic ANF threshold. Thus selector removal is possible in an
explicit polynomial-time family, but not by the natural Reed--Muller
easy-table splice construction. No MCSP or unrestricted lower bound follows.

## Cycle 182

Affine-plane slope partitions give an explicit `q(q-1)`-member order family
with seed at most `2 log q`: blocks from distinct slopes meet in one point, and
balanced block-prefix Venn cells have exact product size up to one `O(q)`
boundary block. This is a genuine cross-splice candidate for designated order
pairs, stronger and cleaner than invoking small bias for rectangle incidence.
It gives an exact designated-order theorem: equality has
`width >= 2^((q^2-1)/2)` in every nonzero-slope affine order, since the middle
cut splits `2 floor(q/2)(q-floor(q/2))` equality pairs. It does not imply
order-independent OBDD hardness: the paired variable order has width two, and
a selector for hidden matchings may itself be read first. Even exponential
OBDD hardness would remain restricted-model:
there is no reverse simulation to unrestricted circuits, RAMs, or the exact
MMW `search-MCSP^SAT` relation. No separation is claimed.

## Cycle 97

Gate elimination for one-sided average-case MCSP loses the easy-function
promise under truth-table patches; exact patch closure at fixed size is
impossible.  Compressed decision trees give only `Omega(n)` certificate bounds.
Easy-table-preserving circuit-generated restrictions can leave a full OR on all
live variables, defeating an unconditional switching lemma.  Constant-density
sample inconsistency has an enumerative `N^O(log log N)` circuit/SAT-oracle
upper bound, while tiny-density hardwired cylinders have `poly(n)` size.  The
required `N^.01` lower bound must charge global circuit fitting; all tested
local mechanisms were retired.

## Cycle 96

Oliveira--Santhanam average-case MCSP magnification is valid: a fixed-power
lower bound for formal zero-error average-case `MCSP[n^c]` against unrestricted
circuits implies `P!=NP`.  The formal solver must be decisive on `1-1/n` of
uniform truth tables, not merely one half.  Their proof constructs a one-sided
rejector with coverage `1-2^-n`.  Ruling out constant-density one-sided
rejectors is sufficient but not equivalent to ruling out arbitrary ternary
solvers.  Compressed MUX decision trees fit every short labeled sample, so local
query/restriction methods cannot charge the global circuit-fitting predicate.
The theorem is preserved, but the route is not promoted.

## Cycle 93

For permutation-invariant randomized query algorithms, hypergeometric
indistinguishability and infinite pigeonhole give an exact canonical boundary-
layer refuter, subject to boundary-index uniformity.  Deterministic and
uniformly enumerable small-random-support subclasses also admit constructive
adversarial completions.  For unrestricted algorithms the mean acceptance is
a degree-`q` polynomial and a convex combination of depth-`q` trees, but
thresholding, symmetrization, minimax, and known PTF generators do not select a
uniform error.  These restricted theorems do not satisfy CJSW; no separation is
claimed.

## Cycle 92

The CJSW GapMaj theorem is a valid full-reach constructive-separation target:
uniform `AC0` refuters against every `o(epsilon^-2)` randomized query algorithm
imply `P != NP`.  A three-bit exact counterexample defeats the proposed
pessimistic-estimator seed fixing: randomized coordinate sampling is pointwise
`2/3` correct, while every fixed coordinate has a promised error.  Query
hardness gives dense errors but no deterministic shallow selector.  The
seed-fixing mechanism was retired; no separation is claimed.

Bounded scout is queued to derive a memorization upper bound for fitting an
arbitrary proposed antichecker and compare its gate exponent with the target.
This is an adversarial test, not evidence from solver failure.

## Bounded scout tick 2

Any arbitrary labels on `h` distinct `N`-bit examples can be memorized by a
binary decision tree with at most `h-1` internal nodes. Multiplexer conversion
uses at most `3(h-1)+min(N,h-1)` De Morgan gates with shared input negations.
Hence an antichecker against size `N^2` circuits must have cardinality greater
than `(N^2-N)/3+1` under this convention. Subquadratic anticheckers are
decisively impossible; the route must target a superquadratic sample and still
needs a separate all-exponents amplification theorem.

## Bounded scout cycle 36

The `122` six-vertex coloring masks have an exact irredundant core of size
`90`.  Distinct masks are unlabeled partitions into at most three nonempty
color classes, and

`S(6,1)+S(6,2)+S(6,3)=1+31+90=122`.

Every proper three-block partition gives a complete tripartite graph whose
only proper three-color partition is that partition, up to color names.  Hence
any cover of all colorable graphs by coloring masks must contain all `S(6,3)=90`
proper three-block masks.  Conversely those masks cover every six-vertex
3-colorable graph, since a coloring using fewer than three colors can split a
color class.  Thus witness-mask deletion stops exactly at `90`; this is a
finite monotone-DNF obstruction and gives no unrestricted circuit lower bound.

## Bounded scout cycle 39

The mask-cover computation has an exact all-`n` form.  For every `n>=3`, any
cover of all labeled `n`-vertex 3-colorable graphs by coloring-partition masks
must contain every partition into exactly three nonempty blocks: the complete
tripartite graph associated with such a partition has no other proper
three-block coloring.  Conversely, every coloring with fewer than three
nonempty classes can be refined by splitting a class, so the three-block masks
cover the whole family.  The exact minimum is therefore

`S(n,3)=(3^n-3*2^n+3)/6`.

This generalizes `S(6,3)=90` and shows that the finite witness-mask DNF itself
has exponential irredundancy, without implying an unrestricted circuit lower
bound.

## Bounded scout cycle 41

The memorization obstruction extends quantitatively to every target size.  A
binary decision tree separating `h` distinct `N`-bit examples has at most
`h-1` internal nodes.  Implementing each node as
`(x and A) or ((not x) and B)` takes three binary De Morgan gates, with at most
`min(N,h-1)` shared input negations.  Hence every labeling is fit by a circuit
of size at most

`3(h-1)+min(N,h-1)`.

An antichecker against size `s` must satisfy
`3(h-1)+min(N,h-1)>s`; when `h>=N+1`, necessarily
`h>(s-N)/3+1`.  In particular, direct anticheckers for size `N^k` require
order-`N^k` samples.  This exact obstruction still gives no mechanism for
amplifying a fixed exponent into a superpolynomial lower bound.

## Bounded scout cycle 42

Integer inversion of the memorization bound is piecewise exact. In the regime
`h<=N+1`, an antichecker must satisfy `4(h-1)>s`, hence
`h>=floor(s/4)+2`. In the regime `h>=N+1`, it must satisfy
`3(h-1)+N>s`, hence `h>=floor((s-N)/3)+2`. For the quadratic target and
`N>=4`, this forces

`h>=floor((N^2-N)/3)+2`.

The threshold remains quadratic, so this exact rounding does not supply
all-exponents amplification.

## Bounded scout cycle 43

Cartesian padding cannot amplify empirical hardness. For any labeled sample
`A subset {0,1}^N`, let `c(A)` be the minimum binary De Morgan circuit size
fitting it, and define the cylinder `A^(up r)=A times {0,1}^r` with labels
independent of the new coordinates. Then

\[
c(A^{\uparrow r})=c(A),\qquad |A^{\uparrow r}|=2^r|A|.
\]

One inequality follows by ignoring the tag variables. For the other, restrict
any fitting circuit to one fixed tag and simplify constants, which cannot
increase gate count. Thus exponential sample replication, padding, or
irrelevant coordinates create no new circuit hardness. An all-exponents
amplifier must create genuinely new label dependencies. This does not prove a
quadratic antichecker, a lower bound, or `P!=NP`.

## Bounded scout cycle 50

A factor in a Boolean gadget composition is recoverable by restriction exactly
when the gadget has an attainable nonconstant unary section in that coordinate.
Iterating a fixed `r`-ary gadget on a depth-`d` tree gives

\[
c(T_d(A))\le r^d c(A)+s_{DM}(g){r^d-1\over r-1}.
\]

Since input length is `r^dN`, fixed-arity composition adds leaf fitting costs
and cannot increase a fixed hardness exponent. This is a black-box
amplification no-go, not a circuit lower bound or P-versus-NP result.

## Bounded scout cycle 46

Direct-product composition does not multiply fitting hardness. For labeled
samples `A_i` and a Boolean connective `g`, running fitting circuits on
disjoint blocks gives
`c(g(A_1,...,A_t))<=sum c(A_i)+s_DM(g)`. In particular,
`c(A xor B)<=c(A)+c(B)+4`. Restricting one factor shows only polarity-insensitive
preservation:

\[
\max(c_\pm(A),c_\pm(B))\le c(A\mathbin{\mathrm{xor}}B)
\le c(A)+c(B)+4.
\]

Thus the `t`-fold XOR product has multiplied sample cardinality but at most
`t c(A)+4(t-1)` fitting complexity. Black-box XOR/direct-product replication
cannot amplify one fixed circuit exponent to all exponents. This gives no
antichecker, lower bound, or P-versus-NP result.

## Bounded scout cycle 59

Any nonuniform gadget tree with `L` sample copies, total input length `M=LN`,
and total gadget complexity `S` obeys `c(T(A_N))<=L c(A_N)+S`. Growing arity
cannot amplify exponent `a` beyond `max(a,b)` when `S<=M^(b+o(1))`; the gadgets
must already import the larger hardness. This proves no circuit lower bound.

## Bounded scout cycle 63

For an acyclic composition DAG, substituting one fitting circuit per distinct
call node gives `c(B_D)<=S(D)+sum_u c(A_u)`. Free fanout and DAG sharing only
improve this bound. With direct external calls and maximum coordinate overlap
`Delta`, base exponent `a` becomes at most `a+log_M Delta`; subpolynomial
overlap cannot amplify it. Polynomially many heavily overlapping or nested
 calls remain the only black-box escape and would require a new direct-sum lower
 bound robust to cross-instance sharing. No P-versus-NP result follows.

## Main funnel cycles 75--76

McKay--Murray--Williams supplies a full-target implication. For
`s(n)=2^(n/log^* n)`, proving that exact `search-MCSP^SAT[s]` has no
deterministic one-pass solver with both `N^epsilon` space and `N^epsilon`
update time for one fixed `epsilon>0` implies `P!=NP`. This corrects the prior
all-exponents diagnosis, which belonged only to the antichecker funnel.

Ordinary continuation signatures cannot reach the threshold. At any stream
cut, their number is at most the number of size-`s` circuit functions plus one,
giving only `O(s log(n+s))=N^o(1)` bits. Emitted output must also be charged,
and pure fixed-power space lower bounds are false with unbounded update time.
The promoted bottleneck is an update-time-sensitive, non-localizable lower
bound for one exact `Stream-Merge` operation. The current canonical circuit
already summarizes every preceding block, so there is no independent
many-block consistency burden. No lower bound or separation is claimed.

## Main funnel cycle 77

Quantifier normalization confirms that canonical merge is a higher-PH local
optimization predicate, but supplies no bounded-update lower bound. The block
process is Markovian; proof-complexity needs a missing correctness-to-proof
compiler; and pseudorandom anticheckers presuppose nonempty error sets. More
decisively, canonical merge belongs to the MMW upper-bound construction, while
the magnification hypothesis attacks relational search-MCSP, whose solver may
emit any witness. Hardness of the canonicalized problem does not transfer. The
Stream-Merge tactic is retired. No separation is claimed.

## Main candidate cycle 87

Oliveira--Santhanam time--space magnification gives full reach for adjacency-
matrix `k`-Vertex-Cover at fixed `k(n)=2^sqrt(log n)`: an `m^(1+epsilon)` time,
`m^o(1)` space lower bound implies `P!=NP`. Buss kernelization explains both the
implication and the barrier. The full matrix reduces to an `m^o(1)`-bit kernel,
so generic probes/local oracles collapse; the proof must charge computation on
that kernel. The route is eligible as a full-reach target but has no promoted
lower-bound mechanism yet. No separation is claimed.

## Main-funnel cycle 88

Post-Buss self-reduction costs only `k+O(log k)` calls, an `m^o(1)` multiplier,
and does not force adaptivity on arbitrary RAMs. The complete kernel fits in the
allowed workspace, defeating query, hidden-location, communication, and
read-limited extraction. Restricted branching-program/proof lower bounds lack a
reverse simulation; syntax-sensitive extractors also fail a junk-computation
robustness test. Standard SAT reductions have fatal adjacency-matrix and
parameter blowups. The proof mechanism is retired while the magnification
implication remains valid. No separation is claimed.

## Bounded scout cycle 209

Prefix-constrained MCSP is the exact completion predicate
`min_(f extends rho) C(f)<=s`. A complete padded table cannot simply contain a
chosen completion, because choosing it is the search being reduced. Literal
tagged slices have the wrong quantifier: restriction gives a maximum over slice
complexities, not the existential minimum. More strongly, distinct completions
of one balanced prefix can share essentially their full cost. For
`A={x_1=0}` and `f_i=H XOR (x_1 AND x_(i+1))`, all `f_i` agree on `A` and each
has complexity at least `C(H)-2`, while the tagged table is
`H XOR (x_1 AND x_(sel(a)+1))` and has size `C(H)+O(t)`. Thus repetition and easy
truth-table tags do not provide additive resource isolation. This refutes the
padding/tagging construction, not every possible many-one reduction; the
missing ingredient remains an unrestricted-circuit anti-sharing theorem. No
MCSP lower bound or separation is claimed.
