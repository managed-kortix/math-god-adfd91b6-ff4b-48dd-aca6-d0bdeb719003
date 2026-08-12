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

The seven uncertified clean-sink parent groups are repartitioned into 57 exact
`(q,H_CC)` shards with a 500-parent cap by
`m6_clean_sink_balanced_shards.py`. The certified 2,470-parent `B6-l4` group is
excluded, and its certificate ledger/verifier are bound alongside the clean
stream, manifests, and theorems. The canonical table and member hashes are in
`m6-clean-sink-balanced-shards.tsv`; all CNF dimensions and hashes are in
`m6-clean-sink-balanced-shard-hashes.tsv`. Run the independent exhaustive gate
with `python3 test_m6_clean_sink_balanced_shards.py`. This layer only freezes a
partition and encoding; it does not solve any shard.

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

The 42-parent clean-sink `B7-l6` group also has an exact state refinement. For
each parent it fixes the ordered root/A-hole vector of C16 and C17, the internal
C pair state (hole, `16->17`, or `17->16`), the exact two-bit high-C mask, and
the separate C16-to-B and C17-to-B arc counts. The compatible surviving states
form exactly 30 leaves and 260 parent/state incidences; all 42 parents occur.
Each leaf reuses the frozen base variables, adds two seven-input unary counters,
three state units, and selectors guarded only to the exact parent holes.

```sh
python3 m6_b7_l6_state_split.py --leaf 0 --output /tmp/b7-l6-leaf.cnf
python3 check_m6_b7_l6_state_split.py /tmp/b7-l6-leaf.cnf
python3 test_m6_b7_l6_state_split.py
```

The complete manifest is `m6-b7-l6-state-split.tsv` (4,382 bytes, SHA-256
`a3b8f9d17b50dbfccd5f00740b33c6e90f6f10d26a3854dd627a45681e5c890e`);
`m6-b7-l6-state-leaf-hashes.tsv` freezes all 30 CNF hashes (3,163 bytes,
SHA-256 `eec464838f7d01e6cf053c7cbf8fa1442068d78738f4bd2772b15a8417543ae4`).
The independent checker reconstructs the 42 parents from the clean stream and
cover/filter, independently derives all exact states, checks complete coverage,
and rebuilds every clause. A post-gate 30-second CaDiCaL scout returned 11
UNSAT and 19 TIMEOUT leaves, with no SAT result. All eleven UNSAT leaves were
then certified with retained LRATs accepted by pinned `lrat-check`; they cover
exactly 90 incidences. The other 19 leaves contain 170 incidences and remain
uncertified. The exact scout is `m6-b7-l6-state-scout-30s.json`; certificate
identities are `m6-b7-l6-state-certificates.tsv`, replayed by
`verify_m6_b7_l6_state_certificates.py --checker /path/to/pinned/lrat-check`.

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

Two exact balanced `B6-l5`, `H_CC=2` shards are also certified UNSAT: q=0 has
78 parents and q=1 has 26. Their retained `xz -3` LRATs total 943,048 bytes.
`m6-clean-sink-B6-l5-HCC2-certificates.tsv` binds the frozen shard manifest and
partition theorem, complete CNF hash ledger, producer/checker, pinned tools,
CNFs, raw proofs, and durable artifacts. Fresh strict replay is:

```sh
python3 verify_m6_clean_sink_B6_l5_HCC2_certificates.py \
  --checker /path/to/pinned/lrat-check
```

The proof report is `../attempts/tick54-clean-sink-B6-l5-HCC2-certificates.md`.
No claim is made for the other 55 balanced shards.

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

The committed B7-l6 state campaign leaves exactly 19 uncertified hard state
leaves with 170 parent/state incidences. They are refined, and only they are
refined, by the simultaneous `S7(B)` orbit of the two exact C-to-B subsets.
For fixed subset sizes the complete orbit invariant is
`t = |N+(C16) intersect N+(C17) intersect B|`. This gives exactly 42
selector-batched orbit leaves and 392 parent/orbit incidences.

