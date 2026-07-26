# SUPERSEDED FOR COMPLETENESS: uncut marked-root `T^6P` incidence census

**Date:** 2026-07-26

## Scope and corrected verdict

> **SUPERSEDED -- RESTRICTED LEDGER ONLY.** This `877=868+9` artifact is retained
> to reproduce the old exception list. It is not a proof of `(G6PP)` and its
> E1--E9 follow-up is defective. The proof source is the strict-last-bridge
> `877=861+16` certificate.

**Superseded completeness claim.** This uncut-connector census remains useful
only as an exact `877=868+9` exception list for its restricted ledger. Its
E1--E9 follow-up does not close six rows, so it is not a proof of `(G6PP)`. The
sole authoritative complete proof is the strict-last-bridge `877=861+16`
certificate, which closes `16/16` with no residual.

This is the entry-sensitive census for the disconnected octacyclic row

```text
T^6P_0 | P_1,
```

when `P_0` is an incidence leaf and the external connector to `P_1` enters at
the unique `P_0` cut or through its attached triangular component.  The
executable is

```bash
python research/octacyclic-t6p-marked-root-incidence-census.py
```

It enumerates all 226 color-preserving unrooted `T^6P_0` incidence trees as a
completeness check, retains the 111 trees in which `P_0` is a leaf, and then
marks every orbit of a cyclic-hull entry vertex in the triangular component.
There are exactly 877 marked-root classes.  A conservative packet search using
ordinary triangle interval splits resolves 868 and leaves exactly nine marked
exceptions.

**Connector correction.** The original prose cut the last bridge before
`P_1` and then charged `P_1` to the root-owning interval packet. That packet
would be disconnected, so every one of the 868 accepted rows was invalid under
that instruction. The finite calculation itself has the correct profile: keep
the connector uncut and join its whole territory and `P_1` to the interval
containing the marked root. The lemma below proves that this is an induced
packet of exactly the type charged by the script. Thus the corrected census
still gives `877=868+9`.

This is an exact exception list for the stated packet ledger, not a list of
spectral counterexamples.  In particular, the search deliberately does not use
the rooted hostile-cycle guard theorem or any conclusion derived from it.

## Enumerated objects

The incidence object is a bipartite tree with six interchangeable triangle
nodes `T`, one distinguished pentagon node `P`, and uncolored shared-cut nodes
`X`.  Every cut has degree at least two, triangle degree is at most three, and
pentagon degree is at most five.  Isomorphisms preserve `T/P/X` colors.

The unrooted counts are

| cut nodes `c` | 1 | 2 | 3 | 4 | 5 | 6 | total |
|---:|---:|---:|---:|---:|---:|---:|---:|
| all `T^6P` trees | 1 | 8 | 33 | 73 | 78 | 33 | 226 |
| `P`-leaf trees | 1 | 5 | 20 | 38 | 36 | 11 | 111 |

For each `P`-leaf tree, delete the leaf `P` conceptually.  Its unique cut lies
in a connected six-triangle cactus.  The external entry root may be:

1. any shared cyclic cut of that triangular cactus; or
2. any private triangle vertex.

A triangle of incidence degree `d` has `3-d` private cyclic positions.  At
degree one the reflection fixing the incident cut exchanges its two private
vertices, so they form one marked-root orbit but contribute two positions.  At
degree two there is one private position, and at degree three there is none.
Canonical coding with a root color gives the following exact totals:

| cut nodes `c` | 1 | 2 | 3 | 4 | 5 | 6 | total |
|---:|---:|---:|---:|---:|---:|---:|---:|
| marked-root orbits | 2 | 24 | 126 | 303 | 316 | 106 | 877 |
| cyclic positions before root quotient | 13 | 65 | 260 | 494 | 468 | 143 | 1443 |

