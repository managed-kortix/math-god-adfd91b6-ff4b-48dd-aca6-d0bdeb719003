# Kernel 17: physical parity cover from the all-odd Gram certificate

This is a standalone exact packet. It does not alter a main theorem or verifier.

## Kernel and physical census

In upper-triangle order, kernel 17 is

`(0,0,1,1,1,1,0,1,1,1,0,1,1,0,0)`.

Its nine edges, in the order used here, are

`03,04,05,12,14,15,23,25,34`.

Every edge is simple. A physical canonical row is therefore a word
`p in {0,1}^9`, where `1` means canonical odd length one and `0` means
canonical even length two. The exact census has `2^9=512` rows. Longer paths
of the same parity are covered by fixed-parity path monotonicity.

Kernel 17 is the triangular prism: the two triangles are `034` and `125`, and
the matching is `05,14,23`.

## The all-odd excess-two certificate

Give vertex `v` the planar angle `pi a_v/3`, with

`a=(0,1,5,2,4,3)`.

The three matching edges have correlation `-1`; the other six edges have
correlation `-1/2`. Thus the all-odd row has three zero terms and six terms
`1/3`, for exact excess two.

For a physical row, switch signs at branch vertices. Fix the switch at vertex
zero and enumerate the other `2^5=32` switches. This changes a vector angle by
`pi` but never changes a physical path parity or canonical length. For each
physical row the verifier evaluates all 32 switched matrices and retains the
least exact cost.

The only possible canonical terms belong to `Q(sqrt(3))`:

| correlation | odd length one | even length two |
|:---:|---:|---:|
| `-1` | `0` | `2` |
| `-1/2` | `1/3` | `2/3` |
| `1/2` | `3` | `14-8sqrt(3)` |
| `1` | infinite | `0` |

Comparison with the tetracyclic budget three is exact: the verifier compares
`a+b sqrt(3)` by rational squaring with sign control.

## Exact single-matrix classification

The switched sign orbit of the same all-odd matrix certifies exactly

`284 covered + 228 residual = 512 physical rows`.

Under the genuine order-12 automorphism group of the triangular prism, this is

`46 covered orbits + 28 residual orbits = 74 parity orbits`.

The word "residual" here means only that no sign switch of this one matrix has
canonical excess at most three. It is not a failure of DNN and not a graph
counterexample.

This is also the precise switching/debit interpretation. Relative to the
all-odd value two, a sign switch chooses which physical odd/even terms incur
the displayed debits. A row is accepted exactly when the total exact debit is
at most one. The calculation is performed on the physical canonical row, not
on switched path lengths.

## Seven-template exact cover

Six further planar templates on the same `pi/3` grid close the single-matrix
residual. Listed after the all-odd template, the seven angle words are

```text
(0,1,5,2,4,3)
(0,0,1,1,2,2)
(0,1,0,2,1,2)
(0,0,0,1,1,1)
(0,1,2,1,2,0)
(0,0,1,2,2,1)
(0,1,0,2,2,0)
```

For each template all 32 branch sign switches are allowed, again while
retaining the original physical parities and canonical lengths. In the listed
order, the disjoint first-cover gains are

`284,123,56,24,13,8,4`.

They sum to 512. Hence the exact final ledger is

`512 covered + 0 residual`.

This is a small-template all-length DNN cover of every kernel-17 subdivision,
including arbitrary rooted-tree attachments by one-vertex additivity.

## Fail-closed audit

The standalone verifier is

`research/rank-four-kernel17-all-odd-switching-verifier.py`.

Run

```text
python research/rank-four-kernel17-all-odd-switching-verifier.py
python -O research/rank-four-kernel17-all-odd-switching-verifier.py
```

It decodes the kernel, regenerates all 512 physical rows and the order-12
automorphism group, evaluates exact `Q(sqrt(3))` costs for every switch, checks
the `284/228` single-matrix partition and `46/28` orbit partition, verifies the
seven disjoint gains and zero final residual, digest-locks all single-matrix
row costs, and rejects hostile mutations. It contains no numerical optimizer.
