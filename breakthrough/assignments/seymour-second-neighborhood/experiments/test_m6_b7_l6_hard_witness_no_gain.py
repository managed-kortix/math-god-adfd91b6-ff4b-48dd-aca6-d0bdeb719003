#!/usr/bin/env python3
"""Exhaustive exact no-gain CNF, hash, source-binding, and mutation tests."""

import gc
import hashlib
import json
import tempfile
from pathlib import Path

import check_m6_b7_l6_hard_witness_no_gain as checker
import m6_b7_l6_hard_witness_no_gain as producer

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "m6-b7-l6-hard-witness-no-gain.tsv"


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


produced = producer.load_leaves()
checked = checker.derive_leaves()
projection = lambda leaf: (leaf[0], leaf[1], leaf[3], leaf[4], [(a, c) for a, c, _ in leaf[2][6]])
if list(map(projection, produced)) != list(map(projection, checked)):
    raise RuntimeError("producer and independent checker source frontiers differ")
manifest = producer.manifest_payload(produced)
if manifest != checker.manifest_payload(checked) or manifest != MANIFEST.read_bytes():
    raise RuntimeError("producer/checker/frozen no-gain manifests differ")
counts = [len(producer.no_gain_paths(leaf)) for leaf in produced]
if set(counts) != {16, 32} or sum(count == 16 for count in counts) != 12 or sum(count == 32 for count in counts) != 105:
    raise RuntimeError("exact 16/32 no-gain unit census changed")
print("PASS bound 117-source frontier, 1066 incidences, and exact 16/32 negative-path units")
checker.check_scout()

with tempfile.TemporaryDirectory(prefix="m6-witness-no-gain-test-", dir=HERE.parent) as directory:
    directory = Path(directory)
    expected, generated, retained = checker.load_hashes(manifest), {}, None
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
        raise RuntimeError("generated no-gain CNFs differ from complete hash ledger")
    print("PASS emitted, independently reconstructed, and hashed all 117 no-gain CNFs")

    def mutate(label, predicate, replacement):
        lines = retained.decode("ascii").splitlines()
        index = next(i for i, line in enumerate(lines) if predicate(line))
        lines[index] = replacement(lines[index])
        path = directory / f"bad-{label}.cnf"
        path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(path), label)

    mutate("source-hash", lambda line: line.startswith("c witness-scout-sha256 "),
           lambda line: line[:-1] + ("0" if line[-1] != "0" else "1"))
    mutate("unit-count", lambda line: line.startswith("c negative-path-unit-clauses "),
           lambda _: "c negative-path-unit-clauses 32")
    mutate("gain-scope", lambda line: line.startswith("c gain-refinement-leaves "),
           lambda _: "c gain-refinement-leaves 2978")
    mutate("path-unit", lambda line: line.startswith("-") and len(line.split()) == 2,
           lambda line: line[1:])
    print("PASS hostile source/count/scope/path-unit mutations")

    scout = json.loads(checker.SCOUT_PATH.read_text(encoding="ascii"))

    def mutate_scout(label, change):
        changed = json.loads(json.dumps(scout))
        change(changed)
        path = directory / f"bad-scout-{label}.json"
        path.write_text(json.dumps(changed, sort_keys=True, indent=2) + "\n",
                        encoding="ascii", newline="\n")
        reject(lambda: checker.check_scout(path), label)

    def swap_statuses(payload):
        unsat = next(row for row in payload["rows"] if row["status"] == "UNSAT")
        timeout = next(row for row in payload["rows"] if row["status"] == "TIMEOUT")
        unsat["status"], timeout["status"] = timeout["status"], unsat["status"]

    mutate_scout("status-swap", swap_statuses)
    mutate_scout("solver-hash", lambda payload: payload.update(solver_sha256="0" * 64))
    mutate_scout("solver-bytes", lambda payload: payload.update(solver_bytes=1002217))
    mutate_scout("solver-version", lambda payload: payload.update(solver_version="1.7.4"))

    ledger_lines = checker.HASH_PATH.read_text(encoding="ascii").splitlines()

    def mutate_ledger(label, index, replacement):
        lines = list(ledger_lines)
        lines[index] = replacement(lines[index])
        path = directory / f"bad-ledger-{label}.tsv"
        path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.load_hashes(manifest, path), label)

    mutate_ledger("format", 0, lambda _: checker.HASH_FORMAT + "-hostile")
    mutate_ledger("header", 4, lambda line: line.replace("cnf-sha256", "sha256"))
    mutate_ledger("key", 5, lambda line: line.replace("o00-w00", "o00-w01"))
    mutate_ledger("uppercase-hex", 5, lambda line: line[:-64] + line[-64:].upper())
    mutate_ledger("extra-row-field", 5, lambda line: line + "\textra")
    print("PASS hostile status-swap/solver/hash-ledger format/header/key/hex/row mutations")

print("PASS m6 B7-l6 hard witness exact no-gain tests")
