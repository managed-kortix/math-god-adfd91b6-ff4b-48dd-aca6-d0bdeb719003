# LaTeX exposition modules for the rank-six synthesis

## Scope

This note supplies LaTeX-ready analytic and finite-reduction modules.  The
statements about finite certificates are deliberately conditional on exact
certificate ownership.  The note makes no all-connected theorem claim, does
not promote an incomplete coverage gate, and does not alter project state.

The snippets use the following notation.  For a finite simple graph $H$, let
$A(H)$ have eigenvalues $\rho_1,\ldots,\rho_n$ and put

```latex
\[
 s^+(H)=\sum_{\rho_i>0}\rho_i^2,
 \qquad
 s^-(H)=\sum_{\rho_i<0}\rho_i^2.
\]
```

The cyclomatic rank of a connected graph is
$\beta(H)=|E(H)|-|V(H)|+1$.  A \emph{positive-rank cyclic block} means a block
$B$ with $\beta(B)>0$.  This terminology avoids the incorrect phrase
``one nontrivial block,'' since bridge copies of $K_2$ are nontrivial blocks in
the standard block convention.

## Module A: DNN bound and the meaning of a witness

```latex
\begin{definition}[The DNN parameter]
For a finite graph $H=(V,E)$, define
\[
 \kappa(H)=
 \min\left\{
   \sum_{uv\in E}\frac{2}{1-R_{uv}}:
   R\succeq0,\ R_{vv}=1\ (v\in V)
 \right\}.
\]
A summand is interpreted as $+\infty$ when $R_{uv}=1$.  Thus a
\emph{DNN witness of budget $b$} for $H$ is a correlation matrix $R$ for
which every edge denominator is positive and
\[
 \sum_{uv\in E(H)}\frac{2}{1-R_{uv}}\le b.
\]
\end{definition}

\begin{lemma}[What a DNN witness proves]\label{lem:dnn-witness-meaning}
For every finite simple graph $H$,
\[
 s^-(H)\le \kappa(H).
\]
Consequently, a DNN witness of budget $b$ proves
\[
 s^+(H)\ge 2|E(H)|-b.
\]
The witness need only be feasible; it need not minimize the defining
objective of $\kappa(H)$.
\end{lemma}

\begin{proof}
Write the adjacency matrix as $A=P-N$, where $P,N\succeq0$ are its positive
and negative spectral parts.  Put $M=N\circ N$.  By the Schur product theorem,
$M\succeq0$, and it is entrywise nonnegative.  Moreover,
\[
 \langle J,M\rangle=\operatorname{tr}N^2=s^-(H),
 \qquad
 \frac{s^-(H)}2=-\sum_{uv\in E(H)}N_{uv}
 \le\sum_{uv\in E(H)}\sqrt{M_{uv}}.
\]
Let $R$ be any correlation matrix having finite objective.  Since both $R$ and
$M$ are positive semidefinite, $\langle R,M\rangle\ge0$; also
$1-R_{uv}\ge0$.  Hence
\[
 \begin{aligned}
 \langle J,M\rangle
 &-2\sum_{uv\in E(H)}(1-R_{uv})M_{uv}\\
 &=\langle R,M\rangle
   +2\sum_{\substack{u<v\\uv\notin E(H)}}(1-R_{uv})M_{uv}\ge0.
 \end{aligned}
\]
Weighted Cauchy--Schwarz now gives
\[
 4\left(\sum_{uv\in E(H)}\sqrt{M_{uv}}\right)^2
 \le \langle J,M\rangle
       \sum_{uv\in E(H)}\frac{2}{1-R_{uv}}.
\]
If $s^-(H)>0$, the preceding two displays allow cancellation of $s^-(H)$ and
give
\[
 s^-(H)\le\sum_{uv\in E(H)}\frac{2}{1-R_{uv}}.
\]
The assertion is immediate when $s^-(H)=0$ or the objective is infinite.
Minimizing over $R$ proves $s^-(H)\le\kappa(H)$.

Since $H$ is simple,
\[
 s^+(H)+s^-(H)=\operatorname{tr}A(H)^2=2|E(H)|.
\]
If $R$ is a feasible correlation matrix of objective at most $b$, then
$\kappa(H)\le b$, and hence
\[
 s^+(H)=2|E(H)|-s^-(H)
       \ge 2|E(H)|-\kappa(H)
       \ge 2|E(H)|-b.
\]
\end{proof}

\begin{remark}[Exact Gram-chain certificates]
Suppose $R$ is represented by unit vectors $x_v$.  On a path
$v_0v_1\cdots v_\ell$, set $y_j=(-1)^j x_{v_j}$ and
$q_j=\langle y_{j-1},y_j\rangle$.  Then
\[
 \frac{2}{1-\langle x_{v_{j-1}},x_{v_j}\rangle}
 =\frac{2}{1+q_j}
 =1+\frac{1-q_j}{1+q_j}.
\]
It follows that a path-by-path Gram certificate satisfying
\[
 q_j>-1,
 \qquad
 \sum_{\text{all path steps }j}\frac{1-q_j}{1+q_j}\le 5
\]
is exactly a feasible witness for
$\kappa(H)\le |E(H)|+5$.  When all vector coordinates and inner products are
rational, the unit-norm identities, shared-endpoint identities, denominator
signs, positive semidefiniteness, and the final inequality can all be checked
with integer arithmetic after clearing positive denominators.  Decimal
optimizer output is not part of this proof.
\end{remark}
```

