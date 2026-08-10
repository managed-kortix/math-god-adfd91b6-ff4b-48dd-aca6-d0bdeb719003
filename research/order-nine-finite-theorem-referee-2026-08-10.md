# Referee report: order-nine rank-six finite certificate

## Verdict

The final order-nine manifest is complete at the finite-certificate level. Its
nine chunks cover the contiguous residual interval `[0,186295)`, and the
manifest commits to all `2,794,425 = 186,295 * 15` canonical-plus-coordinate
targets. I found no acceptance path by which a stored rational record, a
payload-free signed-cycle template, or a symbolically owned unresolved target
can evade an exact cost-at-most-five check.

This verdict is about the finite order-nine premise. An untracked draft
`research/rank-six-order-nine-kernel-theorem-verifier.py` is present and its
dependency pins, manifest checks, and 13 local hostile mutations pass. It is not
registered by the orders-2--10 master, has no frozen output digest, and was not
run in full mode in this referee session. More importantly, it does not pin a
source containing the canonical-domination, fixed-parity monotonicity, DNN
implication, and rooted-tree arguments that it promotes from strings in the
coverage report to a theorem conclusion. The current coverage gate still emits
`theorem_claimed=false`. The arbitrary-length lift is mathematically valid, but
it remains an analytic dependency rather than something proved by the binary
pack auditor alone.

I performed one successful exact segment replay, exact template replays,
manifest-wide identity/coverage regeneration, and hostile mutations. I did not
complete a fresh full-manifest exact replay in this referee session. Therefore
the persisted report does not replace the mandatory full replay required by
the completion gate.

## Artifacts reviewed

- `positive-square-energy/experiments/rank6_order9_search_manifest.json`
- `positive-square-energy/experiments/rank6_order9_pack_auditor.py`
- `positive-square-energy/experiments/rank6_order9_sparse_witness.py`
- `positive-square-energy/experiments/rank6_order8_sparse_pipeline.py`
- `positive-square-energy/experiments/rank6_order9_symbolic_recognizers.py`
- `positive-square-energy/experiments/rank6_orders8_10_atom_ledger_search.py`
- `positive-square-energy/experiments/rank6_orders8_10_atom_ledger_classification.json`
- `pentacyclic/research/order7-dim7-rational-gram-experiment.py`
- `research/rank-six-order-nine-coverage-verifier.py`
- `research/rank-six-order-nine-kernel-theorem-verifier.py` (untracked draft)
- `positive-square-energy/hexacyclic-general/order-nine-rank-six-master-architecture.md`
- `positive-square-energy/hexacyclic-general/latex-exposition-modules.md`

The manifest transitively pins the code/data dependencies used by its actual
audit. Its current SHA-256 is
`8aa9d797d9ed786ad438d6fd685e0ec576247b45c17a14749b76c45eebbe9168`.

## Exact rational and template records

### Shared rational records

For a shared record the decoder reconstructs a positive common denominator,
nine branch stereographic parameter rows, and both the canonical and `+2`
internal chains for all fourteen physical paths. The verifier maps every
parameter row to a rational unit vector and sums

`(1-<x,y>)/(1+<x,y>)`

with `Fraction` over every adjacent pair in every chain. An antipodal step is
rejected by the rational engine. Path widths are checked against the regenerated
canonical ledger, and all fifteen totals are separately required to be at most
five. Thus a shared record is not accepted from a floating score or from a
single canonical total.

### Individual records

An individual bitmap is range checked and decoded into at most fifteen separate
witnesses. For each present target the target-specific path ledger is
regenerated, including the selected coordinate's length increase by two. The
order-nine override checks exact types, dimensions, common denominators, path
widths, rational unit vectors, and the complete `Fraction` sum before requiring
the total to be at most five. Missing bitmap targets return `None`; they are not
silently counted as rational certificates.

### Payload-free signed-cycle templates

