#!/usr/bin/env python3
"""Freeze residual memberships eliminated by the rooted clean-sink theorem."""

import argparse
import hashlib
import itertools
from collections import Counter
from pathlib import Path

import m6_parent_cnf as parent
import m6_residual_group_cnf as residual

HERE = Path(__file__).resolve().parent
FORMAT = "m6-clean-sink-partition-v1"
STREAM_FORMAT = "m6-clean-sink-memberships-v1"
SOURCE_MANIFEST = HERE / "m6-residual-selector-groups.tsv"
THEOREM = HERE.parent / "attempts" / "tick52-rooted-clean-sink-theorem.md"
SOURCE_IDENTITY = (3915, "b55f0b8e69a77b64254285b9134262cedb961e18a13ad10e4ce350bd04caa85a")
THEOREM_IDENTITY = (4156, "bd0631529bb4658061663460b718ef2ee3186d02fdc599fb2673d3cff3b94ee2")
MANIFEST_IDENTITY = (2104, "733e06c8aa9881e0006409efff23729f1bf88d8af7b1a70e8a78fd3775b53217")
ELIMINATED_IDENTITY = (1705845, "df4cbe415253944712011bf1fb46898925f6a63a087081bef2bbaf2e11f153b6")
REMAINING_IDENTITY = (2262190, "416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642")


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_inputs():
    if identity(SOURCE_MANIFEST) != SOURCE_IDENTITY:
        raise RuntimeError("frozen 23-group source manifest changed")
    if THEOREM_IDENTITY != (0, "") and identity(THEOREM) != THEOREM_IDENTITY:
        raise RuntimeError("rooted clean-sink theorem report changed")


def realizations(row, target_r, target_t):
    branch = row["branch"]
    labels = parent.CELL_LABELS[branch]
    _, holes = parent.embedded_holes(branch, row["word"], row["edges"])
    colors = {vertex: cell for cell_labels, cell in zip(labels, "RABC")
              for vertex in cell_labels}
    cs = labels[3]
    cc = [pair for pair in itertools.combinations(cs, 2) if pair not in holes]
    result = []
    for directions in itertools.product((0, 1), repeat=len(cc)):
        internal = Counter(pair[direction] for pair, direction in zip(cc, directions))
        choices = []
        for c in cs:
            forced_u = sum(colors[v] in "RA" and tuple(sorted((c, v))) not in holes
                           for v in range(18))
            available_b = sum(colors[v] == "B" and tuple(sorted((c, v))) not in holes
                              for v in range(18))
            choices.append([(target - forced_u - internal[c], int(target == 9), internal[c])
                            for target in (8, 9)
                            if 0 <= target - forced_u - internal[c] <= available_b])
        for state in itertools.product(*choices):
            if sum(item[0] for item in state) == target_r and sum(item[1] for item in state) == target_t:
                result.append(state)
    return result


def eliminated(row, r, t):
    states = realizations(row, r, t)
    if not states:
        raise RuntimeError("residual membership has no pointwise realization")
    return universally_clean(states)


def universally_clean(states):
    """Expose the universal quantifier for direct mixed-state regression tests."""
    if not states:
        raise ValueError("clean-sink state family must be nonempty")
    return all(any(x == 0 and high == 1 and internal == 0
                   for x, high, internal in state) for state in states)


def partition(groups):
    streams = {"eliminated": [], "remaining": []}
    for group_ordinal, key in enumerate(residual.GROUP_KEYS):
        branch, lam, r, t = residual.key_parameters(key)
        for member, (accepted, row) in enumerate(groups[key]):
            disposition = "eliminated" if eliminated(row, r, t) else "remaining"
            streams[disposition].append((group_ordinal, key, member, accepted,
                                         row["cover_index"], branch, lam, r, t))
    if sum(map(len, streams.values())) != residual.RESIDUAL_MEMBERSHIPS:
        raise RuntimeError("clean-sink partition does not cover all residual memberships")
    return streams


