# Master theorem for all 118 rank-five suppressed kernels

## Theorem

Let `K` be a loopless multigraph with no cut vertex, minimum degree at least
three, and cyclomatic rank five. Let `B` be any finite simple subdivision of
`K`, and obtain `G` by attaching arbitrary finite rooted trees at arbitrary
vertices of `B`. Then

`s^+(G) >= |V(G)|`.

This is a theorem about the single rank-five block families. It does not claim
the result for every connected pentacyclic graph: graphs whose rank is split
among several cyclic blocks require the separate multiblock argument.

## Exact exhaustion

Suppressing the degree-two vertices of `B` recovers `K`. The independently
regenerated rank-five census proves that every such kernel has order two
through eight and belongs to exactly one of the following canonical classes:

| order | 2 | 3 | 4 | 5 | 6 | 7 | 8 | total |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| kernels | 1 | 3 | 13 | 24 | 38 | 23 | 16 | 118 |

The canonical fixture is `research/fixtures/rank-five-kernels.json`, with
SHA-256

`027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884`.

The census verifier regenerates incidence solutions from the degree-excess
partitions, canonicalizes them independently of the fixture, and requires
exact fixture equality. Thus the ledger is an exhaustion theorem, not a count
assumed by the implication master.

## Proof composition

The 118 rows have the following exact proof owners.

| fixture orders | rows | theorem package |
|:---|---:|:---|
| 2--4 | 17 | low-order master: six-path theorem, three-vertex orbit theorem, and four-vertex sieve/frontier composition |
| 5 except the all-odd `K5-e` row | 24 kernels, with one physical family separated | order-five kernel-family theorem |
| 5, all-odd `K5-e` | one separated physical family of kernel 32 | all-odd `K5-e` disjunctive theorem |
| 6 | 38 | order-six kernel-family theorem |
| 7 | 23 | order-seven kernel-family theorem |
| 8 | 16 | order-eight kernel-family theorem |

The two order-five packages are complementary, not two universal claims for
the same scope. In particular, the all-odd `K5-e` result uses a disjunction of
DNN and induced-territory certificates; this master does not infer a universal
DNN excess-four bound. The order-six package likewise retains its structural
cases as structural conclusions. Every package proves all allowed physical
path lengths by its stated exact frontier and fixed-parity monotonicity
argument, and each includes arbitrary rooted-tree attachments. Their scopes
therefore cover every subdivision of every one of the 118 census rows.

## Fail-closed master audit

`research/rank-five-order2-8-master-verifier.py` digest-locks the census and all
six implication owners, invokes each verifier, checks its acceptance ledger,
and hashes the complete dependency/output manifest. It separately checks the
canonical 118-row fixture and rejects census omission, every theorem-owner
omission, a widened `K5-e` scope, and a changed census digest. No Python
`assert` is used for a proof check.

Run both modes:

```text
python3 research/rank-five-order2-8-master-verifier.py
python3 -O research/rank-five-order2-8-master-verifier.py
```

The report is intentionally compact and explicitly records the multiblock
nonclaim. Passing this verifier establishes exactly the theorem above; it does
not promote the still-separate multiblock frontier to a theorem about all
connected pentacyclic graphs.
