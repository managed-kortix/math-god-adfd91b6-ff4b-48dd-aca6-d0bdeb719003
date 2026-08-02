#!/usr/bin/env python3
"""Exhaustive hashes, attribution gates, and mutations for clean-sink parent CNFs."""

import gc
import hashlib
import tempfile
from pathlib import Path

import check_m6_clean_sink_group_cnf as checker
import m6_clean_sink_group_cnf as producer

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "m6-clean-sink-selector-groups.tsv"
REMAINING = HERE / "m6-clean-sink-remaining.tsv"
COVER = HERE / "m6-placement-cover.txt"
FILTER = HERE / "m6-placement-filter.txt"


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


producer_groups = producer.load_groups()
checker_groups = checker.derive_groups(checker.REMAINING, COVER, FILTER)
for key in checker.GROUP_KEYS:
    if [(a, c) for a, c, _ in producer_groups[key]] != [(a, c) for a, c, _ in checker_groups[key]]:
        raise RuntimeError(f"producer/checker unique-parent stream differs for {key}")
producer_manifest = producer.manifest_payload(producer_groups)
checker_manifest = checker.manifest_payload(checker_groups)
if not (producer_manifest == checker_manifest == MANIFEST.read_bytes()):
    raise RuntimeError("producer, checker, and frozen eight-group manifest differ")
if (len(checker_manifest), hashlib.sha256(checker_manifest).hexdigest()) != (
        checker.MANIFEST_BYTES, checker.MANIFEST_SHA256):
    raise RuntimeError("eight-group manifest fingerprint changed")
print("PASS exact no-mixed-parent projection: 46164 memberships -> 18862 parents in eight groups")

