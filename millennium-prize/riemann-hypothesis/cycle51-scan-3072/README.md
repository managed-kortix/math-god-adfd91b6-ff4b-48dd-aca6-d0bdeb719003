# Cycle 51 certified local scan through checkpoint 3072

Scope: finite 192-bit Arb certification only. No asymptotic theorem or RH claim.

The four certificate streams cover local cells `2304..3071`; the terminal
checkpoint contains `P_3072`. Each adjacent leg resumes from the preceding
checkpoint. Run from `millennium-prize/riemann-hypothesis`:

```text
uv run --with python-flint python cycle41_local_scan.py \
  --max-N 2368 --bits 192 --jobs 2 --chunk-size 1 \
  --resume-from cycle42-checkpoint-2304.json \
  --checkpoint cycle51-scan-3072/checkpoint-2368.json \
  --output-dir /tmp/rh-scan-2368

uv run --with python-flint python cycle41_local_scan.py \
  --max-N 2560 --bits 192 --jobs 2 --chunk-size 1 \
  --resume-from cycle51-scan-3072/checkpoint-2368.json \
  --checkpoint cycle51-scan-3072/checkpoint-2560.json \
  --output-dir /tmp/rh-scan-2560

uv run --with python-flint python cycle41_local_scan.py \
  --max-N 2816 --bits 192 --jobs 2 --chunk-size 1 \
  --resume-from cycle51-scan-3072/checkpoint-2560.json \
  --checkpoint cycle51-scan-3072/checkpoint-2816.json \
  --output-dir /tmp/rh-scan-2816

uv run --with python-flint python cycle41_local_scan.py \
  --max-N 3072 --bits 192 --jobs 2 --chunk-size 1 \
  --resume-from cycle51-scan-3072/checkpoint-2816.json \
  --checkpoint cycle51-scan-3072/checkpoint-3072.json \
  --output-dir /tmp/rh-scan-3072
```

Uncompressed certificate SHA-256 hashes:

```text
2304..2367  31d7174dfba2335582b3937ffaf5926ecebad4a927c84e9337d7656c4db39c73
2368..2559  311fc348e68be59d79bcdec605ea1728d1ecceb5d08359cbc64dbe31dd2e5c49
2560..2815  e9e1d65418f4b371b74e827508d47f038d7f60f44101a5c4af425091ecf50918
2816..3071  75a8e6302d4a196ffcbab842f7a48c13324f73086ebcb625f87d61fbdb0322ae
```

Environment used for independent reproduction: Python 3.12.13,
python-flint 0.9.0. Gzip container hashes may vary because gzip records
metadata; compare the uncompressed JSONL streams.
