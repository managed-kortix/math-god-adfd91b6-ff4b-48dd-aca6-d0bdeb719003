# Order-nine segmented promotion semantics

## Accepted repository proof artifact

The finite order-nine premise may be represented by
`positive-square-energy/experiments/rank6_order9_chunk_replays/proof-aggregate.json`
together with every receipt named by that aggregate. This is acceptable
repository theorem evidence only when the fail-closed validator establishes all
of the following:

1. The aggregate and receipts are canonical ASCII JSON with the current exact
   schemas and `theorem_evidence=true`.
2. Every receipt is produced by an independent `--chunk-index` invocation of
   the exact auditor, records `status=complete`, has zero uncertified targets,
   and reports disjoint rational and symbolic ownership of every target in its
   half-open range.
3. There is exactly one receipt for each final-manifest chunk, in manifest
   order, with no gap, overlap, omission, duplicate, or extra range. Their union
   is `[0,186295)` and their certified-target sum is `2,794,425`.
4. Receipt paths remain below the aggregate directory. Receipt bytes, auditor,
   manifest, chunks, target stream, and all transitive code/data dependencies
   match the identities embedded in the artifact and frozen by the promotion
   owner.
5. The aggregate is regenerated only after all independent replay commands exit
   successfully. A failed, interrupted, or absent replay cannot create a valid
   receipt and leaves the aggregate incomplete.

The receipts are execution records because the exact replay process writes them
only after recomputing and validating every certificate in the selected chunk.
SHA-256 is not execution proof. Digests provide identity and tamper detection;
they neither establish that a command ran nor establish the mathematics of the
audited certificates. The validator must inspect the receipt claims and exact
coverage semantics, not merely compare hashes.

The artifact is reproducible without one long-lived monolithic process. A
reviewer may delete one receipt, replay exactly that chunk, and rebuild the
aggregate. Replaying all chunks independently reconstructs the complete finite
evidence.

## Promotion semantics

`ready` means only that a coverage gate could discharge the finite premise. It
is not a theorem claim. Order-nine promotion occurs only when the narrow theorem
owner:

1. validates the complete segmented proof artifact under the rules above;
2. pins and audits the analytic lift owner, manifest, and proof note;
3. emits the exact scope
   `order=9;rank=6;kernels=K971-K1132;single-nontrivial-block`;
4. emits the finite conclusion `kappa(B)<=|E(B)|+5` and only then applies the
   audited fixed-parity length and rooted-tree lift to conclude
   `s+(G)>=|V(G)|`; and
5. has its source and canonical output frozen before a parent master accepts it.

This promotion covers the order-nine single-positive-rank-block class only. It
does not promote multiblock graphs, all connected hexacyclic graphs, order ten,
or any project-global status.

## Replay commands

Each segment is replayed in a separate process:

```sh
python3 positive-square-energy/experiments/rank6_order9_pack_auditor.py \
  --chunk-index I --write-chunk-receipt \
  positive-square-energy/experiments/rank6_order9_chunk_replays/chunk-START-STOP.json
```

After all nine receipts exist, build the aggregate with
`--aggregate-receipts` and `--write-aggregate`. The theorem owner validates the
aggregate and every referenced receipt; it does not rerun the twenty-minute
full-manifest process.
