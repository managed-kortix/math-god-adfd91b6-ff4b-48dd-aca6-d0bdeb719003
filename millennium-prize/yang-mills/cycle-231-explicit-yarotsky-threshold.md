# Cycle 231: bulk activity/KP candidate audit for square-lattice `SU(2)`

This note audits a proposed explicit specialization of Yarotsky's proof for the
untruncated square-lattice `SU(2)` rotor. It does not prove a numerical coupling
endpoint or a numerical spectral gap. The gauge normalization, finite support
cardinalities, and the conditional arithmetic following Yarotsky's Lemma 3 are
retained. The proposed polymer count fails because coincident `I` and `J` events
invalidate the event-count injection. Boundary insertions and the passage from
bulk convergence to a gap on the full Hilbert space also remain unquantified.

## 1. Verified gauge-model constants

Use the Casimir normalization

\[
 C_2(j)=j(j+1),\qquad c_{SU(2)}=C_2(1/2)=\frac34.       \tag{231.1}
\]

Group the two positively oriented links leaving a vertex into one tensor site.
For a plaquette based at `x`, the assigned-link cells are

\[
 A+x,\qquad A=\{0,e_1,e_2\}.                            \tag{231.2}
\]

Thus `Lambda_0=A`, with cardinality three. Every assigned-link cell lies in
exactly `r=3` translates, and there is one unoriented coordinate plaquette type
per square-lattice vertex, so `s=1`. With

\[
 h_x=\frac{4}{3}\sum_{e:\operatorname{cell}(e)\in A+x}C_e,
 \qquad \Phi_x=-\frac12\operatorname{Re}\operatorname{Tr}U_p,
\]

one has `sum_x h_x=4T`, local gap one, and `||Phi_x||<=1`. After removal of the
scalar magnetic term, the normalized perturbation is

\[
 \phi_x=4\lambda\Phi_x,\qquad \|\phi_x\|\le b:=4|\lambda|. \tag{231.3}
\]

No Peter--Weyl cutoff is used in this normalization.

## 2. Verified support geometry

Write `D=A-A` and `B=A+D`. Direct finite enumeration gives

\[
 |D|=7,\qquad |B|=12,                                    \tag{231.4}
\]

and

\[
 |B-B|=37,\quad |B-D|=|D-B|=27,\quad |D-D|=19.           \tag{231.5}
\]

For a software-independent check, the horizontal row lengths, in increasing
vertical coordinate, are

\[
 \begin{array}{c|c|c}
 \text{set}&\text{vertical coordinates}&\text{row lengths}\\ \hline
 B-B&-3,-2,-1,0,1,2,3&4,5,6,7,6,5,4\\
 B-D&-2,-1,0,1,2,3&4,5,6,5,4,3\\
 D-B&-3,-2,-1,0,1,2&3,4,5,6,5,4\\
 D-D&-2,-1,0,1,2&3,4,5,4,3.
 \end{array}                                               \tag{231.6}
\]

Each row is an integer interval, so the displayed sums prove (231.5).

In the proposed event representation, a `J` event has spatial support `D+x`,
an `I` event has spatial support `B+x`, and either occupies two adjacent time
layers. The support arithmetic therefore gives the candidate overlap-degree
bounds

\[
 \Delta_I\le3(37+27)-1=191,\qquad
 \Delta_J\le3(27+19)-1=137,                              \tag{231.7}
\]

and at most `2(12+7)=38` event labels through a prescribed space-time point.
These are finite support-cardinality statements; they do not by themselves
count polymers by support size.

## 3. Fatal event-count flaw

The earlier version asserted that a polymer of support cardinality `n` has at
most `n` events. Its proposed injection sent each event to its center and used
the claim that an `I` event and a `J` event cannot have the same center. That
claim is false: the expansion permits coincident `I` and `J` events. Their
supports and labels differ, but their centers can agree. Consequently the map
from events to support points is not injective, and the bound `m<=n` was not
proved.

