#!/usr/bin/env python3
"""Strict independent checker for exact residual m=6 selector-group CNFs."""

import argparse
import hashlib
import itertools
from collections import Counter
from functools import lru_cache
from pathlib import Path

from check_m6_parent_cnf import (
    BASE_CLAUSES, BASE_CLAUSE_SHA256, BASE_VARIABLES, BASE_VARIABLE_MAP_SHA256,
    COVER_SHA256, FILTER_SHA256, LABELS, PAIRS, clause_sha256, expected_projection,
    parse_cnf, read_acceptance, read_cover, variable_map_sha256,
)
from snc_cnf import CNF, generate, threshold

HERE = Path(__file__).resolve().parent
FORMAT = "m6-residual-selector-group-cnf-v1"
MANIFEST_FORMAT = "m6-residual-selector-groups-v1"
IDENTITY_PATHS = {
    "forced-certificate-ledger": HERE / "m6-forced-group-certificates.tsv",
    "forced-certificate-verifier": HERE / "verify_m6_forced_group_certificates.py",
    "forced-selector-manifest": HERE / "m6-forced-selector-groups.tsv",
}
IDENTITIES = {
    "forced-certificate-ledger": (4060, "819cc1c2015923d2ef59649028a34a841641519e5c46ef7559698720e18f5c65"),
    "forced-certificate-verifier": (5794, "d2e15b03ba68e6222cf140e0f742f2c1ae627e7ae0f1f657966bf8c48d51cebf"),
    "forced-selector-manifest": (1611, "6cf29f05bc2d76437c10b8c19e173c6d8c666f8001a3b1504ab1cf108932a29c"),
}
EXCLUSIONS = "B6:lambda=3;B7:lambda=1"
GROUP_KEYS = (
    "B6-l4-r0-t2", "B6-l4-r1-t3", "B6-l5-r0-t1", "B6-l5-r1-t2", "B6-l5-r2-t3",
    "B6-l6-r0-t0", "B6-l6-r1-t1", "B6-l6-r2-t2", "B6-l6-r3-t3",
    "B7-l2-r0-t1", "B7-l2-r1-t2", "B7-l3-r0-t0", "B7-l3-r1-t1", "B7-l3-r2-t2",
    "B7-l4-r1-t0", "B7-l4-r2-t1", "B7-l4-r3-t2", "B7-l5-r2-t0", "B7-l5-r3-t1",
    "B7-l5-r4-t2", "B7-l6-r3-t0", "B7-l6-r4-t1", "B7-l6-r5-t2",
)
GROUP_COUNTS = (6679, 6679, 1576, 1910, 1910, 167, 310, 340, 340, 17689, 17689,
                5016, 6981, 6981, 1649, 1943, 1943, 322, 358, 358, 42, 46, 46)
