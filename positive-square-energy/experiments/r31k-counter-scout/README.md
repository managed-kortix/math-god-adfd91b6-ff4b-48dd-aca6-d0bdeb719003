# R31-K finite counterexample scout bundle

Preserved: 2026-11-19 UTC
Target theorem note SHA-256:
`7e2d3a233cf05e9926c12b1740d075c422e26d2cd0a82939102755455da8a540`

This is a **nonpromotional finite corroboration bundle**, not a proof and not
an exhaustion of unbounded bridge lengths or arbitrary rooted-tree payloads.
It preserves the counterexample search and exact target certificates used to
audit the theorem note identified above.  No lane-state or publication file was
changed to produce these artifacts.

## Preserved payload SHA-256

```text
8c62f17e0e24cd8c0017f7e9e86bf5f9d1ae3bf60a6c0b11755f1262331f1071  r31k_scout.py
02d2d7cdaab3ff3cbc36e341911b1dc5bd6d6f986bec73e702d7a31d01ebf8ef  r31k_ledger_audit.py
0574b18bbf1475b302282db05ac46b1d57490b0579d56ae701ad37028aa111b6  ledger_b3.json
0ebde217434c16293ebd0cecbce0c77ba5e23a9a990b2c39787186a1997d0543  target_topology_minima_exact.json
```

`r31k_scout.py` requires Python, NumPy, and pynauty. Its exact-certificate
path also imports `research/shared_triangle_rooted_exact.py` from the target
repository (`--repo`, default `/workspace/repo`). When running from another
checkout, pass that checkout explicitly with `--repo`. The exact helper used in
the original run had SHA-256
`6fed7cdcd3fc17bcaf2ccf073b5e9f93ec6601ca383966fc69be52d8bd83e668`.
Observed environment: Python 3.12.13, NumPy 2.5.5, pynauty 2.8.8.1.

## Reproduce the preserved ledger

From the extracted directory, with its path on `PYTHONPATH` implicitly via the
current directory:

```sh
python r31k_ledger_audit.py --max-bridge 3 --output ledger_b3.replay.json
sha256sum ledger_b3.replay.json
```

Expected output SHA-256:
`0574b18bbf1475b302282db05ac46b1d57490b0579d56ae701ad37028aa111b6`.
The run enumerates 379,043 nauty-deduplicated cores formed from a literal K4
and the indicated four literal cycles, recursively attaching each cycle at any
existing vertex by a shared cut or by a bridge path of length 1, 2, or 3.

Expected counts:

```text
profile    graphs   Case I  Case II  Case III  distinct case records
T4          17,289    3,572        0    13,717                      5
T3C5        85,621   12,371    1,132    72,118                     13
T3C7       114,737   15,067    2,503    97,167                      9
T2C5C5     161,396   14,997    2,694   143,705                     23
TOTAL      379,043
violations: 0
```

This replay targets the three-case combinatorial ownership/ledger conditions,
including shared cuts, repeated cuts, nesting orders, mixed branches, and four
independent arms. It does not itself prove the imported spectral contracts.

## Reproduce a spectral census

Example full bridge-bound-3 census (large JSON output; exact-certifying the
closest row requires the repository helper):

```sh
python r31k_scout.py --max-bridge 3 --payload-extra 0 \
  --exact-keep 1 --repo /path/to/repo --output scout-b3.replay.json
```

To replay only floating spectra while still supplying a repository containing
the importable exact helper:

```sh
python r31k_scout.py --max-bridge 3 --payload-extra 0 \
  --exact-keep 1 --skip-exact --skip-rays --repo /path/to/repo \
  --output scout-b3-float.replay.json
```

Original bridge-bound-3 core counts and minimum floating values were:

```text
T4          17,289   10.389185421335437
T3C5        85,621    9.672290307921724
T3C7       114,737    9.891672904822919
T2C5C5     161,396    8.952317190839228
```

All 379,043 floating values were positive. The four listed global bare-core
minima occur already within bridge bound 2 and were certified by exact integer
characteristic polynomials plus rational Sturm isolation in the original run.
(The larger strict integer lower bounds 10, 9, 9, and 8, respectively, follow
from those exact intervals.)

## Reproduce `target_topology_minima_exact.json`

The artifact stores 11 targeted topology minima, each with canonical edges,
integer characteristic polynomial, multiplicity-aware positive-root intervals,
and a rational interval for `sigma = s^+(G)-|V(G)|`. Every lower endpoint is
strictly positive. It was generated from bridge-bound-2 cores by selecting the
minimum floating row in each applicable category:

- `four_independent_arms`: away-cycle groups `(1,1,1,1)`;
- `mixed_root_one`: exactly one cycle on the K4 root side;
- `root_all_no_direct_triangle`: all four cycles on the root side and no
  direct root triangle (not applicable to profile T4).

Reproduction pseudocode (uses public functions in `r31k_scout.py`):

```python
import json
from pathlib import Path
import r31k_scout as s

profiles = {
    'T4': (3,3,3,3), 'T3C5': (3,3,3,5),
    'T3C7': (3,3,3,7), 'T2C5C5': (3,3,5,5),
}
exact = s.load_exact_module(
    Path('/path/to/repo/research/shared_triangle_rooted_exact.py'))
out = {}
for name, profile in profiles.items():
    graphs, _ = s.generate_cores(profile, 2)
    targets = {}
    for g in graphs:
        z = s.topology_stats(g)
        labels = []
        if z['away_cycle_groups'] == (1,1,1,1):
            labels.append('four_independent_arms')
        if z['root_cycles'] == 1:
            labels.append('mixed_root_one')
        if z['root_cycles'] == 4 and z['direct_root_triangles'] == 0:
            labels.append('root_all_no_direct_triangle')
        value = s.sigma_float(g)[0]
        for label in labels:
            if label not in targets or value < targets[label][0]:
                targets[label] = (value, g)
    out[name] = {}
    for label, (value, g) in targets.items():
        cert, _, _ = s.exact_certificate(g, exact, 44)
        out[name][label] = {
            'record': s.graph_record(g, value), 'exact': cert}
Path('target_topology_minima_exact.replay.json').write_text(
    json.dumps(out, indent=2, sort_keys=True, default=list) + '\n')
```

Then:

```sh
sha256sum target_topology_minima_exact.replay.json
```

Expected SHA-256:
`0ebde217434c16293ebd0cecbce0c77ba5e23a9a990b2c39787186a1997d0543`.

## Verdict represented by these files

No counterexample was found in the finite scope above. In particular, the
ledger audit found no failure of the injection from potentially negative
away/opened pieces to distinct original nontriangles (`s <= h`) in the tested
physical block-cut trees. This is corroboration only; universal validity rests
on the analytic proof, not this finite search.
