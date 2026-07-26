#!/usr/bin/env python3
"""Fail-closed conditional frontier census for rank-eleven cactus residuals.

The packet ledger assumes the rank-ten cactus conclusion for every connected
component of rank at most ten.  The program proves no graph theorem: it only
enumerates colored cluster partitions and fully shared cycle-cut incidence
trees for the sharp-DNN residuals T^10Q and T^9PP.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "rank_nine_incidence", HERE / "nonacyclic-fully-shared-incidence-census.py"
)
BASE = module_from_spec(SPEC)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


require(SPEC.loader is not None, "cannot load incidence-tree generator")
sys.modules[SPEC.name] = BASE
SPEC.loader.exec_module(BASE)

TRIANGLE_MARGIN = {
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 2,
    6: 1,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
}

EXPECTED_PARTITIONS = {
    "T^10Q": (139, 138, 133, 5),
    "T^9PP": (267, 266, 253, 13),
}

EXPECTED_T10Q = {
    "q=3": {1: 1, 2: 14, 3: 116, 4: 615, 5: 2167, 6: 5018, 7: 7431, 8: 6614, 9: 3141, 10: 598},
    "q=4": {1: 1, 2: 14, 3: 116, 4: 624, 5: 2208, 6: 5166, 7: 7732, 8: 7000, 9: 3398, 10: 672},
    "q=5": {1: 1, 2: 14, 3: 116, 4: 624, 5: 2215, 6: 5192, 7: 7805, 8: 7112, 9: 3493, 10: 704},
    "q=6": {1: 1, 2: 14, 3: 116, 4: 624, 5: 2215, 6: 5197, 7: 7819, 8: 7144, 9: 3525, 10: 719},
    "q=7": {1: 1, 2: 14, 3: 116, 4: 624, 5: 2215, 6: 5197, 7: 7822, 8: 7151, 9: 3536, 10: 725},
    "q=8": {1: 1, 2: 14, 3: 116, 4: 624, 5: 2215, 6: 5197, 7: 7822, 8: 7153, 9: 3539, 10: 728},
    "q=9": {1: 1, 2: 14, 3: 116, 4: 624, 5: 2215, 6: 5197, 7: 7822, 8: 7153, 9: 3540, 10: 729},
    "q=10": {1: 1, 2: 14, 3: 116, 4: 624, 5: 2215, 6: 5197, 7: 7822, 8: 7153, 9: 3540, 10: 730},
    "hostile q>=11": {1: 1, 2: 14, 3: 116, 4: 624, 5: 2215, 6: 5197, 7: 7822, 8: 7153, 9: 3540, 10: 730},
}

EXPECTED_T9PP = {
    1: 1,
    2: 22,
    3: 264,
    4: 1790,
    5: 7560,
    6: 20080,
    7: 33154,
    8: 32369,
    9: 16775,
    10: 3497,
}

EXPECTED_CLASS_DIGESTS = {
    ("TQ", 3): "43e52041bcf83b695a781fc079a2d23118ba812851e15216e8d0dd9b64d9c684",
    ("TQ", 4): "776c6cb6c04c824522d2c8de4789e26a2538bbcf04a39fb1543629c94747db5b",
    ("TQ", 5): "1a8055ce4afc004641ab2ec12244d5e0d0d1c929360fe2cc3858872bd3135c1e",
    ("TQ", 6): "d61711031f88e89295654302926dbb0de7149e63c7fbf4c608085ba8ac207e8a",
    ("TQ", 7): "ff40e19b970ce298f47a8acf8e0ca0eaf23295fb3e7d770c8bfbd4d21fb5b955",
    ("TQ", 8): "f019d6c94d8cc3e0f83271a9252abf7a1c8ac833639098460ef06aac39b94800",
    ("TQ", 9): "803c2cb33ec2368d7eb8557f782d6a3ad458af295d7633e7f28dec5a50da0a4f",
    ("TQ", 10): "18c7664d93d56d7bc16970bf951a3d0acf740c3206609a50c4172e1be994e467",
    ("TPP", 0): "65f4d845ff0ef17ce7880992810de149fd2108927e2ef03b8fac57032ac72ce2",
}

EXPECTED_RESIDUAL_DIGESTS = {
    "common": "a05009b2d94240464412b26915b203925b874685ff0a3286f753da3363f7f853",
    "hostile": "328bf92b88e9d14060effd1bd5b6ccbe8398e55849351b89ff025a6ab3fbb1e9",
    "TPP": "a0da0cf78b0dc0a11a86151a985fefddcd425b6743814877e7caf8d00ff5a56e",
}

T10Q_COMMON = "X(Q()T()T()T()T()T()T()T()T()T()T())"
T10Q_HOSTILE = {
    T10Q_COMMON,
    "T(X(Q())X(T()T()T()T()T()T()T()T()T()))",
    "T(X(Q())X(T())X(T()T()T()T()T()T()T()T()))",
}

T9PP_EXCEPTIONS = {
    "X(P()P()T()T()T()T()T()T()T()T()T())",
    "P(X(P())X(T()T()T()T()T()T()T()T()T()))",
    "T(X(P())X(P()T()T()T()T()T()T()T()T()))",
    "P(X(P())X(T())X(T()T()T()T()T()T()T()T()))",
    "T(X(P())X(P())X(T()T()T()T()T()T()T()T()))",
    "T(X(P())X(P()T()T()T()T()T()T()T())X(T()))",
    "X(T()T()T()T()T()T()T()T(X(P()))T(X(P())))",
    "P(X(P())X(T())X(T())X(T()T()T()T()T()T()T()))",
    "X(T()T()T()T()T()T()T(X(P()))T(X(P())X(T())))",
    "X(T()T()T()T()T()T(X(P())X(T()))T(X(P())X(T())))",
}
NEW_ROUTER = "P(X(P())X(T())X(T())X(T()T()T()T()T()T()T()))"


def signature_digest(signatures):
    return sha256(("\n".join(signatures) + "\n").encode("ascii")).hexdigest()


def partitions(triangles, distinguished, minimum=(0, 0)):
    rows = []
    for triangles_here in range(triangles + 1):
        for distinguished_here in range(distinguished + 1):
            part = (triangles_here, distinguished_here)
            if part == (0, 0) or part < minimum:
                continue
            if part == (triangles, distinguished):
                rows.append((part,))
                continue
            for rest in partitions(
                triangles - triangles_here,
                distinguished - distinguished_here,
                part,
            ):
                rows.append((part,) + rest)
    return rows


def triangle_bound(triangles):
    require(triangles in TRIANGLE_MARGIN, f"missing A_{triangles} bound")
    return Fraction(TRIANGLE_MARGIN[triangles]), True


def tq_profile_bound(part):
    triangles, q_count = part
    require(q_count in (0, 1), f"invalid TQ profile {part}")
    if q_count == 0:
        return triangle_bound(triangles)
    if triangles == 0:
        return Fraction(-1), False
    if triangles == 1:
        return Fraction(0), True
    if triangles == 2:
        return Fraction(0), False
    return Fraction(0), True


def tpp_profile_bound(part):
    triangles, pentagons = part
    require(pentagons in (0, 1, 2), f"invalid TPP profile {part}")
    rank = triangles + pentagons
    if pentagons == 0:
        return triangle_bound(triangles)
    if part == (0, 1):
        return Fraction(-1, 4), False
    if part == (1, 1):
        return Fraction(3, 4), True
    if part == (0, 2):
        return Fraction(0), True
    if part == (1, 2):
        return Fraction(3, 2), True
    if rank in (2, 3):
        return Fraction(0), False
    return Fraction(0), True


def partition_audit(triangles, distinguished, bound):
    all_rows = partitions(triangles, distinguished)
    require(len(all_rows) == len(set(all_rows)), "duplicate colored partition")
    proper_rows = [row for row in all_rows if len(row) > 1]
    residual = []
    for row in proper_rows:
        bounds = [bound(part) for part in row]
        total = sum((value for value, _ in bounds), Fraction())
        strict = any(flag for _, flag in bounds)
        if not (total > 0 or (total == 0 and strict)):
            residual.append(row)
    return all_rows, proper_rows, residual


def tq_component_bound(label, tree, component):
    counts = Counter(tree.colors[cycle] for cycle in component[0])
    triangles, q_count = counts["T"], counts["Q"]
    require(q_count in (0, 1), "component contains multiple Q cycles")
    if q_count == 0:
        value, strict = triangle_bound(triangles)
        return BASE.Bound(value, strict, f"A_{triangles}")
    if triangles == 0:
        if label == "q=3":
            return BASE.Bound(Fraction(0), True, "Q=T>0")
        if label in {"q=4", "q=6", "q=8", "q=10"}:
            return BASE.Bound(Fraction(0), False, "even Q>=0")
        return BASE.Bound(Fraction(-1), True, "hostile Q>-1")
    if triangles == 1:
        return BASE.Bound(Fraction(0), True, "TQ>0")
    if triangles == 2:
        return BASE.Bound(Fraction(0), False, "TTQ>=0")
    require(triangles <= 9, "split unexpectedly retained rank eleven")
    return BASE.Bound(Fraction(0), True, f"conditional rank-{triangles + 1}>0")


def tpp_component_bound(tree, component):
    cycles, internal_cuts, adjacency = component
    triangle_set = {cycle for cycle in cycles if tree.colors[cycle] == "T"}
    triangles = len(triangle_set)
    pentagons = len(cycles) - triangles
    rank = len(cycles)
    require(pentagons in (0, 1, 2), "component has invalid pentagon count")
    if pentagons == 0:
        value, strict = triangle_bound(triangles)
        return BASE.Bound(value, strict, f"A_{triangles}")
    if rank == 1:
        return BASE.Bound(Fraction(-1, 4), True, "P>-1/4")
    if (triangles, pentagons) == (1, 1):
        return BASE.Bound(Fraction(3, 4), True, "TP>3/4")
    if (triangles, pentagons) == (0, 2):
        return BASE.Bound(Fraction(0), True, "PP>0")
    if (triangles, pentagons) == (2, 1) and any(
        triangle_set <= set(adjacency[cut]) for cut in internal_cuts
    ):
        return BASE.Bound(Fraction(7, 4), True, "shared-cut TTP>7/4")
    if (triangles, pentagons) == (1, 2):
        return BASE.Bound(Fraction(3, 2), True, "TPP>3/2")
    if rank == 3:
        return BASE.Bound(Fraction(0), False, "rank-3>=0")
    if (triangles, pentagons) == (3, 1) and any(
        len(triangle_set & set(adjacency[cut])) >= 2 for cut in internal_cuts
    ):
        return BASE.Bound(Fraction(1), True, "shared-pair T^3P>1")
    require(4 <= rank <= 10, f"unsupported mixed component rank {rank}")
    return BASE.Bound(Fraction(0), True, f"conditional rank-{rank}>0")


def validate_classes(classes, colors, q_cap, expected_digest):
    signatures = set()
    expected_colors = Counter(colors)
    require(classes, "canonical generator returned no classes")
    require(
        tuple(signature for signature, _ in classes)
        == tuple(sorted(signature for signature, _ in classes)),
        "canonical classes are not signature-sorted",
    )
    for signature, tree in classes:
        require(signature not in signatures, f"duplicate signature {signature}")
        signatures.add(signature)
        require(signature == BASE.signature(tree), f"noncanonical representative {signature}")
        require(Counter(tree.colors) == expected_colors, "wrong cycle colors")
        adjacency = BASE.adjacency(tree)
        require(len(tree.edges) == len(adjacency) - 1, "incidence graph is not a tree")
        seen = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        require(len(seen) == len(adjacency), "incidence graph is disconnected")
        cycle_count = len(tree.colors)
        for cut in range(cycle_count, len(adjacency)):
            require(len(adjacency[cut]) >= 2, "degree-one cut node")
            require(all(cycle < cycle_count for cycle in adjacency[cut]), "cut-cut edge")
        for cycle, color in enumerate(tree.colors):
            capacity = q_cap if color == "Q" else BASE.CAPACITY[color]
            require(1 <= len(adjacency[cycle]) <= capacity, "cycle capacity violation")
            require(all(cut >= cycle_count for cut in adjacency[cycle]), "cycle-cycle edge")
    require(
        signature_digest(signature for signature, _ in classes) == expected_digest,
        "canonical signature digest changed",
    )


def exact_census(colors, q_cap, bound_function, expected_digest):
    colors = tuple(sorted(colors))
    classes = BASE.enumerate_colors(colors, q_cap)
    validate_classes(classes, colors, q_cap, expected_digest)
    totals = Counter()
    safe = Counter()
    unresolved = []
    for signature, tree in classes:
        cuts = BASE.cut_count(tree)
        totals[cuts] += 1
        certificates = [
            BASE.split_certificate(tree, cycle, bound_function)
            for cycle in range(len(tree.colors))
        ]
        if any(certificate is not None for certificate in certificates):
            safe[cuts] += 1
        else:
            unresolved.append((cuts, signature, BASE.cut_profile(tree), tree))
    unresolved.sort(key=lambda row: (row[0], row[1]))
    require(sum(totals.values()) == len(classes), "census total mismatch")
    require(sum(safe.values()) + len(unresolved) == len(classes), "classification mismatch")
    return totals, safe, unresolved


def check_equal(actual, expected, label):
    require(actual == expected, f"{label}: expected {expected!r}, got {actual!r}")


def new_router_audit(unresolved):
    matches = [row for row in unresolved if row[1] == NEW_ROUTER]
    require(len(matches) == 1, "new router signature is absent or duplicated")
    cuts, _, _, tree = matches[0]
    require(cuts == 4, "new router must have four cut nodes")
    adjacency = BASE.adjacency(tree)
    candidates = [
        cycle
        for cycle, color in enumerate(tree.colors)
        if color == "P" and len(adjacency[cycle]) == 4
    ]
    require(len(candidates) == 1, "new obstruction lacks a unique degree-four P router")
    require(len(tree.colors) == 11, "new router must have eleven cycle nodes")
    require(len(adjacency) == 15, "new router must have fifteen incidence vertices")
    require(len(tree.edges) == 14, "new router must have fourteen incidence edges")
    components = BASE.components_after_split(tree, candidates[0])
    profiles = sorted(
        tuple(sorted(Counter(tree.colors[cycle] for cycle in component[0]).items()))
        for component in components
    )
    expected = sorted([(("P", 1),), (("T", 1),), (("T", 1),), (("T", 7),)])
    check_equal(profiles, expected, "new router branch profiles")
    sizes = (len(tree.colors), cuts, len(adjacency), len(tree.edges))
    branch_ranks = tuple(sum(count for _, count in profile) for profile in profiles)
    return sizes, branch_ranks, profiles


def display_partitions(name, result):
    all_rows, proper_rows, residual = result
    print(
        f"{name} partitions: total={len(all_rows)} proper={len(proper_rows)} "
        f"direct={len(proper_rows) - len(residual)} structural={len(residual)}"
    )
    for row in residual:
        print("  structural", row)


def display_census(name, result):
    totals, safe, unresolved = result
    print(f"{name} all: {dict(sorted(totals.items()))} = {sum(totals.values())}")
    print(f"{name} SAFE: {dict(sorted(safe.items()))} = {sum(safe.values())}")
    print(f"{name} exceptions: {dict(sorted(Counter(row[0] for row in unresolved).items()))} = {len(unresolved)}")
    for cuts, signature, _, _ in unresolved:
        print(f"  c={cuts} signature={signature}")


def validate_residuals(result, expected_signatures, digest_key):
    totals, safe, unresolved = result
    signatures = tuple(row[1] for row in unresolved)
    require(
        set(signatures) == expected_signatures,
        "residual canonical signature set changed",
    )
    require(
        signature_digest(signatures) == EXPECTED_RESIDUAL_DIGESTS[digest_key],
        "residual canonical signature digest changed",
    )
    expected_safe = Counter(totals)
    expected_safe.subtract(Counter(row[0] for row in unresolved))
    expected_safe += Counter()
    require(safe == expected_safe, "SAFE cut-count ledger is incomplete")


def main():
    print("CONDITIONAL INPUT: rank-ten cactus theorem; this is not a theorem checker")
    print("Sharp-DNN rank-eleven residuals: T^10Q and T^9PP")
    partition_results = {
        "T^10Q": partition_audit(10, 1, tq_profile_bound),
        "T^9PP": partition_audit(9, 2, tpp_profile_bound),
    }
    for name, result in partition_results.items():
        observed = (
            len(result[0]),
            len(result[1]),
            len(result[1]) - len(result[2]),
            len(result[2]),
        )
        check_equal(observed, EXPECTED_PARTITIONS[name], f"{name} partitions")
        display_partitions(name, result)

    regimes = (
        ("q=3", 3),
        ("q=4", 4),
        ("q=5", 5),
        ("q=6", 6),
        ("q=7", 7),
        ("q=8", 8),
        ("q=9", 9),
        ("q=10", 10),
        ("hostile q>=11", 10),
    )
    for label, capacity in regimes:
        result = exact_census(
            ("T",) * 10 + ("Q",),
            capacity,
            lambda tree, component, label=label: tq_component_bound(label, tree, component),
            EXPECTED_CLASS_DIGESTS[("TQ", capacity)],
        )
        check_equal(result[0], Counter(EXPECTED_T10Q[label]), f"T^10Q {label} totals")
        expected = {T10Q_COMMON} if label in {"q=3", "q=4", "q=6", "q=8", "q=10"} else T10Q_HOSTILE
        validate_residuals(
            result,
            expected,
            "common" if len(expected) == 1 else "hostile",
        )
        display_census(f"T^10Q {label}", result)

    tpp_result = exact_census(
        ("T",) * 9 + ("P",) * 2,
        0,
        tpp_component_bound,
        EXPECTED_CLASS_DIGESTS[("TPP", 0)],
    )
    check_equal(tpp_result[0], Counter(EXPECTED_T9PP), "T^9PP totals")
    validate_residuals(tpp_result, T9PP_EXCEPTIONS, "TPP")
    check_equal(
        Counter(row[0] for row in tpp_result[2]),
        Counter({1: 1, 2: 2, 3: 4, 4: 2, 5: 1}),
        "T^9PP exception cuts",
    )
    sizes, branch_ranks, profiles = new_router_audit(tpp_result[2])
    display_census("T^9PP", tpp_result)
    print(f"new minimal degree-four P-router sizes (cycles,cuts,vertices,edges): {sizes}")
    print(f"new minimal degree-four P-router branch ranks: {branch_ranks}")
    print(f"new minimal degree-four P-router profiles: {profiles}")
    print("PASS: all frozen conditional frontier checks succeeded under fail-closed guards")


if __name__ == "__main__":
    main()
