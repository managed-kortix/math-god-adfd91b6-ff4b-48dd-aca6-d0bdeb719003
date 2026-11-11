#!/usr/bin/env python3
"""Independent exhaustive checker for the frozen 57 clean-sink shards."""

import argparse
import hashlib
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import check_m6_clean_sink_group_cnf as clean
from check_m6_parent_cnf import (
    BASE_CLAUSES, BASE_CLAUSE_SHA256, BASE_VARIABLES, BASE_VARIABLE_MAP_SHA256,
    PAIRS, clause_sha256, expected_projection, parse_cnf, variable_map_sha256,
)
from snc_cnf import generate

HERE = Path(__file__).resolve().parent
FORMAT = "m6-clean-sink-balanced-shard-cnf-v1"
MANIFEST_FORMAT = "m6-clean-sink-balanced-shards-v1"
HASH_LEDGER_FORMAT = "m6-clean-sink-balanced-shard-hashes-v1"
HASH_LEDGER_PATH = HERE / "m6-clean-sink-balanced-shard-hashes.tsv"
CAP = 500
EXCLUDED_GROUP = "B6-l4"
GROUP_KEYS = clean.GROUP_KEYS[1:]
LABELS = {
    "B6": {"B": range(9, 15), "C": range(15, 18)},
    "B7": {"B": range(9, 16), "C": range(16, 18)},
}
IDENTITY_PATHS = {
    "clean-parent-manifest": HERE / "m6-clean-sink-selector-groups.tsv",
    "clean-remaining-stream": HERE / "m6-clean-sink-remaining.tsv",
    "clean-partition-manifest": HERE / "m6-clean-sink-manifest.tsv",
    "clean-sink-theorem": HERE.parent / "attempts" / "tick52-rooted-clean-sink-theorem.md",
    "balanced-partition-theorem": HERE.parent / "attempts" / "tick53-clean-sink-balanced-shards.md",
    "excluded-certificate-ledger": HERE / "m6-clean-sink-B6-l4-certificate.tsv",
    "excluded-certificate-verifier": HERE / "verify_m6_clean_sink_B6_l4_certificate.py",
}
IDENTITIES = {
    "clean-parent-manifest": (1838, "6e7eee0ddd5b4c7ef02cdf459c9a0647f720513e7ee4987a3a8b0c17af37eeda"),
    "clean-remaining-stream": (2262190, "416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642"),
    "clean-partition-manifest": (2104, "733e06c8aa9881e0006409efff23729f1bf88d8af7b1a70e8a78fd3775b53217"),
    "clean-sink-theorem": (4156, "bd0631529bb4658061663460b718ef2ee3186d02fdc599fb2673d3cff3b94ee2"),
    "balanced-partition-theorem": (2490, "a6aa643ae2cad46349a8a1aee88f837e112532aef2858913c9e19289e8200a87"),
    "excluded-certificate-ledger": (1807, "e46e7189e50d423f721e481868b6c5b2cbe4f3ab9d208407f652a27c4c6359e2"),
    "excluded-certificate-verifier": (7741, "91f5b7c89d3ab23b63df2eea5b632aa64f1465f1baf6c15d9676ea5d4002aea9"),
}
BALANCING_TABLE = (
    ("B6-l5", 0, 0, 398, (398,)), ("B6-l5", 0, 1, 326, (326,)),
    ("B6-l5", 0, 2, 78, (78,)), ("B6-l5", 1, 0, 97, (97,)),
    ("B6-l5", 1, 1, 99, (99,)), ("B6-l5", 1, 2, 26, (26,)),
    ("B6-l6", 0, 0, 80, (80,)), ("B6-l6", 0, 1, 97, (97,)),
    ("B6-l6", 0, 2, 36, (36,)), ("B6-l6", 0, 3, 7, (7,)),
    ("B7-l2", 0, 0, 3973, (497, 497, 497, 497, 497, 496, 496, 496)),
    ("B7-l2", 1, 0, 2694, (449, 449, 449, 449, 449, 449)),
    ("B7-l2", 2, 0, 1212, (404, 404, 404)), ("B7-l2", 3, 0, 213, (213,)),
    ("B7-l2", 4, 0, 27, (27,)),
    ("B7-l3", 0, 0, 2064, (413, 413, 413, 413, 412)),
    ("B7-l3", 0, 1, 724, (362, 362)), ("B7-l3", 1, 0, 1306, (436, 435, 435)),
    ("B7-l3", 1, 1, 389, (389,)), ("B7-l3", 2, 0, 341, (341,)),
    ("B7-l3", 2, 1, 141, (141,)), ("B7-l3", 3, 0, 36, (36,)),
    ("B7-l3", 3, 1, 15, (15,)),
    ("B7-l4", 0, 0, 818, (409, 409)), ("B7-l4", 0, 1, 322, (322,)),
    ("B7-l4", 1, 0, 290, (290,)), ("B7-l4", 1, 1, 148, (148,)),
    ("B7-l4", 2, 0, 47, (47,)), ("B7-l4", 2, 1, 24, (24,)),
    ("B7-l5", 0, 0, 159, (159,)), ("B7-l5", 0, 1, 110, (110,)),
    ("B7-l5", 1, 0, 32, (32,)), ("B7-l5", 1, 1, 21, (21,)),
    ("B7-l6", 0, 0, 26, (26,)), ("B7-l6", 0, 1, 16, (16,)),
)
PARENTS = 16392
SHARDS = 57
MANIFEST_BYTES = 8414
MANIFEST_SHA256 = "20f6d04a9e8ca0662efd011ead7804402d3c0dd21e025311cb4485fae8403fdb"
HASH_LEDGER_BYTES = 5972
HASH_LEDGER_SHA256 = "46045d216f32a22b1d618910c4e3fc5528c700b34277be2e17eab89e6ccae125"
SHARD_CNF_SHA256 = {}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_identities():
    for name, path in IDENTITY_PATHS.items():
        if identity(path) != IDENTITIES[name]:
            raise RuntimeError(f"frozen bound identity changed: {name}")


