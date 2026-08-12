#!/usr/bin/env python3
"""Emit the exact grouped residual after checked singleton exclusions."""

import argparse
import hashlib
import re
import tempfile
from itertools import combinations
from pathlib import Path

import m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover as residual
from m6_parent_cnf import PAIRS, embedded_holes

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-hard-witness-positive-gain-coordinate"
FORMAT = f"{PREFIX}-grouped-residual-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-grouped-residual-v1"
HASH_FORMAT = f"{PREFIX}-grouped-residual-hashes-v1"
LEAVES = 153
SELECTORS = 1255
WIDTHS = {1: 1, 2: 3, 3: 2, 4: 38, 10: 109}
CERTIFICATE_LEDGER = HERE / f"{PREFIX}-residual-singleton-parent-certificates.tsv"
CERTIFICATE_VERIFIER = HERE / f"verify_{PREFIX.replace('-', '_')}_residual_singleton_parent_certificates.py"
BOUND_IDENTITIES = {
    "singleton-certificate-ledger": (72132, "bdad79d28b22d2b48ed0aef779765a6aafed752227c1952da36a8e180b48ca3d"),
    "singleton-certificate-verifier": (16978, "ca3205e94f01b3b6e551373bad75333130a5d82bf3bc7cdf2e00f92be55e2d08"),
}
BOUND_PATHS = {
    "singleton-certificate-ledger": CERTIFICATE_LEDGER,
    "singleton-certificate-verifier": CERTIFICATE_VERIFIER,
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def checked_singleton_scope():
    for name, path in BOUND_PATHS.items():
        actual = identity(path)
        if actual != BOUND_IDENTITIES[name]:
            raise RuntimeError(f"current committed bound identity changed: {name}: {actual}")
    lines = CERTIFICATE_LEDGER.read_text(encoding="ascii").splitlines()
    marker = next((i for i, line in enumerate(lines) if line.startswith("columns\t")), -1)
    if marker < 0:
        raise RuntimeError("singleton certificate ledger has no columns")
    columns = lines[marker].split("\t", 1)[1].split(",")
    if "membership-ordinal" not in columns or "artifact" not in columns:
        raise RuntimeError("singleton certificate ledger scope columns changed")
    rows = [dict(zip(columns, line.split("\t"))) for line in lines[marker + 1:]]
    ordinals = tuple(int(row["membership-ordinal"]) for row in rows)
    if len(rows) != 127 or ordinals != tuple(sorted(set(ordinals))):
        raise RuntimeError("checked singleton certificate scope is not 127 unique ordered rows")
    if any(re.fullmatch(r"[0-9a-f]{64}", row.get("xz-sha256", "")) is None for row in rows):
        raise RuntimeError("singleton certificate artifact identities are malformed")
    return frozenset(ordinals)


def parent_projection(parent):
    row = parent[2]
    return embedded_holes(row["branch"], row["word"], row["edges"])[1]


def load_groups():
    certified = checked_singleton_scope()
    _, cover = residual.load_cover()
    groups = []
    membership = 0
    for leaf_ordinal, item in enumerate(cover):
        survivors = []
        for parent_ordinal, parent in enumerate(item[1][4][2][6]):
            if membership not in certified:
                survivors.append((membership, parent_ordinal, parent))
            membership += 1
        if not survivors:
            raise RuntimeError("singleton certificates closed an entire residual leaf")
        groups.append((leaf_ordinal, item, tuple(survivors)))
    widths = {width: sum(len(group[2]) == width for group in groups) for width in WIDTHS}
    if membership != 1382 or len(groups) != LEAVES or sum(len(group[2]) for group in groups) != SELECTORS:
        raise RuntimeError("grouped residual census changed")
    if widths != WIDTHS or any(len(group[2]) not in WIDTHS for group in groups):
        raise RuntimeError(f"grouped residual width distribution changed: {widths}")
    return tuple(groups)


def strip_old_selector_layer(cnf, selectors, parents):
    matches = [i for i, clause in enumerate(cnf.clauses) if tuple(clause) == tuple(selectors)]
    if len(matches) != 1:
        raise RuntimeError("old selector ALO is not unique")
    start = matches[0]
    stop = start + 1 + 153 * len(selectors)
    expected = []
    for selector, parent in zip(selectors, parents):
        holes = parent_projection(parent)
        expected.extend((-selector, cnf.names[f"h_{a}_{b}"] if (a, b) in holes else
                         -cnf.names[f"h_{a}_{b}"]) for a, b in PAIRS)
    if cnf.clauses[start + 1:stop] != expected:
        raise RuntimeError("old guarded selector projection count, order, or literals changed")
    del cnf.clauses[start:stop]
    selector_names = {name for name, number in cnf.names.items() if number in selectors}
    if len(selector_names) != len(selectors) or sorted(selectors) != list(range(len(cnf.names) - len(selectors) + 1,
                                                                               len(cnf.names) + 1)):
        raise RuntimeError("old selector variables are not the exact terminal layer")
    for name in selector_names:
        del cnf.names[name]


def build_group(group):
    leaf_ordinal, item, survivors = group
    cnf, old_selectors = residual.build_leaf(item)
    strip_old_selector_layer(cnf, old_selectors, item[1][4][2][6])
    selectors = [cnf.var(f"grouped_residual_leaf_{leaf_ordinal:03d}_selector_{i:02d}")
                 for i in range(len(survivors))]
    cnf.add(*selectors)
    for left, right in combinations(selectors, 2):
        cnf.add(-left, -right)
    for selector, (_, _, parent) in zip(selectors, survivors):
        holes = parent_projection(parent)
        for a, b in PAIRS:
            hole = cnf.names[f"h_{a}_{b}"]
            cnf.add(-selector, hole if (a, b) in holes else -hole)
    return cnf, tuple(selectors)


def dimensions(group):
    cnf, _ = build_group(group)
    return len(cnf.names), len(cnf.clauses)


def manifest_payload(groups):
    lines = [MANIFEST_FORMAT]
    for name, value in BOUND_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{value[0]}", f"{name}-sha256\t{value[1]}"))
    lines.extend(("singleton-certificate-scope\texactly the 127 ordered LRAT rows accepted by the bound verifier",
                  "disjunction-equivalence\tper frozen residual leaf, checked singleton UNSAT members are false; the surviving exact-parent disjunction is equivalent",
                  "selector-rebuild\tremove the complete old selector ALO/guard layer; add surviving ALO, pairwise AMO, and 153 guarded projection clauses per survivor",
                  f"leaves\t{LEAVES}", f"selectors\t{SELECTORS}",
                  "width-distribution\t1x1,3x2,2x3,38x4,109x10",
                  "columns\tleaf-ordinal,key,width,certified-memberships,surviving-memberships,variables,clauses"))
    for leaf_ordinal, item, survivors in groups:
        all_members = len(item[1][4][2][6])
        variables, clauses = dimensions((leaf_ordinal, item, survivors))
        survivor_ids = ",".join(f"{entry[0]:04d}" for entry in survivors)
        survivor_set = {entry[0] for entry in survivors}
        first = sum(len(group[1][1][4][2][6]) for group in groups[:leaf_ordinal])
        certified = ",".join(f"{i:04d}" for i in range(first, first + all_members) if i not in survivor_set)
        lines.append(f"{leaf_ordinal:03d}\t{residual.key(item)}\t{len(survivors)}\t{certified}\t"
                     f"{survivor_ids}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(group, manifest, selectors):
    leaf_ordinal, item, survivors = group
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))),
              ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, value in BOUND_IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(value[0])), (f"{name}-sha256", value[1])))
    result.extend((("leaf-ordinal", str(leaf_ordinal)), ("key", residual.key(item)),
                   ("surviving-selectors", str(len(selectors))),
                   ("surviving-memberships", ",".join(f"{entry[0]:04d}" for entry in survivors)),
                   ("selector-alo-clauses", "1"),
                   ("selector-amo-clauses", str(len(selectors) * (len(selectors) - 1) // 2)),
                   ("projection-clauses-per-selector", "153"),
                   ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    return result


def write_group(path, group, cnf, selectors, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(group, manifest, selectors):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def hash_payload(groups, manifest, hashes=None):
    hashes = hashes or {}
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"leaves\t{LEAVES}",
             "columns\tleaf-ordinal,key,width,variables,clauses,cnf-bytes,cnf-sha256"]
    for group in groups:
        variables, clauses = dimensions(group)
        size, digest = hashes.get(group[0], ("", ""))
        lines.append(f"{group[0]:03d}\t{residual.key(group[1])}\t{len(group[2])}\t{variables}\t{clauses}\t{size}\t{digest}")
    return ("\n".join(lines) + "\n").encode("ascii")


def populate_hashes(groups, manifest):
    result = {}
    with tempfile.TemporaryDirectory(prefix="m6-grouped-residual-hashes-", dir=HERE.parent) as directory:
        path = Path(directory) / "leaf.cnf"
        for group in groups:
            cnf, selectors = build_group(group)
            write_group(path, group, cnf, selectors, manifest)
            result[group[0]] = identity(path)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaf", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    groups = load_groups()
    manifest = manifest_payload(groups)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.hash_output:
        hashes = populate_hashes(groups, manifest) if args.populate_hashes else None
        args.hash_output.write_bytes(hash_payload(groups, manifest, hashes))
    if args.output:
        if args.leaf is None or not 0 <= args.leaf < LEAVES:
            parser.error("--output requires a valid --leaf")
        group = groups[args.leaf]
        cnf, selectors = build_group(group)
        write_group(args.output, group, cnf, selectors, manifest)
    print(f"leaves={LEAVES} selectors={SELECTORS} widths=1x1,3x2,2x3,38x4,109x10 "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
