#!/usr/bin/env python3
"""Emit the frozen exact 30-leaf state split of clean-sink B7-l6."""

import argparse
import hashlib
import itertools
from collections import Counter, defaultdict
from pathlib import Path

import m6_clean_sink_group_cnf as source
from snc_cnf import threshold

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-state-leaf-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-state-split-v1"
HASH_FORMAT = "m6-b7-l6-state-leaf-hashes-v1"
GROUP = "B7-l6"
C_VERTICES = (16, 17)
B_VERTICES = tuple(range(9, 16))
IDENTITY_PATHS = {
    "clean-parent-manifest": HERE / "m6-clean-sink-selector-groups.tsv",
    "clean-remaining-stream": HERE / "m6-clean-sink-remaining.tsv",
    "clean-partition-manifest": HERE / "m6-clean-sink-manifest.tsv",
    "clean-sink-theorem": HERE.parent / "attempts" / "tick52-rooted-clean-sink-theorem.md",
    "clean-group-producer": HERE / "m6_clean_sink_group_cnf.py",
    "clean-group-checker": HERE / "check_m6_clean_sink_group_cnf.py",
}
IDENTITIES = {
    "clean-parent-manifest": (1838, "6e7eee0ddd5b4c7ef02cdf459c9a0647f720513e7ee4987a3a8b0c17af37eeda"),
    "clean-remaining-stream": (2262190, "416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642"),
    "clean-partition-manifest": (2104, "733e06c8aa9881e0006409efff23729f1bf88d8af7b1a70e8a78fd3775b53217"),
    "clean-sink-theorem": (4156, "bd0631529bb4658061663460b718ef2ee3186d02fdc599fb2673d3cff3b94ee2"),
    "clean-group-producer": (11550, "9eb6455daf71a2127f76a197012c2e0f4a7c7f42021ddfcfbe244f9f733ed817"),
    "clean-group-checker": (14918, "07d2ac0802c8d9fc854e8c5e10ef0e1a67f54dda2c06c1a71bf69465390ee536"),
}
PARENTS = 42
INCIDENCES = 260
LEAVES = 30
MANIFEST_BYTES = 4382
MANIFEST_SHA256 = "a3b8f9d17b50dbfccd5f00740b33c6e90f6f10d26a3854dd627a45681e5c890e"
HASH_BYTES = 3163
HASH_SHA256 = "eec464838f7d01e6cf053c7cbf8fa1442068d78738f4bd2772b15a8417543ae4"
LEAF_CNF_SHA256 = {
    "h14-ch-m00-b03": "8c805a8d0b1e7d909475cf9a4fffd6ccd88f2e78cede01b076fb8e82ae722eb4",
    "h14-ch-m01-b04": "963ed28a0b24540d26c1ea624d446769588e837cf6740f07d12af63cd08e885d",
    "h14-ch-m10-b13": "d2b905aa02fb085592af294a4c965ff087c2c421c45f4aed2e8692716f24a12d",
    "h14-ch-m11-b14": "7baf1e6dfb25020830d7a6b000eb50f9614a92cff0879d432b5973e835d208cd",
    "h15-cf-m10-b04": "6cf8973a10f84c5c9cc371a0ba9f615a8e9b98cebedacf5100dfb4b368bd687a",
    "h15-cf-m11-b05": "193cd7b8a0a5017a41ba3c86c12de12c89d7f5f00a5a3b4889f0b365803f9830",
    "h15-cr-m00-b03": "efc5d792fe89c48bc493a330fa4a74526f49d229bc7a3b2cb569d08fde469405",
    "h15-cr-m01-b04": "2192bf35606c6e8546ed069d9288d60fb925424943e8c2a62a309da17909bebe",
    "h15-cr-m10-b13": "ce09ed3263228a39cbab38f6c733d5ec288978643b086d40f02c32f7ef7596d9",
    "h15-cr-m11-b14": "cf3643522bf65ca7a0ce90ff167e3572f015628f88dac3f287504a1e4cb50610",
    "h23-ch-m00-b12": "bf21a50bb66619b4f069f85c592056cef16464077beeb79671c4435ca1cd35c1",
    "h23-ch-m01-b13": "6879655193d4db61e297b16c09d4564abf29d60eb3d969c8fb81af6accfd7a7a",
    "h23-ch-m10-b22": "48c41d7aa457e250be36efa1a92f0d39025c25d0823fc7c9613989942b07a589",
    "h23-ch-m11-b23": "6de35d696ee9e87e47c71562b16d39997a0ce9c7c1d2421953e802dd7004493c",
    "h24-cf-m00-b03": "a0f6fe7abfb659912282e300bec7b2775df05f88b208c69505e0c92ddc24e521",
    "h24-cf-m01-b04": "4c4855998d3b2bd590b0a5dd5355116abaf7c7250bce5e841e5018382d3bbba8",
    "h24-cf-m10-b13": "26c50d303af8b171323d55e6b42f5808ad5607f5fe1e0f274b7ba4bc0abe303a",
    "h24-cf-m11-b14": "780bf5d15e6fa82c091f1c374352fc4af888395bdafae51ac0dc767bf7891ad5",
    "h24-cr-m00-b12": "eff542c0473d3b0d7b0e3fa02bbe83cbb1e2bbee72002cd5271581fd4ea421fb",
    "h24-cr-m01-b13": "45d628b10c2dfe010d20a59ae0af7f7a0294f7a19e57f36896417923758603d1",
    "h24-cr-m10-b22": "bfe53fa4f7eec79426e5c11581f36d2b71ccea535634bce09fbb44205fecc5a8",
    "h24-cr-m11-b23": "eab0e6f1799f41dbaf84310bcfb42afb679c8337b043755ffa86b1244208ee6b",
    "h33-cf-m00-b12": "5a11d0d718fb112ab9873efebceaa4dcea65eac84ca98f7c2b0f82fe158e541a",
    "h33-cf-m01-b13": "8be09a8e6dcbe0df0cb21ca757fe25e20ff7e3452ab9611d34b3c8e13fbaad78",
    "h33-cf-m10-b22": "873d8ab2066218f2c3c8ffbb73a53958417bf29457cbc7c1ba9501bece319c1f",
    "h33-cf-m11-b23": "3cbd81c3d8c6f8c0528f17c74c926f3f5f8feaf3c67bd1af5572db2299ebc736",
    "h33-cr-m00-b21": "4e0e54495efde438bec4639c34bf4e0df2608fc60e50bfcbaf38c1c003aa3768",
    "h33-cr-m01-b22": "2fbb8aa3637ba5cd2f3a10e1825d03da202fd1097eeabc9cc084dccf8e1109c7",
    "h33-cr-m10-b31": "1efde0f900b4dff014998729692f45104137ed74e6a876af4aeff78cf1422637",
    "h33-cr-m11-b32": "4febed03d6bf7d49ed87a4aa0ec6e2d0d290260606721c4f1b4176429b7c4a64",
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_identities():
    for name, path in IDENTITY_PATHS.items():
        if IDENTITIES[name] != (0, "") and identity(path) != IDENTITIES[name]:
            raise RuntimeError(f"frozen clean-group identity changed: {name}")


def state_key(hvec, internal, high, cb):
    internal_name = {"h": "h", "16>17": "f", "17>16": "r"}[internal]
    return f"h{hvec[0]}{hvec[1]}-c{internal_name}-m{high[0]}{high[1]}-b{cb[0]}{cb[1]}"


def parent_states(row):
    labels = source.parent.CELL_LABELS[GROUP[:2]]
    _, holes = source.parent.embedded_holes(row["branch"], row["word"], row["edges"])
    colors = {vertex: cell for vertices, cell in zip(labels, "RABC") for vertex in vertices}
    hvec = tuple(sum(tuple(sorted((c, vertex))) in holes
                     for vertex in range(18) if colors[vertex] in "RA") for c in C_VERTICES)
    internal_states = ("h",) if C_VERTICES in holes else ("16>17", "17>16")
    result = []
    for internal in internal_states:
        internal_out = (0, 0) if internal == "h" else ((1, 0) if internal == "16>17" else (0, 1))
        for high in itertools.product((0, 1), repeat=2):
            cb = []
            for index, c in enumerate(C_VERTICES):
                fixed = sum(colors[v] in "RA" and tuple(sorted((c, v))) not in holes
                            for v in range(18)) + internal_out[index]
                available = sum(colors[v] == "B" and tuple(sorted((c, v))) not in holes
                                for v in range(18))
                required = 8 + high[index] - fixed
                if not 0 <= required <= available:
                    break
                cb.append(required)
            if len(cb) != 2:
                continue
            if any(high[i] and internal_out[i] == 0 and cb[i] == 0 for i in range(2)):
                continue
            result.append((hvec, internal, high, tuple(cb)))
    if not result:
        raise RuntimeError("clean B7-l6 parent has no surviving exact C state")
    return result


def load_leaves():
    verify_identities()
    parents = source.load_groups()[GROUP]
    if len(parents) != PARENTS:
        raise RuntimeError("clean B7-l6 parent count changed")
    cells = defaultdict(list)
    for member in parents:
        for state in parent_states(member[2]):
            cells[state].append(member)
    leaves = [(state_key(*state), state, cells[state]) for state in sorted(cells)]
    flattened = [(key, accepted, cover) for key, _, members in leaves
                 for accepted, cover, _ in members]
    if len(leaves) != LEAVES or len(flattened) != INCIDENCES:
        raise RuntimeError("exact state split count changed")
    if len(flattened) != INCIDENCES or {accepted for _, accepted, _ in flattened} != {
            accepted for accepted, _, _ in parents}:
        raise RuntimeError("state incidences are not a complete disjoint leaf cover")
    return leaves


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:02d}\t{accepted:05d}\t{cover:06d}"
                 for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def counter_shape(target):
    return 28, 98 + (1 if target in (0, 7) else 2)


