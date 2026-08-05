#!/usr/bin/env python3
"""Exhaustive cover, CNF hashes, attribution, and hostile state mutations."""

import gc
import hashlib
import tempfile
from pathlib import Path

import check_m6_b7_l6_state_split as checker
import m6_b7_l6_state_split as producer

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "m6-b7-l6-state-split.tsv"
HASHES = HERE / "m6-b7-l6-state-leaf-hashes.tsv"


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


producer_leaves = producer.load_leaves()
checker_leaves = checker.derive_leaves()
producer_members = [[(a, c) for a, c, _ in leaf[2]] for leaf in producer_leaves]
checker_members = [[(a, c) for a, c, _ in leaf[2]] for leaf in checker_leaves]
if producer_members != checker_members:
    raise RuntimeError("producer/checker state incidence streams differ")
producer_manifest = producer.manifest_payload(producer_leaves)
checker_manifest = checker.manifest_payload(checker_leaves)
if not (producer_manifest == checker_manifest == MANIFEST.read_bytes()):
    raise RuntimeError("producer/checker/frozen manifests differ")
if (len(producer_manifest), hashlib.sha256(producer_manifest).hexdigest()) != (
        producer.MANIFEST_BYTES, producer.MANIFEST_SHA256):
    raise RuntimeError("manifest fingerprint changed")
if (HASHES.stat().st_size, hashlib.sha256(HASHES.read_bytes()).hexdigest()) != (
        checker.HASH_BYTES, checker.HASH_SHA256):
    raise RuntimeError("leaf hash ledger fingerprint changed")
print("PASS independent exact cover: 42 parents, 260 incidences, 30 state leaves")

with tempfile.TemporaryDirectory(prefix="m6-b7-l6-state-", dir=HERE.parent) as directory:
    directory = Path(directory)
    generated = {}
    retained = None
    expected_hashes = checker.load_hashes()
    if set(expected_hashes) != {leaf[0] for leaf in producer_leaves}:
        raise RuntimeError("hash ledger does not cover exactly 30 leaves")
    for ordinal, leaf in enumerate(producer_leaves):
        cnf, shapes, selectors = producer.build_leaf(leaf[1], leaf[2])
        path = directory / "leaf.cnf"
        producer.write_leaf(path, ordinal, leaf, cnf, shapes, selectors, producer_manifest)
        generated[leaf[0]] = hashlib.sha256(path.read_bytes()).hexdigest()
        if generated[leaf[0]] != expected_hashes[leaf[0]]:
            raise RuntimeError(f"frozen CNF hash changed for {leaf[0]}")
        variables, clauses, members, checked_selectors = checker.check(path)
        if ordinal == 0:
            retained = (path.read_bytes(), variables, clauses, members, checked_selectors)
        path.unlink()
        del cnf, shapes, selectors, variables, clauses, members, checked_selectors
        gc.collect()
    if generated != expected_hashes:
        raise RuntimeError("generated hashes differ from complete ledger")
    print("PASS emitted, independently checked, dimensioned, and hashed all 30 CNFs")

    raw, variables, _, members, selectors = retained
    path = directory / "leaf.cnf"
    path.write_bytes(raw)
    tautologies = [(number, -number) for number in range(1, len(variables) + 1)]
    values = {number: True for number in range(1, len(variables) + 1)}
    for selector in selectors:
        values[selector] = selector == selectors[0]
    holes = checker.expected_projection(members[0][2])[1]
    names = {name: number for number, name in enumerate(variables, 1)}
    for pair in checker.PAIRS:
        values[names[f"h_{pair[0]}_{pair[1]}"]] = pair in holes
    complete = [number if values[number] else -number for number in range(1, len(variables) + 1)]
    checked, selected = checker.validate_model(variables, tautologies, complete, selectors)
    if selected != 0 or any(checked[names[f"h_{a}_{b}"]] != ((a, b) in holes)
                            for a, b in checker.PAIRS):
        raise RuntimeError("complete attribution selected the wrong parent")
    reject(lambda: checker.validate_model(variables, tautologies, complete[:-1], selectors), "partial model")
    multiple = complete.copy(); multiple[selectors[1] - 1] = selectors[1]
    reject(lambda: checker.validate_model(variables, tautologies, multiple, selectors), "multiple selectors")
    print("PASS complete-model exact-one-selector attribution mutations")

    def mutate(label, predicate, replacement, clause_delta=0):
        lines = raw.decode("ascii").splitlines()
        index = next(i for i, line in enumerate(lines) if predicate(line))
        lines[index] = replacement(lines[index])
        if clause_delta:
            header = next(i for i, line in enumerate(lines) if line.startswith("p cnf "))
            fields = lines[header].split(); fields[3] = str(int(fields[3]) + clause_delta)
            lines[header] = " ".join(fields)
        target = directory / f"bad-{label}.cnf"
        target.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(target), label)

    mutate("h-vector", lambda line: line.startswith("c h-vector "), lambda _: "c h-vector 9,9")
    mutate("internal", lambda line: line.startswith("c internal-C "), lambda _: "c internal-C 16>17")
    mutate("high-mask", lambda line: line.startswith("c high-mask "), lambda _: "c high-mask 11")
    mutate("per-c-count", lambda line: line.startswith("c C16-to-B "), lambda _: "c C16-to-B 7")
    header = raw.decode("ascii").splitlines().index(next(line for line in raw.decode("ascii").splitlines()
                                                     if line.startswith("p cnf ")))
    mutate("base", lambda line: line == raw.decode("ascii").splitlines()[header + 1], lambda _: "-2 0")
    mutate("selector-name", lambda line: "b7_l6_parent_selector_00" in line, lambda line: line.rsplit(" ", 1)[0] + " wrong")
    print("PASS hostile h-vector/internal/high-mask/per-C/base/selector mutations")

print("PASS m6 B7-l6 exact state split tests")
