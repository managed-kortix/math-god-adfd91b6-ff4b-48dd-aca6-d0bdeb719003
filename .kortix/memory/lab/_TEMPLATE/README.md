# problem lab folder — canonical layout (ShouqiaoW/erdos style)

Every problem you attack gets a folder `.kortix/memory/lab/<slug>/` with:

```
<slug>/
  prompt.md        ← THE attack prompt (authored first, per `prompt-authoring` skill)
  attack-plan.md   ← live plan: lines of attack, current line, next experiments, retreat criteria
  notebook.md      ← numbered experiments: hypothesis → code → result → conclusion
  paper.tex        ← LaTeX source of the proof/paper (this is the "paper")
  paper.pdf        ← compiled via `bash scripts/build-paper.sh <dir>` (commit both)
  nogo/            ← per-worker no-go lemmas (append-only, merge-safe filenames)
  experiments/     ← Python/PARI/SAT scripts + data + exact certificates
  lean/            ← Lean formalization (the gold-standard verification)
```

Workflow (math-god-operator §6 + prompt-authoring):
1. `prompt.md` FIRST — dissect the problem into the proven structure.
2. Attack it with the swarm executing prompt.md's multiagent-search section.
3. When a result survives §7 gates + adversarial audit: write `paper.tex`,
   build `paper.pdf`, formalize key lemmas in `lean/`, then publish the
   illustrated X thread (x-operator) pointing at the certificate.
4. Only a complete, adversarially-audited result is a result. Everything else
   stays here, internal.
