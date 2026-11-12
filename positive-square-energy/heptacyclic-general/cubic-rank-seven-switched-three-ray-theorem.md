# Switched three-ray owners for cubic rank-seven kernels

## Statement

Let `K` be a loopless cubic multigraph of cyclomatic rank seven. Then `K` has
twelve vertices and eighteen physical edges. Write a bundled edge as
`e=(u,v;m_e)` and let `q_e` be the number of odd paths in its physical parity
row. Its canonical simple lengths are one `1` and `q_e-1` copies of `3` when
`q_e>0`, together with `m_e-q_e` copies of `2`.

Choose a color `c_v in Z/3` and a switch bit `s_v in F_2` at every branch
vertex. Put

```text
x_e = [c_u != c_v],        d_e = s_u xor s_v.
```

The three unit rays have pairwise correlation `-1/2`; state `(c,s)` denotes
`(-1)^s` times ray `c`. Define the scaled bundle table bound `W_e(x,d)` by

```text
x=0: W_e(0,d)=0 if (q_e=0,d=0) or (q_e=m_e,d=1), and infinity otherwise;

x=1, q_e=0: W_e(1,0)=27m_e,       W_e(1,1)=3m_e;
x=1, q_e>0: W_e(1,0)=27m_e-25q_e+4,
             W_e(1,1)=3m_e+15q_e+36.
```

### Theorem (exact signed three-color/cut table-bound certificate)

The parity row has a switched three-ray table-bound certificate if and only if
there are `c:V(K)->Z/3` and `s:V(K)->F_2` such that

```text
sum_e W_e([c_u != c_v], s_u xor s_v) <= 108.                 (1)
```

Every such certificate constructs a switched three-ray structural owner of DNN
excess at most six. No converse is claimed for arbitrary switched-three-ray
Grams: they may use path-optimal Gram chains whose exact costs are smaller than
the retained rational table bounds.

The same sufficient certificate, with no change, works for any loopless
multikernel after replacing eighteen by its physical-edge count. A witness is
retained under every same-parity lengthening and under attachment of arbitrary
rooted trees. Thus, in the canonical-plus-coordinate reduction, one witness
owns the canonical target and every coordinate frontier of its row.

This is a sufficient owner criterion, not a universal existence assertion. In
particular, the completed order-twelve coarse-residual census has `6,138,723`
parity orbits. Exactly `1,430,594` pass this table-bound criterion and
`4,708,129` fail it. The latter are classified exactly as weighted-CSP failures
of (1), not as counterexamples to the square-energy theorem or as proofs that no
other switched-three-ray Gram exists; they require another owner lane.

## Proof

Take equilateral unit vectors `a_0,a_1,a_2`, so
`<a_i,a_j>=-1/2` for `i!=j`, and assign
`z_v=(-1)^{s_v}a_{c_v}`. If `x_e=0`, the endpoint correlation is
`(-1)^{d_e}`. In this retained table-bound family, an `x_e=0` path is
assigned finite charge only when its parity agrees with `d_e`; then it is a
signed zero-cost contraction. A parity mismatch has transformed correlation
`t=-1`, whose actual optimum is
`f_l(-1)=l tan^2(pi/(2l))`: finite for `l>1` and infinite for `l=1`. This
restricted family nevertheless deliberately assigns it charge `+infinity`.
Hence a monochromatic bundle is admitted only in the two pure cases in the
first table line.

If `x_e=1`, put `t=(-1)^l<z_u,z_v>` for a path of length `l`. Its exact
path-optimal DNN excess is

```text
f_l(t) = l tan^2(acos(t)/(2l)).
```

