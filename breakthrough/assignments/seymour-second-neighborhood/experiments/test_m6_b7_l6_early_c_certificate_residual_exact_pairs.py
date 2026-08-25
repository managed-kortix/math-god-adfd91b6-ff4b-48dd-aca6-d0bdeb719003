#!/usr/bin/env python3
"""Regression and hostile tests for certificate-relative exact-pair cells."""

import hashlib
import json
import tempfile
from pathlib import Path

import check_m6_b7_l6_early_c_certificate_residual_exact_pairs as checker
import m6_b7_l6_early_c_certificate_residual_exact_pairs as producer


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise AssertionError(f"hostile mutation accepted: {label}")


produced = producer.load_children()
checked = checker.derive()
project = lambda record: (record[0], record[1][0], record[1][1], record[1][3], record[1][5])
assert tuple(map(project, produced)) == tuple(map(project, checked))
assert len(produced) == 20
assert sum(len(record[1][5]) for record in produced) == checker.CELL_PARENT_MEMBERSHIPS
assert len({(record[1][1], parent) for record in produced for parent in record[1][5]}) == \
    checker.COMPATIBLE_PROFILE_PARENT_GRAPHS
manifest = producer.manifest_payload(produced)
assert manifest == checker.manifest_payload(checked) == checker.MANIFEST.read_bytes()
checker.check_exhaustion()

with tempfile.TemporaryDirectory(prefix="certificate-residual-test-", dir=producer.HERE.parent) as directory:
    directory = Path(directory)
    hashes = checker.load_hashes(manifest)
    shape_support_representatives = {}
    for cell, record in enumerate(produced):
        pair_shape = tuple("R" if vertex < 9 else "B" if vertex < 16 else "C"
                           for vertex in sorted(record[1][3]))
        shape_support_representatives.setdefault((pair_shape, len(record[1][5])), cell)
    assert len(shape_support_representatives) == 10

    retained = None
    for cell in sorted(shape_support_representatives.values()):
        path = directory / f"cell-{cell}.cnf"
        record = produced[cell]
        cnf, selectors = producer.build_child(record)
        producer.write_child(path, cell, record, cnf, selectors, manifest)
        assert (path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest()) == hashes[record[1][0]]
        checker.check(path)
        if cell == 0:
            retained = path.read_text(encoding="ascii")

        names, _, rebuilt_selectors = checker.reconstruct(checked[cell])
        child = checked[cell][1]
        low = checker.source.low_vertex(child[2][3])
        support = checker.source.parent_nonoutneighbors(
            child[2], child[2][7][child[5][0]][2])[1]
        positive = min(support - child[3])
        q = names.index(f"q_{low}_{positive}") + 1
        selector = rebuilt_selectors[child[5][0]]
        hostile = directory / f"bad-shape-support-{cell}.cnf"
        hostile.write_text(path.read_text(encoding="ascii").replace(
            f"-{selector} {q} 0", f"-{selector} -{q} 0", 1),
            encoding="ascii", newline="\n")
        reject(lambda hostile=hostile: checker.check(hostile),
               f"shape-support-class-{cell}")

    names, clauses, selectors = checker.reconstruct(checked[0])
    child = checked[0][1]
    low = checker.source.low_vertex(child[2][3])
    support = checker.source.parent_nonoutneighbors(child[2], child[2][7][child[5][0]][2])[1]
    positive = min(support - child[3])
    q = names.index(f"q_{low}_{positive}") + 1
    selector = selectors[child[5][0]]
    mutations = (
        retained.replace("c exact-inaccessible-pair 0,3", "c exact-inaccessible-pair 0,2", 1),
        retained.replace("c positive-q-clauses 7", "c positive-q-clauses 6", 1),
        retained.replace("c source-child 1", "c source-child 2", 1),
    )
    for index, text in enumerate(mutations):
        path = directory / f"bad-{index}.cnf"
        path.write_text(text, encoding="ascii", newline="\n")
        reject(lambda path=path: checker.check(path), f"CNF-{index}")

    original = checker.CERTIFICATES
    hostile = directory / "bad-certificates.tsv"
    hostile.write_bytes(original.read_bytes().replace(b"\n000\t", b"\n001\t", 1))
    saved = checker.CERTIFICATES
    checker.CERTIFICATES = hostile
    try:
        reject(checker.certificate_scope, "certificate-scope")
    finally:
        checker.CERTIFICATES = saved

    scout = json.loads(checker.SCOUT10.read_text(encoding="ascii"))
    scout["rows"][0]["status"] = "UNSAT"
    hostile_scout = directory / "bad-scout.json"
    hostile_scout.write_text(json.dumps(scout, sort_keys=True, indent=2) + "\n", encoding="ascii", newline="\n")
    reject(lambda: checker.check_scout(manifest, hashes, hostile_scout, require_frozen_identity=False),
           "scout-status")

print("PASS frozen B7-l6 certificate-relative exact-pair tests")
