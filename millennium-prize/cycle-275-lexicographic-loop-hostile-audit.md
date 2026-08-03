# Cycle 275: hostile audit of lexicographic selection and inactive packet loops

## Verdict

The established tuple

\[
L=(\text{barrier crossing},\text{non-equivalence},
   \text{finite falsifiability},\text{official transfer})
\]

is useful as a milestone ledger, but it is not a valid policy for choosing the
next action. Used lexicographically, it gives infinite exchange rates between
coordinates, ignores action cost and the probability of obtaining a useful
outcome, and does not distinguish a live target from retained infrastructure.

Cycles 274--276 exhibit the resulting failure mode. Navier--Stokes retains
`(1,1,0,1)` because `ND251` is sufficient and has an official transfer, but the
C265 route is inactive and its stop rule forbids turning the missing datum into
a campaign. Its score is unchanged by that inactivity. Lower-scoring lanes
with bounded actions therefore cannot be selected by the tuple. Cycle 274
responds by selecting a lane-neutral one-packet admission wrapper. The sole
Cycle 275 packet returns `WALL` at its missing official implication, again
without changing the Navier score. Cycle 276 correctly forbids another intake,
but the unchanged ordering then generates a new Navier conjecture and selects a
one-split audit because promoting a lower lane is declared impermissible. This
removes the literal packet-intake loop, not the stale-score selection bias.
Reapplying the old policy can still alternate between an inactive leading lane
and freshly named discovery gates without comparing their expected return to
live bounded actions elsewhere.

Formally, let `s` contain the six milestone tuples and stop rules, and let the
policy first choose `argmax_i L_i`. If the maximizing lane has no admissible
action, let it choose a packet-intake wrapper. A terminal intake result that
does not alter any `L_i`, stop rule, or supplied candidate returns a state
equivalent to `s` for selection purposes. The policy therefore has a self-loop.
The repository does not prove that execution will continue forever, but the
selection rule supplies no decreasing potential that prevents it.

This is also why the repeated selection of `ND251` in Cycles 237, 242, 251,
257, 270, and 274 should not be read as six independent pieces of evidence that
Navier--Stokes had the best next action. Much of that persistence comes from a
retained first and fourth coordinate. The tuple records ambition and transfer;
it does not price the next experiment.

## Replacement: bounded value-of-information selection

Keep `L` as an audit ledger, but choose among concrete actions rather than lane
names. At cycle `t`, an action `a` is eligible only if it already has:

1. one exact target and a stated implication or information gain;
2. fixed terminal outputs, a resource cap `c_a>0`, and a first-failure stop;
3. all inputs needed to execute the action without searching for a missing
   datum, bridge, representative, or packet; and
4. a novelty check showing that the action is not a stopped route with changed
   labels.

An inactive theorem target is not an action. A packet-intake wrapper with no
new independently supplied packet is likewise not an action.

For each eligible action, put a bounded utility on terminal outcomes:

\[
U(o)=W_{\rm sol}{\bf1}_{\rm official\ solution}
 +W_{\rm off}q(o)+W_{\rm sep}s(o)+W_{\rm thm}h(o)+W_{\rm info}i(o).
\]

Here `q` is the fraction of an explicitly named official quantifier closed,
`s` records a new separated transfer or barrier crossing, `h` records a
reusable nontrivial theorem, and `i` records a decisive exact obstruction or
retirement. All terms lie in `[0,1]`. Freeze finite weights with

\[
W_{\rm sol}\gg W_{\rm off}>W_{\rm sep}>W_{\rm thm}>W_{\rm info}>0,
\]

but do not use infinite lexicographic weights. A very small speculative chance
of touching a high coordinate must not automatically dominate a near-certain
bounded theorem or decisive no-go. The large finite `W_sol` preserves the
program's ambition while permitting cost-sensitive comparison.

Given the current evidence `D_t`, select the action maximizing the finite-horizon
upper-confidence value-of-information rate

\[
I_t(a)=\frac{\mathbb E[U(O_a)-U(s)\mid D_t]
 +\beta_t\sqrt{\operatorname {Var}(U(O_a)\mid D_t)}}{c_a}.
\tag{275.1}
\]

