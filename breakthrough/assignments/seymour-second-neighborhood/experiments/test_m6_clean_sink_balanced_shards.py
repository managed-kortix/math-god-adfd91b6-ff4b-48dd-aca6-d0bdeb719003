#!/usr/bin/env python3
"""Exhaustive 57-shard hashes, cover, attribution, and hostile mutations."""

import gc
import hashlib
import tempfile
from pathlib import Path

import check_m6_clean_sink_balanced_shards as checker
import m6_clean_sink_balanced_shards as producer

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "m6-clean-sink-balanced-shards.tsv"
HASH_LEDGER = HERE / "m6-clean-sink-balanced-shard-hashes.tsv"


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


producer_shards = producer.load_shards()
checker_shards = checker.derive_shards()
producer_members = [[(a, c) for a, c, _ in shard[-1]] for shard in producer_shards]
checker_members = [[(a, c) for a, c, _ in shard[-1]] for shard in checker_shards]
if producer_members != checker_members:
    raise RuntimeError("producer/checker 57-shard member streams differ")
producer_manifest = producer.manifest_payload(producer_shards)
checker_manifest = checker.manifest_payload(checker_shards)
if not (producer_manifest == checker_manifest == MANIFEST.read_bytes()):
    raise RuntimeError("producer, checker, and full frozen manifest differ")
if (len(checker_manifest), hashlib.sha256(checker_manifest).hexdigest()) != (
        checker.MANIFEST_BYTES, checker.MANIFEST_SHA256):
    raise RuntimeError("57-shard manifest fingerprint changed")
producer_ledger = producer.hash_ledger_payload(producer_shards, producer_manifest)
checker_ledger = checker.hash_ledger_payload(checker_shards, checker_manifest)
if not (producer_ledger == checker_ledger == HASH_LEDGER.read_bytes()):
    raise RuntimeError("producer, checker, and frozen complete hash ledger differ")
if (len(checker_ledger), hashlib.sha256(checker_ledger).hexdigest()) != (
        checker.HASH_LEDGER_BYTES, checker.HASH_LEDGER_SHA256):
    raise RuntimeError("complete shard hash ledger fingerprint changed")
print("PASS independent exact cover: seven groups, 35 q,H_CC cells, 16392 parents, 57 shards")

