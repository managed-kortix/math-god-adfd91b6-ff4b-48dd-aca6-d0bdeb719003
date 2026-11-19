#!/usr/bin/env python3
"""Residualize the certified pair union into 20 disjoint exact-pair cells."""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

import m6_b7_l6_early_c_inaccessible_pair_orbits as source

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-early-c-certificate-residual-exact-pair"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-orbits-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
SCOUT = HERE / "m6-b7-l6-early-c-inaccessible-pair-scout-1s.json"
CERTIFICATES = HERE / "m6-b7-l6-early-c-inaccessible-pair-scout-unsat-certificates.tsv"
SCOUT_IDENTITY = (47594, "1c324d6ce3b73ebdb9abdc8bafcaed1a3373541b208c7ef22002d1556bd3a480")
CERTIFICATE_IDENTITY = (61761, "85a74a1a11f5abc169fc91a9ea61ea9068258a2bb0435d097709ec80c825e42e")
CHILDREN = 20
CELL_PARENT_MEMBERSHIPS = 101
COMPATIBLE_PROFILE_PARENT_GRAPHS = 55
PROFILE_PARENTS = 72


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def certified_ordinals():
    if identity(SCOUT) != SCOUT_IDENTITY or identity(CERTIFICATES) != CERTIFICATE_IDENTITY:
        raise RuntimeError("frozen scout or committed certificate ledger changed")
    scout = json.loads(SCOUT.read_text(encoding="ascii"))
    scout_unsat = tuple(row["child"] for row in scout["rows"] if row["status"] == "UNSAT")
    lines = CERTIFICATES.read_text(encoding="ascii").splitlines()
    columns = lines.index(next(line for line in lines if line.startswith("columns\t")))
    ledger_scope = tuple(int(line.split("\t", 1)[0]) for line in lines[columns + 1:])
    if len(scout["rows"]) != 192 or len(scout_unsat) != 172 or ledger_scope != scout_unsat:
        raise RuntimeError("certificate ledger is not exactly the committed 172-child UNSAT set")
    return frozenset(scout_unsat)


def load_children():
    all_children = source.load_children()
    certified = certified_ordinals()
    children = tuple((ordinal, child) for ordinal, child in enumerate(all_children)
                     if ordinal not in certified)
    memberships = sum(len(child[5]) for _, child in children)
    compatible_graphs = len({(child[1], parent) for _, child in children for parent in child[5]})
    profile_parents = sum(len(next(child[2] for _, child in children if child[1] == profile)[7])
                          for profile in sorted({child[1] for _, child in children}))
    if (len(children), memberships, compatible_graphs, profile_parents) != \
            (CHILDREN, CELL_PARENT_MEMBERSHIPS, COMPATIBLE_PROFILE_PARENT_GRAPHS,
             PROFILE_PARENTS):
        raise RuntimeError("certificate-relative residual count tuple differs")
    return children


def parent_nonoutneighbors(child, parent_ordinal):
    profile = child[2]
    row = profile[7][parent_ordinal][2]
    low = source.low_vertex(profile[3])
    return source.nonoutneighbors(low, profile[3], profile[5], source.parent_holes(row))


def dimensions(record):
    _, child = record
    variables, clauses = source.dimensions(child)
    return variables, clauses + 7 * len(child[5])


def build_child(record):
    _, child = record
    cnf, selectors = source.build_child(child)
    low, pair = source.low_vertex(child[2][3]), child[3]
    for parent_ordinal in child[5]:
        nonout = parent_nonoutneighbors(child, parent_ordinal)
        if not pair < nonout or len(nonout - pair) != 7:
            raise RuntimeError("compatible parent does not have seven residual vertices")
        selector = selectors[parent_ordinal]
        for vertex in sorted(nonout - pair):
            cnf.add(-selector, cnf.names[f"q_{low}_{vertex}"])
    return cnf, selectors


