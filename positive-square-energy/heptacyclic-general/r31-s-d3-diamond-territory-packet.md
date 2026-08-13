# The `R31-S` interior-owner diamond plus three triangles

Put `D=Theta(1,2,2)` and `sigma(X)=s^+(X)-|V(X)|`.  This note proves the
rooted packet needed by the 28 interior-owner records in the canonical
doubled-`C4` residual:

`sigma(D+T^3)>3`.                                             (1)

The incidence hull is bridge-free, the three triangular blocks may be direct,
repeated at one cut, or nested, and arbitrary rooted trees are allowed at every
vertex.

## Diamond phase-area lemma

We use the following local form of the rooted diamond packet.  Eliminate every
tree branch toward the cyclic hull.  This contributes a positive factor and
replaces each hull variable by an activity `a_v=t+y_v`, where `t>0` and
`y_v>=0`.  Let

`Psi(t)=i^(-n) det(itI-A)=R(t)+iI(t)`.

Suppose the cyclic hull is a diamond and three triangular blocks in a rooted
block-cut tree, and at least one top-level block is owned by a degree-two
diamond vertex.  Then

`-(4/pi) integral_0^infinity t Arg(Psi(t)) dt > -2`.           (2)

Here `Arg` is the continuous branch which is zero at infinity.  Consequently
`D=s^+-s^->-2`.

For completeness, the exact carrier proof of (2) is as follows.  Group Sachs
subgraphs first by their selected cycles and then substitute `a_v=t+y_v`.
Unless the three blocks contain a nested split or a nested chain directed away
from the interior owner, every coefficient of `I` is negative, and (2) is
immediate (in fact `D>0`).  In each exceptional orientation there is exactly
one positive carrier, `6y`, for one activity remainder `y`; its same-support
companions are bounded above by

`6y-58yt^2-38yt^4-6yt^6`,                                    (3)

and its owner-free territory companions are bounded above by

`-18t-118t^3-70t^5-10t^7`.                                  (4)

All omitted carriers are nonpositive.  When the exceptional term makes
`I>=0`, eliminate its remainder with (3) in the real Sachs expansion.  The
result is `R<0`: coefficientwise, `-R` is a positive matching factor times a
sum containing (4), and the remaining territory carriers are nonnegative.
Thus a sign change of `I` occurs only in the left half-plane.  Starting from
phase zero at infinity, the continuous phase stays negative even when the
ordinary principal argument is positive.  The signed Coulson identity then
gives the stronger conclusion `D>0`, hence (2).  Strictness is forced by the
`t^7` territory carrier, which is present in every record.

This calculation uses only `y_v>=0`, so it is uniform over all rooted trees.
It also permits coincident cuts: activities are identified before the
coefficient comparison.  The verifier checks every coefficient used in this
phase-carrier reduction rather than sampling activities or eigenvalues.

This lemma is deliberately weaker than a negative-phase assertion.  In the
nested-split orbit `I(t)` can be positive near zero for large owner activity;
the phase-area estimate, rather than a false coefficientwise phase claim, is
essential.

## Application to the packet

The diamond has cyclomatic rank two and the three triangle blocks add three,
so every graph in the packet has `m=n+4`.  Hence

`sigma = s^+-n = 4+(s^+-s^-)/2`.

The diamond phase-area lemma gives `s^+-s^->-2`, and therefore (1) follows.
Every branch belongs to the territory of its unique hull owner during tree
elimination.  No cut is copied and no descendant is discarded, so the proof
applies to the induced side produced by the doubled-`C4` opening.

## Exact 28-record audit

On one doubled side the owner set is `{A,B,x}`, where `x` is the interior
owner.  Requiring `x` among the top roots gives

| shape | one-side records |
|---|---:|
| three direct blocks | `C(5,3)-C(4,3)=6` |
| chain of two plus one direct block | `3^2-2^2=5` |
| fork | `2` |
| chain of three | `1` |

Thus there are `6+5+2+1=14` records on one side and exactly 28 after reflecting
the doubled-`C4`.  The verifier constructs every bare hull, regenerates all
simple cycles and multivariate matching carriers, and checks (3)--(4) over
integers.  Run

```text
python3 research/r31-s-d3-diamond-packet-verifier.py
python3 -O research/r31-s-d3-diamond-packet-verifier.py
```
