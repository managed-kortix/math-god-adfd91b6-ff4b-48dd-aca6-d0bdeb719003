# Every nonunicyclic cactus has strict positive square energy

**Date:** 2026-07-30

## Theorem and boundary

Let `G` be a finite simple connected cactus of cyclomatic rank `k>=2`, and let
`n=|V(G)|`. Then

```text
s+(G)>n.
```

Rank one is deliberately excluded. The cycle `C4` is a connected unicyclic
cactus with adjacency spectrum `2,0,0,-2`, so `s+(C4)=4=|V(C4)|`; strictness
is false at the excluded boundary.

## 1. Rank-uniform sharp-DNN reduction

If the cyclic blocks have lengths `l_1,...,l_k` and there are `b` bridge
blocks, block counting gives

```text
b+sum_i l_i=n+k-1.
```

Define

```text
epsilon_l = 0                         if l is even,
epsilon_l = l tan^2(pi/(2l))          if l is odd.
```

The exact cactus DNN theorem gives

```text
s-(G) <= b+sum_i(l_i+epsilon_(l_i)).
```

Since `s+(G)+s-(G)=2|E(G)|=2(n+k-1)`, it follows that

```text
sigma(G):=s+(G)-n >= k-1-sum_i epsilon_(l_i).       (1)
```

Put `T=C3`, `P=C5`, and `a=epsilon_5=5-2sqrt(5)`. The odd sequence
`epsilon_l` decreases strictly after `l=3`; `epsilon_3=1`, and every
nontriangle contributes at most `a`. The exact comparisons used below are

```text
3a<2,       2a>1,       a+epsilon_7<1.              (2)
```

The derivative proof and exact radical/rational certificates are frozen by
`research/rank-uniform-cactus-dnn-frontier-verifier.py`.

## 2. Exact uniform deficiency frontier

Let `h` be the number of nontriangular cycles.

- If `h>=3`, then `sum epsilon <= (k-h)+ha <= (k-3)+3a<k-1`.
- If `h=2`, an even cycle contributes zero. If both are odd but are not both
  pentagons, their contribution is at most `a+epsilon_7<1`. Hence (1) is
  strict except for the pair `PP`; that pair is genuinely residual because
  `2a>1`.
- If `h<=1`, write the multiset as `T^(k-1)Q`, allowing `Q=T` when `h=0`.
  Its epsilon sum is `(k-1)+epsilon_q>=k-1`, so the DNN bound alone is not
  strict.

Therefore the sharp-DNN non-strict set is exactly

```text
T^(k-1)Q,       T^(k-2)PP.                            (3)
```

The argument has a fixed number of inequalities independent of `k`; it is not
a rank census. The verifier encodes every bound as an affine expression
`cK+d` with `c,d` in `Q(sqrt(5))`. It mechanically checks that `K` cancels in
the comparisons, that the resulting constants have the required exact signs,
and that the `h>=3` bound decreases with `h`, hence is maximal at `h=3`.
Canonical expression records, rather than prose or calls to a `frontier(k)`
function, determine the certificate digest. Semantic substitutions at
`K=2,3,4,5,7,13,64` test all generated templates as identities but are not the
proof of arbitrary rank. Seven hostile mutations are rejected, including
changes to a `K` coefficient, radical sign, case bounds, and survivor families.

## 3. Structural closure of `T^(k-1)Q`

Here `k>=2`, so there are `k-1>=1` triangles.

- If `q=1 mod 4`, necessarily `q>=5`, and the all-rank one-hostile-cycle
  theorem applies.
- If `q` is even or `q=3 mod 4`, the all-rank nonhostile one-cycle theorem
  applies. It explicitly includes `q=3`, so it also closes the all-triangle
  member.

Together these two established theorems cover every integer `q>=3`. Both
permit arbitrary shared cut vertices, bridge connectors, incidence topology,
and finite tree attachments.

## 4. Structural closure of `T^(k-2)PP`

If `k>=3`, put `r=k-2>=1`. The all-rank two-pentagon theorem applies directly
to every cactus with `r` triangles and two pentagons, with arbitrary incidence,
connectors, and attached trees.

The boundary `k=2` is the pure `PP` bicyclic family and is handled separately:

- If the two pentagons share their unique possible common vertex, the
  two-`C5` bouquet theorem gives
  `s+(G)>=n+1-4/(3sqrt(13))>n`.
- Otherwise the cycles are vertex-disjoint. Their unique connecting path has
  positive length, and the all-connectors theorem gives
  `s+(G)>n+5-2sqrt(5)>n`.

These two cases exhaust connected cacti with exactly two pentagonal cyclic
blocks. This explicit rank-two split avoids applying the all-rank
`T^rPP` theorem outside its stated hypothesis `r>=1`.

## 5. Dependency map

```text
main theorem
|
+-- sharp DNN bound and exact frontier
|   +-- sharp-cactus-dnn/paper.tex
|   +-- research/rank-uniform-cactus-dnn-frontier-verifier.py
|
+-- T^(k-1)Q closure
|   +-- q=1 mod 4: all-rank-triangle-hostile-cacti/paper.tex
|   +-- q even or 3 mod 4:
|       research/all-rank-nonhostile-one-cycle-theorem-2026-07-30.md
|
+-- T^(k-2)PP closure
    +-- k>=3: all-rank-triangle-two-pentagon-cacti/paper.tex
    +-- k=2, shared cut: two-c5-bouquet-trees/paper.tex
    +-- k=2, positive connector: two-c5-all-connectors/paper.tex
```

No rank-specific cactus theorem is logically needed. The earlier rank-two
through rank-thirteen papers are corroborating specializations, not premises.

## 6. Reproduction and scope

From the repository root, run:

```bash
python3 research/rank-uniform-cactus-dnn-frontier-verifier.py
python3 -O research/rank-uniform-cactus-dnn-frontier-verifier.py
bash scripts/build-paper.sh all-nonunicyclic-cacti
```

The verifier certifies only the arithmetic classification (3), not the sharp
DNN theorem or any structural closure theorem. Its displayed frontier is not a
trusted finite-rank oracle: the trusted claim is the serialized symbolic
ledger in `Q(sqrt(5))[K]`. The manuscript proves a theorem
for finite simple connected cacti of cyclomatic rank at least two. It does not
claim the corresponding statement for all graphs, disconnected graphs,
non-cactus block intersections, or rank one.

## AI disclosure

This proof note and its assembly were generated by an AI coding and
mathematical reasoning system from the cited repository proof objects. No human
authorship, review, or verification is claimed. Nothing was published by this
task.
