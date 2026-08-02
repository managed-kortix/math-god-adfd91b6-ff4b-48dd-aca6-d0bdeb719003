# Cycle 251: exact deck-collision filter for F242

## Scope and correction

Write the columns of one block as

\[
 L=(\ell_X\ \ell_Y\ \ell_Z):E^3\longrightarrow E^6.
\]

This note isolates collisions obtained by replacing one source point by one of
the three deck transforms `sigma_X p`, `sigma_Y p`, `sigma_Z p`. It gives an
exact combinatorial necessary and sufficient condition for avoiding this deck
mechanism. It is not a necessary and sufficient condition for injectivity of
`L phi` against arbitrary pairs of points.

The tempting stronger claim that one must retain two quotient coordinates is
false. Cycle 250's collision used the simultaneous fixed relation
`sigma_X(P)=sigma_Z(P)` and does not generalize to arbitrary `P`.

## Exact criterion

For `j in {X,Y,Z}`, the quotient coordinate `q_j` is invariant under
`sigma_j`. The other two coordinates are not invariant: their differentials
lie in the two nontrivial Klein characters and change sign under `sigma_j`.
More precisely, after choosing origins on the quotient elliptic curves (the
constants cancel in differences),

\[
 \phi(p)-\phi(\sigma_Xp)=(0,2q_Y(p),2q_Z(p)),
\]

and cyclically. Here the two displayed nonzero quotient components belong to
distinct Klein-character factors of `J(C)`, so no linear cancellation between
them is possible. Therefore
the `sigma_X` deck difference is identically killed by `L` if and only if
`ell_Y=ell_Z=0`; similarly for the other two involutions. Equivalently,

\[
 \boxed{L\phi=L\phi\sigma_j\text{ identically}
 \iff \operatorname{supp}(L)\subseteq\{j\}
 \iff E_{\{X,Y,Z\}\setminus\{j\}}^2\subseteq\ker L.}
 \tag{251.1}
\]

Consequently the purely support-theoretic condition for avoiding all three
identical deck collisions is

\[
 \boxed{|\operatorname{supp}(L)|\ge2.}
 \tag{251.2}
\]

This criterion is exact for the three deck involutions and depends only on
which columns vanish. It is strictly weaker than `rank(L)>=2`: for example,
three equal nonzero columns have full support and rank one, while avoiding
identical deck invariance. The existing dimension argument already rejects all
rank-one blocks, so (251.2) adds no rejection after the Cycle 243 block-rank
filter.

## Special fixed-locus collisions

Cycle 250 exhibits a different, pointwise mechanism. If `p` lies on the fixed
locus of `sigma_j sigma_k`, then projectively
`sigma_j(p)=sigma_k(p)=q`. At this pair, quotient coordinates `j` and `k`
agree, while the remaining coordinate need not. Hence

\[
 L\phi(p)=L\phi(q)\quad\Longleftrightarrow\quad \ell_m=0,
 \qquad \{j,k,m\}=\{X,Y,Z\},
 \tag{251.3}
\]

provided `p != q`. Every coordinate axis section of the Fermat quartic supplies
such points, and the non-invariant quotient map is unramified there, so its two
values differ. Thus avoidance of all these two-deck fixed-locus collisions is
exactly

\[
 \boxed{\ell_X\ne0,\quad\ell_Y\ne0,\quad\ell_Z\ne0.}
 \tag{251.4}
\]

In kernel language, no coordinate elliptic factor may lie in `ker L`. This is
the correct generalization of the Cycle 250 witness rejection. It is a cheap
necessary condition for one-factor injectivity, not a sufficient one: arbitrary
non-deck pairs still require the full difference-curve test.

## Finite enumeration up to row operations

For the norm-one box `B={0,1,-1,i,-i}`, a row is one of 125 vectors in `B^3`.
Left row operations preserve the `Q(i)`-row space, so all `5^18` matrices fall
into exactly 160 realizable row-space classes:

\[
\begin{array}{c|rrrr}
\operatorname{rank}&0&1&2&3\\ \hline
\text{classes}&1&31&127&1\\
\text{matrices}&1&484344&3990628320&3810706152960.
\end{array}
\]

Among them, 141 classes have all three columns nonzero (16 of rank one, 124 of
rank two, and the unique rank-three class). Exactly

\[
 (5^6-1)^3=3813964890624
\]

matrices pass (251.4), while

\[
 5^{18}-(5^6-1)^3=732375001
\]

are rejected by a zero column. All rank-two and rank-three matrices necessarily
have at least two nonzero columns, so the universal deck-invariance filter
(251.2) rejects only matrices already rejected by `rank(L)<2`. Condition
(251.4), however, removes three rank-two row-space classes (the coordinate
planes), accounting for 732375000 rank-two matrices; it should be applied
before expensive geometry.

For comparison, 113 row-space classes have rank two on every pair of columns,
accounting for 3811036078080 matrices. This stronger linear condition is not
licensed as a collision criterion: a rank-one restriction of two columns does
not by itself imply equality of the corresponding elliptic-valued functions.
It is printed only to prevent accidental promotion of a convenient rank test
to a geometric theorem.

Reproduce the exact Gaussian elimination, dynamic matrix counts, direct support
count, and optional 113 representatives with

```sh
python3 millennium-prize/hodge/verify_cycle251_f242_deck_collision_filter.py
python3 millennium-prize/hodge/verify_cycle251_f242_deck_collision_filter.py --representatives
```

## Outcome

The exact new prefilter for each block is: reject if any one of its three
columns is zero. Applied to a triple, this is necessary for G0 and independent
of the other source factors, because fixing those factors preserves a
one-factor collision. It rejects the Cycle 249 sparse witness immediately.

No support or kernel condition can be sufficient for one-factor injectivity:
matrices with the same kernel can have the same linear section of the full
difference surface, while incidence with non-deck differences is geometric,
not support-combinatorial. The finite F242 enumeration, total-rank and Weil
filters, full difference scheme, and deformation gates remain `INCOMPLETE`.
No Hodge result is claimed.