def manifest_payload(children):
    lines = [MANIFEST_FORMAT,
             f"source-scout-bytes\t{SCOUT_IDENTITY[0]}", f"source-scout-sha256\t{SCOUT_IDENTITY[1]}",
             f"certificate-ledger-bytes\t{CERTIFICATE_IDENTITY[0]}",
             f"certificate-ledger-sha256\t{CERTIFICATE_IDENTITY[1]}",
             "committed-certified-children\t172", f"children\t{CHILDREN}",
             f"cell-parent-memberships\t{CELL_PARENT_MEMBERSHIPS}",
             f"distinct-compatible-profile-parent-graphs\t{COMPATIBLE_PROFILE_PARENT_GRAPHS}",
             f"profile-parents-traversed\t{PROFILE_PARENTS}",
             "semantics\teach compatible selector adds seven guarded positive q clauses, leaving exactly its inaccessible pair",
             "cover\toriginal 192-pair profile cover minus the certified 172-orbit union equals this disjoint exact-pair cover",
             "columns\tcell,source-child,key,profile,low-C,pair,compatible-parents,positive-q-clauses,variables,clauses"]
    for cell, (source_ordinal, child) in enumerate(children):
        variables, clauses = dimensions((source_ordinal, child))
        lines.append(f"{cell:03d}\t{source_ordinal:03d}\t{child[0]}\t{child[1]:02d}\t"
                     f"{source.low_vertex(child[2][3])}\t{','.join(map(str, sorted(child[3])))}\t"
                     f"{len(child[5])}\t{7 * len(child[5])}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def write_child(path, cell, record, cnf, selectors, manifest):
    source_ordinal, child = record
    metadata = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
                ("manifest-bytes", str(len(manifest))),
                ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
                ("cell", str(cell)), ("source-child", str(source_ordinal)),
                ("child-key", child[0]), ("profile", str(child[1])),
                ("low-C", str(source.low_vertex(child[2][3]))),
                ("exact-inaccessible-pair", ",".join(map(str, sorted(child[3])))),
                ("compatible-parent-ordinals", ",".join(map(str, child[5]))),
                ("compatible-parents", str(len(child[5]))),
                ("positive-q-clauses", str(7 * len(child[5]))),
                ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))]
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata:
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def hash_payload(children, manifest, hashes):
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"children\t{CHILDREN}",
             "columns\tcell,source-child,key,compatible-parents,variables,clauses,cnf-bytes,cnf-sha256"]
    for cell, record in enumerate(children):
        source_ordinal, child = record
        variables, clauses = dimensions(record)
        size, digest = hashes.get(child[0], ("", ""))
        lines.append(f"{cell:03d}\t{source_ordinal:03d}\t{child[0]}\t{len(child[5])}\t"
                     f"{variables}\t{clauses}\t{size}\t{digest}")
    return ("\n".join(lines) + "\n").encode("ascii")


def populate_hashes(children, manifest):
    result = {}
    with tempfile.TemporaryDirectory(prefix="certificate-residual-hashes-", dir=HERE.parent) as directory:
        path = Path(directory) / "cell.cnf"
        for cell, record in enumerate(children):
            cnf, selectors = build_child(record)
            write_child(path, cell, record, cnf, selectors, manifest)
            result[record[1][0]] = identity(path)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cell", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    children = load_children()
    manifest = manifest_payload(children)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.hash_output:
        hashes = populate_hashes(children, manifest) if args.populate_hashes else {}
        args.hash_output.write_bytes(hash_payload(children, manifest, hashes))
    if args.output:
        if args.cell is None or not 0 <= args.cell < CHILDREN:
            parser.error("--output requires a valid --cell")
        cnf, selectors = build_child(children[args.cell])
        write_child(args.output, args.cell, children[args.cell], cnf, selectors, manifest)
    print(f"PASS cells={CHILDREN} cell_parent_memberships={CELL_PARENT_MEMBERSHIPS} "
          f"compatible_profile_parent_graphs={COMPATIBLE_PROFILE_PARENT_GRAPHS} "
          f"profile_parents_traversed={PROFILE_PARENTS} "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
