# Hostile audit verdict: connected rank-nine cacti

**Date:** 2026-07-26

## Verdict

**ACCEPT, with the dependency boundary stated below.** The current artifact set
does prove that every connected cactus of cyclomatic rank nine satisfies

```text
s+(G)>|V(G)|.
```

The controlling artifact is
`research/nonacyclic-cactus-complete-synthesis-2026-07-26.md`. Earlier status
notes and the local census notes deliberately decline to claim the global
theorem; those scope disclaimers are not gaps once the later synthesis supplies
the exhaustion map. The four principal exact certificates reproduce, and the
two-pentagon coefficient certificate reproduces in the repository's SymPy
environment.

This verdict rejects any use, explicit or disguised, of the open two-pivot
winding theorem. The accepted proof does not need it: every two-interface
rank-nine kernel is converted by finite router splits or a pentagon opening into
one-pivot or already proved packets.

## 1. Reproduction

The following exact certificates ran successfully:

```bash
python3 research/rank-nine-cactus-residual-census.py
python3 research/nonacyclic-t7p-last-bridge-conservative.py
python3 research/nonacyclic-t7-two-interface-census.py
python3 research/nonacyclic-t7pp-seven-exceptions-resolution.py
/tmp/opencode/octacyclic-cacti-venv/bin/python \
  positive-square-energy/experiments/c5_bouquet_matching_certificate.py
```

They reproduce:

1. the two sharp-DNN residual families `T^8Q` and `T^7PP`;
2. the disconnected partition counts `67/66/63/3` and `118/117/109/8`;
3. the fully shared `T^8Q` counts in every capacity regime;
4. the fully shared `T^7PP` count `8004=7997+7`;
5. all 3188 entry-locked `T^7P|P` marked classes, with `3150+38` certificates
   and zero failures;
6. all 3188 labelled `P|A_7|P` classes, with 3182 ordinary-router acceptances
   and six explicit bouquet repairs; and
7. the 1290-term nonnegative coefficient certificate underlying the scalar
   common-cut two-pentagon bound, with the frozen SHA-256 digest.

These programs certify finite enumeration and ledger claims. The analytic
packet inequalities remain mathematical inputs proved in their cited notes;
the audit does not mistake finite enumeration for an independent spectral
proof.

## 2. Global exhaustion

The sharp-DNN calculation is exact. For rank nine,

```text
sigma(G)>=8-sum_i epsilon_(l_i),
```

and the symbolic comparisons leave exactly

```text
T^8Q,       q>=3,
T^7PP.
```

Every other cycle multiset is strictly positive before incidence or connector
data enter.

For either residual multiset, contracting maximal shared-cut cyclic clusters
while retaining actual bridge connectors gives a tree. This creates an
exhaustive dichotomy:

1. more than one shared-cut cluster; or
2. one fully shared cluster containing all nine cyclic blocks.

The disconnected color census does not itself enumerate tree topology, but the
subsequent reduced-tree argument is sufficient. If a singleton triangle is a
leaf, cutting the first actual bridge gives a strict triangle and a strict
octacyclic complement. If no singleton triangle is a leaf, only the two
distinguished endpoint clusters can be leaves; a finite tree with exactly those
two leaves is their path. Pairing the singleton triangle nearest a distinguished
pentagon or `Q` gives a positive `TP` or `TQ` terminal packet and a strict
lower-rank complement. This is the same proved actual-bridge lemma used at lower
ranks, and it is insensitive to connector length and internal cluster
incidence.

After this pruning, the only disconnected endpoints are

```text
A_8|Q,
T^7P_0|P_1,
P_0|A_7|P_1.
```

Sections 5 and 6 of the complete synthesis map these endpoints to the exact
finite certificates. The fully shared side maps directly to the exhaustive
colored incidence censuses. No residual topology is omitted.

## 3. `T^8Q` attack

### Disconnected `A_8|Q`

Project the connector to its first cyclic-hull entry. In a nonbouquet
eight-triangle incidence tree, an internal triangle supplies a legal router.
A triangle has at most three occupied cyclic marks, including a private entry.
If the `Q` territory retains `k` triangles, the cases are exhaustive:

```text
k=1:       TQ is strict;
k=2:       TTQ is nonnegative and another triangular branch is strict;
3<=k<=7:  the retained lower-rank packet is strict;
k=0:       seven triangles occupy at most two branches, so one has at least
           four triangles and surplus >3, absorbing Q>-1.
```

If no internal triangle exists, the connected bipartite incidence tree has one
cut and is a bouquet. All eight triangles contain one hub, so their packing
number is one. The one-hostile-cycle theorem allows a direct attachment or an
arbitrary joining path and gives `sigma>8-delta_q>0`. Nonhostile `Q` is easier.

### Fully shared `T^8Q`

The exact incidence census stabilizes at `Q` capacity eight because only eight
other cycle nodes exist. Ordinary splitting leaves the common-cut bouquet and,
for the hostile ledger, one two-cut router shape. In both, all eight triangles
contain one hub. The former uses the scalar common-cut theorem; the latter uses
the one-hostile-cycle packing-one theorem. Both have margin
`>8-delta_q>0`.

Thus all `T^8Q` cases close without a two-interface estimate.

## 4. Disconnected `T^7PP`: both 3188 censuses

The two occurrences of 3188 count different spaces and are correctly kept
separate.

### Entry-locked `T^7P|P`