def parameters(row):
    holes = expected_projection(row)[1]
    labels = LABELS[row[0]]
    b, c = set(labels["B"]), set(labels["C"])
    q = sum((low in b and high in c) or (high in b and low in c) for low, high in holes)
    h_cc = sum(low in c and high in c for low, high in holes)
    return q, h_cc


def shard_key(group, q, h_cc, part):
    return f"{group}-q{q}-c{h_cc}-s{part:02d}"


def derive_shards(remaining=clean.REMAINING, cover=HERE / "m6-placement-cover.txt",
                  filter_path=HERE / "m6-placement-filter.txt"):
    verify_identities()
    groups = clean.derive_groups(remaining, cover, filter_path)
    cells = defaultdict(list)
    excluded = groups.pop(EXCLUDED_GROUP)
    if len(excluded) != 2470 or set(groups) != set(GROUP_KEYS):
        raise RuntimeError("certified group exclusion is not exact")
    for group in GROUP_KEYS:
        for member in groups[group]:
            cells[group, *parameters(member[2])].append(member)
    shards = []
    for group, q, h_cc, total, sizes in BALANCING_TABLE:
        members = cells.pop((group, q, h_cc), None)
        if members is None or len(members) != total or sum(sizes) != total:
            raise RuntimeError("canonical q,H_CC table differs from independent projection")
        if max(sizes) > CAP or max(sizes) - min(sizes) > 1:
            raise RuntimeError("cell split is not cap-500 balanced")
        offset = 0
        for part, size in enumerate(sizes):
            shard_members = members[offset:offset + size]
            shards.append((shard_key(group, q, h_cc, part), group, q, h_cc, part,
                           len(sizes), shard_members))
            offset += size
    flattened = [(group, accepted, cover_index) for _, group, _, _, _, _, members in shards
                 for accepted, cover_index, _ in members]
    expected = [(group, accepted, cover_index) for group in GROUP_KEYS
                for accepted, cover_index, _ in groups[group]]
    if cells or len(shards) != SHARDS or len(flattened) != PARENTS or set(flattened) != set(expected):
        raise RuntimeError("all-shard cover is not exhaustive, disjoint, and exact")
    return shards


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:03d}\t{accepted:05d}\t{cover:06d}"
                 for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def dimensions(group, count):
    return BASE_VARIABLES + count, BASE_CLAUSES[group[:2]] + 1 + 153 * count


