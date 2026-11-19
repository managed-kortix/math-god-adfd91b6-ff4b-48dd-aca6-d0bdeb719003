#!/usr/bin/env python3
"""Independent structural checker for exact m=5 selector-batch CNFs.

The checker does not import the producer.  It reconstructs both canonical
placement covers, the 80-batch partition, the manifest, the common CNF base,
and every guarded fixed-hole clause.
"""

import argparse
import hashlib
import itertools
from collections import Counter
from functools import lru_cache
from pathlib import Path

from snc_cnf import generate

FORMAT = "m5-selector-batch-cnf-v1"
MANIFEST_FORMAT = "m5-selector-batches-v1"
CELLS = "RABC"
BATCH_SIZE = 100
BASE_VARIABLES = 23616
BASE_VARIABLE_MAP_SHA256 = "cff4c18a4425f26c188790871da51a58b13569764bf89c83d1c736d5f9db070e"
BASE_CLAUSES = {"B6": 142736, "B7": 142729}
BASE_CLAUSE_SHA256 = {
    "B6": "2e01725de3023fc1b314f628d755ff83015091ef468428758aa092f5728dc913",
    "B7": "5af8262714f3e42a595fb19f437f7a87042715056a3735e61e0d06b918db2ccb",
}
MANIFEST_BYTES = 10925
MANIFEST_SHA256 = "c0d5bab4be917a9f68141713f348359cf58f73bb530df785bbc875a7eba60ecc"
CAPACITIES = {"B6": (1, 8, 6, 3), "B7": (1, 8, 7, 2)}
LABELS = {
    "B6": {"R": (0,), "A": tuple(range(1, 9)), "B": tuple(range(9, 15)), "C": tuple(range(15, 18))},
    "B7": {"R": (0,), "A": tuple(range(1, 9)), "B": tuple(range(9, 16)), "C": tuple(range(16, 18))},
}
# Independent graph specification (sets rather than the producer's tuples).
SUPPORTS = {
    "P6": (6, frozenset({(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)})),
    "P4_P3": (7, frozenset({(0, 1), (1, 2), (2, 3), (4, 5), (5, 6)})),
    "C3_P3": (6, frozenset({(0, 1), (1, 2), (0, 2), (3, 4), (4, 5)})),
    "C4_K2": (6, frozenset({(0, 1), (1, 2), (2, 3), (0, 3), (4, 5)})),
    "P3_P3_K2": (8, frozenset({(0, 1), (1, 2), (3, 4), (4, 5), (6, 7)})),
}
EXPECTED_COUNTS = {
    "B6": (688, 1459, 283, 194, 1731),
    "B7": (526, 1031, 218, 150, 1158),
}
EXPECTED_RAW = {"B6": 21594, "B7": 14591}
PLACEMENT_IDENTITY = {
    "B6": (85330, "e5873a71afa80a126079e2aa7ce716f7d6c8347c241489b616cfb8f67d305ed9"),
    "B7": (59627, "f028a33aa632d73d66e0986c5be5638e98ca8830a2ccfb1e786809eec4091731"),
}
RESIDUAL23 = frozenset({
    100, 104, 138, 367, 389, 391, 394, 881, 941, 1462, 1498, 1506,
    1564, 1572, 2188, 2331, 2339, 2467, 2573, 2576, 2944, 3872, 3875,
})
PAIRS = tuple((x, y) for y in range(1, 18) for x in range(y))


def graph_automorphisms(order, edges):
    result = []
    for permutation in itertools.permutations(range(order)):
        image = frozenset(
            tuple(sorted((permutation[u], permutation[v]))) for u, v in edges
        )
        if image == edges:
            result.append(permutation)
    return tuple(result)


