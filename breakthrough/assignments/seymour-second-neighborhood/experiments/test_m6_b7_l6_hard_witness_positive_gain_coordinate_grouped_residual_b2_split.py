#!/usr/bin/env python3
"""Regeneration and hostile tests for the exact grouped B2 split."""

import hashlib
import json
import tempfile
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual_b2_split as checker
import m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual_b2_split as producer


def reject(call, label):
    try:
        call()
    except (RuntimeError, ValueError, UnicodeError, IndexError):
        return
    raise RuntimeError(f"hostile B2 split mutation accepted: {label}")


checker.check_partition()
items = producer.children()
manifest = producer.manifest_payload(items)
hashes = checker.load_hashes()
with tempfile.TemporaryDirectory(prefix="m6-grouped-b2-test-", dir=producer.HERE.parent) as directory:
    directory = Path(directory)
    samples = {}
    for ordinal, child in enumerate(items):
        path = directory / f"child-{ordinal:02d}.cnf"
        cnf, selectors = producer.build_child(child)
        producer.write_child(path, ordinal, child, cnf, selectors, manifest)
        if producer.identity(path) != hashes[ordinal]:
            raise RuntimeError(f"regenerated split child differs: {ordinal:02d}")
        checker.check_identity(path, ordinal)
        if ordinal in (0, 2, 26):
            checker.check(path)
        samples[ordinal] = path.read_bytes()

    def mutate(ordinal, label, predicate, replacement):
        lines = samples[ordinal].decode("ascii").splitlines()
        index = next(i for i, line in enumerate(lines) if predicate(line))
        lines[index] = replacement(lines[index])
        path = directory / f"bad-{label}.cnf"
        path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(path), label)

    mutate(0, "split-polarity", lambda line: line == "4691 0", lambda _: "-4691 0")
    mutate(1, "split-variable", lambda line: line == "-4691 0", lambda _: "-4692 0")
    mutate(0, "path-arc", lambda line: line.startswith("c path-x-arcs "), lambda line: line + ",hostile")
    mutate(0, "selector-guard", lambda line: line.startswith("-23617 ") and len(line.split()) == 3,
           lambda line: line[1:])

    checker.check_scout()
    scout_bytes = checker.SCOUT.read_bytes()
    scout = json.loads(scout_bytes.decode("ascii"))

    def mutate_scout(label, mutation, require_frozen_identity=False):
        hostile = json.loads(scout_bytes.decode("ascii"))
        mutation(hostile)
        path = directory / f"bad-{label}.json"
        path.write_text(json.dumps(hostile, sort_keys=True, indent=2) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check_scout(path, require_frozen_identity), label)

    mutate_scout("scout-status", lambda payload: payload["rows"][0].update(status="SAT", seconds=1.0))
    mutate_scout("scout-bool-seconds", lambda payload: payload["rows"][0].update(seconds=True))
    mutate_scout("scout-timeout-seconds", lambda payload: payload["rows"][0].update(seconds=19.999))
    mutate_scout("scout-row-hash", lambda payload: payload["rows"][0].update(cnf_sha256="0" * 64))
    frozen_mutation = directory / "bad-scout-frozen-identity.json"
    frozen_mutation.write_bytes(scout_bytes.replace(b'"seconds": 20.006', b'"seconds": 20.007', 1))
    reject(lambda: checker.check_scout(frozen_mutation), "scout-frozen-identity")
print("PASS grouped B2 split: 15 sources, 30 exact disjoint children, selectors preserved, hostile CNF/scout mutations")
