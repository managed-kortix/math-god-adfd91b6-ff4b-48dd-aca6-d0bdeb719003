# Three-vertex rank-five kernels: exact physical orbit theorem

## Theorem

Let `K` be a simple subdivision of a loopless three-vertex multigraph whose
bundle multiplicities are `(1,2,4)`, `(1,3,3)`, or `(2,2,3)`. Then

`kappa(K) <= |E(K)|+4`.

Consequently, if `G` is obtained from `K` by attaching arbitrary rooted trees
at arbitrary vertices, then `s^+(G) >= |V(G)|`.

## Exact path reduction

Label the branch vertices `0,1,2`. For a path of length `l` and endpoint
correlation `r`, exact path elimination gives the excess term

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.

For fixed parity this decreases when `l` is replaced by `l+2`. Thus it is
enough to use

`f_1(r)=(1+r)/(1-r)` and `f_2(r)=2 tan^2(acos(r)/4)`.

Simultaneously using `f_1` for parallel odd paths is an upper bound on their
separate terms; it does not assert that several parallel paths are direct in a
simple subdivision.

For rational `0<=t<=1`, put

`r(t)=(1-6t^2+t^4)/(1+t^2)^2`.

Then `f_2(r(t))=2t^2`, while for `t>0`,

`f_1(r(t))=((1-t^2)/(2t))^2`.

Hence every certificate below is an exact rational correlation Gram matrix and
has an exact rational cost.

## Complete certificates

Write `q=(q_01,q_02,q_12)` for the physical odd-path counts. If `sum(q)=0`,
use the rank-one all-ones Gram matrix; its canonical excess is zero.

If `sum(q)>=2`, use the equilateral Gram matrix

`R_eq=[[1,-1/2,-1/2],[-1/2,1,-1/2],[-1/2,-1/2,1]]`.

It is positive semidefinite with determinant zero. Each odd path costs `1/3`
and each even path costs `2/3`. Since every kernel has seven paths, its excess
is

`sum(q)/3 + 2(7-sum(q))/3 = (14-sum(q))/3 <= 4`.

It remains to list the singleton rows. In pair order `01,02,12`, use the Gram
matrix with off-diagonal entries `r(t_01),r(t_02),r(t_12)` from this table:

| multiplicities | odd bundle | `(t_01,t_02,t_12)` | exact excess | determinant |
|:---:|:---:|:---:|---:|---:|
| `(1,2,4)` | `01` | `(1/2,1/4,1/4)` | `21/16` | `6634496/52200625` |
| `(1,2,4)` | `02` | `(1/2,1/2,0)` | `25/16` | `0` |
| `(1,2,4)` | `12` | `(1/4,1/4,1/2)` | `39/16` | `6634496/52200625` |
| `(1,3,3)` | `01` | `(1/2,1/4,1/4)` | `21/16` | `6634496/52200625` |
| `(1,3,3)` | `02` | `(1/2,1/2,0)` | `33/16` | `0` |
| `(1,3,3)` | `12` | `(1/2,0,1/2)` | `33/16` | `0` |
| `(2,2,3)` | `01` | `(1/2,1/4,1/4)` | `27/16` | `6634496/52200625` |
| `(2,2,3)` | `02` | `(1/4,1/2,1/4)` | `27/16` | `6634496/52200625` |
| `(2,2,3)` | `12` | `(1/4,1/4,1/2)` | `33/16` | `6634496/52200625` |

All two-by-two principal minors are nonnegative, and the displayed determinants
prove positive semidefiniteness. Every singleton cost is strictly below four.
Together with the all-even and equilateral cases, this covers every physical
row.

## Exact orbit fixture

The three boxes contain respectively `30`, `32`, and `36` labeled physical
rows, for `98` total. Genuine vertex automorphism groups have orders `1,2,2`.
Quotienting by these groups only, with no switching quotient, gives respectively
`30`, `20`, and `24` orbits, for `74` total.

`research/fixtures/rank-five-three-vertex-orbits.json` stores all 74 canonical
representatives, physical bundle counts, complete labeled orbits, and exact
rational Gram certificates. Run

```text
python research/rank-five-three-vertex-orbit-verifier.py
python -O research/rank-five-three-vertex-orbit-verifier.py
```

The verifier independently regenerates all 98 rows and 74 orbits, recomputes
every rational Gram minor and canonical cost, requires the raw fixture bytes to
equal the canonical ASCII JSON serialization, and SHA-locks those raw bytes.
It requires byte-identical normal and optimized output and rejects eleven
hostile mutations, including a noncanonical raw-byte mutation. It uses explicit
exceptions rather than `assert`.

The canonical fixture SHA-256 digest, including its final line feed, is

`e3ec57422ba2d9ca0c25ad2ba7d85b8bc74a5d656ebfe20fdb072a0688d01fa9`.

## Spectral conclusion

The suppressed multigraph has seven edges and three vertices, hence cyclomatic
rank five. A subdivision with `L` edges has `|V(K)|=L-4`. The LTZ/DNN bound and
the trace identity give

`s^+(K) >= 2L-kappa(K) >= L-4 = |V(K)|`.

If rooted trees with `h` total edges are attached, one-vertex-sum additivity
gives `kappa(G)<=L+4+h`, while `|E(G)|=L+h` and `|V(G)|=L-4+h`.
The same calculation proves `s^+(G)>=|V(G)|`.
