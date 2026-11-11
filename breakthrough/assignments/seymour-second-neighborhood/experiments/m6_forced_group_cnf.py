#!/usr/bin/env python3
"""Emit selector-grouped CNFs for the residual frozen m=6 forced children."""

import argparse
import hashlib
from pathlib import Path

import m6_forced_child_cnf as child

HERE = Path(__file__).resolve().parent
FORMAT = "m6-forced-selector-group-cnf-v1"
MANIFEST_FORMAT = "m6-forced-selector-groups-v1"
PROOF_SOURCE = "attempts/tick51-b7-q0-human-proof.md"
HUMAN_PROOF = HERE.parent / PROOF_SOURCE
PROOF_BYTES = 3055
PROOF_SHA256 = "506c0750df64f01885f01f7d8674c70a7a9b5d2885b42a7471c8dd1ed5783a71"
GROUP_KEYS = (
    "B6-q0", "B6-q1", "B6-q2", "B6-q3",
    "B7-q1", "B7-q2", "B7-q3", "B7-q4", "B7-q5",
)
GROUP_COUNTS = {
    "B6-q0": 6286, "B6-q1": 5541, "B6-q2": 2410, "B6-q3": 412,
    "B7-q1": 9577, "B7-q2": 5431, "B7-q3": 1584, "B7-q4": 297,
    "B7-q5": 30,
}
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


def residual_groups(eligible):
    groups = {key: [] for key in GROUP_KEYS}
    for original_child, (accepted, row) in enumerate(eligible):
        _, q, _ = child.hole_parameters(row)
        if row["branch"] == "B7" and q == 0:
            continue
        key = f"{row['branch']}-q{q}"
        if key not in groups:
            raise RuntimeError(f"unexpected residual forced cell {key}")
        groups[key].append((original_child, accepted, row))
    counts = {key: len(rows) for key, rows in groups.items()}
    if counts != GROUP_COUNTS or sum(counts.values()) != RESIDUAL_ROWS:
        raise RuntimeError(f"residual forced partition changed: {counts}")
    for key, members in groups.items():
        projections = []
        for _, _, row in members:
            _, holes = child.parent.embedded_holes(key[:2], row["word"], row["edges"])
            projections.append(frozenset(holes))
        if len(set(projections)) != len(projections):
            raise RuntimeError(f"group {key} has duplicate member projections")
    return groups


def member_payload(members):
    lines = ["columns\tmember-ordinal,original-child-ordinal,accepted-ordinal,cover-index"]
    for member, (original_child, accepted, row) in enumerate(members):
        lines.append(
            f"{member:05d}\t{original_child:05d}\t{accepted:05d}\t{row['cover_index']:06d}"
        )
    return ("\n".join(lines) + "\n").encode("ascii")


def group_shape(key, count):
    branch = key[:2]
    labels = child.parent.CELL_LABELS[branch]
    common = len(labels[2]) * len(labels[3]) + len(labels[3])
    variables = child.parent.BASE_VARIABLES + count
    clauses = child.parent.BASE_CLAUSES[branch] + common + 1 + len(child.parent.PAIRS) * count
    return branch, variables, clauses, common


def verify_human_proof(path=HUMAN_PROOF):
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if len(payload) != PROOF_BYTES or digest != PROOF_SHA256:
        raise RuntimeError("excluded B7-q0 human proof differs from its frozen identity")


def manifest_payload(groups, proof_path=HUMAN_PROOF):
    verify_human_proof(proof_path)
    lines = [
        MANIFEST_FORMAT,
        f"cover-sha256\t{child.parent.COVER_SHA256}",
        f"filter-sha256\t{child.parent.FILTER_SHA256}",
        f"eligible-manifest-sha256\t{child.MANIFEST_SHA256}",
        "excluded-human-cell\tB7-q0:8847",
        f"excluded-human-proof-source\t{PROOF_SOURCE}",
        f"excluded-human-proof-bytes\t{PROOF_BYTES}",
        f"excluded-human-proof-sha256\t{PROOF_SHA256}",
        f"groups\t{len(GROUP_KEYS)}",
        f"rows\t{RESIDUAL_ROWS}",
        "columns\tgroup-ordinal,key,branch,q,h,members,first-selector,last-selector,variables,clauses,member-sha256",
    ]
    for ordinal, key in enumerate(GROUP_KEYS):
        members = groups[key]
        branch = key[:2]
        q = int(key[4:])
        h = (3 if branch == "B6" else 5) - q
        _, variables, clauses, _ = group_shape(key, len(members))
        digest = hashlib.sha256(member_payload(members)).hexdigest()
        first = child.parent.BASE_VARIABLES + 1
        last = child.parent.BASE_VARIABLES + len(members)
        lines.append(
            f"{ordinal}\t{key}\t{branch}\t{q}\t{h}\t{len(members)}\t{first}\t{last}\t"
            f"{variables}\t{clauses}\t{digest}"
        )
    return ("\n".join(lines) + "\n").encode("ascii")