## Module B: finite reduction to rank-six kernels

```latex
\begin{lemma}[Suppression of a rank-six cyclic block]
\label{lem:rank-six-suppression}
Let $B$ be a finite simple $2$-connected graph with $\beta(B)=6$.  Suppress
every degree-two vertex: replace each maximal path whose internal vertices have
degree two by one edge.  The resulting object $K$ is a loopless
$2$-connected multigraph of minimum degree at least three.  Moreover,
\[
 \beta(K)=6,
 \qquad
 |E(K)|=|V(K)|+5,
 \qquad
 2\le |V(K)|\le10.
\]
Conversely, $B$ is recovered from $K$ by replacing its edges with positive
length, pairwise internally vertex-disjoint paths, subject to the requirement
that the resulting graph be simple.
\end{lemma}

\begin{proof}
Because $B$ is $2$-connected, every vertex has degree at least two.  The branch
vertices, namely those of degree different from two, therefore have degree at
least three.  They are nonempty: if every vertex had degree two, then $B$ would
be a cycle and would have cyclomatic rank one.

Suppressing one degree-two vertex removes one vertex and one edge.  It
therefore preserves $|E|-|V|$, connectedness, and cyclomatic rank.  Iterating
gives $\beta(K)=6$ and hence
\[
 |E(K)|=|V(K)|+5.
\]
Suppression cannot create a loop.  Indeed, such a loop would come from a cycle
in $B$ meeting the rest of $B$ in a single branch vertex.  That vertex would be
a cut vertex unless the cycle were all of $B$, and the latter alternative has
rank one.  Suppression also preserves the absence of a cut vertex: expanding
each kernel edge into a path does not join two components of $K-v$ that were
previously separate.  Thus $K$ is loopless and $2$-connected, with parallel
edges permitted.

Write $k=|V(K)|$.  Since every vertex of $K$ has degree at least three,
\[
 3k\le\sum_{v\in V(K)}d_K(v)=2|E(K)|=2k+10,
\]
so $k\le10$.  A loopless $2$-connected multigraph has at least two vertices,
which gives $k\ge2$.  The final assertion merely reverses the suppression
operation.  Distinct replacement paths have disjoint interiors and meet only
at their prescribed endpoints.  Simplicity is an additional condition because
parallel kernel edges cannot both be realized by unit paths.
\end{proof}

\begin{proposition}[Finite kernel census: computational statement]
\label{prop:rank-six-kernel-census}
Up to multigraph isomorphism, the loopless $2$-connected multigraphs $K$ with
\[
 \delta(K)\ge3,
 \qquad
 |E(K)|=|V(K)|+5
\]
have the following order distribution:
\[
\begin{array}{c|rrrrrrrrr}
 |V(K)|&2&3&4&5&6&7&8&9&10\\ \hline
 \#K&1&4&26&84&216&314&325&162&66.
\end{array}
\]
In particular, the census contains $1198$ isomorphism classes.
\end{proposition}

\begin{proof}[Computer-assisted proof]
For each order $k\in\{2,\ldots,10\}$, encode a loopless multigraph by the
upper-triangular multiplicity vector
$(m_{ij})_{1\le i<j\le k}$.  The finite universe to be traversed consists of
the nonnegative integer solutions of
\[
 \sum_{i<j}m_{ij}=k+5,
 \qquad
 \sum_{j\ne i}m_{ij}\ge3\quad(1\le i\le k).
\]
The implementation traverses this universe by degree partitions and exact
residual-degree recursion.  For orders eight and nine it fixes one vertex
inside its degree class and enumerates its multiplicity row up to permutations
of equal-degree vertices before completing all residual rows.  At order ten,
the degree equations force cubicity; the implementation uses inverse
two-edge-expansion generation from the exhaustively generated order-eight
cubic bases.  The source displays all three expansion cases:
expansion on two distinct edges, on two copies of one parallel edge, and twice
on one simple edge.  Completeness here uses the inverse-expansion fact that a
loopless $2$-connected cubic multigraph on ten vertices has a pair of adjacent
vertices whose deletion and degree-two suppression produces a loopless
$2$-connected cubic multigraph on eight vertices; reversing that reduction is
exactly one of the three displayed cases.  This finite graph lemma is therefore
part of the census argument and must be retained with the specialized
order-ten generator.  Subject to it, the optimized generators are symmetry
reductions of the displayed finite integer universe, rather than probabilistic
searches or bounded heuristic scans.

The verifier rejects a vector whenever deletion of some vertex disconnects the
remaining support.  Every surviving vector is put into a canonical isomorphism
form by exact individualization and partition refinement, and duplicate
canonical forms are removed.

The resulting sorted list is compared entry-for-entry with the canonical
fixture, not merely by comparing totals.  The verifier also checks every
fixture row independently for the edge count, minimum degree, absence of a cut
vertex, and canonical form; regenerates the displayed order counts and the
degree-multiset ledger; and rejects test fixtures with a deleted row, duplicated
row, changed multiplicity, changed policy field, reordered row, extra field, or
noncanonical JSON encoding.  Thus the mathematical trust placed in the
calculation is limited to the stated finite enumeration algorithm (including
the order-ten inverse-expansion lemma), exact integer arithmetic,
canonical-label implementation, JSON parser, Python runtime, and hardware.  No
floating-point computation and no spectral calculation enters this census.
\end{proof}
```

