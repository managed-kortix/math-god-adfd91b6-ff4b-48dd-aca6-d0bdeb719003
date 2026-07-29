# Cycle 115: exact obstruction to the proposed Fermat candidate

Da Silva's 2021 notes ask whether an explicit surface can project nontrivially
to every exceptional character space on a Fermat fourfold.  The answer is no
for that surface, for two independent exact reasons.

Let `m=3d`, `3` not divide `d`, and put `y_i=x_i^d`.  With `e_j` the elementary
symmetric polynomials in six variables, the proposed surface is

\[
 W_d=V(e_1(y),e_2(y),e_3(y))\subset\mathbf P^5.
\]

Newton's identity gives

\[
 \sum_i y_i^3=e_1^3-3e_1e_2+3e_3.
\]

Therefore, for the Fermat fourfold
`X_(3d)=V(sum x_i^(3d))`, the homogeneous ideals satisfy exactly

\[
 (e_1(y),e_2(y),e_3(y))
 =(e_1(y),e_2(y),\sum_i x_i^{3d}).
\]

Thus `W_d` is scheme-theoretically the intersection on `X_(3d)` of the two
Cartier divisors `e_1(y)=0` and `e_2(y)=0`.  It is an ambient complete
intersection of type `(d,2d,3d)`, and

\[
 [W_d]=2d^2H^2\in CH^2(X_{3d}).
\]

Its primitive cohomological projection is consequently zero.  In particular,
for `d=11`,

\[
 [W_{11}]=242H^2,
\]

and its projection to every primitive Fermat character space vanishes.

There is also a character-theoretic proof.  Since the equations depend only on
the `x_i^11`, `W_11` is invariant under `(mu_11)^5`.  A nonzero character
projection must therefore have every coordinate divisible by `11`; among
primitive `(2,2)` characters, only permutations of

\[
 (11,11,11,22,22,22)
\]

can survive this necessary test.  Da Silva's exceptional degree-33 character

\[
 \alpha=(7,10,13,19,22,28)
\]

is nontrivial on that subgroup, so its projection vanishes immediately.
The character itself is valid: all twenty unit multiples have residue sum
`99`, it has no proper zero-sum coordinate subset, and its Jacobian monomial
has degree `93`.

This resolves the paper's proposed candidate question negatively; it does not
resolve the exceptional character's algebraicity or the Hodge conjecture.  The
published version has the correct Newton term `3e_3`; an arXiv version's
`3e_3^3` is a dimensionally impossible typo.  No external contact or
publication claim is made from this lane.

Reproduce the arithmetic checks with

```sh
python millennium-prize/hodge/verify_cycle115_fermat_obstruction.py
```
