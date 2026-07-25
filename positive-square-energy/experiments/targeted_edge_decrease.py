#!/usr/bin/env python3
"""Heuristic search for a connected simple threshold-crossing pair.

The target is a connected simple graph G and a nonedge e such that
s+(G)-n >= 0 but s+(G+e)-n < 0. Seeds include connectedizations of the exact
disconnected D/cycle construction and random sparse graphs. Moves rewire edges
but reject every disconnected proposal. Output is numerical discovery data,
not an exact certificate.
"""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass

import networkx as nx
import numpy as np


D_GRAPH6 = b"HQzV]zn"
D_TARGET = (2, 3)


@dataclass(frozen=True)
class Candidate:
    g6: str
    u: int
    v: int
    n: int
    m: int
    before: float
    after: float

    @property
    def decrease(self) -> float:
        return self.before - self.after

    @property
    def before_slack(self) -> float:
        return self.before - self.n

    @property
    def after_slack(self) -> float:
        return self.after - self.n

    @property
    def crossing(self) -> bool:
        return self.before_slack >= 0.0 and self.after_slack < 0.0

    @property
    def boundary_error(self) -> float:
        return max(-self.before_slack, self.after_slack)


def splus(g: nx.Graph, extra: tuple[int, int] | None = None) -> float:
    a = nx.to_numpy_array(g, nodelist=range(len(g)), dtype=float)
    if extra is not None:
        u, v = extra
        a[u, v] = a[v, u] = 1.0
    eig = np.linalg.eigvalsh(a)
    pos = eig[eig > 0.0]
    return float(pos @ pos)


def evaluate(g: nx.Graph, edge: tuple[int, int], before: float | None = None) -> Candidate:
    u, v = sorted(edge)
    before = splus(g) if before is None else before
    after = splus(g, (u, v))
    g6 = nx.to_graph6_bytes(g, header=False).strip().decode("ascii")
    return Candidate(g6, u, v, len(g), g.number_of_edges(), before, after)


def quality(c: Candidate) -> tuple[bool, bool, float, float]:
    """Crossing first; otherwise approach the boundary without losing a drop."""
    return c.crossing, c.decrease > 0.0, -c.boundary_error, c.decrease


def better(c: Candidate, incumbent: Candidate) -> bool:
    if c.crossing != incumbent.crossing:
        return c.crossing
    if c.crossing:
        return (c.after_slack, -c.decrease) < (incumbent.after_slack, -incumbent.decrease)
    if (c.decrease > 0.0) != (incumbent.decrease > 0.0):
        return c.decrease > 0.0
    return (-c.boundary_error, c.decrease) > (-incumbent.boundary_error, incumbent.decrease)


def anneal_score(c: Candidate) -> float:
    # The large first term prevents a discovered crossing from being discarded;
    # the second retains edge decrease while the boundary error is optimized.
    return ((20.0 if c.crossing else 0.0) + (10.0 if c.decrease > 0.0 else 0.0)
            - c.boundary_error + 0.01 * c.decrease)


