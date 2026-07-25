# Positive square energy for a two-C5 bouquet with arbitrary trees

## Theorem and exact scope

Let `G` be a connected cactus whose only cyclic blocks are two copies of
`C5`, and suppose that the two cycles have exactly one common vertex `v0`.
Every edge outside the two cycles is allowed to lie in an arbitrary tree
attached at a core vertex. Then

`s^+(G) >= n(G) + 1 - 4/(3 sqrt(13)) > n(G)`.                 (1)

In particular, `s^+(G)>n(G)`.

This statement is only about the shared-vertex two-`C5` cactus. It does not
claim a result for disjoint cycles joined by a path, for more than two cycles,
or for arbitrary bicyclic cacti.

The proof has two independent ingredients. First, exact matching belief
propagation eliminates every attached tree and produces vertex activities at
least `t`. Second, a coefficientwise polynomial certificate bounds the Sachs
phase of the resulting weighted two-cycle core.

## 1. Signless matching partitions

For a forest `F`, put

`Z_F(t)=sum_M t^(|V(F)|-2|M|)`,                              (2)

where the sum is over all matchings of `F`. More generally, if a graph `H`
has positive vertex activities `a_v`, write

`Z_H(a)=sum_M prod_(v unmatched by M) a_v`.                  (3)

All edge activities are one. Thus `Z_F(t)` is obtained from (3) by setting
every vertex activity equal to `t`.

For any graph, define the imaginary-axis characteristic function

`Psi_G(t)=i^(-n) phi_G(it)=prod_j (t+i lambda_j)`, `t>0`.     (4)

The grouped Sachs expansion expresses `Psi_G` as a sum over vertex-disjoint
cycle collections, with the empty collection giving the signless matching
partition. A cycle of length `l` contributes the multiplier

`-2 i^(-l)`.

For `l=5` this multiplier is `2i`. The two cycles in the present graph share
`v0`, so they cannot occur together in a Sachs subgraph. There is therefore
no two-cycle term.

## 2. Exact matching BP for an arbitrary rooted tree

Orient an attached tree toward its core vertex. For an oriented noncore edge
`u -> p`, let `T_(u->p)` be the component below `u`, and define

`q_(u->p)(t) = Z_(T_(u->p))(t) / Z_(T_(u->p)-u)(t)`.         (5)

The denominator is a product of the child-subtree partitions and is positive
for `t>0`. Splitting a matching according to whether `u` is unmatched or is
matched to one of its children gives the exact recursion

`q_(u->p)(t) = t + sum_(w child of u) 1/q_(w->u)(t).`        (6)

For a leaf the message is `t`. Induction in (6) consequently proves

`q_(u->p)(t) >= t > 0`.                                     (7)

Now eliminate all noncore vertices. If the noncore neighbors of a core vertex
`v` are `u`, its effective activity is

`a_v(t) = t + sum_(u attached at v) 1/q_(u->v)(t).`          (8)

In particular,

`a_v(t)=t+y_v(t)` with `y_v(t)>=0`.                           (9)

There is also a common positive prefactor

`K(t)=prod_(u adjacent to the core) Z_(T_(u->v))(t)>0`.      (10)

To check the factor carefully, consider one branch rooted at `u`. If the core
vertex is not matched to `u`, that branch contributes `Z_T`. If the edge `vu`
is used, it contributes `Z_(T-u)`. After `Z_T` is extracted, the latter choice
has weight

`Z_(T-u)/Z_T = 1/q_(u->v)`.

Summing these mutually exclusive choices adds exactly the terms in (8).
Doing this independently for every branch proves

`Z_G(t)=K(t) Z_core(a(t))`.                                  (11)

The same factor `K(t)` occurs after deleting either `C5`: a branch whose core
root is deleted is simply disconnected and contributes its full `Z_T`, while
branches at retained vertices are absorbed into the corresponding effective
activity. This common-factor fact is essential; no unrecorded ratio of tree
partitions remains in either cycle carrier.

Equations (5)-(11) also cover a rooted tree presented as one tree identified
with a core vertex: remove the core root, regard each resulting component as
a branch, and apply the same messages.

## 3. The weighted two-C5 core

Label the common vertex by `0`. On lobe `j in {1,2}`, label the other four
vertices consecutively by `1,2,3,4`, and abbreviate their activities by
`x1,x2,x3,x4`. The weighted matching partition of the path left after deleting
the common vertex is

`A(x1,x2,x3,x4)`
` = x1 x2 x3 x4 + x3 x4 + x1 x4 + x1 x2 + 1`.               (12)

The five terms correspond respectively to the empty matching, each of the
three one-edge matchings of `P4`, and its unique two-edge matching.

If the common vertex is matched along this lobe, summing the two possible
incident cycle edges gives

`B(x1,x2,x3,x4)`
` = x2 x3 x4 + x2 + x4 + x1 x2 x3 + x1 + x3`.               (13)

