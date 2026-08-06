# Victory record: all connected tetracyclic graphs

## Target

Prove that every finite simple connected graph `G` with
`|E(G)|=|V(G)|+3` satisfies `s^+(G)>=|V(G)|`.

## Exact structure

The positive cyclic-block ranks partition four as

`1+1+1+1`, `2+1+1`, `2+2`, `3+1`, or `4`.

This is exhaustive because cyclomatic rank is additive over blocks. In the
coarser packet language, `1^4` is the cactus row, `2+1+1` and `3+1` are the
two ways a tricyclic packet can be accompanied by one cycle, `2+2` is the
bicyclic-plus-bicyclic row, and `4` is one rank-four block. The coarse
description must not erase the distinct `2+1+1` and `3+1` ownership problems.

## Exact closure ledger

Write `epsilon_q=0` for even `q` and
`epsilon_q=q tan^2(pi/(2q))` for odd `q`, and let `Delta` be the exact theta
DNN excess.

| block ranks | direct closure | residual and closure |
|---|---|---|
| `1^4` | sharp cactus DNN when `sum epsilon_q<=3` | the exact cactus theorem closes `{3,3,3,q}` for odd `q` and `{3,3,5,5}` by induced territories and shared-cut packets |
| `2+1+1` | block DNN when `Delta+epsilon_p+epsilon_q<=3` | only `Theta(1,2,r)+C3+C3` and `Theta(1,2,2)+C3+C5`; the proved owner-exact induced-territory packets close every bridge/shared-cut incidence |
| `2+2` | block DNN when `Delta_1+Delta_2<=3` | only two diamonds `Theta(1,2,2)`; an actual bridge gives two attached bicyclic territories, while a shared cut opens one diamond into an attached diamond of credit `>1` and one tree of credit `-1` |
| `3+1` | use the actual rank-three certificate and close when `e_B+epsilon_q<=3` | the canonical doubled-triangle/doubled-`C4` rows and all-odd `K4` rows with at most one long path close by stronger hostile-cycle DNN certificates or owner-exact induced openings; the unsubdivided `K4` uses its `>2` packet |
| `4` | exact path-elimination DNN with excess at most three | the few structural frontier rows use induced attached-`K4` or favorable-triangle packets; all are included in the 17-kernel theorem |

An actual bridge cut may invoke the established bicyclic or tricyclic theorem
on each induced side. At a shared cut, or when opening a path inside a cyclic
block, the cut vertex, every connector remnant, and every rooted branch must
have exactly one owner. The unquantified tricyclic conclusion `s^+>=|V|`
cannot pay a deleted tree; the rows above use a strict packet credit or DNN
budget instead.

## One rank-four block

Suppress all degree-two paths inside the block. The kernel is loopless,
2-connected, has minimum degree at least three, and satisfies

`sum_v(deg(v)-2)=6`.

Hence it has two through six branch vertices. Independent regeneration gives
exactly `1,2,5,4,5` kernels by branch order, for 17 total. Exact physical-row
ledgers, fixed-parity path monotonicity, symbolic equality certificates, and
the structural packets close every simple subdivision and arbitrary rooted
tree attachment.

## What counts

- a complete multi-block residual packet library;
- an exact rank-four kernel classification;
- all-length path/tree arguments, not finite graph sampling;
- exact rational/symbolic certificates and hostile audits.

## What does not count

- assuming edge addition preserves `s^+`;
- using the tricyclic theorem to pay a deleted tree without a quantified unit
  of surplus;
- treating switching as changing physical canonical path lengths;
- a kernel or parity census without independent regeneration;
- numerical SDP evidence.

## Status

**COMPLETE.** Every finite simple connected tetracyclic graph satisfies
`s^+(G)>=|V(G)|`. The integrated proof is
`all-tetracyclic-graphs/paper.tex`; the master exact audit is
`research/tetracyclic-master-verifier.py`. Its full transitive dependency
manifest has digest
`9fa7bdf4a4a296a69f818bf78d5fe1a3aba5bddb38639ea784593d0291dfe19f`.
No global strictness claim is made because several DNN certificates attain the
auxiliary excess budget three.

Artifact reconciliation (2026-08-05): the historical manifest digest was
`38b93ad68fe94e678de68547f916e4e4c0b58845377050df455ad860f4e16202`.
The dependency drift consists of an expanded rank-four kernel census and
stricter exact-type checks in the finite verifiers. Its canonical payload
digest remains
`d89e6e60c66e480ba89e662ab90b5ace211cbcff7292f92ad1614bb0937eb8e9`,
while it adds automorphism and simple-subdivision checks and increases rejected
hostile mutations from 9 to 11. The master records both digest generations and
preserves that reconciled direct-manifest pin as provenance. The current master
also covers every loaded module and fixture byte plus all direct and nested
verifier outputs, pinned by the transitive digest above. All seven direct
verifiers reject boolean, floating, and nonintegral exact payload mutations.
