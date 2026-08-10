# Order-ten rank-six master architecture (completion-gated draft)

## Status and boundary

This document is a proof architecture, not a theorem statement. It makes no
order-ten theorem claim while the exact pack manifest is incomplete. The
completion gate accepts a supplied manifest rather than pinning today's partial
manifest digest. A future final manifest therefore becomes green without code
changes if, and only if, its transitive identities, contiguous coverage, exact
certificates, and final ownership all pass.

The intended eventual scope is one loopless 2-connected rank-six multigraph
kernel on ten branch vertices, with minimum degree at least three, all simple
positive-length subdivisions of its fifteen edges, and arbitrary finite rooted
trees attached at branch or subdivision vertices. Multiblock and broader
connected hexacyclic conclusions remain outside this architecture.

## Exact census layer

The digest-owned fixture gives 66 order-ten kernels, K1133--K1198. Every kernel
is cubic and has fifteen edges. The integer-only parity-orbit census regenerates:

| item | exact count |
|:--|--:|
| physical parity rows | 1,508,832 |
| automorphism orbits | 497,572 |
| coarse-certified orbits | 372,115 |
| residual orbits | 125,457 |
| canonical-plus-coordinate targets | 2,007,312 |

There are sixteen targets per residual: the canonical simple length vector and
one vector obtained by adding two to each of the fifteen coordinates in turn.
The coarse and residual rows are disjoint by construction.

## Final full manifest contract

The final manifest uses the existing
`rank-six-order-ten-r10g-search-pack-manifest-v1` schema. Its ordered XZ chunks
must embed exactly the contiguous residual interval `[0,125457)`. The hardened
auditor binds compressed and raw sizes and digests, the ordered target-key
stream, kernel fixture, census, witness stream, equality recognizer and fixture,
and symbolic ledger and fixture. Gaps, overlaps, repeated paths, path escapes,
malformed streams, changed dependencies, bad exact records, or missing ranges
are fatal.

The completion verifier does not pin the manifest's digest. The selected
manifest binds every chunk and transitive dependency, while the verifier
independently requires all 125,457 residual rows and 2,007,312 target keys.
Replacing today's partial manifest with a correctly built complete manifest is
the only data-plane action needed to turn the gate green.

The promotion owner at
`research/rank-six-order-ten-kernel-theorem-verifier.py` adds a second,
theorem-facing gate. Full mode accepts no receipt or aggregate: it requires the
selected manifest itself to cover `[0,125457)` and then causes a fresh exact
streaming replay. Practical mode replays one selected manifest segment exactly,
but marks that execution as non-theorem evidence and cannot emit a child
manifest. The owner also pins and invokes the separate conditional analytic
lift owner, its manifest, and its canonical output.

## Exact final ownership

The symbolic ledger independently regenerates 178 exact decompositions in the
three profiles `mixed-1/simplex-3-4`, `mixed-2/simplex-4`, and
`mixed-5/simplex-none`. It verifies the atom model, signed contractions,
prescribed quotient correlations, and agreement with the separate equality
recognizer. Their union is an exact dictionary of 692 target keys.

Every covered target receives exactly one final owner:

1. a stored exact rational certificate, including a target also present in the
   symbolic dictionary; or
2. a symbolic certificate, only when its stored target is unresolved and its
   key belongs to the independently regenerated dictionary.

An unresolved key outside that dictionary is fatal. Rational owners and
symbolic-only owners are disjoint, and their union must equal the covered key
set. At full coverage this union must contain exactly 2,007,312 keys. Symbolic
membership cannot excuse a missing pack row.

## Arbitrary lengths

For each parity orbit let `c` be its canonical simple length vector. Every
allowed subdivision vector `l` has `c<=l` coordinatewise with even coordinate
differences after permuting equivalent parallel paths. If `l=c`, use the
canonical target. Otherwise choose `i` with `l_i>=c_i+2`; the audited target
`c+2e_i` is coordinatewise at most `l`. Fixed-parity path-energy monotonicity
under lengthening by two carries that certificate through all remaining
simultaneous coordinate increases. Coarse certificates lift by the same
monotonicity. Thus sixteen targets per residual suffice for arbitrary lengths.

## Rooted-tree lift

If a subdivided rank-six block `B` has `L` edges, then `|V(B)|=L-5`. Once the
finite layer establishes the needed `kappa(B)<=L+5` bound, attaching rooted
trees with `t` total edges uses one-vertex-sum additivity and
`kappa(T)=|E(T)|` to give `kappa(G)<=L+5+t`. Together with the DNN/trace
inequalities, this is the planned lift to arbitrary finite tree shapes rooted
at branch or subdivision vertices. This records dependencies only and does not
promote the incomplete finite layer to a theorem.

## Completion gate

From the repository root run:

```sh
python3 research/rank-six-order-ten-coverage-verifier.py
python3 -O research/rank-six-order-ten-coverage-verifier.py
```

With the current partial manifest both commands exit nonzero and print the
exact missing residual and target counts. The unchanged gate exits zero for a
final manifest only after exact arithmetic establishes complete disjoint
ownership. Green output still records `theorem_claimed=false`; theorem wording,
project-state changes, and broader claims are separate future promotion steps.

The promotion owner has the same present fail-closed boundary:

```sh
python3 research/rank-six-order-ten-kernel-theorem-verifier.py --full
python3 -O research/rank-six-order-ten-kernel-theorem-verifier.py --full
```

For a bounded exact replay of an available segment, use:

```sh
python3 research/rank-six-order-ten-kernel-theorem-verifier.py --practical --chunk-index 0
```

Practical output is explicitly a nonclaim. No theorem or `STATE.md` promotion
is made by this architecture.
