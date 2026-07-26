# breakthrough-maxing program

## Architecture

One `math-god` keyed root session owns this lane end to end. It selects only
when `BREAKTHROUGH_STATE.md` is `vacant`, `solved`, or `retired`, freezes one
assignment, and then remains on that assignment until verified resolution or a
committed strategic retirement. This avoids selector/worker dispatch races while
preventing continual rescoring of exciting problems.

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
conditional statement, numerical observation, or reformulation. The lane
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
   check, commit, and the complete `research/procedural/PUBLICATION.md` workflow.

For a genuinely Tier-1 resolution, announcement becomes urgent only after all
gates close: issue one definitive post immediately with the exact claim,
rendered certificate, direct folder/PDF links, API readback, and ledger entry.
The theorem supplies the drama. Do not substitute screaming, profanity,
repetition, or hype for verification.

The Dinitz--Garg--Goemans counterexample workflow is the model: persistence is
useful when each failed search is compressed into structure and fed into the
next construction. Repeating an unchanged brute-force search is not progress.

## Concurrency and recovery

- Exactly one keyed breakthrough root lane is configured.
- Every durable update is committed and pushed; sibling lanes pull with rebase.
- If the session crashes, the keyed trigger resumes the same assignment; it
  does not choose a more fashionable problem.
- The never-stop plugin handles ordinary idle events and the daily heartbeat is
  only a resurrection net.
