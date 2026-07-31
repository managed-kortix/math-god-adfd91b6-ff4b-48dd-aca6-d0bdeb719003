#!/usr/bin/env python3
"""Strict independent checker for residual selector-grouped m=6 forced CNFs."""

import argparse
import hashlib
from collections import Counter
from functools import lru_cache
from pathlib import Path

from check_m6_parent_cnf import (
    BASE_CLAUSES, BASE_CLAUSE_SHA256, BASE_VARIABLES, BASE_VARIABLE_MAP_SHA256,
    COVER_SHA256, FILTER_SHA256, LABELS, PAIRS, clause_sha256, expected_projection,
    parse_cnf, read_acceptance, read_cover, variable_map_sha256,
)
from snc_cnf import generate

HERE = Path(__file__).resolve().parent
FORMAT = "m6-forced-selector-group-cnf-v1"
MANIFEST_FORMAT = "m6-forced-selector-groups-v1"
PROOF_SOURCE = "attempts/tick51-b7-q0-human-proof.md"
HUMAN_PROOF = HERE.parent / PROOF_SOURCE
PROOF_BYTES = 3055
PROOF_SHA256 = "506c0750df64f01885f01f7d8674c70a7a9b5d2885b42a7471c8dd1ed5783a71"
ELIGIBLE_MANIFEST_SHA256 = "751da64e518bc3c880e3cb02b8aa8cdf1a7bcc5e1aff4d16abfc8a42d2cc1950"
GROUP_KEYS = (
    "B6-q0", "B6-q1", "B6-q2", "B6-q3",
    "B7-q1", "B7-q2", "B7-q3", "B7-q4", "B7-q5",
)
GROUP_COUNTS = (6286, 5541, 2410, 412, 9577, 5431, 1584, 297, 30)
RESIDUAL_ROWS = 31568
MANIFEST_BYTES = 1611
MANIFEST_SHA256 = "6cf29f05bc2d76437c10b8c19e173c6d8c666f8001a3b1504ab1cf108932a29c"
GROUP_CNF_SHA256 = {
    "B6-q0": "5ccfa4331ed41a0c84dcf929ffc6577909a46d7f242541f92d0d10d2c5b85be4",
    "B6-q1": "48e329579dd571caedce0eb76bb23bb1dc14fe1e3f6ce8f2067e2eb43f778501",
    "B6-q2": "1b012dadc1a00d582269880496bd4b118317a3d7291d6b58ec69792d847f1560",
    "B6-q3": "634fa13de3c0fbcb5e1040f1366bef8a8c2317783952bf1127d83bf742f11f4a",
    "B7-q1": "0c20f6aa2ad10bb0f43c316fd5d0ce0c0e70d027ebfa6cc0cb26774ad13a84f9",
    "B7-q2": "dd86e95528cf0d8167522c1865741063d1cd95a227777514c9799747a0eeae25",
    "B7-q3": "eb39b1abbd7abd8e7db13c9de89b3c6984f574e365d309a014a1d45ff2a9e08d",
    "B7-q4": "9ff7b0206e2c35ba3f3abaf36302e0493330e92a6244537b0640d2299a295be2",
    "B7-q5": "bdb81f13e64f9e7ac0df95bea013ff78147ac03dac8e50751b903bebb88b6e84",
}


@lru_cache(maxsize=None)
def frozen_inputs(cover_path, filter_path):
    rows = read_cover(Path(cover_path))
    statuses = read_acceptance(Path(filter_path))
    return rows, derive_groups(rows, statuses)


@lru_cache(maxsize=None)
def frozen_base(branch):
    base = generate(18, 6 if branch == "B6" else 7, 6,
                    robust_witness=True, arc_minimal=True)
    return base, list(base.names), list(base.clauses)


