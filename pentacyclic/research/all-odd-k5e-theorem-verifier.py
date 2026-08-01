#!/usr/bin/env python3
"""Fail-closed exact verifier for the all-odd K5-e theorem fixture."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SIEVE = ROOT / "pentacyclic/research/all-odd-k5e-territory-sieve.py"
FIXTURE = ROOT / "pentacyclic/research/all-odd-k5e-theorem.json"
PAPER = ROOT / "positive-square-energy/pentacyclic-general/all-odd-k5e-induced-territory-frontier.md"
SIEVE_SHA256 = "047a472d4e1af46850198dc68b5780f98b930618f79b51174f11460afcc0334d"
FIXTURE_SHA256 = "35523cc3be872181e2f343a7e21936f82b14e4a6968896fc2dcfd5f545da1ee1"
EDGES = (("a", "x"), ("a", "y"), ("a", "z"),
         ("b", "x"), ("b", "y"), ("b", "z"),
         ("x", "y"), ("x", "z"), ("y", "z"))
CENTERS = ("x", "y", "z")
EXPECTED_ORBIT_SIZES = (6, 6, 1, 12, 12, 6, 12, 3, 6, 6, 12, 12, 12, 12, 12, 12)

# Deterministic search output. Each row is (state, branch stereographic
# parameters, one internal-parameter tuple per physical path).
RAW_CERTIFICATES = (
 ("000001100",("0","17/64","-55/32","-193/64","43/32"),((),(),(),(),(),("-3/64","-23/64"),("-43/64","-9/64"),(),())),
 ("001010000",("0","-47/64","203/64","-13/8","27/64"),((),(),("-13/32","-63/64"),(),("-15/64","5/32"),(),(),(),())),
 ("000000111",("0","1/64","-535/8","-169/64","175/64"),((),(),(),(),(),(),("155/64","31/32"),("-145/64","-15/16"),("-21/16","-47/64"))),
 ("000001101",("0","3/16","-55/32","-631/32","53/32"),((),(),(),(),(),("-1/16","-5/16"),("-13/16","-21/64"),(),("-81/32","-19/16"))),
 ("000001102",("0","-11/64","113/64","-11333/32","-111/64"),((),(),(),(),(),("1/16","19/64"),("27/32","3/8"),(),("19/4","9/4","11/8","29/32"))),
 ("000011001",("0","-17/64","87/64","-27/16","-207/64"),((),(),(),(),("0","9/32"),("-5/64","7/64"),(),(),("-43/64","-9/64"))),
 ("000012010",("0","1/8","-209/64","21/16","-25/16"),((),(),(),(),("-9/64","-27/64"),("7/32","5/16","13/32","33/64"),(),("117/16","25/16"),())),
 ("001001100",("0","-1/64","1299/64","95/32","-9/16"),((),(),("23/64","27/32"),(),(),("23/64","27/32"),("-159/64","-15/16"),(),())),
 ("001002100",("0","3/32","-89/32","-345/16","33/64"),((),(),("-25/64","-57/64"),(),(),("-5/32","-13/32","-23/32","-37/32"),("-33/32","-25/64"),(),())),
 ("001010002",("0","1/16","-97/64","111/64","81/32"),((),(),("-1/8","-1/4"),(),("-9/64","-11/32"),(),(),(),("61/64","33/64","13/64","-3/32"))),
 ("001010010",("0","31/64","-143/64","13/8","-31/32"),((),(),("9/32","19/32"),(),("7/64","-7/32"),(),(),("-42","41/16"),())),
 ("001010020",("0","29/64","-65/32","105/64","-71/64"),((),(),("1/4","17/32"),(),("3/32","-15/64"),(),(),("-5","129/8","3","49/32"),())),
 ("001011000",("0","-21/64","207/64","-101/64","11/32"),((),(),("-7/16","-69/64"),(),("-1/64","9/32"),("-23/32","-43/32"),(),(),())),
 ("001012000",("0","-1/4","203/64","-51/32","5/16"),((),(),("-29/64","-9/8"),(),("1/32","19/64"),("-31/64","-49/64","-37/32","-57/32"),(),(),())),
 ("001020100",("0","-35/64","71/4","-41/16","39/64"),((),(),("-23/64","-13/16"),(),("-11/32","-5/32","1/64","13/64"),(),("137/64","15/16"),(),())),
 ("001120000",("0","185/64","-177/64","93/64","-9/32"),((),(),("15/32","19/16"),("11/8","3/4"),("875/64","-337/64","-133/64","-75/64"),(),(),(),())),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unit(text: str) -> tuple[Fraction, Fraction]:
    t = Fraction(text)
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def neg(v):
    return -v[0], -v[1]


def step_cost(left, right) -> Fraction:
    dot = left[0] * right[0] + left[1] * right[1]
    require(dot != -1, "antipodal path step")
    return (1 - dot) / (1 + dot)


def certificate_sequences(record):
    state = tuple(map(int, record["state"]))
    lengths = tuple({0: 1, 1: 3, 2: 5}[value] for value in state)
    branches = dict(zip(("a", "b", "x", "y", "z"), map(unit, record["branch"])))
    require(len(record["internal"]) == 9, "wrong path count")
    sequences = {}
    for edge, length, row in zip(EDGES, lengths, record["internal"]):
        require(len(row) == length - 1, "wrong internal path width")
        u, v = edge
        sequences[edge] = (branches[u], *(unit(t) for t in row), neg(branches[v]))
    return state, branches, sequences


def sequence_cost(sequences) -> Fraction:
    return sum(step_cost(a, b) for sequence in sequences.values()
               for a, b in zip(sequence, sequence[1:]))


def maps():
    for permutation in itertools.permutations(CENTERS):
        for swap in (False, True):
            mapping = dict(zip(CENTERS, permutation))
            mapping.update(a="b" if swap else "a", b="a" if swap else "b")
            yield mapping


def transport(state, mapping):
    index = {tuple(sorted(edge)): i for i, edge in enumerate(EDGES)}
    out = [None] * 9
    for value, (u, v) in zip(state, EDGES):
        out[index[tuple(sorted((mapping[u], mapping[v])))]] = value
    return tuple(out)


def transported_sequences(sequences, mapping):
    out = {}
    for (u, v), sequence in sequences.items():
        mu, mv = mapping[u], mapping[v]
        if (mu, mv) in EDGES:
            out[(mu, mv)] = sequence
        else:
            require((mv, mu) in EDGES, "transported nonedge")
            out[(mv, mu)] = tuple(neg(vector) for vector in reversed(sequence))
    return out


def fixture_payload():
    records = []
    for state, branch, internal in RAW_CERTIFICATES:
        record = {"state": state, "branch": list(branch),
                  "internal": [list(row) for row in internal]}
        _, _, sequences = certificate_sequences(record)
        record["cost"] = str(sequence_cost(sequences))
        records.append(record)
    return {"schema": 1, "theorem": "complete_all_odd_K5_minus_edge",
            "budget": "4", "records": records}


def verify_paper_tables(data) -> None:
    text = PAPER.read_text(encoding="ascii")
    for record in data["records"]:
        branch = "(" + ",".join(record["branch"]) + ")"
        internal = []
        for index, row in enumerate(record["internal"]):
            if row:
                internal.append(f"{index}:[{','.join(row)}]")
        parameter_row = (f"| `{record['state']}` | `{branch}` | "
                         f"`{'; '.join(internal)}` |")
        cost_row = f"| `{record['state']}` | `{record['cost']}` |"
        require(text.count(parameter_row) == 1,
                f"paper parameter table mismatch for {record['state']}")
        require(text.count(cost_row) == 1,
                f"paper cost table mismatch for {record['state']}")


def write_fixture() -> None:
    FIXTURE.write_text(json.dumps(fixture_payload(), indent=2, separators=(",", ": ")) + "\n",
                       encoding="ascii")
    print(f"wrote {FIXTURE.relative_to(ROOT)} sha256={digest(FIXTURE)}")


def load_sieve():
    spec = importlib.util.spec_from_file_location("k5e_sieve", SIEVE)
    require(spec is not None and spec.loader is not None, "cannot load source sieve")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify(data, mutation=None):
    require(data == fixture_payload(), "fixture differs from deterministic source records")
    if mutation == "drop-record":
        data["records"].pop()
    elif mutation == "branch-vector":
        data["records"][0]["branch"][1] = "9/10"
    elif mutation == "internal-vector":
        data["records"][1]["internal"][2][0] = "7/8"
    elif mutation == "physical-cost":
        data["records"][1]["cost"] = "3"
    elif mutation == "state-key":
        data["records"][2]["state"] = "000000112"
    elif mutation == "budget":
        data["budget"] = "5"
    elif mutation == "theorem":
        data["theorem"] = "frontier_only"
    require(data == fixture_payload(), "deterministic fixture record changed")
    require(data["schema"] == 1 and data["budget"] == "4", "fixture header changed")
    require(data["theorem"] == "complete_all_odd_K5_minus_edge", "theorem status changed")
    verify_paper_tables(data)

    sieve = load_sieve()
    dispositions, encoded = sieve.audit()
    require(dict(dispositions) == sieve.EXPECTED_DISPOSITIONS, "source disposition mismatch")
    require(tuple(record["state"] for record in data["records"]) == encoded,
            "certificate keys do not equal residual orbit keys")

    certificate_by_state = {}
    for record in data["records"]:
        state, _, sequences = certificate_sequences(record)
        cost = sequence_cost(sequences)
        require(cost == Fraction(record["cost"]), "stored physical cost changed")
        require(cost < 4, f"certificate {record['state']} has cost {cost}")
        certificate_by_state[state] = (sequences, cost)

    all_maps = tuple(maps())
    require(len(all_maps) == 12, "automorphism group order changed")
    orbit_sizes = tuple(len({transport(state, mapping) for mapping in all_maps})
                        for state in certificate_by_state)
    require(orbit_sizes == EXPECTED_ORBIT_SIZES, "residual orbit sizes changed")
    require(sum(orbit_sizes) == 142, "residual orbit-size sum changed")

    residual_count = transported_count = 0
    for state in itertools.product(range(3), repeat=9):
        kind = sieve.disposition(state)
        if kind == "complete-k4":
            require(any(sieve.retained_k4_is_complete(state, endpoint)
                        for endpoint in ("a", "b")), "invalid actual-K4 close")
        if kind != "residual":
            continue
        residual_count += 1
        matches = [(rep, mapping) for rep in certificate_by_state for mapping in all_maps
                   if transport(rep, mapping) == state]
        require(matches, "residual has no exact automorphism transport")
        rep, mapping = matches[0]
        sequences, original_cost = certificate_by_state[rep]
        moved = transported_sequences(sequences, mapping)
        require(set(moved) == set(EDGES), "transport lost a physical path")
        require(sequence_cost(moved) == original_cost, "transport changed physical cost")
        transported_count += 1
    require(residual_count == transported_count == 142, "residual coverage changed")


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] == "--write-fixture":
        write_fixture()
        return
    require(len(sys.argv) == 1, "usage: verifier.py [--write-fixture]")
    require(digest(SIEVE) == SIEVE_SHA256, "source sieve SHA-256 lock failed")
    require(digest(FIXTURE) == FIXTURE_SHA256, "fixture SHA-256 lock failed")
    pristine = json.loads(FIXTURE.read_text(encoding="ascii"))
    verify(pristine)
    mutations = ("drop-record", "branch-vector", "internal-vector", "physical-cost",
                 "state-key", "budget", "theorem")
    rejected = 0
    for mutation in mutations:
        candidate = json.loads(FIXTURE.read_text(encoding="ascii"))
        try:
            verify(candidate, mutation)
        except (RuntimeError, KeyError, IndexError, ValueError, ZeroDivisionError):
            rejected += 1
    require(rejected == len(mutations), "a hostile mutation survived")
    print("all-odd K5-e theorem verifier: PASS")
    print("states=19683 simplex=18848 actual_k4=53 theta=640 residual=142")
    print(f"certificates=16 transported=142 mutations={rejected}/{len(mutations)}")
    print(f"fixture_sha256={FIXTURE_SHA256}")


if __name__ == "__main__":
    main()