with tempfile.TemporaryDirectory(prefix="m6-clean-sink-groups-", dir=HERE) as directory:
    directory = Path(directory)
    generated, retained = {}, {}
    if set(checker.GROUP_CNF_SHA256) != set(checker.GROUP_KEYS):
        raise RuntimeError("checker hash ledger does not cover all eight groups")
    if checker.GROUP_CNF_SHA256 != producer.GROUP_CNF_SHA256:
        raise RuntimeError("producer/checker eight-hash ledgers differ")
    for key in checker.GROUP_KEYS:
        members = producer_groups[key]
        path = directory / f"{key}.cnf"
        cnf, selectors = producer.build_group(key, members)
        producer.write_group(path, key, members, cnf, selectors, producer_manifest)
        generated[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        if generated[key] != checker.GROUP_CNF_SHA256[key]:
            raise RuntimeError(f"frozen CNF hash changed for {key}")
        variables, clauses, checked_members, checked_selectors = checker.check(path)
        if len(cnf.names) != checker.BASE_VARIABLES + len(members):
            raise RuntimeError(f"unexpected non-selector variables in {key}")
        if len(cnf.clauses) != checker.BASE_CLAUSES[key[:2]] + 1 + 153 * len(members):
            raise RuntimeError(f"unexpected non-base/non-guard clauses in {key}")
        if key in ("B6-l6", "B7-l6"):
            retained[key] = path, variables, clauses, checked_members, checked_selectors
        del cnf, selectors, variables, clauses, checked_members, checked_selectors
        gc.collect()
    if generated != checker.GROUP_CNF_SHA256:
        raise RuntimeError("generated all-eight hash ledger differs from frozen ledger")
    print("PASS emitted, independently reconstructed, dimensioned, and hashed all eight CNFs")

    path, variables, clauses, members, selectors = retained["B7-l6"]
    tautologies = [(number, -number) for number in range(1, len(variables) + 1)]
    values = {number: True for number in range(1, len(variables) + 1)}
    for selector in selectors:
        values[selector] = selector == selectors[0]
    holes = checker.expected_projection(members[0][2])[1]
    name_to_number = {name: number for number, name in enumerate(variables, 1)}
    for pair in checker.PAIRS:
        values[name_to_number[f"h_{pair[0]}_{pair[1]}"]] = pair in holes
    complete = [number if values[number] else -number for number in range(1, len(variables) + 1)]
    checked_values, selected = checker.validate_model(
        variables, tautologies, complete, selectors[0], len(selectors))
    if selected != 0 or any(checked_values[name_to_number[f"h_{a}_{b}"]] != ((a, b) in holes)
                            for a, b in checker.PAIRS):
        raise RuntimeError("complete model attribution returned wrong parent")
    reject(lambda: checker.validate_model(variables, tautologies, complete[:-1], selectors[0], len(selectors)),
           "partial model")
    reject(lambda: checker.validate_model(variables, tautologies, complete + [complete[0]],
                                          selectors[0], len(selectors)), "duplicate assignment")
    no_selector = complete.copy(); no_selector[selectors[0] - 1] = -selectors[0]
    reject(lambda: checker.validate_model(variables, tautologies, no_selector,
                                          selectors[0], len(selectors)), "zero selectors")
    multiple = complete.copy(); multiple[selectors[1] - 1] = selectors[1]
    reject(lambda: checker.validate_model(variables, tautologies, multiple,
                                          selectors[0], len(selectors)), "multiple selectors")
    falsified = complete.copy(); falsified[0] = -1
    reject(lambda: checker.validate_model(variables, [(1,)] + tautologies, falsified,
                                          selectors[0], len(selectors)), "falsified clause")
    print("PASS complete-model evaluation and exact-one-selector parent attribution gates")

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
        reject(lambda: checker.check(target), label)

    first = lambda header, offset: header + 1 + offset
    base = checker.BASE_CLAUSES["B7"]
    mutate(path, "base", lambda lines, header: lines.__setitem__(first(header, 0), "-2 0"))
    mutate(path, "alo-delete", lambda lines, header: lines.pop(first(header, base)), -1)
    mutate(path, "guard", lambda lines, header: lines.__setitem__(first(header, base + 1), "-1 0"))
    mutate(path, "metadata-counter", lambda lines, header: lines.__setitem__(
        next(i for i, line in enumerate(lines) if line == "c counter-variables 0"),
        "c counter-variables 1"))
    mutate(path, "selector-name", lambda lines, header: lines.__setitem__(
        next(i for i, line in enumerate(lines) if line ==
             f"c var {selectors[0]} clean_sink_parent_selector_00000"),
        f"c var {selectors[0]} wrong_selector"))
    b6_path = retained["B6-l6"][0]
    mutate(b6_path, "B6-base", lambda lines, header: lines.__setitem__(first(header, 0), "-2 0"))
    print("PASS hostile B6/B7 base/ALO/guard/metadata/selector mutations")

    coherent_rt = directory / "coherent-rt-mutation.tsv"
    coherent_rt.write_bytes(REMAINING.read_bytes().replace(
        b"00000\t00\tB6-l4-r0-t2\t00018\t00059\t000260\tB6\t4\t0\t2",
        b"00000\t01\tB6-l4-r1-t3\t00018\t00059\t000260\tB6\t4\t1\t3", 1))
    if coherent_rt.read_bytes() == REMAINING.read_bytes():
        raise RuntimeError("coherent r,t mutation target not found")
    reject(lambda: checker.derive_groups(coherent_rt, COVER, FILTER), "coherent checker r,t fields")
    reject(lambda: producer.load_groups(coherent_rt, COVER, FILTER), "coherent producer r,t fields")
    mutated_identity = (coherent_rt.stat().st_size, hashlib.sha256(coherent_rt.read_bytes()).hexdigest())
    checker_identity = checker.IDENTITIES["remaining-stream"]
    checker_path = checker.IDENTITY_PATHS["remaining-stream"]
    producer_identity = producer.IDENTITIES["remaining-stream"]
    producer_path = producer.IDENTITY_PATHS["remaining-stream"]
    checker.IDENTITIES["remaining-stream"] = mutated_identity
    checker.IDENTITY_PATHS["remaining-stream"] = coherent_rt
    producer.IDENTITIES["remaining-stream"] = mutated_identity
    producer.IDENTITY_PATHS["remaining-stream"] = coherent_rt
    try:
        reject(lambda: checker.derive_groups(coherent_rt, COVER, FILTER),
               "coherent checker r,t fields with matching hostile ledger")
        reject(lambda: producer.load_groups(coherent_rt, COVER, FILTER),
               "coherent producer r,t fields with matching hostile ledger")
    finally:
        checker.IDENTITIES["remaining-stream"] = checker_identity
        checker.IDENTITY_PATHS["remaining-stream"] = checker_path
        producer.IDENTITIES["remaining-stream"] = producer_identity
        producer.IDENTITY_PATHS["remaining-stream"] = producer_path
    print("PASS coherent key/r/t mutation rejected by frozen identity and independent semantics")

    for name, source in list(checker.IDENTITY_PATHS.items()):
        altered = directory / f"bad-{source.name}"
        altered.write_bytes(source.read_bytes() + b"\n")
        checker.IDENTITY_PATHS[name] = altered
        reject(checker.verify_identities, f"bound identity {name}")
        checker.IDENTITY_PATHS[name] = source
    print("PASS stream/manifest/theorem/prior-forced-certificate identity mutations")

print("PASS m6 clean-sink exact parent-selector CNF tests")
