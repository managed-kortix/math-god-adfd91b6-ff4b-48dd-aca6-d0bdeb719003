#!/usr/bin/env python3
"""Build the minimal sound residual cover after frozen coordinate certificates."""

import argparse
import hashlib
import tempfile
from collections import defaultdict
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain_coordinate as frozen
import m6_b7_l6_hard_witness_positive_gain_coordinate as coordinate

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover-v1"
HASH_FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover-hashes-v1"
SOURCE_PATHS = {
    "coordinate-manifest": frozen.MANIFEST_PATH,
    "coordinate-hash-ledger": frozen.HASH_PATH,
    "coordinate-scout": frozen.SCOUT_PATH,
    "coordinate-certificate-ledger": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-certificates.tsv",
}
SOURCE_IDENTITIES = {
    "coordinate-manifest": (13557, "c1ea02ae0127713063efed74eeae84e9c6f22f800b0c6899d293b1a962028b49"),
    "coordinate-hash-ledger": (25213, "aec75e12d82a9ad829dd64b8bce54687f493dbe0d73d5d7665eb965d97f905b6"),
    "coordinate-scout": (92091, "1ad3075ef0386c8bc8afec26b5a2cd392c140d17d8a69daa025063f4e8f3efab"),
    "coordinate-certificate-ledger": (9990, "19d3d8e1a3f5e11545ae6095b1cc74b674512d59b12f2212d19c34fbb9b976f3"),
}
ANCESTOR_CERTIFICATES = 3
COORDINATE_CERTIFICATES = 8
WITNESS_SOURCES = 117
UNRESOLVED_SOURCES = 114
UNRESOLVED_INCIDENCES = 1036
LEAVES = 153
MEMBERSHIPS = 1382
B = tuple(range(9, 16))
C = (16, 17)


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        if identity(path) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"bound frozen coordinate source changed: {name}")


def reduction(child):
    """Classify and exactly reduce one coordinate ALO using fixed arc units."""
    deleted, witness, leaf = child[2], child[3], child[4]
    other = 33 - deleted
    state, subsets = leaf[2][3][1], leaf[2][5]
    if witness == other:
        if state != f"{other}>{deleted}":
            raise RuntimeError("tautological coordinate lacks its fixed true path")
        return "tautological", coordinate.coordinate_paths(child)
    if witness in C:
        raise RuntimeError("unexpected C witness coordinate")
    if state == f"{other}>{deleted}" and witness not in subsets[other - 16]:
        return "structural", ((witness, other, deleted),)
    candidates = tuple(b for b in B if b != witness and b not in subsets[deleted - 16])
    if not 2 <= len(candidates) <= 6:
        raise RuntimeError("reduced B ALO width outside 2..6")
    return "b-reduced", tuple((witness, b, deleted) for b in candidates)


def load_sources():
    verify_sources()
    leaves = coordinate.source.load_leaves()
    if len(leaves) != WITNESS_SOURCES:
        raise RuntimeError("frozen witness source census changed")
    return leaves


def load_cover():
    load_sources()
    children = coordinate.load_leaves()
    scout = frozen.check_scout()
    certified = {row["leaf"] for row in scout["rows"] if row["status"] == "UNSAT"}
    if certified != set(frozen.SCOUT_UNSAT_ORDINALS):
        raise RuntimeError("coordinate certificate scope changed")
    grouped = defaultdict(list)
    for ordinal, child in enumerate(children):
        grouped[child[0]].append((ordinal, child, *reduction(child)))

    unresolved = []
    cover = []
    for source_ordinal in coordinate.timeout_ordinals():
        items = grouped[source_ordinal]
        unresolved.append((source_ordinal, items[0][1][4]))
        uncertified = [item for item in items if item[0] not in certified]
        equivalent = [item for item in uncertified if item[2] in ("tautological", "structural")]
        if equivalent:
            cover.extend(equivalent[:1])
        else:
            cover.extend(uncertified)

    if len(unresolved) != UNRESOLVED_SOURCES or sum(len(leaf[2][6]) for _, leaf in unresolved) != UNRESOLVED_INCIDENCES:
        raise RuntimeError("unresolved source census changed")
    if len(cover) != LEAVES or sum(len(item[1][4][2][6]) for item in cover) != MEMBERSHIPS:
        raise RuntimeError("minimal residual cover census changed")
    return tuple(unresolved), tuple(cover)


def key(item):
    return coordinate.child_key(item[1])


def dimensions(item):
    variables, clauses = coordinate.source.source.dimensions(item[1][4])
    return variables, clauses + 1


