# Shared-vertex C3+C5 cactus: exact phase domination

## Result

Let `G` be a connected cactus whose only cyclic blocks are one `C3` and one
`C5`, sharing exactly one vertex `0`. Arbitrary rooted trees may be attached at
every vertex. For `t>0`, normalize the characteristic polynomial by

`Psi_G(t)=i^(-n) phi_G(it)=prod_j (t+i lambda_j)`.

Then its continuous phase satisfies the pointwise bound

`arg Psi_G(t) < atan(2/Z_C5(t))`,

where

`Z_C5(t)=t^5+5t^3+5t`.

Thus the phase is strictly below the positive phase of the bare `C5`. The
argument allows the mixed-core phase to have either sign; when it is negative,
the claimed upper bound is automatic, and the certificate below also handles
the nontrivial positive case uniformly.

## Exact tree compression

For an oriented branch edge `u -> p`, let `T_(u->p)` be the subtree below `u`
and set

`q_(u->p)=Z_(T_(u->p))(t)/Z_(T_(u->p)-u)(t)`.

Splitting matchings according to the status of `u` gives exact matching BP:

`q_(u->p)=t+sum_(w child of u) 1/q_(w->u) >= t`.

After all noncore vertices are eliminated, each core vertex has activity

`a_v=t+y_v`, with `y_v>=0`.

All terms in the grouped Sachs expansion have the same positive real factor

`K(t)=prod_(u adjacent to the core) Z_(T_(u->v))(t)`.

This remains true when a Sachs cycle deletes a core vertex: each branch at a
deleted vertex contributes its full `Z_T`, already present in `K`. Hence no
uncontrolled ratio of tree partitions occurs.

## Weighted core partitions

Write `u1,u2` for the activities at the two nonshared triangle vertices.
Deleting `0` leaves one edge, while matching `0` into the triangle has two
possible incident edges. The corresponding partitions are

`A3=u1 u2+1`,

`B3=u1+u2`.

Write `x1,x2,x3,x4` consecutively around the nonshared part of the pentagon.
Deleting `0` leaves `P4`, giving

`A5=x1 x2 x3 x4+x3 x4+x1 x4+x1 x2+1`.

The sum over matchings that match `0` along a pentagon edge is

`B5=x2 x3 x4+x2+x4+x1 x2 x3+x1+x3`.

Partitioning all core matchings by the status of `0` gives the exact real
matching term

`R=a0 A3 A5+B3 A5+A3 B5`.

## Exact Sachs polynomial

In the normalized grouped Sachs expansion, a cycle of length `l` contributes
`-2 i^(-l)`. Therefore `C3` contributes `-2i`, while `C5` contributes `2i`.
The cycles share `0`, so they cannot occur together in a Sachs subgraph. If
the triangle is selected, deleting it leaves the pentagon's `P4`, with
partition `A5`. If the pentagon is selected, deleting it leaves the
triangle's `P2`, with partition `A3`. Consequently

`Psi_G(t)=K(t) [R-2i A5+2i A3]`

and hence

`Psi_G(t)=K(t) [R+2i(A3-A5)]`.                         (1)

Because `R,K>0`, the phase always lies in `(-pi/2,pi/2)` and is exactly

`Theta_G(t)=atan(2(A3-A5)/R)`.                         (2)

This right-half-plane formula also fixes the continuous argument without any
winding ambiguity.

## Coefficientwise certificate

Since `Z_C5(t)>0` and `R>0`, monotonicity of `atan` shows that the desired
pointwise inequality follows from

`R >= Z_C5(t)(A3-A5)`.                                  (3)

Substitute

`a0=t+y0`, `u_j=t+y_(3,j)`, `x_k=t+y_(5,k)`,

with all seven `y` variables nonnegative, and form

`Q=R-(t^5+5t^3+5t)(A3-A5)`.                             (4)

The exact SymPy script

`positive-square-energy/experiments/c3_c5_shared_vertex_phase_certificate.py`

expands `Q` over `ZZ` and verifies:

- `Q` has 293 nonzero monomials;
- every coefficient is a positive integer, with minimum 1 and maximum 26;
- the part independent of all `y` variables is
  `t(t^4+3t^2+1)(t^4+5t^2+7)`, which is positive for `t>0`;
- the canonical ordered term stream has SHA-256 digest
  `07af9b8b357dc505ada2e47ecd633f085ce16f49077262475bdb4dd09f80086c`.

Thus `Q>0` for `t>0` on the full nonnegative orthant. Equations (2)-(4) give
the strict bound

`Theta_G(t) < atan(2/(t^5+5t^3+5t))`.

The right side is exactly the bare pentagon phase because

`Psi_C5(t)=Z_C5(t)+2i`.

Run the certificate from the repository root with

```text
python positive-square-energy/experiments/c3_c5_shared_vertex_phase_certificate.py
```

This closes the shared-common-vertex mixed `C3+C5` case at the requested
pointwise phase level. It does not address a triangle and pentagon that are
vertex-disjoint and joined by a path.
