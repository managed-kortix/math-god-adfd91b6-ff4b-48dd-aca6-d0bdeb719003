# Four-vertex rank-four kernels: exact census and certificate blocker

## Status

This file does **not** claim the four-vertex DNN theorem.  The requested exact
census is reproducible, and 33 switching-orbit representatives have exact Gram
matrices of canonical excess at most three.  Those representative certificates
do not, however, transport to all 342 physical bundle-count rows while keeping
their physical odd/even canonical path costs.  The accompanying verifier fails
closed at that point.

## Exact physical census

Use the edge order `01,02,03,12,13,23`.  The five four-vertex kernels from the
rank-four kernel classification are

`(0,1,2,1,2,1)`, `(0,1,2,2,1,1)`, `(0,1,2,2,2,0)`,
`(0,1,2,3,1,0)`, and `(1,1,1,1,1,2)`.

For a multiplicity vector `m`, a physical bundle-count row is an integer vector
`q` with `0<=q_e<=m_e`; `q_e` is the number of physically odd paths in that
parallel bundle.  Independent Cartesian enumeration therefore gives

| kernel | physical rows |
|:---|---:|
| `(0,1,2,1,2,1)` | `72` |
| `(0,1,2,2,1,1)` | `72` |
| `(0,1,2,2,2,0)` | `54` |
| `(0,1,2,3,1,0)` | `48` |
| `(1,1,1,1,1,2)` | `96` |
| total | `342` |

Switching a branch vertex replaces `q_e` by `m_e-q_e` in every incident
bundle.  Quotienting by the eight switch patterns (modulo global switching) and
by each kernel's full vertex automorphism group gives respectively

`6,6,7,6,8`,

hence exactly 33 orbits.  The verifier derives these numbers rather than
reading a row list.

## Exact candidate certificates

`research/rank-four-four-vertex-dnn-verifier.py` contains one immutable
certificate record for each of the 33 canonical orbit representatives.  In 32
records, four rational parameters `a_i` specify planar vectors at angles
`4 atan(a_i)`.  For an edge `ij`, put

`t_ij=|tan((theta_i-theta_j)/4)|`.

The verifier obtains this rationally from

`|(a_i-a_j)/(1+a_i a_j)|`, reduced to the smaller-angle value, and checks

`r_ij=(1-6t_ij^2+t_ij^4)/(1+t_ij^2)^2`,

`c_odd(t_ij)=(1-t_ij^2)^2/(4t_ij^2)`,

`c_even(t_ij)=2t_ij^2`.

The remaining record is the regular-simplex Gram matrix, encoded by
`t_ij^2=1/3` on every pair.  Its correlations are `-1/3`, every odd canonical
cost is `1/3`, and every even canonical cost is `2/3`.

For every representative the program constructs every Gram entry as a
`Fraction`, checks all 15 principal minors are nonnegative by exact rational
Gaussian elimination, computes the exact weighted path excess, and verifies it
is at most three.  The largest is exactly three.

## Why this is not yet a theorem

Switching is valid for naming signed-kernel orbits and changing Gram-vector
signs, but it does not change a physical path length.  In particular, a
certificate checked only after replacing `q_e` by `m_e-q_e` may exchange the
odd cost with the even cost in a bundle.  The transformed matrix must therefore
be substituted back into the original physical row and rechecked there.

The verifier performs that substitution for the rational planar records.  Some
transported rows either place an odd path at a zero-cost denominator boundary
or have exact excess greater than three.  The regular-simplex boundary record
also does not provide rational transported costs after a nontrivial sign
switch.  Consequently the 33 representative checks are insufficient to cover
the 342 physical rows.

Run the audit with

```text
python research/rank-four-four-vertex-dnn-verifier.py
python -O research/rank-four-four-vertex-dnn-verifier.py
```

It prints the exact census and representative maximum, reports the number of
failed physical transports, and then raises

`BLOCKER: orbit representatives do not certify every physical row`.

An actual theorem artifact requires either an exact certificate attached to
each physical row (certificates may be shared only after direct physical-cost
verification), or a symbolic transport argument that preserves the physical
canonical costs.  Neither is supplied here, so no four-vertex DNN theorem or
tetracyclic closure is claimed.
