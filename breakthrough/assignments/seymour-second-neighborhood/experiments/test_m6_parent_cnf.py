#!/usr/bin/env python3
"""Boundary and all-placement regression tests for frozen m=6 parent CNFs."""

import subprocess
import sys
import tempfile
from pathlib import Path

import m6_parent_cnf as producer
from check_m6_parent_cnf import (
    check, expected_projection, graph6_edges, read_acceptance, read_cover,
)

HERE = Path(__file__).resolve().parent
COVER = HERE / "m6-placement-cover.txt"
FILTER = HERE / "m6-placement-filter.txt"


rows = read_cover(COVER)
statuses = read_acceptance(FILTER)
accepted = [index for index, status in enumerate(statuses) if status == 0]
if len(accepted) != producer.ACCEPTED_ROWS:
    raise RuntimeError("wrong accepted-row total")


def require_failure(action, label):
    try:
        action()
    except (RuntimeError, ValueError, IndexError, UnicodeError):
        return
    raise RuntimeError(f"mutation was accepted: {label}")


for ordinal in (-1, producer.ACCEPTED_ROWS):
    require_failure(lambda ordinal=ordinal: producer.select_row(rows, statuses, ordinal, None),
                    f"accepted ordinal {ordinal}")
for index in (-1, len(rows), next(i for i, status in enumerate(statuses) if status != 0)):
    require_failure(lambda index=index: producer.select_row(rows, statuses, None, index),
                    f"cover index {index}")
require_failure(lambda: producer.select_row(rows, statuses, None, None), "missing selector")
require_failure(lambda: producer.select_row(rows, statuses, 0, accepted[0]), "double selector")
print("PASS selector negative and bounds tests")

sample_code = rows[accepted[0]][3]
for malformed in ("", sample_code + "?", "~" + sample_code[1:], sample_code[:-1]):
    require_failure(lambda malformed=malformed: producer.decode_graph6(malformed),
                    f"producer graph6 {malformed!r}")
    require_failure(lambda malformed=malformed: graph6_edges(malformed),
                    f"checker graph6 {malformed!r}")
