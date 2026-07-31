# Kernel 9, row `(0,1,1,1,1)`: all-length packet and residual

## Scope

Use the nonzero-bundle order

`03,04,12,14,23`

and multiplicities `m=(1,2,1,2,2)`. In physical row `q=(0,1,1,1,1)`, write

`l_03=2+2a`, `l_12=1+2b`,

and write each doubled bundle `ij in {04,14,23}` as an odd path of length
`1+2x_ij` and an even path of length `2+2y_ij`. All parameters are
nonnegative integers, subject only to simplicity when an odd path has length
one. Arbitrary rooted trees may be attached at arbitrary vertices.

This note proves every fixed-parity descendant: doubled-path descendants use
new exact DNN certificates, while the doubled-canonical subfamily extends the
previous structural deletion packet to arbitrary singleton-path lengths.

## Theorem

Every simple subdivision `G` of kernel 9 in physical row `(0,1,1,1,1)`, with
arbitrary rooted-tree attachments, satisfies

`s^+(G)>|V(G)|`.

## DNN reduction

For a path of length `l` whose branch-vector endpoint correlation is `r`, put

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                       (1)

Exact path elimination in the correlation dual gives, for a core with total
path length `L`,

`kappa(core)<=L+sum_paths f_l(r_path)`.                      (2)

For fixed `r` and fixed parity, `f_l(r)` strictly decreases under
`l -> l+2` unless its transformed endpoint angle is zero. Rooted trees add
exactly one to `kappa` per edge. Since this rank-four core has `L-3` vertices,
an excess at most three proves `s^+(G)>=|V(G)|`; a strict bound proves the
strict conclusion.

It is therefore enough to certify the four doubled-path frontier types. The
two singleton paths are instead handled by the structural argument below; the
rational search used here did not certify their one-step frontier within the
DNN budget. The kernel automorphism

`(0,1,2,3,4) -> (1,0,3,2,4)`

interchanges `P_03` with `P_12` and the two physical paths in bundle `04` with
their parity-matched paths in bundle `14`; it fixes bundle `23` setwise. This
is an involution of the suppressed kernel, not a switch of physical path
parities. Thus the DNN frontier types are:

`O_a, E_a, O_23, E_23`,                                      (3)

where `O_a,E_a` lengthen the odd or even member of `04` or `14`, and
`O_23,E_23` do the same in `23`.

## Exact rational certificates

A certificate assigns every branch vertex and every internal path vertex a
rational stereographic parameter `t`; the associated unit vector is

`u(t)=((1-t^2)/(1+t^2),2t/(1+t^2))`.                        (4)

For transformed consecutive vectors `u,v`, the exact path excess is

`(1-u dot v)/(1+u dot v)`.                                  (5)

Thus every entry below is a rational PSD Gram certificate, and its total cost
is checked using integer arithmetic only. Paths are ordered

`03; 04_odd,04_even; 12; 14_odd,14_even; 23_odd,23_even`.

| type | representative lengths | branch parameters `(0,1,2,3,4)` | internal parameters by path | exact excess |
|:---|:---|:---|:---|:---|
| `O_a` | `(2;3,2;1;1,2;1,2)` | `(0,1/2,-2,0,-3/4)` | `(0); (3/8,3/4); (-3/8); (); (); (-1/8); (); (-5/8)` | `274636609/106750224` |
| `E_a` | `(2;1,4;1;1,2;1,2)` | `(0,-35/128,363/128,5/32,-449/128)` | `(5/64); (); (-43/128,-97/128,-187/128); (); (); (-127/128); (); (53/64)` | `<3` |
| `O_23` | `(2;1,2;1;1,2;3,2)` | `(0,-13/8,5/8,0,7/4)` | `(0); (); (5/8); (); (); (-381/4); (5/4,21/8); (1/4)` | `169397265426892375078896116727548029/66498943294333381292657717152262400` |
| `E_23` | `(2;1,2;1;1,2;1,4)` | `(0,0,-31/4,-1/8,-13/8)` | `(-1/8); (); (-5/8); (); (); (-1/2); (); (-2,-1,-1/2)` | `24574309112220291047807/9464079288722234391072` |

The `E_a` exact fraction is

`2455762417234397771632703751839480116390241219369499364904459306592428429364885494167`

divided by

`961994787065419545265007148397320162556673426780741122018796796569502796106728243200`,

which is less than three by direct cross multiplication. Every displayed
excess is strictly below three. The table covers all placements within a
doubled bundle by naming the physical odd and even member rather than an
arbitrary parallel-edge label.

## Antichain completion

If at least one path in a doubled bundle is lengthened by two, select one such
coordinate. The resulting length vector coordinatewise dominates its
corresponding representative in the table. Fixed-parity monotonicity, with the
same branch correlations, can only decrease the eliminated path cost.
Consequently its DNN excess is strictly below three. Equations (1)--(2), DNN
tree additivity, and `s^-(G)<=kappa(G)` then give

`s^+(G)>|V(G)|`.                                               (6)

It remains to allow arbitrary same-parity lengths on `P_03,P_12` while all
three doubled bundles retain lengths `{1,2}`. Open either singleton path that
has internal vertices, preferring `P_03`; if neither has changed, open the
canonical length-two `P_03`. Let `T` contain all internal vertices of the open
path and all rooted branches based there. Then `T` is a nonempty induced tree.
Its complement is connected and has exactly the three doubled-bundle cycles,
all triangles. The favorable packing-two phase argument from
`kernel9-row01111-structural-packet.md` is unchanged and gives `D(H)>0`.
Thus `sigma(H)>2`, `sigma(T)=-1`, and induced superadditivity gives the strict
conclusion. This extends that deletion proof from its two stated first-length
realizations to every singleton-path descendant.

In particular, the coordinatewise minimal lengths are

`(2;1,2;1;1,2;1,2)`.

This is the all-`l1/l2` state of `kernel9-row01111-structural-packet.md`, where
opening the internal vertex of `P_03` leaves three favorable triangles and
proves the stronger induced-packet estimate.

Hence the doubled-canonical subfamily is structural and every descendant with
a lengthened doubled path is DNN-certified. There is no residual length
family.

## Search provenance and audit boundary

The rational data were proposed by
`positive-square-energy/experiments/five_vertex_rational_gram_search.py` and
then evaluated exactly through (4)--(5). Numerical optimization is not an
acceptance condition. The argument uses no physical-parity switching: the
kernel involution transports complete physical length assignments, and
monotonicity changes lengths only by two on the same path.

The standalone fail-closed audit is
`research/kernel9-row01111-all-length-verifier.py`. Run

```text
python research/kernel9-row01111-all-length-verifier.py
python -O research/kernel9-row01111-all-length-verifier.py
```

It checks the four rational fixtures `O_a,E_a,O_23,E_23`, their strict budgets,
hostile mutations, and byte-identical normal/optimized output without using
Python `assert`.

Residual: none within kernel 9, physical row `(0,1,1,1,1)`. This theorem does
not classify any other kernel or physical parity row.
