# Physical rank-(6,1) bridge theorem with a single rank-six cyclic block

## Exact theorem and scope

For a finite graph `H`, write

```text
s+(H) = sum_{lambda_i(H)>0} lambda_i(H)^2,
sigma(H) = s+(H)-|V(H)|,
beta(H) = |E(H)|-|V(H)|+1                 (H connected).
```

**Theorem (R61-PHYSICAL-SINGLE-BLOCK).** Let `G` be finite, simple, and
connected. Suppose `xy` is an actual bridge and

```text
G-xy = R disjoint-union U,
x in V(R), y in V(U), beta(R)=6, beta(U)=1.
```

Assume that `R` has exactly one positive-rank cyclic block. Equivalently, its
unique cyclic block is a simple positive-length subdivision of a loopless
2-connected rank-six kernel, and all material outside that block consists of
finite rooted trees attached at unique vertices. No restriction is placed on
the bridge ports `x,y`; either may lie in any attached tree. Then

```text
s+(G) >= |V(G)|.                                           (1)
```

An arbitrary bridge chain is included: choose any edge on the chain whose
removal has side ranks `6|1`; the two remaining chain portions are ordinary
tree material on the two sides.

This theorem is deliberately narrow. It does **not** assert a theorem for a
rank-six side with several positive-rank cyclic blocks, a shared-cut `R61`
configuration, a connector meeting a side more than once, several rank-one
arms, all physical `R61`, all multiblock heptacyclic graphs, or all
heptacyclic graphs. It does not assert strictness in every case.

The normative machine-readable scope is
`research/fixtures/r61-physical-single-block-theorem-manifest.json`.

## Imported analytic facts

The proof uses the following established facts with exactly the displayed
contracts.

1. **DNN inequality and additivity.** For

   ```text
   kappa(H)=min_{C psd, C_vv=1} sum_{uv in E(H)} 2/(1-C_uv),
   ```

   one has `s-(H)<=kappa(H)`. The constant is additive under a genuine
   one-vertex sum, and `kappa(T)=|E(T)|` for every tree `T`.
2. **Induced superadditivity.** If the original vertices are partitioned as
   `V(G)=V_1 dot-union ... dot-union V_r`, then

   ```text
   sigma(G) >= sum_i sigma(G[V_i]).                         (2)
   ```

   Every nonempty tree has `sigma=-1`.
3. **Unicyclic DNN bound.** If `U` is connected and unicyclic and its unique
   cycle has length `q`, then

   ```text
   kappa(U) <= |E(U)|+epsilon_q,
   epsilon_q = 0                              (q even),
   epsilon_q = q tan^2(pi/(2q)) <= 1          (q odd).       (3)
   ```

   Tree attachments are included by one-vertex additivity. Consequently the
   weaker standard floor `sigma(U)>=-1` is always available.
4. **Rooted actual-`K4` packet.** A connected induced territory whose unique
   positive-rank block is a literal, unsubdivided `K4`, with arbitrary finite
   rooted-tree material attached at its vertices, has

   ```text
   sigma > 2.                                               (4)
   ```

5. **Typed rank-six owner theorem.** The all-length rank-six single-block
   families are the disjoint union of ordinary DNN owners and exactly three
   structural schemas: `K110-0`, `K110-1`, and `K223`. The DNN owners satisfy
   `kappa(R)<=|E(R)|+5`. The structural schemas are described below. The owner
   adapter authenticates the established orders-2--10 master; its committed
   child-execution records are execution attestations, not fresh replays of
   every underlying segment.

The verifier digest-authenticates these analytic sources and exactly checks the
finite and affine consequences used here. A SHA-256 digest authenticates bytes;
it does not by itself reprove an analytic statement.

## DNN-owner lane

Put `m_R=|E(R)|`, `m_U=|E(U)|`, and `m_G=m_R+m_U+1`. If `R` is DNN-owned,
then (3), the exact bridge-`K2` cost one, and one-vertex additivity give

```text
kappa(G)
 <= (m_R+5) + 1 + (m_U+epsilon_q)
 <= m_R+m_U+7
  = m_G+6.                                                  (5)
```

Because `beta(G)=7`, the Euler identity is

```text
|V(G)|=m_G-6.                                               (6)
```

Using `s+(G)+s-(G)=2m_G` and `s-(G)<=kappa(G)`, equations (5)--(6) yield

```text
s+(G) >= 2m_G-kappa(G) >= m_G-6 = |V(G)|.                  (7)
```

Both ports are irrelevant to this calculation. In particular, the bridge is a
genuine one-vertex sum of `R`, a `K2`, and `U`; no endpoint is copied.