The template tag is legal only when the regenerated source row has the K971
forest/five-cycle structure. The verifier reconstructs the signed quotient
Gram matrix, checks unit diagonal and every principal minor, checks the
singleton contractions and doubled-bundle correlations, and obtains exact cost
five as five copies of `1/3+2/3`.

For the fourteen coordinate extensions, retaining the old chain and inserting
two duplicate consecutive vectors gives two zero-cost steps and preserves path
parity and endpoints. Therefore every template frontier has a feasible cost-five
chain. The implementation records this as adding
`2*(1-1)/(1+1)=0`. This is sufficient for `<=5`; it does not assert that the
extended path minimum remains equal to five.

I independently decoded chunk 0 and replayed all ten template records. Their
source indices are `83,84,87,97,98,103,104,154,155,158`, and each returned the
exact fifteen-tuple `(5,...,5)`.

## Symbolic key set

The operative symbolic dictionary is not the older
`rank6_order9_symbolic_templates.json`. It is regenerated by
`rank6_order9_symbolic_recognizers.py` from the exact atom classifier and its
canonical classification fixture.

The recognizer:

1. regenerates the complete ordered residual census;
2. regenerates every order-nine classifier result and requires ordered equality
   with the pinned classification records;
3. constructs the quotient Gram for each accepted atom decomposition;
4. checks positive semidefiniteness through all principal minors;
5. pulls the quotient Gram back through classes and switches;
6. audits every physical occurrence and obtains exact total cost five; and
7. derives only the canonical key and the coordinates whose canonical local
   cost is zero.

The resulting frozen report has 82 exact decompositions on 80 rows, with
geometry row counts `10,56,14` for signed five-cycle,
tetrahedron-plus-apex, and coupled triangle/tetrahedron respectively. The union
contains 388 distinct keys. Duplicate decompositions do not inflate the key
set because ownership is a `frozenset` of `(source_index, frontier)` pairs.

This is the correct symbolic key policy. A coordinate is symbolically owned
only when the same exact geometry admits a zero-cost same-parity extension. A
positive-cost coordinate is not inferred from canonical equality; it must have
a rational pack certificate. Conversely, symbolic completeness need not mean
classification of every possible equality geometry. The auditor only needs,
and enforces, that every unresolved pack target belong to this verified finite
dictionary.

The final ownership arithmetic is fail-closed:

- every non-`None` exact cost is inserted into the rational set;
- every `None` cost is inserted into the unresolved set;
- `unresolved - symbolic_keys` must be empty;
- within each chunk, rational keys plus symbolically owned unresolved keys must
  equal exactly `records * 15`; and
- every expected symbolic key in the chunk must be either numerically certified
  or symbolically certified.

Because source ranges are contiguous and disjoint, accumulation by per-chunk
counts cannot double count a target across chunks. Rational ownership takes
priority when a key is also in the symbolic dictionary, so the reported final
rational/symbolic owner totals are disjoint.

## Frontier extension

The canonical physical path multiset is minimal in its parity class after an
allowed permutation inside each parallel bundle: one unit path when available,
remaining odd paths of length three, and even paths of length two. Simplicity
allows at most one unit path in a parallel bundle. Hence every simple realization
has a length vector `l` with `c <= l` and even coordinate differences.

If `l=c`, the canonical target applies. Otherwise choose any coordinate `i`
with `l_i>=c_i+2`; the audited target `c+2e_i` is coordinatewise at most `l`.
For fixed branch correlation and fixed parity, exact path elimination gives

`f_q(r)=q*tan^2(acos((-1)^q*r)/(2q))`,

and the derivative argument in `latex-exposition-modules.md` proves that this
is nonincreasing when the path is lengthened by two. Replacing path interiors
by equal-angle chains, in separate auxiliary subspaces when necessary, therefore
lifts the selected frontier witness through all remaining simultaneous
lengthenings. The fifteen-target frontier is sufficient; exponentially many
multi-coordinate targets are not required.