The proposition is reproducible from the repository root with

```text
python3 research/rank-six-kernel-census-verifier.py
```

The source is `research/rank-six-kernel-census-verifier.py`; the canonical data
are in `research/fixtures/rank-six-kernels.json`.  A digest identifies the exact
bytes audited, but the proof obligation is the verifier's regeneration and
entrywise comparison, not the digest alone.

## Module C: canonical simple lengths

```latex
\begin{definition}[Physical parity row and canonical length vector]
Let $K$ be a loopless multigraph with physical edges
$e_1,\ldots,e_p$.  A subdivision length vector is
$\ell=(\ell_1,\ldots,\ell_p)\in\mathbb Z_{>0}^p$.  For every unordered endpoint
pair $\{u,v\}$, its parallel class consists of the physical edges joining
$u$ and $v$.  Its physical parity datum is the number $o$ of odd lengths in
that class.

For a parallel class of multiplicity $m$ and odd count $o$, define its
canonical simple length multiset by
\[
 c(m,o)=
 \begin{cases}
  (2,\ldots,2),&o=0,\\
  (1,\underbrace{3,\ldots,3}_{o-1},
     \underbrace{2,\ldots,2}_{m-o}),&o>0.
 \end{cases}
\]
Concatenating these classwise choices gives the canonical vector $c$ of the
physical parity row.
\end{definition}

\begin{lemma}[Canonical domination]
\label{lem:canonical-domination}
Let $\ell$ be a length vector whose subdivision of $K$ is simple, and let $c$
be the canonical vector for its physical parity row.  After permuting physical
edges inside each parallel class,
\[
 c_i\le\ell_i
 \quad\text{and}\quad
 \ell_i-c_i\in2\mathbb Z_{\ge0}
 \qquad(1\le i\le p).
\]
\end{lemma}

\begin{proof}
An even positive length is at least two.  An odd positive length is either one
or at least three.  In a parallel class, simplicity allows at most one path of
length one, since two such paths would give two edges with the same endpoints.
If a unit path occurs, match it to the canonical coordinate of length one; if
none occurs, match any odd path to that coordinate.  Match the remaining odd
paths to the canonical coordinates of length three and the even paths to those
of length two.  Every matched difference is nonnegative and even.  Repeating
this independently in every parallel class proves the assertion.
\end{proof}
```

