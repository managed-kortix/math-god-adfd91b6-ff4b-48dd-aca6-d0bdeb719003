#!/usr/bin/env python3
"""Independent checker for the frozen exact B7-l6 30-leaf state split."""

import argparse
import hashlib
import itertools
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import check_m6_clean_sink_group_cnf as clean
from check_m6_parent_cnf import (
    BASE_CLAUSES, BASE_CLAUSE_SHA256, BASE_VARIABLES, BASE_VARIABLE_MAP_SHA256,
    PAIRS, clause_sha256, expected_projection, parse_cnf, variable_map_sha256,
)
from snc_cnf import CNF, generate, threshold

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-state-leaf-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-state-split-v1"
HASH_FORMAT = "m6-b7-l6-state-leaf-hashes-v1"
HASH_PATH = HERE / "m6-b7-l6-state-leaf-hashes.tsv"
GROUP = "B7-l6"
B_VERTICES = tuple(range(9, 16))
C_VERTICES = (16, 17)
PARENTS = 42
INCIDENCES = 260
LEAVES = 30
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
MANIFEST_BYTES = 4382
MANIFEST_SHA256 = "a3b8f9d17b50dbfccd5f00740b33c6e90f6f10d26a3854dd627a45681e5c890e"
HASH_BYTES = 3163
HASH_SHA256 = "eec464838f7d01e6cf053c7cbf8fa1442068d78738f4bd2772b15a8417543ae4"


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_identities():
    for name, path in IDENTITY_PATHS.items():
        if identity(path) != IDENTITIES[name]:
            raise RuntimeError(f"frozen clean-group identity changed: {name}")


def full_parent(row):
    full = ["R"] + ["A"] * 8 + ["B"] * 7 + ["C"] * 2
    return full, set(expected_projection(row)[1])


def independent_states(row):
    colors, holes = full_parent(row)
    hvec = tuple(sum(tuple(sorted((c, v))) in holes for v in range(18) if colors[v] in "RA")
                 for c in C_VERTICES)
    internal_options = ("h",) if C_VERTICES in holes else ("16>17", "17>16")
    states = []
    for internal in internal_options:
        internal_out = {"h": (0, 0), "16>17": (1, 0), "17>16": (0, 1)}[internal]
        for high in itertools.product((0, 1), repeat=2):
            cb = []
            for index, c in enumerate(C_VERTICES):
                universal_out = sum(colors[v] in "RA" and tuple(sorted((c, v))) not in holes
                                    for v in range(18))
                slots = sum(colors[v] == "B" and tuple(sorted((c, v))) not in holes
                            for v in range(18))
                value = 8 + high[index] - universal_out - internal_out[index]
                if value < 0 or value > slots:
                    break
                cb.append(value)
            if len(cb) == 2 and not any(high[i] and internal_out[i] == 0 and cb[i] == 0
                                         for i in range(2)):
                states.append((hvec, internal, high, tuple(cb)))
    return states


def key(state):
    hvec, internal, high, cb = state
    code = {"h": "h", "16>17": "f", "17>16": "r"}[internal]
    return f"h{hvec[0]}{hvec[1]}-c{code}-m{high[0]}{high[1]}-b{cb[0]}{cb[1]}"


def derive_leaves(remaining=clean.REMAINING, cover=HERE / "m6-placement-cover.txt",
                  filter_path=HERE / "m6-placement-filter.txt"):
    verify_identities()
    parents = clean.derive_groups(remaining, cover, filter_path)[GROUP]
    if len(parents) != PARENTS:
        raise RuntimeError("independent B7-l6 parent count changed")
    cells = defaultdict(list)
    for member in parents:
        for state in independent_states(member[2]):
            cells[state].append(member)
    leaves = [(key(state), state, cells[state]) for state in sorted(cells)]
    triples = [(name, accepted, cover_index) for name, _, members in leaves
               for accepted, cover_index, _ in members]
    if len(leaves) != LEAVES or len(triples) != INCIDENCES or len(set(triples)) != INCIDENCES:
        raise RuntimeError("independent 30-leaf/260-incidence split changed")
    if {accepted for _, accepted, _ in triples} != {accepted for accepted, _, _ in parents}:
        raise RuntimeError("independent state split does not cover all 42 parents")
    return leaves


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:02d}\t{accepted:05d}\t{cover:06d}"
                 for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def counter_shape(value):
    return 28, 98 + (1 if value in (0, 7) else 2)


