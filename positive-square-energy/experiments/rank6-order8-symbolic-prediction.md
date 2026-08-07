# Order-eight rank-six symbolic equality prediction

## Prediction

The order-eight census and the order-seven terminal geometry suggest that the
final numerical failures will be a small equality packet rather than a diffuse
tail. Before a complete search exists, the exact combinatorial recognizer finds
the following residual-row candidates:

| geometry | kernels | residual rows |
|:--|:--|--:|
| signed five-cycle | K744, K756 | 12 |
| tetrahedron plus apex | K706, K717, K737, K762, K817, K822, K835, K842, K946, K949, K953, K954, K958 | 33 |
| total | 15 kernels | 45 |

The conservative prediction extrapolates the exact order-seven failure pattern:
the canonical target and the coordinate carried by each zero-cost contraction.
Order seven had two contractions and three failed targets per equality row;
order eight has three contractions and therefore predicts four. This gives
**132 final equality residual targets beyond K744/K756** on the 33 simplex/apex
rows. If the 12 signed-cycle rows had not already been removed before numerical
search, the same rule would predict 48 targets there, for 180 total. The
recognizers actually construct a cost-five Gram and a free `+2` extension for
every coordinate, so all 630 row-target pairs have symbolic coverage if the
numerical search leaves more than the predicted contraction frontiers null.

This is a prediction, not an identification of the eventual null-witness set.
Only the completed search can determine whether all 45 candidates survive as
numerical residuals and whether any noncandidate target remains unresolved.

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

`rank6_order8_symbolic_recognizers.py` derives the simplex/apex kernel list from
the locked kernel fixture. It does not contain an assumed candidate list. It
then scans the exact 102,988-row residual stream and requires:

1. three acyclic singleton contractions giving five quotient classes;
2. six singleton quotient supports forming exactly a `K4`;
3. two doubled quotient supports sharing the fifth class as apex;
4. odd parity on every `K4` support and one odd path in each doubled support;
5. exact positive semidefiniteness and exact total DNN cost five.

Arbitrary singleton parities on contracted supports are handled by switching.
Rows that violate the apex Schur boundary are rejected even when their unsigned
support quotient has the right shape.

Run:

```sh
python3 positive-square-energy/experiments/rank6_order8_symbolic_recognizers.py
python3 positive-square-energy/experiments/rank6_order8_symbolic_recognizers.py \
  --targets all --list-rows
```

The first command reports the conservative 132-target prediction beyond the
preclassified K744/K756 packet (180 including that packet). The second reports
all 630 targets already covered by the templates. The experiment keeps
`full_theorem=false`; it neither substitutes for the complete rational search
nor claims that the prediction is the final null set.
