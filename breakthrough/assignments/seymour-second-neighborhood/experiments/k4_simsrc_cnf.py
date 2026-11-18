#!/usr/bin/env python3
"""Deterministic CNF producer for the conditional rooted m=8, k=4 projection.

The graph T has labels

    v=0, r=1, A'={2,...,8}, K={9,...,14}, b0=15.

Only p=|P| in {6,7} is emitted: the separate outsider-saturation argument
proves p>=6.  A repeated ``--select a:u,t`` argument fixes the inaccessible
pair selected for source ``a``.  The certificate cover uses either one unit
(source 2) or two units (sources 2 and 3).

This file is self-contained.  It imports neither the historical scratch
producer nor any repository SAT helper.  Output is deterministic ASCII DIMACS.
"""

from __future__ import annotations

import argparse
import itertools
import os
from pathlib import Path

V = tuple(range(16))
ROOT = 0
R = 1
AP = tuple(range(2, 9))
K = tuple(range(9, 15))
B0 = 15
B = K + (B0,)


class CNF:
    def __init__(self) -> None:
        self.n = 0
        self.names: dict[str, int] = {}
        self.clauses: list[tuple[int, ...]] = []

    def var(self, name: str) -> int:
        value = self.names.get(name)
        if value is None:
            self.n += 1
            value = self.n
            self.names[name] = value
        return value

    def add(self, *literals: int) -> None:
        self.clauses.append(tuple(literals))


def at_most(cnf: CNF, literals, bound: int, tag: str) -> None:
    """Sinz sequential encoding of ``sum(literals) <= bound``.

    Inputs may be signed literals.  Auxiliary variable ``sc:tag:i:j`` denotes
    that at least ``j`` of the first ``i+1`` inputs are true in the canonical
    extension.
    """

    inputs = tuple(literals)
    n = len(inputs)
    if bound < 0:
        cnf.add()
        return
    if bound >= n:
        return
    if bound == 0:
        for literal in inputs:
            cnf.add(-literal)
        return

    sequential = {
        (i, j): cnf.var(f"sc:{tag}:{i}:{j}")
        for i in range(n - 1)
        for j in range(1, bound + 1)
    }
    cnf.add(-inputs[0], sequential[0, 1])
    for j in range(2, bound + 1):
        cnf.add(-sequential[0, j])
    for i in range(1, n - 1):
        cnf.add(-inputs[i], sequential[i, 1])
        cnf.add(-sequential[i - 1, 1], sequential[i, 1])
        for j in range(2, bound + 1):
            cnf.add(-inputs[i], -sequential[i - 1, j - 1], sequential[i, j])
            cnf.add(-sequential[i - 1, j], sequential[i, j])
        cnf.add(-inputs[i], -sequential[i - 1, bound])
    cnf.add(-inputs[-1], -sequential[n - 2, bound])


def exact(cnf: CNF, literals, value: int, tag: str) -> None:
    inputs = tuple(literals)
    at_most(cnf, inputs, value, tag + ":hi")
    at_most(cnf, tuple(-literal for literal in inputs), len(inputs) - value, tag + ":lo")


def allowed_pairs(source: int) -> tuple[tuple[int, int], ...]:
    return tuple(itertools.combinations((x for x in V if x != source), 2))


