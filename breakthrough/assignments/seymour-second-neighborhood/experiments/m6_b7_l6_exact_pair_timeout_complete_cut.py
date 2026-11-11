#!/usr/bin/env python3
"""Classify the 33 frozen singleton TIMEOUTs by their forced complete cuts."""

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as singleton
import m6_b7_l6_early_c_inaccessible_pair_orbits as pairs

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-exact-pair-timeout-complete-cut"
FORMAT = f"{PREFIX}-census-v1"
SCOUT = HERE / f"{singleton.PREFIX}-scout-5s.json"
SCOUT_IDENTITY = (29545, "adc5c7af3ffdc53512e953b98019334835612040481204d0dd921ecc6287cb88")
A = frozenset(range(9))
B = frozenset(range(9, 16))
C = frozenset((16, 17))


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def is_hole(holes, u, v):
    return tuple(sorted((u, v))) in holes


def records():
    if identity(SCOUT) != SCOUT_IDENTITY:
        raise RuntimeError("frozen five-second singleton scout changed")
    scout = json.loads(SCOUT.read_text(encoding="ascii"))
    _, memberships = singleton.load_memberships()
    timeout_ordinals = tuple(row["membership"] for row in scout["rows"]
                             if row["status"] == "TIMEOUT")
    if len(timeout_ordinals) != 33 or timeout_ordinals[0] != 0:
        raise RuntimeError("frozen singleton TIMEOUT scope changed")
    result = []
    for ordinal in timeout_ordinals:
        member = memberships[ordinal]
        cell, (_, child), parent = member
        profile, pair = child[2], frozenset(child[3])
        low = pairs.low_vertex(profile[3])
        holes = singleton.parent_projection(member)
        nonout = pairs.nonoutneighbors(low, profile[3], profile[5], holes)
        out = frozenset(range(18)) - nonout - {low}
        if len(out) != 8:
            raise RuntimeError("invalid low-C outneighborhood or pair")
        forced = tuple(sorted((endpoint, target) for endpoint in pair for target in out
                              if not is_hole(holes, endpoint, target)))
        loads = tuple(sum(is_hole(holes, endpoint, target) for target in out)
                      for endpoint in sorted(pair))
        low_load = sum(is_hole(holes, low, vertex) for vertex in range(18) if vertex != low)
        other_load = 6 - low_load - sum(loads) - int(is_hole(holes, *sorted(pair)))
        if ordinal == 0:
            class_key = "exceptional-membership000"
            epsilon = b_count = chi = "-"
        else:
            a_endpoint = next(iter(pair & A), None)
            c_endpoint = next(iter(pair & C), None)
            if a_endpoint is None or c_endpoint is None or loads[sorted(pair).index(a_endpoint)] != 0:
                raise RuntimeError("nonexceptional pair is not an A-C packet with zero A-S holes")
            epsilon = int(is_hole(holes, a_endpoint, c_endpoint))
            b_count = len(out & B)
            chi = loads[sorted(pair).index(c_endpoint)]
            class_key = f"epsilon{epsilon}-b{b_count}-chi{chi}"
        if other_load < 0 or low_load + sum(loads) + int(is_hole(holes, *sorted(pair))) + other_load != 6:
            raise RuntimeError("six-hole load identity failed")
        result.append({"membership": ordinal, "cell": cell, "profile": child[1],
                       "parent": parent, "low": low, "pair": tuple(sorted(pair)),
                       "out": tuple(sorted(out)), "forced": forced, "loads": loads,
                       "low_load": low_load, "pair_hole": int(is_hole(holes, *sorted(pair))),
                       "other_load": other_load, "epsilon": epsilon, "b": b_count,
                       "chi": chi, "class": class_key})
    if sum(record["class"] != "exceptional-membership000" for record in result) != 32:
        raise RuntimeError("A-C packet total changed")
    return tuple(result)


def payload(rows):
    classes = defaultdict(list)
    for row in rows:
        classes[row["class"]].append(row["membership"])
    lines = [FORMAT, f"source-scout-bytes\t{SCOUT_IDENTITY[0]}",
             f"source-scout-sha256\t{SCOUT_IDENTITY[1]}", "memberships\t33",
             "A-C-packets\t32", "exceptional-memberships\t000",
             "S-definition\tS=N+(low-C)",
             "orientation\tfor inaccessible endpoint x and s in S, every present pair is forced x->s",
             "implication\texisting q equivalence, exact pair projection, arc exclusivity, and hole equivalence imply every forced orientation",
             "cnf-action\tnone; no nonredundant constraint identified",
             "hole-load-identity\t6=low-load+endpoint-S-loads+pair-hole+other-load",
             f"classes\t{len(classes)}",
             "class-columns\tclass,count,memberships"]
    for key in sorted(classes):
        values = classes[key]
        lines.append(f"class\t{key}\t{len(values)}\t{','.join(f'{value:03d}' for value in values)}")
    lines.append("columns\tmembership,cell,profile,parent,low-C,pair,S,forced-present-arcs,endpoint-S-hole-loads,pair-hole,low-hole-load,other-hole-load,class")
    for row in rows:
        arcs = ",".join(f"{u}>{v}" for u, v in row["forced"])
        lines.append(f"{row['membership']:03d}\t{row['cell']:02d}\t{row['profile']:02d}\t"
                     f"{row['parent']:02d}\t{row['low']}\t{','.join(map(str, row['pair']))}\t"
                     f"{','.join(map(str, row['out']))}\t{arcs}\t{','.join(map(str, row['loads']))}\t"
                     f"{row['pair_hole']}\t{row['low_load']}\t{row['other_load']}\t{row['class']}")
    return ("\n".join(lines) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = records()
    data = payload(rows)
    if args.output:
        args.output.write_bytes(data)
    print(f"PASS memberships=33 A_C_packets=32 classes={len(set(r['class'] for r in rows))} "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