def dimensions(state, count):
    return (BASE_VARIABLES + 56 + count,
            BASE_CLAUSES["B7"] + sum(counter_shape(v)[1] for v in state[3]) + 4 + 153 * count)


def manifest_payload(leaves):
    lines = [MANIFEST_FORMAT]
    for name, item in IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend((f"parent-group\t{GROUP}", f"parents\t{PARENTS}", f"incidences\t{INCIDENCES}",
                  f"leaves\t{LEAVES}",
                  "columns\tleaf-ordinal,key,h16,h17,internal,high-mask,cb16,cb17,parents,variables,clauses,member-sha256"))
    for ordinal, (name, state, members) in enumerate(leaves):
        hvec, internal, high, cb = state
        variables, clauses = dimensions(state, len(members))
        lines.append(f"{ordinal:02d}\t{name}\t{hvec[0]}\t{hvec[1]}\t{internal}\t{high[0]}{high[1]}\t"
                     f"{cb[0]}\t{cb[1]}\t{len(members)}\t{variables}\t{clauses}\t"
                     f"{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def load_hashes():
    raw = HASH_PATH.read_bytes()
    if HASH_BYTES and identity(HASH_PATH) != (HASH_BYTES, HASH_SHA256):
        raise RuntimeError("frozen leaf hash ledger changed")
    lines = raw.decode("ascii").splitlines()
    if len(lines) != LEAVES + 5 or lines[0] != HASH_FORMAT:
        raise RuntimeError("malformed leaf hash ledger")
    hashes = {}
    for ordinal, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if len(fields) != 6 or fields[0] != f"{ordinal:02d}" or len(fields[5]) != 64:
            raise RuntimeError("malformed leaf hash row")
        hashes[fields[1]] = fields[5]
    return hashes


@lru_cache(maxsize=1)
def frozen_base():
    cnf = generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    return tuple(cnf.names), tuple(cnf.clauses)


def force_exact(cnf, outputs, value):
    if value == 0:
        cnf.add(-outputs[0])
    elif value == len(outputs):
        cnf.add(outputs[-1])
    else:
        cnf.add(outputs[value - 1]); cnf.add(-outputs[value])


def expected_prefix(state):
    names, clauses = map(list, frozen_base())
    if (len(names) != BASE_VARIABLES or variable_map_sha256(names) != BASE_VARIABLE_MAP_SHA256 or
            len(clauses) != BASE_CLAUSES["B7"] or clause_sha256(clauses) != BASE_CLAUSE_SHA256["B7"]):
        raise RuntimeError("independent B7 base differs from frozen identity")
    cnf = CNF()
    cnf.names = {name: number for number, name in enumerate(names, 1)}
    cnf.clauses = clauses
    _, internal, high, cb = state
    internal_name = {"h": "h_16_17", "16>17": "a_16_17", "17>16": "a_17_16"}[internal]
    cnf.add(cnf.names[internal_name])
    for c, bit in zip(C_VERTICES, high):
        var = cnf.names[f"cnt_d1_{c}_17_9"]
        cnf.add(var if bit else -var)
    shapes = []
    for c, value in zip(C_VERTICES, cb):
        before = len(cnf.names), len(cnf.clauses)
        force_exact(cnf, threshold(cnf, [cnf.names[f"a_{c}_{b}"] for b in B_VERTICES],
                                       f"b7_l6_cb_{c}"), value)
        shapes.append((len(cnf.names) - before[0], len(cnf.clauses) - before[1]))
    return cnf, tuple(shapes)


def expected_metadata(ordinal, leaf, manifest, shapes, selectors):
    name, state, members = leaf
    hvec, internal, high, cb = state
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))),
              ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for bound, item in IDENTITIES.items():
        result.extend(((f"{bound}-bytes", str(item[0])), (f"{bound}-sha256", item[1])))
    result.extend((("leaf-ordinal", str(ordinal)), ("leaf-key", name), ("parent-group", GROUP),
                   ("parents", str(len(members))), ("h-vector", f"{hvec[0]},{hvec[1]}"),
                   ("internal-C", internal), ("high-mask", f"{high[0]}{high[1]}"),
                   ("C16-to-B", str(cb[0])), ("C17-to-B", str(cb[1])),
                   ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
                   ("base-variables", str(BASE_VARIABLES)),
                   ("base-variable-map-sha256", BASE_VARIABLE_MAP_SHA256),
                   ("base-clauses", str(BASE_CLAUSES["B7"])),
                   ("base-clause-sha256", BASE_CLAUSE_SHA256["B7"]),
                   ("state-unit-clauses", "3"),
                   ("C16-counter-variables", str(shapes[0][0])),
                   ("C16-counter-clauses", str(shapes[0][1])),
                   ("C17-counter-variables", str(shapes[1][0])),
                   ("C17-counter-clauses", str(shapes[1][1])),
                   ("alo-clauses", "1"), ("guarded-hole-clauses-per-parent", "153"),
                   ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    return result


def validate_model(variables, clauses, literals, selectors):
    values = {}
    for literal in literals:
        if not 1 <= abs(literal) <= len(variables) or abs(literal) in values:
            raise RuntimeError("model contains invalid or duplicate assignment")
        values[abs(literal)] = literal > 0
    if len(values) != len(variables):
        raise RuntimeError("model is incomplete")
    if any(not any(values[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses):
        raise RuntimeError("model falsifies a clause")
    selected = [i for i, selector in enumerate(selectors) if values[selector]]
    if len(selected) != 1:
        raise RuntimeError("model does not select exactly one parent")
    return values, selected[0]


def read_model(path):
    literals, terminated = [], False
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if not line or line.startswith("c ") or line in ("s SATISFIABLE", "SAT"):
            continue
        fields = line[2:].split() if line.startswith("v ") else line.split()
        for field in fields:
            value = int(field)
            if terminated:
                raise RuntimeError("model data follows terminator")
            if value == 0:
                terminated = True
            else:
                literals.append(value)
    if not terminated:
        raise RuntimeError("model has no terminator")
    return literals


def check(cnf_path, model_path=None):
    leaves = derive_leaves()
    manifest = manifest_payload(leaves)
    if MANIFEST_BYTES and (len(manifest), hashlib.sha256(manifest).hexdigest()) != (MANIFEST_BYTES, MANIFEST_SHA256):
        raise RuntimeError("independent state manifest changed")
    metadata, variables, clauses, declared = parse_cnf(cnf_path)
    ordinal = int(dict(metadata).get("leaf-ordinal", "-1"))
    if not 0 <= ordinal < LEAVES:
        raise RuntimeError("leaf ordinal outside exact split")
    leaf = leaves[ordinal]
    name, _, members = leaf
    prefix, shapes = expected_prefix(leaf[1])
    selectors = [prefix.var(f"b7_l6_parent_selector_{i:02d}") for i in range(len(members))]
    prefix.add(*selectors)
    if metadata != expected_metadata(ordinal, leaf, manifest, shapes, selectors):
        raise RuntimeError("leaf metadata differs from exact frozen record")
    if variables != list(prefix.names) or clauses[:len(prefix.clauses)] != list(prefix.clauses):
        raise RuntimeError("leaf base/state/counters/ALO prefix differs")
    suffix = iter(clauses[len(prefix.clauses):])
    for selector, (_, _, row) in zip(selectors, members):
        holes = expected_projection(row)[1]
        for pair in PAIRS:
            hole = prefix.names[f"h_{pair[0]}_{pair[1]}"]
            if next(suffix, None) != (-selector, hole if pair in holes else -hole):
                raise RuntimeError("selector is not guarded to its exact parent holes")
    if next(suffix, None) is not None or declared != dimensions(leaf[1], len(members)):
        raise RuntimeError("leaf suffix or DIMACS dimensions differ")
    digest = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
    hashes = load_hashes()
    if digest != hashes[name]:
        raise RuntimeError("leaf CNF hash differs from frozen ledger")
    print(f"PASS leaf={ordinal:02d} key={name} parents={len(members)} vars={declared[0]} "
          f"clauses={declared[1]} sha256={digest}")
    if model_path:
        values, selected = validate_model(variables, clauses, read_model(model_path), selectors)
        accepted, cover_index, row = members[selected]
        holes = expected_projection(row)[1]
        if any(values[prefix.names[f"h_{a}_{b}"]] != ((a, b) in holes) for a, b in PAIRS):
            raise RuntimeError("selected model holes disagree with attributed parent")
        print(f"PASS model-attribution leaf={ordinal:02d} selector={selected} "
              f"accepted={accepted} cover={cover_index}")
    return variables, clauses, members, selectors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()
    check(args.cnf, args.model)


if __name__ == "__main__":
    main()