def build(p: int) -> CNF:
    if p not in (6, 7):
        raise ValueError("p must be 6 or 7")

    cnf = CNF()
    arc = {(i, j): cnf.var(f"a:{i}>{j}") for i in V for j in V if i != j}
    hole: dict[tuple[int, int], int] = {}

    # Exact trichotomy on every unordered pair: forward arc, reverse arc, hole.
    for i, j in itertools.combinations(V, 2):
        missing = cnf.var(f"h:{i}-{j}")
        hole[i, j] = missing
        cnf.add(arc[i, j], arc[j, i], missing)
        cnf.add(-arc[i, j], -arc[j, i])
        cnf.add(-arc[i, j], -missing)
        cnf.add(-arc[j, i], -missing)

    exact(cnf, hole.values(), 4, "holes")

    # Frozen root row N_T^+(v)={r} union A'.
    for x in (R,) + AP:
        cnf.add(arc[ROOT, x])
    for x in B:
        cnf.add(-arc[ROOT, x])

    # Exact T-outdegrees forced by the k=4 profile.
    degree = {
        ROOT: 8,
        R: 9,
        **{x: 8 for x in AP},
        **{x: 6 for x in K},
        B0: 7,
    }
    for x in V:
        exact(cnf, (arc[x, y] for y in V if y != x), degree[x], f"deg:{x}")

    # Frozen robust-witness consequence: every B column has an A' predecessor.
    for b in B:
        cnf.add(*(arc[x, b] for x in AP))

    # P is exactly the predecessor union of the six K columns.
    P = AP[:p]
    outside_P = AP[p:]
    for b in K:
        cnf.add(*(arc[x, b] for x in P))
    for x in P:
        cnf.add(*(arc[x, b] for b in K))
    for x in outside_P:
        for b in K:
            cnf.add(-arc[x, b])

    # For every source in P, select exactly one pair of T-inaccessible vertices.
    # The AMO clauses only choose one witness among possibly many; they do not
    # strengthen the projection onto graph variables.
    for source in P:
        selectors: list[int] = []
        for u, t in allowed_pairs(source):
            selector = cnf.var(f"sel:{source}:{u},{t}")
            selectors.append(selector)

            # Endpoints are outside S_source={source} union N_T^+(source).
            cnf.add(-selector, -arc[source, u])
            cnf.add(-selector, -arc[source, t])

            # Every present endpoint--source pair points endpoint -> source.
            cnf.add(-selector, hole[min(source, u), max(source, u)], arc[u, source])
            cnf.add(-selector, hole[min(source, t), max(source, t)], arc[t, source])

            # No source -> x -> endpoint two-walk inside T.
            for x in V:
                if x in (source, u, t):
                    continue
                cnf.add(-selector, -arc[source, x], hole[min(u, x), max(u, x)], arc[u, x])
                cnf.add(-selector, -arc[source, x], hole[min(t, x), max(t, x)], arc[t, x])

        cnf.add(*selectors)
        for left, right in itertools.combinations(selectors, 2):
            cnf.add(-left, -right)

    return cnf


def parse_selection(text: str) -> tuple[int, int, int]:
    try:
        source_text, pair_text = text.split(":", 1)
        u_text, t_text = pair_text.split(",", 1)
        source, u, t = int(source_text), int(u_text), int(t_text)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("selection must have form source:u,t") from None
    if u > t:
        u, t = t, u
    return source, u, t


def emit(cnf: CNF, path: Path, map_path: Path | None = None, units=()) -> None:
    clauses = cnf.clauses + [(literal,) for literal in units]
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(f"p cnf {cnf.n} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    os.replace(temporary, path)

    if map_path is not None:
        temporary_map = map_path.with_name(map_path.name + ".tmp")
        with temporary_map.open("w", encoding="ascii", newline="\n") as handle:
            for name, variable in sorted(cnf.names.items(), key=lambda item: item[1]):
                handle.write(f"{variable}\t{name}\n")
        os.replace(temporary_map, map_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("p", type=int, choices=(6, 7))
    parser.add_argument("output", type=Path)
    parser.add_argument("--map", dest="map_path", type=Path)
    parser.add_argument("--select", action="append", default=[], type=parse_selection,
                        metavar="SOURCE:U,T")
    args = parser.parse_args()

    cnf = build(args.p)
    sources = AP[:args.p]
    selected_sources: set[int] = set()
    unit_literals: list[int] = []
    normalized: list[str] = []
    for source, u, t in args.select:
        if source not in sources:
            parser.error(f"source {source} is outside canonical P={sources}")
        if source in selected_sources:
            parser.error(f"source {source} selected more than once")
        if (u, t) not in allowed_pairs(source):
            parser.error(f"invalid pair {u},{t} for source {source}")
        selected_sources.add(source)
        unit_literals.append(cnf.names[f"sel:{source}:{u},{t}"])
        normalized.append(f"{source}:{u},{t}")

    emit(cnf, args.output, args.map_path, unit_literals)
    print(f"p={args.p} vars={cnf.n} clauses={len(cnf.clauses) + len(unit_literals)} "
          f"selections={';'.join(normalized) if normalized else '-'}")


if __name__ == "__main__":
    main()