def dimensions(state, count):
    cb = state[3]
    cv = sum(counter_shape(value)[0] for value in cb)
    cc = sum(counter_shape(value)[1] for value in cb)
    return source.parent.BASE_VARIABLES + cv + count, source.parent.BASE_CLAUSES["B7"] + cc + 3 + 1 + 153 * count


def exact(cnf, outputs, value):
    if value == 0:
        cnf.add(-outputs[0])
    elif value == len(outputs):
        cnf.add(outputs[-1])
    else:
        cnf.add(outputs[value - 1])
        cnf.add(-outputs[value])


def add_state(cnf, state):
    _, internal, high, cb = state
    internal_var = cnf.names["h_16_17"] if internal == "h" else cnf.names[
        "a_16_17" if internal == "16>17" else "a_17_16"]
    cnf.add(internal_var)
    for c, bit in zip(C_VERTICES, high):
        var = cnf.names[f"cnt_d1_{c}_17_9"]
        cnf.add(var if bit else -var)
    shapes = []
    for c, value in zip(C_VERTICES, cb):
        before = len(cnf.names), len(cnf.clauses)
        outputs = threshold(cnf, [cnf.names[f"a_{c}_{b}"] for b in B_VERTICES], f"b7_l6_cb_{c}")
        exact(cnf, outputs, value)
        shapes.append((len(cnf.names) - before[0], len(cnf.clauses) - before[1]))
    return tuple(shapes)


