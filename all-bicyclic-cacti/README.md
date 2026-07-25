# Positive square energy of all bicyclic cacti

`paper.tex` proves that every connected bicyclic cactus `G` on `n` vertices
satisfies

```text
s+(G) >= n.
```

The theorem allows the two cyclic blocks to share a cut vertex or to be joined
by a path of arbitrary length, with arbitrary trees attached anywhere. It does
not claim the result for all bicyclic graphs.

## Proof map

- The sharp block-additive DNN constant settles all but the cycle-length pairs
  `{5,5}` and `{3,4k+1}`; the common `3 mod 4` Sachs phase handles its triangle
  subfamily.
- A full product-subpartition comparison handles `C3` together with
  `C_(4k+1)` and gives `s+(G) > n + 2 - sec(pi/(4k+1))`.
- An exact coefficientwise polynomial certificate handles two pentagons with
  a shared vertex and gives `s+(G) >= n + 1 - 4/(3 sqrt(13))`.
- An actual-lobe continuant factorization handles two vertex-disjoint
  pentagons with every connector and gives `s+(G) > n + 5 - 2 sqrt(5)`.

## Build

From this directory run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

## Exact certificate

From the repository root run:

```sh
python positive-square-energy/experiments/c5_bouquet_matching_certificate.py
```

Expected digest:

```text
4c436cac772395d2a8edfdd81408ffe426759d3e94d66df2e4ab0235a3343110
```

An optional audit of the connector factorization is available with:

```sh
python positive-square-energy/experiments/connector_factor_audit.py
```

The appendix of `paper.tex` lists all local companion manuscripts and
certificate paths used in the proof.
