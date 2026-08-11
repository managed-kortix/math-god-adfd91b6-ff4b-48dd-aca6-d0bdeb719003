# All-connected hexacyclic synthesis plan

## Status and promotion boundary

This is a file plan and dependency contract for the main-lane synthesis after
the order-nine and order-ten exact coverage gates are green. It is not a
theorem artifact, does not promote either coverage gate, and does not support a
claim that the all-connected theorem is complete.

The final target is:

> Let `G` be a finite simple connected graph with `|V(G)|=n` and
> `|E(G)|=n+5`. Then `s+(G)>=n`.

Use **unique positive-rank cyclic block**, not "exactly one nontrivial block."
Bridge `K2` blocks belonging to attached trees are nontrivial blocks in the
standard block convention. This wording distinction is a theorem-layer
obligation, not editorial polish.

No file listed below should be called a theorem owner merely because a search
process exits, a manifest has full ranges, or a coverage gate prints
`ready_for_theorem_promotion=true`. In particular, the order-nine and order-ten
coverage payloads deliberately retain `theorem_claimed=false`.

## Exhaustive mathematical split

For every cyclic block `B`, put `beta(B)=|E(B)|-|V(B)|+1`. Block additivity of
cyclomatic rank gives

```text
sum_(cyclic blocks B) beta(B)=6.
```

The eleven positive integer partitions are

```text
1+1+1+1+1+1   2+1+1+1+1   2+2+1+1   2+2+2
3+1+1+1       3+2+1       3+3       4+1+1
4+2           5+1         6.
```

The first ten are exactly the multiblock branch. The last has one
positive-rank cyclic block `B` of rank six. Suppressing all degree-two vertices
of `B` gives a loopless 2-connected multigraph `K` with minimum degree at least
three. If `v=|V(K)|`, then `|E(K)|=v+5` and `3v<=2v+10`, hence `2<=v<=10`.
The canonical kernel fixture has order counts

```text
1, 4, 26, 84, 216, 314, 325, 162, 66; total 1198.
```

Thus the final proof has a disjoint two-branch implication:

```text
all connected rank-six graphs
  = graphs with at least two positive-rank cyclic blocks
    disjoint-union graphs with one positive-rank cyclic block
  -> multiblock theorem OR rank-six orders-2-through-10 theorem.
```

The paper must prove this block-decomposition implication. An executable master
can audit the owner registry and scopes, but cannot replace the standard block
theory argument.

## Dependency DAG and current identity locks

All SHA-256 values in this section identify the repository bytes inspected for
this plan. Final publication roots must be regenerated after the order-nine and
order-ten manifests and promotion owners are frozen; these current values are
not final theorem roots.

### Multiblock owner

Direct verifier:

```text
research/hexacyclic-multiblock-ledger-verifier.py
current source SHA-256:
1ca6a90c763f5f9339143e729767a026225cad331ccf81888a8dc8f490a117ca
```

It generates all eleven partitions, selects the ten multiblock partitions,
locks nine sources, regenerates the three rank-five structural families, checks
12 owner-incidence cases, and rejects 19 hostile mutations. Its locked leaves
are:

| logical owner | path | SHA-256 pinned by verifier |
|:--|:--|:--|
| combined theorem | `positive-square-energy/hexacyclic-general/multiblock-items1-7-combined-theorem-audit.md` | `7c9e6a371000283958d4d1eb7db0a181b4968fe50cf4a37fd8d7d26eddc43378` |
| items 1--4 | `positive-square-energy/hexacyclic-general/multiblock-items1-4-owner-exact-closure.md` | `49a24ebe705aecd9248224cc39c748041c0d6d4981a137f6daad6d93019a1cb1` |
| items 5--7 | `positive-square-energy/hexacyclic-general/multiblock-items5-7-owner-exact-closure.md` | `1c5722565e874ebf04533e908c5bf335f7be0b56a5665f5b607cfdef14ac8c67` |
| theta--triangle packet | `positive-square-energy/hexacyclic-general/favorable-theta-triangle-shared-cut-packet.md` | `d222e09a20dce19703f8386c6a3a3699e0621b63f761e553fee3215adf8e2446` |
| rank-four ledger | `all-tetracyclic-graphs/paper.tex` | `ae4b50ba72d1e3e66b2fe8aa95e4851397f1b805a27f904561da68ea4fa6b2da` |
| all-odd K5-e ledger | `positive-square-energy/pentacyclic-general/all-odd-k5e-induced-territory-frontier.md` | `e43bbd97566ab5ea28b360311a2e3e1bc40397c3f40f250e954d1c016d94e6a5` |
| K5-e sieve | `pentacyclic/research/all-odd-k5e-territory-sieve.py` | `047a472d4e1af46850198dc68b5780f98b930618f79b51174f11460afcc0334d` |
| K22 fixture | `pentacyclic/research/order5-kernel-family-theorem.json` | `4d8b826b397dc269c7853b8bd386d00bf469282b52720b8dac96d850e9e616d8` |
| K71 fixture | `pentacyclic/research/order6-kernel-family-theorem.json` | `69b236b014aef58c037c610ca01fa62ad82601f7bb34153939ec4ddd3b5f364d` |

