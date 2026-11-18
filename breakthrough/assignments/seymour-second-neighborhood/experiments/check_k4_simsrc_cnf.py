#!/usr/bin/env python3
"""Producer-independent structural/semantic checker for k4_simsrc_cnf.py.

The checker never imports the producer.  It independently reconstructs the
expected variable ordering and complete DIMACS clause sequence, audits the
Sinz counter truth semantics exhaustively on small widths, and checks that the
requested branch units form a valid one- or two-level selector split.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path

V = tuple(range(16))
ROOT = 0
R = 1
AP = tuple(range(2, 9))
K = tuple(range(9, 15))
B0 = 15
B = K + (B0,)


class Expected:
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


def expected_at_most(formula: Expected, literals, bound: int, tag: str) -> None:
    inputs = tuple(literals)
    n = len(inputs)
    if bound < 0:
        formula.add()
        return
    if bound >= n:
        return
    if bound == 0:
        for literal in inputs:
            formula.add(-literal)
        return

    state = {
        (i, j): formula.var(f"sc:{tag}:{i}:{j}")
        for i in range(n - 1)
        for j in range(1, bound + 1)
    }
    formula.add(-inputs[0], state[0, 1])
    for j in range(2, bound + 1):
        formula.add(-state[0, j])
    for i in range(1, n - 1):
        formula.add(-inputs[i], state[i, 1])
        formula.add(-state[i - 1, 1], state[i, 1])
        for j in range(2, bound + 1):
            formula.add(-inputs[i], -state[i - 1, j - 1], state[i, j])
            formula.add(-state[i - 1, j], state[i, j])
        formula.add(-inputs[i], -state[i - 1, bound])
    formula.add(-inputs[-1], -state[n - 2, bound])


def expected_exact(formula: Expected, literals, value: int, tag: str) -> None:
    inputs = tuple(literals)
    expected_at_most(formula, inputs, value, tag + ":hi")
    expected_at_most(formula, (-literal for literal in inputs), len(inputs) - value, tag + ":lo")


def allowed_pairs(source: int) -> tuple[tuple[int, int], ...]:
    return tuple(itertools.combinations((x for x in V if x != source), 2))


def reconstruct(p: int) -> Expected:
    if p not in (6, 7):
        raise RuntimeError("p must be 6 or 7")

    formula = Expected()
    arc = {(i, j): formula.var(f"a:{i}>{j}") for i in V for j in V if i != j}
    hole: dict[tuple[int, int], int] = {}

    for i, j in itertools.combinations(V, 2):
        missing = formula.var(f"h:{i}-{j}")
        hole[i, j] = missing
        formula.add(arc[i, j], arc[j, i], missing)
        formula.add(-arc[i, j], -arc[j, i])
        formula.add(-arc[i, j], -missing)
        formula.add(-arc[j, i], -missing)

    expected_exact(formula, hole.values(), 4, "holes")
    for x in (R,) + AP:
        formula.add(arc[ROOT, x])
    for x in B:
        formula.add(-arc[ROOT, x])

    degrees = {
        ROOT: 8,
        R: 9,
        **{x: 8 for x in AP},
        **{x: 6 for x in K},
        B0: 7,
    }
    for x in V:
        expected_exact(formula, (arc[x, y] for y in V if y != x), degrees[x], f"deg:{x}")

    for b in B:
        formula.add(*(arc[x, b] for x in AP))

    P = AP[:p]
    for b in K:
        formula.add(*(arc[x, b] for x in P))
    for x in P:
        formula.add(*(arc[x, b] for b in K))
    for x in AP[p:]:
        for b in K:
            formula.add(-arc[x, b])

    for source in P:
        selectors: list[int] = []
        for u, t in allowed_pairs(source):
            selector = formula.var(f"sel:{source}:{u},{t}")
            selectors.append(selector)
            formula.add(-selector, -arc[source, u])
            formula.add(-selector, -arc[source, t])
            formula.add(-selector, hole[min(source, u), max(source, u)], arc[u, source])
            formula.add(-selector, hole[min(source, t), max(source, t)], arc[t, source])
            for x in V:
                if x in (source, u, t):
                    continue
                formula.add(-selector, -arc[source, x], hole[min(u, x), max(u, x)], arc[u, x])
                formula.add(-selector, -arc[source, x], hole[min(t, x), max(t, x)], arc[t, x])
        formula.add(*selectors)
        for left, right in itertools.combinations(selectors, 2):
            formula.add(-left, -right)

    return formula


def parse_cnf(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = clauses_declared = None
    clauses: list[tuple[int, ...]] = []
    for line_number, line in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            if variables is not None:
                raise RuntimeError("duplicate DIMACS header")
            fields = line.split()
            if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                raise RuntimeError("malformed DIMACS header")
            variables, clauses_declared = map(int, fields[2:])
            continue
        values = tuple(map(int, line.split()))
        if not values or values[-1] != 0 or any(value == 0 for value in values[:-1]):
            raise RuntimeError(f"malformed clause at line {line_number}")
        clauses.append(values[:-1])
    if variables is None or len(clauses) != clauses_declared:
        raise RuntimeError("DIMACS dimensions disagree")
    if any(abs(literal) > variables for clause in clauses for literal in clause):
        raise RuntimeError("literal exceeds DIMACS variable bound")
    return variables, clauses


def parse_map(path: Path) -> tuple[list[str], dict[str, int]]:
    names: list[str] = []
    reverse: dict[str, int] = {}
    for ordinal, line in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        fields = line.split("\t", 1)
        if len(fields) != 2 or int(fields[0]) != ordinal or fields[1] in reverse:
            raise RuntimeError("malformed or duplicate variable map row")
        names.append(fields[1])
        reverse[fields[1]] = ordinal
    return names, reverse


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


def clauses_hold(clauses, assignment: dict[int, bool]) -> bool:
    return all(any(assignment[abs(literal)] == (literal > 0) for literal in clause) for clause in clauses)


def audit_small_counter_semantics() -> None:
    """Exhaustively test independent counter clauses on all small inputs."""

    for n in range(1, 9):
        for bound in range(0, n + 1):
            formula = Expected()
            inputs = [formula.var(f"x:{i}") for i in range(n)]
            expected_at_most(formula, inputs, bound, "audit")
            for bits in itertools.product((False, True), repeat=n):
                assignment = {variable: bit for variable, bit in zip(inputs, bits)}
                for name, variable in formula.names.items():
                    if not name.startswith("sc:audit:"):
                        continue
                    _, _, i_text, j_text = name.split(":")
                    assignment[variable] = sum(bits[:int(i_text) + 1]) >= int(j_text)
                if clauses_hold(formula.clauses, assignment) != (sum(bits) <= bound):
                    raise RuntimeError(f"counter audit failed for n={n}, bound={bound}, bits={bits}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("p", type=int, choices=(6, 7))
    parser.add_argument("cnf", type=Path)
    parser.add_argument("map", type=Path)
    parser.add_argument("--select", action="append", default=[], type=parse_selection,
                        metavar="SOURCE:U,T")
    args = parser.parse_args()

    audit_small_counter_semantics()
    expected = reconstruct(args.p)
    actual_variables, actual_clauses = parse_cnf(args.cnf)
    actual_names, actual_reverse = parse_map(args.map)

    expected_names = [name for name, _ in sorted(expected.names.items(), key=lambda item: item[1])]
    if actual_variables != expected.n or actual_names != expected_names:
        raise RuntimeError("variable universe/order differs from independent reconstruction")

    expected_units: list[tuple[int, ...]] = []
    seen_sources: set[int] = set()
    normalized: list[str] = []
    for source, u, t in args.select:
        if source not in AP[:args.p] or source in seen_sources or (u, t) not in allowed_pairs(source):
            raise RuntimeError("invalid or duplicate branch selection")
        seen_sources.add(source)
        expected_units.append((actual_reverse[f"sel:{source}:{u},{t}"],))
        normalized.append(f"{source}:{u},{t}")

    expected_clauses = expected.clauses + expected_units
    if actual_clauses != expected_clauses:
        mismatch = next((i for i, (left, right) in enumerate(zip(actual_clauses, expected_clauses))
                         if left != right), min(len(actual_clauses), len(expected_clauses)))
        raise RuntimeError(f"clause sequence differs at zero-based index {mismatch}")

    # Explicit semantic guard audit, independent of sequence equality.
    clause_set = set(actual_clauses)
    for source in AP[:args.p]:
        selectors = [actual_reverse[f"sel:{source}:{u},{t}"] for u, t in allowed_pairs(source)]
        if tuple(selectors) not in clause_set:
            raise RuntimeError("source selector ALO missing")
        for left, right in itertools.combinations(selectors, 2):
            if (-left, -right) not in clause_set:
                raise RuntimeError("source selector AMO missing")
        for u, t in allowed_pairs(source):
            selector = actual_reverse[f"sel:{source}:{u},{t}"]
            for endpoint in (u, t):
                if (-selector, -actual_reverse[f"a:{source}>{endpoint}"]) not in clause_set:
                    raise RuntimeError("endpoint-outside-source-row clause missing")
                missing = actual_reverse[f"h:{min(source, endpoint)}-{max(source, endpoint)}"]
                if (-selector, missing, actual_reverse[f"a:{endpoint}>{source}"]) not in clause_set:
                    raise RuntimeError("endpoint-to-source guard missing")
                for x in V:
                    if x in (source, u, t):
                        continue
                    missing_x = actual_reverse[f"h:{min(endpoint, x)}-{max(endpoint, x)}"]
                    guarded = (-selector, -actual_reverse[f"a:{source}>{x}"], missing_x,
                               actual_reverse[f"a:{endpoint}>{x}"])
                    if guarded not in clause_set:
                        raise RuntimeError("two-walk exclusion guard missing")

    print(f"PASS p={args.p} vars={actual_variables} clauses={len(actual_clauses)} "
          f"selections={';'.join(normalized) if normalized else '-'} "
          f"cnf_sha256={sha256(args.cnf)} map_sha256={sha256(args.map)}")


if __name__ == "__main__":
    main()