RESIDUAL_MEMBERSHIPS = 80974
BRANCH_MEMBERSHIPS = {"B6": 19911, "B7": 61063}
MANIFEST_BYTES = 3915
MANIFEST_SHA256 = "b55f0b8e69a77b64254285b9134262cedb961e18a13ad10e4ce350bd04caa85a"
GROUP_CNF_SHA256 = {
    "B6-l4-r0-t2": "d084873ba4f0e5f4c04777b9a49cecbc395ba3c552038c0301c26a21c8a6e62f",
    "B6-l4-r1-t3": "541f990890cb268d8a02a579ca56568e852d914ca8d9f793b4ca54e793ff7b19",
    "B6-l5-r0-t1": "3ab1592bed3b9b47edf6a02232c4a7d8e862ebf6570c24516f239ab393c10291",
    "B6-l5-r1-t2": "65054cf65b0c7a969447ea2428e8efe18fd5a5aca339d3f4e9569c23f8118448",
    "B6-l5-r2-t3": "3133a0f4254e60b2edb26beb999ee5310dba02a525e6e86b7b1f394afaa31ac0",
    "B6-l6-r0-t0": "4583f05df489799afb994d80f3cd5b7342924b6642d57552f887c1fb21bd674b",
    "B6-l6-r1-t1": "9b10be6dbca83c25a857e0da0e9a2718f05d09a50eff086f0c218f12a6bf0ca9",
    "B6-l6-r2-t2": "7a4dfb9def8ff473d6d990003e523807860c0a57d7f7b2e8e3261c14e0e7c842",
    "B6-l6-r3-t3": "7c9ac22fb54a1273582fa1bafdb03c2c2bba11a0dfa8751ffb8aa2b5c4538ee7",
    "B7-l2-r0-t1": "530b31ade1004cedc2a223ae9599469a761880780f52d31232366e9015f44426",
    "B7-l2-r1-t2": "03d1137f79460e66a2894d8d29f1bcc877f2636762fc5b9342d3ee312d174ace",
    "B7-l3-r0-t0": "6ccb5da5f75c1272c69185032f7661fe4b553a5413cfd28ecfe414798dcac60d",
    "B7-l3-r1-t1": "deb0a7b2350fc355cfa998038ddc13cb3fdf971777d2391850867464b36fd8ee",
    "B7-l3-r2-t2": "9d74bb0711953bd1d1a154f6c1a3659ea5c1cc9bc9deb94a927b323b00792f34",
    "B7-l4-r1-t0": "0be75640eb45fc62c817a396765465e90b9165eda405a5453ea91838f8da0d5f",
    "B7-l4-r2-t1": "cdd7df07b3b155a19dd00bcadfb0c3ed45288f2e3a913d5d6c3c3c4bda54241a",
    "B7-l4-r3-t2": "9aa5d6bb979b3369c8cd15305a1bbf98adca02af5f8f92a6881aedbf3b999270",
    "B7-l5-r2-t0": "f535f1797b0148b2b2c601ef0a641461dfea45678f889489cf4317138d015f64",
    "B7-l5-r3-t1": "c93086a1ab2d9cfb8d5dfffcfa8c356684f3e3ff3e0501d1f3405b38e0208cd0",
    "B7-l5-r4-t2": "9fad28d1f675f807aec327739bb746d89a5852b95786e21bf17ebbd6a3c24b94",
    "B7-l6-r3-t0": "e8af05abc8ef494227c6bd5aa0790f7bfc15a67280fcd022e0068cdab259838d",
    "B7-l6-r4-t1": "18157e438bec5a28c0ad82dd4da36f73a0c8b779cccdcb8b9b63e52ef879e33c",
    "B7-l6-r5-t2": "a1baeed7c055c635a1aaa3ab6848541bad2f47f5f00547c3bb2abefe33561dcc",
}


def verify_identities():
    for name, path in IDENTITY_PATHS.items():
        data = path.read_bytes()
        if (len(data), hashlib.sha256(data).hexdigest()) != IDENTITIES[name]:
            raise RuntimeError(f"excluded forced certificate identity changed: {name}")


def parameters(key):
    branch, lam, r, t = key.split("-")
    return branch, int(lam[1:]), int(r[1:]), int(t[1:])


def exact_states(row):
    """Enumerate internal-C orientations and each C vertex's exact degree target."""
    branch, _, _, _, colors, _, support_holes = row
    sizes = (1, 8, 6, 3) if branch == "B6" else (1, 8, 7, 2)
    full = list(colors)
    for color, size in zip("RABC", sizes):
        full.extend(color for _ in range(size - full.count(color)))
    holes = set(support_holes)
    cs = [vertex for vertex, color in enumerate(full) if color == "C"]
    present = lambda left, right: tuple(sorted((left, right))) not in holes
    lam = sum(1 for left, right in holes
              if "C" in (full[left], full[right]) and "B" not in (full[left], full[right]))
    states = set()
    cc_pairs = [pair for pair in itertools.combinations(cs, 2) if present(*pair)]
    for directions in itertools.product((0, 1), repeat=len(cc_pairs)):
        internal = Counter(pair[direction] for pair, direction in zip(cc_pairs, directions))
        options = []
        for c in cs:
            fixed = sum(full[v] in "RA" and present(c, v) for v in range(18)) + internal[c]
            available = sum(full[v] == "B" and present(c, v) for v in range(18))
            options.append([(target - fixed, int(target == 9)) for target in (8, 9)
                            if 0 <= target - fixed <= available])
        for choice in itertools.product(*options):
            states.add((sum(item[0] for item in choice), sum(item[1] for item in choice)))
    return branch, lam, states


