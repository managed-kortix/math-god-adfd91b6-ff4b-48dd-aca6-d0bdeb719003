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
`(-1)^s` times ray `c`. Define the scaled bundle weight `W_e(x,d)` by

```text
x=0: W_e(0,d)=0 if (q_e=0,d=0) or (q_e=m_e,d=1), and infinity otherwise;

x=1, q_e=0: W_e(1,0)=27m_e,       W_e(1,1)=3m_e;
x=1, q_e>0: W_e(1,0)=27m_e-25q_e+4,
             W_e(1,1)=3m_e+15q_e+36.
```

### Theorem (exact signed three-color/cut criterion)

The parity row has a switched three-ray structural owner of DNN excess at most
six if and only if there are `c:V(K)->Z/3` and `s:V(K)->F_2` such that

```text
sum_e W_e([c_u != c_v], s_u xor s_v) <= 108.                 (1)
```

The same statement, with no change, holds for any loopless multikernel after
replacing eighteen by its physical-edge count. A witness is retained under
every same-parity lengthening and under attachment of arbitrary rooted trees.
Thus, in the canonical-plus-coordinate reduction, one witness owns the
canonical target and every coordinate frontier of its row.

This is a criterion, not a universal existence assertion. In particular, the
completed order-twelve coarse-residual census has `6,138,723` parity orbits.
Exactly `1,430,594` pass this criterion and `4,708,129` fail it. The latter are
classified exactly as weighted-CSP failures of (1), not as counterexamples to
the square-energy theorem; they require another owner lane.

## Proof

Take equilateral unit vectors `a_0,a_1,a_2`, so
`<a_i,a_j>=-1/2` for `i!=j`, and assign
`z_v=(-1)^{s_v}a_{c_v}`. If `x_e=0`, the endpoint correlation is
`(-1)^{d_e}`. A canonical path is finite only when its parity agrees with
`d_e`. Hence a monochromatic bundle is possible precisely in the two pure
cases in the first line of the table, and then all of its paths are signed
zero-cost contractions.

If `x_e=1`, the endpoint correlation is `(-1)^{d_e+1}/2`. For a path of length
`l`, the linear Gram-chain construction has excess

```text
(1-r')/(l(1+r')),          r'=(-1)^l <z_u,z_v>.
```

After multiplication by `18`, a cheap path contributes `6/l` and an expensive
path contributes `54/l`. For `q>0`, the reciprocal-length sum over odd paths is
`1+(q-1)/3=(q+2)/3`, while the even paths contribute `(m-q)/2`. Summing gives
exactly the four finite weights displayed above. Bundle interiors can be put in
mutually orthogonal auxiliary spaces, so the costs add. This proves both
directions of (1): a state assignment constructs the Gram, and every switched
three-ray Gram determines its colors, switch cut, and the same tabulated sum.

Increasing any path length by two weakly decreases its retained-chain cost.
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
equisatisfiable with (1), so SAT plus a checked weighted sum is an exact proof;
UNSAT is an exact failure classification for this owner family.

There is also a graph reading. The switch bits select a cut `delta(S)`, so
`d_e=1` exactly on that cut. The colors partition the vertices into at most
three cells, so `x_e=1` exactly on the associated three-cut. Pure bundles may
lie inside a color cell only when their required sign is realized by the switch
cut; every mixed bundle must cross the three-cut. Among all compatible signed
three-cuts, (1) asks whether the minimum table weight is at most `108`.

## Audited decision procedure

`rank7_order12_structural_owners.py` implements the six-state CSP directly.
Arc constraints handle the zero-cost simple-cubic case; the general solver uses
branch-and-bound with the exact per-edge lower bound. It now returns the actual
six-state witness, and `three_ray_witness_cost` independently replays its exact
integer cost. The Boolean owner predicates are wrappers around witness
existence.

Run the local exact tests with

```text
python3 -m unittest \
  positive-square-energy/experiments/test_rank7_order12_structural_owners.py
```

The committed order-twelve manifest is a complete classification of the
coarse-residual universe for this criterion. Its `full_theorem=false` flag is
essential: failure of (1) only excludes a switched three-ray owner.
