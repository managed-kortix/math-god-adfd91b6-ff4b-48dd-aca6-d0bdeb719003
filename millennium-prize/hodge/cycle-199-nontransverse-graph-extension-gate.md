# Cycle 199: clean graph extensions do not alter the Weil class or dense-open obstruction

## Smallest nontransverse pair

Let

\[
X=E_i^3\times E_i^3,
\qquad F_0=O_{\Gamma_I},
\qquad F_1=O_{\Gamma_D},
\qquad D=\operatorname {diag}(3,1,1).
\]

The graphs meet cleanly along

\[
Y=\Gamma_I\cap\Gamma_D=E_i[2]\times E_i^2,
\]

a disjoint union of four abelian surfaces. This is the smallest scalar-diagonal
modification of the diagonal graph for which the intersection has positive
dimension and the cross `Ext^2` group is nonzero.

Write `d=dim Y=2`, `c=codim_X Gamma_I=3`, and let

\[
e=\operatorname {rk}E=\dim X-\dim\Gamma_I-\dim\Gamma_D+\dim Y=2
\]

be the excess. The common tangent directions in the two graphs are the last
two elliptic factors. The two excess directions are the corresponding common
normal directions. The remaining first-coordinate normal direction is the
unique transverse normal line `L`. All these bundles are trivial on each
component of `Y`.

## Excess-intersection Ext algebra

The clean-intersection Koszul calculation gives

\[
\mathcal Ext_X^q(F_0,F_1)
 \simeq \bigwedge^{q-1}E^\vee\otimes L,
\qquad q=1,2,3,
\]

and zero otherwise. Since all bundles are trivial and the local-to-global
spectral sequence degenerates,

\[
\operatorname {Ext}_X^n(F_0,F_1)
 \simeq H^*(Y,O_Y)\otimes L[1]\otimes\bigwedge^*E^\vee.
\]

Equivalently, on each connected component, with `h_1,h_2` the cohomology
degree-one generators, `tau` the transverse generator of degree one, and
`e_1,e_2` the excess generators of degree one,

\[
\operatorname {Ext}^*(F_0,F_1)
 \simeq \tau\,\bigwedge(h_1,h_2,e_1,e_2).
\]

The four components multiply every dimension by four, hence

\[
\dim\operatorname {Ext}^n(F_0,F_1)=4(1,4,6,4,1),
\qquad 1\le n\le5.
\]

In particular,

\[
\operatorname {Ext}^1(F_0,F_1)=H^0(Y,L)\simeq\mathbb C^4,
\]

and

\[
\operatorname {Ext}^2(F_0,F_1)
 \simeq H^1(Y,L)\oplus H^0(Y,L\otimes E^\vee)
 \simeq\mathbb C^{16}.
\]

Thus the requested cross `Ext^2` is explicit: its eight local excess classes
are `tau e_1,tau e_2` on the four components, and its eight global classes are
`h_1 tau,h_2 tau`.

Composition is wedge product after the natural clean-intersection pairings.
For a reverse degree-one class `sigma in Ext^1(F_1,F_0)`, both `tau` and
`sigma` use the same unique transverse conormal line. Therefore

\[
\boxed{\sigma\circ\tau=\tau\circ\sigma=0}
\]

in self `Ext^2`: locally this product contains the square of one odd transverse
generator. Cross `Ext^2` being nonzero does not change this return-product
calculation.

## The smallest exact objects

Choose a nonzero component class `tau in Ext^1(F_1,F_0)`. It defines the
ordinary nonsplit extension

\[
0\longrightarrow F_0\longrightarrow E_\tau
 \longrightarrow F_1\longrightarrow0,
\qquad
E_\tau\simeq\operatorname {Cone}(F_1[-1]\xrightarrow{\tau}F_0).
\]

This is the smallest exact non-split object: two unshifted graph sheaves and one
cross degree-one class. A cross class

\[
\xi\in\operatorname {Ext}^2(F_1,F_0)
\]

