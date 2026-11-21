# Cycle 43 divisor-admission multiprobe audit

## Scope and verdict

The exact compensated divisor-admission test at

\[
 \theta={1\over4\log a}
\]

has a **small-rank finite certificate** on each requested complete block.  In
the full family consisting of the affine column and all squarefree divisor
columns below the block endpoint, midpoint-greedy selection needs ranks
`1, 1, 2` on `[39,42)`, `[95,103)`, and `[219,231)`, respectively.  Even when
the affine column is forbidden, the respective families `{3}`, `{3}`, and
`{3,215}` certify the blocks.  Thus these finite tests do **not** demonstrate a
near-full-rank obstruction.

There is, however, a sharp negative result for a more local interpretation of
“admission.”  The columns first admitted *inside the current block* fail even
when all of them are used: ranks `2, 4, 8` have certified negative margins on
the three blocks.  The successful directions are an affine direction and/or
old divisor columns.  Consequently, the calculation does not yet isolate a
new-divisor-only arithmetic mechanism that could plausibly be iterated.

All underlying signs and values are certified by outward-rounded 192-bit Arb
balls serialized in `cycle43-divisor-admission-multiprobe-results.json`, using
the complete restricted Vasyunin Gram matrix.  The decimals in the Markdown
tables below are rounded centers, not interval enclosures.  There is no
unit-cell cutoff.  The greedy ordering uses ball midpoints and is a labeled
floating heuristic; every candidate and final verdict is evaluated by Arb
interval linear algebra.  Any nonfinite value, unresolved determinant, or
unresolved sign aborts.  This is a finite diagnostic, not an asymptotic theorem
and not an RH claim.

## 1. Exact compensated square

Let

\[
 L_n=\log n,\qquad w_n=1-{L_n\over L_{n+1}},\qquad
 \theta={1\over4L_a}.
\]

Retain

\[
 U_n=\chi+\sum_{d\le n}\mu(d)\rho_d,
 \qquad D_n=\sum_{d\le n}\mu(d)L_d\rho_d,
 \qquad E_n={D_n\over L_n}.
\]

Define

\[
 A_n=1+{L_n\over L_{n+1}}-2\theta,
 \qquad \eta_n={1-2\theta\over A_n},
 \qquad B_n=2\theta+{(1-2\theta)^2\over A_n},
\]

and `Z_n=E_n-eta_n U_n`.  The exact identity from the preceding analysis is

\[
 \boxed{
 \mathcal R_\theta(a,b)
 =P_a-P_b-2\theta\sum_{n=a}^{b-1}w_nP_n
 =\sum_{n=a}^{b-1}w_n
 \left(A_n\|Z_n\|^2-B_n\|U_n\|^2\right).}
 \tag{43.1}
\]

Put

\[
 X=(\sqrt{w_nA_n}Z_n)_{a\le n<b},
 \qquad N_\theta=\sum_{n=a}^{b-1}w_nB_n\|U_n\|^2.
 \tag{43.2}
\]

Then `R_theta=||X||^2-N_theta`.

## 2. Exact probe family

Label the affine probe by `0`.  Probe label `1` is the distinct divisor column
`rho_1`, not the affine probe; their scalar scale coefficients happen to agree
because `log(1)=0`, but their spatial vectors and Gram entries differ.  For
every squarefree `d<b`, define

\[
 p_0=(-\sqrt{w_nA_n}\,\eta_n\chi)_n,
 \tag{43.3}
\]

\[
 p_d=\left(
 \mathbf1_{d\le n}\sqrt{w_nA_n}\,\mu(d)
 \left({L_d\over L_n}-\eta_n\right)\rho_d
 \right)_n.
 \tag{43.4}
\]

These are exactly the affine and divisor summands of `X`; all Möbius signs and
all scale weights remain in place.  For a selected family `S`, set

\[
 G_{de}=\langle p_d,p_e\rangle,
 \qquad c_d=\langle X,p_d\rangle.
\]

The complete-Gram projection bound is

\[
 \boxed{
 \mathcal R_\theta(a,b)
 \ge c_S^TG_S^{-1}c_S-N_\theta.}
 \tag{43.5}
\]

For every selected family, its full Gram determinant is certified positive
before inversion.  Each exact matrix is a Hilbert Gram matrix and therefore
positive semidefinite a priori; positive determinant consequently makes it
positive definite.  An ordinary inverse then suffices, and no numerical
pseudoinverse is used.  No claim is made that every principal minor was tested.

The entries are finite sums of complete restricted Vasyunin products:

\[
 \langle\rho_d,\rho_e\rangle
 =G^\infty_{d,e}-{1\over de},
 \qquad
 \langle\chi,\rho_d\rangle={L_d+1-\gamma\over d}.
 \tag{43.6}
\]

Thus the complete Gram, including its off-diagonal cotangent content and the
rank-one restricted correction, is preserved.

## 3. Certified block data

The positive square, negative budget, and exact compensated residual are:

| block | `theta` | `||X||^2` | `N_theta` | exact `R_theta` |
|---|---:|---:|---:|---:|
| `[39,42)` | 0.06823960510234935 | 0.005241346957311129 | 0.001340284613147913 | 0.003901062344163216 |
| `[95,103)` | 0.05489827809379648 | 0.003523560164369878 | 0.001395455651217583 | 0.002128104513152295 |
| `[219,231)` | 0.04639017859361700 | 0.001828583000924642 | 0.000972520631435903 | 0.000856062369488739 |

These residuals were also checked by a separate endpoint-energy contraction
(sharing the same restricted Vasyunin Gram evaluator) against

\[
 P_a-P_b-2\theta\sum_{a\le n<b}w_nP_n
\]

using `complete_energies`.

### Smallest cardinalities found

