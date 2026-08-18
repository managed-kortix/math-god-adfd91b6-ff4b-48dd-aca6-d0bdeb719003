#!/usr/bin/env python3
"""Emit the exact grouped B7-l6 C-to-B (3,1), t=0/1 campaign."""

import argparse
import hashlib
import tempfile
from pathlib import Path

import m6_clean_sink_group_cnf as clean
import m6_parent_cnf as parent

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-c-to-b-31-orbits"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
B = tuple(range(9, 16))
C = (16, 17)
PROFILES = ((frozenset(B[:3]), frozenset((B[3],))),
            (frozenset(B[:3]), frozenset((B[0],))))
SOURCE_PATHS = {
    "placement-cover": HERE / "m6-placement-cover.txt",
    "placement-filter": HERE / "m6-placement-filter.txt",
    "clean-parent-manifest": HERE / "m6-clean-sink-selector-groups.tsv",
    "clean-remaining-stream": HERE / "m6-clean-sink-remaining.tsv",
}
SOURCE_IDENTITIES = {
    "placement-cover": (6659672, "22d7744f1eecee3ea22527e4beec645ae999c912184f1f23c1a7f701e966ed5e"),
    "placement-filter": (95083, "9bfd2fadda610dde6cef7c13956edba6b0fa763e2ffc31226c0ddf1323fd1d0c"),
    "clean-parent-manifest": (1838, "6e7eee0ddd5b4c7ef02cdf459c9a0647f720513e7ee4987a3a8b0c17af37eeda"),
    "clean-remaining-stream": (2262190, "416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642"),
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        if identity(path) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"bound source changed: {name}")


def compatible(row):
    """Test the profile before choosing labelled C-to-B subsets."""
    labels = parent.CELL_LABELS["B7"]
    _, holes = parent.embedded_holes(row["branch"], row["word"], row["edges"])
    colors = {v: cell for vertices, cell in zip(labels, "RABC") for v in vertices}
    if tuple(sorted(C)) in holes:
        return False
    internal_out = (0, 1)  # fixed internal arc 17 -> 16
    high = (1, 0)
    required = []
    for i, c in enumerate(C):
        fixed = sum(colors[v] in "RA" and tuple(sorted((c, v))) not in holes
                    for v in range(18)) + internal_out[i]
        available = sum(colors[v] == "B" and tuple(sorted((c, v))) not in holes
                        for v in range(18))
        value = 8 + high[i] - fixed
        if not 0 <= value <= available:
            return False
        required.append(value)
    return tuple(required) == (3, 1)


def load_parents():
    verify_sources()
    all_parents = clean.load_groups()["B7-l6"]
    selected = tuple(item for item in all_parents if compatible(item[2]))
    if len(all_parents) != 42 or len(selected) != 10:
        raise RuntimeError("committed B7-l6/profile parent census changed")
    if tuple((x[0], x[1]) for x in selected) != (
        (23728, 112443), (23737, 112460), (24899, 114188), (24952, 114264),
        (24958, 114275), (29966, 121458), (30098, 121657), (30101, 121663),
        (41947, 138180), (42075, 138397),
    ):
        raise RuntimeError("exact ten compatible committed parents changed")
    return all_parents, selected


def member_payload(parents):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index,support,graph6,word"]
    lines.extend(f"{i:02d}\t{a:05d}\t{cover:06d}\t{row['support']:03d}\t{row['code']}\t{row['word']}"
                 for i, (a, cover, row) in enumerate(parents))
    return ("\n".join(lines) + "\n").encode("ascii")


