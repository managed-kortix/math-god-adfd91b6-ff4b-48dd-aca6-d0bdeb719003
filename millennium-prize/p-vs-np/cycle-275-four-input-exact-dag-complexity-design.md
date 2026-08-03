# Cycle 275: exact four-input DAG-complexity design

## Scope and frozen model

Let `F` be the set of all `2^16=65536` Boolean functions on four inputs.  The
source functions are

\[
 S_0=\{0,1,x_1,x_2,x_3,x_4\}.
\]

The counted gates are fan-in-two `AND` and `XOR` and fan-in-one `NOT`, with
free fanout and free source constants.  In this model `NOT(u)` and `XOR(u,1)`
are interchangeable at the same cost.  Thus an exact search may use only
`AND` and `XOR`, provided the constant-one source remains available.

## The exact finite state

A state after `r` gates is the set

\[
 S=S_0\mathbin\cup\{g_1,\ldots,g_r\}\subseteq F
\]

of all source and gate-output truth tables simultaneously available.  Its
successors are

\[
 S\cup\{u\mathbin{\operatorname{AND}}v\},\qquad
 S\cup\{u\mathbin{\operatorname{XOR}}v\}\quad (u,v\in S),
\]

when the added function is not already in `S`.  Equivalently one may retain
`NOT` as a third transition.  Free fanout is exactly what makes the available
set sufficient: every future gate depends only on which functions are
simultaneously available, not on how often they are used or on the wiring that
produced them.

This state retains the information lost by a one-number-per-function closure.
That closure proves a formula recurrence because it combines independently
optimal realizations and charges their common subcircuits twice.  Two prefixes
having the same cheapest individual functions but different simultaneously
available sets can have different continuation costs.

No minimum circuit needs two gates with the same truth table.  If a later gate
duplicates an earlier output, redirect all of its fanouts to the earlier gate
and delete it.  Hence a depth-`r` reduced state has exactly `6+r` functions,
and it can be stored canonically as the sorted `r` non-source 16-bit words.
Breadth-first search on these states is exact: the first layer containing `f`
is `C_B(f)`.

The finite state space is nevertheless enormous.  A coarse ambient bound is
`2^65530` states (or `sum_{j<=r} binom(65530,j)` through depth `r`).  Reachability
and canonicalization reduce this greatly, but they do not provide a useful
worst-case bound.  A global available-set BFS is therefore an exact
specification and a useful small-depth cross-check, not the recommended
proof-producing computation.

## Certified exact synthesis

For a target `f` and gate bound `k`, form an acyclic straight-line-program SAT
instance `E(f,k)`:

1. Sources `0,1,x_1,...,x_4` have their fixed sixteen-bit columns.
2. Gate `i` selects two predecessors from the sources and gates `0,...,i-1`
   and selects `AND` or `XOR`.
3. Sixteen semantic variables for each gate enforce the selected operation on
   every input assignment.
4. An output selector chooses a source or one of the `k` gates and is constrained
   to equal the sixteen bits of `f`.

The output selector makes this an *at-most* `k` encoding; unused gates are
allowed.  Consequently `E(f,k)` is satisfiable exactly when `C_B(f)<=k`.
Selected predecessors preserve arbitrary DAG sharing, so this is not a formula
encoding.

For each non-source `f` of claimed complexity `c`, retain:

- a concrete satisfying assignment for `E(f,c)`, decoded as a circuit; and
- an LRAT (or equivalently checkable) refutation of `E(f,c-1)`.

A small independent checker evaluates every witness on all sixteen inputs and
checks every LRAT proof against a deterministically generated CNF.  A manifest
must bind the encoder version, variable map, target ordering, certificates,
and hashes.  These two checks prove `C_B(f)=c`; no trust in the optimizing SAT
solver is required.

There is a uniform finite cap much better than the earlier minterm bound.
Compute the six quadratic, four cubic, and one quartic ANF monomials using
eleven `AND` gates, then XOR the selected terms among the constant, four linear
terms, and eleven nonlinear terms using at most fifteen `XOR` gates.  Therefore

\[
 C_B(f)\le 26
\]

for every four-input function.  Only bounds `0,...,26` need occur.

Input-variable permutations preserve this exact gate count.  Burnside's lemma
gives

\[
 \frac{2^{16}+6\,2^{12}+3\,2^{10}+8\,2^8+6\,2^6}{24}=3984
\]

orbits of four-input truth tables under `S_4`.  It is therefore enough to
certify 3984 canonical representatives and have the checker expand each orbit.
Output complementation and affine changes of input variables are not free
symmetries in this counted model and must not be used to reduce the census.

The resulting SAT instances have at most 26 gates and only sixteen semantic
rows.  A 3984-representative SAT/LRAT campaign is technically feasible on
ordinary finite compute, subject to measured proof-log storage and a frozen
resource manifest.  This is a feasibility conclusion, not a completed census:
no complexity value or threshold property is certified until all witnesses,
refutations, and checker runs exist.  The available-set BFS, by contrast, is
not presently justified as feasible to completion.

## Relation to the sole packet

The exact complexity census is the missing computational payload needed to
evaluate every entry of the threshold matrices in the four-input `INDEX_2`
packet.  Once the census exists, checking every one of the `binom(16,8)=12870`
balanced cuts, every relevant threshold, and all column pairs is a separate
small exhaustive step that should also emit a checkable witness or a complete
negative certificate.

It is not, however, the first missing item for admission of that packet as a
Millennium re-entry packet.  The packet currently gives a finite restricted
OBDD/MCSP target but no implication from that target to a quantified part of
the official `P` versus `NP` statement.  This is item 2 of the frozen
`C275-ONE-PACKET-ADMISSION` requirements and precedes the absent census.  The
census would settle the bounded threshold question only; it would not supply
the unrestricted-circuit anti-sharing theorem or an official transfer.

`C275-WALL: the first admission item missing from the sole packet is an
explicit valid implication to a quantified part of the official P-versus-NP
statement.  The exact four-input DAG-complexity census is also absent and is
the first computational payload for the packet's finite INDEX_2 test, but
producing it cannot repair the earlier official-transfer wall.`

No finite four-input census, OBDD lower bound, or packet audit resolves
`P` versus `NP`.
