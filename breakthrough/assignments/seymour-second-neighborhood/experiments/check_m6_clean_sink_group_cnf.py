#!/usr/bin/env python3
"""Independent checker for clean-sink remaining exact parent-selector CNFs."""

import argparse
import hashlib
from functools import lru_cache
from pathlib import Path

import check_m6_clean_sink_manifest as clean_sink
from check_m6_parent_cnf import (
    BASE_CLAUSES, BASE_CLAUSE_SHA256, BASE_VARIABLES, BASE_VARIABLE_MAP_SHA256,
    PAIRS, clause_sha256, expected_projection, parse_cnf, read_acceptance,
    read_cover, variable_map_sha256,
)
from snc_cnf import generate

HERE = Path(__file__).resolve().parent
FORMAT = "m6-clean-sink-selector-group-cnf-v1"
MANIFEST_FORMAT = "m6-clean-sink-selector-groups-v1"
REMAINING = HERE / "m6-clean-sink-remaining.tsv"
IDENTITY_PATHS = {
    "remaining-stream": REMAINING,
    "clean-sink-manifest": HERE / "m6-clean-sink-manifest.tsv",
    "clean-sink-theorem": HERE.parent / "attempts" / "tick52-rooted-clean-sink-theorem.md",
    "forced-certificate-ledger": HERE / "m6-forced-group-certificates.tsv",
    "forced-certificate-verifier": HERE / "verify_m6_forced_group_certificates.py",
    "forced-selector-manifest": HERE / "m6-forced-selector-groups.tsv",
}
IDENTITIES = {
    "remaining-stream": (2262190, "416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642"),
    "clean-sink-manifest": (2104, "733e06c8aa9881e0006409efff23729f1bf88d8af7b1a70e8a78fd3775b53217"),
    "clean-sink-theorem": (4156, "bd0631529bb4658061663460b718ef2ee3186d02fdc599fb2673d3cff3b94ee2"),
    "forced-certificate-ledger": (4060, "819cc1c2015923d2ef59649028a34a841641519e5c46ef7559698720e18f5c65"),
    "forced-certificate-verifier": (5794, "d2e15b03ba68e6222cf140e0f742f2c1ae627e7ae0f1f657966bf8c48d51cebf"),
    "forced-selector-manifest": (1611, "6cf29f05bc2d76437c10b8c19e173c6d8c666f8001a3b1504ab1cf108932a29c"),
}
GROUP_KEYS = ("B6-l4", "B6-l5", "B6-l6", "B7-l2", "B7-l3", "B7-l4", "B7-l5", "B7-l6")
GROUP_COUNTS = (2470, 1024, 220, 8119, 5016, 1649, 322, 42)
MEMBERSHIP_COUNTS = (4940, 3072, 827, 16238, 15048, 4947, 966, 126)
PARENTS = 18862
MEMBERSHIPS = 46164
MANIFEST_BYTES = 1838
MANIFEST_SHA256 = "6e7eee0ddd5b4c7ef02cdf459c9a0647f720513e7ee4987a3a8b0c17af37eeda"
GROUP_CNF_SHA256 = {
    "B6-l4": "f576b3b590135c41ca1cf1eddf11338d3dddc58a9ca9d13bf92283e2def96e19",
    "B6-l5": "16bde62125cbba48611ca022f6d265b21bfcc73ce0d5e65b90abc99d467b3257",
    "B6-l6": "c45fe0333585d8703c97db388c210d75a0f3eeddcbef34d5e25e3e6cc1eb98d9",
    "B7-l2": "362b5d0a5170360ce6fc4b191f998c3a0c68f7275e7809a2a9473bfdc843acd0",
    "B7-l3": "7ea1fcff31c795e3b6b5d0b331c8f4fd39134ad2fbea763b19fddb914230ecec",
    "B7-l4": "ac9759582a7b894fb726f3933fc5556b2ee10c73824bab361810e3c016f38a30",
    "B7-l5": "fef3ea51cae3c239a787eb27ec19f43d16a4cc24621df83ab9af5c9a6f46b829",
    "B7-l6": "afc62aa046f16a1bfa4c3de50c2847888c6144f1e6f466ff0c20ad7739629777",
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_identities():
    for name, path in IDENTITY_PATHS.items():
        if identity(path) != IDENTITIES[name]:
            raise RuntimeError(f"frozen bound input identity changed: {name}")


def reconstructed_remaining(cover, filter_path):
    if clean_sink.file_identity(clean_sink.SOURCE) != clean_sink.SOURCE_IDENTITY:
        raise RuntimeError("source residual manifest identity changed")
    rows, statuses = read_cover(cover), read_acceptance(filter_path)
    streams = clean_sink.derive(rows, statuses)
    return rows, statuses, streams["remaining"], clean_sink.expected_stream(
        "remaining", streams["remaining"])


def derive_groups(remaining, cover, filter_path):
    supplied = remaining.read_bytes()
    if (len(supplied), hashlib.sha256(supplied).hexdigest()) != IDENTITIES["remaining-stream"]:
        raise RuntimeError("supplied remaining stream differs from frozen identity")
    rows, statuses, semantic_records, expected = reconstructed_remaining(cover, filter_path)
    if supplied != expected:
        raise RuntimeError("remaining stream differs from independent clean-sink reconstruction")
    accepted = [(index, row) for index, (row, status) in enumerate(zip(rows, statuses)) if status == 0]
    groups = {key: [] for key in GROUP_KEYS}
    parent_group, seen_memberships = {}, set()
    membership_counts = {key: 0 for key in GROUP_KEYS}
    for old_group, old_key, member, accepted_index, cover_index, branch, lam, r, t in semantic_records:
        membership = old_group, member
        if membership in seen_memberships:
            raise RuntimeError("duplicate remaining membership")
        seen_memberships.add(membership)
        if not 0 <= accepted_index < len(accepted) or accepted[accepted_index][0] != cover_index:
            raise RuntimeError("remaining parent attribution differs from cover/filter")
        row = accepted[accepted_index][1]
        if row[0] != branch or old_key != f"{branch}-l{lam}-r{r}-t{t}":
            raise RuntimeError("remaining membership fields are inconsistent")
        key = f"{branch}-l{lam}"
        if key not in groups:
            raise RuntimeError(f"unexpected parent group {key}")
        membership_counts[key] += 1
        if accepted_index in parent_group and parent_group[accepted_index] != key:
            raise RuntimeError("no-mixed-parent theorem fact changed")
        if accepted_index not in parent_group:
            parent_group[accepted_index] = key
            groups[key].append((accepted_index, cover_index, row))
    if len(seen_memberships) != MEMBERSHIPS or len(parent_group) != PARENTS:
        raise RuntimeError("remaining membership/parent totals changed")
    if tuple(len(groups[key]) for key in GROUP_KEYS) != GROUP_COUNTS:
        raise RuntimeError("eight parent-group counts changed")
    if tuple(membership_counts[key] for key in GROUP_KEYS) != MEMBERSHIP_COUNTS:
        raise RuntimeError("eight source-membership counts changed")
    for key, members in groups.items():
        projections = [frozenset(expected_projection(row)[1]) for _, _, row in members]
        if len(projections) != len(set(projections)):
            raise RuntimeError(f"duplicate parent projections in {key}")
    return groups


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{ordinal:05d}\t{accepted:05d}\t{cover:06d}"
                 for ordinal, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def dimensions(key, count):
    return BASE_VARIABLES + count, BASE_CLAUSES[key[:2]] + 1 + 153 * count


def manifest_payload(groups):
    verify_identities()
    lines = [MANIFEST_FORMAT]
    for name, (size, digest) in IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.extend((f"groups\t{len(GROUP_KEYS)}", f"parents\t{PARENTS}",
                  f"source-memberships\t{MEMBERSHIPS}", "mixed-parents\t0",
                  "columns\tgroup-ordinal,key,branch,lambda,parents,first-selector,last-selector,variables,clauses,member-sha256"))
    for ordinal, key in enumerate(GROUP_KEYS):
        members = groups[key]
        variables, clauses = dimensions(key, len(members))
        lines.append(f"{ordinal}\t{key}\t{key[:2]}\t{key[4:]}\t{len(members)}\t{BASE_VARIABLES + 1}\t"
                     f"{variables}\t{variables}\t{clauses}\t{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


@lru_cache(maxsize=None)
def frozen_base(branch):
    cnf = generate(18, 6 if branch == "B6" else 7, 6, robust_witness=True, arc_minimal=True)
    return tuple(cnf.names), tuple(cnf.clauses)


def validate_model(variables, clauses, literals, first_selector, count):
    values = {}
    for literal in literals:
        if literal == 0 or not 1 <= abs(literal) <= len(variables) or abs(literal) in values:
            raise RuntimeError("model contains invalid or repeated assignment")
        values[abs(literal)] = literal > 0
    if len(values) != len(variables):
        raise RuntimeError(f"model omits {len(variables) - len(values)} variables")
    for ordinal, clause in enumerate(clauses):
        if not any(values[abs(lit)] == (lit > 0) for lit in clause):
            raise RuntimeError(f"model falsifies clause {ordinal}")
    selected = [number - first_selector for number in range(first_selector, first_selector + count)
                if values[number]]
    if len(selected) != 1:
        raise RuntimeError(f"model must have exactly one true selector, found {len(selected)}")
    return values, selected[0]


def read_model(path):
    literals, terminated = [], False
    for line_number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("c ") or line in ("s SATISFIABLE", "SAT"):
            continue
        fields = line[2:].split() if line.startswith("v ") else line.split()
        try:
            numbers = [int(field) for field in fields]
        except ValueError as error:
            raise RuntimeError(f"noninteger model token line {line_number}") from error
        for number in numbers:
            if terminated:
                raise RuntimeError("model data follows zero terminator")
            if number == 0:
                terminated = True
            else:
                literals.append(number)
    if not terminated:
        raise RuntimeError("model has no zero terminator")
    return literals


def check(cnf_path, remaining=REMAINING, cover=HERE / "m6-placement-cover.txt",
          filter_path=HERE / "m6-placement-filter.txt", model_path=None):
    verify_identities()
    groups = derive_groups(remaining, cover, filter_path)
    manifest = manifest_payload(groups)
    manifest_hash = hashlib.sha256(manifest).hexdigest()
    if MANIFEST_BYTES and (len(manifest), manifest_hash) != (MANIFEST_BYTES, MANIFEST_SHA256):
        raise RuntimeError("independent selector manifest fingerprint changed")
    metadata_items, variables, clauses, declared = parse_cnf(cnf_path)
    metadata = dict(metadata_items)
    ordinal = int(metadata.get("group-ordinal", "-1"))
    if not 0 <= ordinal < len(GROUP_KEYS):
        raise RuntimeError("group ordinal outside exact eight-group manifest")
    key, members = GROUP_KEYS[ordinal], groups[GROUP_KEYS[ordinal]]
    branch = key[:2]
    base_names, base_clauses = map(list, frozen_base(branch))
    if (len(base_names) != BASE_VARIABLES or variable_map_sha256(base_names) != BASE_VARIABLE_MAP_SHA256 or
            len(base_clauses) != BASE_CLAUSES[branch] or clause_sha256(base_clauses) != BASE_CLAUSE_SHA256[branch]):
        raise RuntimeError("independent branch base differs from frozen identity")
    selectors = list(range(BASE_VARIABLES + 1, BASE_VARIABLES + len(members) + 1))
    expected_names = base_names + [f"clean_sink_parent_selector_{i:05d}" for i in range(len(members))]
    expected_metadata = [("format", FORMAT), ("group-manifest-format", MANIFEST_FORMAT),
                         ("group-manifest-bytes", str(len(manifest))),
                         ("group-manifest-sha256", manifest_hash)]
    for name, (size, digest) in IDENTITIES.items():
        expected_metadata.extend(((f"{name}-bytes", str(size)), (f"{name}-sha256", digest)))
    expected_metadata.extend((("group-ordinal", str(ordinal)), ("group-key", key),
                              ("branch", branch), ("lambda", key[4:]),
                              ("parents", str(len(members))),
                              ("source-memberships", str(MEMBERSHIP_COUNTS[ordinal])),
                              ("mixed-parents", "0"),
                              ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
                              ("base-variables", str(BASE_VARIABLES)),
                              ("base-variable-map-sha256", BASE_VARIABLE_MAP_SHA256),
                              ("base-clauses", str(BASE_CLAUSES[branch])),
                              ("base-clause-sha256", BASE_CLAUSE_SHA256[branch]),
                              ("counter-variables", "0"), ("counter-clauses", "0"),
                              ("alo-clauses", "1"), ("guarded-hole-clauses-per-parent", "153"),
                              ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    if metadata_items != expected_metadata:
        raise RuntimeError("metadata is not the canonical bound clean-sink record")
    if variables != expected_names or clauses[:len(base_clauses)] != base_clauses:
        raise RuntimeError("CNF is not immutable branch base plus canonical selectors")
    suffix = iter(clauses[len(base_clauses):])
    if next(suffix, None) != tuple(selectors):
        raise RuntimeError("CNF has no exact selector ALO")
    name_to_number = {name: number for number, name in enumerate(variables, 1)}
    for selector, (_, _, row) in zip(selectors, members):
        holes = expected_projection(row)[1]
        for pair in PAIRS:
            hole = name_to_number[f"h_{pair[0]}_{pair[1]}"]
            if next(suffix, None) != (-selector, hole if pair in holes else -hole):
                raise RuntimeError("CNF lacks canonical 153 guarded holes per parent")
    if next(suffix, None) is not None or declared != dimensions(key, len(members)):
        raise RuntimeError("CNF suffix or DIMACS dimensions differ from exact shape")
    digest = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
    if GROUP_CNF_SHA256 and digest != GROUP_CNF_SHA256[key]:
        raise RuntimeError("group CNF hash differs from frozen eight-hash ledger")
    print(f"PASS group={key} parents={len(members)} vars={declared[0]} clauses={declared[1]} "
          f"bytes={cnf_path.stat().st_size} sha256={digest}")
    if model_path:
        values, selected = validate_model(variables, clauses, read_model(model_path), selectors[0], len(selectors))
        accepted, cover_index, row = members[selected]
        holes = expected_projection(row)[1]
        for pair in PAIRS:
            if values[name_to_number[f"h_{pair[0]}_{pair[1]}"]] != (pair in holes):
                raise RuntimeError("selected parent disagrees with guarded projection")
        print(f"PASS model-attribution selector={selected}:accepted={accepted}:cover={cover_index}")
    return variables, clauses, members, selectors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--remaining", type=Path, default=REMAINING)
    parser.add_argument("--cover", type=Path, default=HERE / "m6-placement-cover.txt")
    parser.add_argument("--filter", type=Path, default=HERE / "m6-placement-filter.txt")
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()
    check(args.cnf, args.remaining, args.cover, args.filter, args.model)


if __name__ == "__main__":
    main()
