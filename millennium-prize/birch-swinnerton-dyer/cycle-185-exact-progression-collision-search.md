# Cycle 185: exact progression and Kummer-row collision search

## Fixed fiber

Fix `E=433a1`, `p=7`, `P=(0,1)`, `Q=(-1,1)`, `ell=29`, and

\[
 M=8\cdot7\cdot433\cdot29=703192.
\]

Use the exactly checked small admissible prime `1289` as a Frobenius-fiber
anchor.  Search

\[
 q=1289+kM\qquad(k\geq1).
\]

This congruence gives exactly the same Frobenius in
`Q(zeta_M)`, not merely the same separate residues at selected factors.  It
also fixes the fundamental-discriminant sign convention and the Legendre
symbol at `ell=29` (the common value for the anchor fiber is `+1`).  It does
not fix Frobenius in the nonabelian Kummer
field.

## Dependency-free local screen

For every prime progression term, count `E(F_q)` exactly by the quadratic
character sum on the integral model

\[
 W^2=X^3+X^2+64,
\]

obtained from `X=4x`, `W=4(2y+x)`.  Retain only terms with
`a_q=2 mod 7` and exact `7`-valuation one in `#E(F_q)`.  If
`m=#E(F_q)/7`, compute `[m]P` and `[m]Q`.  These are the images of `P,Q` in
the order-seven quotient.  Find the unique `t in F_7` with
`[m]Q=t[m]P`, with separate handling when `[m]P=0`, and canonicalize the row
projectively.  The verifier independently establishes
`#E(F_1289)=1330`, `a_1289=-40`, and row `(1,1)`, and retains exactly that
projective row.  These local values are not values of `c(1289,29)`.

Run the small first-prime screen with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle185_progression_search.py
```

The script uses only the Python standard library, deterministic Miller--Rabin
below `2^64`, exact finite-field arithmetic, and an exact character sum.  Its
default range reaches the first prime progression term and screens only that
prime.  Increase work explicitly with `--terms` and `--prime-limit`.  The
character sum is linear in `q`, so this is a small-candidate strategy, not a
large-scale replacement for SEA.

## Exact `c(q,29)` stage

Do not infer `c(q,29)` from the progression or local row.  For each retained
prime, produce all 28 exact rational plus modular symbols of `E^(D_q)` using
the pinned producer required by Cycle 182.  Fix `eta=2`, whose order modulo 29
is exactly 28.  Store numerators, denominators, and the discrete logs to `eta`.
A dependency-free
consumer then checks every denominator is a 7-adic unit and recomputes

\[
 c(q,29)=\sum_{a=1}^{28}[a/29]^+_{E^{(D_q)}}\log_\eta(a)\pmod7.
\]

Bucket retained primes by their residue `c in F_7`, and compare a new prime
only against earlier nonempty buckets.  Prioritize a `c=0` versus `c!=0` pair,
but any two distinct residues meet the requested differing-`c` screen.  No
value of `c` is asserted before these exact symbol rows exist.

## Acceptance gate

Matching `q mod M`, residual trace, and projective row is an exact cheap screen
under the maximal semidirect-product identification.  It is not yet the full
Cycle 182 certificate.  Before accepting a pair, provide explicit comparison
maps for the two local quotient lines, certify the actual Galois image and the
Kummer conjugacy class (or a class-separating residue-field witness), replay the
modular-symbol producer, and run the independent rational/mod-7 verifier.  A
factorization type or two matching printed labels is insufficient.

A found zero/nonzero pair refutes governance only by the named field
`L_0`; a finite search with no pair proves no factorization theorem and no BSD
case.
