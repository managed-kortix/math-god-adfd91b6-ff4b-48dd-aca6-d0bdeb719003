# Cycle 39: rational coefficient-path counterexamples at kappa = 1/2

## 1. Rational model of the exact update

The coefficient kinematics can be separated from the transcendental values of
the logarithms.  Choose increasing positive rational numbers `L_n`, put

\[
 x_n=L_n^{-1},\qquad h_n=x_n-x_{n+1},\qquad
 w_n=h_nL_n=1-{L_n\over L_{n+1}},
\]

and assign signs `epsilon_q` in `{0,+1,-1}`.  In a coefficient space with
basis `e_0,e_2,e_3,...`, set

\[
 u_n=e_0+\sum_{2\le q\le n}\epsilon_q
       \left(1-{L_q\over L_n}\right)e_q.             \tag{39.1}
\]

The entering coefficient at `q=n` is zero, exactly as for the complete Mobius
approximant.  Moreover

\[
 u_{n+1}-u_n=h_nD_n,
 \qquad D_n=\sum_{2\le q\le n}\epsilon_qL_qe_q.       \tag{39.2}
\]

Thus (39.1) preserves the exact reciprocal-log affine law, nested prefix,
zero-at-entry convention, and one-prefix update.  Only the numerical logarithm
table is rationalized.  A rational positive semidefinite matrix `G` defines a
Hilbert seminorm by `P_n=u_n^TGu_n`.  The proposed block inequality at
`kappa=1/2` is

\[
 P_a-P_b\ \ge\ \sum_{a\le n<b}w_nP_n.                \tag{39.3}
\]

## 2. Smallest strict counterexample

Take `L_2=1`, `L_3=2`, `epsilon_2=mu(2)=-1`.  Then

\[
 u_2=(1,0),\qquad u_3=(1,-1/2),\qquad h_2=w_2=1/2.
\]

With the rational positive definite Gram matrix

\[
 G=\begin{pmatrix}1&1/2\\1/2&1\end{pmatrix}
 \quad(\det G=3/4),
\]

one obtains

\[
 P_2=1,\qquad P_3=3/4,
\]

and hence

\[
 P_2-P_3={1\over4}
 <{1\over2}=w_2P_2.                                  \tag{39.4}
\]

The norm genuinely decreases, so this is not merely an outward-step example.
It obeys the exact coefficient update `u_3-u_2=h_2(-e_2)` and has a strictly
positive Gram matrix.

There is also an exact threshold family.  Replacing the off-diagonal `1/2` by
`r` while keeping both diagonal entries equal to one gives

\[
 P_2-P_3=r-{1\over4},\qquad w_2P_2={1\over2}.
\]

The matrix is positive definite for `|r|<1`.  Therefore `r=3/4` gives equality
at `kappa=1/2`, every `1/4<r<3/4` gives a decreasing strict counterexample,
and every `3/4<r<1` gives strict success.  Positivity and the update law do not
distinguish the three cases, so the constant `1/2` cannot be selected by those
axioms.

## 3. Nested two-step counterexample with positive covariance

The one-step example has no scale covariance.  To retain that feature, take

\[
 (L_2,L_3,L_4)=(1,2,3),\qquad
 (\epsilon_2,\epsilon_3,\epsilon_4)=(-1,-1,0),
\]

which is the actual Mobius sign/zero pattern through four.  In coordinates
`(e_0,e_2,e_3)`,

\[
 u_2=(1,0,0),\quad
 u_3=(1,-1/2,0),\quad
 u_4=(1,-2/3,-1/3),                                  \tag{39.5}
\]

and

\[
 h_2={1\over2},\quad h_3={1\over6},\qquad
 w_2={1\over2},\quad w_3={1\over3}.
\]

Use

\[
 G=vv^T+{1\over36}I_3,
 \qquad v=(1,1/2,0),                                  \tag{39.6}
\]

or explicitly

\[
 G=\begin{pmatrix}
 37/36&1/2&0\\
 1/2&5/18&0\\
 0&0&1/36
 \end{pmatrix}.
\]

This is positive definite.  It has an entirely rational Euclidean
realization: map the three coefficient basis vectors respectively to

\[
 (1,1/6,0,0),\qquad(1/2,0,1/6,0),\qquad(0,0,0,1/6)
 \quad\hbox{in }\mathbb R^4.                           \tag{39.7}
\]

Direct calculation gives

\[
 P_2={37\over36},\qquad P_3={43\over72},\qquad
 P_4={79\over162}.                                    \tag{39.8}
\]

Both steps are inward:

\[
 P_2-P_3={31\over72}>0,\qquad
 P_3-P_4={71\over648}>0.                              \tag{39.9}
\]

Nevertheless the complete two-step block fails at `kappa=1/2`:

\[
 P_2-P_4={175\over324}
 <{77\over108}
 ={1\over2}P_2+{1\over3}P_3,                          \tag{39.10}
\]

with exact surplus `-14/81`.

This failure survives the positive mean/covariance completion.  If `F_n` is
the realization (39.7) of `u_n`, then `W=w_2+w_3=5/6` and

\[
 \sum_{n=2}^3w_n\|F_n\|^2
 =W\|\overline F\|^2+
   \sum_{n=2}^3w_n\|F_n-\overline F\|^2
 ={151\over216}+{1\over72}={77\over108}.              \tag{39.11}
\]

The covariance square is strictly positive, not discarded.  Gram positivity,
same-scale products, and the exact covariance identity therefore remain
compatible with failure.

## 4. What arithmetic is still absent

These examples already impose all of the following:

1. the affine reciprocal-log coefficient formula;
2. zero coefficient on entry and nested prefix updates;
3. the genuine values `mu(2)=mu(3)=-1`, `mu(4)=0`;
4. a rational positive definite physical Gram matrix;
5. decreasing endpoint energy at every displayed step; and
6. the undropped positive coefficient-covariance square.

Consequently, neither the Mobius signs nor abstract Gram positivity is the
missing ingredient.  At least one hypothesis must couple those signs to the
*specific* physical vectors `phi_q(t)={t/q}`.  Equivalently, it must use the
actual Mobius-weighted fractional-part correlations

\[
 \sum_{q,r}\mu(q)\mu(r)(\cdots)G^{\rm Vas}_{q,r},
\]

including their off-diagonal Vasyunin/cotangent content, or prove a scalar
consequence of that coupling such as the compensated radial alignment

\[
 -\langle F_n,D_n\rangle-{h_n\over2}\|D_n\|^2
\]

on complete blocks.  This is the minimum Mobius-specific ingredient in the
logical sense: a condition that excludes arbitrary positive Gram realizations
while retaining the fixed fractional-part Gram realization.  Merely adding
`mu(q)` to the coefficient path does not do so.

The examples do not disprove `kappa=1/2` for the actual Vasyunin Gram matrix.
They show precisely that `kappa=1/2` cannot follow from coefficient kinematics,
Mobius signs, and Gram/covariance positivity alone.
