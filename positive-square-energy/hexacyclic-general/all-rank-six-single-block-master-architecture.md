# All rank-six single-block master theorem and certificate architecture

## 1. Final theorem and exact scope

The intended final statement should be one theorem, not nine unrelated finite
claims.

> **Master single-block theorem.** Let `G` be a finite connected simple graph
> of cyclomatic rank six with exactly one nontrivial block. Equivalently, after
> deleting attached trees and suppressing the degree-two vertices of its
> 2-connected core, obtain a loopless 2-connected multigraph `K` of minimum
> degree at least three. Then
>
> `s+(G) >= |V(G)|`.
>
> The conclusion permits arbitrary positive subdivision lengths and arbitrary
> finite rooted trees attached at every branch or subdivision vertex.

If `n=|V(K)|`, then `|E(K)|=n+5`, while minimum degree three gives
`3n<=2n+10`. Hence `2<=n<=10`. The frozen orders-two-through-ten fixture is
therefore an exhaustive kernel universe, not an experimental cutoff. Its order
ledger is

```text
1, 4, 26, 84, 216, 314, 325, 162, 66; total 1198.
```

The theorem is deliberately a **single-block** theorem. It must not be promoted
to all connected hexacyclic graphs without a separate block-tree synthesis.

The finite theorem interface is the uniform inequality

`kappa(B) <= |E(B)|+5`                                           (M1)

for every simple subdivision `B` of every one of the 1198 kernels. Everything
in the master certificate should prove exactly (M1); the spectral conclusion
and tree lift occur once, after all nine order slices have been combined.

## 2. One canonical finite universe

For each kernel support pair `e`, let `m_e` be its multiplicity and let `o_e`
be the number of odd replacement paths. A physical parity row is the vector
`(o_e)_e`, with `0<=o_e<=m_e`. The canonical simple length multiset on that
support is

```text
(1,3,...,3,2,...,2) if o_e>0,
(2,...,2)           if o_e=0,
```

where simplicity allows at most one unit path in a parallel class. Quotient
physical rows by the full multigraph automorphism group, but retain enough data
to reconstruct the physical path order. Every orbit receives a stable key

```text
(order, kernel_id, canonical_sparse_parity_row, orbit_index).
```

For a kernel with `p=n+5` physical paths and canonical vector `c`, define

`F(c)={c} union {c+2e_i: 0<=i<p}`.                            (M2)

Thus the target label is `C` or `X_i`. The target-key stream, in canonical
kernel/orbit/label order, is the theorem universe for that order. Counts and a
digest are useful identity checks, but the verifier must regenerate the stream
and prove set equality; totals alone are not completeness.

The exact tetrahedral sieve may own an entire parity orbit before (M2) is
materialized. All remaining orbits form the residual source stream. For each
order the ownership partition is therefore

```text
all parity orbits
  = coarse tetrahedral or analytic owners
    disjoint-union residual orbits,

all residual frontier keys
  = rational-witness keys
    disjoint-union symbolic-equality keys.
```

No key may be silently omitted, multiply owned, or accepted by a discovery
status bit.

## 3. Certificate layers

The final certificate should have five layers.

### Layer A: kernel and orbit census

Regenerate the 1198 canonical kernels, their order partition, supports,
degrees, automorphism groups, physical parity rows, orbit representatives,
canonical length vectors, and residual target-key streams. The existing frozen
fixture can remain the distribution format, but an independent verifier must
check its defining properties and canonical ordering.

### Layer B: small exact owners

Keep the current low-order and coarse certificates:

- order two: analytic seven-path theorem;
- orders three through six: exact rational/tetrahedral owners and their named
  exceptional ledgers;
- orders seven through ten: exact integer tetrahedral sieve before residual
  expansion.

These owners should emit key-stream commitments and scope records, not merely
headline acceptance text.

### Layer C: huge compressed rational chunks

For residual targets not routed symbolically, retain the already successful
proof model: exact rational Gram-chain feasibility at excess at most five. It
has a smaller trusted base than a support-bound format involving certified
transcendental intervals.

