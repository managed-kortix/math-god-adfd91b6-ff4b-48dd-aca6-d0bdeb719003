# Certificate fragment cleanup

Cleanup on 2026-08-14 used
`python3 scripts/cleanup_superseded_certificate_fragments.py --apply`.
The script is an allowlist, requires each fragment directory's merged output to
be a committed file, and refuses to remove a directory or output currently open
by another process.

## Removed as superseded

- All listed R10 checkpoint directories from residual 50000 through 125457.
  Their complete merged `chunk-*.r10g.xz` packs and authenticated search
  manifest are committed. The merge routine validates every canonical fragment,
  concatenates its record body, validates the result, and atomically writes the
  merged pack.
- All listed R7 order-seven checkpoint directories. Decoding established that
  the sampled complete and overlapping prefixes through row 32000 equal the
  corresponding records in the eight committed canonical packs: 33000 decoded
  fragment rows, zero mismatches. The remaining fragment ranges are covered by
  the same merge validation and authenticated committed manifest; overlapping
  legacy ranges map to the canonical 25000--29000, 29000--32000,
  32000--35000, 35000--38000, and 38000--40964 packs.
- The complete R7 order-eight 000000--005000 checkpoint directory. Its merged
  pack is committed and is pinned by SHA-256 in
  `rank7_order8_exact_gram_library_coverage.json`.
- Untracked `paper.aux`, `paper.log`, `paper.out`, `paper.fls`, and
  `paper.fdb_latexmk` products in the two explicitly listed paper directories.

## Preserved

- R7 order-eight fragment directories beginning at 005000, 010000, 015000,
  and 020000 are incomplete and have no committed merged packs. They remain as
  restart checkpoints.
- Committed merged packs, manifests, logs, exact verifiers, census artifacts,
  and proof documents are never cleanup targets.
- PID files and every path associated with an active process are outside the
  cleanup allowlist.

Thus no unique certificate record or proof input is removed: deleted fragments
are byte-decodable records already represented by committed merged packs, while
the only fragments not yet represented by merged packs are retained.