Publication contract: promote this verifier to emit a canonical scope/conclusion
manifest, pin both normal and optimized output digests, and make the final
all-connected master consume that manifest. Preserve the nonstrict relation:
the rank-five excess-four plus triangle row meets budget five exactly.

### Kernel census

```text
fixture: research/fixtures/rank-six-kernels.json
fixture SHA-256:
5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476

verifier: research/rank-six-kernel-census-verifier.py
current source SHA-256:
325b78066b626a00deaceb6a026377dd7f898a906c63c597f77831548585e1ee
```

The census must remain the unique authority for `K1`--`K1198`, order interval
`2`--`10`, degree constraints, no-cut-vertex checks, canonicalization, and the
order partition `1+4+26+84+216+314+325+162+66`.

### Orders two through seven

Current implication owner:

```text
research/rank-six-order2-7-master-verifier.py
current source SHA-256:
a84d100a61433eae1944db1036693a0eec136c53343192d6c238392335cf742f
```

Its direct registry is already explicit:

| scope | verifier | source SHA-256 pinned by owner |
|:--|:--|:--|
| census 2--10, selected 2--7 | `research/rank-six-kernel-census-verifier.py` | `325b78066b626a00deaceb6a026377dd7f898a906c63c597f77831548585e1ee` |
| orders 2--4, `K1`--`K31` | `research/rank-six-low-order-master-verifier.py` | `aa440adb33e7315cf8abe1d83d7d201e3faacb50d6b67900cce133397c8de458` |
| order 5, `K32`--`K115` | `research/rank-six-order-five-kernel-theorem-verifier.py` | `7c6f4048f9c4bf955aaab71a2e92aaec36cf6ba6aa7d6feaa2fff50fe2881046` |
| order 6, `K116`--`K331` | `research/rank-six-order-six-kernel-theorem-verifier.py` | `e4b5b21900eafd41910ab7fda7f0b178effaef37411cfb36da983d9f8686a46c` |
| order 7, `K332`--`K645` | `research/rank-six-order-seven-equality-frontier-verifier.py` | `a9806d2a6a8fc1e7c93b3c0b6ec18cef84a7184e15b25cae4455e2cb5b4f4457` |

Transitive finite leaves are owned by those verifiers:

- orders 2--4: the kernel fixture and
  `positive-square-energy/hexacyclic-general/seven-path-dnn-theorem.md`, pinned
  there as `cf3625413b6e77e84f87414b103d5f9e656cbd106445c2d2803469f3586fbb92`;
- order 5: `research/fixtures/rank-six-order-five-tetra-census.json` at
  `9656146c9dfefacc1c8df15fa9e7c8423f04b12c802c08af93f6e3f3e520bf22`
  and `research/fixtures/rank-six-order-five-dim5-rational-gram-results.json`
  at `ae5f78b189a04e9a3e790188c5f4577a92c5dd19463267aceaec1a8f54bbd2c0`;
- order 6: `research/fixtures/rank-six-order-six-theorem.json`, the three
  rational chunks named by that fixture, the order-six coarse census, and the
  canonical rank-six kernel source, all digest-checked by the owner;
