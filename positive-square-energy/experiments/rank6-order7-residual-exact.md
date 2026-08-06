# Exact closure of the 39 order-seven Gram residuals

## Result

All 39 residual targets in the batched order-seven frontier have exact PSD Gram
certificates of cost exactly five. No deletion packet is needed. The residuals
are the canonical target and two zero-cost coordinate lengthenings on each of
13 source rows.

The exact verifier is `rank6_order7_residual_exact.py`. It reads the frozen
frontier census, reconstructs all 39 target path ledgers, and checks symmetry,
unit diagonal, positive semidefiniteness, and exact cost over `Fraction` and
SymPy rationals.

## Signed five-cycles

The six rows on `K534` and `K548` give 18 targets. Contract the signed singleton
forest `03,12`. On the resulting five classes use the signed-cycle matrix

```text
Q_ii = 1,
Q_ij = -s_ij/2  on the five quotient-cycle edges,
Q_ij = 0         otherwise.
```

Pulling `Q` back through the signed contraction gives the displayed branch
Gram matrix algorithmically. Switching reduces `Q` to a balanced or unbalanced
five-cycle matrix, so it is PSD. Each mixed doubled bundle costs
`1/3 + 2/3 = 1`; both singleton paths cost zero. The total is exactly five.
The unresolved frontiers lengthen a singleton path and therefore still cost
zero on that path.

## Structural matrices

The four `K469` rows use `A469` and switches at vertices 3 and/or 4:

```text
A469 =
[ 1, 1/2, 1/2,-1/2, 1,-1/2,-1/2]
[1/2, 1,-1/3,-1/3,1/2,-1/3,-1/3]
[1/2,-1/3, 1,-1/3,1/2,-1/3,-1/3]
[-1/2,-1/3,-1/3, 1,-1/2, 1,-1/3]
[ 1, 1/2, 1/2,-1/2, 1,-1/2,-1/2]
[-1/2,-1/3,-1/3, 1,-1/2, 1,-1/3]
[-1/2,-1/3,-1/3,-1/3,-1/2,-1/3, 1].
```

Its nonzero characteristic factor is

```text
(3x-4)(18x^3-102x^2+143x-28)/54.
```

The three `K511` matrices and their complete rational entries are recorded in
the verifier. For the first, the nonzero characteristic factor is

```text
(3x-8)(3x-4)(2x^2-6x+1)/18.
```

The verifier does not rely on numerical roots. For every matrix it finds a
positive-definite full-rank principal block using exact positive leading
minors and checks that the exact Schur complement is zero. This proves PSD.

On each structural row, six odd paths have branch correlation `-1/3`, hence
cost `1/2` each. Two mixed doubled bundles cost one each. Every remaining path
has transformed endpoint correlation one and costs zero, including the two
lengthened frontiers. Thus every target has exact total

```text
6(1/2) + 2(1) = 5.
```

## Reproduction

```sh
python3 positive-square-energy/experiments/rank6_order7_residual_exact.py
```

The terminal line is:

```text
exact_targets=39 unresolved=0 all_costs=5 psd=true
```