def manifest_payload(shards):
    lines = [MANIFEST_FORMAT]
    for name, (size, digest) in IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.extend((f"excluded-certified-group\t{EXCLUDED_GROUP}:2470", f"cap\t{CAP}",
                  f"groups\t{len(GROUP_KEYS)}", f"q-hcc-cells\t{len(BALANCING_TABLE)}",
                  f"shards\t{SHARDS}", f"parents\t{PARENTS}",
                  "columns\tshard-ordinal,key,parent-group,q,H_CC,cell-part,cell-parts,parents,first-selector,last-selector,variables,clauses,member-sha256"))
    for ordinal, (key, group, q, h_cc, part, parts, members) in enumerate(shards):
        variables, clauses = dimensions(group, len(members))
        lines.append(f"{ordinal:02d}\t{key}\t{group}\t{q}\t{h_cc}\t{part}\t{parts}\t{len(members)}\t"
                     f"{BASE_VARIABLES + 1}\t{variables}\t{variables}\t{clauses}\t"
                     f"{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def hash_ledger_payload(shards, manifest):
    lines = [HASH_LEDGER_FORMAT, f"partition-manifest-bytes\t{len(manifest)}",
             f"partition-manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
             f"shards\t{SHARDS}",
             "columns\tshard-ordinal,key,parents,variables,clauses,cnf-sha256"]
    for ordinal, shard in enumerate(shards):
        key, group, _, _, _, _, members = shard
        variables, clauses = dimensions(group, len(members))
        lines.append(f"{ordinal:02d}\t{key}\t{len(members)}\t{variables}\t{clauses}\t{SHARD_CNF_SHA256[key]}")
    return ("\n".join(lines) + "\n").encode("ascii")


def load_hash_ledger():
    raw = HASH_LEDGER_PATH.read_bytes()
    if (len(raw), hashlib.sha256(raw).hexdigest()) != (HASH_LEDGER_BYTES, HASH_LEDGER_SHA256):
        raise RuntimeError("complete shard hash ledger identity changed")
    lines = raw.decode("ascii").splitlines()
    expected_header = [HASH_LEDGER_FORMAT, f"partition-manifest-bytes\t{MANIFEST_BYTES}",
                       f"partition-manifest-sha256\t{MANIFEST_SHA256}", f"shards\t{SHARDS}",
                       "columns\tshard-ordinal,key,parents,variables,clauses,cnf-sha256"]
    if lines[:5] != expected_header or len(lines) != SHARDS + 5:
        raise RuntimeError("complete shard hash ledger framing changed")
    hashes = {}
    for ordinal, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if (len(fields) != 6 or fields[0] != f"{ordinal:02d}" or fields[1] in hashes or
                len(fields[5]) != 64 or any(character not in "0123456789abcdef" for character in fields[5])):
            raise RuntimeError("malformed complete shard hash ledger row")
        int(fields[2]); int(fields[3]); int(fields[4])
        hashes[fields[1]] = fields[5]
    return hashes


SHARD_CNF_SHA256 = load_hash_ledger()


@lru_cache(maxsize=None)
def frozen_base(branch):
    cnf = generate(18, 6 if branch == "B6" else 7, 6, robust_witness=True, arc_minimal=True)
    return tuple(cnf.names), tuple(cnf.clauses)


def read_model(path):
    literals, terminated = [], False
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if not line or line.startswith("c ") or line in ("s SATISFIABLE", "SAT"):
            continue
        fields = line[2:].split() if line.startswith("v ") else line.split()
        for field in fields:
            number = int(field)
            if terminated:
                raise RuntimeError("model data follows terminator")
            if number == 0:
                terminated = True
            else:
                literals.append(number)
    if not terminated:
        raise RuntimeError("model has no terminator")
    return literals


def validate_model(variables, clauses, literals, selectors):
    values = {}
    for literal in literals:
        if literal == 0 or not 1 <= abs(literal) <= len(variables) or abs(literal) in values:
            raise RuntimeError("model contains invalid or duplicate assignment")
        values[abs(literal)] = literal > 0
    if len(values) != len(variables):
        raise RuntimeError("model is not complete")
    if any(not any(values[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses):
        raise RuntimeError("model falsifies a clause")
    selected = [i for i, selector in enumerate(selectors) if values[selector]]
    if len(selected) != 1:
        raise RuntimeError("model does not select exactly one parent")
    return values, selected[0]


def expected_metadata(ordinal, shard, manifest, selectors):
    key, group, q, h_cc, part, parts, members = shard
    result = [("format", FORMAT), ("shard-manifest-format", MANIFEST_FORMAT),
              ("shard-manifest-bytes", str(len(manifest))),
              ("shard-manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, (size, digest) in IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(size)), (f"{name}-sha256", digest)))
    result.extend((("excluded-certified-group", f"{EXCLUDED_GROUP}:2470"), ("cap", str(CAP)),
                   ("shard-ordinal", str(ordinal)), ("shard-key", key), ("parent-group", group),
                   ("branch", group[:2]), ("lambda", group[4:]), ("q", str(q)),
                   ("H_CC", str(h_cc)), ("cell-part", str(part)), ("cell-parts", str(parts)),
                   ("parents", str(len(members))),
                   ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
                   ("base-variables", str(BASE_VARIABLES)),
                   ("base-variable-map-sha256", BASE_VARIABLE_MAP_SHA256),
                   ("base-clauses", str(BASE_CLAUSES[group[:2]])),
                   ("base-clause-sha256", BASE_CLAUSE_SHA256[group[:2]]),
                   ("alo-clauses", "1"), ("guarded-hole-clauses-per-parent", "153"),
                   ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    return result


def check(cnf_path, model_path=None):
    shards = derive_shards()
    manifest = manifest_payload(shards)
    if MANIFEST_BYTES and (len(manifest), hashlib.sha256(manifest).hexdigest()) != (MANIFEST_BYTES, MANIFEST_SHA256):
        raise RuntimeError("independent manifest fingerprint changed")
    metadata_items, variables, clauses, declared = parse_cnf(cnf_path)
    metadata = dict(metadata_items)
    ordinal = int(metadata.get("shard-ordinal", "-1"))
    if not 0 <= ordinal < SHARDS:
        raise RuntimeError("shard ordinal outside complete manifest")
    shard = shards[ordinal]
    key, group, _, _, _, _, members = shard
    base_names, base_clauses = map(list, frozen_base(group[:2]))
    if (len(base_names) != BASE_VARIABLES or variable_map_sha256(base_names) != BASE_VARIABLE_MAP_SHA256 or
            len(base_clauses) != BASE_CLAUSES[group[:2]] or
            clause_sha256(base_clauses) != BASE_CLAUSE_SHA256[group[:2]]):
        raise RuntimeError("independent branch base differs from frozen identity")
    selectors = list(range(BASE_VARIABLES + 1, BASE_VARIABLES + len(members) + 1))
    names = base_names + [f"clean_sink_parent_selector_{i:05d}" for i in range(len(members))]
    if metadata_items != expected_metadata(ordinal, shard, manifest, selectors):
        raise RuntimeError("metadata is not the canonical fully bound shard record")
    if variables != names or clauses[:len(base_clauses)] != base_clauses:
        raise RuntimeError("CNF base or selector map differs")
    suffix = iter(clauses[len(base_clauses):])
    if next(suffix, None) != tuple(selectors):
        raise RuntimeError("missing exact selector ALO")
    name_to_number = {name: i for i, name in enumerate(variables, 1)}
    for selector, (_, _, row) in zip(selectors, members):
        holes = expected_projection(row)[1]
        for pair in PAIRS:
            hole = name_to_number[f"h_{pair[0]}_{pair[1]}"]
            if next(suffix, None) != (-selector, hole if pair in holes else -hole):
                raise RuntimeError("guarded parent projection differs")
    if next(suffix, None) is not None or declared != dimensions(group, len(members)):
        raise RuntimeError("suffix or dimensions differ")
    digest = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
    if SHARD_CNF_SHA256 and digest != SHARD_CNF_SHA256[key]:
        raise RuntimeError("shard hash differs from complete ledger")
    if model_path:
        values, selected = validate_model(variables, clauses, read_model(model_path), selectors)
        holes = expected_projection(members[selected][2])[1]
        if any(values[name_to_number[f"h_{a}_{b}"]] != ((a, b) in holes) for a, b in PAIRS):
            raise RuntimeError("model attribution disagrees with selected parent")
        print(f"PASS model-attribution shard={ordinal:02d} selector={selected} accepted={members[selected][0]} cover={members[selected][1]}")
    print(f"PASS shard={ordinal:02d} key={key} parents={len(members)} vars={declared[0]} clauses={declared[1]} bytes={cnf_path.stat().st_size} sha256={digest}")
    return variables, clauses, members, selectors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()
    check(args.cnf, args.model)


if __name__ == "__main__":
    main()