def derive_groups(rows, statuses):
    groups = {key: [] for key in GROUP_KEYS}
    excluded = Counter()
    accepted = 0
    for index, (row, status) in enumerate(zip(rows, statuses)):
        if status != 0:
            continue
        branch, lam, states = exact_states(row)
        if (branch, lam) in (("B6", 3), ("B7", 1)):
            excluded[branch] += 1
        else:
            for r, t in sorted(states):
                key = f"{branch}-l{lam}-r{r}-t{t}"
                if key not in groups:
                    raise RuntimeError(f"unexpected independently derived state {key}")
                groups[key].append((accepted, index))
        accepted += 1
    if excluded != Counter(B6=14649, B7=25766):
        raise RuntimeError("certified forced exclusions changed")
    if tuple(map(len, groups.values())) != GROUP_COUNTS:
        raise RuntimeError("independently derived residual partition changed")
    branch_counts = Counter(key[:2] for key, members in groups.items() for _ in members)
    if branch_counts != Counter(BRANCH_MEMBERSHIPS):
        raise RuntimeError(f"independently derived branch subtotals changed: {branch_counts}")
    for key, members in groups.items():
        projections = [frozenset(expected_projection(rows[index])[1]) for _, index in members]
        if len(projections) != len(set(projections)):
            raise RuntimeError(f"duplicate projections in {key}")
    return groups


