# Cycle 204: the smallest weighted Pfaffian center is still horizontal

## Weighted Buchsbaum--Eisenbud format

Let `N_1,...,N_5` be line-bundle classes and suppose

\[
        2T=N_1+\cdots+N_5.                                      \tag{204.1}
\]

An alternating `5 x 5` matrix with entry `(i,j)` in
`H^0(T-N_i-N_j)` has submaximal Pfaffians of classes `N_i`.  Its
height-three Pfaffian center `W` has resolution

\[
0\longrightarrow O(-T)\longrightarrow
 \bigoplus_iO(-(T-N_i))\longrightarrow
 \bigoplus_iO(-N_i)\longrightarrow O\longrightarrow O_W
 \longrightarrow0.                                               \tag{204.2}
\]

Consequently

\[
\operatorname {ch}(O_W)=1-\sum_i e^{-N_i}
 +\sum_i e^{-(T-N_i)}-e^{-T},                                    \tag{204.3}
\]

and its first nonzero component is

\[
\boxed{\operatorname {ch}_3(O_W)=
 C(N):={\sum_iN_i^3-\sum_i(T-N_i)^3+T^3\over6}.}                 \tag{204.4}
\]

Writing `e_k=e_k(N_1,...,N_5)`, this is equivalently

\[
             C(N)={e_1^3-4e_1e_2+8e_3\over8}.                    \tag{204.5}
\]

For a contained graph `G`, the canonical liaison sheaf therefore has

\[
              \operatorname {ch}_3(I_G/I_W)=C(N)-[G].             \tag{204.6}
\]

Thus cancellation of the first graph obstruction is possible only if the
universal center class satisfies

\[
 \kappa(C(N))=\kappa([G]),                                       \tag{204.7}
\]

where `kappa` is contraction with a PEL tangent.  In particular, cancellation
for `Gamma_I` (respectively `Gamma_D`) requires exceptional coefficient `1`
(respectively `3`) in the normalization of Cycle 152.

## The formal nonhorizontal solution

For arbitrary divisor classes `X,Y,Z,H`, put

\[
(N_1,N_2,N_3,N_4,N_5)=(X,Y,Z,H,X+Y+Z-H),\qquad T=X+Y+Z.          \tag{204.8}
\]

Direct substitution in (204.4) gives the exact identity

\[
                         \boxed{C(N)=XYZ}.                        \tag{204.9}
\]

Hence the weighted `5 x 5` format has enough formal freedom to manufacture a
nonhorizontal cubic, and choosing `XYZ` with graph contraction would cancel
(204.6).  This is not yet a geometric center: the ten matrix-entry classes
include

\[
T-N_1-N_5=H-X,\quad T-N_2-N_5=H-Y,\quad
T-N_3-N_5=H-Z,                                                     \tag{204.10}
\]

as well as `T-N_1-N_2=Z`, `T-N_1-N_3=Y`, and `T-N_2-N_3=X`.
Effectivity therefore demands simultaneous inequalities that are very
restrictive; setting `H=0` recovers the clean identity but forces negative
entry classes.

## Smallest integral effective test

Test the smallest polarization-weight model by taking every class to be an
integer multiple of a fixed ample class `P`: `N_i=n_iP`, with `n_i>0`,
`2t=sum n_i`, and every entry effective:

\[
                       t-n_i-n_j\geq0.                            \tag{204.11}
\]

Then

\[
C(N)=c(n)P^3,\qquad
c(n)={\sum_i n_i^3-\sum_i(t-n_i)^3+t^3\over6}.                   \tag{204.12}
\]

Exact enumeration in increasing total weight gives:

* the unique smallest weakly effective vector, up to permutation, is
  `(1,1,1,1,2)`, with `t=3` and `c=1`;
* four entry degrees are zero, so the format is not a genuinely positive
  weighted center;
* if every entry degree is positive, the unique smallest vector is
  `(2,2,2,2,2)`, with `t=5` and `c=5`.

Both classes are multiples of `P^3`, hence PEL-horizontal.  The first has the
numerical coefficient needed for `Gamma_I`, but its contraction is zero rather
than the graph map.  The second is merely the homogeneous Cycle 203 center.
Thus scalar weights cannot cancel either graph obstruction.

There is a useful near miss with three formal directions.  Among nonnegative
coordinate weights having nonzero total degree for all five generators and all
ten entries, the first vector total that attains exceptional coefficient `3`
is `14`; one representative is

\[
\begin{aligned}
N_1&=Y+Z,&N_2&=X+2Z,\\
N_3&=N_4=N_5=X+Y+Z,&T&=2X+2Y+3Z.
\end{aligned}                                                     \tag{204.13}
\]

But its center cubic is

\[
C(N)=X^2Y+X^2Z+XY^2+3XYZ+2XZ^2+2Y^2Z+2YZ^2+Z^3.                 \tag{204.14}
\]

The desired graph-sized `3XYZ` is inseparable from seven contaminating mixed
terms.  Unless their PEL contractions vanish by additional geometric
relations, (204.14) does not cancel `Gamma_D`.

## Bounded conclusion

The universal weighted Chern character is (204.3)--(204.6).  A formal exact
solution `C(N)=XYZ` exists, so there is no identity-level Pfaffian no-go.
However, the smallest integral effective one-ray formats are horizontal, and
the smallest positive format is exactly homogeneous.  The first effective
three-direction coefficient match has unavoidable contamination.  Therefore
the smallest weighted `5 x 5` center does not cancel the horizontal-plus-graph
obstruction.  Any continuation must exhibit actual effective divisor classes
whose complete cubic (not only one monomial coefficient) has contraction equal
to the graph map.  No Hodge-conjecture result is claimed.

Reproduce all identities and bounded searches with

```sh
python3 millennium-prize/hodge/verify_cycle204_weighted_pfaffian.py
```
