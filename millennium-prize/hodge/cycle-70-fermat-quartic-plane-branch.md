# Cycle 70: the Fermat quartic plane branch

Let

\[
X_0:\ x_0^4+\cdots+x_5^4=0\subset\mathbf P^5.
\]

Choose `a_i^4=-1` and

\[
P:\ x_0=a_0x_1,\quad x_2=a_1x_3,\quad x_4=a_2x_5.
\]

The root condition is essential: coordinate planes or choices with `a_i^4=1`
are not contained in this quartic.

The Jacobian ring is

\[
R=\mathbf C[x_0,\ldots,x_5]/(x_0^3,\ldots,x_5^3),
\]

with `H^(3,1)_prim=R_2`, `H^(2,2)_prim=R_6`, and deformation tangent `R_4`.
Up to nonzero scalar, the plane class is represented by

\[
p_P=\prod_{i=0}^2(u_i^2+a_i u_iv_i+a_i^2v_i^2)\in R_6.          \tag{70.1}
\]

Diagonal rescaling reduces rank to multiplication by
`prod_i(u_i^2+u_iv_i+v_i^2)` over the rationals. The exact verifier
`verify_cycle70_fermat_quartic.py` proves

\[
\boxed{\dim R_4=90,\quad\dim R_{10}=21,
\quad\operatorname{rank}(R_4\xrightarrow{\cdot p_P}R_{10})=6.}   \tag{70.2}
\]

Thus the selected Hodge tangent space has codimension six.

A fixed plane imposes `h^0(O_P(4))=15` conditions and `Gr(3,6)` has dimension
nine, so plane incidence has codimension six. At `(X_0,P)`, the normal map on
sections is

\[
(\ell_0,\ell_1,\ell_2)\mapsto\ell_0u^3+\ell_1v^3+\ell_2w^3.
\]

Its nine monomials are distinct; the verifier proves rank nine and hence
`H^0(N_(P/X_0))=0`. The incidence image is a smooth codimension-six germ.

The universal relative plane supplies a scheme-theoretic inclusion into the
selected Hodge germ. The period Jacobian has rank six by (70.2), making that
Hodge germ smooth of codimension six. Inclusion plus equal smooth dimension
therefore gives

\[
\boxed{
\widehat{\operatorname{im}(\mathrm{Incidence})}_{(X_0,P)}
=\widehat{\mathrm{Hodge}}_{(X_0,[P]_{prim})}.}                    \tag{70.3}
\]

There are 21 period pairings before rank reduction; six suitable combinations
have independent differentials. This is one selected formal branch of an
already algebraic class, not a new case of the official Hodge conjecture.

The new main funnel targets componentwise relative-cycle domination for marked
Hodge components of hypersurface fourfolds. The immediate next lemma must join
scheme-theoretic cycle inclusion, generic IVHS dimension equality, and Hilbert
obstruction control to prove dominance onto a specified component. No full
Hodge result is claimed.
