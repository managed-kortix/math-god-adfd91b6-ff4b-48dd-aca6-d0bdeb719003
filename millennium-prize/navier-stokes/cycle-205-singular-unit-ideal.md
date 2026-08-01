# Cycle 205: Singular unit-ideal campaign

## Outcome

All 514 frozen Cycle 204 equations were translated verbatim from the committed
JSON ledger into a 36-variable Singular ideal over `Q`.  Exact rational row
reduction of the 44 linear equations has rank 27 and leaves nine variables.
Substitution into all 514 equations gives 36 nonzero source images and 22
distinct primitive equations: 14 quadratics and 8 cubics. The corrected
terminal rows have the same reduced image.

Singular computes the reduced ideal as the unit ideal over each of

```text
32003  32009  32027  32029  32051
```

and independently over `Q`.  Every modular reduced Groebner basis is the
singleton `[1]`.  These modular runs are reconnaissance: by themselves they do
not prove characteristic-zero infeasibility, since reduction can enlarge an
ideal at exceptional primes.

## Rational reconstruction and certificate

The repeated modular support indicates a sparse low-degree certificate.  There
is no need to perform CRT coefficient reconstruction here because Singular's
exact `Q` lift recovers and verifies one directly.  In the reduced generator
order `r00,...,r21`, with

```text
x2 = q1_o9_planar_im
x5 = q1_o10_planar_re
```

the certificate is

\[
  -\frac14r_{00}
  +\left(\frac{x_2}{16}+\frac34\right)r_{01}
  -\frac14r_{02}
  +\left(-\frac{x_2}{16}+\frac34\right)r_{03}
  +\frac12r_{06}
  +\frac{x_5}{48}r_{20}
  -\frac{5x_5}{48}r_{21}=1.
\]

The generated Singular script multiplies the generator row by this coefficient
column and prints remainder zero.  A second, independent `lift` against the
original 514-generator ideal also returns a sparse certificate and verifies its
remainder as zero.  Thus the full frozen ideal is `(1)` over `Q`, and hence has
no rational, real, or complex point.

A reconstruction workflow for a larger instance would retain the coefficient
support from several good primes, CRT-lift each integer residue, use rational
reconstruction after the modulus exceeds the coefficient-height bound, and
accept the result only after exact expansion of `sum h_i f_i=1` over `Q`.
The exact `Q` lift and remainder checks in this campaign perform that final,
decisive step without relying on an assumed height bound.

## Reproduction and artifacts

Run the complete campaign with

```sh
python3 millennium-prize/navier-stokes/run_cycle205_singular.py
```

The exact transcript is `cycle205_singular.log`; its final status is `PASS`.
The SHA-256 and byte size of every source and generated artifact are in
`cycle205_manifest.json`.  `generate_cycle205_singular.py --check` regenerates
all Singular inputs and the reduction ledger byte for byte.

The principal artifacts are:

```text
cycle205_full_qq.sing                 all 514 equations over Q
cycle205_linear_reduction.json        exact rank-27 substitutions and 22 equations
cycle205_mod_*.sing                   five modular Groebner runs
cycle205_reduced_qq.sing              reduced rational certificate and check
cycle205_full_certificate_qq.sing     original-514 rational certificate and check
cycle205_singular.log                 exact command/output transcript
cycle205_manifest.json                hashes, sizes, commands, and exit codes
```

This is an exact obstruction only to the pinned seed, frozen support, terminal
policy, and two-jet tangency system encoded by Cycle 204.  It is not a
Navier--Stokes regularity or blowup result.
