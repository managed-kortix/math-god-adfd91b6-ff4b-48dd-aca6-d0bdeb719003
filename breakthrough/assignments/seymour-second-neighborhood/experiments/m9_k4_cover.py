#!/usr/bin/env python3
"""Deterministic missing-graph feasibility cover for all m=9,k=4 cells."""
import hashlib
import itertools
import sys

from m9_k4_shapes import P

EXPECTED_KEY_HASH = "51700d5bd4f592859442da60b83b9c49a434d9a31b09618bfe61b09326b61195"
EXPECTED_LEDGER_HASH = "9e8ebba3b2617beb5ee58c052e4f59a03abbb20a3a09f9d11c4ee6b2019f1cae"

SHAPES = {
    "c4": ((0, 1), (1, 2), (2, 3), (0, 3)),
    "paw": ((0, 1), (1, 2), (0, 2), (0, 3)),
    "p5": ((0, 1), (1, 2), (2, 3), (3, 4)),
    "triangle_edge": ((0, 1), (1, 2), (0, 2), (3, 4)),
    "fork": ((0, 1), (0, 2), (0, 3), (1, 4)),
    "k1_4": ((0, 1), (0, 2), (0, 3), (0, 4)),
    "p4_edge": ((0, 1), (1, 2), (2, 3), (4, 5)),
    "two_p3": ((0, 1), (1, 2), (3, 4), (4, 5)),
    "claw_edge": ((0, 1), (0, 2), (0, 3), (4, 5)),
    "p3_two_edges": ((0, 1), (1, 2), (3, 4), (5, 6)),
    "four_matching": ((0, 1), (2, 3), (4, 5), (6, 7)),
}


def marked(edges):
    deg = [0] * (1 + max(max(e) for e in edges))
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    return {v for v, d in enumerate(deg) if d >= 2}, len(deg)


def feasible_coordinates(shape, kappa):
    edges = SHAPES[shape]
    M, order = marked(edges)
    out = set()
    # Colors are root, A', B\K, K. Capacities are 1,7,7-kappa,kappa.
    for colors in itertools.product(range(4), repeat=order):
        sizes = tuple(colors.count(c) for c in range(4))
        if any(x > cap for x, cap in zip(sizes, (1, 7, 7-kappa, kappa))):
            continue
        alpha = sum(colors[v] == 1 for v in M)
        beta = sum(colors[v] in (2, 3) for v in M)
        epsilon = sum(colors[v] == 0 for v in M)
        lam = sum(colors[v] == 3 for v in M)
        eta = sum(colors[u] == colors[v] == 3 for u, v in edges)
        out.add((alpha, beta, epsilon, eta, lam))
    return out


def terminal_keys():
    for rho in range(3):
        for shape, profile in P.items():
            n2 = profile[0]
            for epsilon in (0, 1):
                for alpha in range(n2 - epsilon + 1):
                    beta = n2 - epsilon - alpha
                    for kappa in (5, 6):
                        lo = max(0, beta - (7-kappa))
                        hi = min(beta, kappa)
                        for eta in range(5):
                            for lam in range(lo, hi + 1):
                                key = (f"m9-k4/rho={rho}/shape={shape}/alpha={alpha}/"
                                       f"beta={beta}/epsilon={epsilon}/kappa={kappa}/"
                                       f"eta={eta}/lambda={lam}")
                                yield key, (alpha, beta, epsilon, eta, lam) in feasible_coordinates(shape, kappa)


def main():
    rows = sorted(terminal_keys())
    if len(rows) != 2925 or len({key for key, _ in rows}) != 2925:
        raise AssertionError("terminal hierarchy is not a 2925-key partition")
    keys = "".join(key + "\n" for key, _ in rows).encode("ascii")
    ledger = "".join(f"{key}\t{'FEASIBLE' if ok else 'EMPTY'}\n" for key, ok in rows).encode("ascii")
    feasible = sum(ok for _, ok in rows)
    if feasible != 1140:
        raise AssertionError(f"expected 1140 feasible cells, got {feasible}")
    if hashlib.sha256(keys).hexdigest() != EXPECTED_KEY_HASH:
        raise AssertionError("canonical key digest changed")
    if hashlib.sha256(ledger).hexdigest() != EXPECTED_LEDGER_HASH:
        raise AssertionError("canonical ledger digest changed")
    if len(sys.argv) == 2:
        with open(sys.argv[1], "wb") as f:
            f.write(ledger)
    elif len(sys.argv) != 1:
        raise SystemExit("usage: m9_k4_cover.py [ledger.txt]")
    print(f"keys={len(rows)} feasible={feasible} empty={len(rows)-feasible}")
    print(f"key_sha256={hashlib.sha256(keys).hexdigest()}")
    print(f"ledger_sha256={hashlib.sha256(ledger).hexdigest()}")


if __name__ == "__main__":
    main()
