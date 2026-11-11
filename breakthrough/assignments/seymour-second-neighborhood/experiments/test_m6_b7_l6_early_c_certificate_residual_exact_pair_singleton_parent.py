#!/usr/bin/env python3
"""Regression and hostile tests for the 101 singleton exact-pair CNFs."""

import hashlib
import json
import tempfile
from pathlib import Path

import check_m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as checker
import m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as producer


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError, IndexError):
        return
    raise AssertionError(f"hostile singleton mutation accepted: {label}")


cells, memberships, manifest = checker.check_cover()
produced_cells, produced_memberships = producer.load_memberships()
hashes = checker.load_hashes()
assert len(cells) == 20 and len(memberships) == 101
assert tuple((member[0], member[2]) for member in memberships) == tuple(
    (cell, parent) for cell, (_, child) in enumerate(cells) for parent in child[5])
assert tuple((member[0], member[1][0], member[1][1][0], member[2]) for member in memberships) == tuple(
    (member[0], member[1][0], member[1][1][0], member[2]) for member in produced_memberships)
assert all(len({checker.independent_projection(child, parent) for parent in child[5]}) == len(child[5])
           for _, child in cells)

with tempfile.TemporaryDirectory(prefix="exact-pair-singleton-test-", dir=producer.HERE.parent) as directory:
    directory = Path(directory)
    path = directory / "membership.cnf"
    generated = {}
    samples = {}
    checked_parent_counts = set()
    for ordinal, member in enumerate(produced_memberships):
        cnf, selectors = producer.build_membership(member)
        producer.write_membership(path, ordinal, member, cnf, selectors, manifest)
        generated[producer.membership_key(member)] = (path.stat().st_size,
                                                       hashlib.sha256(path.read_bytes()).hexdigest())
        if len(member[1][1][5]) not in checked_parent_counts:
            checker.check(path)
            checked_parent_counts.add(len(member[1][1][5]))
        samples.setdefault((member[0], len(member[1][1][5])), path.read_text(encoding="ascii"))
    assert generated == hashes

    sample = samples[next(iter(samples))]
    mutations = (
        sample.replace("c parent-ordinal 1", "c parent-ordinal 0", 1),
        sample.replace("c selector-unit-clauses 1", "c selector-unit-clauses 0", 1),
        sample.replace("c lrat-status not-generated", "c lrat-status generated", 1),
    )
    for index, text in enumerate(mutations):
        bad = directory / f"bad-{index}.cnf"
        bad.write_text(text, encoding="ascii", newline="\n")
        reject(lambda bad=bad: checker.check(bad), f"metadata-{index}")

    ordinal = next(i for i, member in enumerate(produced_memberships) if len(member[1][1][5]) > 1)
    member = produced_memberships[ordinal]
    cnf, selectors = producer.build_membership(member)
    producer.write_membership(path, ordinal, member, cnf, selectors, manifest)
    selected = selectors[member[2]]
    bad = directory / "bad-selector-unit.cnf"
    bad.write_text(path.read_text(encoding="ascii").replace(f"{selected} 0\n", f"-{selected} 0\n", 1),
                   encoding="ascii", newline="\n")
    reject(lambda: checker.check(bad), "selected-selector-polarity")

    checker.check_scout()
    scout = json.loads(checker.SCOUT.read_text(encoding="ascii"))
    scout["rows"][0]["cnf_sha256"] = "0" * 64
    bad_scout = directory / "bad-scout.json"
    bad_scout.write_text(json.dumps(scout, sort_keys=True, indent=2) + "\n",
                         encoding="ascii", newline="\n")
    reject(lambda: checker.check_scout(bad_scout, require_frozen_identity=False), "scout-cnf-hash")

print(f"PASS exact-pair singleton tests: 20 disjoint/exhaustive refinements, 101 CNF hashes, "
      f"{len(checked_parent_counts)} parsed parent-count shapes, hostile mutations")
