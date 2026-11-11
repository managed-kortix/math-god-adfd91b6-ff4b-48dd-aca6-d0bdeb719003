#!/usr/bin/env python3
"""Regression and hostile tests for the exact 60-orbit early C census."""

import hashlib
import tempfile
from pathlib import Path

import check_m6_b7_l6_early_c_profile_census as checker
import m6_b7_l6_early_c_profile_census as producer
import m6_b7_l6_early_c_profile_scout as scout
import m6_b7_l6_c_to_b_31_orbits as certified


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise AssertionError(f"hostile mutation accepted: {label}")


orbits = producer.load_orbits()
independent = checker.derive()
assert len(orbits) == len(independent) == 60
assert sum(len(x[7]) for x in orbits) == 544
assert [(x[1], x[2], x[3], x[4], x[6], len(x[7])) for x in orbits] == [
    (x[1], x[2], x[3], x[4], x[6], len(x[7])) for x in independent]
manifest = producer.manifest_payload(orbits)
assert manifest == checker.manifest_payload(independent) == checker.MANIFEST.read_bytes()
assert [(orbits[i][3][3], orbits[i][4]) for i in (34, 35)] == [((3, 1), 0), ((3, 1), 1)]
assert orbits[31][3][3] == (2, 2) and orbits[31][4] == 0
checker.check_exhaustion()

closure_members = independent[31][7]
checker.check_parent_support_closure(closure_members)
closure_supports = {frozenset(checker.expected_projection(row)[1]) for _, _, row in closure_members}
closure_supports.add(frozenset({(0, 9)}))
reject(lambda: checker.check_parent_support_closure(closure_members, supports_override=closure_supports),
       "parent-support-permutation-closure")

scout_payload = scout.payload()
assert len(scout_payload["rows"]) == 58
assert scout_payload["excluded_certified_orbits"] == [34, 35]
assert not scout_payload["orbit_31_certified"]
assert {row["orbit"] for row in scout_payload["rows"]} == set(range(60)) - {34, 35}
assert sum(row["status"] == "UNSAT" for row in scout_payload["rows"]) == 31
assert sum(row["status"] == "TIMEOUT" for row in scout_payload["rows"]) == 27
assert scout_payload["total_eliminated_including_certified"] == 33
assert producer.scout_sequence(orbits) == checker.independent_scout_sequence(independent)

_, certified_parents = certified.load_parents()
for ordinal, t in producer.CERTIFIED.items():
    authoritative_cnf, _ = producer.build_orbit(orbits[ordinal])
    certified_cnf, _ = certified.build_group(t, certified_parents)
    assert authoritative_cnf.clauses == certified_cnf.clauses
    assert list(authoritative_cnf.names.values()) == list(certified_cnf.names.values())

with tempfile.TemporaryDirectory(prefix="early-c-profile-test-", dir=producer.HERE.parent) as directory:
    directory = Path(directory)
    hashes = checker.load_hashes(manifest)
    hash_lines = checker.HASHES.read_text(encoding="ascii").splitlines()
    fields = hash_lines[5 + 23].split("\t")
    fields[6] = "0" * 64
    hash_lines[5 + 23] = "\t".join(fields)
    bad_hashes = directory / "bad-hashes.tsv"
    bad_hashes.write_text("\n".join(hash_lines) + "\n", encoding="ascii", newline="\n")
    altered_hashes = checker.load_hashes(manifest, bad_hashes)
    hash_path = directory / "o23-hash.cnf"
    checker.write_reconstruction(hash_path, 23, independent[23], manifest)
    reject(lambda: None if checker.identity(hash_path) == altered_hashes[23] else
           (_ for _ in ()).throw(RuntimeError("arbitrary hash mismatch")), "arbitrary-hash-row")
    for ordinal in (0, 31, 34, 35, 59):
        path = directory / f"o{ordinal:02d}.cnf"
        cnf, selectors = producer.build_orbit(orbits[ordinal])
        producer.write_orbit(path, ordinal, orbits[ordinal], cnf, selectors, manifest)
        assert producer.identity(path) == hashes[ordinal]
        names, clauses, expected_selectors = checker.reconstruct(independent[ordinal])
        assert list(cnf.names) == names and cnf.clauses == clauses and selectors == expected_selectors
        checker.check(path)
        if ordinal != 31:
            path.unlink()

    source = (directory / "o31.cnf").read_text(encoding="ascii")
    mutations = (
        source.replace("c orbit 31", "c orbit 34", 1),
        source.replace("c C-row-sizes 2,2", "c C-row-sizes 3,1", 1),
        source.replace("c intersection-t 0", "c intersection-t 1", 1),
        source.replace("c S7-orbit-size 210", "c S7-orbit-size 209", 1),
        source.replace("c parents 10", "c parents 9", 1),
        source.replace("c C16-subset 9,10", "c C16-subset 9,11", 1),
        source.replace("c first-selector 23617", "c first-selector 23618", 1),
        source.replace("23617 23618 23619 23620 23621 23622 23623 23624 23625 23626 0",
                       "23617 23617 23619 23620 23621 23622 23623 23624 23625 23626 0", 1),
    )
    for i, text in enumerate(mutations):
        path = directory / f"bad-{i}.cnf"
        path.write_text(text, encoding="ascii", newline="\n")
        reject(lambda path=path: checker.check(path), f"CNF-{i}")

    altered = dict(scout_payload)
    altered["orbit_31_certified"] = True
    assert hashlib.sha256((__import__("json").dumps(altered, sort_keys=True, indent=2) + "\n").encode("ascii")).hexdigest() != \
        hashlib.sha256((__import__("json").dumps(scout_payload, sort_keys=True, indent=2) + "\n").encode("ascii")).hexdigest()

print("PASS frozen B7-l6 authoritative 60-orbit early C-profile census tests")
