# Hostile audit of the tricyclic assembly

Date: 5 August 2026

## Verdict

The six requested pieces are complete after two bookkeeping repairs found in
the hostile pass:

1. The exceptional doubled-`C4` orbit is not one switching class. It contains
   four physical rows in class `110` and four in class `111`.
2. The all-odd `K4` argument must cover the entire eight-row switching class,
   not only the physically all-odd row. The repaired argument does so without
   switching physical lengths.

With those repairs, the kernel classification and global block proof are
exhaustive. No tricyclic family remains open in the current assembly.

## Piece-by-piece audit

### Cactus `1+1+1`

Status: complete by dependency.

- Three rank-one cyclic blocks form exactly a tricyclic cactus.
- `all-nonunicyclic-cacti/paper.tex` supplies the stronger strict theorem for
  arbitrary bridges and rooted trees.
- `all-tricyclic-cacti/paper.tex` independently supplies the tricyclic residual
  analysis.

Remaining gap: none.

### Theta plus cycle (`2+1`)

Status: complete.

- Exact DNN additivity leaves only `Theta(1,2,r)+C3`, `r>=2`, and
  `Theta(1,2,2)+C5`.
- In the triangle residual, a non-route internal theta vertex always exists;
  opening it leaves an attached two-triangle cactus against one nonempty tree.
- In the pentagon residual, a bridge separates the packets, or a shared cut
  opens `C5` into one induced tree while retaining `Theta(1,2,2)`.

Remaining gap: none.

### Four-path theta

Status: complete.

- Simplicity is exactly the condition that at most one parallel path has
  length one.
- Fixed-parity monotonicity reduces all lengths to the no-unit and one-unit
  tangent cases.
- All five no-unit parity counts and all four one-unit parity counts are
  covered. Auxiliary DNN equality occurs only at `(1,2,2,2)`.
- One-vertex additivity includes arbitrary rooted trees.

Remaining gap: none.

### Doubled triangle

Status: complete.

- The physical census has 32 labelled rows in 12 orbits.
- Twenty-eight rows have exact rational Gram certificates.
- The four `EO,EO`/odd-connector rows split exhaustively into a noncanonical
  parallel path, covered by one of two DNN certificates, or canonical pairs
  `{1,2}`.
- Canonical pairs open either the connector, leaving two triangles, or an even
  parallel member, leaving `Theta(1,2,2)`, against one nonempty tree.

Remaining gap: none.

### Doubled `C4`

Status: complete after correcting the switching label.

- The explicit 28-row DNN ledger and eight-row exceptional automorphism orbit
  partition all 36 simple physical parity rows.
- The exceptional orbit contains four rows in class `110` and four in class
  `111`; it must not be called a unique failed switching class.
- A noncanonical doubled member is covered by one of two exact long-path DNN
  certificates.
- With both doubled pairs canonical, opening the even connector leaves an
  attached two-triangle cactus against one nonempty tree.

Remaining gap: none.

### `K4`

Status: complete after extending the last-class proof to all physical rows.

- The seven non-all-odd switching classes comprise 56 physical parity rows and
  have direct physical-row Gram certificates.
- In the remaining class, physical parities have
  `p_ij = 1 xor s_i xor s_j`. Switching the endpoint vectors makes every
  transformed angle the all-odd angle while preserving each physical length.
- Every even physical path is long. A nonconstant switch produces exactly
  three or four even paths, namely a nontrivial `K4` cut.
- With at least four long paths, the simplex costs less than
  `(6-q)/2+q/4 <= 2`. With exactly three, the sole switched case has three even
  length-two paths and three odd units; its sharper simplex cost is less than
  `3/2+3/6=2`.
- Exactly two long paths forces the switch to be constant, reducing to the
  adjacent/opposite all-odd certificates. Exactly one long path opens to a
  bipartite theta of credit one plus a tree of credit minus one. Zero long
  paths is the attached-`K4` packet.

This case split covers all eight physical parity rows in the switching class
and all path lengths. Remaining gap: none.

## Exhaustive kernel classification

Let `B` be a simple 2-connected block of cyclomatic rank three. Suppress every
maximal path whose internal vertices have degree two in `B`, retaining parallel
edges. Suppression creates no loop: such a loop would represent a cycle meeting
the rest only at one branch vertex, contradicting 2-connectivity, unless `B`
were itself rank one.

In the loopless kernel `K`, every degree is at least three and

```text
sum_v (deg_K(v)-2) = 2(|E(K)|-|V(K)|) = 4.
```

Hence the excess-degree partition is `2+2`, `2+1+1`, or `1+1+1+1`, giving:

- `(4,4)`: four parallel edges;
- `(4,3,3)`: a triangle with the two sides incident to the degree-four vertex
  doubled;
- simple `(3,3,3,3)`: `K4`;
- nonsimple `(3,3,3,3)`: two disjoint doubled edges joined by two single edges,
  namely doubled `C4`.

Simplicity of the original graph says at most one path in each parallel kernel
class has length one. These four kernels are exhaustive.

## Global proof

Let `G` be finite, simple, connected, and satisfy `m=n+2`.

1. Positive cyclomatic ranks of cyclic blocks add to three, so the rank
   partition is exactly `1+1+1`, `2+1`, or `3`.
2. Rank `1+1+1` is covered by the tricyclic cactus theorem.
3. Rank `2+1` is one theta block and one cycle block, covered by the exact DNN
   sieve and its two induced-territory repairs.
4. In rank `3`, suppress degree-two paths. The exhaustive classification gives
   four-path theta, doubled triangle, `K4`, or doubled `C4`; apply the completed
   theorem for that kernel.
5. Bridge blocks and rooted trees are included by one-vertex additivity of
   `kappa` in DNN rows and by explicit branch ownership in structural rows.

Therefore every alternative satisfies `s^+(G)>=n`.

## Verification

The following all pass normally and with assertions disabled where applicable:

```sh
python3 research/tricyclic-finite-rational-certificates-verifier.py
python3 -O research/tricyclic-finite-rational-certificates-verifier.py
python3 positive-square-energy/experiments/k4_all_odd_exact_verify.py
python3 -O positive-square-energy/experiments/k4_all_odd_exact_verify.py
python3 research/tricyclic-gram-obstruction-verifier.py
bash scripts/build-paper.sh all-tricyclic-graphs
```

The main finite audit reports digest
`795f7772618d4f0280da914a85042970492f641909cd093abe9e30b434aa279c`
and rejects all 21 hostile mutations. These scripts audit the finite
records; the analytic duality, monotonicity, structural deletions, and block
classification remain mathematical arguments in the proof notes and paper.
