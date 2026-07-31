# Five-vertex rank-four kernels: closure of the eight residual rows

## Theorem

Use pair order

`01,02,03,04,12,13,14,23,24,34`.

Every simple subdivision in any of the eight physical rows left by the exact
three-color sieve satisfies

`s^+(G)>=|V(G)|`

after arbitrary rooted trees are attached at arbitrary vertices.  The
canonical equality family in item 2 is asserted only non-strictly; the frozen
frontiers have strict auxiliary slack. The eight
canonical rows are

| kernel | physical row |
|---:|:---|
| 9 | `(0,0,0,1,1,0,1,1,0,0)` |
| 9 | `(0,0,1,1,1,0,1,1,0,0)` |
| 9 | `(0,0,1,1,1,0,1,2,0,0)` |
| 9 | `(0,0,1,1,1,0,2,1,0,0)` |
| 10 | `(0,0,0,1,1,1,1,1,1,0)` |
| 10 | `(0,0,1,0,1,1,1,1,1,0)` |
| 11 | `(0,0,1,1,0,0,1,1,0,0)` |
| 11 | `(0,0,1,1,1,1,1,1,0,0)` |

Together with `five-vertex-three-color-dnn-sieve.md`, this leaves no
five-branch-vertex residual row for kernels 9--12.

## Exact DNN rule

For a rational stereographic parameter `t`, put

`u(t)=((1-t^2)/(1+t^2),2t/(1+t^2))`.

For a physical path of length `l`, the certificate joins the branch vectors
through `l-1` stored internal vectors and uses the transformed final vector
`(-1)^l u(t_v)`. Every consecutive transformed pair `x,y` contributes

`(1-x dot y)/(1+x dot y)`.

The verifier evaluates this sum independently with `fractions.Fraction`. Every
accepted sum is strictly less than the tetracyclic excess budget three. For
fixed transformed endpoints and fixed parity, replacing a path length `l` by
`l+2` can only decrease its optimally eliminated cost. Rooted trees add exactly
one unit per edge to the DNN quantity, so a strict core budget supplies strict
auxiliary slack with all rooted attachments; the equality family below retains
only the stated non-strict conclusion.

## The four kernel-9 parity variants

In nonzero-bundle order `03,04,12,14,23`, the four residual rows are

`(0,1,1,1,1)`, `(1,1,1,1,1)`, `(1,1,1,1,2)`, `(1,1,1,2,1)`.

They are covered as follows.

1. Row `(0,1,1,1,1)` is the all-length theorem in
   `kernel9-row01111-all-length-packet.md`: its doubled-path frontier consists
   exactly of `O_a,E_a,O_23,E_23`, and its remaining singleton-path family is
   closed by the induced structural deletion.
2. Row `(1,1,1,1,1)` is not the image of row `(0,1,1,1,1)` under the kernel
   involution and is not imported by a parity switch.  When all three doubled
   bundles retain canonical lengths `{1,2}`, use planar branch angles
   `0,2pi/3,5pi/3,pi,4pi/3` at vertices `0,1,2,3,4`.  Then the two odd
   singleton paths `03,12` have correlation `-1` and cost zero, while every
   doubled bundle has correlation `-1/2` and exact cost
   `f_1(-1/2)+f_2(-1/2)=1/3+2/3=1`.  Thus the total DNN excess is exactly
   three, independently of the odd singleton lengths by fixed-parity
   monotonicity.  The six doubled-path `+2` frontiers are frozen explicitly
   and cover every descendant in which a doubled path changes.
3. Rows `(1,1,1,1,2)` and `(1,1,1,2,1)` have frozen exact rational vector
   certificates at their canonical first-simple length vector and at every
   one-coordinate `+2` frontier. Their canonical entries are included because
   they are not inferred from a limiting or numerical argument.

For the last two rows, if no coordinate is lengthened the canonical certificate
applies. Otherwise choose any lengthened coordinate. The given length vector
dominates that coordinate's stored `+2` vector; repeated fixed-parity
monotonicity then covers all simultaneous and larger increments.

The involution wording is therefore limited to what it proves. The map
`(0,1,2,3,4)->(1,0,3,2,4)` interchanges `P_03,P_12`, interchanges bundles
`04,14`, and fixes bundle `23` setwise. It fixes row `(1,1,1,1,1)` and reduces
placements within that row; it does not identify that row with
`(0,1,1,1,1)` and does not alter a physical path parity.

## Kernel 10 and kernel 11

Each of the two kernel-10 and two kernel-11 rows has eight physical paths. For
each row the frozen fixture stores nine certificates:

- one certificate for the canonical first-simple vector;
- one certificate for each of the eight vectors obtained by increasing exactly
  one physical path length by two.

Thus these four rows contribute `4*(1+8)=36` certificates. The two remaining
kernel-9 rows contribute `2*(1+8)=18`, and the self-invariant kernel-9 row adds
six doubled-path frontiers, for 60 frozen certificates in total.
The certificate records contain the physical length vector, five branch
parameters, every internal path parameter, and the independently recomputed
exact rational cost.

The upward argument is coordinatewise and physical-path-specific. Given an
arbitrary same-parity descendant, use the canonical certificate if it is the
minimal vector. Otherwise select one changed physical path and use its `+2`
certificate. Every additional increment is by two and only decreases the
eliminated cost with the stored branch correlations. This covers all subsets
of changed coordinates and all larger increments; it does not assume that a
single certificate works at incomparable frontier points.

## Fail-closed artifacts

The frozen rational data are in

`research/fixtures/rank-four-five-vertex-residual-frontiers.json`.

The standalone verifier is

`research/rank-four-five-vertex-residual-closure-verifier.py`.

Run

```text
python research/rank-four-five-vertex-residual-closure-verifier.py
python -O research/rank-four-five-vertex-residual-closure-verifier.py
```

The verifier requires the exact seven-row and 60-record key set, reconstructs
all canonical and one-coordinate frontier vectors, checks every internal
ledger, recomputes every cost with `Fraction`, requires strict cost below three,
and digest-locks the canonical fixture. It imports and reevaluates the accepted
kernel-9 all-length certificates. For kernel-9 row `(1,1,1,1,1)`, it separately
encodes the five canonical planar vectors over `Q(sqrt(3))`, verifies their unit
norms and physical path ledger, checks singleton correlation `-1` and arbitrary
odd-parity cost zero, and checks each doubled-bundle correlation `-1/2`, costs
`1/3+2/3=1`, and total three. It also checks the four-row ledger and relabeling
action, rejects ten hostile mutations including a changed canonical angle,
captures the optimized subprocess, and requires byte-identical normal and `-O`
output.
There is no stdout-only numerical search evidence in the acceptance path.

The proposal search is deterministic from fixed seeds. Its output has been
frozen; floating-point optimization is neither rerun nor trusted by the
verifier. If the fixture is unavailable, it must be regenerated by the
deterministic search and then reviewed and frozen under a new explicit digest,
not silently accepted.

Residual: none among the eight five-vertex three-color residual rows.