def row_parameters(row):
    branch, _, _, _, colors, _, support_holes = row
    totals = Counter()
    for left, right in support_holes:
        cells = sorted((colors[left], colors[right]), key="RABC".index)
        totals["".join(cells)] += 1
    lam = totals["RC"] + totals["AC"] + totals["CC"]
    q = totals["BC"]
    return branch, lam, q, 6 - lam - q


def derive_groups(rows, statuses):
    groups = {key: [] for key in GROUP_KEYS}
    accepted = original_child = 0
    excluded = 0
    for index, (row, status) in enumerate(zip(rows, statuses)):
        if status != 0:
            continue
        branch, lam, q, _ = row_parameters(row)
        forced = lam == (3 if branch == "B6" else 1)
        if forced:
            if branch == "B7" and q == 0:
                excluded += 1
            else:
                key = f"{branch}-q{q}"
                if key not in groups:
                    raise RuntimeError(f"unexpected independently derived group {key}")
                groups[key].append((original_child, accepted, index))
            original_child += 1
        accepted += 1
    if excluded != 8847:
        raise RuntimeError("human-closed B7-q0 count changed")
    if tuple(map(len, groups.values())) != GROUP_COUNTS or sum(map(len, groups.values())) != RESIDUAL_ROWS:
        raise RuntimeError("independently derived residual group partition changed")
    for key, members in groups.items():
        projections = [frozenset(expected_holes(rows[index])) for _, _, index in members]
        if len(set(projections)) != len(projections):
            raise RuntimeError(f"independently derived group {key} has duplicate projections")
    return groups


def member_payload(members):
    records = ["columns\tmember-ordinal,original-child-ordinal,accepted-ordinal,cover-index"]
    records.extend(
        f"{member:05d}\t{original:05d}\t{accepted:05d}\t{index:06d}"
        for member, (original, accepted, index) in enumerate(members)
    )
    return ("\n".join(records) + "\n").encode("ascii")


def dimensions(key, count):
    branch = key[:2]
    c_count = 3 if branch == "B6" else 2
    b_count = 6 if branch == "B6" else 7
    common = b_count * c_count + c_count
    return BASE_VARIABLES + count, BASE_CLAUSES[branch] + common + 1 + 153 * count


def verify_human_proof(path=HUMAN_PROOF):
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if len(payload) != PROOF_BYTES or digest != PROOF_SHA256:
        raise RuntimeError("excluded B7-q0 human proof differs from its frozen identity")


def manifest_payload(groups, proof_path=HUMAN_PROOF):
    verify_human_proof(proof_path)
    records = [
        MANIFEST_FORMAT,
        f"cover-sha256\t{COVER_SHA256}",
        f"filter-sha256\t{FILTER_SHA256}",
        f"eligible-manifest-sha256\t{ELIGIBLE_MANIFEST_SHA256}",
        "excluded-human-cell\tB7-q0:8847",
        f"excluded-human-proof-source\t{PROOF_SOURCE}",
        f"excluded-human-proof-bytes\t{PROOF_BYTES}",
        f"excluded-human-proof-sha256\t{PROOF_SHA256}",
        "groups\t9", f"rows\t{RESIDUAL_ROWS}",
        "columns\tgroup-ordinal,key,branch,q,h,members,first-selector,last-selector,variables,clauses,member-sha256",
    ]
    for ordinal, key in enumerate(GROUP_KEYS):
        members = groups[key]
        branch = key[:2]
        q = int(key[4:])
        h = (3 if branch == "B6" else 5) - q
        variables, clauses = dimensions(key, len(members))
        digest = hashlib.sha256(member_payload(members)).hexdigest()
        records.append(
            f"{ordinal}\t{key}\t{branch}\t{q}\t{h}\t{len(members)}\t23617\t"
            f"{BASE_VARIABLES + len(members)}\t{variables}\t{clauses}\t{digest}"
        )
    return ("\n".join(records) + "\n").encode("ascii")


def selector_name(member):
    return f"forced_group_selector_{member:05d}"


def expected_holes(row):
    return expected_projection(row)[1]