Use one binary format version per incompatible path width (`R7G*`, `R8G2`,
`R9G1`, `R10G1` are acceptable), wrapped in XZ. A record may be:

```text
shared     one exact branch/path realization owns every target in this source;
bitmap     a target bitmap followed by exact realizations for selected labels;
individual one exact realization for one target;
symbolic   payload-free equality-ledger tag.
```

The canonical decoder must reject trailing bytes, nonminimal integers,
out-of-range dimensions, unknown tags, duplicate labels, malformed bitmaps,
zero denominators, and any record whose embedded source range disagrees with
the manifest. For each rational target it reconstructs all unit vectors over
`Fraction`, checks endpoint consistency and the complete path-length ledger,
and verifies

`sum_(path steps xy) (1-<x,y>)/(1+<x,y>) <= 5`                (M3)

exactly, with every denominator positive. Search scores and decimal costs are
never read by the theorem verifier.

Large files should be contiguous source ranges, preferably sized for practical
parallel audit rather than maximal compression. Chunks may be tens or hundreds
of megabytes. Compression is only transport: completeness is certified from
the decoded key stream.

### Layer D: symbolic equality dictionary

Keep equality records out of the large payloads. A symbolic record contains a
geometry tag, switching/contraction map, atom-to-physical-path assignment, and
the minimal rational quotient Gram or an exact gluing prescription. The shared
atom dictionary currently needs at least:

| atom | physical ledger | exact lower cost |
|:--|:--|--:|
| `M2` | one odd and one even path on one endpoint pair | 1 |
| `S3` | three odd unit paths forming `K3` | 1 |
| `S4` | six odd unit paths forming `K4` | 3 |
| `Z` | signed contraction path | 0 |

The known cost-five compositions are

```text
5 M2                         signed five-cycle quotient;
S4 + 2 M2                   tetrahedron plus apex;
S3 + S4 + M2                coupled triangle/tetrahedron ledger.
```

The third composition is mandatory: it occurs at order eight (`K883`, `K942`),
order nine (`K1060`, `K1119`, `K1123`), and order ten (`K1188`, `K1197`). A
master restricted to the first two geometries is false.

The symbolic verifier must do both sides of equality. It proves the lower bound
by the scalar mixed-pair inequality and simplex tangent stresses, then proves
attainment by exact PSD completion, checking the physical path assignment and
cost five. For a coordinate target `X_i`, it must either verify a zero-cost
same-parity extension under the same symbolic geometry or route that target to
an ordinary rational record. It must not infer all coordinate targets from the
canonical tag.

This architecture does **not** require a global theorem saying these are every
possible cost-five geometry. It requires the weaker, finite, fail-closed fact
that every target key is owned by either a verified rational record or one of
the verified symbolic records. Any new numerical null simply remains unproved
until it receives one of those two forms.

### Layer E: order and global masters

Each order master regenerates its expected residual key stream, audits every
chunk and symbolic table, and requires exact disjoint set equality. The global
master then requires exact order coverage `{2,...,10}`, exact kernel coverage
`K1,...,K1198`, and the theorem conclusion (M1) from every order owner.

The global master must contain no search, optimizer, random seed, denominator
loop, or fallback acceptance path.

## 4. Transitive manifests

Use a three-level manifest graph rather than one handwritten list of chunk
hashes.

### Chunk manifest

One canonical ASCII JSON manifest per order records:

```text
schema and format version
order and kernel ID interval
kernel-fixture digest
census-program digest and census-output digest
ordered residual-source-stream digest
ordered target-key-stream digest
frontiers per residual
for every chunk:
  source half-open range
  relative path
  compressed byte count and SHA-256
  raw byte count and SHA-256
  decoded record count
  decoded owned-key count and ordered-key digest
symbolic-fixture path, digest, key count, and ordered-key digest
expected complete source range and complete target count
```

