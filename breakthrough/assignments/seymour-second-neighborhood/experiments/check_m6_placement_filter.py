#!/usr/bin/env python3
"""Independent formula and partition audit for the frozen m=6 placement filter."""

import argparse
import base64
import hashlib
import itertools
from collections import Counter
from pathlib import Path

COVER_ROWS = 187324
COVER_BYTES = 6659672
COVER_SHA256 = "22d7744f1eecee3ea22527e4beec645ae999c912184f1f23c1a7f701e966ed5e"
LEDGER_BYTES = 95083
LEDGER_SHA256 = "9bfd2fadda610dde6cef7c13956edba6b0fa763e2ffc31226c0ddf1323fd1d0c"
CELLS = {"B6": (1, 8, 6, 3), "B7": (1, 8, 7, 2)}
NAMES = ("ACCEPT", "B_NO_PRESENT_A", "A_OUT_CAPACITY", "C_LOCAL_CAPACITY",
         "B6_C_HOLES", "C_DEGREE_DP")


def graph_edges(code):
    n = ord(code[0]) - 63
    stream = []
    for char in code[1:]:
        number = ord(char) - 63
        stream += [bool(number & mask) for mask in (32, 16, 8, 4, 2, 1)]
    pairs = [(x, y) for y in range(1, n) for x in range(y)]
    return n, {pair for pair, bit in zip(pairs, stream) if bit}


def read_rows(path):
    raw = path.read_bytes()
    if len(raw) != COVER_BYTES or hashlib.sha256(raw).hexdigest() != COVER_SHA256:
        raise RuntimeError("placement cover is not the frozen payload")
    result = []
    lines = raw.decode("ascii").splitlines()
    if len(lines) != COVER_ROWS + 7:
        raise RuntimeError("wrong cover line count")
    for index, line in enumerate(lines[7:]):
        fields = line.split("\t")
        if len(fields) != 7 or fields[0] != f"{index:07d}":
            raise RuntimeError(f"bad cover row {index}")
        branch, order_text, code, colors = fields[1], fields[3], fields[4], fields[5]
        order, holes = graph_edges(code)
        if branch not in CELLS or order != int(order_text) or len(colors) != order or len(holes) != 6:
            raise RuntimeError(f"bad cover identity at row {index}")
        result.append((branch, colors, holes))
    return result


def exact_c_degrees(branch, colors, holes):
    full_colors = list(colors)
    for color, size in zip("RABC", CELLS[branch]):
        full_colors.extend(color for _ in range(size - colors.count(color)))
    cs = [v for v, color in enumerate(full_colors) if color == "C"]

    def present(x, y):
        return tuple(sorted((x, y))) not in holes

    fixed = [
        sum(full_colors[v] in "RA" and present(c, v) for v in range(len(full_colors)))
        for c in cs
    ]
    available_b = [
        sum(full_colors[v] == "B" and present(c, v) for v in range(len(full_colors)))
        for c in cs
    ]
    present_cc = [(x, y) for x, y in itertools.combinations(cs, 2) if present(x, y)]
    for directions in itertools.product((0, 1), repeat=len(present_cc)):
        lower = list(fixed)
        for pair, direction in zip(present_cc, directions):
            lower[cs.index(pair[direction])] += 1
        for targets in itertools.product((8, 9), repeat=len(cs)):
            if sum(target == 9 for target in targets) > 3:
                continue
            if all(lower[i] <= targets[i] <= lower[i] + available_b[i] for i in range(len(cs))):
                return True
    return False