def validate_model(variables, clauses, literals, selector_count):
    values = {}
    for literal in literals:
        if literal == 0 or abs(literal) > len(variables):
            raise RuntimeError("model contains an invalid literal")
        number = abs(literal)
        value = literal > 0
        if number in values and values[number] != value:
            raise RuntimeError("model assigns both polarities")
        values[number] = value
    missing = [number for number in range(1, len(variables) + 1) if number not in values]
    if missing:
        raise RuntimeError(f"model omits {len(missing)} CNF variables")
    for ordinal, clause in enumerate(clauses):
        if not any(values[abs(literal)] == (literal > 0) for literal in clause):
            raise RuntimeError(f"model falsifies CNF clause {ordinal}")
    selector_numbers = range(BASE_VARIABLES + 1, BASE_VARIABLES + selector_count + 1)
    selected = [number - BASE_VARIABLES - 1 for number in selector_numbers if values[number]]
    if len(selected) != 1:
        raise RuntimeError(f"model must have exactly one true group selector, found {len(selected)}")
    return values, selected[0]


def attribute_model(variables, clauses, literals, rows, members):
    values, member = validate_model(variables, clauses, literals, len(members))
    hole_numbers = {}
    for number, name in enumerate(variables, 1):
        if name.startswith("h_"):
            _, left, right = name.split("_")
            hole_numbers[(int(left), int(right))] = number
    index = members[member][2]
    holes = expected_holes(rows[index])
    for pair in PAIRS:
        number = hole_numbers[pair]
        if values[number] != (pair in holes):
            raise RuntimeError("true selector disagrees with its guarded hole projection")
    return [(member,) + members[member]]


def read_model(path):
    literals = []
    terminated = False
    with path.open("r", encoding="ascii") as handle:
        for line_number, raw in enumerate(handle, 1):
            line = raw.strip()
            if not line or line.startswith("c ") or line in ("s SATISFIABLE", "SAT"):
                continue
            fields = line[2:].split() if line.startswith("v ") else line.split()
            try:
                values = [int(field) for field in fields]
            except ValueError as error:
                raise RuntimeError(f"noninteger model token line {line_number}") from error
            for value in values:
                if terminated:
                    raise RuntimeError("model has data after its zero terminator")
                if value == 0:
                    terminated = True
                else:
                    literals.append(value)
    if not terminated:
        raise RuntimeError("model has no zero terminator")
    return literals


