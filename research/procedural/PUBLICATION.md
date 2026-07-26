# Verified-result publication workflow

This is the repository's mandatory destination-aware publishing contract. A
result is published once, accurately, and with enough public evidence for a
stranger to check it. External submission is not a substitute for verification.

## 1. Acceptance gate

Before any external action, require all of the following:

1. exact sourced statement and current-status/novelty check;
2. complete proof or counterexample, with scope and non-solutions explicit;
3. `paper.tex`, built `paper.pdf`, reproducibility instructions, and every cited
   certificate committed;
4. hostile mathematical audit and independent reproduction where computation
   is material;
5. material AI assistance disclosed in the paper/evidence;
6. permanent public folder and PDF URLs at the committed revision;
7. a row in `research/publication-manifest.json` with an eligibility decision.

Restricted classes, finite checks, heuristics, and conditional results are never
reported as resolving the original universal conjecture.

## 2. Destination decisions

### X

Announce a finished theorem or counterexample once, using a readable flat claim,
rendered card, direct folder/PDF links, API readback, and
`research/tweet-ledger.md`.

### Open Conjecture Board (OCB)

OCB is a registry of open conjectures and resolutions, not a theorem repository.

- If a sourced conjecture is still open and absent from the Board, submit its
  exact original statement through `POST https://openconjectures.org/submit`.
- Verify the requested link using the connected Gmail mailbox. Never store a
  verification token or raw verification URL in Git or a ledger.
- At most three verified pending submissions may exist for one email address.
  Do not evade this limit; wait for editorial review.
- A full proof/counterexample may be reported only after the corresponding
  conjecture has a public `/c/<id>` page whose JSON advertises the
  `report_resolution` action. Report the exact resolution scope, evidence URL,
  and AI involvement. A special case is not a kill.
- If a result is not a full resolution, place it in the public evidence for the
  open conjecture and manifest, but do not send a resolution report.
- Discover state from `https://openconjectures.org/api/v1/conjectures/<id>`;
  never assume a write action remains available.
- Do not retry an uncertain write. Reconcile the Board, Gmail, and ledger first.

OCB form fields and limits are documented in `scripts/open-conjectures.py`.
Every completed action is appended to
`research/open-conjectures-ledger.md`; tokens, private email contents, and
credentials are forbidden there.

### Authors

Contact the source conjecture's corresponding author when reasonably possible
before a public resolution report, as OCB requests. Prefer one concise courtesy
message after a stable public evidence link exists:

- identify the exact conjecture and literal claimed scope;
- distinguish full resolution from partial progress;
- disclose autonomous AI proof search, drafting, code, and internal audits;
- invite corrections/prior-work pointers without requesting endorsement;
- no large attachment, no mass mail, no repeated follow-ups (at most one after
  two or three weeks), and never treat silence as approval.

Draft and log the decision. Sending requires an appropriate accountable identity
and final message review; the connected `agent@kortix.ai` mailbox may be used for
transparent Agent Mirko correspondence, not to impersonate a human author.

For a major result, one professional outreach thread is part of normal closeout:
write the corresponding/source author or one clearly relevant expert, not a
mailing list. Start a new thread once, then use Gmail's `inReplyToMessageId` for
every follow-up so context remains intact. Search the mailbox before sending to
avoid duplicates. Additional recipients require a distinct mathematical reason,
not publicity. Record the message/thread ID and purpose in
`research/email-outreach-ledger.md`, never private reply content without consent.

For the strongest results, one additional technical-review invitation is
permitted when it has a distinct reason—for example, the result extends that
recipient's theorem and asks them to inspect the dependency trace. The default
maximum is two initial external threads per result in total: one source-author
courtesy thread and one technically targeted peer-review thread. More requires
a documented response, referral, or concrete gap that only that specialist can
assess. Never send a generic promotional request or imply that review is owed.

### Publication inbox and status review

The Main core performs one consolidated review per UTC day and records the date
in `research/publication-inbox-state.json`:

1. Search Gmail for replies in ledgered outreach threads and operational mail
   from `board@openconjectures.org`.
2. Read only relevant threads. Continue with `inReplyToMessageId`; never fork a
   conversation into a new subject.
3. Respond when there is a mathematical correction, question, referral, or
   administrative request. Do not send acknowledgments merely to keep a thread
   active. Keep private mathematical feedback private unless permission is
   explicit.
4. Check public OCB JSON for every pending manifest item. If approved, record
   the public ID and readback. If an exact full-resolution item exposes
   `report_resolution`, contact having already occurred, submit the narrowly
   worded report and disclose AI involvement. If rejected or unchanged, do not
   repeatedly resubmit.
5. Update token-free ledgers and the manifest only on a status change or
   substantive exchange. Never store verification links, tokens, private message
   bodies, or third-party personal data beyond necessary public contact metadata.

This daily review is operational housekeeping, not a license for daily email.

### Preprints, archives, and journals

- Prepare a consolidated preprint package and metadata, but arXiv/HAL/journal
  submission requires a real accountable human author or approved proxy who can
  truthfully accept authorship, rights, licensing, and correctness obligations.
  Never list an AI system as an author or invent a human author.
- Prefer one primary preprint (normally arXiv `math.CO`) and one curated immutable
  certificate archive (normally Zenodo), linked bidirectionally. Do not spray
  duplicate records across repositories.
- Do not use MathOverflow to announce results or request proof checking.
- Avoid salami publication: consolidate overlapping rank-by-rank or superseded
  manuscripts before journal submission.
- Candidate venues for spectral graph theory include Electronic Journal of
  Combinatorics, Linear Algebra and its Applications, and Discrete Mathematics;
  verify current scope, AI policy, fees, and author instructions at submission.

## 3. Idempotent execution

1. Run `python3 scripts/publish-result.py check <slug>`.
2. Inspect the manifest and both ledgers for prior destination/result/commit
   actions.
3. Use `scripts/open-conjectures.py prepare <manifest-id>` to produce a redacted
   review payload. Network writes require explicit `--submit`.
4. For conjecture submissions, retrieve the verification email through Gmail,
   inspect the host, and complete GET + confirmation POST. Never print or commit
   the token.
5. Read back public state when possible, then append a token-free ledger record.
6. Update the manifest status and lane state; commit and push.

No publication action runs from a Git hook, heartbeat, or idle plugin. Research
triggers invoke this workflow only after the acceptance gate is closed.

## 4. Current packaging policy

- Submit/report exact sourced conjectures, not every theorem paper.
- The cactus rank papers are major partial progress on AKMPZ Conjecture 1.2 but
  are not nine separate OCB conjectures or kills.
- `all-decacyclic-cacti` is authoritative over duplicate
  `all-rank-ten-cacti`.
- The component bicyclic papers are subsumed by `all-bicyclic-cacti` for external
  packaging.
- AKMPZ Conjecture 9.2(i) is a claimed full resolution in
  `tree-equality-square-energy`; it must be linked to the Board entry for that
  exact conjecture, not conflated with Conjecture 1.2.
