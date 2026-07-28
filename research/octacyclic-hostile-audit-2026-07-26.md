# Hostile audit of the corrected octacyclic synthesis

**Date:** 2026-07-26

## Verdict: ACCEPT

The corrected artifacts prove that every connected octacyclic cactus `G`
satisfies

```text
s+(G)>|V(G)|.
```

The proof does not use the then-retracted, now restored, all-rank rooted
hostile-cycle guard. Its
hostile packing-one input is the standalone theorem in
`research/octacyclic-packing-one-hostile-cycle-lemma-2026-07-26.md`. In its sole
application, the seven retained triangles form a common-cut bouquet, so their
vertex-packing number is visibly one.

## Exhaustion trace

1. The sharp DNN estimate leaves exactly `T^7Q` and `T^6PP`.  The inequalities
   `3 epsilon_5<2`, `2 epsilon_5>1`, and
   `epsilon_5+epsilon_7<1` separate every other eight-cycle multiset.
2. For a disconnected shared-cut graph, the exact colored partition census
   returns `45/44/42` for `T^7Q` and `77/76/70` for `T^6PP`.  Reduced-tree
   leaf/path arguments reduce the exceptional rows to `T^7|Q` and
   `T^6P_0|P_1`; the apparent `P_0|T^6|P_1` row has ledger
   `>1-2delta>0`.
3. Every nonbouquet `T^7|Q` incidence has a legal internal-triangle interval
   split.  A private-entry bouquet gives `A_6+Q>1-delta_q`.  The one locked
   common-cut entry is itself a packing-one seven-triangle lobe, so the valid
   packing-one Sachs lemma gives `sigma>7-delta_q>0` for hostile `Q`.
4. In disconnected `T^6P_0|P_1`, internal `P_0` and private-`P_0` entry cases
   split directly.  The remaining marked triangular-entry class is exhausted
   by the strict-last-bridge `877=861+16` certificate described below.
5. For a fully shared `T^7Q` cluster, the incidence census resolves every
   nonbouquet type.  The unique bouquet is covered by the independent scalar
   common-cut Schur--Sachs theorem.
6. For a fully shared `T^6PP` cluster, the census gives
   `2116=2110+6`.  The common-cut theorem closes U1 and the five direct router
   packetizations close U2--U6.

These cases partition the structural possibilities: the shared-cut graph is
either disconnected or consists of one cluster, and the DNN step already
removed every nonresidual cycle multiset.

## Root-class audit

The disconnected `G6PP` census first reproduces all 226 unrooted `T^6P_0`
incidence trees and all 111 classes with `P_0` an incidence leaf.  It then marks
every cyclic-hull entry in the attached six-triangle component:

```text
cut roots:             every shared cyclic cut, including the P_0 cut;
private roots:         every private triangle position;
marked root orbits:    877;
labelled positions:    1443.
```

A degree-one triangle's two private vertices form one rooted core orbit but
carry positional multiplicity two; degree-two triangles contribute their one
private vertex; saturated triangles have no private vertex.  This loses no
root class.  Private vertices of `P_0` were already removed by the direct
two-mark `P_0` split.  Connector-internal vertices and off-hull tree vertices
are not missing finite classes: projection to the first cyclic-hull attachment
puts the whole connector/tree remnant under that marked owner's arbitrary-tree
hypothesis.

Under the authoritative strict-last-bridge convention, the conservative search
resolves 861 marked classes and leaves exactly 16, with cut-count distribution
`(2,5,5,4,0,0)`. No five- or six-cut root class is exceptional. The distinct
`868+9` counts belong only to the superseded uncut-connector ledger.

## Strict-last-bridge packet trace

The former uncut E1--E9 completeness claim is defective and superseded. Under
the strict-last-bridge convention, every retained cycle occurs in exactly one
packet, every unsplit shared cut has at most one retained owner, and all 16
conservative failures close with no residual. The verified final ledgers are:

| classes | final cyclic packets, including remote `P_1` | surplus |
|---|---|---:|
| L1--L2 | common-cut `T^6P_0 + P_1` | `>6-2delta` |
| L3--L6 | `T +` common-cut `T^4P_0 + P_1` | `>4-2delta` |
| L7 | `T +` common-cut `T^4P_0 + P_1 + E` | `>3-2delta` |
| L8--L10, L12--L16 | two triangles plus mixed packet and `P_1` | `>2-2delta` |
| L11 | `T + T +` common-cut `T^2P_0 + P_1 + E` | `>1-2delta` |