For a fixed event count `m`, an ordered depth-first traversal still gives the
candidate estimate `191^(2(m-1))` for connected event sets containing a fixed
root. What fails is the conversion from this fixed-`m` estimate to a count at
fixed support cardinality `n`. In particular, the displayed chain

\[
 38\sum_{m=1}^{n}191^{2(m-1)}\le c^n,
 \qquad c=72962,                                          \tag{231.8}
\]

is unsupported. No replacement polymer constant is proved here. Therefore
`c=72962`, `q=12c=875544`, and all numerical smallness values built from them
are candidate bookkeeping only, not theorem constants.

Conditionally, if one independently proves that the number of polymers of
support size `n` through a point is at most `c^n`, and sets `q=12c` and
`eta=q^-1`, then the bulk Kotecky--Preiss sum obeys

\[
 \sum_{\chi':\,\supp\chi'\cap\supp\chi\ne\varnothing}
 |w(\chi')|e^{|\supp\chi'|}
 \le |\supp\chi|\sum_{n\ge1}(3c\eta)^n
 =\frac13|\supp\chi|.                                   \tag{231.9}
\]

This conditional inequality uses `e<3`. It does not repair the missing count.

## 4. Preserved conditional Lemma 3 arithmetic

Yarotsky's Lemma 3, specialized to `|Lambda_0|=3`, gives

\[
 |w(C)|\le
 \left(2\alpha e^{t_0(\beta/\alpha+27)}\right)^{N_I}
 \left(e^{-t_0}\right)^{N_J}.                            \tag{231.10}
\]

The generic support estimate used in that comparison is

\[
 |\supp C|\le54N_I+18N_J,                                \tag{231.11}
\]

from `|tilde Lambda_I|<=27|I|`, `|tilde J|<=9|J|`, and two
time layers. Given a valid polymer constant `c`, put `q=12c`, choose

\[
 t_0=18\log q,\qquad \alpha=\frac1{2q^{558}},\qquad
 \beta=b\le\alpha.                                       \tag{231.12}
\]

Then

\[
 e^{-t_0}=q^{-18}=\eta^{18},                              \tag{231.13}
\]

and

\[
 2\alpha e^{t_0(\beta/\alpha+27)}
 \le q^{-558}q^{18\cdot28}=q^{-54}=\eta^{54}.            \tag{231.14}
\]

Thus Lemma 3 would imply the desired bulk activity estimate once the missing
polymer count is supplied. The arithmetic identity `558=54+18(27+1)` is
correct, as is the normalization conversion `b=4|lambda|`. Substituting the
unsupported candidate value `q=875544` into these conditional formulas does
not prove that `1/(8*875544^558)` is an admissible coupling or gap endpoint.
That claim is retracted.

No alternative endpoint, including one obtained by replacing the generic
support constants with smaller geometric numbers, is asserted here.

## 5. Boundary and gap audit boundary

Even after repairing the bulk polymer count, a full explicit threshold theorem
would require constants not supplied by this note:

1. Boundary-insertion activities and their polymer counts must be controlled
   uniformly for the finite-volume boundary convention used in the theorem.
2. The time-spanning cluster tail must be quantified with a valid tilted KP
   estimate based on the repaired count.
3. Inserted-polymer expansions used for ground-state matrix elements and
   uniqueness must carry explicit constants.
4. The conversion from those estimates to a positive, volume-independent
   spectral gap on the ambient untruncated Hilbert space must be written with a
   numerical lower bound.
5. Restriction to the Gauss-invariant space is valid only after such an ambient
   gap is established; gauge normalization alone does not establish it.

Periodic bulk support arithmetic does not settle small-torus wraparound or
arbitrary open-boundary terms. Accordingly, Cycle 231 now records verified
normalization and support data plus conditional bulk activity/KP arithmetic.
The rigorous lattice conclusion remains the existential small-coupling theorem
described in Cycle 230, not a proved numerical endpoint.