The first 3188 are one-entry marked orbits on incidence-leaf `T^7P` clusters.
The verifier checks 3150 direct one-router certificates and 38 finite
replacements. It checks legal split order, connected retained components,
common-cut/shared-cut hypotheses, both pentagonal deficits, private-entry
costs, and exact positivity. There are no failed rows. The weakest margin is

```text
1-2delta=5-2sqrt(5)>0.
```

The ordinary cases excluded before this census are legitimate pentagon
interval splits: an internal clustered pentagon has distinct incidence marks,
and a leaf pentagon entered privately has its incidence cut and entry as two
distinct marks. The connector follows the entry interval. No graph-level entry
case disappears between this reduction and the marked census.

### Two labelled interfaces on `A_7`

The second 3188 are ordered two-interface classes on 48 pure seven-triangle
incidence trees, obtained from 10800 labelled placements before automorphisms.
The interface universe includes every shared cut and every actual private
triangle vertex; labels may coincide. Frozen canonical digests reproduce.

The uniform router automaton accepts 3182 rows with score at least one, so each
has margin `>1-2delta`. The six residuals are exactly the six bouquet orbits:

| interfaces | replacement | margin |
|---|---|---:|
| hub, hub | open one remote pentagon; retain the other packing-one arm | `>6-delta` |
| hub, private, either order | `P +` common-cut `T^6P` | `>6-2delta` |
| coincident private | `A_6+PP` | `>1` |
| two private vertices on one triangle | `A_6+P+P` | `>1-2delta` |
| private vertices on two triangles | `A_5+P+P` | `>2-2delta` |

The executable's repair function records rather than reconstructs these six
packetizations, so its headline should not be read as a machine proof of their
analytic hypotheses. The accompanying proof supplies those checks: private
intervals retain their connector paths and pentagons; coincident entries form
one connected `PP` packet; and the hub-hub opening charges one exact tree cost
`-1` while leaving seven pairwise intersecting triangles and one hostile arm.
That hand proof is sufficient and uses only established packets.

## 5. Fully shared `T^7PP`: all seven exceptions

The exact census gives

```text
8004 total = 7997 ordinary-split safe + 7 exceptions.
```

The replacement verifier regenerates the seven exact signatures and edge
representatives. For the six router/common-cut rows it checks interval sizes,
sequential branch refinement, connected retained packets, shared-cut
hypotheses, unique cut ownership, and exact radical ledgers.

The genuinely new row `F9` has seven triangles and `P_0` sharing hub `x`, while
leaf pentagon `P_1` meets `P_0` at a second cut `y`. Splitting the router
pentagon is correctly rejected because it yields only `A_7+P_1>-delta`.
Opening the leaf pentagon instead gives

```text
sigma(G)>=sigma(common-cut T^7P_0)+sigma(P_1-y)
        >(7-delta)-1
         =6-delta
         =8-sqrt(5)>0.
```

The ownership proof keeps `y`, `P_0`, all triangles, and branches rooted there
in the common packet; the four private vertices of `P_1` and branches rooted at
them form one nonempty tree. No cut is duplicated and no opening charge is
omitted.

The weakest margins among the remaining replacements are still positive:

```text
1-2delta,
2-2delta,
3-2delta,
6-2delta,
8-4/(3sqrt(13)).
```

No packet margin is spent twice.

## 6. Connectors, entries, and arbitrary trees

The proof does not contract a connector and then forget its vertices. Every
global separation occurs at an actual bridge. Connector remnants and branches
on them stay with an endpoint territory.

At a triangle router, two marks produce a singleton and complementary-edge
interval; three marks produce three singleton intervals. Each incidence branch
and private connector follows its mark. A later router split refines one
already induced territory. Every off-hull tree has one hull attachment and
follows that attachment's owner. These operations produce connected, induced,
disjoint, exhaustive territories.

The scalar common-cut theorem is uniform over arbitrary rooted trees. The
packing-one theorem is uniform over arbitrary joining paths and trees attached
at core or path vertices. The two explicit pentagon openings assign every tree
at an opened private vertex to the opened tree territory and keep trees at the
retained cut with the cyclic packet.

Accordingly, arbitrary connector lengths, cyclic-hull entry positions,
coincident entries, entries through rooted branches, and arbitrary finite tree
attachments are covered rather than inferred from a bare incidence count.

## 7. Two-pivot winding firewall

`research/two-pivot-schur-sachs-triangular-cactus-2026-07-26.md` proves an exact
two-terminal state reduction but explicitly leaves the winding-sensitive
integrated inequality open. Its obstruction example shows why principal
`atan`, entrywise-positive transfers, and two scalar rooted ratios cannot prove
the target. None may be imported into the rank-nine theorem.

The accepted dependency graph avoids that open statement:

- arbitrary nonbouquet two-interface cores are closed by finite router splits;
- five bouquet interface types reduce to common-cut, `PP`, or separate
  pentagon packets;
- the hub-hub bouquet opens one pentagon and applies a one-hostile-arm theorem;
- `F9` opens its leaf pentagon and applies a scalar common-cut theorem; and
- the entry-locked family has its own exact finite marked-entry certificate.

Any alternative proof asserting direct phase control for an unsplit arbitrary
`P|A_7|P` core must still be rejected as hidden use of the unproved winding
theorem. The current synthesis makes no such assertion.

## Final finding

The hostile attacks do not expose an uncovered rank-nine class, an unpaid tree
cost, a duplicated interface, a nonpositive terminal ledger, or a dependency
on two-pivot winding. The finite certificates and the graph-level synthesis
together establish the universal connected rank-nine cactus theorem.
