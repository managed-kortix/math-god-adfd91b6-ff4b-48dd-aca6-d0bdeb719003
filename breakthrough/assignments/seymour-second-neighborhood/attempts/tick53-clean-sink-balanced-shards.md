# Tick 53: exact clean-sink balanced parent shards

## Scope

This is only a deterministic repartition of the seven uncertified clean-sink
parent groups. The certified `B6-l4` group and all 2,470 of its parents are
excluded. Its certificate ledger and strict verifier are bound by exact byte
count and SHA-256. No CNF is solved and no new SAT or UNSAT claim is made.

The source is the frozen clean-sink remaining stream and its complete parent
manifest. Consequently every shard also binds the clean-sink partition
manifest and rooted clean-sink theorem. The exact covered population is 16,392
parents in `B6-l5`, `B6-l6`, `B7-l2`, `B7-l3`, `B7-l4`, `B7-l5`, and `B7-l6`.

## Canonical partition

For each parent, let `q=H_CB` and let `H_CC` be the number of its six holes with
both endpoints in C. Parents retain their canonical source order. Each
`(parent-group,q,H_CC)` cell is split into `ceil(cell-size/500)` consecutive
parts. The part sizes are the unique balanced sizes in nonincreasing order, so
they differ by at most one and never exceed 500. This frozen table has 35 cells
and exactly 57 shards.

The complete table, every shard member hash, dimensions, and all six bound
input identities are in `experiments/m6-clean-sink-balanced-shards.tsv`.
`experiments/m6_clean_sink_balanced_shards.py` emits the manifest or one shard.
Each shard is the immutable branch base, one fresh selector per parent, one
selector ALO, and 153 pair-ordered guarded hole clauses per parent.

## Independent audit

`experiments/check_m6_clean_sink_balanced_shards.py` independently reparses the
clean stream and cover/filter, reconstructs all 18,862 parent groups, removes
exactly certified `B6-l4`, recomputes `q` and `H_CC`, applies the frozen balance
table, and proves the 57 member lists are disjoint and exhaust all 16,392 target
parents. It regenerates both immutable branch bases and checks the exact ordered
variable map, ALO, every guarded projection, metadata, dimensions, and complete
CNF hash ledger. A model is attributed only after a complete assignment
satisfies every clause and exactly one selector is true.

The exhaustive regression emits and hashes all 57 CNFs. Hostile tests mutate
both branch bases, balancing metadata, ALO, guards, selector names, every bound
identity, cell classification, manifest rows, and complete-model attribution.
These checks establish partition and encoding identity only; they do not solve
the shards or extend the restricted order-18 `m=6` theorem.