```sh
python3 m6_b7_l6_hard_orbits.py \
  --manifest-output m6-b7-l6-hard-orbits.tsv
python3 test_m6_b7_l6_hard_orbits.py
python3 m6_b7_l6_hard_orbit_scout.py \
  --solver /path/to/pinned/cadical --seconds 20 \
  --output m6-b7-l6-hard-orbit-scout-20s.json
```

Every orbit CNF is the immutable B7 base, the three prior state units, all 14
positive/negative C-to-B arc units for one canonical subset-pair representative,
one fresh selector per parent, one ALO, and 153 guarded hole clauses per parent.
The independent checker explicitly applies all 5,040 labelled `S7` permutations
to each representative, verifies a disjoint complete cover of every labelled
subset pair, reconstructs every CNF without importing the producer, checks the
complete hash ledger, and strictly attributes only complete exact-one-selector
models. The manifest is 5,533 bytes with SHA-256
`6c1080c6f97f92e68a9de6bc762145ceac9086f0b87dc4aa4ed73a746861b2d4`;
the 42-CNF ledger is 4,025 bytes with SHA-256
`83fe978c89f6f0c7901924123a322d42c2f31a1a15e931cdb30e861e31497030`.

After the exhaustive gate passed, the pinned CaDiCaL 1.7.3 20-second scout
returned 14 UNSAT and 28 TIMEOUT orbit leaves, representing 140 and 252
parent/orbit incidences, with zero SAT. Its 11,413-byte record has SHA-256
`32fa8260e2efb3cc326bafc2ce2d375ec84bf77ebb2fb5f9efd96b5b995ef31a`.
Exactly those 14 scout-UNSAT leaves were regenerated, structurally checked,
solved by pinned CaDiCaL in textual LRAT mode, and accepted by pinned
`lrat-check`. Their `xz -3` artifacts total 94,639,000 bytes and certify exactly
140 parent/orbit incidences. The strict source-bounded ledger and fresh replay
are `m6-b7-l6-hard-orbit-certificates.tsv` and
`verify_m6_b7_l6_hard_orbit_certificates.py`. The other 28 leaves remain
uncertified TIMEOUT frontier; no SAT or UNSAT claim is made for them.

Those 28 frozen TIMEOUTs (252 parent/orbit incidences) are further split by
simultaneous robust witnesses for every high C vertex. For deleted `c`, the
eligible witnesses are exactly `B \\ N+(c)` and the other C vertex when its
fixed internal arc points into `c`. Ordered choices are quotiented by the full
stabilizer in `S7(B)` of the already fixed ordered C-to-B subset pair. This
gives 117 canonical witness leaves and 1,066 parent/witness incidences.

```sh
python3 m6_b7_l6_hard_witness_orbits.py \
  --manifest-output m6-b7-l6-hard-witness-orbits.tsv \
  --hash-output m6-b7-l6-hard-witness-orbit-hashes.tsv --populate-hashes
python3 test_m6_b7_l6_hard_witness_orbits.py
python3 m6_b7_l6_hard_witness_orbit_scout.py \
  --solver /path/to/pinned/cadical --seconds 20 \
  --output m6-b7-l6-hard-witness-orbit-scout-20s.json
```

This is an existential ALO cover, not a model partition: a graph can admit
several robust-witness tuples and hence satisfy several leaves. It is
equisatisfiable because the base already contains one ALO over all robust
witnesses for each deletion, and the stabilizer sends every eligible labelled
tuple to exactly one retained canonical representative while preserving the
fixed subset pair and parent selector family. The independent checker enumerates
all 5,040 labelled `S7` permutations, filters the exact stabilizer, verifies the
disjoint labelled tuple-orbit cover and lexicographic canonical representatives,
then reconstructs and hashes every CNF without importing the producer.

The manifest is 7,151 bytes with SHA-256
`0329c78e2f563670c623206daf8b6b143c3813eac2f50d5e6f7c12b6b791186a`;
the complete 117-CNF ledger is 11,078 bytes with SHA-256
`d38e453e802408fb61b0c8f91641f16e231cfbec875993256b8dfe5acfa59513`.
The pinned CaDiCaL 1.7.3 20-second scout returned 117 TIMEOUT, zero SAT, and
zero UNSAT, representing all 1,066 parent/witness incidences. Its 48,447-byte
record has SHA-256
`1452d679f8cbb12350ec37564f69303fdbc04b3cecf1c037d66f99d8e72d1a3a`;
no proof or satisfiability claim is made.

