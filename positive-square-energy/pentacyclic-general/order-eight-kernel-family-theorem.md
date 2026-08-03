# Complete order-eight rank-five kernel-family theorem

## Theorem

Let `K` be any of the 16 order-eight kernels in the exact rank-five suppressed
kernel classification. Let `B` be any simple subdivision of `K`, and obtain
`G` by attaching an arbitrary rooted tree at each vertex of `B`. Then

`s^+(G) >= |V(G)|`.

Every case has a DNN certificate of excess at most four. The finite proof
ledger has exactly 45,279 keys: 45,249 strict rational records and 30 exact
symbolic equality records.

## Source-locked census and chunks

The exact census independently reconstructs all 16 cubic kernels, 46,736
labeled physical parity rows, and 11,188 automorphism orbits. The regular
tetrahedron certifies 7,705 orbits and leaves 3,483 residuals. Every kernel has
12 suppressed paths, so canonical plus all 12 one-coordinate length-plus-two
frontiers gives

`3483(1+12)=45279`

targets. The theorem verifier derives this key universe from the census rather
than trusting the search output.

The large rational evidence remains in the four original chunks rather than
being duplicated into one giant theorem JSON. Their residual slices are
`[0,871)`, `[871,1742)`, `[1742,2613)`, and `[2613,3483)`. The verifier locks
every chunk digest, requires exact slice/key equality, and rejects duplicate,
missing, or extraneous keys across chunk boundaries. The compact theorem
fixture stores only the 30 symbolic closure records and source digests.

## Rational certificates

For each of 45,249 strict targets, the verifier parses every reduced fraction,
reconstructs all eight unit branch vectors and every internal path vector from
seven stereographic parameters, rebuilds the 12 physical paths, and sums the
exact adjacent-step costs

`(1-r)/(1+r)`.

It requires equality with the stored reduced cost and strict inequality below
four. Numerical optimizer values have no proof role.

## Signed-cycle K118 equality

K118 has single support edges `01,26,35,47` and doubled support edges
`02,17,36,45`. The 30 raw obstructions are exactly six parity rows at the
canonical target and path frontiers `0,5,6,11`, the four single-edge path
coordinates.

For signs `s01,s26,s35,s47` determined by the four single-path parities, use
base vectors `X0,X1,X2,X3` with cyclic Gram entries

```text
<X0,X1> = -1/2
<X1,X2> = -s26/2
<X2,X3> = -s35/2
<X3,X0> = -s01*s47/2
```

and zero on the two diagonals of the cycle. Assign the eight branch vectors

```text
(u0,u1,u2,u3,u4,u5,u6,u7)
  = (X0,s01 X0,X1,X2,X3,s35 X2,s26 X1,s47 X3).
```

The six source rows give six exact signed `C4` matrices. For every row and all
five frontiers, the verifier reconstructs the `4 x 4` base Gram and pulled-back
`8 x 8` branch Gram and checks every principal minor. Each single path has
transformed endpoint correlation one and cost zero. On each doubled edge, the
odd unit path costs `1/3` and the even length-two path costs `2/3`; the latter
also carries an exact PSD midpoint Gram check. Thus the four doubled edges cost
exactly four. Lengthening any of paths `0,5,6,11` preserves zero cost.

## All lengths and arbitrary trees

For every residual row, the canonical target and every one-coordinate frontier
are present. If any coordinate grows, select its strict or symbolic frontier;
fixed-parity path monotonicity covers all further increments by two. The 30
symbolic keys use precisely five frontiers for each of six rows, while the
other eight frontiers of those rows are strict rational certificates. This
checks all simple subdivisions, not only canonical lengths.

Attaching arbitrary rooted trees preserves the conclusion by the standard
one-vertex-sum tree additivity argument. Since an order-eight rank-five
subdivision with `L` edges has `L-4` vertices, excess at most four gives the
claimed `s^+` inequality after any number of tree edges are attached.

## Fail-closed audit

| artifact | SHA-256 |
|:---|:---|
| rank-five kernel source | `027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884` |
| order-eight tetra census | `096a3ec3213bdf02f322a33790c84b206cd65b9a665220dbd76067de25947488` |
| rational chunk 0 | `2b4f2ccdb91c4cb6e8f27da94f99afec24d36c0fd0fc0175683ee9e97cd901f3` |
| rational chunk 1 | `4714d80c3e3b5161add1f915378af0a9541181b210bafd64ce531678c6bb0929` |
| rational chunk 2 | `291beab34f3d3d3649042eea2ce55c76657aa460d59ace71615fa133b6a2b81a` |
| rational chunk 3 | `09e0d6f38b19177b54f7579d14bc05dfc37bfb6f1c5308d870106698130feccf` |
| compact theorem fixture | `f1c08641de224194d871197454d7056eb0884c8972c535dd8daa5abd08a37a6f` |

The audit rejects ten hostile mutations and requires byte-identical normal and
optimized output:

```text
python3 pentacyclic/research/order8-kernel-family-theorem-verifier.py
python3 -O pentacyclic/research/order8-kernel-family-theorem-verifier.py
```

Together with the existing order-two through order-seven packages, this
exhausts the classification ledger `1+3+13+24+38+23+16=118`. The implication
master invokes every exact owner, including the separate all-odd `K5-e`
theorem:

```text
python3 research/rank-five-order2-8-master-verifier.py
python3 -O research/rank-five-order2-8-master-verifier.py
```
