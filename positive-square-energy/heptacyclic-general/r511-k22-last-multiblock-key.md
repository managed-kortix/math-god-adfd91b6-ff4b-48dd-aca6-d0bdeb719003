# R511-K22 exact marked two-cycle packet

## Theorem

Put `sigma(H)=s^+(H)-|V(H)|`. Every bridge-free `R511-K22` physical row is
strict: for either K22 parity state, either legal `P03` frontier, arbitrary
cycle lengths, arbitrary marked attachment cuts, nested or repeated cuts, and
arbitrary rooted-tree attachments,

`sigma(G)>0`.                                                   (1)

Consequently `R511-K22` has empty owner-sensitive residual. This removes the
K22 key returned by `nested-induced-piece-packet-theorem.md`.

## Exact structural targets

Use pair order

`01,02,03,04,12,13,14,23,24,34`.

Kernel 22 has multiplicities `(0,0,1,2,1,1,1,1,1,1)`. Its four structural
targets are exactly

| target | parity row | `P03` length | complete path lengths |
|---|---|---:|---|
| `E0` | `0001111111` | 2 | `2,1,2,1,1,1,1,1,1` |
| `E2` | `0001111111` | 4 | `4,1,2,1,1,1,1,1,1` |
| `O0` | `0011111111` | 1 | `1,1,2,1,1,1,1,1,1` |
| `O2` | `0011111111` | 3 | `3,1,2,1,1,1,1,1,1` |

The path order is `P03,P04^0,P04^1,P12,P13,P14,P23,P24,P34`. In every target
the six last paths are the actual edges of the induced `K4` on `{1,2,3,4}`.
Deleting branch `0` and the interiors of the first three paths gives the
original nonempty induced owner tree.

The exact rational Gram records checked by the verifier give K22 path excess

`e_22 < 21/5`                                                  (2)

on all four targets. Fixed-parity path monotonicity covers every descendant:
lengthening `P03` uses `E2` or `O2`, while lengthening any other path uses its
already certified strict excess-four frontier. Thus (2) is uniform over the
complete structural family, not just the four shortest graphs.

## Exact marked-incidence census

Let the two external cycles be labeled `Q1,Q2`, and project their first owner
routes to marks `x1,x2` in the physical K22 subdivision. Connector and rooted
tree vertices remain with those routes and create no additional structural
orbit. The only nontrivial automorphism in
each target swaps branch vertices `1,2`; it fixes every other vertex. For
`P03` lengths `1,2,3,4`, the physical graph has respectively `6,7,8,9`
vertices and `4,5,6,7` fixed vertices. Burnside therefore gives

`(n^2+(n-2)^2)/2 = 26,37,50,65`                               (3)

ordered marked-cut orbits, respectively. Hence the four exact structural
targets have `178` labeled two-cycle incidence orbits. If `Q1,Q2` are
unlabeled, the corresponding counts are `16,22,29,37`, totaling `104`.
These counts include equal marks, marks at branch vertices, marks inside
`P03`, and the internal mark of the length-two `P04` path. No incidence is
discarded by the proof.

## DNN reduction to two triangles

For a cycle `Q`, write its exact DNN excess as `epsilon(Q)`. We have
`epsilon(Q)<=1`, equality only for a triangle, while every nontriangle has

`epsilon(Q)<=5-2sqrt(5)<3/5`.                                 (4)

If either external cycle is not a triangle, (2)--(4) give

`e_22+epsilon(Q1)+epsilon(Q2) < 21/5+3/5+1 = 29/5 < 6`.

The K22 Gram and the two cycle Grams glue at arbitrary marked cut vertices;
tree and connector edges are exact. The excess-six DNN gate therefore closes
all `178` marked orbits except the two-triangle profile. This is the missing
coupled-Gram debit: it is used only as a sieve and makes no DNN claim at the
two-triangle boundary.

## Two-triangle induced packet

It remains that `Q1=Q2=C3`. Perform the exact K22 opening. Let `A` be the
retained attached actual `K4` and `R` the complete opened owner class.

If a triangle follows `R`, keep that complete class. It has positive rank and
nonnegative credit. Treat the other triangle at its first boundary from `A`;
its complete side has credit at least `-1`. Since `sigma(A)>2`,

`sigma(G)>2+0-1>0`.                                           (5)

Otherwise neither triangle follows `R`, so `R` is the original nonempty tree
and `sigma(R)=-1`. Select the first triangle encountered from `A` (if the two
are nested, select the upstream one) and retain it with `A`. The established
actual-`K4`-plus-triangle packet is attachment-uniform and has credit greater
than three. Treat the unselected triangle at its first boundary; its complete
side has credit at least `-1`. Thus

`sigma(G)>3-1-1>0`.                                           (6)

Repeated marks remain upstream once, and a nested second triangle stays in
one complete first-boundary territory. Every path remnant and rooted descendant
follows its first physical owner. Equations (5)--(6) therefore cover all 178
marked incidences and prove (1).

## Audit

Run in normal and optimized modes:

```text
python3 research/r511-k22-last-multiblock-key-verifier.py
python3 -O research/r511-k22-last-multiblock-key-verifier.py
```

The verifier regenerates the four source-locked K22 targets, reconstructs all
four rational Gram costs with `Fraction`, checks the strict `21/5` bound,
enumerates the exact marked-cut orbits, and rejects arithmetic or incidence
mutations.