def build_leaf(item):
    _, child, _, paths = item
    cnf, selectors = coordinate.source.source.build_leaf(child[4])
    cnf.add(*(cnf.names[f"p_{w}_{midpoint}_{deleted}"] for w, midpoint, deleted in paths))
    return cnf, selectors


def manifest_payload(unresolved, cover):
    lines = [MANIFEST_FORMAT]
    for name, item in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend((f"witness-sources\t{WITNESS_SOURCES}", f"ancestor-certificates\t{ANCESTOR_CERTIFICATES}",
                  f"coordinate-certificates\t{COORDINATE_CERTIFICATES}",
                  f"unresolved-sources\t{UNRESOLVED_SOURCES}",
                  f"unresolved-source-incidences\t{UNRESOLVED_INCIDENCES}", f"cover-leaves\t{LEAVES}",
                  f"cover-memberships\t{MEMBERSHIPS}",
                  "selection\tretain one coordinate representative when unit/structural implication proves it source-equivalent; otherwise retain every coordinate child except a child closed by its own LRAT",
                  "certificate-semantics\tcoordinate LRAT closes only its child; every uncertified sibling remains in the residual source disjunction",
                  "normalization\tonly exact fixed-unit coordinate-ALO reduction; B-only ALOs may be reduced",
                  "columns\tcover-ordinal,key,coordinate-ordinal,source-leaf-ordinal,source-key,disposition,deleted,witness,alo-midpoints,alo-width,parents,variables,clauses"))
    for cover_ordinal, item in enumerate(cover):
        coordinate_ordinal, child, disposition, paths = item
        variables, clauses = dimensions(item)
        lines.append(f"{cover_ordinal:03d}\t{key(item)}\t{coordinate_ordinal:03d}\t{child[0]:03d}\t{child[4][0]}\t"
                     f"{disposition}\t{child[2]}\t{child[3]}\t{','.join(str(path[1]) for path in paths)}\t"
                     f"{len(paths)}\t{len(child[4][2][6])}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def hash_payload(cover, manifest, hashes=None):
    hashes = hashes or {}
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"leaves\t{LEAVES}",
             "columns\tcover-ordinal,key,coordinate-ordinal,disposition,alo-width,parents,variables,clauses,cnf-sha256"]
    for ordinal, item in enumerate(cover):
        variables, clauses = dimensions(item)
        lines.append(f"{ordinal:03d}\t{key(item)}\t{item[0]:03d}\t{item[2]}\t{len(item[3])}\t"
                     f"{len(item[1][4][2][6])}\t{variables}\t{clauses}\t{hashes.get(key(item), '')}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(ordinal, item, manifest, selectors):
    coordinate_ordinal, child, disposition, paths = item
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))),
              ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, value in SOURCE_IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(value[0])), (f"{name}-sha256", value[1])))
    result.extend((("cover-ordinal", str(ordinal)), ("key", key(item)),
                   ("coordinate-ordinal", str(coordinate_ordinal)), ("source-leaf-ordinal", str(child[0])),
                   ("source-key", child[4][0]), ("disposition", disposition),
                   ("deleted", str(child[2])), ("witness", str(child[3])),
                   ("alo-midpoints", ",".join(str(path[1]) for path in paths)),
                   ("alo-width", str(len(paths))), ("equivalence", "exact-fixed-unit-or-structural"),
                   ("parents", str(len(child[4][2][6]))), ("first-selector", str(selectors[0])),
                   ("last-selector", str(selectors[-1]))))
    return result


def write_leaf(path, ordinal, item, cnf, selectors, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(ordinal, item, manifest, selectors):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def populate_hashes(cover, manifest):
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="m6-coordinate-residual-cover-", dir=HERE.parent) as directory:
        path = Path(directory) / "leaf.cnf"
        for ordinal, item in enumerate(cover):
            cnf, selectors = build_leaf(item)
            write_leaf(path, ordinal, item, cnf, selectors, manifest)
            hashes[key(item)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaf", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    unresolved, cover = load_cover()
    manifest = manifest_payload(unresolved, cover)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.hash_output:
        hashes = populate_hashes(cover, manifest) if args.populate_hashes else None
        args.hash_output.write_bytes(hash_payload(cover, manifest, hashes))
    if args.output:
        if args.leaf is None or not 0 <= args.leaf < LEAVES:
            parser.error("--output requires a valid --leaf")
        cnf, selectors = build_leaf(cover[args.leaf])
        write_leaf(args.output, args.leaf, cover[args.leaf], cnf, selectors, manifest)
    print(f"witness_sources={WITNESS_SOURCES} unresolved={UNRESOLVED_SOURCES}/{UNRESOLVED_INCIDENCES} "
          f"cover={LEAVES}/{MEMBERSHIPS} manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