def build_leaf(state, members):
    cnf = source.parent.generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    if (len(cnf.names) != source.parent.BASE_VARIABLES or
            source.parent.variable_map_sha256(cnf) != source.parent.BASE_VARIABLE_MAP_SHA256 or
            len(cnf.clauses) != source.parent.BASE_CLAUSES["B7"] or
            source.parent.clause_sha256(cnf.clauses) != source.parent.BASE_CLAUSE_SHA256["B7"]):
        raise RuntimeError("generated B7 base differs from frozen identity")
    shapes = add_state(cnf, state)
    selectors = [cnf.var(f"b7_l6_parent_selector_{i:02d}") for i in range(len(members))]
    cnf.add(*selectors)
    for selector, (_, _, row) in zip(selectors, members):
        holes = source.parent.embedded_holes(row["branch"], row["word"], row["edges"])[1]
        for pair in source.parent.PAIRS:
            hole = cnf.names[f"h_{pair[0]}_{pair[1]}"]
            cnf.add(-selector, hole if pair in holes else -hole)
    return cnf, shapes, selectors


def manifest_payload(leaves):
    lines = [MANIFEST_FORMAT]
    for name, item in IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend((f"parent-group\t{GROUP}", f"parents\t{PARENTS}", f"incidences\t{INCIDENCES}",
                  f"leaves\t{LEAVES}",
                  "columns\tleaf-ordinal,key,h16,h17,internal,high-mask,cb16,cb17,parents,variables,clauses,member-sha256"))
    for ordinal, (key, state, members) in enumerate(leaves):
        hvec, internal, high, cb = state
        variables, clauses = dimensions(state, len(members))
        lines.append(f"{ordinal:02d}\t{key}\t{hvec[0]}\t{hvec[1]}\t{internal}\t{high[0]}{high[1]}\t"
                     f"{cb[0]}\t{cb[1]}\t{len(members)}\t{variables}\t{clauses}\t"
                     f"{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def hash_payload(leaves, manifest):
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"leaves\t{LEAVES}",
             "columns\tleaf-ordinal,key,parents,variables,clauses,cnf-sha256"]
    for ordinal, (key, state, members) in enumerate(leaves):
        variables, clauses = dimensions(state, len(members))
        lines.append(f"{ordinal:02d}\t{key}\t{len(members)}\t{variables}\t{clauses}\t{LEAF_CNF_SHA256.get(key, '')}")
    return ("\n".join(lines) + "\n").encode("ascii")


