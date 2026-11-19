#!/usr/bin/env python3
"""Exhaustive partition, CNF, mutation, and attribution tests for m=6 residual groups."""

import hashlib
import gc
import tempfile
from pathlib import Path

import m6_residual_group_cnf as producer
import check_m6_residual_group_cnf as checker

HERE = Path(__file__).resolve().parent
COVER = HERE / "m6-placement-cover.txt"
FILTER = HERE / "m6-placement-filter.txt"
MANIFEST = HERE / "m6-residual-selector-groups.tsv"


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


rows = checker.read_cover(COVER)
statuses = checker.read_acceptance(FILTER)
checker_groups = checker.derive_groups(rows, statuses)
checker_manifest = checker.manifest_payload(checker_groups)
producer_groups = producer.load_partition(COVER, FILTER)
producer_manifest = producer.manifest_payload(producer_groups)
if not (checker_manifest == producer_manifest == MANIFEST.read_bytes()):
    raise RuntimeError("producer, checker, and frozen manifest differ")
if (len(checker_manifest), hashlib.sha256(checker_manifest).hexdigest()) != (
        checker.MANIFEST_BYTES, checker.MANIFEST_SHA256):
    raise RuntimeError("manifest fingerprint changed")
for key in checker.GROUP_KEYS:
    produced = [(accepted, row["cover_index"]) for accepted, row in producer_groups[key]]
    if produced != checker_groups[key]:
        raise RuntimeError(f"independent member streams differ for {key}")
    branch, lam, r, t = checker.parameters(key)
    for _, index in checker_groups[key]:
        derived_branch, derived_lam, states = checker.exact_states(rows[index])
        if (derived_branch, derived_lam) != (branch, lam) or (r, t) not in states:
            raise RuntimeError(f"nonfeasible member in {key}")
print("PASS exact pointwise C-state derivation for all 80974 memberships in 23 groups")