def check(cnf_path, cover_path, filter_path, model_path=None, proof_path=HUMAN_PROOF):
    rows, groups = frozen_inputs(str(cover_path.resolve()), str(filter_path.resolve()))
    manifest = manifest_payload(groups, proof_path)
    manifest_hash = hashlib.sha256(manifest).hexdigest()
    if MANIFEST_BYTES and (len(manifest) != MANIFEST_BYTES or manifest_hash != MANIFEST_SHA256):
        raise RuntimeError("independent group manifest fingerprint changed")

    metadata_items, variables, clauses, declared = parse_cnf(cnf_path)
    metadata = dict(metadata_items)
    ordinal = int(metadata.get("group-ordinal", "-1"))
    if not 0 <= ordinal < len(GROUP_KEYS):
        raise RuntimeError("group ordinal is outside the frozen manifest")
    key = GROUP_KEYS[ordinal]
    members = groups[key]
    branch = key[:2]
    q = int(key[4:])
    h = (3 if branch == "B6" else 5) - q
    member_hash = hashlib.sha256(member_payload(members)).hexdigest()
    c_labels = tuple(LABELS[branch]["C"])
    b_labels = tuple(LABELS[branch]["B"])
    expected_metadata = [
        ("format", FORMAT), ("group-manifest-format", MANIFEST_FORMAT),
        ("group-manifest-bytes", str(len(manifest))),
        ("group-manifest-sha256", manifest_hash),
        ("cover-sha256", COVER_SHA256), ("filter-sha256", FILTER_SHA256),
        ("eligible-manifest-sha256", ELIGIBLE_MANIFEST_SHA256),
        ("excluded-human-cell", "B7-q0:8847"),
        ("excluded-human-proof-source", PROOF_SOURCE),
        ("excluded-human-proof-bytes", str(PROOF_BYTES)),
        ("excluded-human-proof-sha256", PROOF_SHA256),
        ("group-ordinal", str(ordinal)), ("group-key", key), ("branch", branch),
        ("q", str(q)), ("h", str(h)), ("members", str(len(members))),
        ("member-sha256", member_hash), ("base-variables", str(BASE_VARIABLES)),
        ("base-variable-map-sha256", BASE_VARIABLE_MAP_SHA256),
        ("base-clauses", str(BASE_CLAUSES[branch])),
        ("base-clause-sha256", BASE_CLAUSE_SHA256[branch]),
        ("orientation-units", str(len(c_labels) * len(b_labels))),
        ("high-c-units", str(len(c_labels))), ("alo-clauses", "1"),
        ("guarded-hole-clauses-per-member", "153"),
        ("first-selector", str(BASE_VARIABLES + 1)),
        ("last-selector", str(BASE_VARIABLES + len(members))),
    ]
    if metadata_items != expected_metadata:
        raise RuntimeError("metadata is not the exact canonical group record")

    base, base_names, base_clauses = frozen_base(branch)
    if (len(base_names) != BASE_VARIABLES or
            variable_map_sha256(base_names) != BASE_VARIABLE_MAP_SHA256 or
            len(base_clauses) != BASE_CLAUSES[branch] or
            clause_sha256(base_clauses) != BASE_CLAUSE_SHA256[branch]):
        raise RuntimeError("independent base reconstruction misses its frozen fingerprint")
    expected_variables = base_names + [selector_name(member) for member in range(len(members))]
    if variables != expected_variables:
        raise RuntimeError("variable map is not base plus consecutive fresh selectors")
    common = [(-base.names[f"a_{c}_{b}"],) for c in c_labels for b in b_labels]
    common += [(base.names[f"cnt_d1_{c}_17_9"],) for c in c_labels]
    selectors = list(range(BASE_VARIABLES + 1, BASE_VARIABLES + len(members) + 1))
    guarded = []
    for selector, (_, _, index) in zip(selectors, members):
        holes = expected_holes(rows[index])
        for pair in PAIRS:
            hole = base.names[f"h_{pair[0]}_{pair[1]}"]
            guarded.append((-selector, hole if pair in holes else -hole))
    expected_clauses = base_clauses + common + [tuple(selectors)] + guarded
    if clauses != expected_clauses:
        raise RuntimeError("clause stream is not base, common suffix, ALO, and guarded rows")
    if declared != dimensions(key, len(members)):
        raise RuntimeError("DIMACS dimensions differ from the frozen group shape")
    file_hash = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
    expected_hash = GROUP_CNF_SHA256.get(key)
    if expected_hash and file_hash != expected_hash:
        raise RuntimeError("group CNF file hash differs from its frozen fingerprint")
    print(
        f"PASS group={key} members={len(members)} vars={declared[0]} clauses={declared[1]} "
        f"bytes={cnf_path.stat().st_size} sha256={file_hash}"
    )
    if model_path is not None:
        attributed = attribute_model(variables, clauses, read_model(model_path), rows, members)
        print("PASS model-attribution " + " ".join(
            f"member={member}:original-child={original}:accepted={accepted}:cover={index}"
            for member, original, accepted, index in attributed
        ))
    return variables, rows, members


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--cover", type=Path, default=HERE / "m6-placement-cover.txt")
    parser.add_argument("--filter", type=Path, default=HERE / "m6-placement-filter.txt")
    parser.add_argument("--human-proof", type=Path, default=HUMAN_PROOF)
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()
    check(args.cnf, args.cover, args.filter, args.model, args.human_proof)


if __name__ == "__main__":
    main()