with tempfile.TemporaryDirectory(prefix="m6-balanced-shards-", dir=HERE) as directory:
    directory = Path(directory)
    generated, retained = {}, {}
    if set(checker.SHARD_CNF_SHA256) != {shard[0] for shard in checker_shards}:
        raise RuntimeError("checker hash ledger does not cover exactly all 57 shards")
    if checker.SHARD_CNF_SHA256 != producer.SHARD_CNF_SHA256:
        raise RuntimeError("producer/checker shard hash ledgers differ")
    for ordinal, shard in enumerate(producer_shards):
        key, group, _, _, _, _, members = shard
        path = directory / f"{ordinal:02d}.cnf"
        cnf, selectors = producer.build_shard(group, members)
        producer.write_shard(path, ordinal, shard, cnf, selectors, producer_manifest)
        generated[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        if generated[key] != checker.SHARD_CNF_SHA256[key]:
            raise RuntimeError(f"frozen CNF hash changed for {key}")
        variables, clauses, checked_members, checked_selectors = checker.check(path)
        if len(variables) != checker.BASE_VARIABLES + len(members):
            raise RuntimeError(f"wrong variable dimension for {key}")
        if len(clauses) != checker.BASE_CLAUSES[group[:2]] + 1 + 153 * len(members):
            raise RuntimeError(f"wrong clause dimension for {key}")
        if ordinal in (6, 56):
            retained[ordinal] = path, variables, clauses, checked_members, checked_selectors
        del cnf, selectors, variables, clauses, checked_members, checked_selectors
        gc.collect()
    if generated != checker.SHARD_CNF_SHA256:
        raise RuntimeError("all generated hashes differ from the frozen complete ledger")
    print("PASS emitted, independently checked, dimensioned, and hashed all 57 shard CNFs")

    path, variables, _, members, selectors = retained[56]
    tautologies = [(number, -number) for number in range(1, len(variables) + 1)]
    values = {number: True for number in range(1, len(variables) + 1)}
    for selector in selectors:
        values[selector] = selector == selectors[0]
    holes = checker.expected_projection(members[0][2])[1]
    name_to_number = {name: number for number, name in enumerate(variables, 1)}
    for pair in checker.PAIRS:
        values[name_to_number[f"h_{pair[0]}_{pair[1]}"]] = pair in holes
    complete = [number if values[number] else -number for number in range(1, len(variables) + 1)]
    checked, selected = checker.validate_model(variables, tautologies, complete, selectors)
    if selected != 0 or any(checked[name_to_number[f"h_{a}_{b}"]] != ((a, b) in holes)
                            for a, b in checker.PAIRS):
        raise RuntimeError("complete model attribution selected the wrong parent")
    reject(lambda: checker.validate_model(variables, tautologies, complete[:-1], selectors), "partial model")
    reject(lambda: checker.validate_model(variables, tautologies, complete + [complete[0]], selectors),
           "duplicate assignment")
    none = complete.copy(); none[selectors[0] - 1] = -selectors[0]
    reject(lambda: checker.validate_model(variables, tautologies, none, selectors), "zero selectors")
    multiple = complete.copy(); multiple[selectors[1] - 1] = selectors[1]
    reject(lambda: checker.validate_model(variables, tautologies, multiple, selectors), "multiple selectors")
    falsified = complete.copy(); falsified[0] = -1
    reject(lambda: checker.validate_model(variables, [(1,)] + tautologies, falsified, selectors),
           "falsified clause")
    print("PASS complete-model evaluation and exact-one-selector attribution mutations")

    def mutate(source, label, edit, clause_delta=0):
        lines = source.read_text(encoding="ascii").splitlines()
        header = next(i for i, line in enumerate(lines) if line.startswith("p cnf "))
        edit(lines, header)
        if clause_delta:
            fields = lines[header].split(); fields[3] = str(int(fields[3]) + clause_delta)
            lines[header] = " ".join(fields)
        target = directory / f"mutation-{label}.cnf"
        target.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(target), label)

    b7_path, _, _, _, b7_selectors = retained[56]
    b7_base = checker.BASE_CLAUSES["B7"]
    first = lambda header, offset: header + 1 + offset
    mutate(b7_path, "B7-base", lambda lines, header: lines.__setitem__(first(header, 0), "-2 0"))
    mutate(b7_path, "alo-delete", lambda lines, header: lines.pop(first(header, b7_base)), -1)
    mutate(b7_path, "guard", lambda lines, header: lines.__setitem__(first(header, b7_base + 1), "-1 0"))
    mutate(b7_path, "balance-metadata", lambda lines, header: lines.__setitem__(
        next(i for i, line in enumerate(lines) if line == "c cap 500"), "c cap 499"))
    mutate(b7_path, "cell-metadata", lambda lines, header: lines.__setitem__(
        next(i for i, line in enumerate(lines) if line.startswith("c H_CC ")), "c H_CC 9"))
    mutate(b7_path, "selector-name", lambda lines, header: lines.__setitem__(
        next(i for i, line in enumerate(lines) if line ==
             f"c var {b7_selectors[0]} clean_sink_parent_selector_00000"),
        f"c var {b7_selectors[0]} wrong_selector"))
    b6_path = retained[6][0]
    mutate(b6_path, "B6-base", lambda lines, header: lines.__setitem__(first(header, 0), "-2 0"))
    print("PASS hostile B6/B7 base/ALO/guard/balance/cell/selector mutations")

    for name, source_path in list(checker.IDENTITY_PATHS.items()):
        altered = directory / f"bad-{name}"
        altered.write_bytes(source_path.read_bytes() + b"\n")
        checker.IDENTITY_PATHS[name] = altered
        reject(checker.verify_identities, f"bound identity {name}")
        checker.IDENTITY_PATHS[name] = source_path
    print("PASS clean stream/manifests/theorems and B6-l4 ledger/verifier identity mutations")

print("PASS m6 clean-sink balanced 57-shard tests")
