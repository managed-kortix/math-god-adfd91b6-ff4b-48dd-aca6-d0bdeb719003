# Cycle 56: the residual beyond the optimal below-`M` witness

## Exact orthogonal decomposition

Fix `M<B<=M+12`, put

\[
Z=\operatorname{span}\{U_{M-1},\rho_M,\ldots,\rho_{B-1}\},
\qquad Q=I-\Pi_Z,
\qquad D=D_{M-1},
\]

and retain the optimal Cycle 55 witness `g_M`, with

\[
g_M\perp Z,
\qquad \langle D,g_M\rangle=\|g_M\|^2=W_M.
\]

Define the residual after extracting that witness by

\[
\boxed{D_+=D-g_M.}                                  \tag{56.1}
\]

Then

\[
\langle g_M,D_+\rangle=0,
\qquad QD=g_M+QD_+,
\qquad \langle g_M,QD_+\rangle=0,
\]

and therefore

\[
\boxed{\|QD\|^2=W_M+\|QD_+\|^2.}                 \tag{56.2}
\]

This is the exact residual that must repair the three Cycle 55 failures.

The name “post-`M` residual” is only shorthand. On `1<t<M`,

\[
D_+(t)=(\ell_{M-1}+c_M)t,                         \tag{56.3}
\]

so it generally retains one below-`M` linear coupling. It is not supported on
`[M,infinity)`. If `Gamma` is the probe Gram matrix and
`b_D=(<D,z>)_(z in Z)`, then

\[
\boxed{
\|QD_+\|^2=\|D\|^2-W_M-b_D^*\Gamma^+b_D.}        \tag{56.4}
\]

No double counting occurs because `g_M` is orthogonal to the full probe span.

## Critical normalized target

For `[M,B)=[219,231)`, the exact finite quantities are

\[
W_{219}=2.340708063678477\ldots,
\]

\[
\|QD_{218}\|^2=2.399113472267766\ldots,
\]

and the normalized repair threshold is

\[
2.385779546739042\ldots.
\]

Thus the below-`M` witness leaves the exact normalized shortfall

\[
\boxed{0.045071483060565\ldots,}                   \tag{56.5}
\]

while the actual residual beyond it is

\[
\|QD_+\|^2=0.058405408589289\ldots.
\]

The surviving normalized budget is `0.013333925528724...`.

## First-shell floor-rank obstruction

On the matched first shell of `r=B-M` consecutive cells and the `r`
consecutive new rows, the floor matrix contains the unit triangular block

\[
\left(\mathbf1_{j\ge i}\right)_{0\le i,j<r}.
\]

After the common linear moment is removed, orthogonality to all `r` rows forces
all `r` detectable cell masses to vanish. Since the old state is affine on each
cell, every witness supported on exactly those matched cells has zero
correlation with `D`. More generally, `s` cells leave at most `s-r` detectable
mass directions. Hence a nontrivial post-cutoff witness requires surplus cells
or global-tail structure.

Using fourteen consecutive cells gives an exact determinant witness, but its
gain is only `O(log^2(M)/M^4)`. After multiplication by the block weight it is
`O(1/(M^5 log M))`, negligible compared with the critical shortfall. Rank alone
does not provide the required scale.

## Finite lagged-state repair

For the three windows missed in Cycle 55, adjoining one residualized global old
state `D_(M-3)` repairs the shortfall at 256-bit Arb precision. If

\[
x^\perp=Q D_{M-3}-{\langle D_{M-3},g_M\rangle\over W_M}g_M,
\]

the extra Schur gain is

\[
\boxed{
G={|\langle QD-g_M,x^\perp\rangle|^2\over\|x^\perp\|^2}.} \tag{56.6}
\]

The certified gains and final repaired margins are:

| window | extra payment `A G` | repaired margin |
|---|---:|---:|
| `[219,231)` | `1.60165041829e-5` | `8.85362206864e-7` |
| `[220,231)` | `1.46040777375e-5` | `9.78785848974e-6` |
| `[222,226)` | `6.65956762393e-6` | `2.49360151164e-6` |

This is non-tautological on these three windows, but `D_(M-3)` imports almost
the entire global old prefix. One or two new reciprocal rows and one- or
two-cell post-`M` impulses are far too weak. The finite repair supplies no
uniform theorem.

## Complexity no-go

On `(M,3M/2)`, the old rows with `M/2<a<3M/4` have distinct jumps at `2a` and
are linearly independent, giving `Omega(M)` old-state dimension. Therefore no
fixed number of scalar post-`M` probes can control arbitrary old coefficient
vectors uniformly. A theorem for the physical Möbius vector must force its
residual into special Vasyunin-correlated directions; floor rank, support, and
Gram positivity alone cannot do so.

The active target is now the specific residual quantity (56.4), not another
fixed local witness. No additive-12 theorem or RH result is claimed.
