#!/usr/bin/env python3
"""Independent frozen-row and hole-projection checker for an m=6 parent CNF."""

import argparse
import base64
import hashlib
from collections import Counter
from pathlib import Path

from snc_cnf import generate

HERE = Path(__file__).resolve().parent
COVER_ROWS = 187324
COVER_BYTES = 6659672
COVER_SHA256 = "22d7744f1eecee3ea22527e4beec645ae999c912184f1f23c1a7f701e966ed5e"
FILTER_BYTES = 95083
FILTER_SHA256 = "9bfd2fadda610dde6cef7c13956edba6b0fa763e2ffc31226c0ddf1323fd1d0c"
BASE_VARIABLES = 23616
BASE_VARIABLE_MAP_SHA256 = "cff4c18a4425f26c188790871da51a58b13569764bf89c83d1c736d5f9db070e"
BASE_CLAUSES = {"B6": 142736, "B7": 142729}
BASE_CLAUSE_SHA256 = {
    "B6": "22b118674d05045d0a1c8628ccb5b9a7f72fbcd53f6086ecab1b2ab369ca12c1",
    "B7": "a21d68c9a70642ad15b836d162996779d0b4ee4590a7bccd7f3af54f394341ab",
}
PAIRS = tuple((low, high) for high in range(1, 18) for low in range(high))
LABELS = {
    "B6": {"R": range(0, 1), "A": range(1, 9), "B": range(9, 15), "C": range(15, 18)},
    "B7": {"R": range(0, 1), "A": range(1, 9), "B": range(9, 16), "C": range(16, 18)},
}


def graph6_edges(code):
    if not code or any(not 63 <= ord(character) <= 126 for character in code):
        raise RuntimeError("invalid graph6 character")
    n = ord(code[0]) - 63
    if not 0 <= n <= 62:
        raise RuntimeError("only short graph6 encoding is accepted")
    bit_count = n * (n - 1) // 2
    if len(code) != 1 + (bit_count + 5) // 6:
        raise RuntimeError("wrong graph6 payload length")
    stream = []
    for character in code[1:]:
        number = ord(character) - 63
        stream.extend(bool(number & bit) for bit in (32, 16, 8, 4, 2, 1))
    if any(stream[bit_count:]):
        raise RuntimeError("nonzero graph6 padding")
    pairs = [(x, y) for y in range(1, n) for x in range(y)]
    return n, {pair for pair, present in zip(pairs, stream[:bit_count]) if present}


def read_cover(path):
    raw = path.read_bytes()
    if len(raw) != COVER_BYTES or hashlib.sha256(raw).hexdigest() != COVER_SHA256:
        raise RuntimeError("cover is not the frozen payload")
    lines = raw.decode("ascii").splitlines()
    if (len(lines) != COVER_ROWS + 7 or lines[0] != "m6-rooted-cell-placement-cover-v1" or
            lines[5] != f"count\t{COVER_ROWS}"):
        raise RuntimeError("bad frozen cover framing")
    rows = []
    for index, line in enumerate(lines[7:]):
        fields = line.split("\t")
        if len(fields) != 7 or fields[0] != f"{index:07d}":
            raise RuntimeError(f"bad cover row {index}")
        order, holes = graph6_edges(fields[4])
        if order != int(fields[3]) or len(fields[5]) != order or len(holes) != 6:
            raise RuntimeError(f"bad support at cover row {index}")
        rows.append((fields[1], int(fields[2]), order, fields[4], fields[5], int(fields[6]), holes))
    return rows


def read_acceptance(path):
    raw = path.read_bytes()
    if len(raw) != FILTER_BYTES or hashlib.sha256(raw).hexdigest() != FILTER_SHA256:
        raise RuntimeError("filter is not the frozen payload")
    lines = raw.decode("ascii").splitlines()
    if (lines[0] != "m6-placement-filter-v1" or lines[1] != f"cover-rows\t{COVER_ROWS}" or
            lines[7] != "encoding\tbase64-packed-3bit-lsb-first" or
            lines[8] != "payload-bytes\t70247"):
        raise RuntimeError("bad frozen filter framing")
    packed = base64.b64decode("".join(lines[9:]), validate=True)
    statuses = []
    buffer = available = 0
    for byte in packed:
        buffer += byte << available
        available += 8
        while available >= 3 and len(statuses) < COVER_ROWS:
            statuses.append(buffer & 7)
            buffer >>= 3
            available -= 3
    if (len(statuses) != COVER_ROWS or buffer or
            Counter(statuses) != Counter({0: 76361, 2: 7, 4: 85134, 5: 25822})):
        raise RuntimeError("filter is not the declared exact partition")
    return statuses


