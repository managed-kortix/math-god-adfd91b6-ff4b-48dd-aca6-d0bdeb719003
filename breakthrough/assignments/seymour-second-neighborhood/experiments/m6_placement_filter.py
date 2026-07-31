#!/usr/bin/env python3
"""Filter the frozen m=6 placement cover by exact placement-only predicates."""

import argparse
import base64
import hashlib
import sys
from collections import Counter
from pathlib import Path

COVER_ROWS = 187324
COVER_BYTES = 6659672
COVER_SHA256 = "22d7744f1eecee3ea22527e4beec645ae999c912184f1f23c1a7f701e966ed5e"
EXPECTED_BYTES = 95083
EXPECTED_SHA256 = "9bfd2fadda610dde6cef7c13956edba6b0fa763e2ffc31226c0ddf1323fd1d0c"
EXPECTED_COUNTS = (76361, 0, 7, 0, 85134, 25822)
CELL_SIZES = {"B6": {"R": 1, "A": 8, "B": 6, "C": 3},
              "B7": {"R": 1, "A": 8, "B": 7, "C": 2}}
REASONS = (
    "ACCEPT",
    "B_NO_PRESENT_A",
    "A_OUT_CAPACITY",
    "C_LOCAL_CAPACITY",
    "B6_C_HOLES",
    "C_DEGREE_DP",
)


def decode_graph6(code):
    order = ord(code[0]) - 63
    bits = []
    for char in code[1:]:
        value = ord(char) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    pairs = ((low, high) for high in range(1, order) for low in range(high))
    return order, frozenset(pair for pair, bit in zip(pairs, bits) if bit)


def load_cover(path):
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != COVER_BYTES or digest != COVER_SHA256:
        raise RuntimeError(f"frozen cover changed: bytes={len(data)} sha256={digest}")
    lines = data.decode("ascii").splitlines()
    if lines[:6] != [
        "m6-rooted-cell-placement-cover-v1",
        "supports\t68",
        "colors\tR,A,B,C",
        "forbidden\tR-A",
        "capacities\tB6:1,8,6,3;B7:1,8,7,2",
        f"count\t{COVER_ROWS}",
    ] or not lines[6].startswith("branch-orders\t"):
        raise RuntimeError("malformed frozen cover header")
    rows = []
    for expected, line in enumerate(lines[7:]):
        fields = line.split("\t")
        if len(fields) != 7 or fields[0] != f"{expected:07d}":
            raise RuntimeError(f"malformed frozen cover row {expected}")
        _, branch, support, stated_order, code, word, weight = fields
        order, edges = decode_graph6(code)
        if (branch not in CELL_SIZES or order != int(stated_order) or
                len(word) != order or any(cell not in "RABC" for cell in word) or
                len(edges) != 6 or int(weight) < 1):
            raise RuntimeError(f"invalid frozen cover row {expected}")
        rows.append((branch, int(support), word, edges))
    if len(rows) != COVER_ROWS:
        raise RuntimeError(f"expected {COVER_ROWS} rows, found {len(rows)}")
    return rows


def cell_holes(word, edges):
    incident = [{cell: 0 for cell in "RABC"} for _ in word]
    totals = Counter()
    for u, v in edges:
        left, right = word[u], word[v]
        incident[u][right] += 1
        incident[v][left] += 1
        totals["".join(sorted((left, right), key="RABC".index))] += 1
    return incident, totals


def c_degree_feasible(branch, word, edges):
    sizes = CELL_SIZES[branch]
    support_cs = [v for v, cell in enumerate(word) if cell == "C"]
    c_position = {v: i for i, v in enumerate(support_cs)}
    forced = [sizes["R"] + sizes["A"] for _ in range(sizes["C"])]
    flexible_b = [sizes["B"] for _ in range(sizes["C"])]
    cc_holes = set()
    for u, v in edges:
        cells = {word[u], word[v]}
        if cells == {"C", "R"} or cells == {"C", "A"}:
            c = u if word[u] == "C" else v
            forced[c_position[c]] -= 1
        elif cells == {"C", "B"}:
            c = u if word[u] == "C" else v
            flexible_b[c_position[c]] -= 1
        elif word[u] == word[v] == "C":
            cc_holes.add(tuple(sorted((c_position[u], c_position[v]))))

    present_cc = [
        (left, right)
        for right in range(1, sizes["C"])
        for left in range(right)
        if (left, right) not in cc_holes
    ]
    states = {tuple(forced)}
    for left, right in present_cc:
        next_states = set()
        for degrees in states:
            for tail in (left, right):
                updated = list(degrees)
                updated[tail] += 1
                next_states.add(tuple(updated))
        states = next_states
    for degrees in states:
        possible_high_counts = {0}
        for i, degree in enumerate(degrees):
            choices = []
            for target in (8, 9):
                if degree <= target <= degree + flexible_b[i]:
                    choices.append(target - 8)
            possible_high_counts = {
                old + choice for old in possible_high_counts for choice in choices
                if old + choice <= 3
            }
        if possible_high_counts:
            return True
    return False


