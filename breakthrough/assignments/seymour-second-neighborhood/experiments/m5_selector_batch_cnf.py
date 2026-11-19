#!/usr/bin/env python3
"""Emit exact selector-batched CNFs for the residual five-shape m=5 cover.

This is an architecture generator, not a certificate claim.  A batch CNF is
satisfiable exactly when at least one represented fixed-hole parent is
satisfiable.  Proof objects, when produced, need a separate authenticated
ledger and independent LRAT replay.
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
BRANCHES = {
    "B6": ((1, 8, 6, 3), ((0,), tuple(range(1, 9)), tuple(range(9, 15)), tuple(range(15, 18)))),
    "B7": ((1, 8, 7, 2), ((0,), tuple(range(1, 9)), tuple(range(9, 16)), tuple(range(16, 18)))),
}
SHAPES = {
    "P6": (6, ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5))),
    "P4_P3": (7, ((0, 1), (1, 2), (2, 3), (4, 5), (5, 6))),
    "C3_P3": (6, ((0, 1), (1, 2), (0, 2), (3, 4), (4, 5))),
    "C4_K2": (6, ((0, 1), (1, 2), (2, 3), (0, 3), (4, 5))),
    "P3_P3_K2": (8, ((0, 1), (1, 2), (3, 4), (4, 5), (6, 7))),
}
EXPECTED_COUNTS = {
    "B6": {"P6": 688, "P4_P3": 1459, "C3_P3": 283, "C4_K2": 194, "P3_P3_K2": 1731},
    "B7": {"P6": 526, "P4_P3": 1031, "C3_P3": 218, "C4_K2": 150, "P3_P3_K2": 1158},
}
EXPECTED_RAW_COLORINGS = {"B6": 21594, "B7": 14591}
PLACEMENT_PAYLOAD = {
    "B6": (85330, "e5873a71afa80a126079e2aa7ce716f7d6c8347c241489b616cfb8f67d305ed9"),
    "B7": (59627, "f028a33aa632d73d66e0986c5be5638e98ca8830a2ccfb1e786809eec4091731"),
}
# This is only a deterministic scheduling partition.  It is not a premise of
# the selector lemma and carries no mathematical "easy" assertion.
B6_RESIDUAL23 = frozenset({
    100, 104, 138, 367, 389, 391, 394, 881, 941, 1462, 1498, 1506,
    1564, 1572, 2188, 2331, 2339, 2467, 2573, 2576, 2944, 3872, 3875,
})
PAIRS = tuple((low, high) for high in range(1, 18) for low in range(high))
MANIFEST_BYTES = 10925
MANIFEST_SHA256 = "c0d5bab4be917a9f68141713f348359cf58f73bb530df785bbc875a7eba60ecc"


def automorphisms(order, edges):
    edge_set = {tuple(sorted(edge)) for edge in edges}
    return tuple(
        permutation for permutation in itertools.permutations(range(order))
        if {tuple(sorted((permutation[u], permutation[v]))) for u, v in edge_set} == edge_set
    )


@lru_cache(maxsize=None)
def placement_rows(branch):
    """Return canonical support-color orbits in fixed shape/word order."""
    if branch not in BRANCHES:
        raise ValueError("branch must be B6 or B7")
    capacity, _ = BRANCHES[branch]
    rows = []
    raw_total = 0
    counts = Counter()
    for shape, (order, edges) in SHAPES.items():
        group = automorphisms(order, edges)
        for word in itertools.product(range(4), repeat=order):
            if any(word.count(cell) > capacity[cell] for cell in range(4)):
                continue
            if any({word[u], word[v]} == {0, 1} for u, v in edges):
                continue
            orbit = {tuple(word[permutation[i]] for i in range(order)) for permutation in group}
            raw_total += 1
            if word == min(orbit):
                rows.append((shape, word, len(orbit)))
                counts[shape] += 1
    payload = "".join(
        f"{ordinal}\t{shape}\t{''.join(CELLS[cell] for cell in word)}\n"
        for ordinal, (shape, word, _) in enumerate(rows)
    ).encode("ascii")
    identity = len(payload), hashlib.sha256(payload).hexdigest()
    if (dict(counts) != EXPECTED_COUNTS[branch] or raw_total != EXPECTED_RAW_COLORINGS[branch]
            or sum(row[2] for row in rows) != raw_total or identity != PLACEMENT_PAYLOAD[branch]):
        raise RuntimeError(f"{branch} canonical placement cover changed")
    projections = [hole_projection(branch, shape, word) for shape, word, _ in rows]
    if len(projections) != len(set(projections)):
        raise RuntimeError(f"{branch} placement cover has duplicate labelled hole projections")
    return tuple(rows)


def hole_projection(branch, shape, word):
    labels = BRANCHES[branch][1]
    used = [0, 0, 0, 0]
    image = {}
    for vertex, cell in enumerate(word):
        if used[cell] == len(labels[cell]):
            raise RuntimeError("placement exceeds its cell capacity")
        image[vertex] = labels[cell][used[cell]]
        used[cell] += 1
    holes = frozenset(
        tuple(sorted((image[u], image[v]))) for u, v in SHAPES[shape][1]
    )
    if len(holes) != 5:
        raise RuntimeError("support projection does not contain five distinct holes")
    return holes


def member_payload(branch, members):
    rows = placement_rows(branch)
    lines = ["columns\tselector-ordinal,parent-ordinal,shape,placement,orbit-weight,hole-sha256"]
    for selector, parent in enumerate(members):
        shape, word, weight = rows[parent]
        holes = hole_projection(branch, shape, word)
        hole_text = ",".join(f"{u}-{v}" for u, v in sorted(holes)).encode("ascii")
        lines.append(
            f"{selector:03d}\t{parent:04d}\t{shape}\t"
            f"{''.join(CELLS[cell] for cell in word)}\t{weight}\t"
            f"{hashlib.sha256(hole_text).hexdigest()}"
        )
    return ("\n".join(lines) + "\n").encode("ascii")


def chunked(values, size=BATCH_SIZE):
    return tuple(tuple(values[start:start + size]) for start in range(0, len(values), size))


@lru_cache(maxsize=1)
def batches():
    """Exact partition: 4,332 B6 main + 23 B6 residual + all 3,083 B7."""
    result = []
    b6_rows = placement_rows("B6")
    for shape in SHAPES:
        members = [i for i, row in enumerate(b6_rows)
                   if row[0] == shape and i not in B6_RESIDUAL23]
        for local, block in enumerate(chunked(members)):
            result.append({
                "key": f"B6-main-{shape}-{local:02d}", "branch": "B6",
                "family": "main4332", "shape": shape, "members": block,
            })
    result.append({
        "key": "B6-residual23-MIXED-00", "branch": "B6",
        "family": "residual23", "shape": "MIXED", "members": tuple(sorted(B6_RESIDUAL23)),
    })
    b7_rows = placement_rows("B7")
    for shape in SHAPES:
        members = [i for i, row in enumerate(b7_rows) if row[0] == shape]
        for local, block in enumerate(chunked(members)):
            result.append({
                "key": f"B7-all-{shape}-{local:02d}", "branch": "B7",
                "family": "all3083", "shape": shape, "members": block,
            })
    b6_seen = [member for batch in result if batch["branch"] == "B6" for member in batch["members"]]
    b7_seen = [member for batch in result if batch["branch"] == "B7" for member in batch["members"]]
    if (sorted(b6_seen) != list(range(len(b6_rows))) or len(b6_seen) != len(set(b6_seen))
            or sorted(b7_seen) != list(range(len(b7_rows))) or len(b7_seen) != len(set(b7_seen))):
        raise RuntimeError("batch partition is not a disjoint exact placement cover")
    if Counter(batch["family"] for batch in result) != Counter(
            {"main4332": 45, "residual23": 1, "all3083": 34}):
        raise RuntimeError("batch family counts changed")
    return tuple(result)


def variable_map_sha256(cnf):
    payload = "".join(f"{number} {name}\n" for name, number in cnf.names.items())
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def clause_sha256(clauses):
    payload = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def frozen_base(branch):
    cnf = generate(18, 6 if branch == "B6" else 7, 5,
                   robust_witness=True, arc_minimal=True)
    if (len(cnf.names) != BASE_VARIABLES
            or variable_map_sha256(cnf) != BASE_VARIABLE_MAP_SHA256
            or len(cnf.clauses) != BASE_CLAUSES[branch]
            or clause_sha256(cnf.clauses) != BASE_CLAUSE_SHA256[branch]):
        raise RuntimeError(f"generated {branch} base differs from its frozen identity")
    return cnf


def dimensions(batch):
    count = len(batch["members"])
    return BASE_VARIABLES + count, BASE_CLAUSES[batch["branch"]] + 1 + len(PAIRS) * count


def manifest_payload():
    records = [
        MANIFEST_FORMAT,
        "scope\tresidual five uncovered five-edge support shapes only",
        f"batch-size\t{BATCH_SIZE}",
        "shapes\t" + ",".join(SHAPES),
        f"B6-placement-bytes\t{PLACEMENT_PAYLOAD['B6'][0]}",
        f"B6-placement-sha256\t{PLACEMENT_PAYLOAD['B6'][1]}",
        f"B6-parents\t{sum(EXPECTED_COUNTS['B6'].values())}",
        f"B6-main4332\t{sum(EXPECTED_COUNTS['B6'].values()) - len(B6_RESIDUAL23)}",
        f"B6-residual23\t{len(B6_RESIDUAL23)}",
        f"B7-placement-bytes\t{PLACEMENT_PAYLOAD['B7'][0]}",
        f"B7-placement-sha256\t{PLACEMENT_PAYLOAD['B7'][1]}",
        f"B7-parents\t{sum(EXPECTED_COUNTS['B7'].values())}",
        f"batches\t{len(batches())}",
        "columns\tbatch-ordinal,key,branch,family,shape,members,first-parent,last-parent,variables,clauses,member-sha256",
    ]
    for ordinal, batch in enumerate(batches()):
        variables, clauses = dimensions(batch)
        members = batch["members"]
        records.append(
            f"{ordinal:02d}\t{batch['key']}\t{batch['branch']}\t{batch['family']}\t"
            f"{batch['shape']}\t{len(members)}\t{members[0]}\t{members[-1]}\t"
            f"{variables}\t{clauses}\t"
            f"{hashlib.sha256(member_payload(batch['branch'], members)).hexdigest()}"
        )
    return ("\n".join(records) + "\n").encode("ascii")


def checked_manifest():
    payload = manifest_payload()
    digest = hashlib.sha256(payload).hexdigest()
    if MANIFEST_BYTES and (len(payload), digest) != (MANIFEST_BYTES, MANIFEST_SHA256):
        raise RuntimeError("selector-batch manifest differs from its frozen identity")
    return payload


def select_batch(key):
    matches = [batch for batch in batches() if batch["key"] == key]
    if len(matches) != 1:
        raise ValueError(f"unknown batch key {key!r}")
    return matches[0]


def selector_name(ordinal):
    return f"m5_batch_selector_{ordinal:03d}"


def build_batch(batch):
    branch = batch["branch"]
    cnf = frozen_base(branch)
    selectors = [cnf.var(selector_name(ordinal)) for ordinal in range(len(batch["members"]))]
    cnf.add(*selectors)
    rows = placement_rows(branch)
    for selector, parent in zip(selectors, batch["members"]):
        shape, word, _ = rows[parent]
        holes = hole_projection(branch, shape, word)
        for pair in PAIRS:
            hole = cnf.names[f"h_{pair[0]}_{pair[1]}"]
            cnf.add(-selector, hole if pair in holes else -hole)
    expected = dimensions(batch)
    if (len(cnf.names), len(cnf.clauses)) != expected:
        raise RuntimeError("batch CNF dimensions changed")
    return cnf, selectors


def metadata(batch, manifest, selectors):
    ordinal = batches().index(batch)
    members = batch["members"]
    return [
        ("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
        ("manifest-bytes", str(len(manifest))),
        ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
        ("scope", "residual five uncovered five-edge support shapes only"),
        ("batch-ordinal", str(ordinal)), ("batch-key", batch["key"]),
        ("branch", batch["branch"]), ("family", batch["family"]),
        ("shape", batch["shape"]), ("members", str(len(members))),
        ("first-parent", str(members[0])), ("last-parent", str(members[-1])),
        ("member-sha256", hashlib.sha256(member_payload(batch["branch"], members)).hexdigest()),
        ("base-variables", str(BASE_VARIABLES)),
        ("base-variable-map-sha256", BASE_VARIABLE_MAP_SHA256),
        ("base-clauses", str(BASE_CLAUSES[batch["branch"]])),
        ("base-clause-sha256", BASE_CLAUSE_SHA256[batch["branch"]]),
        ("alo-clauses", "1"), ("guarded-hole-clauses-per-member", str(len(PAIRS))),
        ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1])),
    ]


def write_batch(path, batch, cnf, selectors, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(batch, manifest, selectors):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", help="batch key from the manifest")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--list", action="store_true", help="print batch keys and dimensions")
    args = parser.parse_args()
    if not (args.output or args.manifest_output or args.list):
        parser.error("request --output, --manifest-output, or --list")
    if args.output is not None and args.key is None:
        parser.error("--output requires --key")
    manifest = checked_manifest()
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.list:
        for batch in batches():
            variables, clauses = dimensions(batch)
            print(f"{batch['key']} members={len(batch['members'])} vars={variables} clauses={clauses}")
    if args.output:
        batch = select_batch(args.key)
        cnf, selectors = build_batch(batch)
        write_batch(args.output, batch, cnf, selectors, manifest)
        digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
        print(
            f"key={batch['key']} members={len(batch['members'])} vars={len(cnf.names)} "
            f"clauses={len(cnf.clauses)} bytes={args.output.stat().st_size} sha256={digest}"
        )
    print(
        f"manifest_batches={len(batches())} B6=4355 B7=3083 bytes={len(manifest)} "
        f"sha256={hashlib.sha256(manifest).hexdigest()}"
    )


if __name__ == "__main__":
    main()
