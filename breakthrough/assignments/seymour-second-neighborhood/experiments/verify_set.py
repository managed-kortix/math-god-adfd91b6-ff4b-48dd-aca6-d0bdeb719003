#!/usr/bin/env python3
"""Strict set-based verifier for an explicit SNC counterexample certificate."""
import hashlib
import re
import sys

DEC = re.compile(rb"0|[1-9][0-9]*")


def parse(data):
    if b"\x00" in data or b"\r" in data:
        raise ValueError("NUL/CR forbidden")
    lines = data.splitlines()
    if not lines or not DEC.fullmatch(lines[0]):
        raise ValueError("bad n")
    n = int(lines[0])
    if n < 1:
        raise ValueError("n must be positive")
    arcs, previous = [], None
    for line in lines[1:]:
        fields = line.split(b" ")
        if len(fields) != 2 or not all(DEC.fullmatch(x) for x in fields):
            raise ValueError("bad arc line")
        arc = tuple(map(int, fields))
        u, v = arc
        if u >= n or v >= n or u == v:
            raise ValueError("bad endpoint or loop")
        if previous is not None and not previous < arc:
            raise ValueError("arcs not strictly sorted")
        if (v, u) in arcs:
            raise ValueError("digon")
        arcs.append(arc)
        previous = arc
    normalized = (str(n) + "\n" + "".join(f"{u} {v}\n" for u, v in arcs)).encode()
    return n, arcs, normalized


def neighborhoods(n, arcs):
    n1 = [set() for _ in range(n)]
    for u, v in arcs:
        n1[u].add(v)
    n2 = []
    for v in range(n):
        reached = set()
        for y in n1[v]:
            reached.update(n1[y])
        n2.append(reached - n1[v] - {v})
    return n1, n2


def main(path):
    n, arcs, normalized = parse(open(path, "rb").read())
    n1, n2 = neighborhoods(n, arcs)
    passed = True
    for v in range(n):
        margin = len(n1[v]) - len(n2[v])
        passed &= margin > 0
        print(f"{v}: N1={sorted(n1[v])} N2={sorted(n2[v])} "
              f"d1={len(n1[v])} d2={len(n2[v])} margin={margin}")
    print("sha256=" + hashlib.sha256(normalized).hexdigest())
    print("PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1]))
    except (IndexError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
