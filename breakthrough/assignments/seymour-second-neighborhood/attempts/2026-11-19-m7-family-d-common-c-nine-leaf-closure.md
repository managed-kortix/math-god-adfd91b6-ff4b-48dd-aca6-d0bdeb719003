# Conditional finite closure of the three common-`C` family-D cells

## Scope

This note closes only the common inaccessible-pair branch `C_u=C_v=C` of the
disjoint-low witness family, after the earlier reduction to

```
(x,z,h)=(0,0,2), (0,1,1), (1,0,1).
```

It is a finite conditional lemma under that normal form.  It is **not** a proof
of the whole `m=7` case and is not Seymour's conjecture.  No arc-minimality
clause is used in the formulas below.

## Exact overlap-orbit lemma

Let `S_u={u} union A_u`, `S_v={v} union A_v`, where both rooted sets have size
nine and `|S_u intersect S_v|=8`.  Therefore

```
P=S_u\S_v, Q=S_v\S_u
```

are singletons.  The selected witness arcs give `r in A_u` and `q in A_v`.
There are three possibilities for the root pair.

1. `u->v`.  Then `v in S_u intersect S_v`, while the reverse arc is forbidden,
   so `u notin A_v`.  Exact `t=8` forces `P={u}`.  Since `q in S_v`, either
   `q` lies in the intersection, in which case `u->q`, or `Q={q}` and
   `u !-> q`.  The high `r` cannot be `Q`, because `r in S_u`; hence
   `r in S_v`, so `v->r`.  Thus the two subtypes are:

   * both cross-high arcs `u->q` and `v->r`;
   * exactly one cross-high arc, here `v->r`.

2. `v->u` is the exchanged version of case 1.

3. Neither root arc is present.  Then exact rooted layers put `v in B_u` and
   `u in B_v`; hence `P={u}`, `Q={v}`.  Both highs lie in the eight-element
   intersection, so both cross-high arcs `u->q`, `v->r` are present.  The root
   pair is a hole.

The alternatives are disjoint by the root-pair status and cross-high-arc
status.  Exchanging the rooted pairs

```
(u,r) <-> (v,q)
```

preserves every hypothesis: the two selected robustness equalities are
exchanged; the universal statement that no low vertex robustly witnesses both
highs is unchanged; and `C`, `T=V\C`, `S_u union S_v`, and therefore
`W=V\(C union S_u union S_v)` are transported to themselves.  Consequently
all three aggregate quantities

```
x=e(C,W), z=h(C,W), h=h(T)
```

are invariant.  Hence, up to this exchange, there are exactly three overlap
types: `oriented-both`, `oriented-one`, and `root-hole`.

The independent enumerator

```
python3 experiments/m7_family_d_common_c_cover.py
```

constructs the entire labelled rooted-set universe rather than trusting this
count.  It finds 13,860 labelled states and 7,392 orbits under the root
exchange alone, split exactly as follows:

```
                     labelled       orbits
oriented-both          11,088         5,544
oriented-one            1,848           924
root-hole                 924           924
```

It then quotients by all permutations of the twelve ordinary low labels as
well as the root exchange and obtains exactly the three canonical orbit keys
used by the CNF producer.  It compares exact labelled-state/orbit sets and
exact root/cross-high signatures, not merely their cardinalities, and explicitly
checks that the opposite placement of the one cross-high arc is the exchanged
copy of `oriented-one`.

## Nine exact formulas

Cross the three aggregate cells with the three overlap types.  Each of the nine
CNFs imposes:

* looplessness and no digons;
* exact outdegrees nine at `r,q` and eight at every low vertex;
* exactly seven holes;
* biconditional exact-distance-two variables for every ordered pair;
* strict global badness `d++(a)<d+(a)` at every vertex;
* both exact rooted rows with `C_u=C_v={16,17}` and `t=8`;
* the selected arcs `u->r`, `v->q`;
* both exact vertex-deletion equalities
  `N++_{D-r}(u)=N++_D(u)` and `N++_{D-q}(v)=N++_D(v)`, with the deleted high
  removed from the comparison domain;
* the universal family-D condition: for every one of the sixteen low vertices
  `a`, it is not the case that `a` is tight and robustly witnesses both high
  vertices;
* one exact aggregate triple.

The producer is `m7_family_d_common_c_cnf.py`.  The checker
`check_m7_family_d_common_c_cnf.py` imports neither that producer nor
`snc_cnf`; it independently reconstructs the bytes, hostile-parses DIMACS, and
requires exact equality.  `m7_family_d_common_c_semantic_tests.py` separately
truth-tables the exact-`N++` biconditional, both directions of deletion
preservation, the universal no-shared-low predicate (including a weakening
mutation), and the aggregate arithmetic.  No formula contains arc minimality.

## Certified result and replay

CaDiCaL source commit
`38e073b389a877b0a0d3c91136d2443ab95fdeba` generated a DRAT proof for every
leaf.  Its campaign binary SHA-256 is recorded in the manifest.  Every proof is
independently accepted by `drat-trim` source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; the pinned checker binary SHA-256
is

```
92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a.
```

The manifest authenticates the exact nine proof files, regenerated CNF bytes,
compressed proof bytes, and decompressed raw proof bytes.  The verifier uses
explicit exceptions rather than Python `assert` and replays all nine proofs.
The natural in-tree replay command is, from the `experiments` directory,

```
python3 verify_m7_family_d_common_c_campaign.py \
  --manifest ../certificates/m7-family-d-common-c/manifest.json \
  --proof-dir ../certificates/m7-family-d-common-c \
  --drat-trim /path/to/pinned/drat-trim \
  --cnf-checker ./check_m7_family_d_common_c_cnf.py
```

When the manifest is inside the proof directory, it is the sole permitted
non-proof file; every other unexpected directory entry is rejected.

Thus all nine leaves are UNSAT, conditionally eliminating exactly the three
common-`C` family-D residual cells and nothing beyond them.
