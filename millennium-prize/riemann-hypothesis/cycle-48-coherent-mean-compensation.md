# Cycle 48: coherent weighted-mean compensation

## Exact finite split

For a fixed physical block, abbreviate

\[
f=F_M,\quad m=\bar F_{M,B},\quad P=\|f\|^2,
\quad W=W_{M,B},\quad V=V_{M,B},
\]

and retain the Cycle 47 reserve `S=P-<f,m>`. The finite terminal budget has the
exact split

\[
\boxed{
Q_{M,B}=(S-V)+\langle f,m\rangle-W\|m\|^2.}       \tag{48.1}
\]

Thus packet surplus and the coherent weighted-mean channel are logically
separate. If `V<=S`, the additional coherent ball condition

\[
\boxed{\langle f,m\rangle\ge W\|m\|^2}            \tag{48.2}
\]

is sufficient for `Q_(M,B)>=0`. It is equivalent to

\[
\left\|m-{f\over2W}\right\|\le {\|f\|\over2W},   \tag{48.3}
\]

or, for `T=Wm`, to `||T||^2<=<f,T>`.

Condition (48.2) is not necessary because positive packet surplus may pay a
coherent deficit. The sharp compensated condition is simply

\[
\boxed{
S-V\ge W\|m\|^2-\langle f,m\rangle,}              \tag{48.4}
\]

which is equivalent to `Q_(M,B)>=0`. Its value is diagnostic rather than a new
proof principle; the useful objective is an arithmetic decomposition proving
(48.4) with separately controlled channels.

## Generic geometry does not close the channel

The distinguished anchor has weight `w=w_M`. If `W>w`, deleting it from the
packet gives the exact variance decomposition

\[
\boxed{
V={wW\over W-w}\|f-m\|^2+V_-,\qquad V_-\ge0.}    \tag{48.5}
\]

This is a lower bound for the subtracted quantity `V`, so substituting it into
(48.1) gives an upper bound for `Q`, not a lower bound. Reversing this logic is
invalid. The coefficient is sharp, with equality precisely when every
non-anchor vector is equal.

Atomic antialignment, strict packet square-payment, and a fixed affine
coordinate still do not force (48.2) or terminal positivity. Exact rational
Hilbert countermodels exist with all three properties and `Q<0`. The common
affine coordinate yields an orthogonal Schur component only after projecting
`chi` off the fractional-part span; it gives a lower bound on `||m||`, whereas
terminal positivity needs an upper bound. Therefore the actual prescribed
Mobius taper and complete affine--Vasyunin correlations must enter.

## Complete finite certificate through 512

The standalone 192-bit Arb verifier evaluates every one of the `130305` blocks
`2<=M<B<=512` from the complete restricted Vasyunin formula. It certifies:

- `Q_(M,B)>0` and `S_(M,B)-V_(M,B)>0` on every block;
- the smallest absolute terminal budget is
  `Q_(511,512)=0.0725258206088661919861338541780966...`;
- the weakest relative terminal budget occurs at `(2,512)` and equals
  `Q_(2,512)/P_2=0.178030395165032265126620975667052...`;
- the pure coherent condition (48.2) fails on exactly `486` blocks, namely
  `(M,B)=(2,B)` for `27<=B<=512`;
- on the weakest coherent block `(2,512)`,
  `<f,m>/(W||m||^2)=0.860852438305205273326362124284257...<1`, yet packet
  surplus more than pays the deficit;
- the compensated ratio
  `(W||m||^2-<f,m>)/(S-V)` is always strictly below `1`, with maximum
  `0.337647750522200002484470948925621...` at `(2,512)`.

Hence imposing the split condition (48.2) would discard genuine favorable
physical blocks. The finite data instead point to a compensated theorem in
which the packet surplus and coherent deficit are estimated together. This is
a finite certificate only and gives no control of the omitted infinite tail.

## Reproduction

```text
uv run --with python-flint python verify_cycle48_coherent_channel.py \
  --max-n 512 --bits 192
```

The verifier checks six independent identities per block, all denominator and
sign conditions, and every strict Arb comparison. No terminal sign theorem or
RH result is claimed.