def random_sparse(n: int, rng: random.Random) -> nx.Graph:
    g = nx.random_labeled_tree(n, seed=rng.randrange(1 << 63))
    excess = rng.randint(1, max(2, min(n // 3, 16)))
    missing = list(nx.non_edges(g))
    rng.shuffle(missing)
    g.add_edges_from(missing[:excess])
    return g


def disconnected_x_blocks(n: int) -> list[nx.Graph]:
    """Truncate the exact D + 117 C5 + C13 construction to order n."""
    if n < 9:
        raise ValueError("D motif requires n >= 9")
    blocks = [nx.convert_node_labels_to_integers(nx.from_graph6_bytes(D_GRAPH6))]
    remaining = n - 9
    if remaining >= 13:
        blocks.append(nx.cycle_graph(13))
        remaining -= 13
    while remaining >= 5:
        blocks.append(nx.cycle_graph(5))
        remaining -= 5
    if remaining:
        blocks.append(nx.path_graph(remaining))
    return blocks


def connectedized_x(n: int, rng: random.Random, splice: bool) -> nx.Graph:
    blocks = disconnected_x_blocks(n)
    g = nx.convert_node_labels_to_integers(blocks[0])
    for block in blocks[1:]:
        h = nx.convert_node_labels_to_integers(block, first_label=len(g))
        old_nodes = list(g)
        new_nodes = list(h)
        g = nx.compose(g, h)
        joined = False
        if splice and h.number_of_edges() > 0:
            forbidden = {tuple(sorted(D_TARGET))}
            nonbridges = [e for e in old_nodes_edges(g, old_nodes)
                          if tuple(sorted(e)) not in forbidden]
            rng.shuffle(nonbridges)
            h_edges = list(h.edges())
            rng.shuffle(h_edges)
            for a, b in nonbridges:
                for c, d in h_edges:
                    q = g.copy()
                    q.remove_edges_from(((a, b), (c, d)))
                    q.add_edges_from(((a, c), (b, d)))
                    if nx.is_connected(q):
                        g = q
                        joined = True
                        break
                if joined:
                    break
        if not joined:
            # Keep the D nonedge's local spectral environment intact when
            # possible; randomized attachment vertices supply the restarts.
            old_choices = [v for v in old_nodes if v not in D_TARGET] or old_nodes
            g.add_edge(rng.choice(old_choices), rng.choice(new_nodes))
    assert len(g) == n and nx.is_connected(g) and not g.has_edge(*D_TARGET)
    return g


def old_nodes_edges(g: nx.Graph, nodes: list[int]) -> list[tuple[int, int]]:
    allowed = set(nodes)
    sub = g.subgraph(nodes)
    bridges = {tuple(sorted(e)) for e in nx.bridges(sub)} if len(sub) > 1 else set()
    return [e for e in sub.edges() if tuple(sorted(e)) not in bridges
            and e[0] in allowed and e[1] in allowed]


def best_target(g: nx.Graph, rng: random.Random, sample: int) -> Candidate:
    nonedges = list(nx.non_edges(g))
    if len(nonedges) > sample:
        nonedges = rng.sample(nonedges, sample)
    before = splus(g)
    return max((evaluate(g, e, before) for e in nonedges), key=quality)


def switched(g: nx.Graph, forbidden: tuple[int, int], rng: random.Random) -> nx.Graph | None:
    edges = list(g.edges())
    for _ in range(32):
        (a, b), (c, d) = rng.sample(edges, 2)
        if len({a, b, c, d}) != 4:
            continue
        proposal = ((a, c), (b, d)) if rng.random() < 0.5 else ((a, d), (b, c))
        proposal = tuple(tuple(sorted(e)) for e in proposal)
        if forbidden in proposal or proposal[0] == proposal[1]:
            continue
        if any(g.has_edge(*e) for e in proposal):
            continue
        h = g.copy()
        h.remove_edges_from(((a, b), (c, d)))
        h.add_edges_from(proposal)
        if nx.is_connected(h):
            return h
    return None


def rewired(g: nx.Graph, forbidden: tuple[int, int], rng: random.Random) -> nx.Graph | None:
    """Relocate one edge, allowing degree changes while preserving m and connectivity."""
    edges = list(g.edges())
    for _ in range(32):
        removed = rng.choice(edges)
        h = g.copy()
        h.remove_edge(*removed)
        nonedges = [e for e in nx.non_edges(h) if tuple(sorted(e)) != forbidden]
        if not nonedges:
            return None
        h.add_edge(*rng.choice(nonedges))
        if nx.is_connected(h):
            return h
    return None


def anneal(
    g: nx.Graph,
    initial: Candidate,
    rng: random.Random,
    steps: int,
    target_sample: int,
) -> tuple[nx.Graph, Candidate]:
    current_g, current = g, initial
    best_g, best = g.copy(), current
    t0, t1 = 0.12, 2e-5
    for step in range(steps):
        temperature = t0 * (t1 / t0) ** (step / max(steps - 1, 1))
        r = rng.random()
        if r < 0.12:
            proposal_g = current_g
            proposal = best_target(current_g, rng, target_sample)
        else:
            forbidden = (current.u, current.v)
            proposal_g = (switched(current_g, forbidden, rng) if r < 0.56
                          else rewired(current_g, forbidden, rng))
            if proposal_g is None:
                continue
            proposal = evaluate(proposal_g, forbidden)
        delta = anneal_score(proposal) - anneal_score(current)
        if delta >= 0.0 or rng.random() < math.exp(max(-700.0, delta / temperature)):
            current_g, current = proposal_g, proposal
        if better(proposal, best):
            best_g, best = proposal_g.copy(), proposal
    return best_g, best


def seed_graph(n: int, lane: str, rng: random.Random) -> tuple[nx.Graph, tuple[int, int] | None]:
    if lane == "D-BRIDGE":
        return connectedized_x(n, rng, splice=False), D_TARGET
    if lane == "D-SPLICE":
        return connectedized_x(n, rng, splice=True), D_TARGET
    return random_sparse(n, rng), None


def print_candidate(lane: str, c: Candidate) -> None:
    print(
        f"{lane}\tn={c.n}\tm={c.m}\tcrossing={int(c.crossing)}"
        f"\tbefore={c.before:.17g}\tafter={c.after:.17g}"
        f"\tbefore_slack={c.before_slack:.17g}\tafter_slack={c.after_slack:.17g}"
        f"\tdecrease={c.decrease:.17g}\terror={c.boundary_error:.17g}"
        f"\tedge={c.u},{c.v}\tg6={c.g6}",
        flush=True,
    )


def high_precision_values(c: Candidate, dps: int) -> tuple[str, str, str, str]:
    import mpmath as mp

    mp.mp.dps = dps
    g = nx.from_graph6_bytes(c.g6.encode("ascii"))
    a = mp.matrix(nx.to_numpy_array(g, nodelist=range(c.n), dtype=int).tolist())
    eig = mp.eigsy(a, eigvals_only=True)
    before = mp.fsum(x * x for x in eig if x > 0)
    a[c.u, c.v] = a[c.v, c.u] = 1
    eig_after = mp.eigsy(a, eigvals_only=True)
    after = mp.fsum(x * x for x in eig_after if x > 0)
    return tuple(mp.nstr(x, dps) for x in (
        before, after, before - c.n, after - c.n))


def print_high_precision(lane: str, c: Candidate, dps: int) -> None:
    before, after, before_slack, after_slack = high_precision_values(c, dps)
    print(
        f"HIGH_PRECISION\tlane={lane}\tdps={dps}\tbefore={before}\tafter={after}"
        f"\tbefore_slack={before_slack}\tafter_slack={after_slack}"
        f"\tedge={c.u},{c.v}\tg6={c.g6}",
        flush=True,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=20)
    ap.add_argument("--nmax", type=int, default=300)
    ap.add_argument("--nstep", type=int, default=1)
    ap.add_argument("--seed", type=int, default=20260724)
    ap.add_argument("--restarts", type=int, default=1)
    ap.add_argument("--steps", type=int, default=800)
    ap.add_argument("--target-sample", type=int, default=16)
    ap.add_argument("--verify-dps", type=int, default=0,
                    help="recompute the top candidate with mpmath at this precision")
    args = ap.parse_args()
    if not 20 <= args.nmin <= args.nmax <= 300:
        ap.error("require 20 <= nmin <= nmax <= 300")

    rng = random.Random(args.seed)
    global_best: list[tuple[str, Candidate]] = []
    for n in range(args.nmin, args.nmax + 1, args.nstep):
        for lane in ("D-BRIDGE", "D-SPLICE", "RANDOM"):
            lane_best: Candidate | None = None
            for _ in range(args.restarts):
                g, target = seed_graph(n, lane, rng)
                c = evaluate(g, target) if target is not None else best_target(
                    g, rng, args.target_sample)
                _, c = anneal(g, c, rng, args.steps, args.target_sample)
                global_best.append((lane, c))
                if lane_best is None or better(c, lane_best):
                    lane_best = c
            assert lane_best is not None
            print_candidate(lane, lane_best)

    print("TOP", flush=True)
    ranked = sorted(global_best, key=lambda item: quality(item[1]), reverse=True)
    for lane, c in ranked[:20]:
        print_candidate(lane, c)
    if args.verify_dps:
        print_high_precision(*ranked[0], args.verify_dps)


if __name__ == "__main__":
    main()
