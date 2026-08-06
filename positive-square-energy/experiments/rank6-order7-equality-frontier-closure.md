# Order-seven rank-six equality-frontier closure

## Result

The 39 targets left unresolved by the batched exact Gram manifest are exact
equality cases, not numerical failures. Two rational Gram templates close all
of them at cost five:

| kernel | source indices | unresolved frontiers | exact geometry |
|:--|:--|:--|:--|
| K469 | 10370, 10372, 10427, 10429 | canonical, 0, 10 | tetrahedron plus apex |
| K511 | 14191, 14206, 14225 | canonical, 2, 5 | tetrahedron plus apex |
| K534 | 15904, 15908, 15927 | canonical, 0, 3 | signed five-cycle quotient |
| K548 | 16796, 16800, 16819 | canonical, 0, 3 | signed five-cycle quotient |

This accounts for `4*3+3*3+3*3+3*3=39` targets. Together with the 319,163
exact rational records in the source-locked batched manifest, it closes all
319,202 finite frontier targets.

## K534 and K548

These are the five-cycle equality templates. Their singleton contractions and
mixed doubled bundles are

```text
K534: contractions 03,12; mixed bundles 06,16,25,34,45
K548: contractions 03,12; mixed bundles 06,15,23,45,46
```

Contract each singleton with the sign forced by its path parity. On the five
quotient classes use diagonal one and signed cycle-edge correlation `-1/2`.
The verifier reconstructs the resulting rational 7 by 7 Gram matrix and checks
every principal minor over `Fraction`. Each contraction costs zero. In each
mixed bundle the odd path costs `1/3` and the even path costs `2/3`; hence the
five bundles cost exactly five.

## K469 and K511

The remaining geometry is a regular tetrahedron together with one apex. The
unit tetrahedron Gram has off-diagonal entry `-1/3`. Two signed singleton
contractions identify two additional branch vertices with tetrahedron or apex
vertices. Two mixed doubled bundles have endpoint correlation `-1/2`.

The apex correlations to two tetrahedron vertices are `+/-1/2`, as forced by
the contraction signs. Its correlations to the other two tetrahedron vertices
are equal and chosen so that their sum with the first pair is zero. This is the
exact Schur-complement boundary of the tetrahedron Gram. Rather than relying on
that description, the verifier constructs each matrix and checks all 127
principal minors exactly.

The six remaining odd singleton paths are tetrahedron edges. They each cost
`1/2`; the two mixed bundles each cost one; the two contraction paths cost
zero. The total is therefore `6/2+2=5`.

The contractions and mixed bundles are

```text
K469: contractions 04,35; mixed bundles 06,34
K511: contractions 06,15; mixed bundles 04,14
```

## Uniform lengthening

Every same-parity lengthening is explicit. Insert two copies of the first unit
vector of a certified path immediately after that vector. Both new Gram steps
have correlation one and cost zero. Repeating this operation realizes every
coordinatewise same-parity descendant with exactly the canonical cost. No
continuity argument or floating-point approximation is used.

For a mixed even path, transformed endpoint correlation is `-1/2`. Its exact
length-two midpoint is the normalized endpoint sum, whose correlation with
both endpoints is `1/2`; its two step costs are therefore `1/3+1/3=2/3`.

## Fail-closed audit

`research/rank-six-order-seven-equality-frontier-verifier.py`:

1. locks all six batched chunks by SHA-256 and checks the ordered manifest;
2. reruns the batched exact verifier and requires the partition 319,163 plus 39;
3. requires the closure fixture to equal the actual null-witness target keys;
4. derives every graph ledger from the locked census rather than trusting the
   fixture for rows or path lengths;
5. checks Gram positive semidefiniteness and all costs using only `Fraction`;
6. reruns itself under `python3 -O` and requires byte-identical output.

Run:

```sh
python3 research/rank-six-order-seven-equality-frontier-verifier.py
python3 -O research/rank-six-order-seven-equality-frontier-verifier.py
```

The numerical costs stored in the batched chunks are never read as proof.
