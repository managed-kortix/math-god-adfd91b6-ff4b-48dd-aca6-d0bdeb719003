# Candidate note: rank-five center with two `C5` bridge arms

Date: 2026-11-25
Status: exact certificate bundle; nonpromotional; no lane-closure claim

## Result and claim boundary

Let

```text
kappa(H) = min_{R PSD, diag(R)=1} sum_{uv in E(H)} 2/(1-R_uv).
```

For a rank-five bridge-free center `C` joined by two bridge edges to two
copies of `C5`, the block-additive DNN route requires

```text
kappa(C)-m(C) <= 6-2(5-2sqrt(5)) = 4sqrt(5)-4.       (1)
```

This bundle proves the following sharply separated statements.

1. **The universal all-center DNN threshold is false.** The order-eight
   multiblock center

   ```text
   C = K4 vee C3 vee C3
   ```

   has `m(C)=12` and exact block-additive `kappa(C)=9+4+4=17`. Hence
   `kappa(C)-m(C)=5`, which violates (1) by
   `9-4sqrt(5)>0`. The integer sign certificate is
   `9^2-16*5=1`. After two `C5` bridge arms, at arbitrary ports including a
   repeated port, the block multiset is unchanged and the same DNN route
   exceeds its rank-seven cap by `9-4sqrt(5)`.

2. **The order-eight minimality statement is conditional on treating the
   standard Graph Atlas census as exhaustive through order seven.** Under
   that external exhaustiveness assumption, the pinned bundled Atlas source
   represents all 1,253 unlabeled simple graphs of orders at most seven. The
   verifier authenticates and parses that source, but does not independently
   prove the Atlas completeness claim. Exact enumeration of the pinned source
   finds 102 simple connected bridge-free rank-five cores: 95 with one
   positive-rank block and 7 multiblock. For every one, the bundle gives a
   rational correlation Gram matrix `R=UU^T` and checks exactly that

   ```text
   sum_edges 2/(1-R_uv) - m < 4sqrt(5)-4.
   ```

   The radical comparison uses no floating point: after writing the rational
   excess as `p/q`, it checks

   ```text
   80q^2-(p+4q)^2 > 0.
   ```

   Therefore none of those 102 cores from the pinned source can obstruct (1).
   The word “smallest” is valid only under the explicit assumption that the
   Graph Atlas source is exhaustive through order seven.

3. **This does not refute the one-positive-rank-block threshold.** The exact
   order-eight witness is multiblock with positive-rank profile `(3,1,1)`.
   All 95 one-positive-block Atlas cores through order seven satisfy (1) by
   explicit rational feasible correlations. No universal claim for larger
   one-positive-block centers is proved here.

4. **This is not a graph-theorem counterexample.** Failure of this particular
   center-only DNN sufficient condition does not imply negative graph surplus.
   The exact witness decomposes into induced owner territories, and structural
   multiblock arguments may absorb the two external pentagon debits. No claim
   of `s+(G)-|V(G)|<0` is made.

## Exact artifacts

- `sources/networkx-3.7-atlas.dat.gz`: pinned Atlas source copied from the
  NetworkX 3.7 distribution.
- `data/atlas-rank5-enumeration.json`: all 153 connected rank-five Atlas
  graphs, their graph6 strings, edges, bridges, articulation data, and block
  scopes; 102 bridge-free cores are selected.
- `data/atlas-rank5-rational-gram-certificates.json`: all 102 rational unit
  vector systems, all 102 explicit rational Gram matrices, each exact edge
  correlation and edge cost, total `Fraction`, and integer radical slack.
- `data/n8-multiblock-route-witness.json`: the exact `K4 vee C3 vee C3`
  center and a representative repeated-port two-`C5` attachment.
- `scripts/construct-certificates.py`: deterministic numerical scout followed
  by exact rational stereographic construction. Floats in this script are not
  trusted for a conclusion.
- `scripts/verify-certificates.py`: dependency-free exact verifier. It rejects
  duplicate JSON keys and scalar type laundering, verifies the strict source
  lock, parses the pinned Atlas source directly, and uses only integers and
  `Fraction`. PSD is certified by checking each stored matrix equals `UU^T`
  over the rationals, with exact unit diagonal. It also executes the exact K4
  and C3 lower witnesses and one-vertex-sum/block-additivity arithmetic.
- `scripts/test-hostile-mutations.py`: fail-closed 18-mutation suite for
  duplicate keys, scalar types, unknown shadow fields, lock closure,
  conditional Atlas wording, local witnesses, and block/route arithmetic.
- `SHA256SUMS`: closed source lock over every bundled artifact except itself.
  Self-inclusion is rejected to avoid a circular hash requirement.
- `output/verify.normal.txt` and `output/verify.optimized.txt`: byte-identical
  successful outputs under normal Python and `python3 -O`.

## Reproduction

Exact verification needs only Python 3:

```bash
python3 scripts/verify-certificates.py
python3 -O scripts/verify-certificates.py
cmp output/verify.normal.txt output/verify.optimized.txt
python3 scripts/test-hostile-mutations.py
```

To regenerate the rational certificates from the pinned Atlas source:

```bash
uv run --with networkx==3.7 --with numpy==2.5.4 --with scipy==1.18.1 \
  python scripts/construct-certificates.py
python3 scripts/verify-certificates.py
```

The constructor's optimizer only locates candidate unit vectors. The verifier
recomputes every certificate conclusion exactly and independently of NumPy,
SciPy, NetworkX, optimizer success flags, and Python assertions.
