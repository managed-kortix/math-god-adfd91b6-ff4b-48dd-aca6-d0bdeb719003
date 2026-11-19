#!/usr/bin/env python3
"""Emit exact selector-grouped CNFs for the residual frozen m=6 frontier."""

import argparse
import hashlib
import itertools
from collections import Counter
from pathlib import Path

import m6_parent_cnf as parent
from snc_cnf import threshold

HERE = Path(__file__).resolve().parent
FORMAT = "m6-residual-selector-group-cnf-v1"
MANIFEST_FORMAT = "m6-residual-selector-groups-v1"
CERTIFICATE_LEDGER = HERE / "m6-forced-group-certificates.tsv"
CERTIFICATE_VERIFIER = HERE / "verify_m6_forced_group_certificates.py"
FORCED_MANIFEST = HERE / "m6-forced-selector-groups.tsv"
IDENTITIES = {
    "forced-certificate-ledger": (4060, "819cc1c2015923d2ef59649028a34a841641519e5c46ef7559698720e18f5c65"),
    "forced-certificate-verifier": (5794, "d2e15b03ba68e6222cf140e0f742f2c1ae627e7ae0f1f657966bf8c48d51cebf"),
    "forced-selector-manifest": (1611, "6cf29f05bc2d76437c10b8c19e173c6d8c666f8001a3b1504ab1cf108932a29c"),
}
EXCLUSIONS = ("B6:lambda=3", "B7:lambda=1")
GROUP_KEYS = (
    "B6-l4-r0-t2", "B6-l4-r1-t3",
    "B6-l5-r0-t1", "B6-l5-r1-t2", "B6-l5-r2-t3",
    "B6-l6-r0-t0", "B6-l6-r1-t1", "B6-l6-r2-t2", "B6-l6-r3-t3",
    "B7-l2-r0-t1", "B7-l2-r1-t2",
    "B7-l3-r0-t0", "B7-l3-r1-t1", "B7-l3-r2-t2",
    "B7-l4-r1-t0", "B7-l4-r2-t1", "B7-l4-r3-t2",
    "B7-l5-r2-t0", "B7-l5-r3-t1", "B7-l5-r4-t2",
    "B7-l6-r3-t0", "B7-l6-r4-t1", "B7-l6-r5-t2",
)
GROUP_COUNTS = (
    6679, 6679, 1576, 1910, 1910, 167, 310, 340, 340,
    17689, 17689, 5016, 6981, 6981, 1649, 1943, 1943,
    322, 358, 358, 42, 46, 46,
)
GROUP_CNF_SHA256 = {
    "B6-l4-r0-t2": "d084873ba4f0e5f4c04777b9a49cecbc395ba3c552038c0301c26a21c8a6e62f",
    "B6-l4-r1-t3": "541f990890cb268d8a02a579ca56568e852d914ca8d9f793b4ca54e793ff7b19",
    "B6-l5-r0-t1": "3ab1592bed3b9b47edf6a02232c4a7d8e862ebf6570c24516f239ab393c10291",
    "B6-l5-r1-t2": "65054cf65b0c7a969447ea2428e8efe18fd5a5aca339d3f4e9569c23f8118448",
    "B6-l5-r2-t3": "3133a0f4254e60b2edb26beb999ee5310dba02a525e6e86b7b1f394afaa31ac0",
    "B6-l6-r0-t0": "4583f05df489799afb994d80f3cd5b7342924b6642d57552f887c1fb21bd674b",
    "B6-l6-r1-t1": "9b10be6dbca83c25a857e0da0e9a2718f05d09a50eff086f0c218f12a6bf0ca9",
    "B6-l6-r2-t2": "7a4dfb9def8ff473d6d990003e523807860c0a57d7f7b2e8e3261c14e0e7c842",
    "B6-l6-r3-t3": "7c9ac22fb54a1273582fa1bafdb03c2c2bba11a0dfa8751ffb8aa2b5c4538ee7",
    "B7-l2-r0-t1": "530b31ade1004cedc2a223ae9599469a761880780f52d31232366e9015f44426",
    "B7-l2-r1-t2": "03d1137f79460e66a2894d8d29f1bcc877f2636762fc5b9342d3ee312d174ace",
    "B7-l3-r0-t0": "6ccb5da5f75c1272c69185032f7661fe4b553a5413cfd28ecfe414798dcac60d",
    "B7-l3-r1-t1": "deb0a7b2350fc355cfa998038ddc13cb3fdf971777d2391850867464b36fd8ee",
    "B7-l3-r2-t2": "9d74bb0711953bd1d1a154f6c1a3659ea5c1cc9bc9deb94a927b323b00792f34",
    "B7-l4-r1-t0": "0be75640eb45fc62c817a396765465e90b9165eda405a5453ea91838f8da0d5f",
    "B7-l4-r2-t1": "cdd7df07b3b155a19dd00bcadfb0c3ed45288f2e3a913d5d6c3c3c4bda54241a",
    "B7-l4-r3-t2": "9aa5d6bb979b3369c8cd15305a1bbf98adca02af5f8f92a6881aedbf3b999270",
    "B7-l5-r2-t0": "f535f1797b0148b2b2c601ef0a641461dfea45678f889489cf4317138d015f64",
    "B7-l5-r3-t1": "c93086a1ab2d9cfb8d5dfffcfa8c356684f3e3ff3e0501d1f3405b38e0208cd0",
    "B7-l5-r4-t2": "9fad28d1f675f807aec327739bb746d89a5852b95786e21bf17ebbd6a3c24b94",
    "B7-l6-r3-t0": "e8af05abc8ef494227c6bd5aa0790f7bfc15a67280fcd022e0068cdab259838d",
    "B7-l6-r4-t1": "18157e438bec5a28c0ad82dd4da36f73a0c8b779cccdcb8b9b63e52ef879e33c",
    "B7-l6-r5-t2": "a1baeed7c055c635a1aaa3ab6848541bad2f47f5f00547c3bb2abefe33561dcc",
}
RESIDUAL_MEMBERSHIPS = 80974
BRANCH_MEMBERSHIPS = {"B6": 19911, "B7": 61063}
MANIFEST_BYTES = 3915
MANIFEST_SHA256 = "b55f0b8e69a77b64254285b9134262cedb961e18a13ad10e4ce350bd04caa85a"


