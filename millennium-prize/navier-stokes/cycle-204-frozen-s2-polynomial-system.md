# Cycle 204: frozen exact S2 polynomial system

## Frozen data

The generator implements the Cycle 203 quadratic-order gate for the small
Cycle 177 packet at `R=Y=nu=1`.  The pinned nonzero Fourier coefficients are

\[
 u_{(\pm2,0,0)}=u_{(\pm6,0,0)}=e_2,
\]

\[
 u_{(-2,1,0)}=u_{(2,-1,0)}=e_3,
 \qquad
 u_{(2,1,0)}=u_{(-2,-1,0)}=-e_3.
\]

The committed support file constructs, rather than hand-lists,

\[
 S_2=(K_0\cup(K_0+K_0))\setminus\{0\},\quad
 U_2=(S_2+S_2)\setminus\{0\},\quad
 U_3=(S_2+U_2)\setminus\{0\}.
\]

The exact counts are

| set | modes | conjugate orbits where applicable |
|---|---:|---:|
| `K0` | 8 | 4 |
| `S2` | 30 | 15 |
| `U2` | 122 | 61 |
| `U3` | 278 | 139 |
| `(U2 union U3) minus S2` | 248 | 124 |

Here `S2` is the frozen first-completion support, not a second elementary
symmetric polynomial.

## Terminal/Q1 reconciliation

The terminal quartet

\[
 Q=\{(\pm8,\pm1,0)\}
\]

lies in `S2` but is absent from the initial seed.  It consists of two Fourier-
reality orbits, not one.  To retain the prep support/coordinate convention
without changing the strategic gate, the support JSON declares the same four
real Q1 coordinate slots (two complex divergence-free coordinates) on every
helper orbit in `S2 minus K0`, including each terminal orbit.  The eight real
terminal slots are marked `pinned_zero_terminal` and substituted as zero before
expansion.  They therefore remain auditable support coordinates but are not
completion freedoms.

There are 11 declared helper orbits and 44 declared real Q1 slots.  Removing
the two terminal orbits leaves 9 free helper orbits and 36 active real
variables.  This realizes simultaneously:

1. the strategic requirement that terminal modes are initially absent; and
2. the prep requirement that the frozen support ledger include their Q1
   coordinate slots.

The two terminal first derivatives are not free normalizations.  With the
fixed Fourier convention

\[
 N_k(u)=-|k|^2u_k-iP_k\sum_{a+b=k}(u_a\mathbin\cdot b)u_b,
\]

the pinned seed gives exactly

\[
 P_{1,(-8,-1,0)}=-i e_3,
 \qquad P_{1,(8,-1,0)}=+i e_3,
\]

with reality mates

\[
 P_{1,(-8,1,0)}=-i e_3,
 \qquad P_{1,(8,1,0)}=+i e_3.
\]

The generator independently recomputes all four values directly from a second
seed coefficient table, separately from the polynomial-field construction. It
includes the two representative equalities only after that check. Thus it uses
neither an arbitrary rescaling nor the weaker slack-variable nonvanishing chart.

## Exact generator

Each free orbit uses a rational basis of `k perp`: the primitive planar vector
`(-k_2/gcd(|k_1|,|k_2|), k_1/gcd(|k_1|,|k_2|), 0)` and `e_3`.  Their complex
coefficients have independent real and imaginary rational variables; negative
modes are inserted by Gaussian conjugation.  All arithmetic is implemented
directly over `Fraction`, with Gaussian-rational polynomial pairs.  No floating
point arithmetic, symbolic dependency, pressure variable, or Galerkin deletion
appears.

The generator computes the full ordered convolution, applies the exact Leray
projector at every nonzero output, and forms

\[
 P_1=N(u_0),\qquad P_2=DN(u_0)[N(u_0)].
\]

It imposes `P1=0` on `U2 minus S2`, `P2=0` on
`(U2 union U3) minus S2`, and the two representative terminal derivative
equalities.  Because `S2` is contained in `U2`, and `U2` in `U3` for this
concrete packet, the tested union has 278 modes.  Two independent transverse
components per representative orbit replace redundant three-component Leray
equations.

## Simplified system

Exact expansion produces 688 real scalar slots.  Primitive normalization
clears rational denominators, divides integer content, and fixes sign.  Removing
152 identically zero slots and merging 22 duplicate nonzero slots leaves 514
distinct equations over `Z`:

| degree | equations |
|---:|---:|
| 1 | 44 |
| 2 | 238 |
| 3 | 232 |

No nonzero constant equation appears, so there is no trivial contradiction.
No Groebner basis, resultant, numerical search, or solution attempt was run.
The Cycle 204 terminal-receiver pivot in
`cycle-204-low-degree-receiver-elimination.md` remains a useful subsystem, but
its helper contamination means it is not by itself a certificate for this full
514-equation ideal.

The JSON equation format stores the ordered variable ledger, source jet/wave/
component metadata, integer coefficients, and monomials as repeated variable
names.  It is suitable for exact replay or translation into a computer algebra
system without reparsing formatted mathematics.

## Reproduction

Generate both artifacts with

```sh
python3 millennium-prize/navier-stokes/generate_cycle204_s2_system.py
```

Replay all construction, count, simplification, hash, and byte checks with

```sh
python3 millennium-prize/navier-stokes/generate_cycle204_s2_system.py --check
python3 millennium-prize/navier-stokes/verify_cycle204_hostile_independent.py
```

The second command uses a separate polynomial and Gaussian-arithmetic
implementation, reconstructs the support and both jets without importing the
generator's field or convolution routines, checks the two terminal signs from
the seed convolution, and compares the resulting primitive equation set with
both the regenerated and committed artifacts.

The frozen artifacts are `cycle204_s2_support.json` and
`cycle204_s2_equations.json`.  This is an exact bounded polynomial feasibility
system, not a solution or obstruction certificate and not a Navier--Stokes
regularity result.