def selector_name(member):
    return f"forced_group_selector_{member:05d}"


def build_group(key, members):
    branch = key[:2]
    cnf = child.parent.generate(
        18, 6 if branch == "B6" else 7, 6, robust_witness=True, arc_minimal=True
    )
    if (len(cnf.names) != child.parent.BASE_VARIABLES or
            child.parent.variable_map_sha256(cnf) != child.parent.BASE_VARIABLE_MAP_SHA256 or
            len(cnf.clauses) != child.parent.BASE_CLAUSES[branch] or
            child.parent.clause_sha256(cnf.clauses) != child.parent.BASE_CLAUSE_SHA256[branch]):
        raise RuntimeError("generated base CNF differs from the frozen branch")
    common = child.forced_suffix(cnf, branch)
    cnf.clauses.extend(common)
    selectors = [cnf.var(selector_name(member)) for member in range(len(members))]
    cnf.add(*selectors)
    for selector, (_, _, row) in zip(selectors, members):
        _, holes = child.parent.embedded_holes(branch, row["word"], row["edges"])
        for left, right in child.parent.PAIRS:
            hole = cnf.names[f"h_{left}_{right}"]
            cnf.add(-selector, hole if (left, right) in holes else -hole)
    return cnf, common, selectors


def write_group(path, key, members, cnf, common, selectors, manifest):
    branch = key[:2]
    q = int(key[4:])
    h = (3 if branch == "B6" else 5) - q
    member_hash = hashlib.sha256(member_payload(members)).hexdigest()
    metadata = [
        ("format", FORMAT), ("group-manifest-format", MANIFEST_FORMAT),
        ("group-manifest-bytes", str(len(manifest))),
        ("group-manifest-sha256", hashlib.sha256(manifest).hexdigest()),
        ("cover-sha256", child.parent.COVER_SHA256),
        ("filter-sha256", child.parent.FILTER_SHA256),
        ("eligible-manifest-sha256", child.MANIFEST_SHA256),
        ("excluded-human-cell", "B7-q0:8847"),
        ("excluded-human-proof-source", PROOF_SOURCE),
        ("excluded-human-proof-bytes", str(PROOF_BYTES)),
        ("excluded-human-proof-sha256", PROOF_SHA256),
        ("group-ordinal", str(GROUP_KEYS.index(key))), ("group-key", key),
        ("branch", branch), ("q", str(q)), ("h", str(h)),
        ("members", str(len(members))), ("member-sha256", member_hash),
        ("base-variables", str(child.parent.BASE_VARIABLES)),
        ("base-variable-map-sha256", child.parent.BASE_VARIABLE_MAP_SHA256),
        ("base-clauses", str(child.parent.BASE_CLAUSES[branch])),
        ("base-clause-sha256", child.parent.BASE_CLAUSE_SHA256[branch]),
        ("orientation-units", str(len(common) - len(child.parent.CELL_LABELS[branch][3]))),
        ("high-c-units", str(len(child.parent.CELL_LABELS[branch][3]))),
        ("alo-clauses", "1"), ("guarded-hole-clauses-per-member", "153"),
        ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1])),
    ]
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata:
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def load_partition(cover, filter_path):
    rows = child.parent.load_cover(cover)
    statuses = child.parent.load_statuses(filter_path)
    return residual_groups(child.eligible_rows(rows, statuses))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=GROUP_KEYS)
    parser.add_argument("--cover", type=Path, default=child.parent.COVER)
    parser.add_argument("--filter", type=Path, default=child.parent.FILTER)
    parser.add_argument("--human-proof", type=Path, default=HUMAN_PROOF)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is None and args.manifest_output is None:
        parser.error("at least one of --output and --manifest-output is required")
    if args.output is not None and args.group is None:
        parser.error("--output requires --group")
    groups = load_partition(args.cover, args.filter)
    manifest = manifest_payload(groups, args.human_proof)
    digest = hashlib.sha256(manifest).hexdigest()
    if MANIFEST_BYTES and (len(manifest) != MANIFEST_BYTES or digest != MANIFEST_SHA256):
        raise RuntimeError("group manifest differs from its frozen fingerprint")
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.output:
        cnf, common, selectors = build_group(args.group, groups[args.group])
        write_group(args.output, args.group, groups[args.group], cnf, common, selectors, manifest)
        file_hash = hashlib.sha256(args.output.read_bytes()).hexdigest()
        expected = GROUP_CNF_SHA256.get(args.group)
        if expected and file_hash != expected:
            raise RuntimeError("group CNF differs from its frozen fingerprint")
        print(
            f"group={args.group} members={len(groups[args.group])} vars={len(cnf.names)} "
            f"clauses={len(cnf.clauses)} bytes={args.output.stat().st_size} sha256={file_hash}"
        )
    print(f"groups=9 rows={RESIDUAL_ROWS} manifest_bytes={len(manifest)} sha256={digest}")


if __name__ == "__main__":
    main()
