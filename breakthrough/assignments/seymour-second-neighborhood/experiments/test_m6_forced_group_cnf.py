#!/usr/bin/env python3
"""Manifest, boundary, mutation, and model-attribution tests for forced groups."""

import hashlib
import tempfile
from pathlib import Path

import m6_forced_group_cnf as producer
from check_m6_forced_group_cnf import (
    BASE_VARIABLES, GROUP_CNF_SHA256, GROUP_KEYS, HUMAN_PROOF, MANIFEST_BYTES,
    MANIFEST_SHA256, PAIRS,
    attribute_model, check, derive_groups, manifest_payload, read_acceptance,
    read_cover, validate_model,
)

HERE = Path(__file__).resolve().parent
COVER = HERE / "m6-placement-cover.txt"
FILTER = HERE / "m6-placement-filter.txt"
FROZEN_MANIFEST = HERE / "m6-forced-selector-groups.tsv"


def require_failure(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise RuntimeError(f"mutation was accepted: {label}")


checker_rows = read_cover(COVER)
statuses = read_acceptance(FILTER)
checker_groups = derive_groups(checker_rows, statuses)
checker_manifest = manifest_payload(checker_groups)
if (len(checker_manifest) != MANIFEST_BYTES or
        hashlib.sha256(checker_manifest).hexdigest() != MANIFEST_SHA256 or
        checker_manifest != FROZEN_MANIFEST.read_bytes()):
    raise RuntimeError("independent manifest differs from frozen bytes")

producer_groups = producer.load_partition(COVER, FILTER)
producer_manifest = producer.manifest_payload(producer_groups)
if producer_manifest != checker_manifest:
    raise RuntimeError("producer and independent group manifests disagree")
for key in GROUP_KEYS:
    production = [(original, accepted, row["cover_index"])
                  for original, accepted, row in producer_groups[key]]
    if production != checker_groups[key]:
        raise RuntimeError(f"producer and checker member stream disagree for {key}")
    checker_projections = [frozenset(producer.child.parent.embedded_holes(
        key[:2], row["word"], row["edges"])[1]) for _, _, row in producer_groups[key]]
    if len(set(checker_projections)) != len(checker_projections):
        raise RuntimeError(f"duplicate member projections in {key}")
print(f"PASS frozen manifest groups=9 rows=31568 bytes={MANIFEST_BYTES} sha256={MANIFEST_SHA256}")

with tempfile.TemporaryDirectory(prefix="m6-forced-groups-") as directory:
    directory = Path(directory)
    checked = {}
    for key in GROUP_KEYS:
        path = directory / f"{key}.cnf"
        cnf, common, selectors = producer.build_group(key, producer_groups[key])
        producer.write_group(
            path, key, producer_groups[key], cnf, common, selectors, producer_manifest
        )
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != GROUP_CNF_SHA256[key]:
            raise RuntimeError(f"frozen CNF hash changed for {key}: {digest}")
        variables, rows, members = check(path, COVER, FILTER)
        if selectors != list(range(23617, 23617 + len(members))):
            raise RuntimeError(f"selector boundary changed for {key}")
        checked[key] = (path, variables, rows, members)
    print("PASS all nine group boundaries and frozen CNF hashes")

    path, variables, rows, members = checked["B7-q5"]
    hole_numbers = {}
    for number, name in enumerate(variables, 1):
        if name.startswith("h_"):
            _, left, right = name.split("_")
            hole_numbers[int(left), int(right)] = number

    def attribution_model(member):
        holes = set()
        row = rows[members[member][2]]
        from check_m6_forced_group_cnf import expected_holes
        holes.update(expected_holes(row))
        values = {number: True for number in range(1, len(variables) + 1)}
        for selected in range(len(members)):
            values[BASE_VARIABLES + selected + 1] = selected == member
        for pair in PAIRS:
            values[hole_numbers[pair]] = pair in holes
        literals = [number if values[number] else -number for number in range(1, len(variables) + 1)]
        return literals

    for member in (0, len(members) - 1):
        attributed = attribute_model(variables, [(number, -number) for number in range(1, len(variables) + 1)],
                                     attribution_model(member), rows, members)
        if attributed != [(member,) + members[member]]:
            raise RuntimeError(f"model attribution failed at member boundary {member}")

    complete = attribution_model(0)
    tautologies = [(number, -number) for number in range(1, len(variables) + 1)]
    require_failure(lambda: validate_model(variables, tautologies, complete[:-1], len(members)),
                    "partial model")
    base_unit = [(1,)] + tautologies
    falsifies_base = complete.copy()
    falsifies_base[0] = -1
    require_failure(lambda: validate_model(
        variables, base_unit, falsifies_base, len(members)), "model falsifying base unit")
    multiple = complete.copy()
    multiple[BASE_VARIABLES + 1] = BASE_VARIABLES + 2
    require_failure(lambda: validate_model(
        variables, tautologies, multiple, len(members)), "multiple true selectors")
    print("PASS complete first/last attribution and hostile full/partial selector models")

    baseline = path.read_text(encoding="ascii").splitlines()

    def mutate(label, edit, clause_delta=0):
        lines = baseline.copy()
        header = next(i for i, line in enumerate(lines) if line.startswith("p cnf "))
        edit(lines, header)
        if clause_delta:
            header = next(i for i, line in enumerate(lines) if line.startswith("p cnf "))
            fields = lines[header].split()
            fields[3] = str(int(fields[3]) + clause_delta)
            lines[header] = " ".join(fields)
        mutated = directory / f"mutation-{label}.cnf"
        mutated.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        require_failure(lambda: check(mutated, COVER, FILTER), label)

    base_count = producer.child.parent.BASE_CLAUSES["B7"]
    common_count = 16
    first_clause = lambda header, offset: header + 1 + offset
    mutate("base", lambda lines, header: lines.__setitem__(first_clause(header, 0), "-2 0"))
    mutate("common", lambda lines, header: lines.__setitem__(
        first_clause(header, base_count),
        str(-int(lines[first_clause(header, base_count)].split()[0])) + " 0"))
    mutate("alo-delete", lambda lines, header: lines.pop(
        first_clause(header, base_count + common_count)), -1)
    mutate("alo-extra-selector", lambda lines, header: lines.__setitem__(
        first_clause(header, base_count + common_count),
        lines[first_clause(header, base_count + common_count)].replace(" 0", " 1 0")))
    guarded_start = base_count + common_count + 1
    mutate("guard-polarity", lambda lines, header: lines.__setitem__(
        first_clause(header, guarded_start),
        " ".join([str(-int(lines[first_clause(header, guarded_start)].split()[0]))] +
                 lines[first_clause(header, guarded_start)].split()[1:])))
    mutate("guard-reorder", lambda lines, header: lines.__setitem__(
        slice(first_clause(header, guarded_start), first_clause(header, guarded_start) + 2),
        lines[first_clause(header, guarded_start):first_clause(header, guarded_start) + 2][::-1]))
    mutate("guard-append", lambda lines, header: lines.append(lines[-1]), 1)
    mutate("metadata", lambda lines, header: lines.__setitem__(
        next(i for i, line in enumerate(lines) if line.startswith("c group-key ")),
        "c group-key B7-q4"))
    mutate("selector-name", lambda lines, header: lines.__setitem__(
        next(i for i, line in enumerate(lines) if line.startswith("c var 23617 ")),
        "c var 23617 wrong_selector"))
    print("PASS hostile mutations base/common/ALO/guards/metadata/selectors")

    mutated_proof = directory / "mutated-human-proof.md"
    mutated_proof.write_bytes(HUMAN_PROOF.read_bytes() + b"\n")
    require_failure(lambda: producer.manifest_payload(producer_groups, mutated_proof),
                    "producer proof-file mutation")
    require_failure(lambda: manifest_payload(checker_groups, mutated_proof),
                    "checker proof-file mutation")
    require_failure(lambda: check(path, COVER, FILTER, proof_path=mutated_proof),
                    "gate proof-file mutation")
    print("PASS excluded human-proof identity and mutation rejection")

print("PASS m6 forced selector group CNF tests")