def build_group(t, parents):
    cnf = parent.generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    cnf.add(cnf.names["a_17_16"])
    cnf.add(cnf.names["cnt_d1_16_17_9"])
    cnf.add(-cnf.names["cnt_d1_17_17_9"])
    for c, subset in zip(C, PROFILES[t]):
        for b in B:
            variable = cnf.names[f"a_{c}_{b}"]
            cnf.add(variable if b in subset else -variable)
    selectors = [cnf.var(f"b7_l6_c_to_b_31_t{t}_parent_{i:02d}") for i in range(10)]
    cnf.add(*selectors)
    for selector, (_, _, row) in zip(selectors, parents):
        holes = parent.embedded_holes(row["branch"], row["word"], row["edges"])[1]
        for pair in parent.PAIRS:
            hole = cnf.names[f"h_{pair[0]}_{pair[1]}"]
            cnf.add(-selector, hole if pair in holes else -hole)
    return cnf, selectors


def dimensions():
    return parent.BASE_VARIABLES + 10, parent.BASE_CLAUSES["B7"] + 3 + 14 + 1 + 1530


def manifest_payload(all_parents, parents):
    member = member_payload(parents)
    lines = [MANIFEST_FORMAT]
    for name, value in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{value[0]}", f"{name}-sha256\t{value[1]}"))
    lines.extend(("branch\tB7", "lambda\t6", f"committed-B7-l6-parents\t{len(all_parents)}",
                  "ordered-C-row-sizes\t3,1", "internal-C\t17>16", "high-mask\t10",
                  "compatible-parents\t10", f"compatible-parent-sha256\t{hashlib.sha256(member).hexdigest()}",
                  "exhaustion\tfilter all 42 committed B7-l6 parents by direct rooted-cell degree accounting; exactly these 10 admit required ordered C-to-B counts (3,1)",
                  "orbits\t2", "columns\torbit,t,C16-subset,C17-subset,parents,variables,clauses"))
    variables, clauses = dimensions()
    for t, subsets in enumerate(PROFILES):
        lines.append(f"{t}\t{t}\t{','.join(map(str, sorted(subsets[0])))}\t"
                     f"{','.join(map(str, sorted(subsets[1])))}\t10\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(t, manifest, parents, selectors):
    member = member_payload(parents)
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))), ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, value in SOURCE_IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(value[0])), (f"{name}-sha256", value[1])))
    result.extend((("branch", "B7"), ("lambda", "6"), ("ordered-C-row-sizes", "3,1"),
                   ("intersection-t", str(t)), ("internal-C", "17>16"), ("high-mask", "10"),
                   ("C16-subset", ",".join(map(str, sorted(PROFILES[t][0])))),
                   ("C17-subset", ",".join(map(str, sorted(PROFILES[t][1])))),
                   ("committed-parent-census", "42"), ("compatible-parents", "10"),
                   ("compatible-parent-sha256", hashlib.sha256(member).hexdigest()),
                   ("profile-unit-clauses", "17"), ("alo-clauses", "1"),
                   ("guarded-hole-clauses-per-parent", "153"),
                   ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    return result


def write_group(path, t, cnf, selectors, manifest, parents):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(t, manifest, parents, selectors):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def hashes_payload(manifest, identities):
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "groups\t2",
             "columns\torbit,t,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    variables, clauses = dimensions()
    for t in range(2):
        size, digest = identities.get(t, ("", ""))
        lines.append(f"{t}\t{t}\t10\t{variables}\t{clauses}\t{size}\t{digest}")
    return ("\n".join(lines) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--orbit", type=int, choices=(0, 1))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    all_parents, parents = load_parents()
    manifest = manifest_payload(all_parents, parents)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    identities = {}
    if args.populate_hashes:
        with tempfile.TemporaryDirectory(prefix="m6-31-orbits-", dir=HERE.parent) as directory:
            for t in range(2):
                path = Path(directory) / f"t{t}.cnf"
                cnf, selectors = build_group(t, parents)
                write_group(path, t, cnf, selectors, manifest, parents)
                identities[t] = identity(path)
    if args.hash_output:
        args.hash_output.write_bytes(hashes_payload(manifest, identities))
    if args.output:
        if args.orbit is None:
            parser.error("--output requires --orbit")
        cnf, selectors = build_group(args.orbit, parents)
        write_group(args.output, args.orbit, cnf, selectors, manifest, parents)
    print(f"PASS committed=42 compatible=10 orbits=2 manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
