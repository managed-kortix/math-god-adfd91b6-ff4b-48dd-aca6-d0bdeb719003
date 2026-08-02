# Exact baseline experiments

Commands (Python 3 and Node.js 18+):

```sh
python3 test_verifiers.py
python3 exhaustive_crosscheck.py --max-n 5
python3 verify_set.py certificate.txt
node verify_matrix.js certificate.txt
~/mathenv/bin/python direct_smt.py --n 17 --b-size 6 --timeout-ms 300000
~/mathenv/bin/python direct_smt.py --n 18 --b-size 6 --missing 3 --minimality --timeout-ms 900000
```

Exit status is 0 only for a valid counterexample, 1 for a valid oriented graph
which is not a counterexample, and 2 for malformed input. `verify_set.py` uses
adjacency sets; `verify_matrix.js` has an independent parser and directly scans
a Boolean matrix. The exhaustive oracle compares every neighborhood set, not
only the final decision. Exhaustion is a regression test and is not claimed as
progress toward proving the universal conjecture.

`direct_smt.py` is a baseline exact SMT search. It fixes a minimum-degree-eight
root with six or seven exact second neighbors and imposes deficit exactly one or
two at every vertex. A `sat` adjacency projection is not trusted until both
external verifiers pass. An `unknown` result has no mathematical force, and an
`unsat` result is not a proof artifact unless independently certified.

`--minimality` adds proved necessary conditions for a globally vertex-minimal,
then arc-minimal counterexample: every vertex has a tight in-neighbor witness,
and every present arc satisfies the exact gain/lost-second-endpoint deletion
inequality. These are not part of an unrestricted fixed-order model.

`snc_cnf.py` is an initial deterministic plain-CNF implementation using full
Tseitin equivalences and exact bidirectional unary counters. It is provisional
until its auxiliary semantics are exhaustively tested against the independent
small-graph oracles. Solver output is not a certificate before that gate and an
independent DRAT/LRAT check both pass.

Semantic regression commands now include:

```sh
python3 test_cnf_semantics.py
```

This exhaustively checks every threshold output through width eight and every
exact-second membership bit for all 760 labelled oriented graphs through order
four. It does not yet validate theorem-specific rooted/minimality clauses or
replace an independent proof checker.

The optional `--robust-witness` mode adds the exact necessary vertex-minimality
condition that every deleted vertex has a selected deficit-one in-neighbor and
that none of the witness's old exact second neighbors loses all two-walks after
the deletion. This mode has been clause-audited, but its selector and deficit
families still require dedicated exhaustive semantic tests before certificate
use. Those tests now cover exact `mu2` linkage through width eight and 3,003
graph/deletion witness cases through order four.

Order-18 normal-form options include `--high` for the exact comma-separated
degree-nine labels and `--force-witness w,u` for a distinguished robust
selector. An empty `--high ''` means every vertex has degree eight. These are
shard constraints, not consequences valid at arbitrary order.

`--arc-minimal` adds the exact gain/lost-endpoint condition for deletion of
every present arc, with no additional variables. Exhaustive mutation testing
compares 7,860 small graph/arc cases directly against recomputation after arc
deletion.

`m8_rows.py` deterministically enumerates the 762 corrected coarse C-margin
rows. `m8_pilot_shard.py` emits one genuine sixth-row terminal leaf. Its
compressed CNF/LRAT, logs, hashes, and manifest are committed as the first
end-to-end independently checked certificate. It proves only that one leaf is
UNSAT, not that the sixth row or the `m=8` branch is eliminated.

`m8_rho5_leaves.py` emits the 735 canonical colored missing-graph/C-to-B
orientation leaves under all 36 `rho=5` rows and hashes their deterministic
stream. This is the production cover generator; an independent labelled-orbit
checker remains required before the cover gate closes.

`check_m8_rho5_cover.py` is that independent checker. It separately enumerates
all ordered pairs of labelled seven-bit masks for the A and B subset systems,
computes orbit multiplicities, audits 63,517,608 labelled configurations, and
reproduces the production cover hash without importing production cover code.

`m8_rho5_shard.py --index I` reconstructs and emits the exact CNF for canonical
leaf `I` in that cover. Leaf 0 has also completed the LRAT pipeline during
development; bulk artifacts are not committed until the independent cover
checker and completion ledger are in place.

`m8_rho5_groups.py` and `m8_rho5_group_shard.py` form the audited 136-margin
grouping: intersection parameters remain existential while all six margins and
the C state remain exact. `check_m8_rho5_groups.py` independently verifies the
weighted partition back to all 735 leaves and 63,517,608 labelled objects.

