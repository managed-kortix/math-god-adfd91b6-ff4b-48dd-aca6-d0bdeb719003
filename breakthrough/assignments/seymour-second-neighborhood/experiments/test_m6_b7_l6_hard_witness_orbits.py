#!/usr/bin/env python3
"""Exhaustive robust-witness orbit cover, CNF, hash, and mutation tests."""

import gc
import hashlib
import tempfile
from pathlib import Path

import check_m6_b7_l6_hard_witness_orbits as checker
import m6_b7_l6_hard_witness_orbits as producer

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "m6-b7-l6-hard-witness-orbits.tsv"


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


produced = producer.load_leaves()
checked = checker.derive_leaves()
projection = lambda leaf: (leaf[0], leaf[1], leaf[3], leaf[4], leaf[5],
                           [(a, c) for a, c, _ in leaf[2][6]])
if list(map(projection, produced)) != list(map(projection, checked)):
    raise RuntimeError("producer and explicit-S7 checker witness covers differ")
manifest = producer.manifest_payload(produced)
if manifest != checker.manifest_payload(checked) or manifest != MANIFEST.read_bytes():
    raise RuntimeError("producer/checker/frozen witness manifests differ")
print("PASS independent fixed-subset stabilizer cover: 28 TIMEOUTs, 252 incidences, 117 witness leaves, 1066 incidences")

with tempfile.TemporaryDirectory(prefix="m6-hard-witness-test-", dir=HERE.parent) as directory:
    directory = Path(directory)
    expected, generated, retained = checker.load_hashes(), {}, None
    for ordinal, leaf in enumerate(produced):
        cnf, selectors = producer.build_leaf(leaf)
        path = directory / "leaf.cnf"
        producer.write_leaf(path, ordinal, leaf, cnf, selectors, manifest)
        generated[leaf[0]] = hashlib.sha256(path.read_bytes()).hexdigest()
        checker.check(path)
        if ordinal == 0:
            retained = path.read_bytes()
        path.unlink()
        del cnf, selectors
        gc.collect()
    if generated != expected:
        raise RuntimeError("generated witness CNFs differ from complete hash ledger")
    print("PASS emitted, independently checked, and hashed all 117 witness CNFs")

    def mutate(label, predicate, replacement):
        lines = retained.decode("ascii").splitlines()
        index = next(i for i, line in enumerate(lines) if predicate(line))
        lines[index] = replacement(lines[index])
        path = directory / f"bad-{label}.cnf"
        path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(path), label)

    mutate("witness", lambda line: line.startswith("c ordered-witnesses "),
           lambda _: "c ordered-witnesses 9")
    mutate("orbit-size", lambda line: line.startswith("c labelled-witness-orbit-size "),
           lambda _: "c labelled-witness-orbit-size 999")
    mutate("cover", lambda line: line.startswith("c existential-cover "),
           lambda _: "c existential-cover disjoint")
    mutate("unit", lambda line: line.startswith("c var ") is False and line.endswith(" 0") and
           len(line.split()) == 2, lambda _: "1 0")
    print("PASS hostile witness/orbit-size/cover/unit mutations")

print("PASS m6 B7-l6 hard robust-witness orbit tests")
