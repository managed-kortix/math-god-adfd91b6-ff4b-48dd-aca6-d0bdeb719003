# Cycle 182: random-order exact OBDD assessment

## Model that can be claimed

Let `N=2^n`, let `MCSP[s]` be the Boolean predicate that accepts exactly the
`N`-bit truth tables computed by circuits of size at most `s`, and let `pi` be a
permutation of the `N` truth-table coordinates. A `pi`-OBDD is a deterministic
layered branching program which queries every coordinate at most once and only
in the order `pi`. The precise bounded statement under assessment is of the
form

\[
 \Pr_{\pi}\left[\operatorname{size}_{\pi\text{-OBDD}}
       (\operatorname{MCSP}[s])\ge L(N,s)\right]\ge 1-\delta(N).
\]

The diagram may depend nonuniformly on `pi`, but it must be correct on every
truth table. This is stronger than proving that one fixed diagram succeeds on
average over `(pi,T)`, and weaker than a lower bound for every variable order.
These quantifiers must accompany any theorem statement.

If the proved quantity is width `W`, an exact one-pass decision streamer in
that fixed order needs at least `log_2 W` bits of state. If only total OBDD size
`L` is lower-bounded, the corresponding conclusion is only

\[
 S\ge \log_2 L-\log_2(N+1),
\]

because an `S`-bit one-pass streamer unfolds into a layered OBDD of size at
most `(N+1)2^S`. This simulation charges neither the complexity nor the time
of a transition. It also presumes that the order is fixed (or conditioned on)
and that stream addresses and any oracle state are accounted for. An
average-order algorithm allowed error needs a distributional lower bound with
matching order/input quantifiers; exact OBDD hardness alone is not that result.

## What the lower bound adds

Cycle 159 proved only

\[
 D(\operatorname{MCSP}[s])\ge N-O(s\log(n+s)).
\]

Decision-tree depth says that an exact algorithm cannot stop early on a
suitable input. It does not prevent all transcripts at a level from merging:
`OR`, for example, has full deterministic depth on one input but a linear-size
OBDD. A superpolynomial or exponential random-order OBDD lower bound would
therefore be a genuine strengthening. It would certify that, for most fixed
orders, exact one-pass evaluation must retain many semantically different
residual MCSP predicates, not merely inspect almost all coordinates.

The standard interpretation is one-way communication. Cutting a width-`W`
`pi`-OBDD after a prefix gives a deterministic one-way protocol of cost
`ceil(log_2 W)` for the induced prefix/suffix partition. Thus the result is a
random-partition deterministic one-way communication lower bound and, after
the simulation above, a fixed-order exact streaming-space lower bound.

## Branching-program boundary

An OBDD is an oblivious read-once branching program. The theorem does not by
itself lower-bound any of the following stronger models:

- the best-order OBDD, unless the theorem holds for every `pi`;
- a free/read-once branching program whose next queried variable depends on
  the preceding answers;
- a branching program that rereads variables;
- a random-access RAM, even one with small workspace;
- randomized or bounded-error branching programs.

In particular, a lower bound for most orders allows an exceptional structured
order. Adaptive variable order can also evade every fixed partition used in
the proof. The exact RAM-to-branching-program simulation from Cycle 159 goes
in the other direction: an `S`-space, `T`-time random-access computation gives
a length-`T`, width-`2^{O(S+\log T)}` layered branching program, not an OBDD.
An OBDD lower bound therefore cannot be applied to that simulation without a
new resource-preserving oblivious read-once normalization theorem. Such a
normalization is false in general and would itself be the substantive bridge.

## Magnification audit

The McKay--Murray--Williams hypothesis concerns exact relational
`search-MCSP^SAT[s]` at

\[
 s(n)=2^{n/\log^* n},
\]

and rules out a deterministic one-pass solver having both `N^epsilon` space
and `N^epsilon` per-item update time for one fixed `epsilon>0`. A random-order
exact OBDD lower bound for Boolean decision `MCSP[s]` does not instantiate this
hypothesis:

1. decision MCSP is not the MMW search relation, whose solver may output any
   valid witness;
2. a random-order statement does not cover the stream/order model in the MMW
   premise without a quantifier-preserving reduction;