Here L13--L16 use the shared-cut `TTP>2-delta` bound: the two triangles
share a cut, but the pentagon need not share that same cut. The weakest exact inequality is
`1-2delta=5-2sqrt(5)>0`.

## Six-exception packet trace

The six fully shared exceptions printed by the independent 2116-class census
match U1--U6 in the replacement note.  Their incidence edges support exactly
the stated operations:

| code | operation and retained packets | surplus |
|---|---|---:|
| U1 | retain common-cut `T^6PP` | `>7-4/(3sqrt(13))` |
| U2 | split one binary router: `P +` common-cut `T^5P` | `>5-2delta` |
| U3 | split one saturated router: `P + T +` common-cut `T^4P` | `>4-2delta` |
| U4 | split two binary routers: `P + P + A_4` | `>3-2delta` |
| U5 | saturated then binary: `P + P + T + A_3` | `>2-2delta` |
| U6 | split two saturated routers: `P + P + T + T + A_2` | `>1-2delta` |

For a binary triangle, the pentagon-side mark owns one singleton vertex and
the other mark owns the complementary edge.  For a saturated triangle, its
three cuts occupy the three distinct vertices and force three singleton
intervals.  The hub cut has one owner after each refinement, each pentagon cut
stays with its pentagon, and split-router remnants retain no cycle.  Therefore
the packetizations are valid for every cyclic order and arbitrary attached
trees, not only for the printed representatives.

## Dependency audit

| theorem input | publication source |
|---|---|
| strict disconnected `G6PP` | `research/octacyclic-t6p-last-bridge-conservative-resolution-2026-07-26.md` (`877=861+16`) |
| packing-one hostile `G7Q` | `research/octacyclic-packing-one-hostile-cycle-lemma-2026-07-26.md` |
| common-cut bouquets | `research/common-cut-bouquet-rooted-schur-2026-07-26.md` |
| fully shared two-pentagon family | `research/octacyclic-fully-shared-incidence-census-2026-07-26.md` plus `research/octacyclic-t6pp-six-exceptions-resolution-2026-07-26.md` (`2116=2110+6`) |

`TTP` in the strict certificate denotes two triangles sharing a cut together
with a pentagon in the same connected packet; the pentagon need not share that
cut. This is distinct from common-cut `T^2P`, where all three cycles share one
pivot.

The proof uses the following quantitative packets and no stronger hidden
claim:

```text
rank 2--3 nonnegativity; rank 4--7 strict positivity;
A_r margins (0,1,2,3,2,1,0), r=1,...,7;
P >= -delta, Q >= -delta_q, TP > 1-delta;
the established small mixed packets used by the conservative censuses;
the valid packing-one hostile Sachs lemma only for G7Q;
the independent common-cut Schur--Sachs T^kQ and T^kPP bounds.
```

The four unresolved kernels R1--R4 belong to the stronger universal rooted
six-triangle target.  They are not used in the global proof.  The nine E-kernels
have empty canonical overlap with R1--R4, and their direct packetizations do not
assert or require a rooted estimate for those four kernels.

## Reproduction

The following certificates ran successfully from the repository root:

```text
octacyclic-disconnected-partition-census.py: 45/44/42 and 77/76/70;
octacyclic-fully-shared-incidence-census.py: all stated T^7Q counts and
  T^6PP=2116=2110+6;
octacyclic-g6pp-last-bridge-census.py: 226, 111, 877=861+16, residual 0;
octacyclic-t6p-last-bridge-sixteen-resolution.py: closed 16/16;
octacyclic-g6pp-last-bridge-four-resolution.py: shared-cut crosscheck 4/4;
octacyclic-rooted-six-triangle-certificate.py: 107/111 and four R-kernels;
c5_bouquet_matching_certificate.py: PASS, 1290 nonnegative terms,
  sha256=4c436cac772395d2a8edfdd81408ffe426759d3e94d66df2e4ab0235a3343110;
octacyclic-t6p-rooted-activity-certificates.py: completed and reproduced the
  documented failures of stronger coefficientwise rooted certificates;
compileall over research and positive-square-energy/experiments: PASS.
```

SymPy was absent from the base environment, so the bouquet certificate was run
with SymPy 1.14 installed under `/tmp/opencode/audit-sympy`; no repository or
global environment file was changed.

The strict-last-bridge artifacts are the sole authoritative complete `(G6PP)`
proof. The uncut E1--E9 artifacts are retained only as superseded audit history
and are not proof dependencies.