The focused next layer adds exactly one no-gain child to each of those 117
committed witness leaves, preserving all 1,066 incidences. For every fixed
robust witness `(w,c)`, it adds `-p_w_k_c` for all 16 possible midpoints `k`.
Thus one-high-C leaves receive 16 units and two-high-C leaves receive 32 units
(12 and 105 leaves respectively). Positive-gain leaves are expressly not
generated by this layer.

```sh
python3 m6_b7_l6_hard_witness_no_gain.py \
  --manifest-output m6-b7-l6-hard-witness-no-gain.tsv \
  --hash-output m6-b7-l6-hard-witness-no-gain-hashes.tsv --populate-hashes
python3 test_m6_b7_l6_hard_witness_no_gain.py
python3 m6_b7_l6_hard_witness_no_gain_scout.py \
  --solver /path/to/pinned/cadical --seconds 20 \
  --output m6-b7-l6-hard-witness-no-gain-scout-20s.json
python3 check_m6_b7_l6_hard_witness_no_gain.py --scout
```

The independent checker derives the source leaves without importing the new
producer, reconstructs every CNF and negative path unit, checks all 117 frozen
hashes, and validates every committed scout row. The manifest is 6,831 bytes
with SHA-256
`a464607da5ca77da9beb4d5634ea5bc51036f44cad3f22354abfae0da9fe83f4`;
the 11,440-byte CNF ledger has SHA-256
`35ceea03f8b3f9d4cc054da5c3114e8fa9b04d1955f2a9bf64b163750fccab90`.
They bind the source witness manifest/hashes/scout and prior hard-orbit
certificate ledger. A fresh pinned CaDiCaL 1.7.3 20-second scout returned 75
UNSAT and 42 TIMEOUT leaves, representing 686 and 380 incidences, with zero
SAT. Its 48,487-byte record has SHA-256
`43bf624d24ca9459bf4de999385ed27367392a174aba46fe95b0773e6d1d7a64`.

Exactly those 75 scout-UNSAT leaves now have retained textual LRATs generated
by the pinned CaDiCaL 1.7.3 and accepted by pinned `lrat-check`. Their `xz -3`
artifacts total 42,951,720 bytes, below the strict exclusive 250,000,000-byte
limit, and certify exactly 686 parent/witness incidences. The ledger binds every
artifact plus the no-gain manifest, complete CNF hash ledger, scout, producer,
structural checker, scout source, test source, certificate producer, and pinned
tools. The ledger and verifier mutually bind canonical forms with only the
opposite hash field zeroed, avoiding an impossible raw-hash cycle. Fresh replay
regenerates and structurally checks each CNF, authenticates and decompresses
each artifact, hashes each raw LRAT, and invokes the pinned checker:

```sh
python3 verify_m6_b7_l6_hard_witness_no_gain_certificates.py \
  --checker /path/to/pinned/lrat-check
```

The other 42 scout-TIMEOUT no-gain leaves remain uncertified. No broader UNSAT
claim is made.

The complementary layer now adds exactly one compact positive-gain child to
each of the same 117 committed witness leaves. If `X` is the exact set of 16
or 32 path variables `p_w_k_c` for the selected ordered robust witness arcs,
the new child adds the single clause `OR X`. Its committed no-gain sibling adds
all units `-x` for `x in X`, which is exactly `NOT (OR X)`. Therefore the two
children are exhaustive by `P OR NOT P` and disjoint because `P AND NOT P` is
false. This is a model partition for each fixed witness leaf, not merely an
equisatisfiable overlapping cover.

```sh
python3 m6_b7_l6_hard_witness_positive_gain.py \
  --manifest-output m6-b7-l6-hard-witness-positive-gain.tsv \
  --hash-output m6-b7-l6-hard-witness-positive-gain-hashes.tsv --populate-hashes
python3 test_m6_b7_l6_hard_witness_positive_gain.py
python3 m6_b7_l6_hard_witness_positive_gain_scout.py \
  --solver /path/to/pinned/cadical --seconds 20 \
  --output m6-b7-l6-hard-witness-positive-gain-scout-20s.json
python3 check_m6_b7_l6_hard_witness_positive_gain.py --partition --scout
```