3. OBDD width charges state but not update time or SAT-oracle access;
4. an OBDD size bound may yield only `log L-log N` space bits;
5. no implication converts restricted OBDD hardness into an unrestricted
   circuit lower bound.

Even a bound `L=2^{N^{Omega(1)}}` would consequently be an unconditional and
potentially strong restricted-model theorem, not a proof of `P != NP`. It
would become a magnification input only after an independent theorem maps every
MMW relational solver to the hard random-order OBDD model while preserving
exactness, witnesses, SAT-oracle access, space, and per-item update time. No
such bridge is presently supplied.

## Novelty calibration

Subfunction counting, prefix/suffix communication, and the conversion between
fixed-order one-pass state and OBDD width are standard OBDD techniques. The
Cycle 159 easy-set cardinality argument alone does not give an OBDD size lower
bound, because query depth and residual-function count are different. A proof
that merely repackages a known subfunction-counting lemma is therefore not a
new method.

The potentially new content would be MCSP-specific: proving that for most
truth-table coordinate orders there are `L(N,s)` inequivalent residual
predicates, with explicit parameters and without assuming an unproved circuit
lower bound for an explicit function. Randomly splicing two easy truth tables
can produce a counting-hard table, but turning this observation into many
pairwise distinct OBDD states requires a simultaneous cross-splice argument;
single-pair hardness gives only two states. Any claimed exponential bound must
make that packing step and all union-bound ranges explicit.

No definitive novelty claim is made here. It requires a primary-source search
covering OBDD/subfunction lower bounds for MCSP and circuit-minimization
problems, random variable order, random-partition communication complexity, and
exact streaming MCSP. Until that audit is completed, the appropriate label is
`candidate new restricted-model theorem`, not `new complexity separation`.

## Assessment of the Cycle 182 constructions

The affine-plane construction in
`cycle-182-explicit-cross-splice-obdd.md` proves an exponential exact OBDD
width lower bound for equality on a designated `q(q-1)`-element family of
orders. The split-pair count is sound and gives width at least
`2^((q^2-1)/2)`. It is not, as presently stated, a random-uniform-order theorem
and not an MCSP theorem. Equality has width two in the paired order, so the
construction proves neither best-order OBDD hardness nor hardness against a
branching program that chooses its order. The ingredients--equality residuals,
split-pair counting, and affine-plane transversality--are standard. Without a
literature audit, the safest novelty description is an explicit illustrative
combination, not a new lower-bound paradigm.

The MCSP splice-packing argument in
`cycle-182-random-order-mcsp-packing-audit.md` is closer to the proposed scout.
For exact decision MCSP, a hard cross-splice separates two easy prefixes, and a
simultaneous packing can force midpoint width at least `|C|` for an appropriate
permutation, or for most permutations when the quantitative union bound is
strong enough. The conditioning is essential: a splice of two tables at
distance `d`, with `k` disagreements in the prefix, is supported on only
`binom(d,k)` tables. It is not uniform over `2^N` tables, and balance by itself
does not imply hardness.

At the MMW parameter, this mechanism has an intrinsic ceiling

\[
 \log_2|C|\leq \log_2|E_{n,s}|=O(s\log(n+s))=N^{o(1)}.
\]

It can therefore force at most `N^{o(1)}` state bits from a packing of easy
tables. That is potentially a valid bounded random-order exact-decision OBDD
theorem, but it cannot exclude `N^epsilon` space for any fixed `epsilon>0` and
cannot trigger MMW magnification. Constant per-input success over random orders
also cannot replace exact correctness on all pair-dependent splices without a
new distributional argument.

## Verdict

A valid random-order exact MCSP OBDD lower bound would improve the Cycle 159
near-linear query result by proving a memory/state-merging obstruction for most
fixed orders. The current equality construction is an exact designated-order
benchmark; the MCSP packing supplies a conditional bounded route with only
`N^{o(1)}` possible forced space at the target parameter. Immediate
consequences remain confined to exact deterministic OBDDs, deterministic
one-way protocols for the corresponding partitions, and properly matched
fixed-order one-pass decision streamers. Neither construction lower-bounds
general branching programs or random-access computation, meets the MMW
relational time--space hypothesis, or implies `P != NP`.
