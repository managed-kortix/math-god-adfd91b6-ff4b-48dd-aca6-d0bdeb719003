# Orders nine and ten: exclusion of long odd-cycle DNN stresses

## Result

After the pentagonal hostile test, the next exceptional support graphs are the
chordless odd cycles `C7` and `C9`. Neither can supply a fourth objective-five
profile in a rank-six order-nine or order-ten path ledger. Exact contraction
enumeration shows that both supports occur only in `K971` and `K1133`, and a
uniform feasible comparison puts the optimum of every nonempty pure long-cycle
component strictly between zero and one. Adding integral tight atoms therefore
cannot produce the integer objective five.

This closes all **chordless odd-cycle support graphs** on at most ten quotient
vertices: `C5` is handled in `orders9-10-pentagonal-stress-exclusion.md`, while
this note handles `C7` and `C9`. It does not classify exceptional DNN matrices
whose support properly contains an odd cycle, or mixed CP/non-CP stresses.

## 1. Why these are the remaining cycle supports

A graph is a completely-positive graph precisely when every doubly
nonnegative matrix with that graph is completely positive. The standard graph
characterization says that failure occurs exactly when the graph contains an
odd cycle of length at least five. For a support graph that is itself a
chordless cycle on at most ten vertices, the only exceptional possibilities are
therefore `C5`, `C7`, and `C9`.

For a comparison Gram on `Cq`, take successive planar unit vectors with
switched endpoint correlation

```text
-cos(pi/q).
```

One odd unit path on a surviving cycle edge then has objective

```text
t_q = (1-cos(pi/q))/(1+cos(pi/q)) = tan^2(pi/(2q)).
```

Chebyshev elimination gives the relevant algebraic equations

```text
q=7:  7 t^3 - 35 t^2 + 21 t - 1 = 0,
q=9:  3 t^3 - 27 t^2 + 33 t - 1 = 0.
```

Exact sign evaluation at rational endpoints isolates the desired roots as

```text
0 < t_7 < 1/16,      0 < t_9 < 1/30.
```

The rational-root theorem also shows that both roots are irrational. The
inequalities, rather than irrationality alone, give the stronger exclusion.
Crucially, the comparison Gram need not be the Gram exposed by the putative
stress and the physical multiplicities need not balance around the cycle.

## 2. Uniform objective obstruction

A rank-six kernel of order at most ten has at most fifteen physical paths.
Assign the comparison vectors above to its quotient classes. For every
surviving transformed odd path, choose the equal-angle geodesic subdivision.
If its length is `l`, its contribution is

```text
l tan^2(pi/(2ql)) <= t_q.
```

Thus the component optimum `E` satisfies

```text
C7:  0 < E <= 15 t_7 < 15/16 < 1,
C9:  0 < E <= 15 t_9 < 1/2 < 1.
```

The lower bound is also strict. Zero objective would force every transformed
edge correlation to its zero-cost endpoint, which cannot be signed consistently
around an odd cycle. Compactness then gives `E>0`. This argument applies to
arbitrary positive edge weights, multiplicities, and odd path lengths; it does
not classify the corresponding DNN stress ray.

Every extracted tight mixed pair or regular simplex atom has integral total
cost in the profile ledger. If the whole objective were five, the residual
long-cycle component would consequently have integral value. No number in
`(0,1)` is integral. This excludes pure `C7` and `C9` residual stresses without
assuming equal physical multiplicities and without relying on cancellation of
irrational coefficients.

## 3. Exact order-nine and order-ten projection

For each frozen near-cubic order-nine kernel and cubic order-ten kernel, the
verifier contracts a forest of zero-stress supports, retains exactly `q`
distinct support pairs, and requires the quotient to be 2-regular on `q`
classes. The complete surviving multiplicity histograms are

```text
order 9,  C7, K971:   1111222:10  1112222:20  1122222:6
order 9,  C9, K971:   111122222:1

order 10, C7, K1133:  1111122:10  1111222:50  1112222:50  1122222:10
order 10, C9, K1133:  111112222:5  111122222:5
```

No other one of the 162 order-nine or 66 order-ten kernels has such a quotient.
All rows are nonempty, so the strict lower bound in the preceding section
applies.

## 4. Reproduction and boundary

Run the integer/algebraic verifier in both modes:

```sh
python3 positive-square-energy/experiments/rank6_orders9_10_long_odd_cycle_stress_obstruction.py
python3 -O positive-square-energy/experiments/rank6_orders9_10_long_odd_cycle_stress_obstruction.py
```

The verifier pins the kernel fixture hash, reproduces every contraction
histogram, checks the rational isolating intervals, and checks the rational-root
obstructions without floating point.

The next unresolved finite class is not another chordless cycle. It consists of
exceptional supports on at most ten vertices that properly contain a long odd
cycle, together with stresses mixing exceptional and completely-positive
summands. Any complete obstruction theorem must reduce those supports to their
extremal DNN rays or prove directly that the physical KKT face splits.