The producer binds the complete witness and committed no-gain artifact chain.
The independent checker does not import either child producer: it derives all
117 source leaves, reconstructs and hashes all 117 no-gain sibling CNFs plus
each positive CNF, and verifies every negative unit is the literalwise
complement of the corresponding positive ALO literal. It also pins the exact
117-entry scout status sequence, 0/3/114 SAT/UNSAT/TIMEOUT totals, 0/30/1,036
incidence totals, UNSAT ordinals 042/095/097, and every solver identity field.
Tests apply real polarity, substitution, omission, and duplication mutations to
the ALO and complement units, as well as witness/source binding mutations.

The 7,616-byte manifest has SHA-256
`eb0021165e41b9912c92abde3f4b26890075b0faafbabb0ced579ad6bb372ab8`;
the 11,695-byte complete 117-CNF ledger has SHA-256
`57a146838c09dca90e83e1ca19a504967199f3fde15f330769f8867a2068552e`.
A sequential pinned CaDiCaL 1.7.3 scout at exactly 20 seconds per leaf returned
3 UNSAT and 114 TIMEOUT, with zero SAT, representing 30 and 1,036 incidences.
The UNSAT leaves are 042 `o15-w01`, 095 `o37-w00`, and 097 `o37-w02`.
The 53,533-byte scout has SHA-256
`f5ed09b7134a3315a37d20db786fdd7d1675b1edc0ab6ef0969655fb7a6802f7`.

Exactly those three scout-UNSAT leaves now have three retained textual LRAT
certificates from
the pinned CaDiCaL 1.7.3, each accepted by pinned `lrat-check` and compressed
with `xz -3`. The artifacts total 35,233,748 bytes under a strict exclusive
250,000,000-byte bound and certify exactly 30 parent/witness incidences. The
ledger binds the complete positive-gain manifest, CNF hashes, scout, producer,
independent structural/partition checker, scout source, both tests, certificate
producer, pinned tools, and the committed no-gain complement manifest and
certificate ledger. No positive-gain leaf outside 042, 095, and 097 is claimed.

```sh
python3 verify_m6_b7_l6_hard_witness_positive_gain_certificates.py \
  --checker /path/to/pinned/lrat-check
```

The 114 committed positive-gain scout-TIMEOUT leaves are split completely by
selected deletion coordinate. A one-coordinate source has one child; a
two-coordinate source has two. Child `i` retains the source leaf and replaces
its 16/32-literal ALO by the 16-literal ALO `P_i` for exactly coordinate `i`.
Thus the source condition is exactly `OR_i P_i`, and existentially choosing a
child covers exactly the source models. This is an overlapping cover, not a
model partition: for a two-coordinate source, a model with both `P_0` and
`P_1` true belongs to both children. No other overlap is introduced by the
coordinate split.

```sh
python3 m6_b7_l6_hard_witness_positive_gain_coordinate.py \
  --manifest-output m6-b7-l6-hard-witness-positive-gain-coordinate.tsv \
  --hash-output m6-b7-l6-hard-witness-positive-gain-coordinate-hashes.tsv \
  --populate-hashes
python3 test_m6_b7_l6_hard_witness_positive_gain_coordinate.py
python3 m6_b7_l6_hard_witness_positive_gain_coordinate_scout.py \
  --solver /path/to/pinned/cadical --seconds 15 \
  --output m6-b7-l6-hard-witness-positive-gain-coordinate-scout-15s.json
python3 check_m6_b7_l6_hard_witness_positive_gain_coordinate.py --cover --scout
```

