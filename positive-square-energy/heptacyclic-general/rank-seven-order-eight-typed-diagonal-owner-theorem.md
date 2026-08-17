# Rank-seven order-eight typed-diagonal owner theorem

## Statement

Let the authenticated rank-seven/order-eight coarse frontier consist of the
493,417 parity residual rows and their canonical plus fourteen one-coordinate
length-plus-two targets. Remove first the 605 rows owned by the exact
payload-free recognizers. In the resulting authenticated 492,812-row stream,
the typed-diagonal rational Gram lane owns exactly 402,712 rows and therefore
6,040,680 frontier targets.

Together, with payload-free ownership taking precedence, these two disjoint
lanes own 403,317 coarse rows and 6,049,755 targets. The exact remainder is
90,100 rows and 1,351,500 targets. No claim is made here that the remainder is
owned.

## Exact certificate

For a residual row, let `S` be its symmetric signed multiplicity matrix,
`S_uv=m_uv-2r_uv`. Vertices are typed by their signed degree and sorted list of
incident `(multiplicity, odd-count)` pairs. The finite deterministic search
chooses rational diagonal matrices `D0,D1`, constant on these exact types, and
sets

```text
X = D0 + D1 S,
M = max_i (XX^T)_ii,
G = XX^T/M + diag(1 - diag(XX^T)/M).
```

All entries are rational. Since `M>0` and every diagonal entry of `XX^T` is at
most `M`, the second summand is a nonnegative diagonal matrix. Hence `G` is
positive semidefinite as an exact sum of Gram squares, and `G_ii=1`.

For every physical path `p=(u,v,L)`, write

```text
c_p(G) = (1 - (-1)^L G_uv) / (L(1 + (-1)^L G_uv)).
```

The verifier checks with exact rational arithmetic that all denominators are
positive and that the canonical sum is at most six. Replacing any one `L` by
`L+2` preserves parity and weakly decreases that summand, so the same Gram owns
the fourteen coordinate frontier targets. The verifier nevertheless computes
all fifteen target sums separately; monotonicity is checked rather than merely
asserted.

## Segmented ownership proof

`rank7_order8_typed_diagonal_segmented_verifier.py` partitions the authenticated
rational-search stream into half-open intervals. For every row in a segment it
reruns the deterministic proposal search, then independently reconstructs and
checks the exact formula above. A canonical segment receipt contains:

1. the source-stream digest and exact stream/source endpoints;
2. the finite search parameters;
3. exact formula, PSD, and 15-cost verification totals;
4. a canonical ownership bitmap and its digest;
5. a digest of every `(stream index, source index, owner bit)` record.

The merger decodes every bitmap, recomputes its coverage digest, and requires a
gap-free, overlap-free partition of all 492,812 rows. It then requires exactly
402,712 typed owners and pins that count to the committed monolithic full scan.
Thus no single process exceeding the practical audit window is part of the
trusted coverage argument: each receipt is independently reproducible, while
the small merger owns the exact global partition arithmetic.

## Combined owner ledger

The rational-search index artifact is, by construction and authentication, the
exact complement of the payload-free owner set. Therefore the 605 payload-free
owners and 402,712 typed owners are disjoint. The merged accounting is

```text
493417 = 605 + 402712 + 90100,
7401255 = 9075 + 6040680 + 1351500.
```

The persisted combined ledger is generated only from a complete receipt
partition plus the canonical payload-free and typed full-scan reports. Its
`full_theorem` field remains false because 90,100 rows await another owner.