instead gives the two-summand twisted complex

\[
C_\xi=\operatorname {Tot}(F_1[-1]\xrightarrow{\xi}F_0),
\]

where the arrow has cohomological degree one after shifting. The notation is a
twisted-complex totalization, not the ordinary cone of a degree-zero morphism.
This is the smallest object that uses cross `Ext^2` itself, but it is not an
ordinary sheaf extension.

Their additive `K_0` classes differ because the cross-`Ext^2` construction uses
one shifted vertex:

\[
[E_\tau]=[F_0]+[F_1],
\qquad [C_\xi]=[F_0]-[F_1].
\]

Consequently their Chern characters are independent of the gluing class:

\[
\operatorname {ch}_3(E_\tau)=[\Gamma_I]+[\Gamma_D],
\qquad
\operatorname {ch}_3(C_\xi)=[\Gamma_I]-[\Gamma_D].
\]

For a diagonal graph `Gamma_M`, the pure exceptional determinant coefficient is
`det(M)`. Thus

\[
P_W\operatorname {ch}_3(E_\tau)
=(1+3)P_W[\Gamma_I]=4P_W[\Gamma_I]\ne0,
\]

whereas

\[
P_W\operatorname {ch}_3(C_\xi)
=(1-3)P_W[\Gamma_I]=-2P_W[\Gamma_I]\ne0.
\]

The extension realizes a nonzero Weil projection, but it cannot realize the
signed seven-graph projector class merely by changing `tau` or `xi`: cones do
not change `K_0`. Signs require shifts or additional summands, returning to the
Cycle 153 block problem.

## Atiyah obstruction audit

For `B in T_0S=M_3(C)`, the two graph obstructions are

\[
\rho_0(B)=Q^{-1}B^t-B,
\qquad
\rho_1(B)=Q^{-1}B^t-DB,
\qquad Q=\operatorname {diag}(1,1,3).
\]

If either cone had zero Atiyah obstruction, restriction to the dense open
`U_j=Gamma_j\setminus Y` would have zero obstruction. On `U_j` the other
component and every cross extension class vanish, while the cone restricts to
`F_j`. Hence zero obstruction would force

\[
\rho_0(B)=\rho_1(B)=0.
\]

Subtracting gives `(D-I)B=0`, so the first row of `B` is zero. Substitution in
`Q^{-1}B^t=B` then leaves only

\[
B=\begin{pmatrix}0&0&0\\0&b&0\\0&0&0\end{pmatrix}.
\]

Therefore these necessary dense-open equations have a one-dimensional common
kernel: the componentwise obstruction already detects eight independent PEL
directions. The extension compatibility terms are supported on `Y`; they can vary
or obstruct the chosen gluing class but cannot cancel either dense-open graph
obstruction. In particular,

\[
\boxed{\dim\ker(o_{E_\tau})\le1,
\qquad\dim\ker(o_{C_\xi})\le1.}
\]

Equivalently, each obstruction map has rank at least eight. The exact rank may
acquire an additional gluing obstruction in the surviving direction, but it
can never be zero. This kills every extension or cone of
this clean pair at the Cycle 198 rank-zero gate, independently of the chosen
class in cross `Ext^1` or cross `Ext^2`.

## Outcome

The smallest nontransverse graph object is the ordinary two-factor extension
`E_tau`; the smallest object genuinely using cross `Ext^2` is `C_xi`. Both
have explicit finite excess-intersection Ext algebras and nonzero projected
`ch_3`, but neither has any potential for full nine-direction Atiyah
cancellation. This is stronger than the vanishing degree-one return product:
the dense-open restriction proves that no intersection-supported higher
correction can cancel component holomorphicity failure.

Thus nonzero cross `Ext^2` alone is not the missing mechanism. The next
candidate must be a single object whose generic support is not a union of
individually obstructed graphs--for example a globally defined complex with a
differential nonzero on every dense component, or genuinely new connected
support. No Hodge case is proved here.
