#!/usr/bin/env python3
"""Exhaustive embedding, boundary-CNF, and mutation tests for forced m=6 children."""

import hashlib
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import m6_forced_child_cnf as producer
from check_m6_forced_child_cnf import (
    MANIFEST_BYTES, MANIFEST_SHA256, check, eligible_indices, manifest_payload,
    parameters, read_acceptance, read_cover,
)

HERE = Path(__file__).resolve().parent
COVER = HERE / "m6-placement-cover.txt"
FILTER = HERE / "m6-placement-filter.txt"


def require_failure(action, label):
    try:
        action()
    except (RuntimeError, ValueError, IndexError, UnicodeError):
        return
    raise RuntimeError(f"mutation was accepted: {label}")


checker_rows = read_cover(COVER)
statuses = read_acceptance(FILTER)
checker_eligible = eligible_indices(checker_rows, statuses)
manifest = manifest_payload(checker_rows, checker_eligible)
if len(manifest) != MANIFEST_BYTES or hashlib.sha256(manifest).hexdigest() != MANIFEST_SHA256:
    raise RuntimeError("independent manifest bytes or hash changed")
print(f"PASS manifest rows={len(checker_eligible)} bytes={len(manifest)} sha256={MANIFEST_SHA256}")

producer_rows = producer.parent.load_cover(COVER)
producer_statuses = producer.parent.load_statuses(FILTER)
producer_eligible = producer.eligible_rows(producer_rows, producer_statuses)
if [(accepted, row["cover_index"]) for accepted, row in producer_eligible] != checker_eligible:
    raise RuntimeError("producer and independent checker eligible manifests disagree")

parameter_counts = Counter()
seen_supports = set()
seen_occupancies = set()
for child, ((accepted, row), (checked_accepted, index)) in enumerate(
        zip(producer_eligible, checker_eligible)):
    branch, lam, q, h = parameters(checker_rows[index])
    if accepted != checked_accepted or producer.hole_parameters(row) != (lam, q, h):
        raise RuntimeError(f"parameter disagreement at child ordinal {child}")
    producer_image, producer_holes = producer.parent.embedded_holes(
        branch, row["word"], row["edges"])
    from check_m6_parent_cnf import expected_projection
    checker_image, checker_holes = expected_projection(checker_rows[index])
    if producer_image != checker_image or set(producer_holes) != checker_holes:
        raise RuntimeError(f"embedding disagreement at child ordinal {child}")
    parameter_counts[branch, lam, q, h] += 1
    seen_supports.add(row["support"])
    seen_occupancies.add((branch, tuple(row["word"].count(cell) for cell in "RABC")))

expected_parameters = Counter({
    ("B6", 3, 0, 3): 6286,
    ("B6", 3, 1, 2): 5541,
    ("B6", 3, 2, 1): 2410,
    ("B6", 3, 3, 0): 412,
    ("B7", 1, 0, 5): 8847,
    ("B7", 1, 1, 4): 9577,
    ("B7", 1, 2, 3): 5431,
    ("B7", 1, 3, 2): 1584,
    ("B7", 1, 4, 1): 297,
    ("B7", 1, 5, 0): 30,
})
if parameter_counts != expected_parameters:
    raise RuntimeError(f"eligible parameter partition changed: {parameter_counts}")
print(
    f"PASS all eligible embeddings={len(producer_eligible)} supports={len(seen_supports)} "
    f"occupancies={len(seen_occupancies)} parameter_cells={len(parameter_counts)}"
)

for selector in (-1, len(producer_eligible)):
    require_failure(lambda selector=selector: producer.select_eligible(
        producer_eligible, child_ordinal=selector), f"child ordinal {selector}")
for field, value in (("accepted_ordinal", 1), ("cover_index", 0)):
    require_failure(lambda field=field, value=value: producer.select_eligible(
        producer_eligible, **{field: value}), f"ineligible {field}")
require_failure(lambda: producer.select_eligible(producer_eligible), "missing selector")
require_failure(lambda: producer.select_eligible(
    producer_eligible, child_ordinal=0, cover_index=2), "double selector")