Ranges must be contiguous, ordered, nonoverlapping, and exhaustive. The auditor
recomputes compressed and raw identities, but then parses and mathematically
checks every record. SHA-256 identifies the bytes under review; it does not
replace proof verification.

### Order theorem manifest

The order master emits a canonical manifest containing:

```text
order scope and kernel IDs
kernel count and orbit ledgers
coarse-owner key digest
residual-source and target-key digests
chunk-manifest digest
symbolic-verifier source/output digests
rational-key and symbolic-key digests
exact partition-equality result
conclusion: kappa(B)<=|E(B)|+5 for every simple subdivision
explicit nonclaims
```

### Global implication manifest

The final master pins the kernel-census verifier and all order theorem
manifests/verifiers. It validates their scopes rather than trusting prose in
stdout, checks that the order/kernel intervals partition the fixture, and emits
one implication manifest for the 1198 families. Every direct dependency should
include

```text
(logical name, relative path, source SHA-256, canonical output SHA-256,
 schema, scope, conclusion).
```

The global verifier runs dependencies using the current interpreter in normal
or optimized mode, uses explicit exceptions rather than `assert`, and requires
byte-identical normal/`python -O` reports. Hostile self-tests should reject an
omitted order, altered range, duplicate owner, changed fixture, truncated
chunk list, unknown equality tag, widened all-hexacyclic claim, and replacement
of `<=5` by an unchecked status flag.

The transitive root printed by the paper is the digest of this canonical global
implication manifest. Reproduction documentation should also list every leaf
artifact so that the root is not an opaque appeal to a hash.

## 5. All-length proof

The all-length argument should appear once as a lemma in the paper and once as
an explicit implication check in every residual census.

Let `l` be any simple subdivision length vector in a fixed physical parity
orbit and let `c` be its canonical vector. After permuting equal parallel
kernel edges, `c<=l` coordinatewise and every difference is even.

- If `l=c`, use the canonical target `C`.
- Otherwise choose any `i` with `l_i>=c_i+2`. Then
  `c+2e_i<=l` coordinatewise, so use target `X_i`.
- For fixed branch correlation and parity,
  `f_j(r)=j tan^2(acos((-1)^j r)/(2j))` is nonincreasing under `j -> j+2`.
  Repeated coordinatewise lengthening therefore cannot increase the certified
  objective.

Thus `C` and the one-coordinate frontiers cover simultaneous arbitrary
lengthening in every coordinate. No claim that one equality Gram survives all
lengthenings is needed: a noncanonical vector is assigned to one certified
`X_i`, and monotonicity handles all remaining coordinates from there.

For coarse tetrahedral rows the canonical certificate alone suffices because
the same Gram is valid and nonincreasing under every same-parity lengthening.
For residual rows the complete `p+1` frontier is required unless a separate
symbolic rule explicitly proves all those targets.

## 6. Tree lift and spectral conclusion

Let `B` have `L` edges. Since its cyclomatic rank is six,

`|V(B)|=L-5`.                                                 (M4)

Attach rooted trees with `t` edges in total at arbitrary vertices of `B` to
obtain `G`. One-vertex-sum additivity of `kappa` and `kappa(T)=|E(T)|` give

`kappa(G)<=kappa(B)+t<=L+5+t`.                               (M5)

Also `|E(G)|=L+t` and `|V(G)|=L-5+t`. Using `s-(G)<=kappa(G)`
and `s+(G)+s-(G)=2|E(G)|`,

```text
s+(G) >= 2(L+t)-(L+5+t)
      = L-5+t
      = |V(G)|.
```

This proof automatically includes trees rooted at internal subdivision
vertices. It should not be repeated in nine finite sections, and no edge
monotonicity or contraction of an attached tree is needed.

## 7. Paper structure

A clean final paper can use the following order.

1. **Introduction and theorem.** State the single-block theorem, the 1198
   kernel count, the computer-assisted nature of the finite middle, and the
   precise nonclaim for multiblock hexacyclic graphs.
2. **DNN and path elimination.** Define `kappa`, prove the trace reduction,
   state exact path elimination and fixed-parity monotonicity.