@lru_cache(maxsize=None)
def reconstruct_rows(branch):
    capacity = CAPACITIES[branch]
    records = []
    raw = 0
    shape_counts = []
    for shape, (order, edges) in SUPPORTS.items():
        group = graph_automorphisms(order, edges)
        count = 0
        for colors in itertools.product(CELLS, repeat=order):
            if any(colors.count(CELLS[cell]) > capacity[cell] for cell in range(4)):
                continue
            if any({colors[u], colors[v]} == {"R", "A"} for u, v in edges):
                continue
            raw += 1
            images = (
                tuple(colors[permutation[vertex]] for vertex in range(order))
                for permutation in group
            )
            integer_word = tuple(CELLS.index(color) for color in colors)
            integer_images = (tuple(CELLS.index(color) for color in image) for image in images)
            if integer_word != min(integer_images):
                continue
            orbit = {
                tuple(colors[permutation[vertex]] for vertex in range(order))
                for permutation in group
            }
            records.append((shape, "".join(colors), len(orbit)))
            count += 1
        shape_counts.append(count)
    payload = "".join(
        f"{ordinal}\t{shape}\t{word}\n"
        for ordinal, (shape, word, _) in enumerate(records)
    ).encode("ascii")
    if (tuple(shape_counts) != EXPECTED_COUNTS[branch] or raw != EXPECTED_RAW[branch]
            or sum(record[2] for record in records) != raw
            or (len(payload), hashlib.sha256(payload).hexdigest()) != PLACEMENT_IDENTITY[branch]):
        raise RuntimeError(f"independent {branch} canonical cover identity changed")
    projections = [project_holes(branch, shape, word) for shape, word, _ in records]
    if len(projections) != len(set(projections)):
        raise RuntimeError(f"independent {branch} cover has repeated labelled projections")
    return tuple(records)


def project_holes(branch, shape, word):
    next_label = Counter()
    image = {}
    for vertex, color in enumerate(word):
        pool = LABELS[branch][color]
        position = next_label[color]
        if position >= len(pool):
            raise RuntimeError("word exceeds independently stated capacity")
        image[vertex] = pool[position]
        next_label[color] += 1
    edges = SUPPORTS[shape][1]
    holes = frozenset(tuple(sorted((image[u], image[v]))) for u, v in edges)
    if len(holes) != 5:
        raise RuntimeError("independent support projection collapsed an edge")
    return holes


def split_blocks(sequence):
    return tuple(tuple(sequence[start:start + BATCH_SIZE])
                 for start in range(0, len(sequence), BATCH_SIZE))


@lru_cache(maxsize=1)
def reconstruct_batches():
    output = []
    b6 = reconstruct_rows("B6")
    for shape in SUPPORTS:
        sequence = [index for index, record in enumerate(b6)
                    if record[0] == shape and index not in RESIDUAL23]
        for local, members in enumerate(split_blocks(sequence)):
            output.append((f"B6-main-{shape}-{local:02d}", "B6", "main4332", shape, members))
    output.append(("B6-residual23-MIXED-00", "B6", "residual23", "MIXED", tuple(sorted(RESIDUAL23))))
    b7 = reconstruct_rows("B7")
    for shape in SUPPORTS:
        sequence = [index for index, record in enumerate(b7) if record[0] == shape]
        for local, members in enumerate(split_blocks(sequence)):
            output.append((f"B7-all-{shape}-{local:02d}", "B7", "all3083", shape, members))
    cover6 = [member for _, branch, _, _, members in output if branch == "B6" for member in members]
    cover7 = [member for _, branch, _, _, members in output if branch == "B7" for member in members]
    if (len(output) != 80 or Counter(row[2] for row in output) !=
            Counter({"main4332": 45, "residual23": 1, "all3083": 34})
            or sorted(cover6) != list(range(4355)) or len(set(cover6)) != 4355
            or sorted(cover7) != list(range(3083)) or len(set(cover7)) != 3083):
        raise RuntimeError("independent batch schedule is not a disjoint exact cover")
    return tuple(output)


def member_bytes(branch, members):
    rows = reconstruct_rows(branch)
    lines = ["columns\tselector-ordinal,parent-ordinal,shape,placement,orbit-weight,hole-sha256"]
    for selector, parent in enumerate(members):
        shape, word, weight = rows[parent]
        holes = project_holes(branch, shape, word)
        hole_stream = ",".join(f"{x}-{y}" for x, y in sorted(holes)).encode("ascii")
        lines.append(
            f"{selector:03d}\t{parent:04d}\t{shape}\t{word}\t{weight}\t"
            f"{hashlib.sha256(hole_stream).hexdigest()}"
        )
    return ("\n".join(lines) + "\n").encode("ascii")


