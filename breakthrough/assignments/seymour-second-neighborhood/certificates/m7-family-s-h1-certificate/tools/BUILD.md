# Pinned toolchain

The default verifier uses only package-local `drat-trim`; it does **not** run a
SAT solver. Package-local CaDiCaL is retained solely for the separate optional
proof-reproduction command.

## drat-trim

Pinned upstream identity:

```text
repository     https://github.com/marijnheule/drat-trim.git
commit         2e3b2dc0ecf938addbd779d42877b6ed69d9a985
tree           b4e75a5f8c89d664652727458369cb5e0b610e31
source blob    cf8a676ffcc7ef5a47124bbafc9b680a2df333e0
source bytes   59,546
source SHA-256 d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee
binary bytes   51,216
binary SHA-256 92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a
ELF build ID   83768248f9562e7a5b87b8530e078148fe0b62a6
compiler       gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
```

The source-path spelling affects the ELF build ID. Reproduce the exact binary
from a checkout whose current directory contains `drat-trim.c`; do not pass an
absolute source pathname:

```bash
cd drat-trim-checkout
test "$(git rev-parse HEAD)" = 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
test "$(git rev-parse HEAD^{tree})" = b4e75a5f8c89d664652727458369cb5e0b610e31
sha256sum drat-trim.c
gcc drat-trim.c -std=c99 -O2 -o drat-trim
sha256sum drat-trim
```

Expected source and binary hashes are the values above. The compile emits a
known `getc_unlocked` declaration warning under strict C99; the retained binary
is nevertheless reproduced byte-for-byte on the pinned compiler/platform.
`drat-trim-LICENSE` is the retained upstream license.

## CaDiCaL

```text
name           CaDiCaL 1.7.3
source commit  38e073b389a877b0a0d3c91136d2443ab95fdeba
binary bytes   1,002,216
binary SHA-256 ff471d3c6b54fbbc161d65545a5f788d0032ad05b9aff4e2c748d9639400e951
ELF build ID   560ab92678327747ed4dae62010a6481075fe9b5
```

`cadical-LICENSE` is the retained upstream license. To reproduce the proof with
the package-local pinned binary, run:

```bash
python3 -O -B verifier/reproduce_proof.py
```

The verifier rejects any other solver bytes; `--solver` may point to a
byte-identical copy. Both retained executables target GNU/Linux x86-64 with
glibc. They are not claimed portable to macOS, Windows, musl, or another
architecture.
