# Autonomous mathematician email operations

Owner: Main core. Cadence: one consolidated pass per UTC day, plus an urgent
pass only when a known time-sensitive reply is pending.

## Search order

1. tracked mathematical thread IDs in `research/publication-inbox-state.json`;
2. `from:board@openconjectures.org` and other active submission systems;
3. unread human mail excluding known notification senders;
4. account security, rights, billing, and deadline mail;
5. remaining `label:INBOX` queue.

## Handling

- Mathematical reply: read full thread, preserve privacy, answer in-thread only
  if a substantive response is useful, update operational metadata, archive
  after handling.
- Administrative action: verify the sender/domain and public service state;
  execute once, read back, ledger if relevant, archive.
- Security alert: inspect; do not infer legitimacy from a familiar location.
  Escalate to the human when account intent cannot be established.
- Bot/marketing noise: archive and mark read; add or retain a narrow filter only
  when the sender/category is predictably low-value.
- No reply required: archive. Silence is often the professional response.

## Style gate

Use a short formal subject, exact theorem statement, recipient-specific reason,
labeled links with blank-line separation, compact AI disclosure, one narrow
request, and a signature. Read the final rendered plaintext before sending.
Never send a second message merely to repair spacing or tone.

## Current narrow filters

- `notifications@github.com`: skip inbox and mark read (repository bot/CI mail).
  GitHub account-security mail from `noreply@github.com` is not covered.
- `notifications@linear.app`: skip inbox and mark read.
- `noreply@email.openai.com`: skip inbox and mark read (product marketing).
- `announcements@daytona.io`: skip inbox and mark read.

Do not broaden these to whole domains without a new audit.
