#!/usr/bin/env python3
"""Emit one full order-18 CNF parent from the frozen accepted m=6 cover."""

import argparse
import base64
import hashlib
from collections import Counter
from pathlib import Path

from snc_cnf import generate

HERE = Path(__file__).resolve().parent
COVER = HERE / "m6-placement-cover.txt"
FILTER = HERE / "m6-placement-filter.txt"
COVER_ROWS = 187324
COVER_BYTES = 6659672
COVER_SHA256 = "22d7744f1eecee3ea22527e4beec645ae999c912184f1f23c1a7f701e966ed5e"
FILTER_BYTES = 95083
FILTER_SHA256 = "9bfd2fadda610dde6cef7c13956edba6b0fa763e2ffc31226c0ddf1323fd1d0c"
ACCEPTED_ROWS = 76361
BASE_VARIABLES = 23616
BASE_VARIABLE_MAP_SHA256 = "cff4c18a4425f26c188790871da51a58b13569764bf89c83d1c736d5f9db070e"
BASE_CLAUSES = {"B6": 142736, "B7": 142729}
BASE_CLAUSE_SHA256 = {
    "B6": "22b118674d05045d0a1c8628ccb5b9a7f72fbcd53f6086ecab1b2ab369ca12c1",
    "B7": "a21d68c9a70642ad15b836d162996779d0b4ee4590a7bccd7f3af54f394341ab",
}
PAIRS = tuple((low, high) for high in range(1, 18) for low in range(high))
CELL_LABELS = {
    "B6": ((0,), tuple(range(1, 9)), tuple(range(9, 15)), tuple(range(15, 18))),
    "B7": ((0,), tuple(range(1, 9)), tuple(range(9, 16)), tuple(range(16, 18))),
}


