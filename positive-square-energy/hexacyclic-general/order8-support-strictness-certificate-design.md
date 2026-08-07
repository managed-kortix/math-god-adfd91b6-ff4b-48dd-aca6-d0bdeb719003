# Order-eight support-level strictness certificate

## Objective

The density lemma in `rank-six-orders8-10-rational-density-reduction.md`
means that a strict real branch Gram is enough: internal rational path vectors
need not be stored.  The current `R8G2` packs nevertheless store 26 complete
path families per residual orbit.  A smaller proof object should instead prove

```text
F_L(G) < 5
```

for every required length ledger `L`, where `G` is a real correlation matrix
and

```text
f_l(r) = l tan^2(acos((-1)^l r)/(2l)),
F_L(G) = sum_paths f_l(G_uv).
```

This already includes the optimal real interpolation along each path.  The
density lemma then produces rational unit vectors for every strict row.  Exact
rational Grams remain necessary only on classified equality faces.

## Proposed packet

Use four authenticated tables rather than one witness per target.

1. `templates`: exact rational branch Grams.  A template can store rational
   stereographic branch parameters (which make PSD automatic) or a rational
   matrix with an exact `LDL^T` certificate.  Optional interval boxes around a
   center are useful for merging numerical candidates, but the proof only needs
   one certified center in each box.
2. `support bounds`: for each template and each support edge, store outward
   rational upper bounds for `f_1`, `f_2`, `f_3`, and the frontier variants
   `f_3`, `f_4`, `f_5`.  Monotonicity of `f_l(r)` makes each bound an endpoint
   evaluation.  Transcendental endpoint values must be enclosed by a small
   independently checked rational interval routine; binary64 is not proof.
3. `domination rules`: map each residual support row to a template and a
   dominating ledger class.  Verification is integer arithmetic:
   multiply the precomputed local upper bounds by the path counts and require
   the sum to be `<5`.  For all 13 frontiers either check 13 sums or use the
   single inequality

   ```text
   canonical_upper + max_i(frontier_upper_i - canonical_upper_i) < 5.
   ```

4. `equality dictionary`: payload-free symbolic tags for the signed-cycle and
   tetrahedron-plus-apex equality rows, with exact rational Grams and exact
   support costs.  Equality classification remains a separate theorem step;
   density cannot replace it.

The row-to-template map can use sorted residual order and delta-coded template
IDs.  A Merkle tree is useful only for distribution, random access, or
incremental extension.  It does not reduce the mathematical certificate: a
single SHA-256 commitment to canonical table bytes is enough for a monolithic
artifact.  If chunks are retained, commit leaves of the form

```text
H(source_index || support_key || template_id || domination_rule)
```

and store the root plus ordered range metadata.  The verifier must still read
every leaf for a full theorem audit.

## Exact verification

For each template the verifier should perform the following fail-closed steps.

1. Check canonical rational encoding, the source-kernel digest, and the ordered
   residual-key digest.
2. Reconstruct the exact rational unit vectors and their Gram, or verify an
   exact rational `LDL^T` factorization.  If a box itself is used as a cover
   object, prove that it contains the certified center; proving every matrix in
   the box PSD is unnecessary.
3. Check interval enclosures for every needed local path function.  On
   `-1<(-1)^l r<1`, `f_l` is monotone in the transformed correlation, so no
   interval optimization is needed after selecting the adverse endpoint.
4. Regenerate each support row and its 13 canonical paths.  Apply only the
   recorded support counts and local bounds; reject unknown edges, dimensions,
   or length classes.
5. Require a positive rational margin `5-U`, never `U<=5`, for density-based
   rows.  Route exact-five rows to the symbolic equality verifier.

This is an exact support-level strictness proof even though optimized real Grams
were used to discover the boxes.  Optimization is absent from the trusted
verifier.

## Finite-cover construction

A practical builder can start from the decoded branch Grams already in the
order-eight packs.

1. Drop all internal path vectors and evaluate every residual on candidate
   branch Grams from the same kernel.
2. Solve set cover greedily, then prune templates by reverse deletion.  Keep a
   rationalized center for each survivor.  Optional rational interval boxes can
   guide merging while assigned strict inequalities are rechecked at the final
   center.
3. Merge nearby boxes only after exact interval re-verification.  Clustering
   rounded Gram entries alone is not sound and, empirically, gives little
   deduplication in the current prefix.
4. Store assignment exceptions before introducing a new template.  Support
   domination may let one template cover rows that have different parity
   vectors but no larger count in any adverse local-cost class.
5. Keep exact-five symbolic rows outside the strict cover.  A box touching five
   cannot invoke density and must either be shrunk or reclassified.

`rank6_order8_template_cover_analysis.py` implements the discovery-only part.
It decodes authenticated `R8G2` witnesses, discards path interiors, computes
branch-Gram signatures, and runs a numerical same-kernel greedy cover.  Its
output is explicitly marked non-rigorous because the set-cover matrix uses
binary64 transcendental evaluations.

## Current order-eight prefix

The available packs form `[0,76000)`, not the full `102988` residual census.
They contain 76,000 residual records and 1,064,000 canonical/frontier targets:

```text
shared rational records       75,988
payload-free cycle templates      12
individual/unresolved records       0
common denominator               256
```

The thirteen compressed chunks occupy 21,505,836 bytes and decode to 33,399,474
bytes.  The checked-in manifest currently pins only `[0,36000)` and should be
rebuilt after the four new chunk processes and logs are finalized.
There are 75,940 unique complete shared payloads and 75,873 branch-Gram
signatures at four or six decimal places.  Thus direct witness or rounded-Gram
deduplication is essentially ineffective.

At numerical margin `1e-7`, restricting candidate reuse to the same kernel,
greedy set cover selects 4,683 branch Grams across 232 represented kernels.
It covers all 75,988 strict rows; the 12 uncovered rows are exactly the
payload-free equality templates.  This is a 16.2-fold reduction in strict
branch templates before interval-box merging or support domination, and a much
larger reduction relative to the 1,064,000 target witnesses represented by the
packs.  The largest source-row cost among decoded branch Grams is about
`4.5691112`, so the covered prefix has substantial observed slack; this decimal
is evidence only.

The immediate high-value experiment is therefore not Merkle compression or
exact-payload deduplication.  It is exact interval certification of the 2,612
candidate templates, followed by support-domination pruning and completion of
the remaining order-eight chunks.

## Reproduction

```sh
python3 positive-square-energy/experiments/rank6_order8_template_cover_analysis.py \
  --margin 1e-7 --output /tmp/rank6-order8-cover.json
```

The script reads every currently available `*.r8g.xz` pack.  Pass explicit pack
paths to analyze a pinned subset.