padding_code = next(row[3] for row in rows if row[2] * (row[2] - 1) // 2 % 6)
padding_mutation = padding_code[:-1] + chr(((ord(padding_code[-1]) - 63) | 1) + 63)
require_failure(lambda: producer.decode_graph6(padding_mutation), "producer graph6 padding")
require_failure(lambda: graph6_edges(padding_mutation), "checker graph6 padding")
print("PASS strict graph6 parser tests")

# Exercise deterministic embedding on every support type and every frozen cell
# occupancy without paying for 76,361 copies of the large base CNF.
seen_supports = set()
seen_occupancies = set()
for index in accepted:
    row = rows[index]
    image, expected_holes = expected_projection(row)
    branch, support, _, _, word, _, edges = row
    actual_image, actual_holes = producer.embedded_holes(branch, word, edges)
    if image != actual_image or expected_holes != set(actual_holes):
        raise RuntimeError(f"embedding disagreement at accepted cover row {index}")
    seen_supports.add(support)
    seen_occupancies.add((branch, tuple(word.count(cell) for cell in "RABC")))
if seen_supports != set(range(68)):
    raise RuntimeError(f"accepted rows omit support types {set(range(68)) - seen_supports}")
print(f"PASS direct embeddings accepted={len(accepted)} supports={len(seen_supports)} occupancies={len(seen_occupancies)}")

last_b6 = max(index for index in accepted if rows[index][0] == "B6")
first_b7 = min(index for index in accepted if rows[index][0] == "B7")
fixtures = (
    ("accepted-zero-hole-isolated", "--accepted-ordinal", "0", accepted[0]),
    ("accepted-row17", "--cover-index", "17", 17),
    ("last-b6-order12", "--cover-index", str(last_b6), last_b6),
    ("first-b7-hole-isolated", "--cover-index", str(first_b7), first_b7),
    ("final-accepted-order12", "--accepted-ordinal", str(len(accepted) - 1), accepted[-1]),
)
if fixtures[0][3] != 2 or statuses[17] != 0 or last_b6 != 112219 or first_b7 != 112221 or accepted[-1] != 187323:
    raise RuntimeError("frozen boundary identities changed")
if rows[last_b6][2] != 12 or rows[accepted[-1]][2] != 12:
    raise RuntimeError("order-12 boundary fixtures changed")
for _, _, _, index in (fixtures[0], fixtures[3]):
    branch, _, _, _, word, _, _ = rows[index]
    if all(word.count(cell) == len(producer.CELL_LABELS[branch][i]) for i, cell in enumerate("RABC")):
        raise RuntimeError("hole-isolated fixture no longer omits a full-graph vertex")

with tempfile.TemporaryDirectory(prefix="m6-parent-") as directory:
    baseline = None
    for name, option, value, expected_index in fixtures:
        output = Path(directory) / f"{name}.cnf"
        commands = (
            [sys.executable, str(HERE / "m6_parent_cnf.py"), option, value, "--output", str(output)],
            [sys.executable, str(HERE / "check_m6_parent_cnf.py"), str(output)],
        )
        for command in commands:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError((command, result.stdout, result.stderr))
            if result.stdout.strip():
                print(result.stdout.strip())
        if f"cover_index={expected_index}" not in result.stdout:
            raise RuntimeError(f"checker selected wrong fixture for {name}")
        if baseline is None:
            baseline = output.read_text(encoding="ascii").splitlines()

    header = next(i for i, line in enumerate(baseline) if line.startswith("p cnf "))
    fields = baseline[header].split()
    declared_clauses = int(fields[3])
    base_start = header + 1
    base_end = base_start + producer.BASE_CLAUSES["B6"]

    def mutated(label, edit, clause_delta=0):
        lines = baseline.copy()
        edit(lines)
        if clause_delta:
            header_index = next(i for i, line in enumerate(lines) if line.startswith("p cnf "))
            parts = lines[header_index].split()
            parts[3] = str(declared_clauses + clause_delta)
            lines[header_index] = " ".join(parts)
        path = Path(directory) / f"mutation-{label}.cnf"
        path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        require_failure(lambda: check(path, COVER, FILTER), label)

    mutated("base-alter", lambda lines: lines.__setitem__(base_start, "-2 0"))
    mutated("base-delete", lambda lines: lines.pop(base_start), -1)
    mutated("base-append", lambda lines: lines.insert(base_end, lines[base_start]), 1)
    mutated("base-reorder", lambda lines: lines.__setitem__(slice(base_start, base_start + 2),
                                                            lines[base_start:base_start + 2][::-1]))
    first_var = next(i for i, line in enumerate(baseline) if line.startswith("c var "))
    second_var = first_var + 1
    mutated("duplicate-name", lambda lines: lines.__setitem__(
        second_var, " ".join(lines[second_var].split()[:3] + [lines[first_var].split()[3]])))
    mutated("variable-zero", lambda lines: lines.__setitem__(first_var,
                                                              lines[first_var].replace("c var 1 ", "c var 0 ", 1)))
    mutated("variable-gap", lambda lines: lines.__setitem__(second_var,
                                                             lines[second_var].replace("c var 2 ", "c var 3 ", 1)))
    mutated("comment-after-header", lambda lines: lines.insert(base_start, "c hostile"))
    metadata_first = 0
    mutated("metadata-reorder", lambda lines: lines.__setitem__(
        slice(metadata_first, metadata_first + 2), lines[metadata_first:metadata_first + 2][::-1]))
    mutated("metadata-extra", lambda lines: lines.insert(header, "c extra forbidden"))
    mutated("metadata-after-map", lambda lines: lines.insert(first_var + 1, lines.pop(0)))
    suffix_start = base_end
    mutated("unit-alter", lambda lines: lines.__setitem__(suffix_start,
                                                          str(-int(lines[suffix_start].split()[0])) + " 0"))
    mutated("unit-delete", lambda lines: lines.pop(suffix_start), -1)
    mutated("unit-append", lambda lines: lines.append(lines[-1]), 1)
    mutated("unit-reorder", lambda lines: lines.__setitem__(
        slice(suffix_start, suffix_start + 2), lines[suffix_start:suffix_start + 2][::-1]))
    print("PASS hostile CNF mutation tests base=4 map=3 framing=4 units=4")
print("PASS m6 parent CNF boundary fixtures")
