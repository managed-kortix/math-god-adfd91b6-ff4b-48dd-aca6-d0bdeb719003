#!/usr/bin/env python3
"""Independent exhaustive checker for the frozen rooted clean-sink partition."""

import argparse
import hashlib
import itertools
from collections import Counter
from pathlib import Path

from check_m6_parent_cnf import read_acceptance, read_cover

HERE = Path(__file__).resolve().parent
FORMAT = "m6-clean-sink-partition-v1"
STREAM_FORMAT = "m6-clean-sink-memberships-v1"
SOURCE = HERE / "m6-residual-selector-groups.tsv"
THEOREM = HERE.parent / "attempts" / "tick52-rooted-clean-sink-theorem.md"
SOURCE_IDENTITY = (3915, "b55f0b8e69a77b64254285b9134262cedb961e18a13ad10e4ce350bd04caa85a")
THEOREM_IDENTITY = (4156, "bd0631529bb4658061663460b718ef2ee3186d02fdc599fb2673d3cff3b94ee2")
MANIFEST_IDENTITY = (2104, "733e06c8aa9881e0006409efff23729f1bf88d8af7b1a70e8a78fd3775b53217")
ELIMINATED_IDENTITY = (1705845, "df4cbe415253944712011bf1fb46898925f6a63a087081bef2bbaf2e11f153b6")
REMAINING_IDENTITY = (2262190, "416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642")
KEYS = (
    "B6-l4-r0-t2", "B6-l4-r1-t3", "B6-l5-r0-t1", "B6-l5-r1-t2", "B6-l5-r2-t3",
    "B6-l6-r0-t0", "B6-l6-r1-t1", "B6-l6-r2-t2", "B6-l6-r3-t3",
    "B7-l2-r0-t1", "B7-l2-r1-t2", "B7-l3-r0-t0", "B7-l3-r1-t1", "B7-l3-r2-t2",
    "B7-l4-r1-t0", "B7-l4-r2-t1", "B7-l4-r3-t2", "B7-l5-r2-t0", "B7-l5-r3-t1",
    "B7-l5-r4-t2", "B7-l6-r3-t0", "B7-l6-r4-t1", "B7-l6-r5-t2",
)
EXPECTED_GROUP_COUNTS = (6679, 6679, 1576, 1910, 1910, 167, 310, 340, 340,
                         17689, 17689, 5016, 6981, 6981, 1649, 1943, 1943,
                         322, 358, 358, 42, 46, 46)


def file_identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def full_row(row):
    branch, _, _, _, colors, _, holes = row
    sizes = (1, 8, 6, 3) if branch == "B6" else (1, 8, 7, 2)
    full = list(colors)
    for color, size in zip("RABC", sizes):
        full.extend([color] * (size - full.count(color)))
    return branch, full, set(holes)


def states(row):
    branch, colors, holes = full_row(row)
    cs = [v for v, color in enumerate(colors) if color == "C"]
    pairs = [pair for pair in itertools.combinations(cs, 2) if pair not in holes]
    result = {}
    for orientation in itertools.product((0, 1), repeat=len(pairs)):
        delta = Counter(pair[bit] for pair, bit in zip(pairs, orientation))
        options = []
        for c in cs:
            u_out = sum(colors[v] in "RA" and tuple(sorted((c, v))) not in holes
                        for v in range(18))
            b_slots = sum(colors[v] == "B" and tuple(sorted((c, v))) not in holes
                          for v in range(18))
            options.append([(degree - u_out - delta[c], degree == 9, delta[c])
                            for degree in (8, 9) if 0 <= degree - u_out - delta[c] <= b_slots])
        for realization in itertools.product(*options):
            key = (sum(point[0] for point in realization),
                   sum(point[1] for point in realization))
            result.setdefault(key, []).append(realization)
    return branch, colors, holes, result


def derive(rows, statuses):
    groups = {key: [] for key in KEYS}
    accepted = 0
    for cover_index, (row, status) in enumerate(zip(rows, statuses)):
        if status:
            continue
        branch, colors, holes, pointwise = states(row)
        lam = sum("C" in (colors[a], colors[b]) and "B" not in (colors[a], colors[b])
                  for a, b in holes)
        if (branch, lam) not in (("B6", 3), ("B7", 1)):
            for r, t in sorted(pointwise):
                key = f"{branch}-l{lam}-r{r}-t{t}"
                if key not in groups:
                    raise RuntimeError(f"unexpected residual membership {key}")
                clean_for_all = all(any(x == 0 and high and delta == 0
                                        for x, high, delta in realization)
                                    for realization in pointwise[(r, t)])
                groups[key].append((accepted, cover_index, clean_for_all))
        accepted += 1
    if tuple(len(groups[key]) for key in KEYS) != EXPECTED_GROUP_COUNTS:
        raise RuntimeError("independently reconstructed 23-group membership counts changed")
    streams = {"eliminated": [], "remaining": []}
    for group, key in enumerate(KEYS):
        branch, lam, r, t = key.split("-")
        for member, (accepted, cover, clean) in enumerate(groups[key]):
            name = "eliminated" if clean else "remaining"
            streams[name].append((group, key, member, accepted, cover, branch,
                                  int(lam[1:]), int(r[1:]), int(t[1:])))
    return streams


