# Rank-seven kernels of order eight

This folder proves the following scoped theorem.

> Let `G` be a finite simple connected graph of cyclomatic rank seven with
> exactly one positive-rank cyclic block. If suppressing the degree-two
> vertices of that block produces a loopless 2-connected multigraph kernel on
> eight vertices, then `s+(G) >= |V(G)|`.

Equivalently, the theorem covers every simple subdivision of every rank-seven,
order-eight kernel, together with arbitrary finite rooted trees attached at
branch or subdivision vertices.

## Scope boundary

This is **not** an all-heptacyclic theorem. It does not cover:

- kernel orders nine through twelve;
- rank-seven graphs with two or more positive-rank cyclic blocks; or
- all finite simple connected graphs with `|E| = |V| + 6`.

It also does not claim fresh recomputation of the four historical base
producers named by the theorem gate. Those byte-pinned producer artifacts are
an explicit part of the computational trust boundary.

## Proof map

1. Suppression reduces the unique rank-seven block to a loopless
   2-connected kernel. An order-eight kernel has fourteen physical edges.
2. The proved removable-ear census contains exactly `4,015` such kernels.
3. Exact automorphism reduction gives `26,426,026` physical parity orbits.
   The regular-tetrahedron coarse Gram certifies `25,932,609` and leaves
   `493,417` residual orbits, each with fifteen canonical-plus-coordinate
   frontier targets.
4. The final exact residual partition is

   ```text
   493417 = 605 + 29000 + 194351 + 185309 + 296
            + 245 + 29013 + 54597 + 1.
   ```

5. Exact path elimination promotes each retained DNN branch Gram to all
   same-parity path lengths, and one-vertex DNN additivity includes arbitrary
   rooted-tree attachments.
6. The unique last orbit is two subdivided copies of `K4` joined by two paths.
   An induced vertex partition produces two connected tricyclic territories,
   so the complete tricyclic theorem and induced superadditivity close it for
   all lengths and all parities.

See `paper.tex` and the compiled `paper.pdf` for the full argument and trust
boundary.

## Verification

From the repository root, run the quick integration gate in normal and
optimized modes:

```sh
python3 -B research/rank-seven-order-eight-kernel-theorem-verifier.py
python3 -O -B research/rank-seven-order-eight-kernel-theorem-verifier.py
python3 -B research/rank-seven-order-eight-kernel-theorem-verifier.py --print-manifest
```

Pinned gate source SHA-256:

```text
02f5176cbb51477a9755c633e6aae7790e618b99eca1bb22000399c59dc7c6a1
```

Expected quick text-only output SHA-256:

```text
d330cc817f2e999828d95e661a696d779f524ae79feadd98728c23cf9266dcd4
```

Expected manifest-plus-text output SHA-256:

```text
9963af971382e296adeff3905cc1df7e50a8f2362851c819205f047799375932
```

Quick mode authenticates sources, artifacts, schemas, exact accounting,
singleton bytes, prior exact child receipts, and twelve hostile rejections. It
does not rerun the semantic child replays. For the full read-only replay, run:

```sh
python3 -B research/rank-seven-order-eight-kernel-theorem-verifier.py --full
```

Full replay still differs from fresh producer recomputation: the payload-free
recognizer semantics, raw scalar-SOS membership semantics, the `492,812`
expensive typed searches behind the receipts, and the `29,000` direct-rational
witness packs remain named, immutable base trust roots.

## Build

```sh
bash scripts/build-paper.sh rank-seven-order-eight-kernels
```

This produces `rank-seven-order-eight-kernels/paper.pdf`. No publication or
external announcement is part of this folder.
