# Cycle 244: shifted two-arrow return path audit

## Exact counterexample to the support-cycle step

Work over `K=Q(i)` with the graph sheaves

\[
 F_k=O_{\Gamma_{u^k}},\qquad u=2+i.
\]

Take the smallest pair `F_0,F_1`.  Since

\[
 N(u-1)^3=N(1+i)^3=2^3=8,
\]

both cross groups `Ext^3(F_0,F_1)` and `Ext^3(F_1,F_0)` have dimension
eight.  Serre duality and Yoneda composition give a perfect pairing

\[
 \operatorname {Ext}^3(F_0,F_1)\otimes
 \operatorname {Ext}^3(F_1,F_0)
 \longrightarrow \operatorname {Ext}^6(F_0,F_0)=K\omega _0.
\]

Choose normalized dual vectors `x=x_(01,0)` and `y=x_(10,0)`.  With the
Cycle 241 multiplication convention,

\[
 yx=\omega _0,\qquad xy=-\omega _1.                         \tag{244.1}
\]

The second sign follows from graded cyclicity because both unshifted classes
have odd degree three.  In particular, neither product vanishes.

Now use the three shifted cells

\[
 A=F_0[0],\qquad B=F_1[2],\qquad C=F_0[4].
\]

Under the convention

\[
 \operatorname {Hom}^d(F_i[r],F_j[s])
 =\operatorname {Ext}^{d-r+s}(F_i,F_j),                       \tag{244.2}
\]

the maps

\[
 A\mathrel{\mathop{\longrightarrow}^{x}}B
 \mathrel{\mathop{\longrightarrow}^{y}}C                    \tag{244.3}
\]

both have shifted degree one:

\[
 1-0+2=3,\qquad 1-2+4=3.
\]

Their composite has shifted degree two and is the nonzero same-support block

\[
 yx=\omega _0\in
 \operatorname {Hom}^2(F_0[0],F_0[4])
 =\operatorname {Ext}^{2-0+4}(F_0,F_0)
 =\operatorname {Ext}^6(F_0,F_0).                              \tag{244.4}
\]

This is support-diagonal but cell-off-diagonal: its source and target are
different shifted copies of `F_0`.  The trace sends `omega_0` to one by the
chosen normalization, so (244.4) is an actual nonzero Ext class, not merely a
formal composable word.

Thus the shifts do not telescope on a path which returns to the same support
but to a different shifted copy.  They telescope only on a closed path of
cells, whose final shifted object equals its initial shifted object.  The cell
quiver in (244.3) is acyclic (`A<B<C`), while its support labels form the return
`0 -> 1 -> 0`.

There is no hidden suspension-sign escape.  We transport composition to the
shifted category without an additional sign, as in the Cycle 241 binary
algebra, and obtain `+omega_0`.  Under the other common suspension transport,
the displayed composite can become `-omega_0`; its nonvanishing is unchanged.
The invariant content is the perfect Ext pairing and the unit coefficient in
(244.1).

## What this breaks

Cycle 200 argues that every term leaving and returning to a graph vertex would
give a directed cycle, and therefore that all cross terms capable of changing
a same-vertex obstruction block are absent.  Path (244.3) is an exact
counterexample to that inference: acyclicity of the shifted-cell quiver does
not imply acyclicity after cells with the same support are grouped together.
Consequently the claimed direct collection of single-support obstruction
blocks is not established by the printed topological-order argument.

Cycle 241 invokes the Cycle 200 finite-twisted-complex theorem at its final
Atiyah-obstruction step.  The connective Karoubi splitting theorem is not
refuted by (244.3), but the stated deduction of `KI240 PASS` is no longer
certified. A refinement by cell order, shift, support, or bar length does not by
itself repair the argument: the nonzero return survives as a possible higher
differential or extension on a later page. A valid repair must compute those
differentials or produce a chain-level functional proving the diagonal Atiyah
class is a permanent cycle for every finite packet.

## Why this is not an Atiyah cancellation

The product in (244.4) is top self-Ext viewed as total degree two between
different shifts.  It is not an element of

\[
 \operatorname {Hom}^2(F_0[r],F_0[r])=
 \operatorname {Ext}^2(F_0,F_0),
\]

where the one-cell Atiyah obstruction lives.  Moreover, if the two arrows in
(244.3) are put by themselves into a strictly upper-triangular candidate
differential

\[
 Q=\begin{pmatrix}0&0&0\\x&0&0\\0&y&0\end{pmatrix},
\]

then

\[
 (Q^2)_{C,A}=yx=\omega _0\ne0.                                  \tag{244.5}
\]

Hence this two-arrow packet fails the Maurer--Cartan equation and is not a
twisted complex.  It cannot itself carry, much less cancel, an Atiyah
obstruction.  A genuine cancellation would require an explicit finite packet
whose complete Maurer--Cartan curvature vanishes and a degree-one endomorphism
`h` satisfying

\[
 \partial h=o_v,
 \qquad \partial h=Qh+ hQ
\]

for the relevant degree-two obstruction cocycle (with the displayed sign for
`|h|=1`).  No such packet or primitive is supplied here.

The exact conclusion is therefore:

\[
 \boxed{\text{nonzero shifted same-support block; proof step refuted; no
 demonstrated Atiyah cancellation.}}
\]

This reopens the finite graph-envelope obstruction proof and hence its use in
`KI240`, but it neither disproves `KI240` nor has a Hodge-conjecture consequence.

## Finite verification

Run

```sh
python3 millennium-prize/hodge/verify_cycle244_shifted_return.py
python3 millennium-prize/hodge/verify_cycle244_shifted_return.py --check
```

The artifact records the field, shifts, unshifted and shifted degrees, pairing
signs, sparse matrices, nonzero curvature block, and scope of the conclusion.
