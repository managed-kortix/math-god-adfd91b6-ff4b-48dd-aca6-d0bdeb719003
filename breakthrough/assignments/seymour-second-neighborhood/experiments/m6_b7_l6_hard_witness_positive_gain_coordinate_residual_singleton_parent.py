#!/usr/bin/env python3
"""Emit one exact-parent CNF for every residual-cover membership."""

import argparse
import hashlib
import tempfile
from pathlib import Path

import m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover as residual
from m6_parent_cnf import embedded_holes

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent-v1"
HASH_FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent-hashes-v1"
LEAVES = 153
MEMBERSHIPS = 1382
IDENTITY_PATHS = {
    "residual-manifest": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover.tsv",
    "residual-hash-ledger": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover-hashes.tsv",
    "residual-producer": HERE / "m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover.py",
    "residual-checker": HERE / "check_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover.py",
    "coordinate-certificates": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-certificates.tsv",
    "positive-gain-certificates": HERE / "m6-b7-l6-hard-witness-positive-gain-certificates.tsv",
    "no-gain-certificates": HERE / "m6-b7-l6-hard-witness-no-gain-certificates.tsv",
    "witness-orbit-certificates": HERE / "m6-b7-l6-hard-orbit-certificates.tsv",
    "state-certificates": HERE / "m6-b7-l6-state-certificates.tsv",
}
IDENTITIES = {
    "residual-manifest": (13269, "ed2f787c0a10ecb5663479db61446ce36bfb5d75cc39bb3f48e2bb8cddf79706"),
    "residual-hash-ledger": (17655, "785268882c06117261f99ab6efabd4e4d61ce9565dc5c87a08273ed47607c96a"),
    "residual-producer": (10609, "b4359639f46a2eff5a99a41b43f268d02af17749a88187d81cc31a69b31c8d52"),
    "residual-checker": (12276, "53d9e62e6fd4c99a9891785f50242087a630fe9ef9dafba82d15db722f5cbe8e"),
    "coordinate-certificates": (9990, "19d3d8e1a3f5e11545ae6095b1cc74b674512d59b12f2212d19c34fbb9b976f3"),
    "positive-gain-certificates": (3687, "ab44c6fccf70dc5bae6b30b82f9e3983fe9c065b82d8301db3fc76bac13e5b59"),
    "no-gain-certificates": (26475, "f780c44424d7925b3b2a1e3d7ee1cbc757a7fc0b1daf14264d9699cc9d1532ec"),
    "witness-orbit-certificates": (6987, "cd46a986097405c2d270f15f2525df67e586cc53137e09ef5eafeafd42f2bd02"),
    "state-certificates": (5030, "037a4a6e51ef5cd76dc070bd461481ef90ac5520a875c0a96973c60f991172c7"),
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_identities():
    for name, path in IDENTITY_PATHS.items():
        if identity(path) != IDENTITIES[name]:
            raise RuntimeError(f"bound residual ancestry changed: {name}")


def parent_fingerprint(parent):
    accepted, cover_index, row = parent
    holes = embedded_holes(row["branch"], row["word"], row["edges"])[1]
    payload = f"{accepted}\t{cover_index}\t" + ",".join(f"{a}-{b}" for a, b in sorted(holes)) + "\n"
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def load_memberships():
    verify_identities()
    _, cover = residual.load_cover()
    result = []
    for leaf_ordinal, item in enumerate(cover):
        for parent_ordinal, parent in enumerate(item[1][4][2][6]):
            result.append((leaf_ordinal, item, parent_ordinal, parent))
    if len(cover) != LEAVES or len(result) != MEMBERSHIPS:
        raise RuntimeError("residual singleton-parent census changed")
    return tuple(cover), tuple(result)


def membership_key(member):
    leaf_ordinal, item, parent_ordinal, parent = member
    return f"r{leaf_ordinal:03d}-{residual.key(item)}-p{parent_ordinal:02d}-a{parent[0]:05d}"


def dimensions(member):
    variables, clauses = residual.dimensions(member[1])
    return variables, clauses + 1


def build_membership(member):
    _, item, parent_ordinal, _ = member
    cnf, selectors = residual.build_leaf(item)
    cnf.add(selectors[parent_ordinal])
    return cnf, selectors


def manifest_payload(cover, memberships):
    lines = [MANIFEST_FORMAT]
    for name, (size, digest) in IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.extend((f"residual-leaves\t{LEAVES}", f"memberships\t{MEMBERSHIPS}",
                  "split\tone CNF per residual membership with a positive unit selecting its exact parent",
                  "selector-cover\tfor each residual leaf, all parent selectors exactly once",
                  "selector-disjoint\tdistinct guarded parent hole projections are incompatible",
                  "selector-exhaustive\tthe residual leaf parent-selector ALO supplies at least one selector",
                  "proof-status\tscout-only; no LRAT generated or committed",
                  "columns\tmembership-ordinal,key,residual-leaf-ordinal,residual-key,parent-ordinal,accepted-ordinal,cover-index,parent-fingerprint,selector,variables,clauses"))
    offset = 0
    for ordinal, member in enumerate(memberships):
        leaf_ordinal, item, parent_ordinal, parent = member
        variables, clauses = dimensions(member)
        selector = variables - len(item[1][4][2][6]) + parent_ordinal + 1
        lines.append(f"{ordinal:04d}\t{membership_key(member)}\t{leaf_ordinal:03d}\t{residual.key(item)}\t"
                     f"{parent_ordinal:02d}\t{parent[0]:05d}\t{parent[1]:06d}\t{parent_fingerprint(parent)}\t"
                     f"{selector}\t{variables}\t{clauses}")
        offset += 1
    if offset != MEMBERSHIPS:
        raise RuntimeError("manifest omitted singleton memberships")
    return ("\n".join(lines) + "\n").encode("ascii")


def hash_payload(memberships, manifest, hashes=None):
    hashes = hashes or {}
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
             f"memberships\t{MEMBERSHIPS}",
             "columns\tmembership-ordinal,key,residual-leaf-ordinal,parent-ordinal,accepted-ordinal,cover-index,variables,clauses,cnf-sha256"]
    for ordinal, member in enumerate(memberships):
        variables, clauses = dimensions(member)
        lines.append(f"{ordinal:04d}\t{membership_key(member)}\t{member[0]:03d}\t{member[2]:02d}\t"
                     f"{member[3][0]:05d}\t{member[3][1]:06d}\t{variables}\t{clauses}\t"
                     f"{hashes.get(membership_key(member), '')}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(ordinal, member, manifest, selectors):
    leaf_ordinal, item, parent_ordinal, parent = member
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))),
              ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, (size, digest) in IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(size)), (f"{name}-sha256", digest)))
    result.extend((("membership-ordinal", str(ordinal)), ("key", membership_key(member)),
                   ("residual-leaf-ordinal", str(leaf_ordinal)), ("residual-key", residual.key(item)),
                   ("parent-ordinal", str(parent_ordinal)), ("accepted-ordinal", str(parent[0])),
                   ("cover-index", str(parent[1])), ("parent-fingerprint", parent_fingerprint(parent)),
                   ("parent-count", str(len(selectors))), ("selected-selector", str(selectors[parent_ordinal])),
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


def populate_hashes(memberships, manifest):
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="m6-residual-singleton-hashes-", dir=HERE.parent) as directory:
        path = Path(directory) / "membership.cnf"
        for ordinal, member in enumerate(memberships):
            cnf, selectors = build_membership(member)
            write_membership(path, ordinal, member, cnf, selectors, manifest)
            hashes[membership_key(member)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--membership", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    cover, memberships = load_memberships()
    manifest = manifest_payload(cover, memberships)
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
    print(f"residual_leaves={len(cover)} memberships={len(memberships)} "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