def write_leaf(path, ordinal, leaf, cnf, shapes, selectors, manifest):
    key, state, members = leaf
    hvec, internal, high, cb = state
    metadata = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
                ("manifest-bytes", str(len(manifest))),
                ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, item in IDENTITIES.items():
        metadata.extend(((f"{name}-bytes", str(item[0])), (f"{name}-sha256", item[1])))
    metadata.extend((("leaf-ordinal", str(ordinal)), ("leaf-key", key), ("parent-group", GROUP),
                     ("parents", str(len(members))), ("h-vector", f"{hvec[0]},{hvec[1]}"),
                     ("internal-C", internal), ("high-mask", f"{high[0]}{high[1]}"),
                     ("C16-to-B", str(cb[0])), ("C17-to-B", str(cb[1])),
                     ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
                     ("base-variables", str(source.parent.BASE_VARIABLES)),
                     ("base-variable-map-sha256", source.parent.BASE_VARIABLE_MAP_SHA256),
                     ("base-clauses", str(source.parent.BASE_CLAUSES["B7"])),
                     ("base-clause-sha256", source.parent.BASE_CLAUSE_SHA256["B7"]),
                     ("state-unit-clauses", "3"),
                     ("C16-counter-variables", str(shapes[0][0])),
                     ("C16-counter-clauses", str(shapes[0][1])),
                     ("C17-counter-variables", str(shapes[1][0])),
                     ("C17-counter-clauses", str(shapes[1][1])),
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
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--leaf", type=int)
    selection.add_argument("--key")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    args = parser.parse_args()
    if not any((args.output, args.manifest_output, args.hash_output)):
        parser.error("at least one output is required")
    leaves = load_leaves()
    manifest = manifest_payload(leaves)
    if MANIFEST_BYTES and identity_bytes(manifest) != (MANIFEST_BYTES, MANIFEST_SHA256):
        raise RuntimeError("state split manifest fingerprint changed")
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    hashes = hash_payload(leaves, manifest)
    if HASH_BYTES and identity_bytes(hashes) != (HASH_BYTES, HASH_SHA256):
        raise RuntimeError("state split hash ledger fingerprint changed")
    if args.hash_output:
        args.hash_output.write_bytes(hashes)
    if args.output:
        matches = [(i, leaf) for i, leaf in enumerate(leaves)
                   if i == args.leaf or leaf[0] == args.key]
        if len(matches) != 1:
            parser.error("--output requires exactly one valid --leaf or --key")
        ordinal, leaf = matches[0]
        cnf, shapes, selectors = build_leaf(leaf[1], leaf[2])
        write_leaf(args.output, ordinal, leaf, cnf, shapes, selectors, manifest)
        digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
        if LEAF_CNF_SHA256 and digest != LEAF_CNF_SHA256[leaf[0]]:
            raise RuntimeError("state leaf CNF fingerprint changed")
        print(f"leaf={ordinal:02d} key={leaf[0]} parents={len(leaf[2])} vars={len(cnf.names)} "
              f"clauses={len(cnf.clauses)} sha256={digest}")
    print(f"parents={PARENTS} incidences={INCIDENCES} leaves={LEAVES} "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


def identity_bytes(data):
    return len(data), hashlib.sha256(data).hexdigest()


if __name__ == "__main__":
    main()
