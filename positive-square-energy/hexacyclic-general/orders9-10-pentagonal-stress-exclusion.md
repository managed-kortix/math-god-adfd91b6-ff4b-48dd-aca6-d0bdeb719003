# Orders nine and ten: exclusion of the pentagonal non-CP stress

## Result

The exceptional five-cycle stress from `cost-five-dual-stress-obstruction.md`
cannot itself produce a fourth objective-five profile in the order-nine and
order-ten rank-six ledgers. More precisely, after contracting every path on
which that stress is zero, the surviving stress graph can be a chordless
five-cycle only in kernels `K971` and `K1133`; and every nonempty physical
odd-unit ledger supported by the exceptional stress has irrational objective.
It therefore cannot equal five.

This is an exact exclusion of the **pure pentagonal non-completely-positive
component**. It does not claim that every doubly nonnegative stress has already
been classified, nor does it exclude a stress having both pentagonal and
completely-positive summands.

## 1. Algebraic obstruction

Let

`rho=(1+sqrt(5))/4`.

The null Gram exposed by the exceptional stress has switched correlation
`-rho` on every edge of its chordless five-cycle. The number `rho` satisfies

`4 rho^2-2 rho-1=0`,

and is irrational. An odd unit path on such an edge has cost

`f_1(-rho)=(1-rho)/(1+rho)=(7-8 rho)/5`.             (1)

The last identity follows by multiplying by `1+rho` and using the displayed
quadratic equation. Consequently, if the physical ledger contains `N>0` odd
unit paths on pentagonal stress edges, their total is

`N(7-8 rho)/5`,                                         (2)

which is irrational. Paths contracted into a zero entry of the stress have
zero cost, and extracting tight mixed atoms contributes an integer. Thus no
pure exceptional pentagonal component can make the total objective the integer
five. This strengthens the earlier observation for one copy of each cycle edge:
physical multiplicities cannot cancel the irrational part because every
coefficient has the same sign.

The statement is deliberately about the canonical odd-unit component. An odd
path lengthened to three has the same transformed endpoint correlation but a
different tangent coefficient and a different algebraic cost. An even path is
different again. Such a ledger is not certified by (2); it belongs to the
one-coordinate frontier or to a mixed KKT stress, both of which remain outside
this proposition. Likewise, multiple odd unit paths on one quotient edge need
not reproduce the normalized stress unless their total derivatives balance
around the cycle. The irrationality argument is a necessary obstruction for
every such pure realization, not an assertion that every projected
multiplicity histogram satisfies the KKT equations.

## 2. Exact cubic/near-cubic path ledger

There are fourteen physical paths at order nine and fifteen at order ten. The
degree partitions are respectively

```text
order 9:  4,3,3,3,3,3,3,3,3,
order 10: 3,3,3,3,3,3,3,3,3,3.
```

The verifier reads the locked rank-six kernel fixture and performs the following
finite projection for every one of the 162 near-cubic order-nine kernels and 66
cubic order-ten kernels.

1. Choose five support pairs to survive.
2. Contract every other support pair and reject a contraction cycle.
3. Require exactly five quotient classes.
4. Require the five surviving pairs to be distinct and 2-regular on the
   quotient, hence a chordless `C5`.
5. Record the five physical multiplicities.

Only one kernel at each order survives:

```text
order 9:  K971
order 10: K1133.
```

The exact multiplicity histograms over all contraction forests are

```text
                 11111  11112  11122  11222  12222  22222
order 9, K971:       0      5     40     60     20      1
order 10, K1133:     1     25    100    100     25      1
```

In particular, every projected pentagon has a nonempty surviving physical
ledger. Equation (2) excludes objective five for a pure exceptional component
in every case, including the all-doubled projections already underlying the
known mixed-five-cycle profile. In that known profile the odd and even members
are first paired into five scalar cost-one atoms; their derivatives cancel, so
the exceptional pentagonal matrix is not the residual dual stress.

## 3. Reproduction

Run the exact verifier in normal and optimized modes:

```sh
python3 positive-square-energy/experiments/rank6_orders9_10_pentagonal_stress_obstruction.py
python3 -O positive-square-energy/experiments/rank6_orders9_10_pentagonal_stress_obstruction.py
```

The script pins the source SHA-256, kernel identities, and every multiplicity
histogram. It uses only integer graph operations for the ledger projection and
records the quadratic identity used in the algebraic exclusion.

## Boundary of the result

This closes the concrete hostile test posed by the earlier dual-stress note:
the minimal non-CP `C5` stress cannot be a realizable fourth optimum profile at
objective exactly five in orders nine or ten. The remaining classification
obligation is narrower but genuine: exclude larger exceptional DNN stresses and
mixed CP/non-CP stresses, or prove that the physical rank-six KKT equations split
them into the three known completely-positive atom profiles.
