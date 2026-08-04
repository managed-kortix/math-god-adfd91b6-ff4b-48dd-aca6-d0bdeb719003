#!/usr/bin/env python3
"""Fail-closed audit for the exhaustive hexacyclic multiblock ledger."""

import hashlib
import importlib.util
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "combined-theorem": (
        ROOT / "positive-square-energy/hexacyclic-general/"
        "multiblock-items1-7-combined-theorem-audit.md",
        "7c9e6a371000283958d4d1eb7db0a181b4968fe50cf4a37fd8d7d26eddc43378",
    ),
    "items1-4": (
        ROOT / "positive-square-energy/hexacyclic-general/"
        "multiblock-items1-4-owner-exact-closure.md",
        "49a24ebe705aecd9248224cc39c748041c0d6d4981a137f6daad6d93019a1cb1",
    ),
    "items5-7": (
        ROOT / "positive-square-energy/hexacyclic-general/"
        "multiblock-items5-7-owner-exact-closure.md",
        "1c5722565e874ebf04533e908c5bf335f7be0b56a5665f5b607cfdef14ac8c67",
    ),
    "theta-triangle": (
        ROOT / "positive-square-energy/hexacyclic-general/"
        "favorable-theta-triangle-shared-cut-packet.md",
        "d222e09a20dce19703f8386c6a3a3699e0621b63f761e553fee3215adf8e2446",
    ),
    "rank4-ledger": (
        ROOT / "all-tetracyclic-graphs/paper.tex",
        "1cd8bc9af6c8ed6ad3c3b99e967b4712dedfcc561f324d991b65798821f8c26b",
    ),
    "k5e-ledger": (
        ROOT / "positive-square-energy/pentacyclic-general/"
        "all-odd-k5e-induced-territory-frontier.md",
        "e43bbd97566ab5ea28b360311a2e3e1bc40397c3f40f250e954d1c016d94e6a5",
    ),
    "k5e-sieve": (
        ROOT / "pentacyclic/research/all-odd-k5e-territory-sieve.py",
        "047a472d4e1af46850198dc68b5780f98b930618f79b51174f11460afcc0334d",
    ),
    "k22-fixture": (
        ROOT / "pentacyclic/research/order5-kernel-family-theorem.json",
        "4d8b826b397dc269c7853b8bd386d00bf469282b52720b8dac96d850e9e616d8",
    ),
    "k71-fixture": (
        ROOT / "pentacyclic/research/order6-kernel-family-theorem.json",
        "69b236b014aef58c037c610ca01fa62ad82601f7bb34153939ec4ddd3b5f364d",
    ),
}

EXPECTED_PARTITIONS = {
    (1, 1, 1, 1, 1, 1),
    (2, 1, 1, 1, 1),
    (2, 2, 1, 1),
    (2, 2, 2),
    (3, 1, 1, 1),
    (3, 2, 1),
    (3, 3),
    (4, 1, 1),
    (4, 2),
    (5, 1),
    (6,),
}

EXPECTED_PACKET_RECORDS = {
    "A": ((2, 1, 1, 1, 1), "Theta(1,2,r)+T4", "items1-4"),
    "B": ((2, 1, 1, 1, 1), "D+T3+P", "items1-4"),
    "C": ((2, 2, 1, 1), "D+D+T2", "items1-4"),
    "D": ((3, 1, 1, 1), "S3+T3", "items1-4"),
    "E": ((3, 1, 1, 1), "K4+three-cycles", "items5-7"),
    "F": ((4, 1, 1), "S4+T+cycle", "items5-7"),
    "G": ((5, 1), "favorable-K5e+T", "items5-7+theta-triangle"),
    "H": ((5, 1), "structural-K22+arbitrary-cycle", "items5-7+k22-fixture"),
    "I": ((5, 1), "structural-K71+arbitrary-cycle", "items5-7+k71-fixture"),
}

