#!/usr/bin/env python3
"""Dependency-free audit aid for the family-S h(T)=0 human proof.

This checks exact integer identities and finite local logic used in the proof.
It is not an order-18 graph search and is not a certificate for the upstream
vertex-minimal-then-arc-minimal normal-form reduction.
"""

from collections import Counter
from itertools import product
from math import comb


def require(condition, message):
    """Fail closed under both normal and optimized Python execution."""
    if not condition:
        raise SystemExit(f"FAIL {message}")


def exact_second(vertices, arcs, source):
    """Return the exact second out-neighborhood from an explicit arc set."""
    first = {v for v in vertices if (source, v) in arcs}
    two_walk_endpoints = {
        z for y in first for z in vertices if (y, z) in arcs
    }
    return two_walk_endpoints - first - {source}


def integer_partitions(total, maximum=None):
    """Yield positive integer partitions in nonincreasing order."""
    if total == 0:
        yield ()
        return
    maximum = total if maximum is None else min(maximum, total)
    for head in range(maximum, 0, -1):
        for tail in integer_partitions(total - head, head):
            yield (head,) + tail


def check_degree_cap_and_census():
    n = 18
    holes = 7
    arcs = comb(n, 2) - holes
    excess = arcs - 8 * n
    require((arcs, excess) == (146, 2), "seven-hole arc/excess identity")

    # Minimum degree eight and arc count alone permit either one excess of two
    # or two excesses of one.  The degree cap is a necessary separate input.
    patterns = set(integer_partitions(excess))
    require(patterns == {(2,), (1, 1)}, "unbounded excess partitions")

    # Recheck the elementary implication of the committed deficit bound.  For
    # each possible badness deficit mu in {1,2}, disjointness says
    # 1+d+(d-mu)<=18.  No integer d>=10 survives.
    survivors = {
        mu: [d for d in range(8, 18) if 1 + d + (d - mu) <= n]
        for mu in (1, 2)
    }
    require(survivors == {1: [8, 9], 2: [8, 9]}, "deficit-to-degree cap")
    bounded = {p for p in patterns if max(p, default=0) <= 1}
    require(bounded == {(1, 1)}, "bounded excess census")
    print(
        "PASS degree cap/census: mu<=2 implies Delta+<=9; "
        "excess 2 then forces 9,9,8^16"
    )


def check_exact_second_semantics():
    vertices = {"a", "b", "c"}
    path = {("a", "b"), ("b", "c")}
    require(exact_second(vertices, path, "a") == {"c"}, "path exact-second endpoint")

    # A direct outneighbor is excluded even when a two-walk also reaches it.
    path_plus_direct = path | {("a", "c")}
    require(exact_second(vertices, path_plus_direct, "a") == set(), "direct endpoint exclusion")

    # In the root-layer situation c is outside N+(w) and N++(w), so w->a->c
    # is impossible.  Exhaust the two remaining pair states, including holes.
    feasible = 0
    for wc, ac in product(range(3), repeat=2):
        # 0=hole, 1=first label -> second, 2=reverse.
        arcs = {("w", "a")}
        if wc == 1:
            arcs.add(("w", "c"))
        elif wc == 2:
            arcs.add(("c", "w"))
        if ac == 1:
            arcs.add(("a", "c"))
        elif ac == 2:
            arcs.add(("c", "a"))
        if "c" in {v for u, v in arcs if u == "w"}:
            continue
        if "c" in exact_second({"w", "a", "c"}, arcs, "w"):
            continue
        feasible += 1
        require(("a", "c") not in arcs, "root-layer A-to-C barrier")
    require(feasible > 0, "nonvacuous root-layer enumeration")
    print("PASS exact-second semantics and root-layer A-not-to-C barrier")


