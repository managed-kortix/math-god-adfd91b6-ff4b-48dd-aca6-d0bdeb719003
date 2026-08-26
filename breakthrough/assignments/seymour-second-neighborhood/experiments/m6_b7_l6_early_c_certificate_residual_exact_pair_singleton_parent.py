#!/usr/bin/env python3
"""Emit one exact-parent CNF for each committed exact-pair membership."""

import argparse
import hashlib
import tempfile
from pathlib import Path

import m6_b7_l6_early_c_certificate_residual_exact_pairs as grouped
from m6_parent_cnf import embedded_holes

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-early-c-certificate-residual-exact-pair-singleton-parent"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
CELLS = 20
MEMBERSHIPS = 101
ANCESTRY_PATHS = {
    "grouped-producer": HERE / "m6_b7_l6_early_c_certificate_residual_exact_pairs.py",
    "grouped-checker": HERE / "check_m6_b7_l6_early_c_certificate_residual_exact_pairs.py",
    "grouped-manifest": HERE / "m6-b7-l6-early-c-certificate-residual-exact-pair-orbits.tsv",
    "grouped-hashes": HERE / "m6-b7-l6-early-c-certificate-residual-exact-pair-hashes.tsv",
}
ANCESTRY_IDENTITIES = {
    "grouped-producer": (8899, "61ffaf4d38fad6e70034ce65491e1ecba035ae41dba318d5f44a876097fa1ca6"),
    "grouped-checker": (16343, "42dc724e9e8ad825dfa84d897417945cbd255c8e3e9368b2a5abc92c3d0307ab"),
    "grouped-manifest": (1666, "ca7dd34a8382f5c5ff7d250c38daa1914f8cec6bde9efeb4945d9c8a1ef1b5d4"),
    "grouped-hashes": (2361, "0c719c2798c78c00c03c013396fa2d359d16abeacb9e9adc397527bead453455"),
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_ancestry():
    for name, path in ANCESTRY_PATHS.items():
        if identity(path) != ANCESTRY_IDENTITIES[name]:
            raise RuntimeError(f"committed grouped ancestry changed: {name}")


def load_memberships():
    verify_ancestry()
    cells = grouped.load_children()
    memberships = tuple((cell, record, parent) for cell, record in enumerate(cells)
                        for parent in record[1][5])
    if len(cells) != CELLS or len(memberships) != MEMBERSHIPS:
        raise RuntimeError("singleton exact-pair membership census changed")
    return cells, memberships


def membership_key(member):
    cell, (_, child), parent = member
    return f"c{cell:03d}-{child[0]}-p{parent:02d}"


def parent_projection(member):
    _, (_, child), parent = member
    row = child[2][7][parent][2]
    if isinstance(row, dict):
        branch, word, edges = row["branch"], row["word"], row["edges"]
    else:
        branch, word, edges = row[0], row[4], row[6]
    return frozenset(embedded_holes(branch, word, edges)[1])


def projection_fingerprint(member):
    payload = ",".join(f"{a}-{b}" for a, b in sorted(parent_projection(member))) + "\n"
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def dimensions(member):
    variables, clauses = grouped.dimensions(member[1])
    return variables, clauses + 1


def build_membership(member):
    _, record, parent = member
    cnf, selectors = grouped.build_child(record)
    cnf.add(selectors[parent])
    return cnf, selectors


def manifest_payload(cells, memberships):
    lines = [MANIFEST_FORMAT]
    for name, (size, digest) in ANCESTRY_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.extend((f"grouped-cells\t{CELLS}", f"memberships\t{MEMBERSHIPS}",
                  "split\tone CNF per cell-parent membership with one positive selector unit",
                  "pair-pattern\tselected parent has two negative q units and seven positive q consequences",
                  "selector-disjoint\tdistinct selected parent projections are incompatible",
                  "selector-exhaustive\teach grouped selector ALO is partitioned over all compatible parents",
                  "proof-status\tscout-only; no LRAT generated",
                  "columns\tmembership,cell,source-child,key,profile,pair,parent,parent-projection-fingerprint,selector,variables,clauses"))
    for ordinal, member in enumerate(memberships):
        cell, (source_child, child), parent = member
        variables, clauses = dimensions(member)
        selector = variables - len(child[2][7]) + parent + 1
        lines.append(f"{ordinal:03d}\t{cell:03d}\t{source_child:03d}\t{membership_key(member)}\t"
                     f"{child[1]:02d}\t{','.join(map(str, sorted(child[3])))}\t{parent:02d}\t"
                     f"{projection_fingerprint(member)}\t{selector}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(ordinal, member, manifest, selectors):
    cell, (source_child, child), parent = member
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))),
              ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, (size, digest) in ANCESTRY_IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(size)), (f"{name}-sha256", digest)))
    result.extend((("membership", str(ordinal)), ("key", membership_key(member)),
                   ("cell", str(cell)), ("source-child", str(source_child)),
                   ("child-key", child[0]), ("profile", str(child[1])),
                   ("low-C", str(grouped.source.low_vertex(child[2][3]))),
                   ("exact-inaccessible-pair", ",".join(map(str, sorted(child[3])))),
                   ("parent-ordinal", str(parent)),
                   ("parent-projection-fingerprint", projection_fingerprint(member)),
                   ("selected-selector", str(selectors[parent])),
                   ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1])),
                   ("selector-unit-clauses", "1"), ("lrat-status", "not-generated")))
    return result


def write_membership(path, ordinal, member, cnf, selectors, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(ordinal, member, manifest, selectors):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def hash_payload(memberships, manifest, hashes=None):
    hashes = hashes or {}
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
             f"memberships\t{MEMBERSHIPS}",
             "columns\tmembership,key,cell,parent,variables,clauses,cnf-bytes,cnf-sha256"]
    for ordinal, member in enumerate(memberships):
        size, digest = hashes.get(membership_key(member), ("", ""))
        variables, clauses = dimensions(member)
        lines.append(f"{ordinal:03d}\t{membership_key(member)}\t{member[0]:03d}\t{member[2]:02d}\t"
                     f"{variables}\t{clauses}\t{size}\t{digest}")
    return ("\n".join(lines) + "\n").encode("ascii")


def populate_hashes(memberships, manifest):
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="exact-pair-singleton-hashes-", dir=HERE.parent) as directory:
        path = Path(directory) / "membership.cnf"
        for ordinal, member in enumerate(memberships):
            cnf, selectors = build_membership(member)
            write_membership(path, ordinal, member, cnf, selectors, manifest)
            hashes[membership_key(member)] = identity(path)
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--membership", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    cells, memberships = load_memberships()
    manifest = manifest_payload(cells, memberships)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.hash_output:
        hashes = populate_hashes(memberships, manifest) if args.populate_hashes else None
        args.hash_output.write_bytes(hash_payload(memberships, manifest, hashes))
    if args.output:
        if args.membership is None or not 0 <= args.membership < MEMBERSHIPS:
            parser.error("--output requires a valid --membership")
        member = memberships[args.membership]
        cnf, selectors = build_membership(member)
        write_membership(args.output, args.membership, member, cnf, selectors, manifest)
    print(f"PASS grouped_cells={len(cells)} memberships={len(memberships)} "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
