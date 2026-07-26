# Cycle 42: finite H-band recovery and the exact minimal lemma

## Scope

Apply the Cycle 41 recovery mechanism to the certified complete-Gram values of

\[
 H_n=\|D_n\|^2-\log n\log(n+1)\|U_n\|^2,
 \qquad
 \beta_n={\log(1+1/n)\over\log n\log^2(n+1)}.
\]

The scan through `n=2047` has exactly the negative runs

\[
 \{2\},\ \{39,40\},\ \{95,96\},\ \{99,100\},\
 \{219,220,221,222\},\ \{226\}.
\]

Runs separated by a positive hole are merged when the first run is not paid
before the next one. This gives the four episodes

\[
 [2,3),\quad[39,41),\quad[95,101),\quad[219,227).
\]

All numerical signs below are certified Arb enclosures. They describe finite
data only and are not an eventual band theorem or an RH proof.

## Exact minimal recovery lemma

Let `beta_n>0`, let `I=[p,q)`, and suppose `H_n>=0` on the proposed payment
window `[q,r)`. Define the signed suffix debt

\[
 \boxed{D^*(p,q)=\max_{p\le a<q}
 \left(-\sum_{a\le n<q}\beta_nH_n\right)_+}                 \tag{42.1}
\]

and `G(q,t)=sum_(q<=n<t) beta_n H_n` for `q<=t<=r`.

**Lemma 42.1 (minimal common-window recovery).** One common `t` in `[q,r]` is a
recovery endpoint for every start `a in [p,q)` if and only if

\[
 \boxed{G(q,t)\ge D^*(p,q).}                              \tag{42.2}
\]

Indeed,

\[
 \sum_{a\le n<t}\beta_nH_n
 =\sum_{a\le n<q}\beta_nH_n+G(q,t),
\]

so (42.2) is sufficient for every `a`; choosing a maximizing suffix in (42.1)
shows necessity. The first common endpoint is the first `t` satisfying (42.2).
No smaller scalar debt functional can work uniformly for the fixed data in
`[p,q)`. Unlike the Cycle 41 bound `sum beta_n H_n^-`, (42.1) retains favorable
terms and is therefore exact for episodes containing positive holes.

For disjoint episodes with `r_j<=p_(j+1)`, Lemma 42.1 plus singleton stops at
nonnegative indices is exactly the local input needed by the consecutive
renewal argument. The genuinely asymptotic missing statement is that such
finite payment windows exist uniformly for all later episodes.

## Certified finite arithmetic

The debt witness, first negative-free payment endpoint, and physical weight
distortion are:

| episode `[p,q)` | debt witness | `D*` | first `t` | payment `G(q,t)` | margin | `beta_p/beta_(t-1)` |
|---|---:|---:|---:|---:|---:|---:|
| `[2,3)` | `2` | `0.216366985215169` | `6` | `0.220378445464762` | `0.004011460249593` | `13.7351923223` |
| `[39,41)` | `39` | `0.000109737807404514` | `42` | `0.000556076895740068` | `0.000446339088335554` | `1.09333796723` |
| `[95,101)` | `95` | `0.000174093700670493` | `103` | `0.000242063827486627` | `0.000067970126816134` | `1.12393208639` |
| `[219,227)` | `219` | `0.0000481049644960970` | `231` | `0.0000525813541458851` | `0.00000447638964978815` | `1.07892159066` |

Thus all observed post-initial episodes obey the uniform finite bounds

\[
 t-p\le12,\qquad t-q\le4,\qquad
 {\beta_p\over\beta_{t-1}}<1.124.                         \tag{42.3}
\]

The exceptional initial episode has `t-p=4`, `t-q=3`, but its small-index
weight distortion is `13.736`. This finite exception is irrelevant to a tail
theorem. The endpoint `231`, rather than `232`, for the last merged episode is
important: positive values at `223,224,225` reduce its exact signed suffix debt
before the final negative value at `226`.

The endpoint ratio is explicit without numerical evaluation. Cycle 41 gives,
for `m=t-1`,

\[
 {\beta_p\over\beta_{t-1}}
 \le {t\over p}{\log(t-1)\over\log p}
 \left({\log t\over\log(p+1)}\right)^2.                  \tag{42.4}
\]

Consequently a hypothetical uniform relative payment radius `t<=Cp` would
give a uniform beta distortion, while `t-p=o(p)` would give distortion `1+o(1)`.
The finite data suggest a bounded additive radius but do not prove one.

## Squarefree-impulse form

Put

\[
 A_q=(C_q-C_{q-1})\|U_{q-1}\|^2\ge0,
 \qquad H_q-H_{q-1}=-A_q+J_q,
\]

where `J_q=0` off the squarefree integers, and define

\[
 B_{q,t}=\sum_{q\le n<t}\beta_n.
\]

Finite summation in the opposite order gives the exact block identity

\[
 \boxed{
 \sum_{p\le n<t}\beta_nH_n
 =B_{p,t}H_p-\sum_{p<q<t}B_{q,t}A_q
 +\sum_{\substack{p<q<t\\q\text{ squarefree}}}B_{q,t}J_q.} \tag{42.5}
\]

This is the requested bridge from band recovery to the sparse recurrence. A
minimal arithmetic sufficient inequality for a prescribed endpoint is

\[
 \sum_{\substack{p<q<t\\q\text{ squarefree}}}B_{q,t}J_q
 \ge -B_{p,t}H_p+\sum_{p<q<t}B_{q,t}A_q.                 \tag{42.6}
\]

It is also necessary, because (42.5) is an identity. Splitting `J_q` into
positive and negative parts turns (42.6) into the one-sided budget

\[
 \sum B_{q,t}J_q^+
 \ge (-B_{p,t}H_p)_++\sum B_{q,t}A_q+\sum B_{q,t}J_q^-, \tag{42.7}
\]

which is slightly stronger only when `H_p>0`. This formulation identifies the
uniform theorem still needed: weighted favorable squarefree impulses in a
bounded payment window must dominate the initial defect, every deterministic
drift charge, and every unfavorable squarefree impulse.

For the four certified blocks, the three terms `(initial, drift, impulse)` in
(42.5) are respectively

| block `[p,t)` | `B_(p,t) H_p` | `-sum B_(q,t) A_q` | `sum B_(q,t) J_q` | residual |
|---|---:|---:|---:|---:|
| `[2,6)` | `-0.320690189174015` | `-0.164194539853486` | `0.488896189277094` | `0.004011460249593` |
| `[39,42)` | `-0.000140873730900942` | `-0.0000398377584971909` | `0.000627050577733686` | `0.000446339088335554` |
| `[95,103)` | `-0.000649766485991690` | `-0.0000494757492838743` | `0.000767212362091698` | `0.000067970126816134` |
| `[219,231)` | `-0.0000995385024310738` | `-0.0000189534947028947` | `0.000122968386783757` | `0.00000447638964978815` |

The impulse surplus is positive in every finite episode, but the last margin
is small. The computation therefore validates the exact bookkeeping and the
minimal lemma; it supplies no uniform lower bound for future squarefree impulse
budgets.

## Reproduction

```text
uv run --with python-flint python cycle42_negative_band_recovery.py
uv run --with python-flint python -m unittest -v \
  test_cycle42_negative_band_recovery.py test_cycle41_h_event_analysis.py
```