print("PASS selector bounds and ineligible-parent tests")

branch_boundary = next(i for i, (_, row) in enumerate(producer_eligible) if row["branch"] == "B7")
if branch_boundary != 14649:
    raise RuntimeError("eligible branch boundary changed")
fixture_ordinals = (0, branch_boundary - 1, branch_boundary, len(producer_eligible) - 1)
expected_hashes = {}

with tempfile.TemporaryDirectory(prefix="m6-forced-child-") as directory:
    baselines = {}
    for child in fixture_ordinals:
        output = Path(directory) / f"child-{child}.cnf"
        for command in (
            [sys.executable, str(HERE / "m6_forced_child_cnf.py"),
             "--child-ordinal", str(child), "--output", str(output)],
            [sys.executable, str(HERE / "check_m6_forced_child_cnf.py"), str(output)],
        ):
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError((command, result.stdout, result.stderr))
        branch = producer_eligible[child][1]["branch"]
        baselines.setdefault(branch, output.read_text(encoding="ascii").splitlines())
        expected_hashes[child] = hashlib.sha256(output.read_bytes()).hexdigest()
        print(result.stdout.strip())
    print("PASS boundary CNF sha256 " + " ".join(
        f"{child}:{expected_hashes[child]}" for child in fixture_ordinals))

    def mutate(branch, label, edit, clause_delta=0):
        lines = baselines[branch].copy()
        header = next(i for i, line in enumerate(lines) if line.startswith("p cnf "))
        original_clauses = int(lines[header].split()[3])
        edit(lines, header)
        if clause_delta:
            header = next(i for i, line in enumerate(lines) if line.startswith("p cnf "))
            fields = lines[header].split()
            fields[3] = str(original_clauses + clause_delta)
            lines[header] = " ".join(fields)
        path = Path(directory) / f"mutation-{branch}-{label}.cnf"
        path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        require_failure(lambda: check(path, COVER, FILTER), f"{branch} {label}")

    for branch in ("B6", "B7"):
        base_count = producer.parent.BASE_CLAUSES[branch]
        parent_count = base_count + len(producer.parent.PAIRS)

        def clause_position(lines, header, offset):
            return header + 1 + offset

        mutate(branch, "base-alter", lambda lines, header: lines.__setitem__(
            clause_position(lines, header, 0), "-2 0"))
        mutate(branch, "hole-alter", lambda lines, header: lines.__setitem__(
            clause_position(lines, header, base_count),
            str(-int(lines[clause_position(lines, header, base_count)].split()[0])) + " 0"))
        mutate(branch, "orientation-alter", lambda lines, header: lines.__setitem__(
            clause_position(lines, header, parent_count),
            str(-int(lines[clause_position(lines, header, parent_count)].split()[0])) + " 0"))
        mutate(branch, "high-alter", lambda lines, header: lines.__setitem__(
            len(lines) - 1, str(-int(lines[-1].split()[0])) + " 0"))
        mutate(branch, "suffix-delete", lambda lines, header: lines.pop(
            clause_position(lines, header, parent_count)), -1)
        mutate(branch, "suffix-append", lambda lines, header: lines.append(lines[-1]), 1)
        mutate(branch, "suffix-reorder", lambda lines, header: lines.__setitem__(
            slice(clause_position(lines, header, parent_count),
                  clause_position(lines, header, parent_count) + 2),
            lines[clause_position(lines, header, parent_count):
                  clause_position(lines, header, parent_count) + 2][::-1]))
        mutate(branch, "metadata-lambda", lambda lines, header: lines.__setitem__(
            next(i for i, line in enumerate(lines) if line.startswith("c lambda ")), "c lambda 9"))
        mutate(branch, "metadata-manifest", lambda lines, header: lines.__setitem__(
            next(i for i, line in enumerate(lines) if line.startswith("c eligible-manifest-sha256 ")),
            "c eligible-manifest-sha256 " + "0" * 64))
    print("PASS hostile mutations branches=2 base=2 parent-hole=2 orientation=2 high=2 suffix=6 metadata=4")

print("PASS m6 forced child CNF tests")
