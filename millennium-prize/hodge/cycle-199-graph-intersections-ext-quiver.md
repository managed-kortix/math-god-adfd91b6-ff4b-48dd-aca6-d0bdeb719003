# Cycle 199: exact graph intersections and the extension quiver

Let `X=E_i^3`, `A=X x X`, `u=2+i`, and

\[
 \Gamma_k=\Gamma_{u^k}=\{(x,u^kx):x\in X\},\qquad 0\leq k\leq6.
\]

This computes every pair among the seven graph objects used by the
denominator-cleared Weil projector.  All calculations are integral Gaussian
linear algebra; in particular, no floating-point rank or intersection test is
used.

## Exact Gaussian matrices

The powers are

\[
(u^0,\ldots,u^6)=(1,2+i,3+4i,2+11i,-7+24i,-38+41i,-117+44i).
\]

For `i<j`, put `delta_ij=u^j-u^i`.  The scheme intersection is

\[
 \Gamma_i\cap\Gamma_j=\ker[\delta_{ij}:X\longrightarrow X].
\]

If `delta=a+bi`, multiplication on the integral lattice of `X` has the exact
matrix

\[
 M(\delta)=\operatorname {diag}(R(\delta),R(\delta),R(\delta)),\qquad
 R(\delta)=\begin{pmatrix}a&-b\\b&a\end{pmatrix}.                 \tag{199.1}
\]

It has nonzero determinant `N(delta)^3`.  Thus every distinct pair intersects
in dimension zero, with expected dimension zero and excess zero.  The table
also records the scheme length.  If `g=gcd(|a|,|b|)`, the Smith invariants of
one block are `(g,N(delta)/g)`; the canonical six invariant factors of (199.1)
are `(g,g,g,N(delta)/g,N(delta)/g,N(delta)/g)`.

| pair | `delta_ij` | block Smith | `N(delta_ij)` | intersection dimension | excess | length |
|---|---:|---:|---:|---:|---:|---:|
| 01 | `1+i` | `(1,2)` | 2 | 0 | 0 | 8 |
| 02 | `2+4i` | `(2,10)` | 20 | 0 | 0 | 8000 |
| 03 | `1+11i` | `(1,122)` | 122 | 0 | 0 | 1815848 |
| 04 | `-8+24i` | `(8,80)` | 640 | 0 | 0 | 262144000 |
| 05 | `-39+41i` | `(1,3202)` | 3202 | 0 | 0 | 32829478408 |
| 06 | `-118+44i` | `(2,7930)` | 15860 | 0 | 0 | 3989418056000 |
| 12 | `1+3i` | `(1,10)` | 10 | 0 | 0 | 1000 |
| 13 | `10i` | `(10,10)` | 100 | 0 | 0 | 1000000 |
| 14 | `-9+23i` | `(1,610)` | 610 | 0 | 0 | 226981000 |
| 15 | `-40+40i` | `(40,80)` | 3200 | 0 | 0 | 32768000000 |
| 16 | `-119+43i` | `(1,16010)` | 16010 | 0 | 0 | 4103684801000 |
| 23 | `-1+7i` | `(1,50)` | 50 | 0 | 0 | 125000 |
| 24 | `-10+20i` | `(10,50)` | 500 | 0 | 0 | 125000000 |
| 25 | `-41+37i` | `(1,3050)` | 3050 | 0 | 0 | 28372625000 |
| 26 | `-120+40i` | `(40,400)` | 16000 | 0 | 0 | 4096000000000 |
| 34 | `-9+13i` | `(1,250)` | 250 | 0 | 0 | 15625000 |
| 35 | `-40+30i` | `(10,250)` | 2500 | 0 | 0 | 15625000000 |
| 36 | `-119+33i` | `(1,15250)` | 15250 | 0 | 0 | 3546578125000 |
| 45 | `-31+17i` | `(1,1250)` | 1250 | 0 | 0 | 1953125000 |
| 46 | `-110+20i` | `(10,1250)` | 12500 | 0 | 0 | 1953125000000 |
| 56 | `-79+3i` | `(1,6250)` | 6250 | 0 | 0 | 244140625000 |

For `i=j`, the intersection is the common threefold `Gamma_i`; relative to
the codimension-three expected self-intersection, its clean excess is three.

## Ext groups

Write `F_k=O_{Gamma_k}`.  Each graph has trivial rank-three normal bundle.
The regular-embedding calculation gives

\[
 \operatorname {Ext}^r_A(F_k,F_k)
 \simeq\bigoplus_{p+q=r}H^p(\Gamma_k,O)\otimes\bigwedge^qN_{\Gamma_k/A},
\]

so the self-Ext dimensions in degrees `0,...,6` are

\[
 (1,6,15,20,15,6,1).                                             \tag{199.2}
\]

In particular, a diagonal pair has `Ext^1` dimension six and `Ext^2`
dimension fifteen.

For `i != j`, the two smooth threefolds meet transversely in the finite scheme
above.  The cross-Ext calculation is concentrated in degree three:

\[
 \operatorname {Ext}^r_A(F_i,F_j)=0\quad(r\ne3),\qquad
 \operatorname {Ext}^3_A(F_i,F_j)\simeq
 H^0(\Gamma_i\cap\Gamma_j,O).                                    \tag{199.3}
\]

Consequently, for every ordered distinct pair,

\[
 \boxed{\dim\operatorname {Ext}^1(F_i,F_j)=
 \dim\operatorname {Ext}^2(F_i,F_j)=0,}
\]

while the dimension of `Ext^3(F_i,F_j)` is the length in the table.  Formula
(199.3) includes nonreduced intersection schemes; replacing length by the
number of geometric points would in general be incorrect.

## Extension quiver and obstruction mixing

The ordinary `Ext^1` quiver has vertices `0,...,6` and no arrows between
distinct vertices.  Each vertex has a six-dimensional self-`Ext^1` space, but
these loops deform one graph object and do not couple two projector summands.
There are therefore no unshifted graph pairs admitting a non-split ordinary
extension.

Nor does any distinct pair allow degree-two diagonal obstruction mixing:
`Ext^1` and `Ext^2` both vanish crosswise.  Shifting objects does not repair
this.  Opposite cross classes then have degrees

\[
 3+r-s\quad\hbox{and}\quad3+s-r,
\]

whose sum is six, so they cannot both be degree-one arrows.  Any opposite
Yoneda return product lands in self-`Ext^6`, not the self-`Ext^2` group that
contains the Atiyah obstruction.  Thus the list of degree-two
obstruction-mixing pairs among `Gamma_(u^k)` is empty.

The calculation decisively retires extensions built only from these seven
scalar graph sheaves.  The next candidate must have a positive-dimensional,
nontransverse intersection (or genuinely new support), together with explicit
cross-`Ext^1` classes and a nonzero opposite Yoneda transfer into self-`Ext^2`.
This is a candidate-architecture no-go, not a Hodge-conjecture result.

Reproduce all powers, determinants, Smith invariants, lengths, and quiver
dimensions with

```sh
python3 millennium-prize/hodge/verify_cycle199_graph_ext_quiver.py
```
