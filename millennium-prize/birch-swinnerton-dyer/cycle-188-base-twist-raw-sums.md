# Cycle 188: exact raw base-twist sums for the first `[1:5]` pair

For `E=433a1`, `p=7`, `ell=29`, and `eta=2`, the Cycle 187 formula was
evaluated exactly in PARI/GP for the first same-`L_0`-class pair
`q=1499,6287`. Both primes are `3 mod 4`, so the calculation uses the base
minus symbol returned by `msfromell(E,-1)` and the positive odd-character sign
of (187.9).

The complete 56 rational values are in `cycle188_base_twist_sums.tsv`. Writing

```text
U_a(q) = sum_{u=1}^{q-1} (u/q) [(aq+29u)/(29q)]^-_E,
T_a(q) = kappa_q U_a(q),
```

the independent exact verifier obtains

```text
q=1499: full integer-log lift = -150; shortened (187.5) lift = 365/2;
        c(q,29)=4 mod 7
q=6287: full integer-log lift = -1616; shortened (187.5) lift = -733/2;
        c(q,29)=1 mod 7
```

The two raw rational lifts differ by multiples of seven because (187.5) uses
the displayed least nonnegative coefficients after pairing; both reduce to the
same pinned `c(q,29)`.

Thus both coordinates are **nonzero**. They do not form a zero/nonzero
collision, although their exact residues differ under the pinned conventions.

For each twist PARI gives the global-minimal change `[u,r,s,t]` as
`[1,125,1,63]` at `1499` and `[1,524,1,262]` at `6287`. The differential scale
is therefore `u=1`, so the positive rational factor in (187.2) is
`kappa_q=1` for both generated global minimal models. More generally, scaling
all rows at one `q` by a 7-adic unit can change the displayed nonzero residue
but cannot change zero versus nonzero.

Reproduce and verify with

```sh
gp -q millennium-prize/birch-swinnerton-dyer/cycle188_433a1_base_twist_sums.gp
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle188_base_twist_sums.py
sha256sum -c millennium-prize/birch-swinnerton-dyer/cycle188_SHA256SUMS
```
