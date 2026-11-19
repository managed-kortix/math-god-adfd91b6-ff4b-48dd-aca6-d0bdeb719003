# Frozen grouped `q` split audit

## Scope

This audits the proposed `q`/`not q` split only for grouped leaves `000`,
`022`, `038`, `065`, and `128`. It does not change or extend any frozen
campaign claim.

## Encoding semantics

In `snc_cnf.py`, `q_w_d` is the exact-second-neighbor indicator:

```
q_w_d <-> r_w_d AND NOT a_w_d,
```

where `r_w_d` says that at least one directed two-walk from `w` to `d`
exists. In particular, the base CNF contains

```
(-q_w_d OR -a_w_d).
```

The robust-witness encoding contains

```
(-wit_w_d OR a_w_d).
```

Every frozen coordinate leaf fixes its listed robust witness with the unit
clause `wit_w_d`. Therefore unit propagation gives `a_w_d`, then `NOT q_w_d`.
Equivalently, resolving the two displayed clauses gives
`(-wit_w_d OR -q_w_d)`.

The five grouped leaves inherit these exact witness units unchanged:

| grouped leaf | key | witness `w` | deleted `d` | forced implication |
|---:|---|---:|---:|---|
| `000` | `o00-w00-c17` | 13 | 17 | `wit_13_17 -> a_13_17 -> not q_13_17` |
| `022` | `o04-w00-c17` | 13 | 17 | `wit_13_17 -> a_13_17 -> not q_13_17` |
| `038` | `o11-w00-c16` | 11 | 16 | `wit_11_16 -> a_11_16 -> not q_11_16` |
| `065` | `o15-w00-c17` | 13 | 17 | `wit_13_17 -> a_13_17 -> not q_13_17` |
| `128` | `o36-w00-c17` | 11 | 17 | `wit_11_17 -> a_11_17 -> not q_11_17` |

This is also the intended graph semantics: the witness condition requires the
arc `w -> d`, while an exact second neighbor is explicitly outside the first
neighborhood of `w`.

## Decision

The proposed positive-`q` child is propositionally inconsistent in every one
of the five sources. Thus `q`/`not q` is formally exhaustive and disjoint, but
it is not a genuine nontrivial partition: the positive side is empty and the
negative side is already implied by the source.

Do not create a ten-child campaign, hashes, scout, or certificates for this
split. The direct simplification is to close each positive-`q` branch by the
two-clause implication above and identify each negative-`q` branch with its
unchanged source CNF. Adding an explicit `-q_w_d` unit would be sound but
redundant because ordinary unit propagation already derives it. Any useful
next split must use an atom not fixed by the robust-witness and exact-second
linkage.