The frozen `m=6` support census consists of all 68 unlabeled isolate-free simple
graphs with six edges. Regenerate and audit its deterministic ASCII graph6
payload with no third-party Python packages:

```sh
python3 m6_support_census.py --output m6-support-census.txt
python3 m6_support_census.py --check m6-support-census.txt
python3 check_m6_support_census.py m6-support-census.txt
python3 test_m6_support_census.py
```

The frozen payload is 934 bytes with SHA-256
`e97de806f6db6c3ac1768cab9259f7f0cd1c91ee26d949c1a3455ef8e471c8be`; both
programs assert that value and the order distribution `1,5,15,20,15,7,3,1,1`
for orders 4 through 12.

The producer uses one-edge canonical augmentation and permutes vertices only
inside connected components of order at most seven. The checker instead uses
arbitrary-neighborhood vertex augmentation and a degree-constrained explicit
isomorphism search before independently reconstructing the payload. Neither
program scans the roughly 90 million labelled six-edge subsets on 12 vertices.

The rooted-cell placement cover decodes that frozen support payload and colors
every support vertex in `R,A,B,C`, with capacities `B6=(1,8,6,3)` and
`B7=(1,8,7,2)`. The only forbidden support edge is `R-A`. Rows are canonical
under the full automorphism group of the uncolored support, and each row records
its raw-coloring orbit size.

```sh
python3 m6_placement_cover.py --output m6-placement-cover.txt
python3 m6_placement_cover.py --check m6-placement-cover.txt
python3 check_m6_placement_cover.py m6-placement-cover.txt
python3 test_m6_placement_cover.py
```

The deterministic payload has 187,324 rows (112,220 B6 and 75,104 B7), is
6,659,672 bytes, and has SHA-256
`22d7744f1eecee3ea22527e4beec645ae999c912184f1f23c1a7f701e966ed5e`.
The independent checker does not import the producer: it reconstructs each full
support automorphism group by degree-constrained backtracking, validates every
canonical representative and orbit size, and separately counts all valid raw
colorings. Orbit weights sum to 1,862,693 B6 and 1,022,346 B7 raw colorings.
This is a placement cover only; it does not orient present pairs, emit CNFs, or
eliminate either branch.

The placement-only filter reads `m6-placement-cover.txt` without regenerating or
relabeling it and assigns every row one deterministic status. Run it and its
materially independent checker with:

```sh
python3 m6_placement_filter.py --output m6-placement-filter.txt
python3 m6_placement_filter.py --check m6-placement-filter.txt
python3 check_m6_placement_filter.py m6-placement-filter.txt
python3 test_m6_placement_filter.py
```

Write `h_X(v)` for the number of six missing pairs from `v` to cell `X`, and
write `H_XY` for the corresponding cell-pair total. Cell sizes are
`(r,a,b,c)=(1,8,6,3)` in B6 and `(1,8,7,2)` in B7. The filter applies only these
necessary predicates, in the displayed order (the ledger records the first
failure):

1. Every `v in B` has a present pair to A: `h_A(v)<8`.
2. Every `v in A` has at least eight possible outgoing pairs in `A union B`:
   `(7+b)-h_A(v)-h_B(v)>=8`.
3. For every actual `v in C`, including C vertices isolated from the six-hole
   support, put `f_v=9-h_R(v)-h_A(v)` and
   `q_v=b+c-1-h_B(v)-h_C(v)`. The locally possible degree interval meets
   `{8,9}` exactly when `f_v<=9` and `f_v+q_v>=8`.
4. In B6, `H_RC+H_AC+H_CC>=3`.
5. The exact C feasibility check uses all `c` actual C vertices, orients every
   present C-C pair (and no missing C-C pair), then asks for targets
   `d_v in {8,9}`, with at most three C targets equal to nine, such that
   `f_v+out_CC(v)<=d_v<=f_v+out_CC(v)+b-h_B(v)` for every `v in C`.

The last check is a tiny finite DP over present C-C pairs in the producer. The
checker instead materializes the full 18-vertex coloring, tests pair presence,
and directly enumerates directions and targets. The bound of three degree-nine
C vertices follows from `C(18,2)-6=147=15*8+3*9`. C-B choices are independent
once their C endpoint is fixed, so the interval condition is exact. The ledger packs each reason code
into three bits in frozen zero-based row order, then base64-encodes that keyed
status stream. The checker requires exactly one valid status per cover row and
checks a disjoint exhaustive partition without duplicating the 6.6 MB cover.
The deterministic ledger is 95,083 bytes with SHA-256
`9bfd2fadda610dde6cef7c13956edba6b0fa763e2ffc31226c0ddf1323fd1d0c`.

