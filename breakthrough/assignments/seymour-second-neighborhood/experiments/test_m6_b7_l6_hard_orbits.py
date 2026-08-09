#!/usr/bin/env python3
"""Exhaustive hard-orbit cover, CNF, hash, and attribution regression."""

import gc
import hashlib
import tempfile
from pathlib import Path

import check_m6_b7_l6_hard_orbits as checker
import m6_b7_l6_hard_orbits as producer

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "m6-b7-l6-hard-orbits.tsv"


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


producer_leaves = producer.load_leaves()
checker_leaves = checker.derive_leaves()
if [(x[0], x[1], x[4], [(a, c) for a, c, _ in x[6]]) for x in producer_leaves] != [
        (x[0], x[1], x[4], [(a, c) for a, c, _ in x[6]]) for x in checker_leaves]:
    raise RuntimeError("producer and labelled-S7 checker orbit covers differ")
manifest = producer.manifest_payload(producer_leaves)
if manifest != checker.manifest_payload(checker_leaves) or manifest != MANIFEST.read_bytes():
    raise RuntimeError("producer/checker/frozen hard-orbit manifests differ")
print("PASS independent labelled S7 cover: 19 hard states, 170 incidences, 42 orbits, 392 incidences")

with tempfile.TemporaryDirectory(prefix="m6-b7-l6-hard-orbits-", dir=HERE.parent) as directory:
    directory = Path(directory)
    generated, retained = {}, None
    expected = checker.load_hashes()
    for ordinal, leaf in enumerate(producer_leaves):
        cnf, selectors = producer.build_leaf(leaf)
        path = directory / "leaf.cnf"
        producer.write_leaf(path, ordinal, leaf, cnf, selectors, manifest)
        generated[leaf[0]] = hashlib.sha256(path.read_bytes()).hexdigest()
        variables, clauses, members, checked_selectors = checker.check(path)
        if ordinal == 0:
            retained = (path.read_bytes(), variables, clauses, members, checked_selectors)
        path.unlink()
        del cnf, selectors, variables, clauses, members, checked_selectors
        gc.collect()
    if generated != expected:
        raise RuntimeError("generated hard-orbit CNFs differ from complete hash ledger")
    print("PASS emitted, independently checked, and hashed all 42 CNFs with 14 forced C-B arcs")

    raw, variables, _, members, selectors = retained
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
    if selected != 0 or any(checked[names[f"h_{a}_{b}"]] != ((a, b) in holes) for a, b in checker.PAIRS):
        raise RuntimeError("complete model attribution selected the wrong parent")
    reject(lambda: checker.validate_model(variables, tautologies, complete[:-1], selectors), "partial model")
    multiple = complete.copy(); multiple[selectors[1] - 1] = selectors[1]
    reject(lambda: checker.validate_model(variables, tautologies, multiple, selectors), "multiple selectors")
    print("PASS complete-model exact-one-selector attribution mutations")

    def mutate(label, predicate, replacement):
        lines = raw.decode("ascii").splitlines()
        index = next(i for i, line in enumerate(lines) if predicate(line))
        lines[index] = replacement(lines[index])
        target = directory / f"bad-{label}.cnf"
        target.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(target), label)

    mutate("intersection", lambda line: line.startswith("c intersection-t "), lambda _: "c intersection-t 9")
    mutate("subset", lambda line: line.startswith("c C16-subset "), lambda _: "c C16-subset 9")
    mutate("arc", lambda line: line == "-" + str(names["a_16_9"]) + " 0", lambda _: "1 0")
    mutate("selector", lambda line: "b7_l6_hard_orbit_selector_00" in line,
           lambda line: line.rsplit(" ", 1)[0] + " wrong")
    print("PASS hostile intersection/subset/arc/selector mutations")

print("PASS m6 B7-l6 hard subset-intersection orbit tests")