def stream_payload(disposition, records):
    lines = [STREAM_FORMAT, f"disposition\t{disposition}",
             "columns\tstream-ordinal,group-ordinal,key,member-ordinal,accepted-ordinal,cover-index,branch,lambda,r,t"]
    lines.extend(f"{ordinal:05d}\t{group:02d}\t{key}\t{member:05d}\t{accepted:05d}\t"
                 f"{cover:06d}\t{branch}\t{lam}\t{r}\t{t}"
                 for ordinal, (group, key, member, accepted, cover, branch, lam, r, t)
                 in enumerate(records))
    return ("\n".join(lines) + "\n").encode("ascii")


def count_rows(streams):
    rows = []
    for scope in ("ALL", "B6", "B7") + residual.GROUP_KEYS:
        selected = {name: [record for record in records
                           if scope == "ALL" or record[5] == scope or record[1] == scope]
                    for name, records in streams.items()}
        eliminated_parents = {record[3] for record in selected["eliminated"]}
        remaining_parents = {record[3] for record in selected["remaining"]}
        all_parents = eliminated_parents | remaining_parents
        rows.append((scope, len(selected["eliminated"]), len(selected["remaining"]),
                     sum(map(len, selected.values())), len(eliminated_parents),
                     len(remaining_parents), len(all_parents),
                     len(eliminated_parents - remaining_parents),
                     len(remaining_parents - eliminated_parents),
                     len(eliminated_parents & remaining_parents)))
    return rows


def manifest_payload(streams, payloads):
    verify_inputs()
    lines = [FORMAT,
             f"source-manifest-bytes\t{SOURCE_IDENTITY[0]}",
             f"source-manifest-sha256\t{SOURCE_IDENTITY[1]}",
             f"theorem-report-bytes\t{identity(THEOREM)[0]}",
             f"theorem-report-sha256\t{identity(THEOREM)[1]}"]
    for name in ("eliminated", "remaining"):
        lines.extend((f"{name}-stream-bytes\t{len(payloads[name])}",
                      f"{name}-stream-sha256\t{hashlib.sha256(payloads[name]).hexdigest()}"))
    lines.append("count-columns\tscope,eliminated-memberships,remaining-memberships,total-memberships,eliminated-stream-parents,remaining-stream-parents,total-distinct-parents,eliminated-only-parents,remaining-only-parents,mixed-parents")
    lines.extend("count\t" + "\t".join(map(str, row)) for row in count_rows(streams))
    return ("\n".join(lines) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-output", type=Path, default=HERE / "m6-clean-sink-manifest.tsv")
    parser.add_argument("--eliminated-output", type=Path, default=HERE / "m6-clean-sink-eliminated.tsv")
    parser.add_argument("--remaining-output", type=Path, default=HERE / "m6-clean-sink-remaining.tsv")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    groups = residual.load_partition()
    streams = partition(groups)
    payloads = {name: stream_payload(name, records) for name, records in streams.items()}
    manifest = manifest_payload(streams, payloads)
    expected = ((len(manifest), hashlib.sha256(manifest).hexdigest()),
                (len(payloads["eliminated"]), hashlib.sha256(payloads["eliminated"]).hexdigest()),
                (len(payloads["remaining"]), hashlib.sha256(payloads["remaining"]).hexdigest()))
    frozen = (MANIFEST_IDENTITY, ELIMINATED_IDENTITY, REMAINING_IDENTITY)
    if MANIFEST_IDENTITY != (0, "") and expected != frozen:
        raise RuntimeError("clean-sink frozen output fingerprints changed")
    paths = (args.manifest_output, args.eliminated_output, args.remaining_output)
    data = (manifest, payloads["eliminated"], payloads["remaining"])
    if args.check:
        if any(path.read_bytes() != content for path, content in zip(paths, data)):
            raise RuntimeError("clean-sink frozen output content changed")
    else:
        for path, content in zip(paths, data):
            path.write_bytes(content)
    totals = count_rows(streams)[0]
    print(f"PASS eliminated={totals[1]} remaining={totals[2]}")
    for path, (size, digest) in zip(paths, expected):
        print(f"{path.name}\t{size}\t{digest}")


if __name__ == "__main__":
    main()
