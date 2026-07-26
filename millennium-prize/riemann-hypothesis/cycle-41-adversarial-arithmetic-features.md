# Cycle 41: adversarial arithmetic features for negative H bands

## Scope and protocol

This is a finite diagnostic on the 2,046 certified Cycle 40 unit signs for
`2 <= n <= 2047`. There are 12 negative cells in six bands:

```text
2, 39-40, 95-96, 99-100, 219-222, 226.
```

The label is the certified Arb sign of the half-surplus, equivalently the sign
of `H_n` because its multiplier is positive. Every arithmetic covariate is an
integer: Mobius and Mertens values, factor counts, primality and prime-power
indicators, enclosing prime gaps and distances, squarefree run lengths and
window counts, and integer prime-power mass proxies. The proxy gives a jump at
`p^k` the integer weight `bit_length(p)`; it locates exact Chebyshev-psi jump
support without importing floating logarithms into the features. Floating
point is used only inside statistical classifiers.

Class imbalance is severe. Accordingly, random train/test splitting and raw
accuracy are rejected. Reported classification uses leave-one-contiguous-
32-cell-block-out predictions, class weighting, balanced accuracy, ROC AUC,
and average precision. A second test removes an entire negative band before
fitting, so adjacent members cannot leak its identity.

## Simple hypotheses are false

No tested one-feature threshold is an iff condition.

| Hypothesis | best threshold | TP / FP / TN / FN | balanced accuracy |
|---|---:|---:|---:|
| enclosing prime gap | `gap <= 4` | 6 / 251 / 1783 / 6 | 0.6883 |
| Mertens jump `mu(n)` | `mu(n) > -1` | 10 / 1417 / 617 / 2 | 0.5683 |
| psi jump support/mass | `mass <= 2` | 12 / 1711 / 323 / 0 | 0.5794 |
| left squarefree run | `run > 2` | 3 / 254 / 1780 / 9 | 0.5626 |

Thus the bands are neither large-gap events nor prime-power jump events. They
also cross squarefree/nonsquarefree boundaries, and a local Mobius jump has
almost no discriminating value. These failures are structural, not merely one
near-threshold miss: each rule has either many false negatives or hundreds to
thousands of false positives.

The strongest scalar association is the Mertens level:

```text
H_n < 0 observed  ==>  M(n) >= 0.
```

It captures all 12 negatives but also 708 positives. It is therefore a finite
necessary observation, not a sufficient condition. Backward eight-cell
Mertens mass ranks second and already misses two negative cells.

## Adversarial classification

The blocked models rank negatives above positives to some extent but do not
identify them reliably:

| model | average precision | ROC AUC | balanced accuracy at 0.5 | TP / FP / TN / FN |
|---|---:|---:|---:|---:|
| balanced logistic | 0.1978 | 0.9508 | 0.6551 | 4 / 47 / 1987 / 8 |
| shallow Extra Trees | 0.0453 | 0.8213 | 0.7242 | 6 / 105 / 1929 / 6 |

Average precision is the important warning: its random baseline is only
`12/2046 = 0.00587`, so there is signal, but precision remains far too low for
a law. Leave-one-negative-band-out Extra Trees recalls both cells at `39-40`
and `95-96`, only one at `99-100`, and none at `2`, `219-222`, or `226` at the
fixed 0.5 threshold. The largest band is not predicted when withheld. This
falsifies the idea that one stable local signature explains all bands.

## Candidate deterministic screen

Searching conjunctions of at most three exact integer thresholds gives the
shortest high-purity necessary screen found in this feature family:

```text
M(n) >= 0
and psi_bit_mass[n-3,n] <= 8
and psi_bit_mass[n,n+3] - psi_bit_mass[n-3,n] <= 8.
```

It contains all 12 observed negative cells, but also 221 positive cells. In
particular `n=65, 93, 94, 97, 98, 101, 145, ...` immediately falsify its
sufficiency. The corresponding depth-three class-balanced decision tree finds
the same condition, so the rule is not an independent confirmation; it is a
post-selected candidate for further algebraic analysis.

The defensible finite conclusion is asymmetric: negative H requires a locally
quiet prime-power environment while the cumulative Mobius balance is
nonnegative in this range, but these arithmetic facts are very far from
determining the sign. H depends on the full Vasyunin Gram history, and the poor
band transfer is evidence against reducing it to any one of the four proposed
local mechanisms.

## Reproduction

The script writes all 2,046 integer rows and a machine-readable report:

```text
cycle41-data/integer-features.csv
cycle41-data/summary.json
```

Run:

```text
uv run --with scikit-learn python cycle41_adversarial_features.py
python -m unittest -v test_cycle41_adversarial_features.py
```

This analysis proposes no asymptotic deterministic law, positivity theorem, or
RH result.
