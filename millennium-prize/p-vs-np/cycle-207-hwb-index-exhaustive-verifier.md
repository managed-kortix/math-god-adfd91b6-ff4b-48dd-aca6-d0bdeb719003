# Cycle 207: hostile audit and exhaustive HWB INDEX verification

## Formal audit

Use one-based coordinates `[8m]={1,...,8m}` and
`HWB_(8m)(x)=x_(|x|)` for positive weight, with the zero-weight value fixed
arbitrarily. Let `P` be the first `4m` coordinates in an arbitrary order and
`Q=[8m]\P`. Rows of the cut matrix are assignments to `P`, columns are
assignments to `Q`, and entries are completed `HWB` values.

The inclusive intervals `J_0=[m,5m]` and `J_1=[3m,7m]` have union `[m,7m]`.
Its complement in `[8m]` has `(m-1)+m=2m-1` coordinates, so

\[
 |P\cap(J_0\cup J_1)|\ge 4m-(2m-1)=2m+1.
\]

If both `|P\cap J_0|` and `|P\cap J_1|` were at most `m-1`, their union would
have size at most `2m-2`. Therefore one interval contains at least `m` prefix
coordinates. Put `r=m` for `J_0` or `r=3m` for `J_1`, and choose distinct data
indices `i_1,...,i_m` from `P\cap[r,r+4m]`.

Choose distinct compensators `c_1,...,c_m` from the remaining `3m` coordinates
of `P`. On the prefix row indexed by `z in {0,1}^m`, set

\[
 x_{i_j}=z_j,\qquad x_{c_j}=1-z_j.
\]

Each pair contributes one to the prefix weight. Exactly `2m` prefix coordinates
remain: set them all to zero for `r=m` and all to one for `r=3m`. Thus every
row has prefix weight exactly `r`, the compensators are disjoint from all data
positions, and the map from `z` to its prefix assignment is injective.

For query `j`, set exactly `t_j=i_j-r` suffix coordinates to one. This is
possible because `0<=t_j<=4m=|Q|`. The assignment is confined to `Q`, whereas
every data position lies in `P`, so it leaves all data bits untouched. The
completed input has weight `r+t_j=i_j` and hence

\[
 HWB_{8m}(alpha_z,beta_j)=x_{i_j}=z_j.
\]

The chosen `i_j` are distinct, so the required weights `t_j` are distinct;
suffix assignments with distinct weights cannot be duplicate columns. The
resulting submatrix is exactly

\[
 K(z,j)=z_j,
 \qquad z\in\{0,1\}^m,\quad j\in[m].
\]

This is the data-rows/query-columns orientation of `INDEX_m`, and is the
transpose of the other common convention. Its `2^m` rows are the distinct words
`z`, so the corresponding prefix assignments induce `2^m` distinct residual
functions and force midpoint OBDD width at least `2^m`.

No flaw survives the audit. Mixing zero-based coordinate labels with the
formula `x_(|x|)` would cause an indexing error, but that is not the convention
used here. The zero-weight value is never queried, and every selected address
lies in `[m,7m] subset [1,8m]`.

## Finite verifier

The dependency-free script `verify_cycle207_hwb_index.py` independently checks
the Cycle 206 construction. For every enumerated midpoint prefix
`P subset [8m]`, `|P|=4m`, it chooses the first viable address interval,
constructs the data and compensator coordinates, materializes all `2^m` rows
and `m` query columns, evaluates `HWB_(8m)` directly, and asserts that the
resulting matrix is exactly `INDEX_m`.

The default exhaustive range is `m<=2` (`N<=16`), comprising `70+12870=12940`
midpoint partitions. The Cycle 207 campaign was also run through `m=3`
(`N=24`), comprising `2717096` cuts in total. A larger finite search is
available with `--max-m`; its cost grows as `binom(8m,4m) 2^m m`. No
counterpartition was found through `N=24`. A failure prints the complete prefix
set under the label `COUNTERPARTITION` and exits nonzero.

The same script checks the construction without expanding the exponential
matrix: it verifies that the prefix and suffix partition `[8m]`, the data and
compensators are disjoint prefix coordinates, every prefix row has fixed weight
`r`, every suffix query weight lies in `[0,4m]`, and each completed weight is
its data coordinate. This structural check runs on four deterministic
representative cuts for every `m<=64` by default. An arbitrary cut can be
supplied with `--partition`.

Run from the repository root:

```text
python3 millennium-prize/p-vs-np/verify_cycle207_hwb_index.py
python3 millennium-prize/p-vs-np/verify_cycle207_hwb_index.py --max-m 3
```

This is finite verification and a checker for the constructive identities. It
does not replace the all-`m`, all-partition argument, and the resulting theorem
is only an exact deterministic all-order OBDD lower bound for HWB. It gives no
unrestricted circuit lower bound and no `P != NP` conclusion.
