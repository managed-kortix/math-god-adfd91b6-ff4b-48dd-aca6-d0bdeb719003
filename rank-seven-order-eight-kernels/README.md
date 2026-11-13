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

It also does not claim fresh reruns of the three residual historical base
producer searches named by the theorem gate: payload-free recognizer semantics,
raw scalar-SOS membership semantics, and the 492,812 typed searches behind the
receipts. Those byte-pinned outputs are an explicit part of the computational
trust boundary. The 29,000 direct-rational packs are not a fourth trust root:
full mode freshly exact-replays all of them.

## Literature boundary

This theorem is a restricted partial result on AKMPZ Conjecture 1.2
([arXiv:2506.07264v1](https://arxiv.org/abs/2506.07264v1)), not a resolution of
that conjecture. The tree-free instances are already covered by broader 2026
theorems for every 2-connected noncycle
([arXiv:2609.04069v1](https://arxiv.org/abs/2609.04069v1)) and every connected
noncycle of minimum degree at least two
([arXiv:2609.06778v1](https://arxiv.org/abs/2609.06778v1)). The additional
scope here relative to those results is the uniform allowance of arbitrary
rooted-tree attachments, including leaf-bearing instances, inside this exact
rank-seven/order-eight-kernel frontier.

The dated source/status audit is
`research/rank-seven-order-eight-source-status-audit-2026-11-11.md`. It found no
public theorem with the full combined scope in the sources searched, but that
negative search does not establish novelty or priority. No firstness claim is
made.

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
334e963b36e88549716e772374c4bf2729b3757b013ebc5482deaf821ab47ee2
```

Expected quick text-only output SHA-256:

```text
c9a4b73d64f4aa4ee141541d97897516b58f25019228d359490b321b7f815319
```

Expected manifest-plus-text output SHA-256:

```text
d153738d36a43d8178598c52de2067453dca1cefce056bf7d911466ce0211ccd
```

Quick mode authenticates sources, artifacts, schemas, exact accounting,
singleton bytes, prior exact child receipts, and 21 hostile rejections. It
AST-checks 26 proof-critical Python sources for optimization-removable
`assert` statements. It does not rerun the semantic child replays. For the
full read-only replay, run:

```sh
python3 -B research/rank-seven-order-eight-kernel-theorem-verifier.py --full
```

Full replay completed successfully on these exact verifier bytes in both normal
and optimized Python. It regenerated the exhaustive kernel fixture and the
complete order-eight parity/coarse census, reconstructed the selected
492,812-row census projection in memory and checked the pinned cache
field-for-field, exact-replayed all 29,000 direct-rational witness records
(435,000 targets), and replayed all downstream children. It does not write a
new cache artifact or rerun the three historical producer searches named
above. The direct-pack child itself consumes the pinned cache; its exact replay
is independently linked to the master-level census projection.

## Build

```sh
bash scripts/build-paper.sh rank-seven-order-eight-kernels
```

This produces `rank-seven-order-eight-kernels/paper.pdf`. No publication or
external announcement is part of this folder.