def cnf_dimensions(branch, members):
    return BASE_VARIABLES + len(members), BASE_CLAUSES[branch] + 1 + 153 * len(members)


def reconstruct_manifest():
    lines = [
        MANIFEST_FORMAT,
        "scope\tresidual five uncovered five-edge support shapes only",
        "batch-size\t100",
        "shapes\t" + ",".join(SUPPORTS),
        f"B6-placement-bytes\t{PLACEMENT_IDENTITY['B6'][0]}",
        f"B6-placement-sha256\t{PLACEMENT_IDENTITY['B6'][1]}",
        "B6-parents\t4355", "B6-main4332\t4332", "B6-residual23\t23",
        f"B7-placement-bytes\t{PLACEMENT_IDENTITY['B7'][0]}",
        f"B7-placement-sha256\t{PLACEMENT_IDENTITY['B7'][1]}",
        "B7-parents\t3083", "batches\t80",
        "columns\tbatch-ordinal,key,branch,family,shape,members,first-parent,last-parent,variables,clauses,member-sha256",
    ]
    for ordinal, (key, branch, family, shape, members) in enumerate(reconstruct_batches()):
        variables, clauses = cnf_dimensions(branch, members)
        digest = hashlib.sha256(member_bytes(branch, members)).hexdigest()
        lines.append(
            f"{ordinal:02d}\t{key}\t{branch}\t{family}\t{shape}\t{len(members)}\t"
            f"{members[0]}\t{members[-1]}\t{variables}\t{clauses}\t{digest}"
        )
    payload = ("\n".join(lines) + "\n").encode("ascii")
    if (len(payload), hashlib.sha256(payload).hexdigest()) != (MANIFEST_BYTES, MANIFEST_SHA256):
        raise RuntimeError("independent manifest differs from its frozen fingerprint")
    return payload


def parse_cnf(path):
    metadata = []
    variables = []
    names = set()
    header = None
    clauses = []
    phase = "metadata"
    with path.open("r", encoding="ascii", newline="") as handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.endswith("\n"):
                raise RuntimeError(f"CNF line {line_number} lacks newline terminator")
            line = raw[:-1]
            if not line:
                raise RuntimeError(f"blank CNF line {line_number}")
            if line.startswith("c var "):
                if phase not in ("metadata", "variables") or header is not None:
                    raise RuntimeError("variable map is out of canonical preamble order")
                phase = "variables"
                fields = line.split(" ", 3)
                if len(fields) != 4 or not fields[3]:
                    raise RuntimeError(f"malformed variable map line {line_number}")
                number = int(fields[2])
                if number != len(variables) + 1 or fields[3] in names:
                    raise RuntimeError("variable map is not sequential and unique")
                variables.append(fields[3])
                names.add(fields[3])
            elif line.startswith("c "):
                if phase != "metadata" or header is not None:
                    raise RuntimeError("metadata is out of canonical preamble order")
                key, separator, value = line[2:].partition(" ")
                if not separator or not key or any(old == key for old, _ in metadata):
                    raise RuntimeError("metadata key is malformed or repeated")
                metadata.append((key, value))
            elif line.startswith("p cnf "):
                if header is not None or phase != "variables":
                    raise RuntimeError("DIMACS header is duplicated or misplaced")
                fields = line.split()
                if len(fields) != 4:
                    raise RuntimeError("malformed DIMACS header")
                header = int(fields[2]), int(fields[3])
                phase = "clauses"
            else:
                if phase != "clauses" or header is None:
                    raise RuntimeError("clause precedes DIMACS header")
                fields = [int(token) for token in line.split()]
                if not fields or fields[-1] != 0 or 0 in fields[:-1]:
                    raise RuntimeError(f"malformed clause line {line_number}")
                clause = tuple(fields[:-1])
                if not clause or any(abs(literal) > header[0] for literal in clause):
                    raise RuntimeError(f"empty or out-of-range clause line {line_number}")
                clauses.append(clause)
    if header is None or header != (len(variables), len(clauses)):
        raise RuntimeError("DIMACS dimensions do not match parsed stream")
    return metadata, variables, clauses