def member_payload(members):
    lines = ["columns\tmember-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{member:05d}\t{accepted:05d}\t{index:06d}"
                 for member, (accepted, index) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def counter_shape(inputs, target):
    return inputs * (inputs + 1) // 2, 2 * inputs * inputs + (1 if target in (0, inputs) else 2)


def dimensions(key, count):
    branch, _, r, t = parameters(key)
    b_count, c_count = len(LABELS[branch]["B"]), len(LABELS[branch]["C"])
    rv, rc = counter_shape(b_count * c_count, r)
    tv, tc = counter_shape(c_count, t)
    return BASE_VARIABLES + rv + tv + count, BASE_CLAUSES[branch] + rc + tc + 1 + 153 * count


def manifest_payload(groups):
    verify_identities()
    lines = [MANIFEST_FORMAT, f"cover-sha256\t{COVER_SHA256}",
             f"filter-sha256\t{FILTER_SHA256}", f"excluded-regimes\t{EXCLUSIONS}"]
    for name, (size, digest) in IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.extend((f"groups\t{len(GROUP_KEYS)}", f"memberships\t{RESIDUAL_MEMBERSHIPS}",
                  *(f"{branch}-memberships\t{count}"
                    for branch, count in BRANCH_MEMBERSHIPS.items()),
                  "columns\tgroup-ordinal,key,branch,lambda,r,t,members,first-selector,last-selector,variables,clauses,r-counter-variables,r-counter-clauses,highC-counter-variables,highC-counter-clauses,member-sha256"))
    for ordinal, key in enumerate(GROUP_KEYS):
        branch, lam, r, t = parameters(key)
        members = groups[key]
        b_count, c_count = len(LABELS[branch]["B"]), len(LABELS[branch]["C"])
        rv, rc = counter_shape(b_count * c_count, r)
        tv, tc = counter_shape(c_count, t)
        variables, clauses = dimensions(key, len(members))
        first = variables - len(members) + 1
        lines.append(f"{ordinal}\t{key}\t{branch}\t{lam}\t{r}\t{t}\t{len(members)}\t{first}\t"
                     f"{variables}\t{variables}\t{clauses}\t{rv}\t{rc}\t{tv}\t{tc}\t"
                     f"{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


@lru_cache(maxsize=None)
def frozen_base(branch):
    cnf = generate(18, 6 if branch == "B6" else 7, 6, robust_witness=True, arc_minimal=True)
    return tuple(cnf.names), tuple(cnf.clauses)


@lru_cache(maxsize=None)
def frozen_inputs(cover_path, filter_path):
    rows = read_cover(Path(cover_path))
    return rows, derive_groups(rows, read_acceptance(Path(filter_path)))


def force_exact(cnf, outputs, target):
    if target == 0:
        cnf.add(-outputs[0])
    elif target == len(outputs):
        cnf.add(outputs[-1])
    else:
        cnf.add(outputs[target - 1]); cnf.add(-outputs[target])


def add_expected_counters(cnf, key):
    branch, _, r, t = parameters(key)
    bs, cs = tuple(LABELS[branch]["B"]), tuple(LABELS[branch]["C"])
    before = len(cnf.names), len(cnf.clauses)
    force_exact(cnf, threshold(cnf, [cnf.names[f"a_{c}_{b}"] for c in cs for b in bs],
                               "residual_r"), r)
    r_shape = len(cnf.names) - before[0], len(cnf.clauses) - before[1]
    before = len(cnf.names), len(cnf.clauses)
    force_exact(cnf, threshold(cnf, [cnf.names[f"cnt_d1_{c}_17_9"] for c in cs],
                               "residual_highC"), t)
    return r_shape, (len(cnf.names) - before[0], len(cnf.clauses) - before[1])


def validate_model(variables, clauses, literals, first_selector, count):
    values = {}
    for literal in literals:
        if literal == 0 or not 1 <= abs(literal) <= len(variables):
            raise RuntimeError("model contains invalid literal")
        number, value = abs(literal), literal > 0
        if number in values:
            raise RuntimeError("model assigns a CNF variable more than once")
        values[number] = value
    if len(values) != len(variables):
        raise RuntimeError(f"model omits {len(variables) - len(values)} CNF variables")
    for ordinal, clause in enumerate(clauses):
        if not any(values[abs(lit)] == (lit > 0) for lit in clause):
            raise RuntimeError(f"model falsifies CNF clause {ordinal}")
    selected = [number - first_selector for number in range(first_selector, first_selector + count)
                if values[number]]
    if len(selected) != 1:
        raise RuntimeError(f"model must have exactly one true selector, found {len(selected)}")
    return values, selected[0]


def read_model(path):
    literals, terminated = [], False
    for line_number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("c ") or line in ("s SATISFIABLE", "SAT"):
            continue
        fields = line[2:].split() if line.startswith("v ") else line.split()
        try:
            numbers = [int(field) for field in fields]
        except ValueError as error:
            raise RuntimeError(f"noninteger model token line {line_number}") from error
        for number in numbers:
            if terminated:
                raise RuntimeError("model has data after zero terminator")
            if number == 0:
                terminated = True
            else:
                literals.append(number)
    if not terminated:
        raise RuntimeError("model has no zero terminator")
    return literals


def check(cnf_path, cover_path, filter_path, model_path=None):
    rows, groups = frozen_inputs(str(cover_path.resolve()), str(filter_path.resolve()))
    manifest = manifest_payload(groups)
    manifest_hash = hashlib.sha256(manifest).hexdigest()
    if MANIFEST_BYTES and (len(manifest) != MANIFEST_BYTES or manifest_hash != MANIFEST_SHA256):
        raise RuntimeError("independent residual manifest fingerprint changed")
    metadata_items, variables, clauses, declared = parse_cnf(cnf_path)
    metadata = dict(metadata_items)
    ordinal = int(metadata.get("group-ordinal", "-1"))
    if not 0 <= ordinal < len(GROUP_KEYS):
        raise RuntimeError("group ordinal outside frozen manifest")
    key, members = GROUP_KEYS[ordinal], groups[GROUP_KEYS[ordinal]]
    branch, lam, r, t = parameters(key)
    frozen_names, frozen_clauses = frozen_base(branch)
    base_names, base_clauses = list(frozen_names), list(frozen_clauses)
    if (len(base_names) != BASE_VARIABLES or variable_map_sha256(base_names) != BASE_VARIABLE_MAP_SHA256 or
            len(base_clauses) != BASE_CLAUSES[branch] or clause_sha256(base_clauses) != BASE_CLAUSE_SHA256[branch]):
        raise RuntimeError("base reconstruction differs from frozen fingerprint")
    base = CNF()
    base.names = {name: number for number, name in enumerate(base_names, 1)}
    base.clauses = base_clauses
    shapes = add_expected_counters(base, key)
    selectors = [base.var(f"residual_group_selector_{member:05d}") for member in range(len(members))]
    base.add(*selectors)
    expected_metadata = [
        ("format", FORMAT), ("group-manifest-format", MANIFEST_FORMAT),
        ("group-manifest-bytes", str(len(manifest))), ("group-manifest-sha256", manifest_hash),
        ("cover-sha256", COVER_SHA256), ("filter-sha256", FILTER_SHA256),
        ("excluded-regimes", EXCLUSIONS),
    ]
    for name, (size, digest) in IDENTITIES.items():
        expected_metadata.extend(((f"{name}-bytes", str(size)), (f"{name}-sha256", digest)))
    expected_metadata.extend((
        ("group-ordinal", str(ordinal)), ("group-key", key), ("branch", branch),
        ("lambda", str(lam)), ("r", str(r)), ("highC", str(t)), ("members", str(len(members))),
        ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
        ("base-variables", str(BASE_VARIABLES)), ("base-variable-map-sha256", BASE_VARIABLE_MAP_SHA256),
        ("base-clauses", str(BASE_CLAUSES[branch])), ("base-clause-sha256", BASE_CLAUSE_SHA256[branch]),
        ("r-counter-variables", str(shapes[0][0])), ("r-counter-clauses", str(shapes[0][1])),
        ("highC-counter-variables", str(shapes[1][0])), ("highC-counter-clauses", str(shapes[1][1])),
        ("alo-clauses", "1"), ("guarded-hole-clauses-per-member", "153"),
        ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1])),
    ))
    if metadata_items != expected_metadata:
        raise RuntimeError("metadata is not exact canonical residual record")
    if variables != list(base.names) or clauses[:len(base.clauses)] != list(base.clauses):
        raise RuntimeError("CNF prefix is not base, exact counters, and selector ALO")
    suffix = iter(clauses[len(base.clauses):])
    for selector, (_, index) in zip(selectors, members):
        holes = expected_projection(rows[index])[1]
        for pair in PAIRS:
            number = base.names[f"h_{pair[0]}_{pair[1]}"]
            expected = (-selector, number if pair in holes else -number)
            if next(suffix, None) != expected:
                raise RuntimeError("CNF suffix is not 153 canonical guarded holes per member")
    if next(suffix, None) is not None:
        raise RuntimeError("CNF has data after canonical guarded-hole suffix")
    if declared != dimensions(key, len(members)):
        raise RuntimeError("DIMACS dimensions differ from exact residual shape")
    digest = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
    if GROUP_CNF_SHA256 and digest != GROUP_CNF_SHA256[key]:
        raise RuntimeError("group CNF hash differs from frozen fingerprint")
    print(f"PASS group={key} members={len(members)} vars={declared[0]} clauses={declared[1]} "
          f"bytes={cnf_path.stat().st_size} sha256={digest}")
    if model_path:
        values, member = validate_model(variables, clauses, read_model(model_path), selectors[0], len(members))
        holes = expected_projection(rows[members[member][1]])[1]
        for pair in PAIRS:
            if values[base.names[f"h_{pair[0]}_{pair[1]}"]] != (pair in holes):
                raise RuntimeError("selected member disagrees with guarded projection")
        print(f"PASS model-attribution member={member}:accepted={members[member][0]}:cover={members[member][1]}")
    return variables, clauses, rows, members, selectors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--cover", type=Path, default=HERE / "m6-placement-cover.txt")
    parser.add_argument("--filter", type=Path, default=HERE / "m6-placement-filter.txt")
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()
    check(args.cnf, args.cover, args.filter, args.model)


if __name__ == "__main__":
    main()