| block | family including affine | projection | margin over `N_theta` | affine-free family | projection | margin |
|---|---|---:|---:|---|---:|---:|
| `[39,42)` | `{0}` | 0.004150860256058698 | +0.002810575642910785 | `{3}` | 0.003659140348449363 | +0.002318855735301450 |
| `[95,103)` | `{0}` | 0.002322151986546049 | +0.000926696335328465 | `{3}` | 0.002049344118560659 | +0.000653888467343076 |
| `[219,231)` | `{0,215}` | 0.001513616121508056 | +0.000541095490072153 | `{3,215}` | 0.001318003557951473 | +0.000345482926515570 |

A rank-zero family has projection zero and cannot certify any positive budget.
For the first two blocks, the displayed rank-one certificates are therefore
cardinality-minimal.  The exhaustive atomic scans find `14/28` and `7/64`
passing singletons respectively (including the affine probe), so the passing
rank-one direction is not unique.  On `[219,231)`, an exhaustive scan of all
143 singleton divisor columns plus the affine singleton finds `0/144` passing
rank-one families; rank two is minimal in this candidate pool.  The exhaustive
singleton result is finite and computational, not a structural theorem about
other probe classes.

For a deterministic, order-independent affine-free family, squarefree divisor
prefixes first pass at:

| block | least cutoff `D` | family `{d<=D: mu(d)!=0}` rank | certified margin |
|---|---:|---:|---:|
| `[39,42)` | 1 | 1 | +0.002293206793821191 |
| `[95,103)` | 1 | 1 | +0.000629206857779840 |
| `[219,231)` | 19 | 13 | +0.000009468555109502 |

The rank-13 prefix for the last block is not minimal by cardinality; it is a
simple deterministic prefix benchmark.

## 4. Local-admission obstruction

If “divisor admission” is restricted to divisors entering during the current
scale block, the full available family fails:

| block | all squarefree `d in [a,b)` | rank | projection | margin over `N_theta` |
|---|---|---:|---:|---:|
| `[39,42)` | `{39,41}` | 2 | 0.000657551536670902 | -0.000682733076477012 |
| `[95,103)` | `{95,97,101,102}` | 4 | 0.000109650248090063 | -0.001285805403127521 |
| `[219,231)` | `{219,221,222,223,226,227,229,230}` | 8 | 0.000180757113542042 | -0.000791763517893860 |

This is a genuine failure of the full local-admission-span **projection
certificate**; it is not a failure of the actual compensated residual, which
is positive on all three blocks.  Adding the affine direction changes the last
block sharply: `{0,227}` passes with margin `+0.000028078565171581`, while
`{0,229}` fails with margin `-0.000038912550272027`.  This edge is consistent
with triangular right-end support loss, but changing `d` also changes the
spatial Gram column `rho_d`, so the comparison does not isolate support length
as the cause.

The successful old divisor `215` in `{0,215}` lies just before the last block,
but for the first two blocks the affine direction already suffices.  Without
the affine probe, `{3,215}` passes the last block.  These successes show that
near-full rank is not needed when old columns are allowed, but they also expose
the weakness of the present finite certificate: very old low-divisor columns
or the affine column can encode a broad component of `X`, so a one- or
two-column projection is not yet an asymptotic arithmetic lemma.

## 5. Interpretation and limitations

1. **What is certified.**  The stated finite projection inequalities, complete
   Gram entries, selected-family Gram-determinant positivity, and margins are
   Arb-certified.
2. **What is floating.**  Greedy probe ordering uses `float(ball.mid())` only
   to choose among candidate gains.  No verdict uses that float: each candidate
   and the retained final margin already use Arb interval linear algebra.  The
   deterministic prefix results do not use greedy ordering.
3. **No cell truncation.**  The implementation never sums unit cells.  It uses
   the complete restricted Vasyunin formula directly, so there is no omitted
   `k`-tail.
4. **Smallest means within a declared pool.**  Cardinality minimality is within
   `{affine} union {squarefree d<b}`.  It says nothing about all conceivable
   linear combinations or asymptotic families.  Multiple rank-one families
   pass the first two blocks; no uniqueness is claimed.
5. **Affine tautology risk.**  The affine probe is a genuine summand of `X`, but
   its striking strength means a certificate using it alone may be geometric
   bookkeeping rather than a useful Möbius-specific estimate.  An asymptotic
   argument would still need a lower bound for its signed numerator.
6. **Old-column risk.**  The successful non-affine families use `d=3` and, on
   the last block, `d=215`.  They are not generated solely by admissions within
   the block.  Current-block admissions alone fail at full local rank.
7. **No extrapolation.**  Three positive finite blocks do not establish a
   uniform family, a stable margin, a stopping theorem, the killed-Hardy
   inequality, or any RH consequence.
8. **Normalization.**  This test is at the deliberately weakened
   `theta=1/(4 log a)`.  Its effective renewal mass is summable under
   polynomial stopping, as already audited; passing these blocks is not an RH
   proof mechanism by itself.

## 6. Reproduction

From `/workspace/research/millennium-prize/riemann-hypothesis`:

```text
uv run --with python-flint python -m unittest -v \
  test_cycle43_divisor_admission_multiprobe.py

uv run --with python-flint python \
  cycle43_divisor_admission_multiprobe.py \
  --bits 192 \
  --json cycle43-divisor-admission-multiprobe-results.json
```

The first command runs eleven tests, including a separate endpoint-energy
contraction that shares the Gram evaluator, direct column checks, fail-closed
nonfinite handling, one-shot-iterator handling, projection monotonicity,
exhaustive atomic
singleton scans, minimal-rank examples, full local-span failures,
deterministic prefixes, and the `[227,229]` support boundary.  The second
command emits the human-readable certificate summary and the machine-readable
Arb intervals.