def decode_graph6(code):
    if not code or any(not 63 <= ord(char) <= 126 for char in code):
        raise ValueError("graph6 code contains an invalid character")
    order = ord(code[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("only short graph6 order encoding is accepted")
    bit_count = order * (order - 1) // 2
    if len(code) != 1 + (bit_count + 5) // 6:
        raise ValueError("graph6 code has the wrong encoded length")
    bits = []
    for char in code[1:]:
        value = ord(char) - 63
        bits.extend(bool(value & mask) for mask in (32, 16, 8, 4, 2, 1))
    if any(bits[bit_count:]):
        raise ValueError("graph6 code has nonzero padding bits")
    pairs = ((low, high) for high in range(1, order) for low in range(high))
    return order, frozenset(pair for pair, bit in zip(pairs, bits[:bit_count]) if bit)


def load_cover(path=COVER):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if len(raw) != COVER_BYTES or digest != COVER_SHA256:
        raise RuntimeError(f"frozen cover changed: bytes={len(raw)} sha256={digest}")
    lines = raw.decode("ascii").splitlines()
    expected = [
        "m6-rooted-cell-placement-cover-v1",
        "supports\t68",
        "colors\tR,A,B,C",
        "forbidden\tR-A",
        "capacities\tB6:1,8,6,3;B7:1,8,7,2",
        f"count\t{COVER_ROWS}",
    ]
    if lines[:6] != expected or not lines[6].startswith("branch-orders\t"):
        raise RuntimeError("malformed frozen cover header")
    rows = []
    for index, line in enumerate(lines[7:]):
        fields = line.split("\t")
        if len(fields) != 7 or fields[0] != f"{index:07d}":
            raise RuntimeError(f"malformed frozen cover row {index}")
        _, branch, support, stated_order, code, word, weight = fields
        order, edges = decode_graph6(code)
        capacity = CELL_LABELS.get(branch)
        if (capacity is None or order != int(stated_order) or len(word) != order or
                any(cell not in "RABC" for cell in word) or len(edges) != 6 or
                any(word.count(cell) > len(capacity[i]) for i, cell in enumerate("RABC")) or
                int(weight) < 1):
            raise RuntimeError(f"invalid frozen cover row {index}")
        rows.append({
            "cover_index": index, "branch": branch, "support": int(support),
            "order": order, "code": code, "word": word, "weight": int(weight),
            "edges": edges,
        })
    if len(rows) != COVER_ROWS:
        raise RuntimeError(f"expected {COVER_ROWS} cover rows, found {len(rows)}")
    return rows


def load_statuses(path=FILTER):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if len(raw) != FILTER_BYTES or digest != FILTER_SHA256:
        raise RuntimeError(f"frozen filter changed: bytes={len(raw)} sha256={digest}")
    lines = raw.decode("ascii").splitlines()
    expected = [
        "m6-placement-filter-v1",
        f"cover-rows\t{COVER_ROWS}",
        f"cover-bytes\t{COVER_BYTES}",
        f"cover-sha256\t{COVER_SHA256}",
        "reason-codes\t0:ACCEPT;1:B_NO_PRESENT_A;2:A_OUT_CAPACITY;3:C_LOCAL_CAPACITY;4:B6_C_HOLES;5:C_DEGREE_DP",
        "reason-counts\t0:76361;1:0;2:7;3:0;4:85134;5:25822",
        "branch-reason-counts\tB6:0:23578,1:0,2:7,3:0,4:85134,5:3501;B7:0:52783,1:0,2:0,3:0,4:0,5:22321",
        "encoding\tbase64-packed-3bit-lsb-first",
        "payload-bytes\t70247",
    ]
    if lines[:9] != expected:
        raise RuntimeError("malformed frozen filter header")
    try:
        packed = base64.b64decode("".join(lines[9:]), validate=True)
    except ValueError as error:
        raise RuntimeError("invalid frozen filter base64") from error
    if len(packed) != 70247:
        raise RuntimeError("wrong frozen filter payload length")
    statuses = []
    accumulator = width = 0
    for byte in packed:
        accumulator |= byte << width
        width += 8
        while width >= 3 and len(statuses) < COVER_ROWS:
            statuses.append(accumulator & 7)
            accumulator >>= 3
            width -= 3
    if (len(statuses) != COVER_ROWS or accumulator or
            Counter(statuses) != Counter({0: 76361, 2: 7, 4: 85134, 5: 25822})):
        raise RuntimeError("frozen filter does not decode to its exact partition")
    return statuses


def first_label_embedding(branch, word):
    """Map support labels to the first unused full-graph label in each cell."""
    labels = CELL_LABELS[branch]
    used = [0, 0, 0, 0]
    result = {}
    for vertex, cell in enumerate(word):
        cell_index = "RABC".index(cell)
        if used[cell_index] == len(labels[cell_index]):
            raise ValueError(f"placement exceeds {branch} {cell} capacity")
        result[vertex] = labels[cell_index][used[cell_index]]
        used[cell_index] += 1
    return result


def embedded_holes(branch, word, edges):
    embedding = first_label_embedding(branch, word)
    holes = frozenset(
        tuple(sorted((embedding[left], embedding[right]))) for left, right in edges
    )
    if len(holes) != 6:
        raise ValueError("support embedding did not produce six distinct holes")
    return embedding, holes


def select_row(rows, statuses, accepted_ordinal=None, cover_index=None):
    if (accepted_ordinal is None) == (cover_index is None):
        raise ValueError("select exactly one of accepted ordinal and cover index")
    if cover_index is not None:
        if not 0 <= cover_index < len(rows):
            raise ValueError("cover index out of range")
        if statuses[cover_index] != 0:
            raise ValueError(f"cover index {cover_index} is rejected with reason {statuses[cover_index]}")
        ordinal = sum(status == 0 for status in statuses[:cover_index])
        return ordinal, rows[cover_index]
    if not 0 <= accepted_ordinal < ACCEPTED_ROWS:
        raise ValueError("accepted ordinal out of range")
    seen = 0
    for row, status in zip(rows, statuses):
        if status == 0:
            if seen == accepted_ordinal:
                return seen, row
            seen += 1
    raise RuntimeError("accepted ordinal missing from frozen partition")


def build_parent(row):
    bsize = 6 if row["branch"] == "B6" else 7
    embedding, holes = embedded_holes(row["branch"], row["word"], row["edges"])
    cnf = generate(18, bsize, 6, robust_witness=True, arc_minimal=True)
    if (len(cnf.names) != BASE_VARIABLES or
            variable_map_sha256(cnf) != BASE_VARIABLE_MAP_SHA256 or
            len(cnf.clauses) != BASE_CLAUSES[row["branch"]] or
            clause_sha256(cnf.clauses) != BASE_CLAUSE_SHA256[row["branch"]]):
        raise RuntimeError("generated base CNF does not match the frozen branch")
    for pair in PAIRS:
        variable = cnf.var(f"h_{pair[0]}_{pair[1]}")
        cnf.add(variable if pair in holes else -variable)
    return cnf, embedding, holes


def variable_map_sha256(cnf):
    payload = "".join(f"{number} {name}\n" for name, number in cnf.names.items())
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def clause_sha256(clauses):
    payload = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def write_parent(path, cnf, ordinal, row, embedding, holes):
    metadata = [
        "format m6-parent-cnf-v1",
        f"cover-sha256 {COVER_SHA256}",
        f"filter-sha256 {FILTER_SHA256}",
        f"accepted-ordinal {ordinal}",
        f"cover-index {row['cover_index']}",
        f"branch {row['branch']}",
        f"b-size {6 if row['branch'] == 'B6' else 7}",
        f"support-index {row['support']}",
        f"support-order {row['order']}",
        f"support-code {row['code']}",
        f"placement {row['word']}",
        f"orbit-weight {row['weight']}",
        "embedding " + ",".join(f"{key}:{embedding[key]}" for key in sorted(embedding)),
        "holes " + ",".join(f"{left}-{right}" for left, right in sorted(holes)),
        "model generate(18,bsize,6,robust_witness=True,arc_minimal=True)",
        f"base-variables {BASE_VARIABLES}",
        f"base-variable-map-sha256 {BASE_VARIABLE_MAP_SHA256}",
        f"base-clauses {BASE_CLAUSES[row['branch']]}",
        f"base-clause-sha256 {BASE_CLAUSE_SHA256[row['branch']]}",
        "hole-units 153",
    ]
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for line in metadata:
            handle.write(f"c {line}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--accepted-ordinal", type=int)
    selector.add_argument("--cover-index", type=int)
    parser.add_argument("--cover", type=Path, default=COVER)
    parser.add_argument("--filter", type=Path, default=FILTER)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = load_cover(args.cover)
    statuses = load_statuses(args.filter)
    ordinal, row = select_row(rows, statuses, args.accepted_ordinal, args.cover_index)
    cnf, embedding, holes = build_parent(row)
    write_parent(args.output, cnf, ordinal, row, embedding, holes)
    print(
        f"accepted_ordinal={ordinal} cover_index={row['cover_index']} branch={row['branch']} "
        f"support={row['support']} order={row['order']} placement={row['word']} "
        f"vars={len(cnf.names)} clauses={len(cnf.clauses)} output={args.output}"
    )


if __name__ == "__main__":
    main()