def expected_projection(row):
    branch, _, _, _, word, _, support_holes = row
    pools = LABELS[branch]
    positions = Counter()
    image = {}
    for vertex, cell in enumerate(word):
        choices = pools[cell]
        offset = positions[cell]
        if offset >= len(choices):
            raise RuntimeError("cover placement exceeds cell capacity")
        image[vertex] = choices[offset]
        positions[cell] += 1
    holes = {
        tuple(sorted((image[left], image[right]))) for left, right in support_holes
    }
    if len(holes) != 6:
        raise RuntimeError("projection collapsed a support edge")
    return image, holes


def parse_cnf(path):
    metadata = []
    variables = []
    names = set()
    declared = None
    clauses = []
    preamble_phase = "metadata"
    with path.open("r", encoding="ascii") as handle:
        for line_number, raw_line in enumerate(handle, 1):
            line = raw_line.rstrip("\n")
            if not line:
                raise RuntimeError(f"blank CNF line {line_number}")
            if line.startswith("c var "):
                if declared is not None:
                    raise RuntimeError(f"comment after DIMACS header line {line_number}")
                preamble_phase = "variables"
                fields = line.split(" ", 3)
                if len(fields) != 4 or not fields[3]:
                    raise RuntimeError(f"bad variable line {line_number}")
                try:
                    number = int(fields[2])
                except ValueError as error:
                    raise RuntimeError(f"bad variable number line {line_number}") from error
                if number != len(variables) + 1 or fields[3] in names:
                    raise RuntimeError(f"noncanonical variable map line {line_number}")
                variables.append(fields[3])
                names.add(fields[3])
            elif line.startswith("c "):
                if declared is not None:
                    raise RuntimeError(f"comment after DIMACS header line {line_number}")
                if preamble_phase != "metadata":
                    raise RuntimeError(f"metadata after variable map line {line_number}")
                key, separator, value = line[2:].partition(" ")
                if not separator or not key or any(old_key == key for old_key, _ in metadata):
                    raise RuntimeError(f"bad metadata line {line_number}")
                metadata.append((key, value))
            elif line.startswith("p cnf "):
                if declared is not None:
                    raise RuntimeError("duplicate DIMACS header")
                fields = line.split()
                if len(fields) != 4:
                    raise RuntimeError("bad DIMACS header")
                declared = int(fields[2]), int(fields[3])
            else:
                if declared is None:
                    raise RuntimeError("clause precedes DIMACS header")
                try:
                    literals = [int(field) for field in line.split()]
                except ValueError as error:
                    raise RuntimeError(f"noninteger clause line {line_number}") from error
                if not literals or literals[-1] != 0 or 0 in literals[:-1]:
                    raise RuntimeError(f"bad clause terminator line {line_number}")
                if any(abs(literal) > declared[0] for literal in literals[:-1]):
                    raise RuntimeError(f"literal out of range line {line_number}")
                clauses.append(tuple(literals[:-1]))
    if declared is None or len(variables) != declared[0] or len(clauses) != declared[1]:
        raise RuntimeError("DIMACS or variable count mismatch")
    return metadata, variables, clauses, declared


