# long computations — the iron rule

tags: computation, background, checkpoint, timeout

The shell tool KILLS any foreground command at 20 minutes and the work is
LOST. Therefore, hard rule with zero exceptions:

**Any command that could run >5 minutes NEVER runs foreground.** Pattern:

```
nohup ~/mathenv/bin/python batch_job.py --checkpoint-dir lab/<slug>/ckpt \
  > lab/<slug>/job-<name>.log 2>&1 &
echo $! > lab/<slug>/job-<name>.pid
```

Then per tick: check the log tail + checkpoint progress (seconds), do OTHER
work (plan analysis, notebook, next experiment design, content lane) while it
runs, and harvest results when done. A tick that only babysits a running job
is a wasted tick.

Requirements for every batch job:
- **Checkpointing mandatory**: append results incrementally (JSONL/g6 slices)
  so a dead sandbox costs minutes, not hours. Resume must skip completed
  slices (you built this for the census — reuse it, never regress).
- **PID + log discipline**: every background job has a .pid and a .log in the
  lab dir; the state ledger lists running jobs so a fresh session can find
  them (or restart them from checkpoints if the sandbox died).
- Commit checkpoint outputs to main at heartbeat boundaries like everything
  else — a checkpoint that only lives in /tmp does not exist. Keep raw bulk
  outputs in lab/<slug>/data/, compress if large.

Why this matters beyond the timeout: foreground mega-commands make the
session LOOK stuck to humans watching the dashboard, hide progress, and
block heartbeat folding. Background + short ticks = visible progress,
resumable state, calm operators.