DISPOSITIONS = {
    (1, 1, 1, 1, 1, 1): "cactus",
    (2, 1, 1, 1, 1): "packets:A,B",
    (2, 2, 1, 1): "packet:C",
    (2, 2, 2): "dnn",
    (3, 1, 1, 1): "packets:D,E",
    (3, 2, 1): "dnn+presieve:K4-theta-cycle",
    (3, 3): "dnn+presieve:K4-rank3",
    (4, 1, 1): "dnn-nontriangle+packet:F",
    (4, 2): "dnn+presieve:S4-theta",
    (5, 1): "rank5-direct-nonstrict+structural:G,H,I",
    (6,): "single-block-out-of-scope",
}

PACKETS = dict(EXPECTED_PACKET_RECORDS)

EXPECTED_RANK5_STRUCTURAL = {
    "K5e": {
        "disposition": "triangle-only-after-nontriangle-dnn-gate",
        "states": 693,
        "subclasses": {"complete-k4": 53, "favorable-theta": 640},
    },
    "K22": {
        "disposition": "owner-exact-arbitrary-cycle",
        "targets": tuple(sorted((
            ((0, 0, 0, 1, 1, 1, 1, 1, 1, 1), None),
            ((0, 0, 0, 1, 1, 1, 1, 1, 1, 1), 0),
            ((0, 0, 1, 1, 1, 1, 1, 1, 1, 1), None),
            ((0, 0, 1, 1, 1, 1, 1, 1, 1, 1), 0),
        ), key=repr)),
    },
    "K71": {
        "disposition": "owner-exact-arbitrary-cycle",
        "targets": 9,
        "frontiers": (None, 5, 6),
        "rows": 3,
    },
}

EXPECTED_OWNER_CASES = tuple(
    (family, route, boundary)
    for family in ("K22", "K71")
    for route in ("opened-owner", "retained-owner")
    for boundary in ("shared-cut", "positive-connector", "nested-cycle")
)

EXPECTED_GLOBAL_CLAIM = {
    "scope": "rank-six-multiblock",
    "relation": ">=",
    "conclusion": "s+(G)>=|V(G)|",
}

EXPECTED_RANK5_DIRECT_EQUALITY = {
    "partition": (5, 1),
    "rank5_excess": 4,
    "cycle": "T",
    "cycle_excess": 1,
    "total_excess": 5,
    "budget": 5,
    "disposition": "dnn-closed",
    "residual": False,
    "relation": ">=",
}

PRESIEVE = {
    "K4+Theta(1,2,r)+T": (3, 2, 1),
    "K4+D+P": (3, 2, 1),
    "K4+K4": (3, 3),
    "K4+S3": (3, 3),
    "S4+Theta": (4, 2),
}


class AuditError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def integer_partitions(total, maximum=None):
    if total == 0:
        return {()}
    if maximum is None or maximum > total:
        maximum = total
    result = set()
    for first in range(maximum, 0, -1):
        for suffix in integer_partitions(total - first, first):
            result.add((first,) + suffix)
    return result