def verify_identity(path, expected):
    payload = path.read_bytes()
    if (len(payload), hashlib.sha256(payload).hexdigest()) != expected:
        raise RuntimeError(f"frozen exclusion identity changed: {path.name}")


def verify_exclusion_identities():
    verify_identity(CERTIFICATE_LEDGER, IDENTITIES["forced-certificate-ledger"])
    verify_identity(CERTIFICATE_VERIFIER, IDENTITIES["forced-certificate-verifier"])
    verify_identity(FORCED_MANIFEST, IDENTITIES["forced-selector-manifest"])


def hole_parameters(row):
    totals = Counter()
    for left, right in row["edges"]:
        cells = sorted((row["word"][left], row["word"][right]), key="RABC".index)
        totals["".join(cells)] += 1
    return totals["RC"] + totals["AC"] + totals["CC"]


def feasible_rt(row):
    """Derive (C->B arc count, high-C count) from exact pointwise C states."""
    branch = row["branch"]
    labels = parent.CELL_LABELS[branch]
    embedding, holes = parent.embedded_holes(branch, row["word"], row["edges"])
    colors = {}
    for index, cell in enumerate("RABC"):
        colors.update((vertex, cell) for vertex in labels[index])
    cs = labels[3]
    present_cc = [pair for pair in itertools.combinations(cs, 2) if pair not in holes]
    states = set()
    for directions in itertools.product((0, 1), repeat=len(present_cc)):
        internal = Counter(pair[direction] for pair, direction in zip(present_cc, directions))
        choices = []
        for c in cs:
            fixed = sum(colors[v] in "RA" and tuple(sorted((c, v))) not in holes
                        for v in range(18)) + internal[c]
            available = sum(colors[v] == "B" and tuple(sorted((c, v))) not in holes
                            for v in range(18))
            pointwise = []
            for target in (8, 9):
                required = target - fixed
                if 0 <= required <= available:
                    pointwise.append((required, int(target == 9)))
            choices.append(pointwise)
        for state in itertools.product(*choices):
            states.add((sum(value[0] for value in state), sum(value[1] for value in state)))
    if not states:
        raise RuntimeError(f"accepted row {row['cover_index']} has no exact pointwise C state")
    return states


def key_parameters(key):
    branch, lam, r, t = key.split("-")
    return branch, int(lam[1:]), int(r[1:]), int(t[1:])