## Module D: exact path elimination and arbitrary subdivisions

```latex
\begin{lemma}[Exact path cost and fixed-parity monotonicity]
\label{lem:fixed-parity-path}
Let a kernel edge with endpoint correlation $r\in[-1,1]$ be replaced by a path
of length $q\ge1$.  The least possible DNN contribution of that path, in
excess of its $q$ edges, is
\[
 f_q(r)=q\tan^2\!\left(
   \frac{\arccos((-1)^q r)}{2q}
 \right).
\]
For fixed $r$ and fixed parity,
\[
 f_{q+2}(r)\le f_q(r).
\]
The inequality is understood in the extended sense at endpoint values where a
denominator vanishes.
\end{lemma}

\begin{proof}
Represent the endpoint correlation by unit vectors and alternately negate the
vectors along the path.  The transformed endpoint angle is
$\beta=\arccos((-1)^q r)$.  If the successive transformed angles are
$\theta_1,\ldots,\theta_q$, the spherical triangle inequality gives
$\sum_j\theta_j\ge\beta$.  Convexity of
$\theta\mapsto\sec^2(\theta/2)$ shows that the minimum is attained by $q$
equal angles $\beta/q$.  Equally spaced planar vectors realize those angles.
The minimum path contribution is therefore
\[
 q\sec^2\!\left(\frac\beta{2q}\right)
 =q+f_q(r).
\]

For fixed parity, $\beta$ is unchanged when $q$ is replaced by $q+2$.  Regard
$q$ temporarily as a positive real variable and set $z=\beta/(2q)$.  Then
\[
 \frac{d}{dq}\left[q\tan^2\!\left(\frac\beta{2q}\right)\right]
 =\tan z\sec^2z\,\bigl(\sin z\cos z-2z\bigr)\le0,
\]
because $\sin z\cos z\le z<2z$ for $z>0$, with equality at $z=0$.
One-sided limits give the endpoint cases.
\end{proof}

\begin{lemma}[Canonical-plus-coordinate frontier]
\label{lem:canonical-coordinate-frontier}
Fix a physical parity row of a loopless kernel with $p$ physical edges and
canonical simple vector $c$.  Put
\[
 \mathcal F(c)=\{c\}\cup\{c+2\mathbf e_i:1\le i\le p\}.
\]
Assume that every member $a\in\mathcal F(c)$ has a feasible DNN witness for
its simple subdivision $B(a)$ satisfying
\[
 \kappa(B(a))\le |E(B(a))|+5.
\]
Then the same inequality holds for every simple subdivision $B(\ell)$ in this
physical parity row.
\end{lemma}

\begin{proof}
By Lemma~\ref{lem:canonical-domination}, after an allowed permutation of
physical edges within parallel classes, $c\le\ell$ coordinatewise and all
differences are even.  If $\ell=c$, use the witness at $c$.  Otherwise choose
$i$ with $\ell_i\ge c_i+2$.  Then
\[
 c+2\mathbf e_i\le\ell
\]
coordinatewise, again with even coordinate differences.

Use the witness belonging to $c+2\mathbf e_i$ and retain its Gram matrix on
the branch vertices.  On every path that must be lengthened, discard the old
internal path vectors and insert an equal-angle chain realizing the exact path
minimum.  Lemma~\ref{lem:fixed-parity-path} says that each replacement has
excess no larger than before.  The chains for different physical edges are
compatible: they share only their prescribed endpoint vectors, and their new
internal components may be placed in mutually orthogonal auxiliary subspaces.
Thus the total excess remains at most five, which is precisely
$\kappa(B(\ell))\le|E(B(\ell))|+5$.
\end{proof}

\begin{remark}
The lemma covers simultaneous lengthening in arbitrarily many coordinates; it
does not assert monotonicity under a one-edge subdivision, which changes
parity.  A canonical witness alone is sufficient only when one fixed branch
Gram is already known to remain within budget under every same-parity
lengthening.  For a residual row whose canonical optimum may equal five, the
canonical target by itself does not justify the descendants: every coordinate
frontier must have an exact owner, or a separate exact extension rule must
replace it.
\end{remark}
```