def formula_status(branch, colors, holes):
    r_size, a_size, b_size, c_size = CELLS[branch]
    by_vertex = [Counter() for _ in colors]
    pair_count = Counter()
    for x, y in holes:
        by_vertex[x][colors[y]] += 1
        by_vertex[y][colors[x]] += 1
        pair_count[frozenset((colors[x], colors[y]))] += 1
    if any(colors[v] == "B" and by_vertex[v]["A"] == a_size for v in range(len(colors))):
        return 1
    if any(colors[v] == "A" and
           (a_size - 1 + b_size - by_vertex[v]["A"] - by_vertex[v]["B"] < 8)
           for v in range(len(colors))):
        return 2
    full_colors = list(colors)
    for color, size in zip("RABC", CELLS[branch]):
        full_colors.extend(color for _ in range(size - colors.count(color)))
    for v, color in enumerate(full_colors):
        if color != "C":
            continue
        hole_counts = by_vertex[v] if v < len(colors) else Counter()
        forced = r_size + a_size - hole_counts["R"] - hole_counts["A"]
        total = forced + b_size + c_size - 1 - hole_counts["B"] - hole_counts["C"]
        if forced > 9 or total < 8:
            return 3
    c_holes = sum(pair_count[frozenset(pair)] for pair in (("R", "C"), ("A", "C"), ("C",)))
    if branch == "B6" and c_holes < 3:
        return 4
    return 0 if exact_c_degrees(branch, colors, holes) else 5


def read_ledger(path):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if len(raw) != LEDGER_BYTES or digest != LEDGER_SHA256:
        raise RuntimeError(f"filter ledger changed: bytes={len(raw)} sha256={digest}")
    lines = raw.decode("ascii").splitlines()
    expected = [
        "m6-placement-filter-v1",
        f"cover-rows\t{COVER_ROWS}",
        f"cover-bytes\t{COVER_BYTES}",
        f"cover-sha256\t{COVER_SHA256}",
        "reason-codes\t" + ";".join(f"{i}:{name}" for i, name in enumerate(NAMES)),
    ]
    if lines[:5] != expected or len(lines) < 9:
        raise RuntimeError("bad filter ledger header")
    declared_counts = {}
    for field in lines[5].removeprefix("reason-counts\t").split(";"):
        code, count = field.split(":")
        declared_counts[int(code)] = int(count)
    branch_counts = {}
    for branch_field in lines[6].removeprefix("branch-reason-counts\t").split(";"):
        branch, fields = branch_field.split(":", 1)
        for field in fields.split(","):
            code, count = field.split(":")
            branch_counts[branch, int(code)] = int(count)
    if lines[7] != "encoding\tbase64-packed-3bit-lsb-first":
        raise RuntimeError("unknown ledger encoding")
    declared_bytes = int(lines[8].removeprefix("payload-bytes\t"))
    try:
        packed = base64.b64decode("".join(lines[9:]), validate=True)
    except ValueError as error:
        raise RuntimeError("invalid base64 status payload") from error
    if len(packed) != declared_bytes or declared_bytes != (3 * COVER_ROWS + 7) // 8:
        raise RuntimeError("wrong packed status size")
    statuses = []
    accumulator = 0
    width = 0
    for byte in packed:
        accumulator |= byte << width
        width += 8
        while width >= 3 and len(statuses) < COVER_ROWS:
            statuses.append(accumulator & 7)
            accumulator >>= 3
            width -= 3
    if (len(statuses) != COVER_ROWS or accumulator or
            any(reason not in range(len(NAMES)) for reason in statuses)):
        raise RuntimeError("packed statuses do not form an exact row partition")
    if Counter(statuses) != Counter(declared_counts):
        raise RuntimeError("ledger counts/partition mismatch")
    return statuses, branch_counts, raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--cover", type=Path, default=Path(__file__).with_name("m6-placement-cover.txt"))
    args = parser.parse_args()
    rows = read_rows(args.cover)
    recorded, declared_branch_counts, raw = read_ledger(args.ledger)
    audited = [formula_status(*row) for row in rows]
    if audited != recorded:
        index = next(i for i, pair in enumerate(zip(audited, recorded)) if pair[0] != pair[1])
        raise RuntimeError(f"status mismatch at row {index}: formula={audited[index]} ledger={recorded[index]}")
    counts = Counter(audited)
    branch_counts = Counter((row[0], status) for row, status in zip(rows, audited))
    if branch_counts != Counter(declared_branch_counts):
        raise RuntimeError("branch reason counts do not match audited rows")
    print(f"PASS rows={len(rows)} bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}")
    print("counts=" + ",".join(f"{NAMES[i]}:{counts[i]}" for i in range(len(NAMES))))


if __name__ == "__main__":
    main()