def residual_groups(rows, statuses):
    groups = {key: [] for key in GROUP_KEYS}
    accepted = 0
    excluded = Counter()
    for row, status in zip(rows, statuses):
        if status != 0:
            continue
        lam = hole_parameters(row)
        branch = row["branch"]
        if (branch, lam) in (("B6", 3), ("B7", 1)):
            excluded[branch] += 1
        else:
            for r, t in sorted(feasible_rt(row)):
                key = f"{branch}-l{lam}-r{r}-t{t}"
                if key not in groups:
                    raise RuntimeError(f"unexpected residual state {key}")
                groups[key].append((accepted, row))
        accepted += 1
    if excluded != Counter(B6=14649, B7=25766):
        raise RuntimeError(f"forced exclusion changed: {excluded}")
    counts = tuple(len(groups[key]) for key in GROUP_KEYS)
    if counts != GROUP_COUNTS or sum(counts) != RESIDUAL_MEMBERSHIPS:
        raise RuntimeError(f"residual partition changed: {counts}")
    branch_counts = Counter(key[:2] for key, members in groups.items() for _ in members)
    if branch_counts != Counter(BRANCH_MEMBERSHIPS):
        raise RuntimeError(f"residual branch subtotals changed: {branch_counts}")
    for key, members in groups.items():
        projections = [frozenset(parent.embedded_holes(
            key[:2], row["word"], row["edges"])[1]) for _, row in members]
        if len(set(projections)) != len(projections):
            raise RuntimeError(f"group {key} has duplicate parent projections")
    return groups


