#!/usr/bin/env python3
"""Select one deterministic high-concentration pilot per k=4 shape."""
import sys


def parse(line):
    key, status = line.rstrip("\n").split("\t")
    fields = dict(piece.split("=", 1) for piece in key.split("/")[1:])
    return key, status, fields


def main():
    path = sys.argv[1] if len(sys.argv) == 2 else "m9-k4-cover.tsv"
    with open(path, encoding="ascii") as f:
        rows = [parse(line) for line in f]
    shapes = sorted({fields["shape"] for _, _, fields in rows})
    selected = []
    for index, shape in enumerate(shapes):
        kappa = str(5 + index % 2)
        pool = [(key, fields) for key, status, fields in rows
                if status == "FEASIBLE" and fields["shape"] == shape
                and fields["kappa"] == kappa]
        key, fields = min(pool, key=lambda row:
                          (-int(row[1]["eta"]), -int(row[1]["lambda"]), row[0]))
        selected.append(key)
    assert len(selected) == len(set(selected)) == 11
    for key in selected:
        print(key)


if __name__ == "__main__":
    main()
