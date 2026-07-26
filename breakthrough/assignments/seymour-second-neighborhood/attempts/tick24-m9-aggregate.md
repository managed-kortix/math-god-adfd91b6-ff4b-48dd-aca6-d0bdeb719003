# Tick 24: aggregate campaign for nine missing pairs

At `n=18,m=9`, all vertices have outdegree eight. If the missing graph has no
isolate, its average degree one forces it to be a perfect matching, already
human-eliminated. Otherwise choose a missing-isolated vertex `z`. A robust
deletion witness `w->z` has rooted layers `|A|=8,|B|=7,|C|=2`, with `z in A`.

For `rho=e(C,B)`, the two C-row degree equations give

```
p=rho+3, e=6-rho, 0<=rho<=6.
```

If `k` of the residual holes lie in `T={w} union A union B`, the other
`6-rho-k` lie between B and C. Hence

```
0<=k<=6-rho,
```

giving 28 disjoint exhaustive aggregate shards. No missing-graph shape is fixed.
The deterministic emitter is `experiments/m9_isolate_shards.py`.

Pilot runs independently LRAT-verified several low-k shards, while unshaped
high-k shards timed out and require structural subdivision. An UNKNOWN shard
has no mathematical force. The next sound split is by missing-degree sequence
and colored high-degree core, or by simultaneous robust-zone overlap among
multiple isolates.