def classify(branch, word, edges):
    sizes = CELL_SIZES[branch]
    incident, totals = cell_holes(word, edges)
    for vertex, cell in enumerate(word):
        if cell == "B" and incident[vertex]["A"] == sizes["A"]:
            return 1
    for vertex, cell in enumerate(word):
        if cell == "A":
            available = sizes["A"] - 1 + sizes["B"]
            available -= incident[vertex]["A"] + incident[vertex]["B"]
            if available < 8:
                return 2
    support_cs = [vertex for vertex, cell in enumerate(word) if cell == "C"]
    c_holes = [incident[vertex] for vertex in support_cs]
    c_holes.extend(Counter() for _ in range(sizes["C"] - len(support_cs)))
    for holes in c_holes:
        forced = sizes["R"] + sizes["A"] - holes["R"] - holes["A"]
        flexible = sizes["B"] + sizes["C"] - 1 - holes["B"] - holes["C"]
        if forced > 9 or forced + flexible < 8:
            return 3
    if branch == "B6" and totals["RC"] + totals["AC"] + totals["CC"] < 3:
        return 4
    if not c_degree_feasible(branch, word, edges):
        return 5
    return 0


def pack_statuses(statuses):
    packed = bytearray()
    accumulator = 0
    width = 0
    for status in statuses:
        accumulator |= status << width
        width += 3
        while width >= 8:
            packed.append(accumulator & 255)
            accumulator >>= 8
            width -= 8
    if width:
        packed.append(accumulator)
    return bytes(packed)


def encode_statuses(statuses, branch_statuses):
    packed = pack_statuses(statuses)
    counts = Counter(statuses)
    lines = [
        "m6-placement-filter-v1",
        f"cover-rows\t{COVER_ROWS}",
        f"cover-bytes\t{COVER_BYTES}",
        f"cover-sha256\t{COVER_SHA256}",
        "reason-codes\t" + ";".join(f"{i}:{name}" for i, name in enumerate(REASONS)),
        "reason-counts\t" + ";".join(f"{i}:{counts[i]}" for i in range(len(REASONS))),
        "branch-reason-counts\t" + ";".join(
            branch + ":" + ",".join(f"{i}:{branch_statuses[branch, i]}" for i in range(len(REASONS)))
            for branch in ("B6", "B7")
        ),
        "encoding\tbase64-packed-3bit-lsb-first",
        f"payload-bytes\t{len(packed)}",
    ]
    encoded = base64.b64encode(packed).decode("ascii")
    lines.extend(encoded[start:start + 96] for start in range(0, len(encoded), 96))
    return ("\n".join(lines) + "\n").encode("ascii"), counts


def make_payload(cover):
    rows = load_cover(cover)
    statuses = [classify(branch, word, edges) for branch, _, word, edges in rows]
    branch_statuses = Counter((row[0], status) for row, status in zip(rows, statuses))
    return encode_statuses(statuses, branch_statuses)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cover", type=Path, default=Path(__file__).with_name("m6-placement-cover.txt"))
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--output", type=Path)
    action.add_argument("--check", type=Path)
    args = parser.parse_args()
    data, counts = make_payload(args.cover)
    digest = hashlib.sha256(data).hexdigest()
    if (len(data) != EXPECTED_BYTES or digest != EXPECTED_SHA256 or
            tuple(counts[i] for i in range(len(REASONS))) != EXPECTED_COUNTS):
        raise RuntimeError(f"frozen filter changed: bytes={len(data)} sha256={digest} counts={counts}")
    if args.check:
        if args.check.read_bytes() != data:
            raise RuntimeError(f"payload differs: {args.check}")
        verb = "PASS"
    elif args.output:
        args.output.write_bytes(data)
        verb = "WROTE"
    else:
        sys.stdout.buffer.write(data)
        verb = "BUILT"
    print(f"{verb} rows={COVER_ROWS} bytes={len(data)} sha256={digest}", file=sys.stderr)
    print("counts=" + ",".join(f"{REASONS[i]}:{counts[i]}" for i in range(len(REASONS))), file=sys.stderr)


if __name__ == "__main__":
    main()
