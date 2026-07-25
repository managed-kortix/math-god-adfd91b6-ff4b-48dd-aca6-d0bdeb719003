# The `{3,5,5}` tiny DNN gap: relaxation audit

## Target and arithmetic

Let `G` be a connected tricyclic cactus of order `n` whose cyclic blocks have
lengths `3,5,5`. Then `m=n+2`, and the sharp cactus DNN constant is

`kappa(G)=n+2+epsilon_3+2 epsilon_5`
`        =n+4+(9-4 sqrt(5))`.

Writing

`delta=9-4 sqrt(5)=0.05572809000084...`,

the DNN argument gives

`s-(G)<=n+4+delta`,
`s+(G)>=n-delta`.

Thus the exact missing improvement is `delta`, equivalently the desired bound
is `s-(G)<=n+4`.

## What the cubic moment cannot prove

The triangle gives the exact spectral constraints

`sum lambda_i=0`,
`sum lambda_i^2=2m=2n+4`,
`sum lambda_i^3=tr(A^3)=6`.

These scalar moments, even together with the sharp DNN upper bound on `s-`, do
not force `s-<=n+4`. The following explicit continuous spectral relaxation is
feasible at the DNN endpoint.

Take `n=20`, put

`X=20-delta`, `Y=24+delta`, `b=sqrt(Y/3)`, `L=3b`,

and choose `x` in `(0.188,0.189)` as follows. For each such `x`, define

`U=L-15x`, `Q=X-15x^2`,
`a=(U+sqrt(2Q-U^2))/2`, c=(U-sqrt(2Q-U^2))/2`.

Let

`F(x)=a^3+c^3+15x^3-(6+3b^3)`.

Direct interval evaluations give

`F(0.188)=-0.1424...`, `F(0.189)=0.0970...`.

The radicand and `c` are positive throughout this interval, so continuity
supplies a root `x_*`. Now take the 20 real numbers

`a, c, x_*,...,x_*` (15 copies), `-b,-b,-b`.

By construction they satisfy exactly

`sum lambda_i=0`, `sum lambda_i^2=44`, `sum lambda_i^3=6`,
`sum_(lambda_i<0) lambda_i^2=Y=24+delta`.

Numerically one may take

`x_*=0.18859...`, `a=4.1288...`, `c=1.5374...`, `b=2.831709...`.

Therefore no scalar certificate using only trace zero, the second moment, the
triangle cubic moment, and `s-<=n+4+delta` can recover any part of the missing
constant. Support/rank/integrality restrictions would have to add genuinely
new information.

The usual polynomial-majorant formulation reaches the same obstruction. Any
pointwise majorant of `x_-^2` whose expectation is evaluated solely from
moments 0 through 3 is valid for the atomic measure above, and hence cannot
prove an upper bound below `Y`.

## Exact first-chain improvement, and its limit

For the actual negative spectral part `B=A_-`, set

`p=sum_(uv in E) max(B_uv,0)`, `s=tr(B^2)=s-(G)`.

The first DNN-chain inequality refines exactly to

`s+8p+16p^2/s<=kappa(G)`.

Consequently the `{3,5,5}` target follows whenever

`8p+16p^2/s>=delta`;

in particular `p>=delta/8` is sufficient. But actual cactus examples can have
`p=0`, so this is not a class-uniform closure.

The spectral-lift constraints also give the exact identity

`-sum_(uv in E) B_uv(1+B_uv)`
` =1/2 sum_u B_uu^2+sum_(uv notin E,u<v) B_uv^2>=0`,

together with `AB+B^2=0`. These expose strict non-liftability of generic DNN
optimizers, but no graph-uniform conversion of that separation into the loss
`delta` is currently available. The triangle equation

`tr(P^3)-tr(B^3)=6`

does not by itself supply such a conversion, as the scalar countermodel above
demonstrates.

## Packet route: useful cases, but not a uniform closure

Existing packet estimates close some incidences with a large margin, but the
naive mixed/unicyclic partition does not recover the tiny DNN gap.

1. If one can partition into an induced triangular unicyclic territory and an
   induced territory containing both pentagons, then

   `s+(triangle packet)>h`,

   while the established two-pentagon theorems give `s+(C5,C5 packet)>k` for
   every shared-cut or connector-path incidence. Superadditivity proves
   `s+(G)>n` immediately. This handles, for example, block-tree incidences in
   which a bridge cut isolates the triangle from a connected two-pentagon
   side.

2. If instead the available adjacent pair is `C3,C5`, the known sharp packet
   estimates are

   `s+(C3,C5 packet)>h+2-sec(pi/5)=h+2-sqrt(5)`,

   `s+(C5 packet)>=k+1-sec(pi/5)=k+1-sqrt(5)`.

   Their sum is only

   `s+(G)>n+3-2sqrt(5)=n-1.472135...`,

   much weaker than even the DNN bound `n-delta`. Hence ordinary packet
   addition loses rather than gains the needed constant.

3. The unresolved packet geometry is typified by three vertex-disjoint cycle
   blocks whose reduced block tree has the triangle between the two pentagons.
   No bridge cut produces a connected induced two-pentagon packet. The same
   obstruction appears in shared-cut configurations where assigning the cut
   vertex to one side breaks a cycle on the other. Closing these cases requires
   a correlated surplus theorem, not the presently known packet bounds in
   isolation.

Thus a two-pentagon packet is decisive whenever that territory exists, but a
general block-incidence proof does not follow. The scalar cubic-moment
relaxation is nevertheless conclusively too weak.

## Verdict

- **Counterexample to the proposed scalar relaxation:** yes, the 20-atom
  construction saturates `s-=n+4+delta` while satisfying the first three graph
  moments, including `tr(A^3)=6`.
- **Strict-liftability route:** exact identities and a conditional sign-gap are
  available, but no uniform `delta` conversion follows.
- **Packet route:** it proves all incidences admitting a triangle / two-`C5`
  induced partition, but the mixed-pair plus unicyclic estimates have a
  `2sqrt(5)-3` deficit and do not close the remaining geometries. A genuinely
  correlated packet or phase estimate is still required.
