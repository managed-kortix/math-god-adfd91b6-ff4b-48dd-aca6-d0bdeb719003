#!/usr/bin/env python3
"""Tests for the exact residual singleton-parent split."""

import hashlib
import json
import tempfile
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent as checker
import m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent as producer


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError, IndexError):
        return
    raise RuntimeError(f"hostile singleton-parent mutation accepted: {label}")


cover, memberships, manifest = checker.check_cover()
expected = checker.load_hashes()
generated = {}
samples = {}
checked_shapes = set()
with tempfile.TemporaryDirectory(prefix="m6-residual-singleton-test-", dir=producer.HERE.parent) as directory:
    directory = Path(directory)
    path = directory / "membership.cnf"
    for ordinal, member in enumerate(memberships):
        cnf, selectors = producer.build_membership(member)
        producer.write_membership(path, ordinal, member, cnf, selectors, manifest)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        generated[producer.membership_key(member)] = digest
        shape = (member[1][2], len(selectors))
        if shape not in checked_shapes:
            checker.check(path)
            checked_shapes.add(shape)
        samples.setdefault(len(selectors), path.read_bytes())
    if generated != expected:
        raise RuntimeError("all 1382 regenerated singleton CNFs differ from hash ledger")

    def mutate(label, predicate, replacement):
        lines = samples[next(iter(samples))].decode("ascii").splitlines()
        index = next(i for i, line in enumerate(lines) if predicate(line))
        lines[index] = replacement(lines[index])
        bad = directory / f"bad-{label}.cnf"
        bad.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(bad), label)

    mutate("parent-ordinal", lambda line: line.startswith("c parent-ordinal "),
           lambda _: "c parent-ordinal 9")
    mutate("selected-selector", lambda line: line.startswith("c selected-selector "),
           lambda line: line.rsplit(" ", 1)[0] + " 1")
    mutate("selector-unit-polarity", lambda line: line.split() == [line.split()[0], "0"] and
           line.split()[0].isdigit(), lambda line: "-" + line)

    checker.check_scout()
    scout = json.loads(checker.SCOUT_PATH.read_text(encoding="ascii"))

    bad_scout_identity = directory / "bad-scout-identity.json"
    bad_scout_identity.write_text(
        checker.SCOUT_PATH.read_text(encoding="ascii").replace('"status": "UNSAT"',
                                                               '"status": "TIMEOUT"', 1),
        encoding="ascii", newline="\n")
    reject(lambda: checker.check_scout(bad_scout_identity), "scout-bytes-hash")

    def mutate_scout(label, change):
        changed = json.loads(json.dumps(scout))
        change(changed)
        bad = directory / f"bad-scout-{label}.json"
        bad.write_text(json.dumps(changed, sort_keys=True, indent=2) + "\n",
                       encoding="ascii", newline="\n")
        reject(lambda: checker.check_scout(bad, require_frozen_identity=False), label)

    def swap_statuses(payload):
        unsat = next(row for row in payload["rows"] if row["status"] == "UNSAT")
        timeout = next(row for row in payload["rows"] if row["status"] == "TIMEOUT")
        unsat["status"], timeout["status"] = timeout["status"], unsat["status"]
        unsat["seconds"], timeout["seconds"] = timeout["seconds"], unsat["seconds"]

    mutate_scout("sat-injection", lambda payload: payload["rows"][0].update(status="SAT"))
    mutate_scout("status-swap", swap_statuses)
    mutate_scout("cnf-hash", lambda payload: payload["rows"][0].update(cnf_sha256="0" * 64))
    mutate_scout("solver-path", lambda payload: payload.update(solver="/tmp/cadical"))
    mutate_scout("solver-bytes", lambda payload: payload.update(solver_bytes=1002217))
    mutate_scout("solver-hash", lambda payload: payload.update(solver_sha256="0" * 64))
    mutate_scout("solver-version", lambda payload: payload.update(solver_version="1.7.4"))
    mutate_scout("jobs", lambda payload: payload.update(jobs=3))
    mutate_scout("job-assignment", lambda payload: payload["rows"][0].update(job=1))
    mutate_scout("timeout-seconds", lambda payload: payload["rows"][1].update(seconds=4.999))

    ledger_lines = checker.HASH_PATH.read_text(encoding="ascii").splitlines()

    def mutate_ledger(label, index, replacement):
        lines = list(ledger_lines)
        lines[index] = replacement(lines[index])
        bad = directory / f"bad-ledger-{label}.tsv"
        bad.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.load_hashes(bad), label)

    mutate_ledger("format", 0, lambda line: line + "-hostile")
    mutate_ledger("header", 4, lambda line: line.replace("cnf-sha256", "sha256"))
    mutate_ledger("uppercase-hash", 5, lambda line: line[:-64] + line[-64:].upper())

print(f"PASS singleton-parent tests: 153 disjoint/exhaustive selector covers, 1382 CNF hashes, "
      f"{len(checked_shapes)} independently parsed shapes, frozen scout, hostile mutations")
