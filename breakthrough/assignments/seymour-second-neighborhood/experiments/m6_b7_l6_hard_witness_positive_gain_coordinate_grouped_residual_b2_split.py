#!/usr/bin/env python3
"""Split the 15 grouped TIMEOUT leaves whose B-reduced coordinate ALO has width two."""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

import m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual as grouped

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-hard-witness-positive-gain-coordinate-grouped-residual-b2-split"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
SOURCES = 15
CHILDREN = 30
EXCLUDED_CERTIFIED_LEAF = 129


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def load_sources():
    groups = grouped.load_groups()
    scout = json.loads((HERE / f"{grouped.PREFIX}-grouped-residual-scout-20s.json").read_text(encoding="ascii"))
    sources = []
    for group, row in zip(groups, scout["rows"]):
        item = group[1]
        if item[2] == "b-reduced" and len(item[3]) == 2 and row["status"] == "TIMEOUT":
            sources.append(group)
    if len(sources) != SOURCES or any(group[0] == EXCLUDED_CERTIFIED_LEAF for group in sources):
        raise RuntimeError("exact 15-leaf B-reduced width-two TIMEOUT scope changed")
    return tuple(sources)


def path_details(group):
    cnf, _ = grouped.build_group(group)
    paths = group[1][3]
    if len(paths) != 2:
        raise RuntimeError("split source does not have exactly two reduced paths")
    details = []
    for witness, midpoint, deleted in paths:
        name = f"p_{witness}_{midpoint}_{deleted}"
        details.append((cnf.names[name], name, f"{witness}>{midpoint},{midpoint}>{deleted}"))
    if tuple(detail[0] for detail in details) not in map(tuple, cnf.clauses):
        raise RuntimeError("source lacks its exact binary path ALO")
    return tuple(details)


def children():
    result = []
    for source in load_sources():
        details = path_details(source)
        result.extend(((source, 0, details), (source, 1, details)))
    return tuple(result)


def build_child(child):
    source, branch, details = child
    cnf, selectors = grouped.build_group(source)
    cnf.add(details[0][0] if branch == 0 else -details[0][0])
    return cnf, selectors


def dimensions(child):
    cnf, _ = build_child(child)
    return len(cnf.names), len(cnf.clauses)


def manifest_payload(items):
    old_manifest = HERE / f"{grouped.PREFIX}-grouped-residual.tsv"
    old_hashes = HERE / f"{grouped.PREFIX}-grouped-residual-hashes.tsv"
    old_scout = HERE / f"{grouped.PREFIX}-grouped-residual-scout-20s.json"
    lines = [MANIFEST_FORMAT]
    for name, path in (("source-manifest", old_manifest), ("source-hash-ledger", old_hashes),
                       ("source-scout", old_scout)):
        size, digest = identity(path)
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.extend(("scope\texactly grouped scout-TIMEOUT leaves with B-reduced coordinate ALO width 2",
                  "partition\tfor source ALO x OR y, child 0 adds x and child 1 adds NOT x; source plus NOT x implies y",
                  "selector-preservation\teach child retains its source grouped selector ALO, AMO, names, and guarded projections unchanged",
                  f"excluded-certified-grouped-leaf\t{EXCLUDED_CERTIFIED_LEAF}", f"sources\t{SOURCES}",
                  f"children\t{CHILDREN}",
                  "columns\tchild-ordinal,source-leaf,key,branch,unit,path-x-var,path-x,path-x-arcs,path-y-var,path-y,path-y-arcs,grouped-width,variables,clauses"))
    for ordinal, (source, branch, details) in enumerate(items):
        variables, clauses = dimensions((source, branch, details))
        unit = details[0][0] if branch == 0 else -details[0][0]
        lines.append(f"{ordinal:02d}\t{source[0]:03d}\t{grouped.residual.key(source[1])}\t{branch}\t{unit}\t"
                     f"{details[0][0]}\t{details[0][1]}\t{details[0][2]}\t{details[1][0]}\t{details[1][1]}\t"
                     f"{details[1][2]}\t{len(source[2])}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(ordinal, child, manifest, selectors):
    source, branch, details = child
    unit = details[0][0] if branch == 0 else -details[0][0]
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))), ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("child-ordinal", str(ordinal)), ("source-leaf", str(source[0])),
            ("key", grouped.residual.key(source[1])), ("branch", str(branch)), ("split-unit", str(unit)),
            ("path-x-var", str(details[0][0])), ("path-x", details[0][1]), ("path-x-arcs", details[0][2]),
            ("path-y-var", str(details[1][0])), ("path-y", details[1][1]), ("path-y-arcs", details[1][2]),
            ("grouped-selectors", str(len(selectors))), ("first-selector", str(selectors[0])),
            ("last-selector", str(selectors[-1]))]


def write_child(path, ordinal, child, cnf, selectors, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(ordinal, child, manifest, selectors):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def hash_payload(items, manifest, hashes=None):
    hashes = hashes or {}
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"children\t{CHILDREN}",
             "columns\tchild-ordinal,source-leaf,key,branch,grouped-width,variables,clauses,cnf-bytes,cnf-sha256"]
    for ordinal, child in enumerate(items):
        source, branch, _ = child
        variables, clauses = dimensions(child)
        size, digest = hashes.get(ordinal, ("", ""))
        lines.append(f"{ordinal:02d}\t{source[0]:03d}\t{grouped.residual.key(source[1])}\t{branch}\t"
                     f"{len(source[2])}\t{variables}\t{clauses}\t{size}\t{digest}")
    return ("\n".join(lines) + "\n").encode("ascii")


def populate_hashes(items, manifest):
    result = {}
    with tempfile.TemporaryDirectory(prefix="m6-grouped-b2-split-", dir=HERE.parent) as directory:
        path = Path(directory) / "child.cnf"
        for ordinal, child in enumerate(items):
            cnf, selectors = build_child(child)
            write_child(path, ordinal, child, cnf, selectors, manifest)
            result[ordinal] = identity(path)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--child", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    items = children()
    manifest = manifest_payload(items)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.hash_output:
        hashes = populate_hashes(items, manifest) if args.populate_hashes else None
        args.hash_output.write_bytes(hash_payload(items, manifest, hashes))
    if args.output:
        if args.child is None or not 0 <= args.child < CHILDREN:
            parser.error("--output requires a valid --child")
        cnf, selectors = build_child(items[args.child])
        write_child(args.output, args.child, items[args.child], cnf, selectors, manifest)
    print(f"sources={SOURCES} children={CHILDREN} excluded={EXCLUDED_CERTIFIED_LEAF} "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
