# Order-eight rank-six exact symbolic templates

## Exact template frontier

The exact combinatorial recognizer finds the following equality-template rows
in the locked order-eight residual stream:

| geometry | kernels | residual rows |
|:--|:--|--:|
| signed five-cycle | K744, K756 | 12 |
| tetrahedron plus apex | K706, K717, K737, K762, K817, K822, K835, K842, K946, K949, K953, K954, K958 | 33 |
| total | 15 kernels | 45 |

For each row, the canonical target has exact DNN cost five. Exactly three of its
13 paths are signed contractions and have local cost zero. Lengthening one of
those paths by two leaves its local cost zero, so those three coordinate
frontiers also have exact cost five. Every other path has positive local cost.
For fixed noncoincident endpoints the equal-step DNN path energy
`L tan^2(theta/(2L))` strictly decreases when `L` is replaced by `L+2`.
Indeed, with `y=theta/(2L)`, its derivative in `L` is
`tan(y)^2-2y tan(y)sec(y)^2<0`: positivity gives
`tan(y)<2y sec(y)^2`. Consequently all other coordinate frontiers are strict
DNN witnesses.

Thus the 630 row-target pairs split exactly into 180 cost-five targets and 450
strict targets. The 180 are the canonical target and three contractions in each
of 45 rows. This proves the symbolic template frontier; it does not assert that
the completed global search has no null target outside these 45 rows.

## DNN budget combinatorics

Both templates spend the rank-six budget of five in indivisible local packets.

For the signed-cycle family, contract three singleton supports with the signs
forced by their parities. Five quotient classes remain and the five doubled
supports form a cycle. Every doubled support is mixed, so its odd path costs
`1/3` and its even path costs `2/3`. Thus

`5*(1/3+2/3)=5`.

The quotient Gram is `I-S/2`, where `S` is the switched adjacency matrix of the
five-cycle. Its spectrum lies in `[-2,2]`, proving positive semidefiniteness for
both cycle switching classes.

For the simplex/apex family, contract three signed singleton supports. The
five-class quotient consists of a `K4` on six singleton supports and an apex
joined to two tetrahedron vertices by the two doubled supports. Require all six
tetrahedral supports to be odd and both doubled supports to be mixed. The six
simplex edges have transformed correlation `1/3` and cost `1/2` each; each
mixed apex bundle costs one. Hence

`6*(1/2)+2*(1/3+2/3)=5`.

The regular tetrahedron has correlation `-1/3`. The two prescribed apex
correlations are signed `-1/2`; the other two are equal and chosen so that all
four switched apex correlations sum to zero. This is the Schur-complement
boundary of the tetrahedron Gram. The recognizer does not trust that argument
alone: it checks all 255 principal minors of each pulled-back `8 by 8` rational
Gram.

## Recognizer

`rank6_order8_symbolic_recognizers.py` derives both template families from the
locked kernel fixture. It does not contain an assumed candidate-row list. It
scans the exact 102,988-row residual stream and requires:

1. three acyclic singleton contractions giving five quotient classes;
2. six singleton quotient supports forming exactly a `K4`;
3. two doubled quotient supports sharing the fifth class as apex;
4. odd parity on every `K4` support and one odd path in each doubled support;
5. exact positive semidefiniteness and exact total DNN cost five.

Arbitrary singleton parities on contracted supports are handled by switching.
Rows that violate the apex Schur boundary are rejected even when their unsigned
support quotient has the right shape. The verifier reconstructs every row and
Gram, audits all principal minors and the exact canonical budget, rebuilds all
13 physical path coordinates, and checks that precisely the three contracted
coordinates have zero local energy.

The canonical fixture
`rank6_order8_symbolic_templates.json` freezes all 45 source indices, rows,
templates, contractions, and 630 target classifications. Its SHA-256 is
`0511ca60c26dd0a376e09c325b26406dcec0830ca598f747a7b6fd2b4bf03cd3`.

Run:

```sh
python3 positive-square-energy/experiments/rank6_order8_symbolic_recognizers.py
python3 -O positive-square-energy/experiments/rank6_order8_symbolic_recognizers.py
python3 positive-square-energy/experiments/rank6_order8_symbolic_recognizers.py \
  --list-rows
python3 positive-square-energy/experiments/rank6_order8_symbolic_recognizers.py \
  --compare-null-set final-null-set.json
```

The comparison input is either a list or an object with a `null_targets` list;
each entry is exactly `{"source_index": integer, "frontier": null-or-integer}`.
The comparison fails closed on duplicates, missing targets, or unexpected
targets. The artifact keeps `full_theorem=false` because identifying the final
global null set still requires the complete search.