These are necessary placement predicates only. They do not orient A-A, A-B,
B-B, or all C incident pairs simultaneously with non-C degrees, do not encode
badness or minimality, and do not eliminate either branch.

`m6_parent_cnf.py` turns exactly one accepted frozen row into a standalone full
order-18 parent CNF. It hard-checks both frozen input hashes and headers, accepts
either the zero-based ordinal among the 76,361 accepted rows or the original
zero-based cover index, and rejects a cover-index selector whose filter status
is nonzero. For each cell it embeds support vertices in support-label order onto
the first available full-graph labels. Thus B6 uses
`R=0,A=1..8,B=9..14,C=15..17`, while B7 uses
`R=0,A=1..8,B=9..15,C=16..17`.

```sh
python3 m6_parent_cnf.py --accepted-ordinal 0 --output /tmp/m6-a0.cnf
python3 m6_parent_cnf.py --cover-index 17 --output /tmp/m6-row17.cnf
python3 check_m6_parent_cnf.py /tmp/m6-a0.cnf
python3 test_m6_parent_cnf.py
```

The emitter calls the complete
`generate(18,bsize,6,robust_witness=True,arc_minimal=True)` model and refuses to
write unless its exact ordered variable map and base clause stream match the
frozen branch fingerprints. The canonical hash serialization is one
`<number> <name>\n` record per variable and one ordinary DIMACS clause line per
base clause. Both branches have 23,616 variables and variable-map SHA-256
`cff4c18a4425f26c188790871da51a58b13569764bf89c83d1c736d5f9db070e`.
B6 has 142,736 base clauses with SHA-256
`22b118674d05045d0a1c8628ccb5b9a7f72fbcd53f6086ecab1b2ab369ca12c1`;
B7 has 142,729 with SHA-256
`a21d68c9a70642ad15b836d162996779d0b4ee4590a7bccd7f3af54f394341ab`.
The historical stream contains two harmless duplicate base clauses in each
branch: units `-1` (`a_0_0`) and `-325` (`q_0_0`) each occur twice. They remain
part of the frozen stream because existing certified campaigns depend on the
exact clauses in `snc_cnf.py`.

After that base, the emitter appends exactly one unit for every one of the 153
unordered-pair hole variables in graph6 pair order
`(0,1),(0,2),(1,2),...,(16,17)`: six positive units for the embedded support
and 147 negative units. Comments record the frozen hashes, both selectors,
branch, support identity, placement, embedding, holes, and model options before
the exact variable map and DIMACS body.

`check_m6_parent_cnf.py` is a hostile-input CNF parser and projection checker.
It separately parses the cover and filter bitstream, strictly parses short-form
graph6 including length and padding, reconstructs the selected frozen branch,
and authenticates both branch hashes plus exact ordered equality of the base
variable map and clause stream. Variable declarations must be unique names
numbered consecutively from 1 through N; metadata must have the canonical order
and exact key set; and no comment is allowed after the DIMACS header. The only
permitted suffix is the exact 153-unit pair-ordered projection.
The regression generates only five large boundary CNFs (accepted ordinal zero,
accepted row 17, last B6, first B7, and final accepted row); direct helper checks
cover all 76,361 accepted embeddings, all 68 support types, and all observed
cell occupancies without generating 76,361 roughly 10 MB files.

This parent layer does not solve any CNF, produce or check a proof, prove that an
accepted placement has an orientation completion, or eliminate B6/B7. The
checker validates exact generator identity and projection but does not establish
the mathematical semantics of each base clause; those semantics retain their
separate small-instance regression and eventual proof-checking requirements.

After the human elimination of forced B7 `q=0`, the selector-grouped residual is
frozen by `m6-forced-selector-groups.tsv`: nine `(branch,q,h)` groups cover all
31,568 remaining forced rows (B6 `q=0..3`, B7 `q=1..5`). Reproduce one group and
run the independent gate with:

```sh
python3 m6_forced_group_cnf.py --group B7-q5 --output /tmp/m6-B7-q5.cnf
python3 check_m6_forced_group_cnf.py /tmp/m6-B7-q5.cnf
python3 test_m6_forced_group_cnf.py
```