## Uniform port-blind structural lane

The three structural owners admit one common proof. Keep the complete rank-one
side `U` intact as one induced territory. On the rank-six side choose a fixed
literal `K4` territory `A` and its fixed complementary nonempty tree territory
`T`. Every rooted tree follows the core vertex (or internal subdivision vertex)
where it is attached. Leave every edge from `A` to `T`, and the physical bridge
`xy`, as crossing edges of the induced partition. This remains valid no matter
whether `x` lies in `A`, in `T`, or anywhere in rooted-tree material: the bridge
simply crosses from whichever rank-six territory owns `x` to the intact `U`
territory.

Thus no bridge-port projection, root orbit, rank-one port, cycle length, tree
shape, or endpoint degree is an input to the selector. Equations (2)--(4) give
the same strict ledger in every structural family:

```text
sigma(G) >= sigma(A)+sigma(T)+sigma(U) > 2-1-1 = 0.         (8)
```

The strictness comes only from the rooted actual-`K4` packet. The standard
nonstrict unicyclic floor `sigma(U)>=-1` is enough; no stronger `q`-dependent
spectral estimate is used in this branch.

### `K110-0`

The cyclic core is the actual `K5` on vertices `0,1,2,3,4`. Use the fixed
partition

```text
A={0,1,2,3},       T={4}.                                  (9)
```

`A` induces a literal `K4`; the one-vertex territory `T`, with all tree material
rooted there, is a nonempty tree. All four `K5` edges between `A` and `T` are
crossing edges. The choice is independent of `x`.

### `K110-1`

Write the unique long odd path as

```text
P: a=v_0,v_1,...,v_ell=b,      ell=2h+1>=3,
```

and call the other three `K5` branch vertices `c,d,e`. The other nine branch
paths are unit edges. Use the fixed partition

```text
A={b,c,d,e},       T={v_0,...,v_(ell-1)}.                  (10)
```

`A` induces a literal `K4`. The induced graph on `T` is the path obtained from
`P` by omitting `b`; it has `ell` vertices and `ell-1` edges and is therefore a
nonempty tree. Edges from `a=v_0` to `c,d,e` cross the partition. The formulas
are symbolic in `h>=1`; no bounded length sample or port orbit is used.

### `K223`

In lexicographic pair order

```text
01,02,03,04,05,12,13,14,15,23,24,25,34,35,45,
```

the row `001111011011111` has edge set

```text
03,04,05,12,14,15,24,25,34,35,45.
```

Use the fixed partition

```text
A={0,3,4,5},       T={1,2}.                                (11)
```

`A` induces a literal `K4`, and `T` induces the edge `12`. The four edges
`14,15,24,25` cross between the two territories. Again, the choice is
independent of `x`. The automorphism group and its two vertex orbits are checked
only as a graph-identity guard; they play no role in selecting (11).

## Completeness of the owner split

The typed owner adapter preserves the exact established all-length rules.

* For all-odd `K110`, zero long paths give `K110-0`, exactly one long path gives
  `K110-1`, and at least two long paths are DNN-owned: choose two long edges,
  use the exact strict incident/disjoint two-edge certificate, and apply
  fixed-parity lengthening.
* Canonical all-unit `K223` is structural. If any path is long, choose one long
  coordinate, use its exact one-coordinate DNN frontier, and apply fixed-parity
  lengthening.
* All other orders-2--10 owner states are DNN-owned, including exact symbolic
  cost-five states; they are not structural exceptions.

Hence the DNN lane and the three structural lanes are disjoint and exhaustive
for the theorem's rank-six side. Equations (7) and (8) prove (1).

## Exact audit and verification boundary

Run from the repository root:

```text
python3 -I -B research/r61-rank-six-single-block-owner-registry-verifier.py --print-manifest
python3 -I -B research/r61-physical-single-block-theorem-verifier.py --print-manifest
python3 -m unittest research/test_r61_physical_single_block_theorem_verifier.py
```

The verifiers also run byte-identical optimized-mode checks when invoked without
`--emit`. They reject scope widening, owner omissions, loss of strictness,
port-dependent structural selection, altered induced partitions, changed
analytic dependencies, and debit omissions.

Exactly machine-checked here are canonical JSON identities, source and output
digests, the fresh typed-registry invocation, affine DNN/trace/Euler arithmetic,
strict rational ledger arithmetic, the three induced core partitions, the
`K223` automorphism/edge guards, symbolic odd-length path arithmetic, and named
hostile mutations. The universal analytic facts listed above and the
unique-positive-block rooted-tree decomposition are imported proof theorems,
not established merely by Python or hashes.