- order 7: the equality fixture at
  `3afbc2bef60604eede74611e5a75c045e5f143f8b0737c7679025c3a1577d6d2`,
  six compressed chunks and their six raw digests, ordered raw-manifest digest
  `5a3693a15beb0a6c37089c5fe15f78eaf76875dcd3096b98a2fc3dbf0f339324`,
  and three engine sources pinned in the equality verifier.

Gate before reuse: replace acceptance-substring-only integration with a
canonical child-manifest interface, or have the new orders-2--10 master parse
and validate the existing canonical `--print-manifest` payload from the
orders-2--7 owner while independently pinning its source and output. Do not
reduce the existing exact replay or hostile checks.

### Order eight

The theorem owner is already separate from its non-theorem census ingredients:

```text
research/rank-six-order-eight-kernel-theorem-verifier.py --full
current source SHA-256:
96f3d75efccbe3da802547bcf2ae2643f506305d1a261115186260db5e29c674
```

Its seven pinned leaves are:

| leaf | SHA-256 |
|:--|:--|
| `research/fixtures/rank-six-kernels.json` | `5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476` |
| `positive-square-energy/experiments/rank6_order8_orbit_frontier_census.py` | `83527bb0b5dba2cd19040fc23c3c9f02fe4c6bed21620eb1ca7c571b70cb3407` |
| `positive-square-energy/experiments/rank6_order8_orbit_frontier_census.json` | `724fdb337b7bb9225b1a8691c28e131ae1c8de7dc38bb13a5adbb98c1f92218e` |
| `positive-square-energy/experiments/rank6_order8_pack_auditor.py` | `21dc6cafe2539bb20e91ea3bf278f3e7ff8d66602b5acbe1c0d3d73f44f02175` |
| `positive-square-energy/experiments/rank6_order8_search_manifest.json` | `dd97ff3059cd637177171cb5d335cc17889a3714459522232e8110c5d79da469` |
| `positive-square-energy/experiments/rank6_order8_symbolic_recognizers.py` | `755dd24b9e3f129dc6cd4fe590c4c13031bd22c41054ca29082981e3f5d909fe` |
| `positive-square-energy/experiments/rank6_order8_symbolic_templates.json` | `2f457374d9627bd27339a0988aa47149db825dd0cba050c71ac9accfa3f72b95` |

The v2 pack manifest transitively owns the 17 XZ chunk identities. The theorem
owner requires full exact replay, 325 kernels `K646`--`K970`, 1,441,832 target
keys, and disjoint ownership `1,441,808` rational plus `24` symbolic.

### Orders nine and ten: green is necessary, not promotion

Current completion gates and current partial-manifest identities are:

| order | completion gate | current gate SHA-256 | current manifest SHA-256 |
|:--|:--|:--|:--|
| 9 | `research/rank-six-order-nine-coverage-verifier.py` | `8fe862c11355a46f052e8be2b37fe7ab531a7dc5a81afe1a2277533a50d7c5f7` | `4c4eaab658d02e66378da1d81c51227808196746171691353582e38623e0f409` |
| 10 | `research/rank-six-order-ten-coverage-verifier.py` | `30a6341dc7a1763b1b87e465b68f44dc140a8dae4d4bd739f7d9b4285ecb0390` | `6620fcfc28a979b6d95b379e1a08bc1e4c6a97c21cec9a576be18a33e56196f8` |

Those manifest digests are expected to change when final chunks are registered.
Never copy them into the paper as final roots.

The order-nine manifest transitively binds:

```text
rank6_order9_sparse_witness.py
rank6_order8_sparse_pipeline.py
pentacyclic/research/order7-dim7-rational-gram-experiment.py
rank6_order9_symbolic_recognizers.py
rank6_orders8_10_atom_ledger_search.py
rank6_orders8_10_atom_ledger_classification.json
research/fixtures/rank-six-kernels.json
every ordered R9G1 XZ chunk and raw stream
```

The order-ten manifest transitively binds:

```text
rank6_order10_cubic_exact_rational.py
rank6_order10_cubic_frontier_census.py
rank6_order10_equality_recognizer.py
rank6_order10_equality_recognizer.json
rank6_orders8_10_atom_ledger_search.py
rank6_orders8_10_atom_ledger_classification.json
research/fixtures/rank-six-kernels.json
every ordered R10G1 XZ chunk and raw stream
```

After green, add theorem-promotion owners rather than weakening the gates:

```text
research/rank-six-order-nine-kernel-theorem-verifier.py
research/rank-six-order-ten-kernel-theorem-verifier.py
```

Each promotion owner must pin the final coverage-gate source, final pack
manifest, auditor and all transitive manifest dependencies; invoke full exact
mode in normal and optimized Python; require complete source intervals
`[0,186295)` and `[0,125457)`; require target totals `2,794,425` and
`2,007,312`; validate exact disjoint rational/symbolic ownership; restate the
simple-subdivision, all-length, and rooted-tree lift contracts; and emit

```text
scope: order=N; rank=6; exact kernel interval; single positive-rank block
conclusion: kappa(B)<=|E(B)|+5 and therefore s+(G)>=|V(G)|
excluded: multiblock and all-connected hexacyclic theorem
```

The wrappers must not accept `ready_for_theorem_promotion` as a status-only
shortcut. They must cause or inherit the exact replay and bind its canonical
output.

## Files to add after both completion gates are green

```text
research/
  rank-six-order-nine-kernel-theorem-verifier.py
  rank-six-order-ten-kernel-theorem-verifier.py
  rank-six-order2-10-master-verifier.py
  hexacyclic-all-connected-master-verifier.py

positive-square-energy/hexacyclic-general/
  order-nine-rank-six-kernel-theorem.md
  order-ten-rank-six-kernel-theorem.md
  all-rank-six-single-block-kernel-theorem.md
  all-connected-hexacyclic-theorem-audit.md

all-hexacyclic-graphs/
  paper.tex
  README.md
  HOSTILE_AUDIT.md
```

Do not create `post.txt`, result cards, or publication text until every
publication gate below passes. They are dissemination artifacts, not proof
dependencies.

### `rank-six-order2-10-master-verifier.py`

Required direct owner registry:

```text
kernel census       orders 2--10, K1--K1198
orders-2--7 owner   orders 2--7,  K1--K645
order-8 owner       order 8,       K646--K970, mandatory --full
order-9 owner       order 9,       K971--K1132, mandatory full exact replay
order-10 owner      order 10,      K1133--K1198, mandatory full exact replay
```

Required predicates:

1. Pin every direct source digest and canonical child-output digest.
2. Parse child manifests; do not infer scope from an acceptance substring.
3. Require exact order set `{2,...,10}` and exact contiguous kernel intervals.
4. Require fixture identity and counts to agree in every child.
5. Require every owner conclusion to be the uniform DNN bound
   `kappa(B)<=|E(B)|+5`, or an explicitly typed structural route proving the
   same final spectral statement.
6. Emit one canonical implication manifest with arbitrary simple subdivision
   lengths and arbitrary genuine rooted-tree attachments.
7. Reject omitted/duplicated orders, altered intervals, changed conclusion,
   status-only owners, widened multiblock scope, changed dependency digests,
   and normal/optimized output drift.

Expected theorem scope after all checks is exactly 1,198 single-block kernel
families. It is not yet the all-connected theorem.

### `hexacyclic-all-connected-master-verifier.py`

Direct owners:

```text
research/hexacyclic-multiblock-ledger-verifier.py
research/rank-six-order2-10-master-verifier.py
```

Required predicates:

1. Pin source and canonical output digests for both owners.
2. Validate scopes `at least two positive-rank cyclic blocks` and `exactly one
   positive-rank cyclic block`; reject the ambiguous phrase "one nontrivial
   block."
3. Require both conclusions to be nonstrict `s+(G)>=|V(G)|`.
4. Record, but do not pretend to execute, the analytic block decomposition
   lemma that the two scopes are exhaustive and disjoint for connected rank-six
   graphs.
5. Emit one canonical root manifest with target hypothesis
   `finite simple connected; |E|=|V|+5` and no strictness/equality claim.
6. Reject a missing branch, overlapping scope, strict promotion, changed
   multiblock equality row, changed single-block kernel total, theorem claim
   based directly on a coverage gate, or normal/optimized drift.

This is the missing executable theorem layer between the two already separate
branches and the paper's headline theorem.

## Paper skeleton and claim ledger

Create `all-hexacyclic-graphs/paper.tex` only after the two new order owners and
the orders-2--10 master are green. Suggested structure:

```text
Title / AI authorship line / date
Abstract
1. Statement and scope
   Theorem: finite simple connected, m=n+5 -> s+(G)>=n
   Explicit nonclaims: strictness, equality classification, edge monotonicity
2. Analytic foundations
   induced superadditivity
   DNN correlation dual and one-vertex additivity
   exact path elimination and fixed-parity monotonicity
3. Block decomposition
   cyclic-block rank additivity
   eleven partitions
   exhaustive two-branch split
4. Multiblock theorem
   ten partitions, DNN rows, structural pre-sieve, packets A--I
   owner-exact connectors/shared cuts/rooted branches
   nonstrict rank-five-equality-plus-triangle boundary
5. Unique positive-rank block
   suppression lemma, simplicity conditions, 2<=order<=10
   canonical 1,198-kernel census
6. Finite single-block theorem
   per-order table: kernels, physical rows, orbits, coarse/residual targets,
   rational/symbolic/structural ownership
7. Arbitrary lengths and trees
   canonical-plus-one-coordinate frontier implication
   internal-subdivision roots and trace calculation
8. Proof of the main theorem
   invoke multiblock or single-block owner after exhaustive split
Appendix A. Exact certificate schemas
Appendix B. Dependency DAG, leaf hashes, and transitive roots
Appendix C. Hostile mutations and normal/-O reproduction
Appendix D. Trusted base and limitations
AI disclosure and bibliography
```

Claims the paper may make after all gates pass:

- every finite simple connected graph with `m=n+5` satisfies `s+(G)>=n`;
- the cyclic-block rank partitions are exactly the displayed eleven;
- the ten multiblock partitions are covered by the audited owner ledger;
- the unique-positive-rank-block branch suppresses to exactly 1,198 kernels on
  branch orders 2--10;
- exact finite owners establish the DNN budget or typed structural conclusion
  for every required canonical/coordinate target;
- fixed-parity monotonicity and one-vertex additivity cover arbitrary simple
  subdivisions and rooted trees, including roots at internal path vertices.

Claims the paper must not make without new proof:

- strict inequality for every hexacyclic graph;
- a classification of equality or of every possible cost-five Gram geometry;
- edge-addition, one-edge subdivision, contraction, or `s+` monotonicity;
- a theorem for multigraph realizations or for replacement paths that are not
  internally disjoint;
- independent verification, human review, peer review, or external publication.

## README and hostile-audit skeleton

`all-hexacyclic-graphs/README.md` should contain:

```text
headline theorem and exact graph hypotheses
proof map: eleven partitions -> 10 multiblock + rank-6 single block
1198-kernel order ledger
finite certificate model and exact ownership rule
short verification commands
full replay commands with runtime/storage warning
final direct and transitive SHA-256 roots
build command
scoped nonclaims and AI disclosure
```

`all-hexacyclic-graphs/HOSTILE_AUDIT.md` should contain:

```text
theorem boundary and trusted base
dependency DAG with source/output/root hashes
mutation matrix by verifier
normal versus python -O byte-identity table
full chunk replay and aggregate procedure for orders 7--10
scope attacks: omitted partition/order, overlap, widened all-connected claim
data attacks: gaps, overlaps, duplicate keys, malformed JSON/XZ/binary/rationals
math-interface attacks: parity change, non-simple realization, connector as tree,
  canonical-only equality inference, strictness promotion
known nonclaims and independent-reimplementation guidance
```

## Publication gates

All gates are conjunctive.

1. **Order-nine finite gate.** Final manifest covers `[0,186295)`, all
   2,794,425 targets have exact disjoint owners, normal and optimized full
   replay agree, and the new order-nine theorem owner emits a scoped conclusion.
2. **Order-ten finite gate.** Final manifest covers `[0,125457)`, all
   2,007,312 targets have exact disjoint owners, normal and optimized full
   replay agree, and the new order-ten theorem owner emits a scoped conclusion.
3. **Single-block master gate.** The orders-2--10 owner validates all nine
   orders, all intervals `K1`--`K1198`, all child conclusions, and one
   transitive manifest root.
4. **Multiblock gate.** Re-run the eleven-partition verifier in both modes;
   promote it to canonical manifest output; preserve all nine packets, five
   pre-sieve rows, three rank-five structural owners, 12 incidence cases, and
   the nonstrict equality boundary.