The pack auditor does not itself prove this analytic lemma. A promotion owner
must state and bind the simple-subdivision/canonical-domination hypotheses and
this fixed-parity implication. In particular, the argument does not prove
one-edge subdivision monotonicity, does not apply to nonsimple subdivisions,
and does not say that one equality Gram remains optimal for every descendant.

## Streaming and arithmetic audit

The chunk reader first validates every manifest record and every chunk's
compressed size/digest. It checks ordered, gap-free, nonoverlapping ranges even
when only one chunk is selected for exact replay. It then validates XZ decoding,
raw size/digest, embedded start and attempt count, exact record count, and full
binary consumption. Paths are confined below the manifest directory.

The manifest-wide target commitment is regenerated from
`[source_index,kernel,row,target]` for all fifteen targets of every covered
source. The observed final values are:

- covered residual range: `[0,186295)`;
- covered target total: `2,794,425`;
- target stream SHA-256:
  `8e4398963209a30141a4c2bbb1c3d4b2a722251fba2096674f20057a148698c2`;
- missing residuals and targets: zero.

The full-manifest streaming callback audits one decoded chunk at a time, so it
does not retain all rational records in memory. The additive totals are safe
because ordered source intervals are validated before consumption. Symbolic
sets are retained globally, which is small and also permits an independent
final inclusion check.

Two details are worth recording but are not acceptance defects for the pinned
manifest. First, the binary varint decoder does not enforce minimal varint
encodings even though the general architecture recommends rejection of
nonminimal integers. Compressed and raw SHA-256 commitments prevent an alternate
encoding from being substituted into this manifest, but a future format revision
should enforce canonical varints directly. Second, chunk reports use
`missing_*` for missing coverage in the complete manifest, not outside the
selected chunk. The field names are potentially confusing, but receipt
validation consistently applies that definition and theorem eligibility is
always false for a single chunk.

## Replays and mutations

Commands were run from the repository root on 2026-08-10.

1. Manifest-wide digest/coverage regeneration passed. It decoded and hashed all
   nine XZ chunks, regenerated the census and 388-key symbolic dictionary, and
   reported full `[0,186295)` coverage. As expected, `--digest-only` reported
   no exact owners and was theorem-ineligible.
2. Exact replay of chunk 8, range `[160000,186295)`, passed. It certified all
   394,425 targets with 26,295 shared rational records, no individual/template/
   unresolved records, zero uncertified targets, and theorem eligibility false.
   Forty-two keys in that segment also belonged to the symbolic dictionary but
   were correctly assigned rational ownership.
3. Exact replay of chunk 0 was started but exceeded the session's 600-second
   command limit before producing a receipt. Chunk 0 was subsequently decoded
   directly and all ten payload-free template records were exactly replayed.
4. Receipt mutations changing rational-owner arithmetic, changing
   `theorem_evidence` to true, and changing the replay range were all rejected.
5. Raw-stream mutations adding a trailing byte, changing the magic, and
   truncating the stream were all rejected.

The successful chunk-8 report was:

```text
range=[160000,186295) targets=394425 exact=394425 uncertified=0
modes: shared=26295 individual=0 template=0 unresolved=0
rational owners=394425 symbolic-only owners=0 theorem_gate_eligible=false
```

## Required next gate

Before making the finite order-nine result a theorem dependency, complete the
draft promotion owner so that it invokes or inherits a fresh full-manifest exact
replay, pins its canonical output and all transitive sources, checks
normal/optimized output identity, and emits the narrow scope
`order=9;rank=6;kernels=K971-K1132;single-nontrivial-block` with conclusion
`kappa(B)<=|E(B)|+5`. It must bind an audited analytic source for canonical
domination, exact path elimination/fixed-parity monotonicity, the DNN trace
implication, one-vertex additivity, and the rooted-tree lift; restating those
facts in output strings is not transitive proof ownership. Only after that full
output is frozen should the orders-2--10 master register the owner.

No `STATE` file was read or modified for this referee report.
