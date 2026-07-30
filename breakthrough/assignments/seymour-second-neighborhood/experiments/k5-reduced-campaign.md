# Common reduced k=5 certificate campaign

The rows `(rho,k)=(0,5)` and `(1,5)` both project to the common 16-vertex
model proved in `attempts/tick47-k5-common-reduction.md`. The complete
source-cut/packet cover has 931 semantic orbits and labelled multiplicity
758,181. Its payload SHA-256 is
`020cbf130cd806d3a91fa11a29dfdbae67e89e97a47d6e1708c10f3a9f45deb5`.

Every leaf is certified UNSAT in the concatenation of
`../certificates/k5-reduced-campaign.tar.xz.part-*`:

- Archive SHA-256:
  `d3f845d980390cac63930b8b7228eba295dbb598f6d261148aab22cf137c0f1d`.
- Archive bytes: 120,197,280.
- Referenced uncompressed LRAT bytes: 917,003,695.
- CaDiCaL 1.7.3 source commit:
  `38e073b389a877b0a0d3c91136d2443ab95fdeba`.
- `lrat-check` source commit:
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

Fresh verification:

```sh
mkdir -p /tmp/k5-reduced
cat ../certificates/k5-reduced-campaign.tar.xz.part-* > /tmp/k5-reduced.tar.xz
tar -xJf /tmp/k5-reduced.tar.xz \
  -C /tmp/k5-reduced --strip-components=1
mkdir -p /tmp/k5-reduced/work
python3 check_k5_reduced_cuts.py
python3 k5_reduced_verify.py \
  --root /tmp/k5-reduced \
  --checker /path/to/pinned/lrat-check
```

Expected final lines:

```text
PASS keys=931 labelled=758181 sha256=020cbf130cd806d3a91fa11a29dfdbae67e89e97a47d6e1708c10f3a9f45deb5
PASS leaves=931 labelled=758181
```

This closes only the two final isolated-root `m=9,k=5` aggregate rows under
their written reduction. It is not a proof of SNC by itself.
