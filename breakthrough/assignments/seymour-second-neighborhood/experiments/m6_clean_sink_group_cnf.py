#!/usr/bin/env python3
"""Emit exact parent-selector CNFs for the clean-sink remaining m=6 frontier."""

import argparse
import hashlib
from collections import Counter
from pathlib import Path

import m6_clean_sink_manifest as clean_sink
import m6_parent_cnf as parent

HERE = Path(__file__).resolve().parent
FORMAT = "m6-clean-sink-selector-group-cnf-v1"
MANIFEST_FORMAT = "m6-clean-sink-selector-groups-v1"
REMAINING = HERE / "m6-clean-sink-remaining.tsv"
CLEAN_MANIFEST = HERE / "m6-clean-sink-manifest.tsv"
THEOREM = HERE.parent / "attempts" / "tick52-rooted-clean-sink-theorem.md"
IDENTITY_PATHS = {
    "remaining-stream": REMAINING,
    "clean-sink-manifest": CLEAN_MANIFEST,
    "clean-sink-theorem": THEOREM,
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
PARENTS = sum(GROUP_COUNTS)
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
            raise RuntimeError(f"frozen clean-sink input identity changed: {name}")


def reconstructed_remaining(cover, filter_path):
    clean_sink.verify_inputs()
    streams = clean_sink.partition(clean_sink.residual.load_partition(cover, filter_path))
    return streams["remaining"], clean_sink.stream_payload("remaining", streams["remaining"])


def load_groups(remaining=REMAINING, cover=parent.COVER, filter_path=parent.FILTER):
    verify_identities()
    supplied = remaining.read_bytes()
    if (len(supplied), hashlib.sha256(supplied).hexdigest()) != IDENTITIES["remaining-stream"]:
        raise RuntimeError("supplied remaining stream differs from frozen identity")
    rows = parent.load_cover(cover)
    statuses = parent.load_statuses(filter_path)
    accepted_rows = [(index, row) for index, (row, status) in enumerate(zip(rows, statuses)) if status == 0]
    semantic_records, expected = reconstructed_remaining(cover, filter_path)
    if supplied != expected:
        raise RuntimeError("remaining stream differs from clean-sink semantic reconstruction")
    groups = {key: [] for key in GROUP_KEYS}
    seen = {}
    memberships = Counter()
    for old_group, old_key, member, accepted, cover_index, branch, lam, r, t in semantic_records:
        if accepted >= len(accepted_rows) or accepted_rows[accepted][0] != cover_index:
            raise RuntimeError("remaining stream parent attribution changed")
        row = accepted_rows[accepted][1]
        if row["branch"] != branch or old_key != f"{branch}-l{lam}-r{r}-t{t}":
            raise RuntimeError("remaining stream group fields changed")
        key = f"{branch}-l{lam}"
        if key not in groups:
            raise RuntimeError(f"unexpected clean-sink parent group {key}")
        memberships[accepted] += 1
        previous = seen.setdefault(accepted, key)
        if previous != key:
            raise RuntimeError("verified no-mixed-parent property failed")
        if memberships[accepted] == 1:
            groups[key].append((accepted, cover_index, row))
    if len(seen) != PARENTS or tuple(map(len, groups.values())) != GROUP_COUNTS:
        raise RuntimeError("clean-sink unique-parent partition changed")
    if sum(memberships.values()) != MEMBERSHIPS:
        raise RuntimeError("clean-sink membership total changed")
    for key, members in groups.items():
        projections = [frozenset(parent.embedded_holes(row["branch"], row["word"], row["edges"])[1])
                       for _, _, row in members]
        if len(projections) != len(set(projections)):
            raise RuntimeError(f"duplicate parent projections in {key}")
    return groups


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{ordinal:05d}\t{accepted:05d}\t{cover:06d}"
                 for ordinal, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def dimensions(key, count):
    return parent.BASE_VARIABLES + count, parent.BASE_CLAUSES[key[:2]] + 1 + 153 * count


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
        first = parent.BASE_VARIABLES + 1
        lines.append(f"{ordinal}\t{key}\t{key[:2]}\t{key[4:]}\t{len(members)}\t{first}\t"
                     f"{variables}\t{variables}\t{clauses}\t{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def build_group(key, members):
    branch = key[:2]
    cnf = parent.generate(18, 6 if branch == "B6" else 7, 6,
                          robust_witness=True, arc_minimal=True)
    if (len(cnf.names) != parent.BASE_VARIABLES or
            parent.variable_map_sha256(cnf) != parent.BASE_VARIABLE_MAP_SHA256 or
            len(cnf.clauses) != parent.BASE_CLAUSES[branch] or
            parent.clause_sha256(cnf.clauses) != parent.BASE_CLAUSE_SHA256[branch]):
        raise RuntimeError("generated base CNF differs from frozen branch")
    selectors = [cnf.var(f"clean_sink_parent_selector_{ordinal:05d}")
                 for ordinal in range(len(members))]
    cnf.add(*selectors)
    for selector, (_, _, row) in zip(selectors, members):
        holes = parent.embedded_holes(row["branch"], row["word"], row["edges"])[1]
        for pair in parent.PAIRS:
            hole = cnf.names[f"h_{pair[0]}_{pair[1]}"]
            cnf.add(-selector, hole if pair in holes else -hole)
    return cnf, selectors


def write_group(path, key, members, cnf, selectors, manifest):
    metadata = [("format", FORMAT), ("group-manifest-format", MANIFEST_FORMAT),
                ("group-manifest-bytes", str(len(manifest))),
                ("group-manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, (size, digest) in IDENTITIES.items():
        metadata.extend(((f"{name}-bytes", str(size)), (f"{name}-sha256", digest)))
    metadata.extend((("group-ordinal", str(GROUP_KEYS.index(key))), ("group-key", key),
                      ("branch", key[:2]), ("lambda", key[4:]), ("parents", str(len(members))),
                      ("source-memberships", str(MEMBERSHIP_COUNTS[GROUP_KEYS.index(key)])),
                     ("mixed-parents", "0"),
                     ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
                     ("base-variables", str(parent.BASE_VARIABLES)),
                     ("base-variable-map-sha256", parent.BASE_VARIABLE_MAP_SHA256),
                     ("base-clauses", str(parent.BASE_CLAUSES[key[:2]])),
                     ("base-clause-sha256", parent.BASE_CLAUSE_SHA256[key[:2]]),
                     ("counter-variables", "0"), ("counter-clauses", "0"),
                     ("alo-clauses", "1"), ("guarded-hole-clauses-per-parent", "153"),
                     ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata:
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=GROUP_KEYS)
    parser.add_argument("--remaining", type=Path, default=REMAINING)
    parser.add_argument("--cover", type=Path, default=parent.COVER)
    parser.add_argument("--filter", type=Path, default=parent.FILTER)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    args = parser.parse_args()
    if args.output is None and args.manifest_output is None:
        parser.error("at least one output is required")
    if args.output is not None and args.group is None:
        parser.error("--output requires --group")
    groups = load_groups(args.remaining, args.cover, args.filter)
    manifest = manifest_payload(groups)
    digest = hashlib.sha256(manifest).hexdigest()
    if MANIFEST_BYTES and (len(manifest), digest) != (MANIFEST_BYTES, MANIFEST_SHA256):
        raise RuntimeError("clean-sink selector manifest fingerprint changed")
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.output:
        cnf, selectors = build_group(args.group, groups[args.group])
        write_group(args.output, args.group, groups[args.group], cnf, selectors, manifest)
        file_hash = hashlib.sha256(args.output.read_bytes()).hexdigest()
        if GROUP_CNF_SHA256 and file_hash != GROUP_CNF_SHA256[args.group]:
            raise RuntimeError("clean-sink group CNF fingerprint changed")
        print(f"group={args.group} parents={len(groups[args.group])} vars={len(cnf.names)} "
              f"clauses={len(cnf.clauses)} bytes={args.output.stat().st_size} sha256={file_hash}")
    print(f"groups=8 parents={PARENTS} memberships={MEMBERSHIPS} "
          f"manifest_bytes={len(manifest)} sha256={digest}")


if __name__ == "__main__":
    main()
