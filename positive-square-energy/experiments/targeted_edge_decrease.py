#!/usr/bin/env python3
"""Targeted heuristic search for an edge-addition threshold crossing.

The search has two lanes.  The sparse lane starts with connected bicyclic
graphs (m=n+1) and uses degree-preserving 2-switches.  The dense lane first
anneals a graph/nonedge pair for a decrease and then greedily removes edges,
with short 2-switch anneals between removals.  Output is numerical discovery
data, not a proof; use exact_certify.py on both members of any claimed pair.
"""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass

import networkx as nx
import numpy as np


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
    def surplus(self) -> float:
        return self.before - self.n

    @property
    def after_slack(self) -> float:
        return self.after - self.n


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


def objective(c: Candidate, surplus_weight: float) -> float:
    if c.surplus < -1e-8:
        return -1e4 + 100.0 * c.surplus
    crossing_bonus = 1e3 if c.after_slack < -1e-8 else 0.0
    return crossing_bonus + c.decrease - surplus_weight * max(c.surplus, 0.0)


def random_bicyclic(n: int, rng: random.Random) -> nx.Graph:
    g = nx.random_labeled_tree(n, seed=rng.randrange(1 << 63))
    missing = list(nx.non_edges(g))
    g.add_edge(*missing.pop(rng.randrange(len(missing))))
    missing = [(u, v) for u, v in missing if not g.has_edge(u, v)]
    g.add_edge(*missing[rng.randrange(len(missing))])
    return g


def handcuff(n: int) -> nx.Graph:
    a = max(3, n // 2)
    if a % 2 == 0:
        a -= 1
    b = n - a
    if b < 3:
        a, b = n - 3, 3
    g = nx.disjoint_union(nx.cycle_graph(a), nx.cycle_graph(b))
    g.add_edge(0, a)
    return g


def best_target(g: nx.Graph, rng: random.Random, sample: int = 0) -> Candidate:
    nonedges = list(nx.non_edges(g))
    if sample and len(nonedges) > sample:
        nonedges = rng.sample(nonedges, sample)
    before = splus(g)
    return max((evaluate(g, e, before) for e in nonedges), key=lambda c: c.decrease)


def switched(g: nx.Graph, forbidden: tuple[int, int], rng: random.Random) -> nx.Graph | None:
    edges = list(g.edges())
    for _ in range(24):
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


def anneal(
    g: nx.Graph,
    initial: Candidate,
    rng: random.Random,
    steps: int,
    surplus_weight: float,
) -> tuple[nx.Graph, Candidate, Candidate]:
    current_g, current = g, initial
    best = current
    best_g = g.copy()
    t0, t1 = 0.08, 2e-5
    for step in range(steps):
        temperature = t0 * (t1 / t0) ** (step / max(steps - 1, 1))
        if rng.random() < 0.16:
            proposal_g = current_g
            proposal = best_target(current_g, rng, sample=12)
        else:
            proposal_g = switched(current_g, (current.u, current.v), rng)
            if proposal_g is None:
                continue
            proposal = evaluate(proposal_g, (current.u, current.v))
        delta = objective(proposal, surplus_weight) - objective(current, surplus_weight)
        if delta >= 0.0 or rng.random() < math.exp(max(-700.0, delta / temperature)):
            current_g, current = proposal_g, proposal
        best_key = (best.after_slack < 0.0, objective(best, surplus_weight), best.decrease)
        new_key = (proposal.after_slack < 0.0, objective(proposal, surplus_weight), proposal.decrease)
        if new_key > best_key:
            best, best_g = proposal, proposal_g.copy()
    return best_g, best, current


def sparse_lane(n: int, rng: random.Random, restarts: int, steps: int) -> list[Candidate]:
    found: list[Candidate] = []
    for restart in range(restarts):
        g = handcuff(n) if restart == 0 else random_bicyclic(n, rng)
        c = best_target(g, rng)
        _, best, _ = anneal(g, c, rng, steps, surplus_weight=0.18)
        found.append(best)
    return found


def dense_lane(n: int, rng: random.Random, steps: int, prune_sample: int) -> list[Candidate]:
    p = rng.uniform(0.28, 0.72)
    g = nx.gnp_random_graph(n, p, seed=rng.randrange(1 << 63))
    if not nx.is_connected(g):
        components = list(nx.connected_components(g))
        for left, right in zip(components, components[1:]):
            g.add_edge(rng.choice(tuple(left)), rng.choice(tuple(right)))
    c = best_target(g, rng, sample=64)
    g, c, _ = anneal(g, c, rng, steps, surplus_weight=0.025)
    trail = [c]
    while g.number_of_edges() > n + 1 and c.decrease > 2e-8:
        removable = list(g.edges())
        rng.shuffle(removable)
        choices: list[tuple[float, nx.Graph, Candidate]] = []
        for edge in removable[:prune_sample]:
            h = g.copy()
            h.remove_edge(*edge)
            if not nx.is_connected(h) or h.has_edge(c.u, c.v):
                continue
            q = evaluate(h, (c.u, c.v))
            if q.surplus >= -1e-8 and q.decrease > 1e-9:
                choices.append((objective(q, 0.08), h, q))
        if not choices:
            break
        _, g, c = max(choices, key=lambda item: item[0])
        g, c, _ = anneal(g, c, rng, max(20, steps // 12), surplus_weight=0.08)
        trail.append(c)
    return trail


def print_candidate(lane: str, c: Candidate) -> None:
    print(
        f"{lane}\tn={c.n}\tm={c.m}\tD={c.decrease:.15g}"
        f"\tsurplus={c.surplus:.15g}\tafter_slack={c.after_slack:.15g}"
        f"\tedge={c.u},{c.v}\tg6={c.g6}",
        flush=True,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=10)
    ap.add_argument("--nmax", type=int, default=50)
    ap.add_argument("--seed", type=int, default=20260724)
    ap.add_argument("--sparse-restarts", type=int, default=3)
    ap.add_argument("--sparse-steps", type=int, default=1200)
    ap.add_argument("--dense-restarts", type=int, default=1)
    ap.add_argument("--dense-steps", type=int, default=900)
    ap.add_argument("--prune-sample", type=int, default=24)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    global_best: list[tuple[str, Candidate]] = []
    for n in range(args.nmin, args.nmax + 1):
        sparse = sparse_lane(n, rng, args.sparse_restarts, args.sparse_steps)
        sbest = max(sparse, key=lambda c: (c.after_slack < 0.0, c.decrease, -abs(c.surplus)))
        print_candidate("SPARSE", sbest)
        global_best.extend(("SPARSE", c) for c in sparse)
        for _ in range(args.dense_restarts):
            trail = dense_lane(n, rng, args.dense_steps, args.prune_sample)
            dbest = max(trail, key=lambda c: (c.after_slack < 0.0, c.decrease, -c.m))
            print_candidate("DENSE", dbest)
            print_candidate("PRUNED", trail[-1])
            global_best.extend(("DENSE", c) for c in trail)
    print("TOP")
    for lane, c in sorted(
        global_best,
        key=lambda item: (item[1].after_slack < 0.0, item[1].decrease, -item[1].after_slack),
        reverse=True,
    )[:20]:
        print_candidate(lane, c)


if __name__ == "__main__":
    main()
