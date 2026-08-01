# Cycle 236: strategic rotation after `CA235 FAIL`

## Decision

Rotate the main funnel out of Yang--Mills. Cycle 235's explicit finite-lattice
strong-coupling gap is preserved, but the Cycle 236 audit finds no
non-equivalent scale-uniform continuum lemma with both an exact finite falsifier
and transfer to an official quantifier. Keeping Yang--Mills because of the
bounded theorem would violate the frozen stop rule.

The portfolio review selects BSD's effective integral Heegner--Kolyvagin packet
for one fixed rank-one curve. It is the only currently stated candidate that
crosses its lane's barrier, is non-equivalent to the official problem, and has
an exact finite falsifier. Success would remain a fixed-curve reduction, not a
proof of BSD.

## Six-lane review

Use the established lexicographic score

\[
 L=(\text{barrier crossing},\text{non-equivalence},
     \text{finite falsifiability},\text{official transfer}).
\]

| lane | score | Cycle 236 status |
|---|---|---|
| BSD | `(1,1,1,0)` | The Cycle 224 integral Heegner--Kolyvagin packet would replace isolated primary checks by one effective finite-prime reduction for a fixed curve; every datum and bound has a finite exact rejection condition. |
| Navier--Stokes | `(1,1,0,1)` | The factor-two `L^3` lemma has official transfer, but fixed finite Fourier support is rigid and the last finite packet failed. No scale-uniform infinite-tail candidate is frozen. |
| Hodge | `(1,1,0,0)` | The relative-Chow target remains separated, but degree-one and degree-two carriers failed consecutively; the stop rule forbids unsupported escalation. |
| RH | `(1,0,0,1)` | Nyman--Beurling and canonical endpoint limits retain official transfer but the production estimate is RH-strength and has no separated finite falsifier. |
| P versus NP | `(0,1,1,0)` | All-order OBDD hardness is exact but does not cross the unrestricted-circuit/MMW relational transfer barrier. |
| Yang--Mills | `(0,1,0,0)` | The proved theorem is off the continuum trajectory; the RG candidate lacks an analytic tail falsifier and the full-complement candidate is gap-equivalent. |

BSD wins lexicographically. This does not authorize more isolated Kurihara
prime checks: the promoted object is the effective all-primary reduction, not
another primary certificate.

## Frozen checkpoint `HK236`

Fix `A=433a1^(-1499)` and the initial field candidate
`K=Q(sqrt(-115))`. The checkpoint must supply all of the following.

1. Certify the Heegner hypothesis, rank-zero twist nonvanishing, optimal
   parametrization, CM divisor, trace, differential, period, and Manin
   conventions defining one integral trace `y in A(Q)`.
2. State and verify an integral Kolyvagin divisibility
   `#Sha(A/Q) | (C_A I_A)^2`, where
   `I_A=[A(Q)_free:Z y]` and every local, Tamagawa, denominator, residual, and
   primitivity contribution to the integer `C_A` is explicit.
3. Give directed bounds `0<h_min<=hhat(G)` for every non-torsion rational
   `G` and `hhat(y)<=H`, then print the integer cutoff
   `M=floor(sqrt(H/h_min))` and `B_A=max(M,P^+(C_A))`.
4. Print the complete remaining list of primes `p<=B_A` after removing the
   already certified primary parts, together with an exact proposed Selmer,
   Kurihara, or Kolyvagin-localization test for each prime.

`HK236 PASS` requires all four items. `FAIL` is an exact contradiction in the
named Heegner datum, nonvanishing, divisibility hypotheses, or directed height
budget. `WALL` is a written proof that the required effective integral factor
or global height bound is unavailable without assuming the same fixed-curve
primary conclusion. Only `PASS` authorizes the finite primary computations.
`FAIL` or `WALL` retires this curve/field architecture and returns to portfolio
review; do not cycle through nearby quadratic fields.

Passing `HK236` would show only that `Sha(A/Q)=1` reduces to a finite explicit
list. Closing that list would prove a refined fixed-curve consequence. Uniform
rank and leading-term formulas for all elliptic curves, and the general
abelian-variety BSD statement, remain later official gates.

No Millennium problem is claimed solved.
