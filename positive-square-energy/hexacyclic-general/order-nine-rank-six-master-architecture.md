# Order-nine rank-six master architecture (completion-gated draft)

## Status and boundary

This document is a proof architecture, not a theorem statement. It makes no
order-nine theorem claim while the exact pack manifest is incomplete. The
completion gate is parameterized by a supplied manifest rather than by the
SHA-256 of today's partial manifest. A future final manifest therefore becomes
green without changing the gate if, and only if, its transitive identities,
contiguous coverage, exact certificates, and symbolic ownership all pass.

The intended eventual scope is one loopless 2-connected rank-six multigraph
kernel on nine branch vertices, with minimum degree at least three, all simple
positive-length subdivisions of its fourteen edges, and arbitrary finite
rooted trees attached at branch or subdivision vertices. Multiblock and broader
connected hexacyclic conclusions remain outside this architecture.

## Exact census layer

The digest-owned kernel fixture gives 162 order-nine kernels, K971--K1132. Each
has degree multiset `4,3,3,3,3,3,3,3,3` and fourteen edges. The integer-only
parity-orbit census regenerates the following universe:

| item | exact count |
|:--|--:|
| physical parity rows | 1,726,000 |
| automorphism orbits | 1,108,126 |
| coarse-certified orbits | 921,831 |
| residual orbits | 186,295 |
| canonical-plus-coordinate targets | 2,794,425 |

There are fifteen targets per residual row: its canonical simple length vector
and one vector obtained by adding two to each of the fourteen coordinates in
turn. The coarse rows and residual rows are disjoint by construction.

## Final full manifest contract

The final manifest must use the existing
`rank-six-order-nine-r9g-search-pack-manifest-v1` schema and must contain ordered
XZ chunks whose embedded half-open residual ranges form exactly
`[0,186295)`. The auditor binds every chunk's compressed and raw sizes and
digests, the ordered target-key stream, the kernel fixture, witness pipeline,
rational engine, sparse base, atom classifier and classification, and symbolic
recognizer. Gaps, overlaps, path escapes, malformed streams, changed digests,
bad records, or any missing range are fatal.

The completion verifier deliberately does not pin the manifest's own digest.
It accepts the manifest selected by `--manifest`, lets that manifest bind its
chunks and transitive dependencies, regenerates the census, and then requires
the full range and all 2,794,425 target keys. Thus replacing today's partial
manifest with a correctly built final manifest is the only data-plane action
needed to turn the gate green.

The pack auditor also supports segmented exact replay with `--chunk-index I`
and `--write-chunk-receipt PATH`. These canonical receipts explicitly identify
themselves as bookkeeping-only and set `theorem_evidence=false`. An aggregate
built by `--aggregate-receipts ... --write-aggregate PATH` authenticates one
receipt per manifest chunk and checks additive coverage and ownership totals,
but remains only an execution index. Neither a chunk receipt nor its aggregate
is accepted by the completion verifier: theorem promotion still requires a
fresh exact replay of the full manifest in one verifier invocation.

## Exact symbolic ownership

The symbolic recognizer independently regenerates 82 exact decompositions on
80 residual rows, spanning signed-five-cycle, tetrahedron-plus-apex, and
coupled-triangle-tetrahedron geometries. It constructs exact rational Gram
matrices, checks positive semidefiniteness by principal minors, audits every
physical path ledger, and derives a dictionary of 388 exact cost-five target
keys.

For each covered target, the pack auditor assigns exactly one final owner:

1. a stored exact rational Gram-chain certificate, including targets that also
   occur in the symbolic dictionary; or
2. a symbolic certificate, only when the stored record is unresolved and its
   key belongs to that independently regenerated dictionary.

An unresolved key outside the symbolic dictionary is rejected. The rational
owner set and symbolic-only owner set are disjoint, and their union must equal
the entire covered target set. At full coverage that union must have exactly
2,794,425 keys. The symbolic dictionary is evidence, not a blanket waiver for
missing pack rows.

## Arbitrary lengths

For each parity orbit let `c` be its canonical simple length vector. Every
permitted simple subdivision vector `l` has `c<=l` coordinatewise with even
coordinate differences after permuting equivalent parallel edges. If `l=c`,
use the canonical target. Otherwise choose a coordinate `i` with
`l_i>=c_i+2`; the audited target `c+2e_i` is coordinatewise at most `l`.
Fixed-parity path-energy monotonicity under lengthening by two then carries the
certificate through all remaining simultaneous coordinate increases. Coarse
certificates use the same coordinatewise monotonicity directly.

This is why the finite universe has fifteen, rather than exponentially many,
targets per residual row.

## Rooted-tree lift

The eventual analytic tail mirrors the audited order-eight architecture. If a
subdivided rank-six block `B` has `L` edges, then `|V(B)|=L-5`. Once the finite
layer establishes the required `kappa(B)<=L+5` bound, attaching rooted trees
with `t` total edges uses one-vertex-sum additivity and `kappa(T)=|E(T)|` to
give `kappa(G)<=L+5+t`. Together with the DNN/trace inequalities this is the
planned lift to arbitrary tree shapes rooted at any branch or subdivision
vertex. This paragraph records the dependency chain; it does not promote the
currently incomplete finite layer to a theorem.

## Completion gate

From the repository root run:

```sh
python3 research/rank-six-order-nine-coverage-verifier.py
python3 -O research/rank-six-order-nine-coverage-verifier.py
```

With today's partial manifest both commands audit fail-closed and exit nonzero,
reporting the exact missing residual and target counts. With a final full
manifest, the same commands exit zero only after exact arithmetic certifies
complete disjoint ownership. Green output says
`ready_for_theorem_promotion=true` and still says `theorem_claimed=false`.
The theorem statement, STATE update, and any broader claim are separate future
promotion steps.