def member_payload(members):
    lines = ["columns\tmember-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{member:05d}\t{accepted:05d}\t{row['cover_index']:06d}"
                 for member, (accepted, row) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def cardinality_shape(inputs, target):
    if not 0 <= target <= inputs:
        raise ValueError("invalid exact cardinality")
    return inputs * (inputs + 1) // 2, 2 * inputs * inputs + (1 if target in (0, inputs) else 2)


def group_shape(key, members):
    branch, _, r, t = key_parameters(key)
    b_count = len(parent.CELL_LABELS[branch][2])
    c_count = len(parent.CELL_LABELS[branch][3])
    r_vars, r_clauses = cardinality_shape(b_count * c_count, r)
    t_vars, t_clauses = cardinality_shape(c_count, t)
    variables = parent.BASE_VARIABLES + r_vars + t_vars + members
    clauses = parent.BASE_CLAUSES[branch] + r_clauses + t_clauses + 1 + 153 * members
    return variables, clauses, r_vars, r_clauses, t_vars, t_clauses


def exact(cnf, outputs, value):
    if value == 0:
        cnf.add(-outputs[0])
    elif value == len(outputs):
        cnf.add(outputs[-1])
    else:
        cnf.add(outputs[value - 1])
        cnf.add(-outputs[value])


def add_counters(cnf, key):
    branch, _, r, t = key_parameters(key)
    b_labels, c_labels = parent.CELL_LABELS[branch][2:]
    before_variables, before_clauses = len(cnf.names), len(cnf.clauses)
    r_outputs = threshold(cnf, [cnf.names[f"a_{c}_{b}"] for c in c_labels for b in b_labels],
                          "residual_r")
    exact(cnf, r_outputs, r)
    r_shape = len(cnf.names) - before_variables, len(cnf.clauses) - before_clauses
    before_variables, before_clauses = len(cnf.names), len(cnf.clauses)
    t_outputs = threshold(cnf, [cnf.names[f"cnt_d1_{c}_17_9"] for c in c_labels],
                          "residual_highC")
    exact(cnf, t_outputs, t)
    t_shape = len(cnf.names) - before_variables, len(cnf.clauses) - before_clauses
    return r_shape, t_shape


def build_group(key, members):
    branch = key[:2]
    cnf = parent.generate(18, 6 if branch == "B6" else 7, 6,
                          robust_witness=True, arc_minimal=True)
    if (len(cnf.names) != parent.BASE_VARIABLES or
            parent.variable_map_sha256(cnf) != parent.BASE_VARIABLE_MAP_SHA256 or
            len(cnf.clauses) != parent.BASE_CLAUSES[branch] or
            parent.clause_sha256(cnf.clauses) != parent.BASE_CLAUSE_SHA256[branch]):
        raise RuntimeError("generated base CNF differs from frozen branch")
    counter_shapes = add_counters(cnf, key)
    selectors = [cnf.var(f"residual_group_selector_{member:05d}")
                 for member in range(len(members))]
    cnf.add(*selectors)
    for selector, (_, row) in zip(selectors, members):
        holes = parent.embedded_holes(row["branch"], row["word"], row["edges"])[1]
        for pair in parent.PAIRS:
            hole = cnf.names[f"h_{pair[0]}_{pair[1]}"]
            cnf.add(-selector, hole if pair in holes else -hole)
    return cnf, counter_shapes, selectors


def manifest_payload(groups):
    verify_exclusion_identities()
    lines = [
        MANIFEST_FORMAT,
        f"cover-sha256\t{parent.COVER_SHA256}",
        f"filter-sha256\t{parent.FILTER_SHA256}",
        f"excluded-regimes\t{';'.join(EXCLUSIONS)}",
    ]
    for name, (size, digest) in IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.extend((
        f"groups\t{len(GROUP_KEYS)}", f"memberships\t{RESIDUAL_MEMBERSHIPS}",
        *(f"{branch}-memberships\t{count}" for branch, count in BRANCH_MEMBERSHIPS.items()),
        "columns\tgroup-ordinal,key,branch,lambda,r,t,members,first-selector,last-selector,variables,clauses,r-counter-variables,r-counter-clauses,highC-counter-variables,highC-counter-clauses,member-sha256",
    ))
    for ordinal, key in enumerate(GROUP_KEYS):
        members = groups[key]
        branch, lam, r, t = key_parameters(key)
        variables, clauses, rv, rc, tv, tc = group_shape(key, len(members))
        first = variables - len(members) + 1
        lines.append(f"{ordinal}\t{key}\t{branch}\t{lam}\t{r}\t{t}\t{len(members)}\t"
                     f"{first}\t{variables}\t{variables}\t{clauses}\t{rv}\t{rc}\t{tv}\t{tc}\t"
                     f"{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def write_group(path, key, members, cnf, counter_shapes, selectors, manifest):
    branch, lam, r, t = key_parameters(key)
    metadata = [
        ("format", FORMAT), ("group-manifest-format", MANIFEST_FORMAT),
        ("group-manifest-bytes", str(len(manifest))),
        ("group-manifest-sha256", hashlib.sha256(manifest).hexdigest()),
        ("cover-sha256", parent.COVER_SHA256), ("filter-sha256", parent.FILTER_SHA256),
        ("excluded-regimes", ";".join(EXCLUSIONS)),
    ]
    for name, (size, digest) in IDENTITIES.items():
        metadata.extend(((f"{name}-bytes", str(size)), (f"{name}-sha256", digest)))
    metadata.extend((
        ("group-ordinal", str(GROUP_KEYS.index(key))), ("group-key", key),
        ("branch", branch), ("lambda", str(lam)), ("r", str(r)), ("highC", str(t)),
        ("members", str(len(members))),
        ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
        ("base-variables", str(parent.BASE_VARIABLES)),
        ("base-variable-map-sha256", parent.BASE_VARIABLE_MAP_SHA256),
        ("base-clauses", str(parent.BASE_CLAUSES[branch])),
        ("base-clause-sha256", parent.BASE_CLAUSE_SHA256[branch]),
        ("r-counter-variables", str(counter_shapes[0][0])),
        ("r-counter-clauses", str(counter_shapes[0][1])),
        ("highC-counter-variables", str(counter_shapes[1][0])),
        ("highC-counter-clauses", str(counter_shapes[1][1])),
        ("alo-clauses", "1"), ("guarded-hole-clauses-per-member", "153"),
        ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1])),
    ))
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata:
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def load_partition(cover=parent.COVER, filter_path=parent.FILTER):
    return residual_groups(parent.load_cover(cover), parent.load_statuses(filter_path))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=GROUP_KEYS)
    parser.add_argument("--cover", type=Path, default=parent.COVER)
    parser.add_argument("--filter", type=Path, default=parent.FILTER)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is None and args.manifest_output is None:
        parser.error("at least one output is required")
    if args.output is not None and args.group is None:
        parser.error("--output requires --group")
    groups = load_partition(args.cover, args.filter)
    manifest = manifest_payload(groups)
    digest = hashlib.sha256(manifest).hexdigest()
    if MANIFEST_BYTES and (len(manifest) != MANIFEST_BYTES or digest != MANIFEST_SHA256):
        raise RuntimeError("residual manifest differs from frozen fingerprint")
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.output:
        cnf, shapes, selectors = build_group(args.group, groups[args.group])
        write_group(args.output, args.group, groups[args.group], cnf, shapes, selectors, manifest)
        file_hash = hashlib.sha256(args.output.read_bytes()).hexdigest()
        if GROUP_CNF_SHA256 and file_hash != GROUP_CNF_SHA256[args.group]:
            raise RuntimeError("group CNF differs from frozen fingerprint")
        print(f"group={args.group} members={len(groups[args.group])} vars={len(cnf.names)} "
              f"clauses={len(cnf.clauses)} bytes={args.output.stat().st_size} sha256={file_hash}")
    print(f"groups=23 memberships={RESIDUAL_MEMBERSHIPS} manifest_bytes={len(manifest)} sha256={digest}")


if __name__ == "__main__":
    main()