5. **All-connected synthesis gate.** The final master validates the disjoint
   two-branch scope and prints the all-connected root without importing search
   status as theorem evidence.
6. **Manuscript audit gate.** Every headline, abstract sentence, theorem,
   table count, command, digest, and nonclaim agrees with emitted manifests;
   bibliography paths exist; no stale cactus-only or strict claim survives.
7. **Reproduction gate.** Run every top-level verifier normally and with
   `python3 -O`; run mandatory full replays; record byte-identical outputs and
   final output SHA-256 values; independently rebuild all canonical manifests.
8. **Build gate.** `bash scripts/build-paper.sh all-hexacyclic-graphs` succeeds
   from a clean artifact directory, the PDF has no undefined references or
   missing citations, and README commands match the repository.
9. **Disclosure gate.** State AI generation and explicitly disclaim human
   authorship, human review, independent verification, peer review, and
   external publication unless any of those events actually occurs.
10. **Dissemination gate.** Only after gates 1--9 may post text, result cards,
    release metadata, or project-state promotion be prepared. This plan does
    not perform that promotion.

## Internal eventual-publication checklist

This checklist specializes `research/procedural/PUBLICATION.md` to
`all-hexacyclic-graphs`. It is a fail-closed record for a possible future
publication, not authorization to contact anyone, submit anything, create a
post, or change project state. Every box remains open while the manuscript is
conditional. Complete the boxes in order and record only committed paths,
public identifiers, dates, and digests; never store credentials, verification
tokens or URLs, mailbox contents, or private replies.

### A. Solved-result acceptance

- [ ] **Unconditional theorem.** Gates 1--5 above are green and the final
  manuscript proves exactly: every finite simple connected graph `G` with
  `|E(G)|=|V(G)|+5` satisfies `s+(G)>=|V(G)|`. Remove the conditional title,
  theorem premise, promotion placeholders, and nonpublication language only
  after the all-connected master accepts the disjoint exhaustive split. Do not
  promote strictness, equality classification, edge/subdivision monotonicity,
  nonsimple realizations, or the general `m>=n+1` conjecture.
- [ ] **All exact replay.** From a clean artifact directory, run every direct
  and transitive theorem verifier under both `python3` and `python3 -O`,
  including mandatory full exact replays for orders 8, 9, and 10, the
  orders-2--10 master, the canonical multiblock owner, and the all-connected
  master. Require zero exits, byte-identical canonical outputs across modes,
  exact regenerated target-set equality, and frozen source/output/transitive
  SHA-256 maps. Digest-only audits, chunk receipts, prior segmented runs,
  coverage totals, and `ready_for_theorem_promotion` fields do not count.
- [ ] **Independent reproduction and hostile audit.** Rebuild every canonical
  manifest from committed sources and certificates; run all malformed-data,
  omitted/duplicated-owner, scope-widening, parity, simplicity, connector, and
  strictness mutations. Record the actual independence level without calling
  a second run of the same implementation independent verification.
- [ ] **Manuscript-source audit.** Check every headline, theorem, abstract
  sentence, count, command, digest, citation, disclosure, and scoped nonclaim
  against the accepted manifests and source files. Confirm all cited
  certificates are committed and reproducibility instructions start from a
  clean checkout.

### B. Source and novelty

- [ ] **Exact source readback.** Re-read the current source paper rather than
  relying on repository prose. The 11 August 2026 audit read back
  `https://arxiv.org/abs/2506.07264v1` (submitted 8 June 2025), whose abstract
  states the connected-simple `m>=n+1` conjecture; before publication, verify
  the current version/history and quote Conjecture 1.2 exactly from the source
  PDF. Record the public source URL/version/date, not author email data.
- [ ] **Current-status and novelty audit.** Search current versions of the
  source paper, arXiv, MathSciNet/zbMATH or available equivalents, citation
  graphs, and targeted web/scholar queries for the full connected hexacyclic
  (`m=n+5`) case and for the specific DNN/kernel method. Read plausible hits,
  distinguish prior cactus and lower-rank results from the claimed scope, and
  write a dated, query-documented audit. A negative search supports careful
  wording only; it never proves novelty or priority.