with tempfile.TemporaryDirectory(prefix="m6-residual-", dir=HERE) as directory:
    directory = Path(directory)
    checked = {}
    if set(checker.GROUP_CNF_SHA256) != set(checker.GROUP_KEYS) or producer.GROUP_CNF_SHA256 != checker.GROUP_CNF_SHA256:
        raise RuntimeError("producer/checker CNF hash tables do not cover the exact 23 groups")
    for key in checker.GROUP_KEYS:
        branch, _, r, t = checker.parameters(key)
        b_count, c_count = len(checker.LABELS[branch]["B"]), len(checker.LABELS[branch]["C"])
        rv, rc = checker.counter_shape(b_count * c_count, r)
        tv, tc = checker.counter_shape(c_count, t)
        expected = (checker.BASE_VARIABLES + rv + tv + len(checker_groups[key]),
                    checker.BASE_CLAUSES[branch] + rc + tc + 1 + 153 * len(checker_groups[key]))
        if checker.dimensions(key, len(checker_groups[key])) != expected:
            raise RuntimeError(f"counter/guard dimensions changed for {key}")
    generated_hashes = {}
    for key in checker.GROUP_KEYS:
        path = directory / f"{key}.cnf"
        cnf, shapes, selectors = producer.build_group(key, producer_groups[key])
        producer.write_group(path, key, producer_groups[key], cnf, shapes, selectors, producer_manifest)
        generated_hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        if generated_hashes[key] != checker.GROUP_CNF_SHA256[key]:
            raise RuntimeError(f"frozen CNF hash changed for {key}")
        producer_selectors = selectors
        del cnf, shapes, selectors
        gc.collect()
        variables, clauses, checked_rows, members, checked_selectors = checker.check(path, COVER, FILTER)
        if producer_selectors != checked_selectors or len(clauses) != checker.dimensions(key, len(members))[1]:
            raise RuntimeError(f"counter/selector boundary changed for {key}")
        if key == "B7-l6-r5-t2":
            checked[key] = path, variables, clauses, checked_rows, members, checked_selectors
        elif key == "B6-l6-r0-t0":
            checked[key] = (path,)
        del producer_selectors, variables, clauses, checked_rows, members, checked_selectors
        gc.collect()
    if generated_hashes != checker.GROUP_CNF_SHA256:
        raise RuntimeError("generated hash ledger differs from all 23 frozen group hashes")
    print("PASS generated, independently reconstructed, checked, and hashed all 23 group CNFs")

    path, variables, clauses, checked_rows, members, selectors = checked["B7-l6-r5-t2"]
    tautologies = [(number, -number) for number in range(1, len(variables) + 1)]
    values = {number: True for number in range(1, len(variables) + 1)}
    for selector in selectors:
        values[selector] = selector == selectors[0]
    holes = checker.expected_projection(checked_rows[members[0][1]])[1]
    name_to_number = {name: number for number, name in enumerate(variables, 1)}
    for pair in checker.PAIRS:
        values[name_to_number[f"h_{pair[0]}_{pair[1]}"]] = pair in holes
    complete = [number if values[number] else -number for number in range(1, len(variables) + 1)]
    checker.validate_model(variables, tautologies, complete, selectors[0], len(selectors))
    reject(lambda: checker.validate_model(variables, tautologies, complete[:-1], selectors[0], len(selectors)),
           "partial model")
    reject(lambda: checker.validate_model(variables, tautologies, complete + [complete[0]],
                                          selectors[0], len(selectors)), "duplicate assignment")
    multiple = complete.copy(); multiple[selectors[1] - 1] = selectors[1]
    reject(lambda: checker.validate_model(variables, tautologies, multiple, selectors[0], len(selectors)),
           "multiple selectors")
    falsified = complete.copy(); falsified[0] = -1
    reject(lambda: checker.validate_model(variables, [(1,)] + tautologies, falsified,
                                                    selectors[0], len(selectors)),
           "falsified clause")
    print("PASS strict complete-model, clause, and exactly-one-selector attribution gates")

    def mutate(source, label, edit, clause_delta=0):
        lines = source.read_text(encoding="ascii").splitlines()
        header = next(i for i, line in enumerate(lines) if line.startswith("p cnf "))
        edit(lines, header)
        if clause_delta:
            header = next(i for i, line in enumerate(lines) if line.startswith("p cnf "))
            fields = lines[header].split(); fields[3] = str(int(fields[3]) + clause_delta)
            lines[header] = " ".join(fields)
        target = directory / f"mutation-{label}.cnf"
        target.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(target, COVER, FILTER), label)

    base_count = checker.BASE_CLAUSES["B7"]
    r_clauses = 394
    high_clauses = 9
    first = lambda header, offset: header + 1 + offset
    mutate(path, "base", lambda lines, header: lines.__setitem__(first(header, 0), "-2 0"))
    mutate(path, "r-counter", lambda lines, header: lines.__setitem__(
        first(header, base_count), str(-int(lines[first(header, base_count)].split()[0])) + " 0"))
    mutate(path, "high-counter", lambda lines, header: lines.__setitem__(
        first(header, base_count + r_clauses), "-1 0"))
    alo = base_count + r_clauses + high_clauses
    mutate(path, "alo-delete", lambda lines, header: lines.pop(first(header, alo)), -1)
    mutate(path, "guard", lambda lines, header: lines.__setitem__(first(header, alo + 1), "-1 0"))
    mutate(path, "metadata", lambda lines, header: lines.__setitem__(
        next(i for i, line in enumerate(lines) if line.startswith("c excluded-regimes ")),
        "c excluded-regimes B6:lambda=3"))
    mutate(path, "selector-name", lambda lines, header: lines.__setitem__(
        next(i for i, line in enumerate(lines) if line == f"c var {selectors[0]} residual_group_selector_00000"),
        f"c var {selectors[0]} wrong_selector"))
    b6_path = checked["B6-l6-r0-t0"][0]
    b6_base = checker.BASE_CLAUSES["B6"]
    mutate(b6_path, "B6-r-counter", lambda lines, header: lines.__setitem__(
        first(header, b6_base), str(-int(lines[first(header, b6_base)].split()[0])) + " 0"))
    mutate(b6_path, "B6-high-counter", lambda lines, header: lines.__setitem__(
        first(header, b6_base + 649), "-1 0"))
    print("PASS hostile B6/B7 base/counter/ALO/guard/metadata/selector mutations")

    for name, identity_path in checker.IDENTITY_PATHS.items():
        altered = directory / identity_path.name
        altered.write_bytes(identity_path.read_bytes() + b"\n")
        old = checker.IDENTITY_PATHS[name]
        checker.IDENTITY_PATHS[name] = altered
        reject(checker.verify_identities, f"checker {name} identity")
        checker.IDENTITY_PATHS[name] = old
    print("PASS forced certificate ledger/verifier/manifest identity mutations")

print("PASS m6 residual selector-group CNF tests")