The second row counts vertices in one representative of each unrooted
incidence class, with symmetric vertices counted separately.  It is supplied
as a conservative positional audit; 877 is the color-preserving rooted
isomorphism count used by the packet search.  Connector lengths, noncyclic
connector vertices, and arbitrary hanging trees are not finite census
parameters.

## Legal packet test

### Connector-interval lemma

Let `K` be the `T^6P_0` cyclic cluster, let `x` be the marked cyclic entry, and
let `D` be the whole connector territory from `x` through the remote pentagon
`P_1`: the unique `x`--`P_1` block-tree path, `P_1`, and every off-path tree
assigned to that path or to `P_1`. Assume that `D-x` contains no cyclic block
other than `P_1`. Split a router triangle `R` into nonempty proper consecutive
vertex intervals. Let `I_x` be the interval containing `x` if `x` lies on `R`;
otherwise let `Q_x` be the incidence-side packet containing `x`.

Do not delete an edge of the connector. Give `D-x` to `Q_x` when `x` is not
on `R`, and give `I_x union (D-x)` to the remote packet when `x` is private on
`R`. Give every other router interval, incidence branch, and attached tree to
the owner of its attachment. Then the resulting vertex sets are disjoint and
exhaustive, and each induces a connected subgraph. The root packet has exactly
the old root-side cyclic blocks together with `P_1`. If `x` is private on the
sacrificed router, its root interval is acyclic, so that packet has `P_1` as its
only cyclic block. Arbitrary connector length, subdivisions, Steiner branches,
and hanging trees do not alter these conclusions.

Indeed, the block-cut object of a cactus is a tree. Removing the router block
separates its incidence branches, while consecutive intervals partition the
router vertices. Every component outside the cyclic hull has a unique first
attachment to one of these sets, proving disjointness and exhaustion. Adding a
full component at its attachment preserves connectedness and inducedness. The
connector territory meets the clustered cyclic hull only at `x`; hence
adjoining all of `D-x` creates no edge between packet sets and joins `P_1` to
the root interval. All new edges outside `P_1` are bridges. Finally, a proper
interval of the sacrificed triangle is a path or singleton, not a cycle. This
also accounts for the router interval omitted from the incidence-cycle
profile: it survives as attached tree material in its owner, and in the
private-root case specifically in the `P_1` packet.

### Finite test

For each marked object and each triangle `C`, delete the cycle node `C` from
the incidence tree.  Its incidence branches, together with a private root mark
when the root lies on `C`, give two or three distinct marks on the actual
triangle.  Since a triangle has three vertices, every assignment is a proper
consecutive-interval split.  Each path fragment, shared cut, connector remnant,
and hanging tree has one owner.  The resulting territories are induced and
connected.

The connector is left uncut, and the root-owning territory receives the whole
connector territory and the remote pentagon `P_1`. The other territories
retain their incidence branches. Acceptance
uses only these established packets:

```text
A_r=T^r:       sigma > 0,1,2,3,2,1 for r=1,...,6;
P:             sigma > -1/4;
TP:            sigma > 3/4;
connected PP:  sigma >= 0;
rank 2 or 3:   sigma >= 0;
rank 4--7:     sigma > 0;
common-cut TTP and shared-pair TTTP refinements from the prior ledger.
```

All arithmetic is exact `Fraction` arithmetic.  A split is accepted only when
the rational sum is positive, or is zero with a strict summand.  Qualitative
rank-seven positivity is never used to pay either `1/4` or an opening cost.
No rooted theorem, rooted quantitative margin, direct spectral comparison, or
multi-cycle sacrifice is admitted.

The executable also audits the former bad instruction. Canonically identify a
rooted row by

```text
cut-count<TAB>unrooted-incidence-signature<TAB>rooted-signature.
```

Exactly all 868 formerly accepted rows are invalid if the last connector
bridge is cut. Their cut-count distribution is

```text
c=1,2,3,4,5,6: 0,21,123,302,316,106.
```

The SHA-256 of their sorted newline-terminated canonical IDs is