- [ ] **Claim wording after audit.** If no prior result is found, say only that
  no prior proof was located in the documented search. If overlapping or prior
  work is found, cite it and narrow or withdraw the novelty/publication claim
  before any outreach or dissemination.

### C. Package and PDF readback

- [ ] **Complete package.** Add the final `README.md` and `HOSTILE_AUDIT.md`,
  retain the AI-assistance disclosure, add the eligible row to
  `research/publication-manifest.json`, and commit `paper.tex`, `paper.pdf`, all
  cited certificates, and exact reproduction instructions at one frozen
  revision. The manifest must classify this as a complete hexacyclic class
  theorem and partial progress on AKMPZ Conjecture 1.2, not a full resolution
  of that conjecture.
- [ ] **Clean build.** Run
  `bash scripts/build-paper.sh all-hexacyclic-graphs` from a clean artifact
  directory; reject missing citations, undefined references, stale TODOs,
  conditional labels, overfull/cropped content that changes readability, and
  commands that do not match the committed repository.
- [ ] **PDF readback.** Extract and read back all PDF text, inspect every page
  visually at normal zoom, and compare title, theorem hypothesis/conclusion,
  equations, tables, links, disclosures, bibliography, page count, and final
  PDF SHA-256 against `paper.tex` and the accepted manifests. After permanent
  public URLs exist, download both folder and direct PDF links anonymously and
  repeat the readback/hash check on the served bytes; a successful local LaTeX
  build alone is insufficient.

### D. Contact and destinations, only after solved

- [ ] **No early external action.** Until A--C are complete, do not contact an
  author or reviewer, prepare/send an OCB write, post on X, create publication
  text or result cards, or imply that the conditional draft is solved. Drafting
  an eventual contact decision is internal only and contains no private data.
- [ ] **Author courtesy contact.** Only after the solved paper and stable public
  evidence links pass PDF readback, search the mailbox and ledgers for duplicate
  threads, identify one source/corresponding author from public source metadata,
  and obtain final message review under the professional-correspondence rules
  in `PUBLICATION.md`. Send at most one concise courtesy thread using an
  accountable identity; state the exact hexacyclic scope, distinguish it from
  the general conjecture, disclose AI involvement, and invite corrections or
  prior-work pointers without requesting endorsement. Log only date, purpose,
  role, and message/thread ID; never persist addresses unnecessarily, tokens,
  private message bodies, or replies without consent. This checklist sends no
  message.
- [ ] **OCB eligibility readback.** Only after the theorem is solved and author
  contact has occurred, read back the Board state idempotently. Do not submit a
  duplicate of the already pending AKMPZ Conjecture 1.2 entry, do not treat the
  hexacyclic class theorem as a kill, and do not call `report_resolution`: it
  does not resolve the source conjecture for all `m>=n+1` graphs. At most add
  the stable paper as public partial-progress evidence if the Board exposes an
  appropriate action and the manifest authorizes it. An absent action means no
  write; an uncertain write is never retried. Store no verification secret.
- [ ] **X publication and readback.** Only after every preceding applicable box
  is closed, prepare one flat, scope-exact announcement with rendered card and
  permanent folder/PDF links. Re-run `python3 scripts/publish-result.py check`
  for the final slug, inspect the manifest and tweet ledger for duplicates,
  post once, then verify through API readback the post ID, account, exact text,
  media, and both links before appending a token-free ledger entry. Failure of
  readback leaves publication unresolved and does not authorize a duplicate
  post. This checklist performs no post.

## Execution order once order nine and ten are green

1. Freeze final order-nine and order-ten manifests and obtain complete exact
   normal/optimized reports.
2. Add and hostile-audit the two order theorem-promotion owners.
3. Normalize orders 2--8 to canonical child manifests without weakening their
   existing exact checks.
4. Add the orders-2--10 master and freeze its direct/output/transitive root.
5. Upgrade the multiblock verifier to canonical manifest output and re-freeze
   its source/output root.
6. Add the all-connected master and test the disjoint scope union.
7. Write the theorem audit note, then `paper.tex`, README, and hostile audit
   from emitted data rather than hand-copied search logs.
8. Run the full publication gates, build the PDF, and only then consider
   dissemination or state changes.
