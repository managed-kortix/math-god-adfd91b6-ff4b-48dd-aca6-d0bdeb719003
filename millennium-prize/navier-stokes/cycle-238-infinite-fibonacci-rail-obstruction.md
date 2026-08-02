# Cycle 238: infinite Fibonacci-rail geometric cancellation obstruction

## Decision

The direct infinite continuation of the Cycle 224 Fibonacci rails with one
geometric amplitude law fails exact off-rail cancellation at depth two.  Let

\[
 k_j=(F_{j+1},F_j),\qquad a_j=A r^{j-1},\qquad Ar\ne0,
\]

and impose reality by giving `-k_j` the same real amplitude.  Exact rational
collection of every rail-pair sum and difference through depth `J=12` produces
a stable one-term equation at the off-rail mode `(1,0)`.  Its saturated ideal is
the unit ideal for every `J>=2`; therefore this obstruction extrapolates to the
full infinite sequence and is not merely a finite-truncation observation.

This retires only this real-even, single-ratio geometric Fibonacci-rail
architecture.  It is not a statement about general infinite tails, Euler
amplification, or Navier--Stokes regularity.

## Exact equations

With the frozen convention `k^perp=(k_2,-k_1)`, an unordered pair contributes

\[
 C(p,q)z_pz_q,
 \qquad
 C(p,q)=-\det(p,q)(|p|^{-2}-|q|^{-2}).
\]

For each canonical off-rail output `m`, the verifier collects all positive-rail
sums `k_i+k_j=m` and differences `k_j-k_i=m` before simplifying.  Under the
geometric ansatz every depth-`J` cancellation equation has the exact form

\[
 A^2\sum_e c_{m,e}r^e=0,
 \qquad c_{m,e}\in\mathbb Q.
\]

The committed certificate stores all 85 equations at `J=12`, including each
contributing pair, interaction type, rational coefficient, and power of `r`.
It also stores counts and SHA-256 digests for every depth from 2 through 12.

## Stable unit-ideal certificate

Already

\[
 k_2-k_1=(2,1)-(1,1)=(1,0).
\]

This representation is unique among the entire infinite rail sequence.  A sum
of two positive rails has positive second coordinate.  A difference has second
coordinate zero only when its Fibonacci coordinates agree; strict growth after
`F_1=F_2=1` leaves only the pair `{k_1,k_2}`.  Its coefficient is

\[
 C(k_2,-k_1)=-\frac3{10},
\]

so exact cancellation requires

\[
 -\frac3{10}A^2r=0. \tag{238.1}
\]

Normalize the generator to `g=A^2 r` and saturate away `Ar=0` with
`h=tA^2r^2-1`.  Over `Q[A,r,t]`,

\[
 tr g-h=1. \tag{238.2}
\]

Thus the saturated cancellation ideal is the unit ideal.  The same equation is
present unchanged at every finite depth `J>=2`, proving the infinite
extrapolation directly.

## Reproduction

Run with Python 3.10 or newer:

```sh
python3 millennium-prize/navier-stokes/verify_cycle238_infinite_rail_cancellation.py \
  --max-depth 12
```

This regenerates
`cycle238-infinite-rail-cancellation-certificate.json` and fails closed if the
stable equation, unique representation, or rational coefficient changes.