```text
aa2ba3d1c606483ed2a04142df1a26c8443b6958120704515e01113b3469a8f2.
```

Run `python research/octacyclic-t6p-marked-root-incidence-census.py
--list-invalid-rows` for all exact IDs. The uncut-connector audit repairs all
868 and checks 2,036 accepted router certificates. Of the repaired rows, 133
admit a certificate sacrificing the private-root router, distributed
`4,19,46,47,17` for `c=2,...,6`; exactly nine rows require such a certificate,
distributed `4,3,2` for `c=2,3,4`. In every such certificate the script asserts
the additional `(0,1)` profile: the sacrificed root interval plus connector
and `P_1` is a one-pentagon packet, not an omitted vertex set.

The result is

| cut nodes `c` | 1 | 2 | 3 | 4 | 5 | 6 | total |
|---:|---:|---:|---:|---:|---:|---:|---:|
| all marked roots | 2 | 24 | 126 | 303 | 316 | 106 | 877 |
| packet-resolved | 0 | 21 | 123 | 302 | 316 | 106 | 868 |
| exceptions | 2 | 3 | 3 | 1 | 0 | 0 | 9 |

## Exact exceptions

Labels in the executable representatives are `0,...,5=T`, `6=P`, and cuts
begin at `7`.
`R` in a signature marks either a cut (`R(...)`) or a private triangle vertex
(`TR(...)`).  A private orbit's `positions` multiplicity counts all symmetric
private vertices represented by that rooted code.

### `c=1`: common-cut bouquet

```text
edges: ((0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7))

E1 root cut 7, positions=1:
   R(P()T()T()T()T()T()T())
E2 root private on a triangle, positions=12:
   X(P()T()T()T()T()T()TR())
```

### `c=2`: hub-tail and pentagon-hub forms

```text
edges: ((0,7),(0,8),(1,7),(2,7),(3,7),(4,7),(5,7),(6,8))

E3 root hub cut 7, positions=1:
   T(R(T()T()T()T()T())X(P()))
E4 root private on a hub-leaf triangle, positions=10:
   T(X(P())X(T()T()T()T()TR()))

edges: ((0,7),(0,8),(1,7),(2,8),(3,7),(4,7),(5,7),(6,7))

E5 root private on the saturated router triangle 1, positions=1:
   TR(X(P()T()T()T()T())X(T()))
```

### `c=3`: saturated router forms

```text
edges: ((0,7),(0,8),(0,9),(1,7),(2,8),(3,7),(4,7),(5,7),(6,9))

E6 root hub cut 7, positions=1:
   T(R(T()T()T()T())X(P())X(T()))
E7 root private on a hub-leaf triangle, positions=8:
   T(X(P())X(T())X(T()T()T()TR()))

edges: ((0,7),(0,8),(1,7),(1,9),(2,8),(3,7),(4,7),(5,7),(6,9))

E8 root private on router triangle 0, positions=1:
   X(T()T()T()T(X(P()))TR(X(T())))
```

### `c=4`: double-router form

```text
edges: ((0,7),(0,8),(0,10),(1,7),(1,9),(2,8),(3,7),(4,7),(5,9),(6,10))

E9 root private on router triangle 1, positions=1:
   X(T()T()T(X(P())X(T()))TR(X(T())))
```

No exception has five or six cut nodes.  The nine rooted classes arise from
five unrooted incidence trees; the root distinguishes entry behavior that the
111-tree unmarked census cannot see.

## Interpretation

The computation closes every marked cyclic entry except E1--E9 by a legal
induced packet decomposition under established unrooted packet bounds.  It
does not prove those nine cases false or open in an absolute sense.  It says
precisely that the admitted ordinary one-triangle ledger does not prove them.

Any claimed resolution of E1--E9 must therefore provide an independently valid
quantitative rooted estimate, a direct nonadditive spectral argument, or a
broader legal decomposition.  An invalid rooted theorem cannot be used to
erase these exceptions, and this certificate intentionally makes no such use.