def check_transport_and_common_dominator():
    u_scores = [8, 9, 9] + [8] * 6
    require(len(u_scores) == 9 and sum(u_scores) == 74, "U score sum")
    t_score_sum = comb(16, 2)
    b_t_score_sum = t_score_sum - sum(u_scores)
    e_b_c = 7 * 8 - b_t_score_sum
    require((t_score_sum, b_t_score_sum, e_b_c) == (120, 46, 10), "score transport")

    vectors = [x for x in product(range(3), repeat=7) if sum(x) == 10]
    distributions = Counter(
        (x.count(2), x.count(1), x.count(0)) for x in vectors
    )
    require(
        distributions == Counter(
            {(3, 4, 0): 35, (4, 2, 1): 105, (5, 0, 2): 21}
        ),
        "common-dominator distribution",
    )
    require(len(vectors) == 161, "B-to-C vector count")
    require(min(x.count(2) for x in vectors) == 3, "common-dominator lower bound")

    # A B vertex with x outgoing C-arcs has T-score 8-x, so only r,q can
    # have T-score at least nine in every transport row.
    for vector in vectors:
        t_scores = sorted(u_scores + [8 - x for x in vector])
        require(
            [score for score in t_scores if score >= 9] == [9, 9],
            "only two T-scores at least nine",
        )
    print(
        "PASS score transport: sum_U=74, sum_B(T)=46, e(B,C)=10; "
        "all 161 vectors have a common C-dominator"
    )


def check_inaccessible_tournament_inneighbor():
    # Labels: a->x_i, z->a, and each x_i--z pair is oriented.  A mask bit
    # means x_i->z and therefore creates a->x_i->z.
    vertices = {"a", "z"} | {f"x{i}" for i in range(8)}
    inaccessible_masks = []
    for mask in range(1 << 8):
        arcs = {("z", "a")} | {("a", f"x{i}") for i in range(8)}
        for i in range(8):
            x = f"x{i}"
            arcs.add((x, "z") if (mask >> i) & 1 else ("z", x))
        if "z" not in exact_second(vertices, arcs, "a"):
            inaccessible_masks.append(mask)
            require(
                all(("z", f"x{i}") in arcs for i in range(8)),
                "inaccessible vertex domination",
            )
            require(
                len({v for u, v in arcs if u == "z"}) == 9,
                "inaccessible vertex score",
            )
    require(inaccessible_masks == [0], "unique inaccessible local orientation")
    print(
        "PASS inaccessible-inneighbor lemma: the unique local orientation "
        "dominates a and all eight outneighbors"
    )


def check_saturation_high_arc_and_terminal_count():
    # Seven T-inneighbors; only bits 0,1 (r,q) may be inaccessible.  The two C
    # endpoints are already exact second neighbors; strict badness caps d++ at 7.
    feasible_inaccessible = []
    for mask in range(1 << 7):
        if mask & ~0b11:
            continue
        exact_t_seconds = 7 - mask.bit_count()
        if exact_t_seconds + 2 <= 7:
            feasible_inaccessible.append(mask)
    require(feasible_inaccessible == [0b11], "badness saturation to both highs")

    x = {f"x{i}" for i in range(8)}
    forced_high_targets = {"a"} | x
    require(len(forced_high_targets) == 9, "nine forced high targets")
    require(len(forced_high_targets | {"r"}) == 10, "q-to-r tenth target")
    require(len(forced_high_targets | {"q"}) == 10, "r-to-q tenth target")

    forced_b_targets = {"w"} | {f"a{i}" for i in range(6)} | {"c0", "c1"}
    require(len(forced_b_targets) == 1 + 6 + 2 == 9, "terminal nine targets")

    # Boundary controls: one external endpoint, non-strict badness, or one
    # fewer ordinary A vertex no longer forces the corresponding contradiction.
    require(
        [k for k in range(3) if (7 - k) + 1 <= 7] == [1, 2],
        "one-endpoint hostile boundary",
    )
    require(
        [k for k in range(3) if (7 - k) + 2 <= 8] == [1, 2],
        "nonstrict-badness hostile boundary",
    )
    require(1 + 5 + 2 == 8, "terminal-count hostile boundary")
    print(
        "PASS saturation/high arc/terminal count: inaccessible={r,q}, "
        "high tail has 10 targets, common dominator has 9"
    )


def main():
    check_degree_cap_and_census()
    check_exact_second_semantics()
    check_transport_and_common_dominator()
    check_inaccessible_tournament_inneighbor()
    check_saturation_high_arc_and_terminal_count()
    print(
        "PASS family-S h(T)=0 local human-proof audit "
        "(not an upstream normal-form certificate)"
    )


if __name__ == "__main__":
    main()