The exact census is 9 one-coordinate and 105 two-coordinate sources, hence 219
children and 1,990 parent/witness/coordinate incidence memberships. Every child
has one 16-literal ALO. The independent checker derives the 114 TIMEOUT sources
from the bound 20-second scout, verifies that its three omitted source leaves
are exactly the committed certificate ordinals 042/095/097, derives every
coordinate without importing the producer, and reconstructs all CNFs and
hashes. Hostile tests reject an omitted coordinate literal, changed polarity,
coordinate, deletion, witness, source, scout binding, or certificate binding.
The 13,557-byte manifest has SHA-256
`c1ea02ae0127713063efed74eeae84e9c6f22f800b0c6899d293b1a962028b49`;
the 25,213-byte complete CNF hash ledger has SHA-256
`aec75e12d82a9ad829dd64b8bce54687f493dbe0d73d5d7665eb965d97f905b6`.
A pinned CaDiCaL 1.7.3 scout at exactly 15 seconds per child returned 8 UNSAT
and 211 TIMEOUT, with zero SAT, representing 72 and 1,918 incidence
memberships. The UNSAT child ordinals are 020, 026, 096, 102, 172, 178, 215,
and 217. The 92,091-byte scout has SHA-256
`1ad3075ef0386c8bc8afec26b5a2cd392c140d17d8a69daa025063f4e8f3efab`.
Exactly those eight scout-UNSAT coordinate leaves now have retained textual
LRATs from pinned CaDiCaL 1.7.3, accepted by pinned `lrat-check`, and compressed
with `xz -3`. The artifacts total 3,756,712 bytes and certify exactly 72
incidence memberships. The strict ledger binds the full coordinate source
chain, all eight artifacts, and the committed positive-gain ancestor and
no-gain complement certificate ledgers, verifiers, and artifact sets. It also
directly binds every tracked Python support script in the transitive coordinate
generation/checking chain rather than relying only on indirect ancestor pins.
Fresh replay regenerates and structurally checks every CNF before checking each
raw LRAT. From
`breakthrough/assignments/seymour-second-neighborhood/experiments`, the exact
scope/replay command is:

```sh
python3 verify_m6_b7_l6_hard_witness_positive_gain_coordinate_certificates.py \
  --checker /path/to/pinned/lrat-check
```

No coordinate leaf outside 020, 026, 096, 102, 172, 178, 215, and 217 is
certified by this ledger; the other 211 scout-TIMEOUT leaves remain open. No
stabilizer quotient is needed or claimed: each child keeps its already
canonical source leaf and fixes a named deletion coordinate in that frozen
labeling. Stabilizers could identify isomorphic children or models and reduce
redundancy, but they cannot affect the literal identity
`OR_i (source AND P_i) = source AND OR_i P_i`, the coverage claim, or any LRAT
check. In particular, the two-coordinate children are an overlapping cover,
not disjoint orbit cells: a model satisfying both coordinate ALOs is retained
by both children and is intentionally counted twice for coverage purposes.

The committed `b7cdeff6816fd29eedc9633aea7d7adb949d55a5` singleton-parent
campaign refines the residual coordinate cover to one CNF per exact parent
membership. Its frozen five-second/two-job scout has the exact status totals
SAT/UNSAT/TIMEOUT `0/127/1255` and status-sequence SHA-256
`1c820b0de4e79a0ac355e9603566eca4a77eedf84f15989a124bdccbb30fbf82`.
Exactly those 127 ordered scout-UNSAT memberships now have textual LRATs from
pinned CaDiCaL 1.7.3, each accepted by pinned `lrat-check` and compressed with
`xz -3`. The 127 artifacts total 61,646,844 bytes, strictly below the exclusive
250,000,000-byte campaign limit; no TIMEOUT membership is certified.

The canonical certificate ledger binds each retained artifact by exact path,
byte count, and SHA-256. Its strict mutual self-pin has canonical ledger SHA-256
recorded in the verifier and canonical verifier SHA-256 recorded in the ledger;
the ordinary file hashes are reported by the final replay. The ledger binds the
base commit, complete residual and singleton
manifest/hash/scout chain, producer/checker/tests/scout/certificate sources,
ancestor certificate ledgers and verifier identities, exact ordered scout status
sequence, pinned solver/checker identities, and all 127 artifacts. The verifier
computes its local Python import closure and requires the frozen 22-source set;
every source executed from singleton certificate verification through CNF
generation and structural checking is pinned directly, including
`m6_parent_cnf.py`, `check_m6_parent_cnf.py`, and all intervening coordinate,
witness, orbit, state, clean-sink, residual-group, and `snc_cnf.py` modules.
Ancestor certificate verifiers are identity-bound but are not recursively
executed: this package's certificate claim is exactly the 127 singleton LRATs;
ancestor ledgers and artifacts are authenticated inputs to CNF reconstruction,
not fresh ancestor-proof replay claims.

