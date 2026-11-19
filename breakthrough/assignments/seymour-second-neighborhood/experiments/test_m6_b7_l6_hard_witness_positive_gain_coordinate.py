#!/usr/bin/env python3
"""Complete coordinate-cover, hash, binding, and hostile mutation tests."""

import gc
import hashlib
import tempfile
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain_coordinate as checker
import m6_b7_l6_hard_witness_positive_gain_coordinate as producer


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError, IndexError):
        return
    raise RuntimeError(f"hostile coordinate mutation accepted: {label}")


produced = producer.load_leaves()
checked = checker.derive_children()
projection = lambda child: (child[0], child[1], child[2], child[3], child[4][0],
                            [(a, c) for a, c, _ in child[4][2][6]])
if list(map(projection, produced)) != list(map(projection, checked)):
    raise RuntimeError("producer and independent checker coordinate covers differ")
manifest = producer.manifest_payload(produced)
if manifest != checker.manifest_payload(checked) or manifest != checker.MANIFEST_PATH.read_bytes():
    raise RuntimeError("producer/checker/frozen coordinate manifests differ")
checker.check_cover()
checker.check_scout()

with tempfile.TemporaryDirectory(prefix="m6-positive-coordinate-test-", dir=producer.HERE.parent) as directory:
    directory = Path(directory)
    expected, generated, retained = checker.load_hashes(manifest), {}, None
    for ordinal, child in enumerate(produced):
        cnf, selectors = producer.build_leaf(child)
        path = directory / "leaf.cnf"
        producer.write_leaf(path, ordinal, child, cnf, selectors, manifest)
        generated[producer.child_key(child)] = hashlib.sha256(path.read_bytes()).hexdigest()
        checker.check(path)
        if ordinal == 0:
            retained = path.read_bytes()
        path.unlink()
        del cnf, selectors
        gc.collect()
    if generated != expected:
        raise RuntimeError("generated coordinate CNFs differ from complete hash ledger")
    print("PASS emitted, independently reconstructed, and hashed all 219 coordinate CNFs")

    def mutate(label, predicate, replacement):
        lines = retained.decode("ascii").splitlines()
        index = next(i for i, line in enumerate(lines) if predicate(line))
        lines[index] = replacement(lines[index])
        path = directory / f"bad-{label}.cnf"
        path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(path), label)

    def alo(line):
        fields = line.split()
        return len(fields) == 17 and fields[-1] == "0" and all(not item.startswith("-") for item in fields[:-1])

    mutate("omitted-coordinate-literal", alo, lambda line: " ".join(line.split()[1:]))
    mutate("wrong-polarity", alo, lambda line: "-" + line)
    mutate("wrong-coordinate", lambda line: line.startswith("c coordinate "), lambda _: "c coordinate 1")
    mutate("wrong-deletion", lambda line: line.startswith("c deleted "), lambda _: "c deleted 16")
    mutate("wrong-witness", lambda line: line.startswith("c witness "), lambda _: "c witness 15")
    mutate("wrong-source", lambda line: line.startswith("c source-leaf-ordinal "),
           lambda _: "c source-leaf-ordinal 1")
    mutate("wrong-scout-binding", lambda line: line.startswith("c positive-gain-scout-sha256 "),
           lambda line: line[:-1] + ("0" if line[-1] != "0" else "1"))
    mutate("wrong-cert-binding", lambda line: line.startswith("c positive-gain-certificate-ledger-sha256 "),
           lambda line: line[:-1] + ("0" if line[-1] != "0" else "1"))
    print("PASS hostile omitted-coordinate/polarity/coordinate/deletion/witness/source/scout/cert mutations")

    scout = checker.SCOUT_PATH.read_bytes()
    bad_scout = directory / "bad-scout.json"
    bad_scout.write_bytes(scout.replace(b'"status": "UNSAT"', b'"status": "TIMEOUT"', 1))
    reject(lambda: checker.check_scout(bad_scout), "scout-status")
    print("PASS hostile scout status mutation")

print("PASS m6 B7-l6 positive-gain deletion-coordinate tests")
