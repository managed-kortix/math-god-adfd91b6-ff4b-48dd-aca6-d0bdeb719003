# Cycle 140: all 33 adjacent extension cones retain a diagonal obstruction

For the actual adjacent Fermat pair of Cycles 138--139, every nonzero graded
extension class gives an `8|8` cone whose first mixed-characteristic obstruction
is nonzero.  The decisive point is not separate component nonliftability alone:
the complete lower-left transfer map must also be unable to absorb the diagonal
class.  Here that transfer vanishes on cohomology, and an exact common
coefficient functional detects the surviving 76-term Fermat carry.

Let

\[
L=V(q,r,s),\qquad M=V(p,r,s),
\]

inside the actual transformed standard Fermat special fiber.  Cycle 138 gives

\[
\operatorname{Ext}^1(L,M)_0\simeq k^2,
\]

so the nonzero extension cones are indexed by

\[
\mathbf P^1(\mathbf F_{32}),
\]

with 33 points.

For an extension class `phi`, the full first-order correction may contain an
unrestricted lower-left cocycle `c`.  Its contribution to the two diagonal
obstruction classes is

\[
\mu_\phi([c])=([\phi c],[c\phi]).
\]

An explicit local/global Koszul calculation gives

\[
\operatorname{Ext}^1(L,M)
\simeq\operatorname{Ext}^1(M,L)
\simeq H^0(\mathbf P^1,O(1)),
\]

while both opposite Yoneda products into the component `Ext^2` groups vanish.
Hence

\[
\boxed{\mu_\phi=0}
\]

for every one of the 33 projective extension classes.  This closes the loophole
identified in Cycle 139: lower-left corrections can alter diagonal defects in
general, but not for this adjacent pair.

The genuine transformed standard Fermat `W_2` potential differs from the
coefficientwise lifted sparse normal form by the Cycle 139 carry.  Its support
is 76 and its pinned hash is

```text
883504597c5e7284aa84d9742da8c651fc259d6f0abf088d6dca86a38633b69b
```

After divided-carry normalization and restriction to either plane, the scalar
class has 16 terms.  Each component Koszul boundary space has rank nine, and
adjoining the carry raises the rank to ten.

For every projective `phi`, adjoining the two possible extension-transfer
columns gives

\[
\boxed{\operatorname{rank}M_\phi=11},\qquad
\boxed{\operatorname{rank}[M_\phi\mid h]=12}.
\]

A uniform left functional is coefficient extraction at

\[
z_1^{16}p^{17}\quad\text{on }L,
\qquad
z_1^{16}q^{17}\quad\text{on }M.
\]

It vanishes on all nine component boundary columns and all extension-transfer
columns, but evaluates to

\[
13\ne0\in\mathbf F_{32}
\]

on the carry.  Its normalized value is one because `13^{-1}=15`.

Therefore the diagonal obstruction pair remains nonzero modulo the complete
lower-left cohomological transfer for every adjacent cone.  No upper-right
compatibility or higher Massey equation can repair an already-unsolved diagonal
lifting equation.  Consequently all 33 specified extension cones are
obstructed as graded matrix factorizations of the fixed transformed standard
Fermat model over `W_2(F_32)`.

The deterministic 66-record aggregate hash is

```text
0f01205954b0393a9136c4ba71b0cf45dc3cf471075951713b74f07857280b57
```

This closes the minimal adjacent two-plane extension-cone ansatz.  It does not
obstruct larger twisted complexes, different coupled matrix factorizations,
other characteristic-two objects, relative Chow cycles, or the Hodge
conjecture.  Even a first-order survivor would still require compatible
all-order perfect lifts, algebraization, and a verified rational codimension-two
Chern character.

Reproduce with

```sh
python3 millennium-prize/hodge/verify_cycle140_adjacent_cone_obstruction.py
```

No Hodge or Millennium solution is claimed.