Fresh replay regenerates and structurally checks every scoped CNF,
authenticates and decompresses every artifact, matches every raw LRAT identity,
and requires `c VERIFIED` from the pinned checker:

```sh
python3 test_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent.py
python3 test_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent_certificates.py
python3 verify_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent_certificates.py \
  --checker /path/to/pinned/lrat-check
```

The checked singleton scope now feeds an exact grouped residual campaign. The
producer verifies the current committed certificate ledger and verifier at
72,132/`bdad79d28b22d2b48ed0aef779765a6aafed752227c1952da36a8e180b48ca3d`
and 16,978/`ca3205e94f01b3b6e551373bad75333130a5d82bf3bc7cdf2e00f92be55e2d08`;
these values were measured from the current committed files, not copied from an
earlier campaign. It removes each residual CNF's complete old selector ALO and
guard layer, then rebuilds the exact surviving selector ALO, pairwise AMO, and
153 pair-ordered guarded parent-projection clauses per survivor.

The 127 checked singleton UNSAT formulas are exactly false disjuncts in their
frozen residual leaves. Removing precisely those disjuncts therefore preserves
each leaf's parent disjunction. The result has 153 leaves and 1,255 selectors,
with widths `1x1,3x2,2x3,38x4,109x10`. The independent checker reparses the
certificate ledger and separately reconstructs all residual leaves, parent
embeddings, six-hole projections, old selector layer, new exact-one layer, and
CNF stream without importing the grouped producer. The manifest is
12,775/`188efce389bbfcca54e6b6d5f881de3d9ae1603f2ecf7d671592abeabc1cd7f1`;
the complete CNF hash ledger is
16,431/`f4cc9738c0a5f40ed2fb213358a7025c72bd9d358d8bc694ad009b6743d93148`.

```sh
python3 test_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual.py
python3 m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual_scout.py \
  --solver /tmp/opencode/cadical-1.7.3/build/cadical --seconds 20 \
  --output m6-b7-l6-hard-witness-positive-gain-coordinate-grouped-residual-scout-20s.json
python3 check_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual.py --campaign --scout
```

The pinned sequential 20-second scout ran all 153 grouped leaves and returned
one UNSAT yield (leaf 129, width two) plus 152 TIMEOUTs, with zero SAT. Its
33,769-byte canonical record has SHA-256
`0729870deced23f34e87866dea86faac6aafc7740168230c54348b3778f53112` and
status-sequence SHA-256
`2fbf70a2995a1925ae0a969ec9e2b645a6cf8d2d62f332472c7b607afefcaeb6`.
Exactly that leaf now has a retained `xz -3` LRAT: 15,420,984 bytes, SHA-256
`f4387b4de1e4968f17d4031fc73e8286224145cb0ff00b66acae6c3a2088dcec`.
The strict one-row ledger binds every canonical row field, the complete grouped
campaign, singleton ancestry, hostile tests, and the exact 22-file transitive
Python runtime closure. Fresh regeneration and pinned proof replay are:

```sh
python3 test_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual_leaf_129_certificate.py
python3 verify_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual_leaf_129_certificate.py \
  --checker /path/to/pinned/lrat-check
```

Together with the retained no-gain certificates for `o37-w00`, `o37-w01`, and
`o37-w02`, the positive-gain certificates for `o37-w00` and `o37-w02`, and this
certificate for the complete surviving positive-gain `o37-w01-c16` residual,
this excludes the entire frozen `s28-t0` state. The statement is deliberately
restricted to this frozen B7 hard-orbit/state refinement: it is not a claim
about any other grouped leaf, B7 state, branch, or Seymour's conjecture.