## Module E: rooted-tree lift and spectral conclusion

```latex
\begin{lemma}[One-vertex additivity and trees]
\label{lem:kappa-one-vertex}
If $H=H_1\vee H_2$ is a one-vertex sum, then
\[
 \kappa(H)=\kappa(H_1)+\kappa(H_2).
\]
In particular, every finite tree $T$ satisfies
$\kappa(T)=|E(T)|$.
\end{lemma}

\begin{proof}
Restricting a feasible correlation matrix of $H$ to the two summands shows
$\kappa(H)\ge\kappa(H_1)+\kappa(H_2)$.  Conversely, choose minimizing Gram
representations of the summands and identify the two unit vectors belonging to
the common vertex.  After an orthogonal change of coordinates, place the
components perpendicular to this common vector in mutually orthogonal
subspaces.  The resulting Gram matrix is feasible for $H$, and its edge
objective is the sum of the two objectives.  This proves the reverse
inequality.

For a tree, every edge summand is at least one because
$R_{uv}\ge-1$.  Assign one unit vector to one bipartition class and its negative
to the other; then every edge has correlation $-1$ and contributes one.
\end{proof}

\begin{lemma}[Rooted-tree lift for a rank-six core]
\label{lem:rank-six-tree-lift}
Let $B$ be a finite simple connected graph of cyclomatic rank six with
$L=|E(B)|$, and suppose
\[
 \kappa(B)\le L+5.
\]
Form $G$ by attaching finite rooted trees at arbitrary vertices of $B$, each
tree meeting the graph already constructed only in its root.  Roots may be
branch vertices or internal subdivision vertices.  Then
\[
 s^+(G)\ge |V(G)|.
\]
\end{lemma}

\begin{proof}
Let $t$ be the total number of tree edges.  Cyclomatic rank six gives
\[
 |V(B)|=L-5.
\]
Repeated application of Lemma~\ref{lem:kappa-one-vertex} gives
\[
 \kappa(G)=\kappa(B)+t\le L+5+t.
\]
Also $|E(G)|=L+t$ and $|V(G)|=L-5+t$.
Lemma~\ref{lem:dnn-witness-meaning} and the adjacency trace identity now give
\[
 \begin{aligned}
 s^+(G)
 &\ge 2|E(G)|-\kappa(G)\\
 &\ge 2(L+t)-(L+5+t)\\
 &=L-5+t=|V(G)|.
 \end{aligned}
\]
The proof uses the one-vertex-sum identity at the actual root, so the degree or
position of that root in $B$ is irrelevant.  No tree is contracted or moved.
\end{proof}
```

A connector that meets the core in two vertices is not a rooted-tree
attachment and is not covered by this lemma.

## Module F: block-rank partition and proof interfaces

