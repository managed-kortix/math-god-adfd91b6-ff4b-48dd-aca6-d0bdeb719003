# Cycle 206: strategic rotation after the frozen Navier architecture

## Decision

Rotate the main funnel from Navier--Stokes to P versus NP, but only to the
selector-free all-order INDEX-minor gate stated below.  Cycle 205 exactly
retires the pinned Cycle 177 seed, frozen first-completion support, terminal
policy, and quadratic-order tangency system: the corrected 514-equation ideal
is the unit ideal over `Q`.  It does not retire other finite Fourier supports,
approximate leakage control, infinite-mode mechanisms, or Navier--Stokes
itself.  No replacement Navier architecture is presently frozen tightly
enough to justify another main-funnel cycle.

## Exact selection criterion

For each scout assign the lexicographic leverage tuple

\[
  L=(B,N,F,R).
\]

Here each entry is binary.

1. `B=1` if success crosses the scout's named current barrier rather than
   measuring a finite shadow that the barrier already shows cannot transfer.
2. `N=1` if the successful statement is not, after standard reconstruction or
   spectral arguments, equivalent to the relevant Clay assertion or to the
   entire missing half of it.
3. `F=1` if the next frozen construction has an exact finite falsifier: a bad
   order, a failed identity, or a rational/interval certificate, rather than
   only failed numerical search.
4. `R=1` if a proved gate has a currently stated resource-preserving route to
   the official quantifiers.  This is a tie-breaker after separated production,
   not permission to promote an equivalent reformulation.

Maximize `L` lexicographically.  This criterion deliberately prefers a new,
non-equivalent theorem that crosses a certified obstruction over a target-level
restatement with greater nominal reach.

The three live scouts score as follows.

| scout | `B` | `N` | `F` | `R` | reason |
|---|---:|---:|---:|---:|---|
| P versus NP: selector-free all-order INDEX | 1 | 1 | 1 | 0 | it crosses the explicit bad-order/selector obstruction and gives exact OBDD hardness, but has no reverse transfer to unrestricted circuits or MMW search |
| Yang--Mills: finite physical block | 0 | 1 | 1 | 0 | a finite block is exactly computable, but contraction or a variational gap on it does not control escaping states in the full vacuum complement |
| RH: canonical endpoint exhaustion | 1 | 0 | 0 | 1 | locally uniform endpoint convergence for shifts tending to zero is, by de Branges reconstruction, the shifted Hermite--Biehler assertion and hence RH-equivalent |

Thus `(1,1,1,0)` wins.  The choice does not assert that P versus NP is easier
or that an OBDD theorem implies a circuit lower bound.

## Promoted gate

For infinitely many input lengths `m`, construct one explicit polynomial-time
Boolean function

\[
  f_m:\{0,1\}^m\longrightarrow\{0,1\}
\]

with no selector field among its inputs, and prove the following statement for
every variable order `pi`.  There are a cut of `pi`, a restriction `rho` of
variables away from the cut, and `r>=c m` live data coordinates on the prefix
side such that the prefix--suffix residual matrix of `f_m|rho` contains an
`INDEX_r` submatrix.  Concretely, after naming `2^r` prefix assignments by
`x in {0,1}^r`, there are suffix assignments `y_1,...,y_r` satisfying

\[
  f_m|\rho(x,y_j)=x_j\qquad(1\le j\le r).
\]

The choice of the cut, restriction, and column assignments may depend on
`pi`; the function may not receive their index as readable advice.  All live
data variables must occur before the cut and all variables varied by each
`y_j` after it.  This immediately gives `2^r` distinct residual functions and
therefore exact deterministic OBDD width at least `2^r` in every order.

The first construction should use one explicit polynomial-size incidence or
matching family with uniform rank/unrank algorithms.  Its finite checkpoint is
exact: enumerate or SAT-certify every order at the first nontrivial parameter,
record an INDEX witness for each order, or return one bad order and verify that
no permitted cut and restriction has the declared minor.  A bad order retires
that frozen incidence construction, not the all-order gate.

## Why the alternatives do not rotate in

The Yang--Mills finite-block scout remains useful for exact finite-lattice
calibration, but Cycle 174 and the escaping-state examples show that any fixed
trial block can contract while the full vacuum-complement norm is one.  The
needed uniform tail estimate must control all moving states; in the surviving
form, combining it with low-block contraction is already the uniform lattice
mass-gap estimate, with continuum tightness, nontriviality, and OS
reconstruction still separate.  Optimizing another finite block does not cross
that wall.

The RH endpoint scout has full official reach, but that is precisely why it is
not selected.  Positive canonical endpoint kernels converging locally
uniformly to the shifted-xi kernel, for shifts tending to zero, are equivalent
to the Hermite--Biehler condition.  Finite endpoint positivity does not supply
the uniform exhaustion error.  Without a new arithmetic Hamiltonian, the gate
is an exact formulation of RH rather than a separated production lemma.

Success at the promoted P-versus-NP gate proves an all-order deterministic
read-once oblivious branching-program lower bound only.  Promotion beyond it
requires a separate resource-preserving transfer to unrestricted computation
or to the exact relational `search-MCSP^SAT` hypothesis.  No such transfer is
assumed, and no Millennium result is claimed.