The expectation and variance must be printed as intervals with their evidence;
unsupported point probabilities are forbidden. The second term is deliberate
exploration: an uncertain action can outrank a familiar one, but only within a
declared budget. Choose the largest lower endpoint when it is positive. If all
lower endpoints are nonpositive, choose the largest upper endpoint for one
bounded information-gathering action. If every upper endpoint is nonpositive,
stop main-funnel execution and wait for genuinely new input rather than
manufacturing another admission cycle.

Equation (275.1) is a one-step Bayesian value-of-information objective with an
optimism bonus. It has the property missing from lexicographic selection:
an action with no possible state change has zero numerator, while positive cost
makes its index nonpositive. Exact probabilities are not presumed; interval
dominance is sufficient for many comparisons in the present portfolio.

## Stop discipline

- Freeze outcome utilities, probability intervals, cost, and the terminal gate
  before execution. Do not rescore after seeing a favorable intermediate
  result.
- Close an action after any terminal output. Reopening it requires a new lemma
  that changes an input or an outcome bound, not a new cycle number.
- Treat `WALL`, `REJECT`, and `NO-INPUT` as observations. A repeated action
  with the same inputs then has zero information gain and is ineligible.
- Permit at most one bounded discovery action after a lane has no executable
  packet. On failure, cool that lane until an independently supplied object
  changes its state.
- Preserve every route-specific prohibition. Exploration changes which live
  action is selected; it does not authorize datum search, cutoff escalation,
  nearby-family substitution, or retries.
- Recompute (275.1) after every terminal result. Do not carry forward an old
  action index merely because its lane retains a high milestone tuple.

These rules give a decreasing finite budget for every attempted action and
remove deterministic self-loops. They do not promise progress on an open
problem; they ensure that failure consumes a declared option rather than
silently recreating it.

## Current expected-value recommendation

The present portfolio can be ordered without invented point probabilities.
Hodge and RH have no eligible packet: each is missing an input that its stop
rule forbids the program to generate automatically. The sole P-versus-NP intake
is closed at an official-transfer wall, and its finite four-input census has
zero official value until that wall is repaired. The Yang--Mills retained
theorem is off the continuum trajectory and its two frozen contraction
mechanisms are closed.

Cycle 276 does provide one executable Navier action,
`C276-CEB-ONE-SPLIT`. Its conjecture has maximal ambition: together with the
exact critical-`L^3` identity it gives the official periodic alternative. But
the proposed experiment starts only from that identity, the pressure equation,
one amplitude split, and standard inequalities. The conjectured `7/8` budget
is already a uniform first-excursion critical-norm bound; the identity merely
rewrites the desired factor-two estimate as integrated pressure work minus
dissipation. No independent scale-sensitive estimate is supplied. The likely
terminal information is therefore the location of an unchargeable pressure
term, not a separated theorem, and the upside remains unsupported by a known
mechanism. It is a valid bounded scout, but not the highest value-of-information
action merely because Navier retains the largest tuple.

Select the **BSD source-only determinant-line applicability audit
`B264-DL-AUDIT`** as one bounded exploration action. This action was specified
in Cycle 264 but has no recorded terminal result. It requires no new curve,
field, primary computation, or conjectural datum. Its cost is source review,
and either allowed output changes the state: a source-backed implication would
identify a genuine class-level leading-term bridge, while an exact
hypothesis/equivalence wall would retire the last unexecuted BSD bridge audit.
That positive information value at low bounded cost dominates the inactive
`ND251` production target, the already-walled four-input P-versus-NP packet,
and, on current evidence, the one-split Navier audit's unsupported chance of a
separated bound. Keep `C276-CEB-ONE-SPLIT` frozen but unselected; choosing BSD
does not retire it or relax any Navier stop.

Freeze the action as follows: name one published rank-one
modular-elliptic-curve determinant-line or leading-term theorem and one
explicit nontrivial class; check every hypothesis and normalization from the
primary source; return exactly `B264-DL-IMPLIES` with the precise unconditional
class-level implication, or `B264-DL-WALL` with the first conjectural,
equivalent, or mismatched hypothesis. Stop after that theorem/class pair. Do
not reopen `43a1`, substitute another isolated curve, or infer a general BSD
claim from a class-level result.

This is an expected-value recommendation for the next bounded action, not a
claim that BSD is globally more tractable than Navier--Stokes and not a
Millennium result.
