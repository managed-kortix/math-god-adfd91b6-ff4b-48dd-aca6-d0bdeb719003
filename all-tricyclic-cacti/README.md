# Positive square energy of all tricyclic cacti

`paper.tex` proves that every connected tricyclic cactus `G` on `n` vertices
satisfies

```text
s+(G) >= n.
```

The theorem allows arbitrary cycle-block incidence, bridge paths, and trees
attached anywhere.

## Proof map

- The exact block-additive cactus DNN constant reduces all cycle-length triples
  to exactly `{3,3,q}` for odd `q` and `{3,5,5}`.
- For `{3,3,q}`, packing-two phase handles the `3 mod 4` case unless all three
  cycles are disjoint, when induced unicyclic territories apply. For `q = 1
  mod 4`, induced packet partitions and a shared-triangle
  product-subpartition comparison exhaust every incidence.
- For bridge-separable `{3,5,5}`, a leaf cyclic cluster is isolated by an
  actual bridge. Unicyclic and bicyclic packet bounds then give `s+(G) > n`.
- For one shared-cut cluster, four weighted cores remain. The exact certificate
  `Phi = 2R(p+q) - I(pq-4) > 0` bounds the core phase by two actual weighted
  pentagon phases and gives `s+(G) > n + 6 - 2 sqrt(5)`.

No triangle-ear lemma or general edge-monotonicity is used.

## Build

From this directory run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

## Exact certificate

From the repository root run:

```sh
python positive-square-energy/experiments/c3_c5_c5_shared_cluster_certificate.py
```

Expected table:

```text
core                                      terms  min  max  SHA-256
bouquet                                    2547    2   32  8112f2944f9823177afd48deccfb958ac960548e09d9d838e4965c33eb39e979
triangle_middle_distinct_vertices          2192    2   32  4fdb04cee38f0c0e2ac2de6dff7e641c2e190a3c018af8308a5c69e378de2ba2
pentagon_middle_cut_distance_1              2925    2   36  bfa73346f169f28ec6109418ce22fe44daaae6b081ade30074932b139f0828f4
pentagon_middle_cut_distance_2              2895    2   36  5c6c213471a856cb743afda8e62407d7d27de5984b612c70ab411499011db437
```

The certificate uses exact integer arithmetic and validates every coefficient,
term count, and digest. The appendix lists the local public proof objects used
for the packet bounds and audited `{3,3,q}` theorem.
