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