def expected_stream(name, records):
    lines = [STREAM_FORMAT, f"disposition\t{name}",
             "columns\tstream-ordinal,group-ordinal,key,member-ordinal,accepted-ordinal,cover-index,branch,lambda,r,t"]
    for ordinal, record in enumerate(records):
        group, key, member, accepted, cover, branch, lam, r, t = record
        lines.append(f"{ordinal:05d}\t{group:02d}\t{key}\t{member:05d}\t{accepted:05d}\t"
                     f"{cover:06d}\t{branch}\t{lam}\t{r}\t{t}")
    return ("\n".join(lines) + "\n").encode("ascii")


def counts(streams):
    result = []
    for scope in ("ALL", "B6", "B7") + KEYS:
        selected = {name: [x for x in values
                           if scope == "ALL" or x[5] == scope or x[1] == scope]
                    for name, values in streams.items()}
        ep = {x[3] for x in selected["eliminated"]}
        rp = {x[3] for x in selected["remaining"]}
        result.append((scope, len(selected["eliminated"]), len(selected["remaining"]),
                       len(selected["eliminated"]) + len(selected["remaining"]),
                       len(ep), len(rp), len(ep | rp), len(ep - rp), len(rp - ep), len(ep & rp)))
    return result


def expected_manifest(streams, payloads):
    lines = [FORMAT, f"source-manifest-bytes\t{SOURCE_IDENTITY[0]}",
             f"source-manifest-sha256\t{SOURCE_IDENTITY[1]}",
             f"theorem-report-bytes\t{file_identity(THEOREM)[0]}",
             f"theorem-report-sha256\t{file_identity(THEOREM)[1]}"]
    for name in ("eliminated", "remaining"):
        lines += [f"{name}-stream-bytes\t{len(payloads[name])}",
                  f"{name}-stream-sha256\t{hashlib.sha256(payloads[name]).hexdigest()}"]
    lines.append("count-columns\tscope,eliminated-memberships,remaining-memberships,total-memberships,eliminated-stream-parents,remaining-stream-parents,total-distinct-parents,eliminated-only-parents,remaining-only-parents,mixed-parents")
    lines += ["count\t" + "\t".join(map(str, row)) for row in counts(streams)]
    return ("\n".join(lines) + "\n").encode("ascii")


def check(manifest, eliminated, remaining, cover, filter_path):
    if file_identity(SOURCE) != SOURCE_IDENTITY:
        raise RuntimeError("source residual manifest identity changed")
    if THEOREM_IDENTITY != (0, "") and file_identity(THEOREM) != THEOREM_IDENTITY:
        raise RuntimeError("theorem report identity changed")
    streams = derive(read_cover(cover), read_acceptance(filter_path))
    payloads = {"eliminated": expected_stream("eliminated", streams["eliminated"]),
                "remaining": expected_stream("remaining", streams["remaining"])}
    expected = expected_manifest(streams, payloads)
    supplied = (manifest.read_bytes(), eliminated.read_bytes(), remaining.read_bytes())
    if supplied != (expected, payloads["eliminated"], payloads["remaining"]):
        raise RuntimeError("manifest or membership stream differs from exhaustive reconstruction")
    identities = tuple((len(data), hashlib.sha256(data).hexdigest()) for data in supplied)
    frozen = (MANIFEST_IDENTITY, ELIMINATED_IDENTITY, REMAINING_IDENTITY)
    if MANIFEST_IDENTITY != (0, "") and identities != frozen:
        raise RuntimeError("clean-sink output fingerprint changed")
    print("PASS exhaustive clean-sink partition")
    for path, item in zip((manifest, eliminated, remaining), identities):
        print(f"{path.name}\t{item[0]}\t{item[1]}")
    for row in counts(streams):
        print("count\t" + "\t".join(map(str, row)))
    return streams


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=HERE / "m6-clean-sink-manifest.tsv")
    parser.add_argument("--eliminated", type=Path, default=HERE / "m6-clean-sink-eliminated.tsv")
    parser.add_argument("--remaining", type=Path, default=HERE / "m6-clean-sink-remaining.tsv")
    parser.add_argument("--cover", type=Path, default=HERE / "m6-placement-cover.txt")
    parser.add_argument("--filter", type=Path, default=HERE / "m6-placement-filter.txt")
    args = parser.parse_args()
    check(args.manifest, args.eliminated, args.remaining, args.cover, args.filter)


if __name__ == "__main__":
    main()
