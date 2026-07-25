# breakthrough-maxing program

## Architecture

This lane has two agents and one-way ownership.

1. `breakthrough-selector` is the control plane. On a scheduled keyed session it
   checks worker health, selects a problem only when the lane is vacant, writes
   a complete frozen attack prompt, pushes it, and launches an independent
   Kortix session pinned to `breakthrough-god`.
2. `breakthrough-god` is the data plane. Its root session runs the never-stop
   autocontinue loop and focuses exclusively on that assignment. It can swarm
   same-target subagents but cannot select or switch problems.

The selector sleeps after dispatch. The worker continues. This prevents the
common failure mode in which one context continually rescores exciting problems
instead of carrying one hard proof through repeated failed attacks.

## Selection scorecard

Select only a problem verified still open from primary sources. Score each
candidate from 1 to 5 on:

- significance and novelty;
- certificate compactness (an explicit graph, matrix, map, finite identity, or
  short exact proof is ideal);
- structural search leverage rather than pure scale;
- exact independent verifiability;
- transfer from known successful counterexample workflows;
- probability that a decisive obstruction can be reached in repeated sessions.

Reject targets whose apparent victory is only a finite check, restricted model,
conditional statement, numerical observation, or reformulation. The selector
records the shortlist and reasons but freezes exactly one winner.

## Assignment contract

Every `breakthrough/assignments/<slug>/prompt.md` must contain:

1. the exact sourced statement and all quantifiers;
2. what constitutes a proof or counterexample;
3. a prominent list of non-solutions and likely overclaim traps;
4. a reproducible verifier specification;
5. structural construction routes and proof routes;
6. adversarial/breaker routes;
7. a first exact experiment and a next-lemma funnel;
8. publication gates: top-level paper, PDF, artifacts, hostile audits, novelty
   check, commit, and only then a simple solved-result post.

The Dinitz--Garg--Goemans counterexample workflow is the model: persistence is
useful when each failed search is compressed into structure and fed into the
next construction. Repeating an unchanged brute-force search is not progress.

## Concurrency and recovery

- At most one `breakthrough-god` root session may be active.
- Before dispatch, the selector runs `kortix sessions status --all --json` and
  reconciles it with `BREAKTHROUGH_STATE.md`.
- Every durable handoff is committed and pushed before a new sandbox consumes
  it. Sibling sessions pull with rebase before push.
- If the worker crashes, the selector restarts or replaces that same assignment;
  it does not choose a more fashionable problem.
- The never-stop plugin handles ordinary idle events. Daily selector ticks are
  a watchdog and dispatch mechanism, not a second research loop.