Here is both the path construction and the promised rational bound. For the
original path vectors `v_0=z_u,v_l=z_v`, set `w_i=(-1)^i v_i`; then
`<w_0,w_l>=t`. Let `beta=acos(t)` and insert the internal `w_i` at equal angular
increments `beta/l` on the endpoint great-circle arc.
The Gram of these actual unit vectors is PSD, has the prescribed endpoints, and
has exact path excess `f_l(t)`. Put `y=beta/2`. For `-1<t<=1`, convexity of
`tan` on `[0,pi/2)` and `tan(0)=0` give

```text
tan(y/l) <= tan(y)/l,

f_l(t) = l tan^2(y/l)
       <= tan^2(y)/l
        = (1-t)/(l(1+t)).                                  (2)
```

All finite `x_e=1` table states have `t` equal to `1/2` or `-1/2`, so (2)
applies. Its right side is a rational certificate charge when `t` is rational;
it is not asserted to be the exact path-chain cost. Equality holds at `l=1`
and the bound is strict for `l>1` in these finite table states. For example,
`t=1/2,l=2` gives exact cost `14-8sqrt(3)<1/6`, while (2) is `1/6`.

After multiplication by `18`, the rational upper charge is `6/l` in the cheap
state and `54/l` in the expensive state. For `q>0`, the reciprocal-length sum
over odd paths is `1+(q-1)/3=(q+2)/3`, while the even paths contribute
`(m-q)/2`. Summing these upper charges gives the four finite table weights.
Install the equal-angle chains simultaneously; only their already fixed branch
endpoints are shared, so their union is a unit-vector Gram and the path excesses
add. Thus a state assignment satisfying (1) constructs a Gram whose exact
excess is at most the tabulated majorant, hence at most six. Conversely, a
six-state assignment using this retained table-bound certificate family
determines its colors, switch cut, and the same tabulated sum. This proves the
stated equivalence only for table-bound certificates and the forward
implication to structural ownership.

Increasing any path length by two weakly decreases the rational bound in (2).
The branch Gram therefore proves every same-parity descendant. One-vertex
additivity assigns each rooted tree its ordinary tree Gram, proving the stated
rooted-tree closure.

## Exact SAT and graph formulation

Use one-hot variables `C_(v,0),C_(v,1),C_(v,2)` and Boolean switch variables
`S_v`. For every bundle introduce `X_e` and `D_e` with

```text
X_e <-> (the endpoint one-hot colors differ),
D_e <-> (S_u xor S_v).
```

Delete each `(X_e,D_e)` pair having infinite table weight. Encode the remaining
four-way choice by indicator variables and impose the pseudo-Boolean inequality
`sum W_e <= 108`. All coefficients are nonnegative integers. Fixing one vertex
to state `(0,0)` removes the global `S_3 x C_2` symmetry. This encoding is
equisatisfiable with existence of a table-bound certificate (1), so SAT plus a
checked weighted sum is an exact proof of that certificate; UNSAT is an exact
failure classification only for this owner family.

There is also a graph reading. The switch bits select a cut `delta(S)`, so
`d_e=1` exactly on that cut. The colors partition the vertices into at most
three cells, so `x_e=1` exactly on the associated three-cut. Pure bundles may
lie inside a color cell only when their required sign is realized by the switch
cut; every mixed bundle must cross the three-cut. Among all compatible signed
three-cuts, (1) asks whether the minimum table-bound weight is at most `108`.

## Audited decision procedure

`rank7_order12_structural_owners.py` implements the six-state CSP directly.
Arc constraints handle the zero-cost simple-cubic case; the general solver uses
branch-and-bound with the exact per-edge table lower bound. It now returns the
actual six-state witness, and `three_ray_witness_cost` independently replays its
exact integer upper charge. The Boolean owner predicates are wrappers around
witness existence.

Run the local exact tests with

```text
python3 -m unittest \
  positive-square-energy/experiments/test_rank7_order12_structural_owners.py
```

The committed order-twelve manifest is a complete classification of the
coarse-residual universe for this table-bound criterion. Its
`full_theorem=false` flag is essential: failure of (1) only excludes this
retained switched three-ray certificate family.
