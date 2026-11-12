# Doubled `C4`: exact 64-row parity census and omitted-row certificates

## Scope and correction

This is a finite exact-computation note, not a theorem promotion. It corrects
the bookkeeping boundary of the old 36-row doubled-`C4` census.

Order the six kernel paths as

`(a,A,b,c,C,d)`, with `a,A:01`, `b:12`, `c,C:23`, and `d:30`.

There are `2^6=64` labelled parity rows. Their first **simple** lengths are

- even path: `2`;
- odd path: `1`;
- odd/odd parallel pair: the unordered pair `{1,3}`.

For deterministic labelled records, this audit assigns `(1,3)` to `(a,A)` or
`(c,C)`. Swapping the two members is a genuine kernel automorphism and does
not change the certificate.

The old 36-row census imposed `not(a=A=odd)` and `not(c=C=odd)` and therefore
omitted exactly

`64-36=28`

valid first-simple rows. Every omitted row contains at least one odd/odd
parallel pair. The computation below certifies all 28 omitted rows directly.
No switching operation is used to quotient physical rows.

## Genuine automorphisms

The verifier derives the automorphism group from the endpoint-multiplicity
matrix of the multigraph. It finds:

- `4` vertex permutations;
- with the compatible permutations inside the two parallel edge fibres, `16`
  edge permutations;
- `18` orbits on all `64` labelled parity rows;
- `9` orbits on the old `36` rows;
- `9` orbits on the omitted `28` rows.

No genuine automorphism orbit mixes an old row with an omitted row. Vertex
switching is not in this group and is never used as an identification.

## Exact planar certificates

For integers `k=(k_0,k_1,k_2,k_3)`, use the planar unit vectors

`u_v=(cos(pi k_v/3), sin(pi k_v/3))`

and their Gram matrix `R_uv=cos(pi(k_u-k_v)/3)`. This matrix is positive
semidefinite with unit diagonal by construction. For a path of length `l`
between `u,v`, its excess contribution is

`l tan^2(acos((-1)^l R_uv)/(2l))`.

The following nine records cover the 28 omitted rows under genuine kernel
automorphisms. Every listed upper bound is rational and at most two.

| orbit representative | first simple lengths | planar `k` | orbit size | exact rational upper bound |
|---|---|---:|---:|---:|
| `000110` | `(2,2,2,1,3,2)` | `(0,1,2,5)` | 2 | `72/125` |
| `000111` | `(2,2,2,1,3,1)` | `(0,0,0,3)` | 4 | `0` |
| `001111` | `(2,2,1,1,3,1)` | `(0,1,5,2)` | 2 | `358/375` |
| `010110` | `(2,1,2,1,3,2)` | `(0,2,2,5)` | 4 | `143/125` |
| `010111` | `(2,1,2,1,3,1)` | `(0,2,1,4)` | 8 | `554/375` |
| `011111` | `(2,1,1,1,3,1)` | `(0,2,0,3)` | 4 | `4/3` |
| `110110` | `(1,3,2,1,3,2)` | `(0,3,3,0)` | 1 | `0` |
| `110111` | `(1,3,2,1,3,1)` | `(0,2,1,4)` | 2 | `68/75` |
| `111111` | `(1,3,1,1,3,1)` | `(0,3,0,3)` | 1 | `0` |

The orbit sizes sum to `28`. The largest certified bound is `554/375<2`.

Only three tangent values occur. The audit uses

- `tan^2(pi/12) < 9/125`;
- `tan^2(pi/6) = 1/3`;
- `tan^2(pi/18) < 4/125`.

The strict inequalities are proved with rational alternating Taylor
enclosures and

`333/106 < pi < 355/113`.

Thus the computation contains no floating-point step. For example, the
largest row bound is

`2*(2*9/125) + 2*(1/3) + 2*9/125 = 554/375 < 2`.

The all-zero records are possible because the chosen endpoint correlations
make every transformed path angle zero, including the length-three members of
odd/odd pairs.

## Exhaustive result

The old 36-row ledger and these 28 new records partition all 64 labelled
parity rows. For every row omitted from the old census, the verifier supplies
a planar Gram matrix with exact rational excess upper bound at most two.
There is therefore **no omitted-row Gram obstruction** at the correct first
simple lengths. The obstruction was only the old census restriction that
excluded odd/odd parallel pairs instead of assigning them `{1,3}`.

This conclusion is intentionally limited to the finite path-reduced Gram
calculation. Its use for arbitrary longer paths depends on the separately
proved fixed-parity monotonicity statement.

## Reproduction

Run both ordinary and optimized Python:

```sh
python3 research/doubled-c4-64-row-exact-verifier.py
python3 -O research/doubled-c4-64-row-exact-verifier.py
```

Expected digest:

```text
2c1efbbf65b2c11f563f0f32cf7c1d70057d0aeb6d4d657ac6f0fe353f3b339c
```

The script independently enumerates the 64 rows, reconstructs the genuine
kernel automorphisms, expands the nine records to all 28 omitted rows,
recomputes every transformed angle and rational bound, rejects any missing
or duplicate coverage, and runs four hostile mutations (missing orbit, wrong
Gram angles, wrong displayed bound, and false tangent bound).
