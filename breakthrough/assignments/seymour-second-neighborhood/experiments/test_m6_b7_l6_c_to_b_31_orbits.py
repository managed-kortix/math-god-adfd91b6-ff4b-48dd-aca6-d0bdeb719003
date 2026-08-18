#!/usr/bin/env python3
"""Regression and hostile tests for the frozen C-to-B (3,1) campaign."""

import tempfile
from pathlib import Path

import check_m6_b7_l6_c_to_b_31_orbits as checker
import m6_b7_l6_c_to_b_31_orbits as producer
import verify_m6_b7_l6_c_to_b_31_orbit_certificates as verifier


def reject(call, label):
    try:
        call()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise AssertionError(f"hostile mutation accepted: {label}")


all_parents, parents = producer.load_parents()
assert len(all_parents) == 42 and len(parents) == 10
assert all(producer.compatible(row) for _, _, row in parents)
assert not any(producer.compatible(row) for row in [x[2] for x in all_parents if x not in parents])
manifest = producer.manifest_payload(all_parents, parents)
assert manifest == checker.manifest_payload(*checker.derive())
checker.check_exhaustion()
orbits = checker.derive_ordered_subset_orbits()
assert tuple(len(orbit) for _, orbit in orbits) == (140, 105)
assert set().union(*(set(orbit) for _, orbit in orbits)) == {
    (frozenset(left), frozenset((right,)))
    for left in __import__("itertools").combinations(checker.B, 3) for right in checker.B
}
metadata, certificate_rows = verifier.load_ledger()
verifier.verify_bindings(metadata)
assert verifier.runtime_source_closure() == verifier.RUNTIME_SOURCE_NAMES

with tempfile.TemporaryDirectory() as directory:
    directory = Path(directory)
    for t in (0, 1):
        path = directory / f"t{t}.cnf"
        cnf, selectors = producer.build_group(t, parents)
        producer.write_group(path, t, cnf, selectors, manifest, parents)
        names, clauses, expected_selectors = checker.reconstruct(t, checker.derive()[1])
        assert list(cnf.names) == names and cnf.clauses == clauses and selectors == expected_selectors
        checker.validate_clause_families(t, names, clauses, expected_selectors, checker.derive()[1])

    source = (directory / "t0.cnf").read_text(encoding="ascii")
    mutations = (
        source.replace("c compatible-parents 10", "c compatible-parents 9", 1),
        source.replace("c intersection-t 0", "c intersection-t 1", 1),
        source.replace("c ordered-C-row-sizes 3,1", "c ordered-C-row-sizes 1,3", 1),
        source.replace("c committed-parent-census 42", "c committed-parent-census 41", 1),
        source.replace("c profile-unit-clauses 17", "c profile-unit-clauses 16", 1),
        source.replace("c C16-subset 9,10,11", "c C16-subset 9,10,12", 1),
        source.replace("c first-selector 23617", "c first-selector 23618", 1),
        source.replace("23617 23618 23619 23620 23621 23622 23623 23624 23625 23626 0",
                       "23617 23617 23619 23620 23621 23622 23623 23624 23625 23626 0", 1),
        source.replace("-23617 ", "-23618 ", 1),
    )
    for i, text in enumerate(mutations):
        path = directory / f"bad-{i}.cnf"
        path.write_text(text, encoding="ascii")
        reject(lambda path=path: checker.check(path), f"CNF-{i}")
        path.unlink()

    original = verifier.LEDGER.read_text(encoding="ascii")
    hostile_ledger_mutations = (
        original.replace(metadata["orbit-manifest-sha256"], "0" * 64, 1),
        original.replace(certificate_rows[0]["artifact"], "certificates/../hostile.lrat.xz", 1),
        original.replace(certificate_rows[0]["xz-sha256"], "0" * 64, 1),
        original + original.rstrip("\n").split("\n")[-1] + "\n",
    )
    for i, text in enumerate(hostile_ledger_mutations):
        path = directory / f"bad-ledger-{i}.tsv"
        path.write_text(text, encoding="ascii", newline="\n")
        def validate_hostile_ledger(path=path):
            verifier.load_ledger(path)
            if verifier.canonical_ledger_hash(path) != verifier.LEDGER_CANONICAL_SHA256:
                raise RuntimeError("canonical ledger pin differs")
        reject(validate_hostile_ledger, f"ledger-{i}")

    runtime_key = "runtime-snc-cnf"
    original_path = verifier.BOUND_PATHS[runtime_key]
    bad_runtime = directory / "snc_cnf.py"
    bad_runtime.write_bytes(original_path.read_bytes() + b"\n")
    verifier.BOUND_PATHS[runtime_key] = bad_runtime
    try:
        reject(lambda: verifier.verify_bindings(metadata), "runtime-pin")
    finally:
        verifier.BOUND_PATHS[runtime_key] = original_path

    artifact = verifier.ROOT / certificate_rows[0]["artifact"]
    assert verifier.identity(artifact) == (int(certificate_rows[0]["xz-bytes"]),
                                           certificate_rows[0]["xz-sha256"])

print("PASS m6 B7-l6 exact C-to-B (3,1), t=0/1 tests")