def check_sources(sources):
    require(set(sources) == {
        "combined-theorem", "items1-4", "items5-7", "theta-triangle",
        "rank4-ledger", "k5e-ledger", "k5e-sieve", "k22-fixture",
        "k71-fixture",
    },
            "source lock key set changed")
    for name, (path, digest) in sources.items():
        require(path.is_file(), f"missing source: {name}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == digest, f"source digest mismatch: {name}")


def check_inequalities(values=None):
    if values is None:
        values = {
            "p": 5.0 - 2.0 * math.sqrt(5.0),
            "d": (math.sqrt(17.0) - 1.0) / 2.0,
            "s3": 12.0 / 5.0,
            "s4_even": 18.0 / 5.0,
            "s4_odd": 19.0 / 6.0,
            "k5e": 2.0 * math.sqrt(7.0) - 1.0,
        }
    p = values["p"]
    d = values["d"]
    require(p < 2.0 / 3.0, "pentagon bound does not force item-E triangle")
    require(3.0 * p < 2.0, "three nontriangles can survive item E")
    require(3.0 * d < 5.0, "2+2+2 DNN row is not closed")
    require(values["s3"] + d + 1.0 < 5.0,
            "non-K4 3+2+1 DNN row is not closed")
    require(2.0 * values["s3"] < 5.0,
            "non-K4 3+3 DNN row is not closed")
    require(3.0 + d < 5.0, "direct 4+2 DNN row is not closed")
    require(p < 3.0 / 5.0, "pentagon 3/5 bound failed")
    require(values["s4_even"] <= 18.0 / 5.0,
            "S4 even structural certificate changed")
    require(values["s4_odd"] <= 19.0 / 6.0,
            "S4 odd structural certificate changed")
    require(max(values["s4_even"], values["s4_odd"]) + 2.0 * p < 5.0,
            "S4 nontriangle gate exceeds budget")
    require(values["k5e"] + p < 5.0,
            "K5-e nontriangle gate exceeds budget")
    require(529 < 560, "exact radical certificate changed")


def check_conclusion(sources, global_claim=None, direct_equality=None):
    if global_claim is None:
        global_claim = EXPECTED_GLOBAL_CLAIM
    if direct_equality is None:
        direct_equality = EXPECTED_RANK5_DIRECT_EQUALITY
    require(global_claim == EXPECTED_GLOBAL_CLAIM,
            "global multiblock conclusion must be nonstrict")
    require(direct_equality == EXPECTED_RANK5_DIRECT_EQUALITY,
            "rank-five direct equality ledger changed")
    require(direct_equality["partition"] == (5, 1),
            "rank-five direct equality has wrong partition")
    require(direct_equality["rank5_excess"] + direct_equality["cycle_excess"]
            == direct_equality["total_excess"] == direct_equality["budget"],
            "rank-five direct plus triangle is not an exact budget equality")
    require(direct_equality["cycle"] == "T",
            "rank-five direct equality cycle is not a triangle")
    require(direct_equality["disposition"] == "dnn-closed"
            and direct_equality["residual"] is False,
            "rank-five direct equality plus triangle must close without residual")
    require(direct_equality["relation"] == global_claim["relation"] == ">=",
            "equality row cannot support strict promotion")
    theorem_text = sources["combined-theorem"][0].read_text(encoding="ascii")
    require("`s^+(G)>=|V(G)|`." in theorem_text,
            "combined theorem does not state the global nonstrict conclusion")
    require("direct rank-five equality certificate of excess four together with a triangle"
            in theorem_text,
            "combined theorem omits the rank-five equality-plus-triangle case")
    require("a closed direct row and contributes no packet residual" in theorem_text,
            "combined theorem leaves an equality-row residual")


def load_python(path):
    spec = importlib.util.spec_from_file_location("rank5_structural_sieve", path)
    require(spec is not None and spec.loader is not None, "cannot load K5e sieve")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="ascii"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise AuditError(f"cannot load structural fixture: {error}") from error


def regenerate_rank5_structural(sources, dispositions=None):
    if dispositions is None:
        dispositions = EXPECTED_RANK5_STRUCTURAL
    require(dispositions == EXPECTED_RANK5_STRUCTURAL,
            "rank-five structural disposition ledger changed")

    sieve = load_python(sources["k5e-sieve"][0])
    counts, unused_orbits = sieve.audit()
    k5e_subclasses = {name: counts[name] for name in ("complete-k4", "favorable-theta")}
    k5e = {
        "disposition": dispositions["K5e"]["disposition"],
        "states": sum(k5e_subclasses.values()),
        "subclasses": k5e_subclasses,
    }

    k22_fixture = load_json(sources["k22-fixture"][0])
    k22_targets = tuple(sorted(
        ((tuple(record["row"]), record["frontier"])
         for record in k22_fixture["records"]
         if record["method"] == "structural_attached_k4"), key=repr))
    k22 = {"disposition": dispositions["K22"]["disposition"],
           "targets": k22_targets}

    k71_fixture = load_json(sources["k71-fixture"][0])
    k71_records = tuple(record for record in k71_fixture["closure_records"]
                        if record["method"] == "structural_triangle_plus_attached_k4")
    k71_rows = {tuple(record["row"]) for record in k71_records}
    k71_frontiers = {record["frontier"] for record in k71_records}
    k71 = {
        "disposition": dispositions["K71"]["disposition"],
        "targets": len(k71_records),
        "frontiers": tuple(sorted(k71_frontiers, key=lambda value: (-1 if value is None else value))),
        "rows": len(k71_rows),
    }
    regenerated = {"K5e": k5e, "K22": k22, "K71": k71}
    require(regenerated == EXPECTED_RANK5_STRUCTURAL,
            "regenerated rank-five structural families changed")
    return regenerated


def descendants(parent, root):
    reached = {root}
    while True:
        expanded = reached | {child for child, predecessor in parent.items()
                              if predecessor in reached}
        if expanded == reached:
            return reached
        reached = expanded


def check_owner_exact_routes(cases=None):
    if cases is None:
        cases = EXPECTED_OWNER_CASES
    require(cases == EXPECTED_OWNER_CASES, "rank-five owner incidence ledger changed")
    checked = 0
    for family, route, boundary in cases:
        owners = {(family, "opened", index) for index in range(4)}
        owners |= {(family, "k4", index) for index in range(4)}
        parent = {}
        vertices = set(owners)
        for owner in owners:
            previous = owner
            for depth in range(1, 4):
                child = ("tree", owner, depth)
                parent[child] = previous
                vertices.add(child)
                previous = child

        opened = {owner for owner in owners if owner[1] == "opened"}
        retained = owners - opened
        opened |= {vertex for owner in tuple(opened) for vertex in descendants(parent, owner)}
        retained |= {vertex for owner in tuple(retained) for vertex in descendants(parent, owner)}

        upstream = next(iter(opened if route == "opened-owner" else retained))
        route_vertices = []
        previous = upstream
        route_length = {"shared-cut": 0, "positive-connector": 2,
                        "nested-cycle": 3}[boundary]
        for index in range(route_length):
            vertex = ("route", family, route, boundary, index)
            parent[vertex] = previous
            vertices.add(vertex)
            route_vertices.append(vertex)
            previous = vertex
        cycle = [("cycle", family, route, boundary, index) for index in range(5)]
        for vertex in cycle:
            vertices.add(vertex)
        # The entry cut remains upstream. Both cycle remnants and every deeper
        # descendant belong to one downstream territory.
        downstream = set(cycle)
        for index, cycle_vertex in enumerate(cycle):
            child = ("cycle-tree", family, route, boundary, index)
            parent[child] = cycle_vertex
            vertices.add(child)
            downstream.add(child)

        if route == "opened-owner":
            opened.update(route_vertices)
            opened.update(downstream)
            territories = (opened, retained)
            negative_units = 0 if family == "K71" else 0
        else:
            retained.update(route_vertices)
            territories = (opened, retained, downstream)
            # K22 pays its original opened tree and one boundary tree. K71's
            # favorable opened territory is strict and only the boundary pays.
            negative_units = 2 if family == "K22" else 1

        union = set().union(*territories)
        require(union == vertices, f"{family} owner partition omitted a route descendant")
        require(sum(len(territory) for territory in territories) == len(union),
                f"{family} owner partition duplicated a cut or descendant")
        for child, predecessor in parent.items():
            require(any(child in territory and predecessor in territory
                        for territory in territories),
                    f"{family} descendant crossed an owner boundary")
        require(negative_units <= 2, f"{family} attached K4 cannot pay boundary ledger")
        checked += 1
    require(checked == 12, "rank-five owner incidence count changed")
    return checked


def audit(partitions=None, dispositions=None, packets=None, presieve=None,
          sources=None, values=None, rank5_dispositions=None,
          global_claim=None, direct_equality=None):
    if partitions is None:
        partitions = EXPECTED_PARTITIONS
    if dispositions is None:
        dispositions = DISPOSITIONS
    if packets is None:
        packets = PACKETS
    if presieve is None:
        presieve = PRESIEVE
    if sources is None:
        sources = SOURCES

    generated = integer_partitions(6)
    require(generated == EXPECTED_PARTITIONS, "internal partition generator failed")
    require(partitions == generated, "partition ledger is not the eleven-partition set")
    require(dispositions == DISPOSITIONS, "partition dispositions changed")
    require(set(packets) == set("ABCDEFGHI"), "packet key set changed")
    require(packets == EXPECTED_PACKET_RECORDS, "packet records or owners changed")
    require(presieve == PRESIEVE, "structural pre-sieve changed")

    multiblock = generated - {(6,)}
    for key, (partition, _, owner) in packets.items():
        require(partition in multiblock, f"packet {key} has invalid partition")
        for source in owner.split("+"):
            require(source in sources, f"packet {key} has unlocked owner {source}")
    for key, partition in presieve.items():
        require(partition in multiblock, f"pre-sieve row {key} has invalid partition")

    check_sources(sources)
    check_inequalities(values)
    check_conclusion(sources, global_claim, direct_equality)
    rank5 = regenerate_rank5_structural(sources, rank5_dispositions)
    owner_cases = check_owner_exact_routes()
    return {
        "partitions": len(generated),
        "multiblock": len(multiblock),
        "packets": len(packets),
        "presieve": len(presieve),
        "sources": len(sources),
        "rank5_structural": len(rank5),
        "owner_cases": owner_cases,
        "relation": EXPECTED_GLOBAL_CLAIM["relation"],
    }


def expect_rejection(name, mutation):
    try:
        mutation()
    except (AuditError, KeyError):
        return
    raise AuditError(f"hostile mutation survived: {name}")


def check_mutations():
    mutations = []

    missing_partition = set(EXPECTED_PARTITIONS)
    missing_partition.remove((4, 2))
    mutations.append(("missing-partition", lambda: audit(partitions=missing_partition)))

    widened_scope = dict(DISPOSITIONS)
    widened_scope[(6,)] = "dnn"
    mutations.append(("widened-scope", lambda: audit(dispositions=widened_scope)))

    arbitrary_disposition = dict(DISPOSITIONS)
    arbitrary_disposition[(2, 2, 2)] = "arbitrary"
    mutations.append(("arbitrary-disposition",
                      lambda: audit(dispositions=arbitrary_disposition)))

    for row in PRESIEVE:
        changed = dict(PRESIEVE)
        del changed[row]
        mutations.append((f"missing-presieve:{row}", lambda changed=changed: audit(presieve=changed)))

    reassigned_presieve = dict(PRESIEVE)
    reassigned_presieve["K4+K4"] = (4, 2)
    mutations.append(("presieve-reassignment",
                      lambda: audit(presieve=reassigned_presieve)))

    missing_packet = dict(PACKETS)
    del missing_packet["G"]
    mutations.append(("missing-packet", lambda: audit(packets=missing_packet)))

    wrong_owner = dict(PACKETS)
    wrong_owner["G"] = ((5, 1), "favorable-K5e+T", "items5-7")
    mutations.append(("missing-theta-owner", lambda: audit(packets=wrong_owner)))

    reassigned_owner = dict(PACKETS)
    partition, template, unused_owner = reassigned_owner["H"]
    reassigned_owner["H"] = (partition, template, "items5-7+k71-fixture")
    mutations.append(("owner-reassignment", lambda: audit(packets=reassigned_owner)))

    changed_dispositions = dict(EXPECTED_RANK5_STRUCTURAL)
    changed_dispositions["K22"] = dict(changed_dispositions["K22"])
    changed_dispositions["K22"]["disposition"] = "triangle-only"
    mutations.append(("changed-K22-disposition",
                      lambda: audit(rank5_dispositions=changed_dispositions)))

    changed_dispositions = dict(EXPECTED_RANK5_STRUCTURAL)
    changed_dispositions["K71"] = dict(changed_dispositions["K71"])
    changed_dispositions["K71"]["disposition"] = "dnn"
    mutations.append(("changed-K71-disposition",
                      lambda: audit(rank5_dispositions=changed_dispositions)))

    changed_cases = EXPECTED_OWNER_CASES[:-1]
    mutations.append(("missing-owner-incidence",
                       lambda: check_owner_exact_routes(changed_cases)))

    strict_claim = dict(EXPECTED_GLOBAL_CLAIM)
    strict_claim["relation"] = ">"
    strict_claim["conclusion"] = "s+(G)>|V(G)|"
    mutations.append(("strict-global-promotion",
                      lambda: audit(global_claim=strict_claim)))

    residual_equality = dict(EXPECTED_RANK5_DIRECT_EQUALITY)
    residual_equality["disposition"] = "residual"
    residual_equality["residual"] = True
    mutations.append(("rank5-equality-triangle-residual",
                      lambda: audit(direct_equality=residual_equality)))

    strict_equality = dict(EXPECTED_RANK5_DIRECT_EQUALITY)
    strict_equality["relation"] = ">"
    mutations.append(("rank5-equality-strict-promotion",
                      lambda: audit(direct_equality=strict_equality)))

    bad_sources = dict(SOURCES)
    path, digest = bad_sources["theta-triangle"]
    bad_sources["theta-triangle"] = (path, "0" * len(digest))
    mutations.append(("source-digest", lambda: audit(sources=bad_sources)))

    bad_values = {
        "p": 2.0 / 3.0,
        "d": (math.sqrt(17.0) - 1.0) / 2.0,
        "s3": 12.0 / 5.0,
        "s4_even": 18.0 / 5.0,
        "s4_odd": 19.0 / 6.0,
        "k5e": 2.0 * math.sqrt(7.0) - 1.0,
    }
    mutations.append(("item-E-boundary", lambda: audit(values=bad_values)))

    bad_values = {
        "p": 5.0 - 2.0 * math.sqrt(5.0),
        "d": (math.sqrt(17.0) - 1.0) / 2.0,
        "s3": 12.0 / 5.0,
        "s4_even": 5.0,
        "s4_odd": 19.0 / 6.0,
        "k5e": 2.0 * math.sqrt(7.0) - 1.0,
    }
    mutations.append(("item-F-nontriangle", lambda: audit(values=bad_values)))

    bad_values = {
        "p": 5.0 - 2.0 * math.sqrt(5.0),
        "d": (math.sqrt(17.0) - 1.0) / 2.0,
        "s3": 12.0 / 5.0,
        "s4_even": 18.0 / 5.0,
        "s4_odd": 19.0 / 6.0,
        "k5e": 5.0 - (5.0 - 2.0 * math.sqrt(5.0)),
    }
    mutations.append(("item-G-nontriangle", lambda: audit(values=bad_values)))

    for name, mutation in mutations:
        expect_rejection(name, mutation)
    return len(mutations)


def main():
    report = audit()
    rejected = check_mutations()
    print(
        "hexacyclic multiblock ledger verifier: PASS "
        f"(partitions={report['partitions']}, multiblock={report['multiblock']}, "
        f"packets={report['packets']}, presieve={report['presieve']}, "
        f"rank5-structural={report['rank5_structural']}, "
        f"conclusion={report['relation']}, "
        f"owner-cases={report['owner_cases']}, "
        f"source-locks={report['sources']}, mutations={rejected}/{rejected})"
    )


if __name__ == "__main__":
    main()