3. **Structural exhaustion.** Suppress the unique nontrivial block, prove
   `2<=n<=10`, define physical parity rows and canonical simple lengths, and
   explain the frozen canonical kernel fixture.
4. **Finite certificate theorem.** State one proposition asserting (M1) for all
   1198 kernels. Describe the coarse/residual ownership partition and the
   canonical-plus-coordinate universe.
5. **Exact rational certificates.** Specify the binary records, exact Gram-chain
   audit, chunk manifests, and complete-key equality. Put large count tables by
   order here, not raw witness data.
6. **Symbolic equality ledgers.** Prove `M2`, `S3`, and `S4`; describe switching,
   contraction, PSD gluing, all three known cost-five compositions, and the
   coordinate-frontier rule.
7. **All-length and tree lift.** Prove the two short lemmas above and derive the
   main theorem from the finite certificate proposition.
8. **Trusted base and reproducibility.** List exact arithmetic, canonical
   parsing, decompression, deterministic generation, transitive manifests,
   normal/`-O` equivalence, commands, expected root digest, and limitations.
9. **Appendices.** Give per-order ledgers, schemas, digest tables, symbolic
   signatures, hostile mutation tests, and a dependency DAG. Keep discovery
   heuristics and optimizer settings in a reproducibility appendix or separate
   data note, not in the logical proof.

The main text should distinguish three statements: exhaustive generation is a
finite combinatorial proof; a rational record is a feasible exact upper-bound
proof; a symbolic ledger additionally proves equality. Numerical optimization
is only a record-discovery mechanism.

## 8. What remains after merely running searches

Finishing order-eight, order-nine, and order-ten search processes is necessary
but is not by itself a theorem. The non-search work is:

1. **Finalize every pack.** Confirm clean process completion, audit every XZ
   stream, rebuild the currently stale order-eight manifest beyond its pinned
   prefix, and generate complete order-nine and order-ten manifests.
2. **Resolve every null exactly.** A failed numerical reconstruction is not an
   equality case. Give it an exact rational witness or a symbolic lower-bound
   and attainment ledger. Extend the dictionary if geometries beyond
   `S3+S4+M2` appear.
3. **Build order-eight through order-ten theorem verifiers.** Existing census,
   structural, recognizer, and search scripts explicitly report non-theorem
   scopes. New masters must regenerate expected keys and prove exact disjoint
   ownership equality.
4. **Unify orders two through seven.** Adapt their existing owners to emit the
   same machine-readable scope/conclusion manifests and key commitments; do not
   weaken already proved exact checks to headline-output matching.
5. **Implement the global orders-two-through-ten master.** Pin and invoke all
   direct dependencies, verify the transitive scope partition, run hostile
   mutations, and require normal/optimized byte identity.
6. **Write the structural front and analytic back of the proof.** The kernel
   order bound, canonical-simple realization lemma, all-length frontier lemma,
   tree additivity, and trace calculation are mathematical obligations even
   when all finite keys have witnesses.
7. **Audit the trusted implementation.** Harden canonical JSON and binary
   parsing, XZ error handling, exact PSD/unit-vector checks, denominator signs,
   duplicate/range detection, equality atom assignment, and assertion-free
   behavior under `python -O`.
8. **Freeze reproducibility artifacts.** Record final source and artifact
   digests, expected counts, commands, software requirements, storage sizes,
   and the transitive root in the manuscript and repository documentation.
9. **Keep the theorem boundary explicit.** The result closes every rank-six
   one-nontrivial-block graph. Passing these searches does not supply the
   decomposition/ownership theorem needed for arbitrary multiblock hexacyclic
   graphs.

If every searched target eventually receives an exact rational record, no
global equality-classification theorem is needed. If symbolic tags are used to
avoid huge equality payloads, only the tagged finite key set must be recognized
and verified exactly; claiming that the three known ledgers classify every
possible rank-six equality objective would be a stronger theorem and remains
unproved.
