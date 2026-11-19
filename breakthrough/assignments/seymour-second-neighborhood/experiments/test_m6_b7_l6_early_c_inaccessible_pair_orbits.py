#!/usr/bin/env python3
"""Regression and hostile tests for the exact inaccessible-pair cover."""

import hashlib
import json
import tempfile
from pathlib import Path

import check_m6_b7_l6_early_c_inaccessible_pair_orbits as checker
import m6_b7_l6_early_c_inaccessible_pair_orbits as producer


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise AssertionError(f"hostile mutation accepted: {label}")


produced = producer.load_children()
checked = checker.derive_children()
project = lambda child: (child[0], child[1], child[3], child[4], child[5])
assert tuple(map(project, produced)) == tuple(map(project, checked))
assert len(produced) == 192 and sum(len(child[5]) for child in produced) == 746
manifest = producer.manifest_payload(produced)
assert manifest == checker.manifest_payload(checked) == checker.MANIFEST.read_bytes()
checker.check_exhaustion()

with tempfile.TemporaryDirectory(prefix="inaccessible-pair-test-", dir=producer.HERE.parent) as directory:
    directory = Path(directory)
    hashes = checker.load_hashes(manifest)
    retained = None
    for ordinal in (0, 1, 52, 124, 191):
        path = directory / f"child-{ordinal}.cnf"
        child = produced[ordinal]
        cnf, selectors = producer.build_child(child)
        producer.write_child(path, ordinal, child, cnf, selectors, manifest)
        assert (path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest()) == hashes[child[0]]
        checker.check(path)
        if ordinal == 0:
            retained = path.read_text(encoding="ascii")

    mutations = (
        retained.replace("c inaccessible-pair 0,1", "c inaccessible-pair 0,2", 1),
        retained.replace("c compatible-parent-ordinals ", "c compatible-parent-ordinals 9,", 1),
        retained.replace("c inaccessible-q-unit-clauses 2", "c inaccessible-q-unit-clauses 1", 1),
        retained.replace("c excluded-selector-unit-clauses ", "c excluded-selector-unit-clauses 99", 1),
        retained.replace("-" + str(checker.frozen_base()[0].index("q_16_0") + 1) + " 0",
                         str(checker.frozen_base()[0].index("q_16_0") + 1) + " 0", 1),
        retained.replace("-" + str(checker.frozen_base()[0].index("q_16_1") + 1) + " 0",
                         "-" + str(checker.frozen_base()[0].index("q_16_2") + 1) + " 0", 1),
        retained.replace("-23618 0", "23618 0", 1),
    )
    for index, text in enumerate(mutations):
        path = directory / f"bad-{index}.cnf"
        path.write_text(text, encoding="ascii", newline="\n")
        reject(lambda path=path: checker.check(path), f"CNF-{index}")

    profile = checked[0][2]
    supports = list(checker.parent_nonoutneighbors(profile, row) for _, _, row in profile[7])
    holes, nonout = supports[0]
    supports.append((holes ^ {tuple(sorted((9, 10)))}, nonout))
    reject(lambda: checker.verify_parent_invariance(profile, tuple(supports),
                                                    checker.explicit_stabilizer(profile[5])),
           "parent-support-invariance")

    scout_bytes = checker.SCOUT.read_bytes()
    scout = json.loads(scout_bytes.decode("ascii"))

    def mutate_scout(label, change):
        hostile = json.loads(scout_bytes.decode("ascii"))
        change(hostile)
        path = directory / f"bad-scout-{label}.json"
        path.write_text(json.dumps(hostile, sort_keys=True, indent=2) + "\n",
                        encoding="ascii", newline="\n")
        reject(lambda: checker.check_scout(manifest, hashes, path, require_frozen_identity=False), label)

    def swap_statuses(payload):
        unsat = next(row for row in payload["rows"] if row["status"] == "UNSAT")
        timeout = next(row for row in payload["rows"] if row["status"] == "TIMEOUT")
        unsat["status"], timeout["status"] = timeout["status"], unsat["status"]
        unsat["seconds"], timeout["seconds"] = timeout["seconds"], unsat["seconds"]

    mutate_scout("status-swap", swap_statuses)
    mutate_scout("solver-path", lambda payload: payload.update(solver="/tmp/cadical"))
    mutate_scout("solver-bytes", lambda payload: payload.update(solver_bytes=1002217))
    mutate_scout("solver-hash", lambda payload: payload.update(solver_sha256="0" * 64))
    mutate_scout("solver-version", lambda payload: payload.update(solver_version="1.7.4"))

    frozen_mutation = directory / "bad-scout-whole-identity.json"
    frozen_mutation.write_bytes(scout_bytes.replace(b'"seconds": 0.164', b'"seconds": 0.165', 1))
    reject(lambda: checker.check_scout(manifest, hashes, frozen_mutation), "scout-whole-identity")

    ledger = checker.HASHES.read_text(encoding="ascii").splitlines()

    def mutate_ledger(label, column, value):
        lines = list(ledger)
        fields = lines[5].split("\t")
        fields[column] = value
        lines[5] = "\t".join(fields)
        path = directory / f"bad-ledger-{label}.tsv"
        path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.load_hashes(manifest, path), label)

    mutate_ledger("compatible-parents", 2, "2")
    mutate_ledger("variables", 3, "23627")
    mutate_ledger("clauses", 4, "144289")

print("PASS frozen B7-l6 early C inaccessible-pair orbit tests")
