#!/usr/bin/env python3
"""Independent finite audits for the k=4 placement/refinement partition."""
from itertools import combinations

from m9_k4_placements import B
from m9_k4_shapes import P


def production_keys():
    for rho in range(3):
        for shape, profile in P.items():
            n2 = profile[0]
            for epsilon in (0, 1):
                for alpha in range(n2 - epsilon + 1):
                    beta = n2 - epsilon - alpha
                    yield rho, shape, alpha, beta, epsilon


def direct_coordinates(kset, holes, marked):
    eta = sum({u, v} <= kset for u, v in holes)
    lam = len(kset & marked)
    return len(kset), eta, lam


def main():
    keys = list(production_keys())
    assert len(keys) == 165 and len(set(keys)) == 165
    by_parent = {}
    for rho, shape, alpha, beta, epsilon in keys:
        by_parent.setdefault((rho, shape), 0)
        by_parent[rho, shape] += 1
    for rho in range(3):
        for shape, profile in P.items():
            assert by_parent[rho, shape] == 2 * profile[0] + 1

    # Exhaustively audit the dynamic coordinates independently of the CNF
    # implementation. K has size five or six; all B-internal four-hole sets and
    # all marked subsets are used. This tests the dynamic coordinate partition,
    # not realizability of a complete four-hole graph on T.
    pairs = list(combinations(B, 2))
    seen = set()
    cases = 0
    for kappa in (5, 6):
        for kt in combinations(B, kappa):
            kset = set(kt)
            for holes in combinations(pairs, 4):
                for mask in range(1 << len(B)):
                    marked = {b for i, b in enumerate(B) if mask >> i & 1}
                    coord = direct_coordinates(kset, holes, marked)
                    assert coord[0] == kappa
                    assert 0 <= coord[1] <= 4
                    lo = max(0, len(marked) - (7 - kappa))
                    hi = min(len(marked), kappa)
                    assert lo <= coord[2] <= hi
                    seen.add(coord)
                    cases += 1
    assert {(k, e) for k, e, _ in seen} == {
        (k, e) for k in (5, 6) for e in range(5)
    }
    print(f"PASS placements={len(keys)} parents={len(by_parent)} dynamic_cases={cases}")


if __name__ == "__main__":
    main()