def map_hash(names):
    stream = "".join(f"{number} {name}\n" for number, name in enumerate(names, 1))
    return hashlib.sha256(stream.encode("ascii")).hexdigest()


def clauses_hash(clauses):
    stream = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return hashlib.sha256(stream.encode("ascii")).hexdigest()


@lru_cache(maxsize=None)
def reconstruct_base(branch):
    cnf = generate(18, 6 if branch == "B6" else 7, 5,
                   robust_witness=True, arc_minimal=True)
    names = tuple(cnf.names)
    clauses = tuple(cnf.clauses)
    if (len(names) != BASE_VARIABLES or map_hash(names) != BASE_VARIABLE_MAP_SHA256
            or len(clauses) != BASE_CLAUSES[branch]
            or clauses_hash(clauses) != BASE_CLAUSE_SHA256[branch]):
        raise RuntimeError(f"independently regenerated {branch} base changed")
    return names, clauses


def selector_name(ordinal):
    return f"m5_batch_selector_{ordinal:03d}"


def expected_metadata(ordinal, record, manifest, selectors):
    key, branch, family, shape, members = record
    return [
        ("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
        ("manifest-bytes", str(len(manifest))),
        ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
        ("scope", "residual five uncovered five-edge support shapes only"),
        ("batch-ordinal", str(ordinal)), ("batch-key", key), ("branch", branch),
        ("family", family), ("shape", shape), ("members", str(len(members))),
        ("first-parent", str(members[0])), ("last-parent", str(members[-1])),
        ("member-sha256", hashlib.sha256(member_bytes(branch, members)).hexdigest()),
        ("base-variables", str(BASE_VARIABLES)),
        ("base-variable-map-sha256", BASE_VARIABLE_MAP_SHA256),
        ("base-clauses", str(BASE_CLAUSES[branch])),
        ("base-clause-sha256", BASE_CLAUSE_SHA256[branch]),
        ("alo-clauses", "1"), ("guarded-hole-clauses-per-member", "153"),
        ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1])),
    ]


def check(path):
    manifest = reconstruct_manifest()
    metadata, names, clauses = parse_cnf(path)
    table = dict(metadata)
    try:
        ordinal = int(table["batch-ordinal"])
    except (KeyError, ValueError) as error:
        raise RuntimeError("missing or invalid batch ordinal") from error
    schedule = reconstruct_batches()
    if not 0 <= ordinal < len(schedule):
        raise RuntimeError("batch ordinal lies outside frozen schedule")
    record = schedule[ordinal]
    key, branch, _, _, members = record
    base_names, base_clauses = reconstruct_base(branch)
    selectors = tuple(range(BASE_VARIABLES + 1, BASE_VARIABLES + len(members) + 1))
    if metadata != expected_metadata(ordinal, record, manifest, selectors):
        raise RuntimeError("CNF metadata is not the exact independently reconstructed record")
    expected_names = base_names + tuple(selector_name(i) for i in range(len(members)))
    if tuple(names) != expected_names:
        raise RuntimeError("CNF variable map differs from independent reconstruction")
    if tuple(clauses[:len(base_clauses)]) != base_clauses:
        raise RuntimeError("CNF common base clause stream changed")
    suffix = [selectors]
    rows = reconstruct_rows(branch)
    for selector, parent in zip(selectors, members):
        shape, word, _ = rows[parent]
        holes = project_holes(branch, shape, word)
        for pair in PAIRS:
            hole_number = names.index(f"h_{pair[0]}_{pair[1]}") + 1
            suffix.append((-selector, hole_number if pair in holes else -hole_number))
    if clauses[len(base_clauses):] != suffix:
        raise RuntimeError("ALO or guarded fixed-hole suffix differs from exact reconstruction")
    expected_dimensions = cnf_dimensions(branch, members)
    if (len(names), len(clauses)) != expected_dimensions:
        raise RuntimeError("CNF dimensions differ from frozen formula")
    print(
        f"PASS key={key} branch={branch} members={len(members)} vars={len(names)} "
        f"clauses={len(clauses)} manifest={MANIFEST_SHA256}"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    check(args.cnf)


if __name__ == "__main__":
    main()