Indeed, after choosing the edge from `0` to vertex `1` or `4`, the remaining
three vertices form a `P3`. This verifies that there is no missing factor of
two in `B`: its two groups are the two distinct choices of edge incident with
`0`.

Let `A_j,B_j` denote (12)-(13) on lobe `j`, and let `a0` be the activity at the
common vertex. Partitioning core matchings according to the status of `0`
gives

`R = a0 A1 A2 + B1 A2 + A1 B2`.                             (14)

The first term leaves `0` unmatched. The next two terms match `0` into lobe
one or lobe two. These cases are disjoint and exhaustive.

Deleting all vertices of lobe one leaves the `P4` in lobe two, and conversely.
The `C5` Sachs multiplier is `2i`, and the two cycles cannot be selected
together. Combining this observation with the common factor (10) gives the
exact factorization

`Psi_G(t)=K(t) [R+2i(A1+A2)].`                               (15)

Every quantity in brackets is positive for `t>0`. Since `K(t)>0` is real, it
does not affect the continuous argument. Hence

`Theta_G(t)=arg Psi_G(t)=atan(2(A1+A2)/R)`,                  (16)

with `0<Theta_G(t)<pi/2`.

## 4. Exact coefficient certificate

Put

`D(t)=t^4+7t^2+9`.                                          (17)

The needed weighted-core inequality is

`2R >= t D(t)(A1+A2)`.                                      (18)

To prove it, substitute

`a0=t+y0`, `x_(j,k)=t+y_(j,k)`

in (12)-(14), where all nine `y` variables are nonnegative, and expand

`P=2(a0 A1 A2+B1 A2+A1 B2)-t(t^4+7t^2+9)(A1+A2)`.           (19)

The exact SymPy certificate

`positive-square-energy/experiments/c5_bouquet_matching_certificate.py`

constructs `P` over `ZZ` and verifies:

- the expanded polynomial has 1290 nonzero terms;
- every coefficient is a positive integer, with minimum `1` and maximum `22`;
- every monomial contains at least one `y` variable, so the `y`-constant part
  is exactly zero;
- the canonical ordered term stream has SHA-256 digest
  `4c436cac772395d2a8edfdd81408ffe426759d3e94d66df2e4ab0235a3343110`.

Thus (19) is nonnegative whenever all `y` variables are nonnegative, proving
(18). The vanishing constant part also records the exact bare-core identity:
(18) is an equality when every activity equals `t`.

Combining (16) and (18), using monotonicity of `atan`, yields

`0<Theta_G(t)<=atan(4/(t D(t))).`                            (20)

The factors are worth noting: the imaginary part in (15) is `2(A1+A2)`, while
(18) bounds `(A1+A2)/R` by `2/(tD)`. Their product gives the numerator `4` in
(20), not `2` or `8`.

## 5. Phase integral and positive square energy

The square-energy Coulson identity, with the continuous argument in (4), is

`s^+(G)-s^-(G)=-(4/pi) integral_0^infinity t Theta_G(t) dt`. (21)

For completeness, it follows by writing (4) as the product over the real
adjacency eigenvalues, taking the continuous sum of their arguments, and
integrating the resulting scalar identity. The trace condition
`sum_j lambda_j=0` cancels the nonintegrable first-order term at infinity.

From (20) and `atan u<=u` for `u>=0`,

`integral_0^infinity t Theta_G(t) dt`
` <= integral_0^infinity 4/(t^4+7t^2+9) dt`.                 (22)

Set `t=sqrt(3)u`. The standard reciprocal-quartic integral

`integral_0^infinity du/(u^4+b u^2+1)=pi/(2 sqrt(2+b))`

for `b>-2` gives

`integral_0^infinity 4/(t^4+7t^2+9) dt`
` = 2pi/(3 sqrt(13)) < pi/2`.                               (23)

Consequently (21) implies

`s^+(G)-s^-(G) >= -8/(3 sqrt(13))`.                          (24)

The graph has exactly two independent cycles, so `m=n+1`. Since adjacency
eigenvalues satisfy

`s^+(G)+s^-(G)=tr A(G)^2=2m=2n+2`,                          (25)

averaging (24) and (25) proves

`s^+(G) >= n+1-4/(3 sqrt(13)) > n`,

which is (1).

## 6. Verification record

Run from the repository root:

```text
python positive-square-energy/experiments/c5_bouquet_matching_certificate.py
```

The script uses only exact integer polynomial arithmetic for the certificate.
The analytic step after the certificate uses only `atan u<=u` and the exact
reciprocal-quartic integral (23).

No attachment is replaced by a star and no spectral-radius grafting argument
is used. Arbitrary attached trees enter only through the exact messages (5)-
(8), which is why the proof remains valid for every rooted tree at every core
vertex while staying restricted to the shared-vertex two-`C5` core.