The manifest and each CNF bind the excluded B7 `q=0` cell to
`attempts/tick51-b7-q0-human-proof.md` by its exact 3,055 bytes and SHA-256.
Each CNF is the exact branch base, the common forced orientation/high-C units,
fresh selectors beginning at 23,617, one selector ALO, and 153 ordered guarded
hole clauses per member. After existentially quantifying the fresh selectors,
the grouped CNF is equisatisfiable with the disjunction of its member CNFs; it
is not logically equivalent over the enlarged variable set. The checker
independently derives the residual rows, asserts every member projection is
unique in every group, reconstructs every clause, and freezes all nine file
hashes. `--model` requires a complete assignment of every CNF variable,
evaluates every clause, requires exactly one true selector, and only then
attributes the model.

All nine groups are now CaDiCaL-UNSAT and independently LRAT-verified. The
durable `xz -3` proofs are `../certificates/m6-forced-*.lrat.xz`; exact CNF,
LRAT, and compressed identities plus Python `time.monotonic` stage timings are
in `m6-forced-group-certificates.tsv`. Fresh verification regenerates and
structurally checks every CNF, decompresses and authenticates every LRAT, and
runs the pinned checker:

```sh
python3 verify_m6_forced_group_certificates.py \
  --checker /path/to/pinned/lrat-check
```

The remaining exact `m=6` parent frontier is frozen independently in
`m6-residual-selector-groups.tsv`. It has 23 `(branch,lambda,r,t)` groups and
80,974 parent/group memberships, with authoritative branch subtotals B6=19,911
and B7=61,063. A parent can occur in more than one group
when its pointwise C states permit more than one exact `(r,t)` pair. The only
excluded regimes are B6 `lambda=3` and B7 `lambda=1`; the manifest and every
CNF bind those exclusions to the committed forced selector manifest,
certificate ledger, and fresh verifier by exact byte count and SHA-256.

```sh
python3 m6_residual_group_cnf.py --group B7-l6-r5-t2 \
  --output /tmp/m6-B7-l6-r5-t2.cnf
python3 check_m6_residual_group_cnf.py /tmp/m6-B7-l6-r5-t2.cnf
python3 test_m6_residual_group_cnf.py
```

The producer derives feasible `r=e(C,B)` and `t=highC` from exact pointwise C
states, adds deterministic unary exact-cardinality counters for both values,
then adds fresh selectors, one ALO clause, and 153 pair-ordered guarded hole
clauses per member. The checker separately enumerates internal-C orientations
and each C vertex's degree-eight/nine target, reconstructs every counter and
clause, and requires a complete satisfying model with exactly one true
selector before attribution. The regression actually emits, independently
reconstructs, checks, and hashes every one of the 23 CNFs. The 3,915-byte
manifest SHA-256 is
`b55f0b8e69a77b64254285b9134262cedb961e18a13ad10e4ce350bd04caa85a`.
This layer freezes all 23 CNFs. Four complete groups now also have retained,
freshly replayable LRAT certificates: `B6-l4-r0-t2`, `B6-l4-r1-t3`,
`B6-l5-r2-t3`, and `B7-l6-r3-t0`, totaling 15,310 memberships. Exact hashes
and tool identities are in `m6-residual-group-certificates.tsv`; verify them via

```sh
python3 verify_m6_residual_group_certificates.py \
  --checker /path/to/pinned/lrat-check
```

No UNSAT claim is made for the other 19 groups.

The rooted clean-sink theorem is a separate post-processing theorem over the
frozen 23-group membership universe; it does not modify those campaign files or
claim group UNSAT. A high C vertex with zero internal-C outdegree and zero
`C->B` outdegree must dominate `R union A`. Its exact second neighborhood is B,
and deleting its arc to the root leaves a counterexample, contradicting arc
minimality. The proof and its hypotheses are recorded in
`../attempts/tick52-rooted-clean-sink-theorem.md`.

For every membership `(parent,r,t)`, the producer enumerates all present
internal-C orientations and all compatible pointwise C degree targets. It
eliminates the membership only if every realization contains such a clean sink.
The independent checker reconstructs the 80,974-membership universe directly
from the frozen placement cover and filter and reimplements that exhaustive
predicate without importing the producer or residual-group producer.

```sh
python3 m6_clean_sink_manifest.py --check
python3 check_m6_clean_sink_manifest.py
python3 test_m6_clean_sink_manifest.py
```

The exact partition is 34,810 eliminated memberships and 46,164 remaining
memberships. These correspond to 17,084 and 18,862 distinct parents,
respectively, with no mixed parent; memberships must not be relabeled as
parents. Branch membership counts are B6 `11,072/8,839` and B7
`23,738/37,325` (eliminated/remaining). The count table, including every one of
the 23 groups, is frozen in `m6-clean-sink-manifest.tsv`. The exact streams are:

```
m6-clean-sink-eliminated.tsv  1,705,845 bytes  df4cbe415253944712011bf1fb46898925f6a63a087081bef2bbaf2e11f153b6
m6-clean-sink-remaining.tsv   2,262,190 bytes  416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642
m6-clean-sink-manifest.tsv        2,104 bytes  733e06c8aa9881e0006409efff23729f1bf88d8af7b1a70e8a78fd3775b53217
```

Mutation tests reject changed counts, disposition headers, truncation,
cross-group movement, duplicate membership rows, and changes to either the
source 23-group manifest or theorem report identity. A synthetic mixed-state
fixture separately checks that the disposition predicate is universal over all
pointwise realizations, not existential.

The clean-sink remaining stream has the stronger verified property that no
parent is mixed between dispositions. Consequently its 46,164 memberships
project exactly to 18,862 unique remaining parents and can be grouped only by
`(branch,lambda)`, with parent counts B6 `l4=2470,l5=1024,l6=220` and B7
`l2=8119,l3=5016,l4=1649,l5=322,l6=42`. The exact eight-group manifest is
`m6-clean-sink-selector-groups.tsv` (1,838 bytes, SHA-256
`6e7eee0ddd5b4c7ef02cdf459c9a0647f720513e7ee4987a3a8b0c17af37eeda`).

```sh
python3 m6_clean_sink_group_cnf.py --group B7-l6 \
  --output /tmp/m6-clean-B7-l6.cnf
python3 check_m6_clean_sink_group_cnf.py /tmp/m6-clean-B7-l6.cnf
python3 test_m6_clean_sink_group_cnf.py
```

Each CNF is exactly the immutable branch base, one fresh selector per unique
parent, one selector ALO, and 153 pair-ordered guarded hole clauses per parent.
There are no `r`, `highC`, or other counter variables or clauses: every retained
parent selector encompasses all of that parent's feasible pointwise states,
while the clean-sink theorem removed complete parents. The files bind the exact
remaining stream, clean-sink manifest and theorem, and prior forced certificate
ledger/verifier/selector manifest identities. The independent checker reparses
the stream, cover, and filter, re-verifies no mixed parent and unique
projections, reconstructs every clause, checks all eight hashes, and attributes
only complete satisfying models having exactly one true selector. Tests mutate
both branch bases, ALO, guards, metadata, selector names, and every bound input.
The eight-group freeze itself makes no blanket SAT/UNSAT claim. The complete
`B6-l4` clean-sink group is now certified UNSAT by a retained LRAT generated by
the pinned CaDiCaL 1.7.3 and accepted by the pinned `lrat-check`. The strict
ledger binds the selector manifest, remaining stream, clean-sink manifest and
theorem, producer, structural checker, CNF, proof, compressed artifact, and tool
identities. Fresh regeneration, structural checking, decompression, hash checks,
and proof replay are:

```sh
python3 verify_m6_clean_sink_B6_l4_certificate.py \
  --checker /path/to/pinned/lrat-check
```

The durable proof is `../certificates/m6-clean-sink-B6-l4.lrat.xz`; exact
identities and stage timings are in `m6-clean-sink-B6-l4-certificate.tsv`. No
UNSAT claim is made here for the other seven clean-sink groups.

```
group   parents  variables  clauses   bytes      sha256
B6-l4      2470      26086   520647   16535716   f576b3b590135c41ca1cf1eddf11338d3dddc58a9ca9d13bf92283e2def96e19
B6-l5      1024      24640   299409   12930838   16bde62125cbba48611ca022f6d265b21bfcc73ce0d5e65b90abc99d467b3257
B6-l6       220      23836   176397   10926464   c45fe0333585d8703c97db388c210d75a0f3eeddcbef34d5e25e3e6cc1eb98d9
B7-l2      8119      31735  1384937   30618652   362b5d0a5170360ce6fc4b191f998c3a0c68f7275e7809a2a9473bfdc843acd0
B7-l3      5016      28632   910178   22882872   7ea1fcff31c795e3b6b5d0b331c8f4fd39134ad2fbea763b19fddb914230ecec
B7-l4      1649      25265   395027   14488940   ac9759582a7b894fb726f3933fc5556b2ee10c73824bab361810e3c016f38a30
B7-l5       322      23938   191996   11180727   fef3ea51cae3c239a787eb27ec19f43d16a4cc24621df83ab9af5c9a6f46b829
B7-l6        42      23658   149156   10482686   afc62aa046f16a1bfa4c3de50c2847888c6144f1e6f466ff0c20ad7739629777
```
