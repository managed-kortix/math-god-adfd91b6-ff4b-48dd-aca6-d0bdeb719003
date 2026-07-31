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