def variable_map_sha256(names):
    payload = "".join(f"{number} {name}\n" for number, name in enumerate(names, 1))
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def clause_sha256(clauses):
    payload = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def check(cnf_path, cover_path, filter_path):
    rows = read_cover(cover_path)
    statuses = read_acceptance(filter_path)
    metadata_items, variables, clauses, declared = parse_cnf(cnf_path)
    metadata = dict(metadata_items)
    required_keys = {
        "format", "cover-sha256", "filter-sha256", "accepted-ordinal", "cover-index",
        "branch", "b-size", "support-index", "support-order", "support-code",
        "placement", "orbit-weight", "embedding", "holes", "model", "base-variables",
        "base-variable-map-sha256", "base-clauses", "base-clause-sha256", "hole-units",
    }
    if set(metadata) != required_keys:
        raise RuntimeError("metadata does not have the exact required key set")
    index = int(metadata["cover-index"])
    ordinal = int(metadata["accepted-ordinal"])
    if not 0 <= index < COVER_ROWS or statuses[index] != 0:
        raise RuntimeError("metadata selects a rejected or absent cover row")
    if sum(status == 0 for status in statuses[:index]) != ordinal:
        raise RuntimeError("accepted ordinal and cover index disagree")
    row = rows[index]
    branch, support, order, code, word, weight, _ = row
    expected_fields = {
        "branch": branch, "b-size": "6" if branch == "B6" else "7",
        "support-index": str(support), "support-order": str(order),
        "support-code": code, "placement": word, "orbit-weight": str(weight),
    }
    for key, value in expected_fields.items():
        if metadata.get(key) != value:
            raise RuntimeError(f"row metadata mismatch for {key}")
    image, holes = expected_projection(row)
    expected_embedding = ",".join(f"{key}:{image[key]}" for key in sorted(image))
    expected_holes_text = ",".join(f"{x}-{y}" for x, y in sorted(holes))
    if metadata.get("embedding") != expected_embedding or metadata.get("holes") != expected_holes_text:
        raise RuntimeError("metadata projection is not the deterministic first-label embedding")
    expected_metadata = [
        ("format", "m6-parent-cnf-v1"), ("cover-sha256", COVER_SHA256),
        ("filter-sha256", FILTER_SHA256), ("accepted-ordinal", str(ordinal)),
        ("cover-index", str(index)), ("branch", branch),
        ("b-size", "6" if branch == "B6" else "7"), ("support-index", str(support)),
        ("support-order", str(order)), ("support-code", code), ("placement", word),
        ("orbit-weight", str(weight)), ("embedding", expected_embedding),
        ("holes", expected_holes_text),
        ("model", "generate(18,bsize,6,robust_witness=True,arc_minimal=True)"),
        ("base-variables", str(BASE_VARIABLES)),
        ("base-variable-map-sha256", BASE_VARIABLE_MAP_SHA256),
        ("base-clauses", str(BASE_CLAUSES[branch])),
        ("base-clause-sha256", BASE_CLAUSE_SHA256[branch]), ("hole-units", "153"),
    ]
    if metadata_items != expected_metadata:
        raise RuntimeError("metadata is not the exact canonical ordered set")

    base = generate(18, 6 if branch == "B6" else 7, 6,
                    robust_witness=True, arc_minimal=True)
    expected_names = [name for name, _ in base.names.items()]
    expected_base_clauses = list(base.clauses)
    if (len(expected_names) != BASE_VARIABLES or
            variable_map_sha256(expected_names) != BASE_VARIABLE_MAP_SHA256 or
            len(expected_base_clauses) != BASE_CLAUSES[branch] or
            clause_sha256(expected_base_clauses) != BASE_CLAUSE_SHA256[branch]):
        raise RuntimeError("reconstructed base does not match its frozen branch hashes")
    if variables != expected_names:
        raise RuntimeError("CNF variable map is not the exact ordered frozen base map")
    if clauses[:BASE_CLAUSES[branch]] != expected_base_clauses:
        raise RuntimeError("CNF base clause stream differs from the reconstructed frozen branch")
    expected_suffix = [
        (base.names[f"h_{left}_{right}"] if (left, right) in holes else
         -base.names[f"h_{left}_{right}"],)
        for left, right in PAIRS
    ]
    if clauses[BASE_CLAUSES[branch]:] != expected_suffix:
        raise RuntimeError("CNF does not end in the exact 153 hole units in pair order")
    print(
        f"PASS accepted_ordinal={ordinal} cover_index={index} branch={branch} "
        f"order={order} holes=6 hole_units=153 vars={declared[0]} clauses={declared[1]}"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--cover", type=Path, default=HERE / "m6-placement-cover.txt")
    parser.add_argument("--filter", type=Path, default=HERE / "m6-placement-filter.txt")
    args = parser.parse_args()
    check(args.cnf, args.cover, args.filter)


if __name__ == "__main__":
    main()