```latex
\begin{lemma}[Additivity of cyclomatic rank over cyclic blocks]
\label{lem:block-rank-additivity}
Let $G$ be a finite connected graph, and let $\mathcal B_+(G)$ be its set of
blocks having positive cyclomatic rank.  Then
\[
 \beta(G)=\sum_{B\in\mathcal B_+(G)}\beta(B).
\]
\end{lemma}

\begin{proof}
Build $G$ by following its block--cut tree.  Adding a block $B$ at its unique
previously present cut vertex adds $|V(B)|-1$ vertices and $|E(B)|$ edges, so it
changes $|E|-|V|+1$ by
\[
 |E(B)|-(|V(B)|-1)=\beta(B).
\]
A bridge block is a copy of $K_2$ and contributes zero.  Induction over the
block--cut tree proves the formula.
\end{proof}

\begin{corollary}[Rank-six block partition]
\label{cor:rank-six-partition}
If $G$ is connected and $\beta(G)=6$, the multiset of positive cyclic-block
ranks is exactly one of
\[
\begin{gathered}
 1+1+1+1+1+1,\quad 2+1+1+1+1,\quad 2+2+1+1,\quad 2+2+2,\\
 3+1+1+1,\quad 3+2+1,\quad 3+3,\quad 4+1+1,\\
 4+2,\quad 5+1,\quad 6.
\end{gathered}
\]
The first ten alternatives have at least two positive-rank cyclic blocks; the
last has a unique positive-rank cyclic block, of rank six.  These alternatives
are disjoint and exhaustive.
\end{corollary}

\begin{proof}
By Lemma~\ref{lem:block-rank-additivity}, the positive block ranks are positive
integers summing to six.  The displayed list is the elementary list of all
integer partitions of six.  A partition has one part if and only if it is the
partition $6$.
\end{proof}

\begin{proposition}[Conditional single-block finite interface]
\label{prop:conditional-rank-six-interface}
Assume the following finite premise: for every kernel in
Proposition~\ref{prop:rank-six-kernel-census}, every physical parity orbit is
owned either by
\begin{enumerate}
 \item one exact coarse certificate whose branch Gram stays within excess five
 under all same-parity coordinate lengthenings; or
 \item exact certificates of excess at most five for the canonical vector and
 every one-coordinate frontier in
 $\mathcal F(c)=\{c\}\cup\{c+2\mathbf e_i\}$.
\end{enumerate}
Assume also that the owner ledger is an exact disjoint cover of the regenerated
target-key set.  Then every finite simple realization of a rank-six kernel,
with arbitrary positive subdivision lengths and arbitrary genuine rooted-tree
attachments, satisfies $s^+(G)\ge|V(G)|$.
\end{proposition}

\begin{proof}
Lemma~\ref{lem:canonical-coordinate-frontier} promotes every residual finite
frontier to all simple subdivisions in its parity orbit; the defining property
of a coarse owner gives the same conclusion for a coarse-owned orbit.  Hence
every subdivided core $B$ has
$\kappa(B)\le|E(B)|+5$.  Lemma~\ref{lem:rank-six-tree-lift} supplies the stated
conclusion after rooted trees are attached.
\end{proof}
```

The block corollary supplies only the exhaustive structural split.  It does not
itself prove either branch.  The first ten partitions require the separate
multiblock owner theorem.  The partition $6$ uses the conditional finite
interface only after exact owner coverage is established.  In particular:

1. A search completion flag, process exit code, target total, or chunk digest
   does not establish the finite premise.
2. The verifier must regenerate the expected keys and prove set equality with
   the disjoint union of mathematically checked owner keys.
3. A rational owner proves feasibility and an upper bound; it need not prove
   optimality.  A symbolic equality owner must separately prove both its lower
   bound and exact attainment.
4. Numerical optimization may discover certificates, but theorem verification
   reads only exact rational or exact symbolic data.
5. Kernel suppression, the all-length implication, the rooted-tree lift, and
   block-rank additivity are analytic arguments in the manuscript; a program
   manifest may record their scope but does not execute or replace them.

## Integration checklist

When these modules are moved into a paper, preserve the following hypotheses
verbatim or equivalently:

- all graphs receiving the trace calculation are finite and simple;
- kernel replacement paths have positive integral lengths, disjoint interiors,
  and only their prescribed common endpoints;
- monotonicity changes path lengths by two and never asserts one-subdivision
  monotonicity of $s^+$;
- every residual canonical and coordinate target has an exact owner;
- tree attachments meet the existing graph at exactly one root;
- the single-block phrase is ``unique positive-rank cyclic block,'' not
  ``exactly one nontrivial block'';
- the finite single-block interface and the multiblock interface remain
  separate until both have complete proof owners.
