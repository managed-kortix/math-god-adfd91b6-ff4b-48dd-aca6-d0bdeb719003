#!/usr/bin/env python3
"""Exact marked one-interface census for the rank-eleven endpoint A_10 | Q.

This first-stage certificate enumerates every incidence tree and every first
hull mark, applies the established final-owner router search, and freezes the
remaining signatures.  It deliberately makes no closure claim for residual
rows until each residual has an explicit analytic repair.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "rank_ten_a9_one_interface_base", HERE / "rank-ten-a9-one-interface-census.py"
)
BASE = module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("one-interface dependency has no import loader")
sys.modules[SPEC.name] = BASE
SPEC.loader.exec_module(BASE)
BASE.BASE.TRIANGLE_MARGIN[10] = 0


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def enumerate_rows():
    classes = BASE.BASE.BASE.enumerate_colors(("T",) * 10, 0)
    validate_classes(classes)
    rows = {}
    placements = 0
    for incidence_signature, tree in classes:
        positions = BASE.BASE.position_universe(tree)
        placements += len(positions)
        local = {}
        for position in positions:
            pair = (position, position)
            signature = BASE.BASE.marked_signature(tree, pair)
            local.setdefault(
                signature,
                BASE.BASE.Row(signature, incidence_signature, tree, pair, 1),
            )
        for signature, row in local.items():
            require(signature not in rows, f"marked signature crosses incidence classes: {signature}")
            rows[signature] = row
    return tuple(rows[key] for key in sorted(rows)), len(classes), placements


def digest(signatures):
    return sha256(("\n".join(signatures) + "\n").encode("ascii")).hexdigest()


def validate_classes(classes):
    generator = BASE.BASE.BASE
    require(classes, "canonical generator returned no classes")
    signatures = tuple(signature for signature, _ in classes)
    require(signatures == tuple(sorted(signatures)), "canonical classes are not sorted")
    require(len(signatures) == len(set(signatures)), "duplicate canonical incidence signature")
    require(
        digest(signatures) == "694551fd1a0e75251e014bb5e8ab552513ce7074e55c26792de73e51e98b74a7",
        "canonical incidence digest changed",
    )
    for signature, tree in classes:
        require(signature == generator.signature(tree), "noncanonical incidence representative")
        require(tree.colors == ("T",) * 10, "wrong incidence colors")
        adjacency = generator.adjacency(tree)
        require(len(tree.edges) == len(adjacency) - 1, "incidence graph is not a tree")
        seen = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        require(len(seen) == len(adjacency), "incidence graph is disconnected")
        for cycle in range(10):
            require(1 <= len(adjacency[cycle]) <= 3, "triangle capacity violation")
            require(all(cut >= 10 for cut in adjacency[cycle]), "cycle-cycle incidence edge")
        for cut in range(10, len(adjacency)):
            require(len(adjacency[cut]) >= 2, "degree-one cut node")
            require(all(cycle < 10 for cycle in adjacency[cut]), "cut-cut incidence edge")


@dataclass(frozen=True, order=True)
class TerminalOwner:
    kind: str
    index: int


@dataclass(frozen=True)
class FinalOwnership:
    cycle_owners: tuple[tuple[int, TerminalOwner], ...]
    cut_owners: tuple[tuple[int, TerminalOwner], ...]
    interval_owners: tuple[tuple[tuple[int, int], TerminalOwner], ...]
    private_owners: tuple[tuple[tuple[int, int], TerminalOwner], ...]
    mark_owner: TerminalOwner


@dataclass(frozen=True)
class ResidualRepair:
    template: str
    terminal: str
    router: int | None
    hub: int
    leaves: tuple[int, ...]
    opened: tuple[int, ...]
    destroyed: tuple[int, ...]
    packet_cycles: tuple[tuple[str, tuple[int, ...]], ...]
    cut_owners: tuple[tuple[int, str], ...]
    mark_owner: str
    q_owner: str
    credit: int
    deficits: int
    tree_costs: int
    strict: bool


def materialize_final_owners(row, plan):
    """Resolve every nested provisional interval to one terminal territory."""
    adjacency = BASE.BASE.BASE.adjacency(row.tree)
    cycle_count = len(row.tree.colors)
    root = frozenset(range(cycle_count))
    mark = row.positions[0]
    steps = {}
    for step in plan.steps:
        active = frozenset(step.active)
        require(active not in steps, "two routers split the same active territory")
        steps[active] = step

    terminals = {}
    cycle_owner = {}
    for index, packet in enumerate(plan.packet_cycles):
        active = frozenset(packet)
        owner = TerminalOwner("packet", index)
        require(active, "empty retained packet")
        require(active not in terminals, "duplicate terminal packet cycle set")
        terminals[active] = owner
        for cycle in active:
            require(cycle not in cycle_owner, "retained cycle has two owners")
            cycle_owner[cycle] = owner
    require(
        set(cycle_owner) == set(root) - set(plan.routers),
        "terminal packets do not cover exactly the retained cycles",
    )
    q_owner = TerminalOwner("hostile-Q", 0)

    def local_positions(router):
        positions = [BASE.BASE.Position("cut", cut) for cut in adjacency[router]]
        positions.extend(
            BASE.BASE.Position("private", router, slot)
            for slot in range(3 - len(adjacency[router]))
        )
        require(len(positions) == 3, "router does not have three geometric vertices")
        return frozenset(positions)

    def records(step):
        require(len(step.owners) == len(step.interval_sizes), "owner/interval mismatch")
        result = tuple(
            (anchor, frozenset(branch), size)
            for (anchor, branch), size in zip(step.owners, step.interval_sizes)
        )
        require(len(result) in (2, 3), "triangle split has invalid interval count")
        require(
            sorted(size for _, _, size in result)
            == ([1, 2] if len(result) == 2 else [1, 1, 1]),
            "triangle split has invalid interval sizes",
        )
        require(len({anchor for anchor, _, _ in result}) == len(result), "duplicate anchors")
        return result

    def choose(active, site):
        step = steps[active]
        options = records(step)
        local = local_positions(step.router)
        if site in local:
            matches = [record for record in options if record[0] == site]
            if not matches:
                matches = [record for record in options if record[2] == 2]
        elif site.kind == "private":
            matches = [record for record in options if site.vertex in record[1]]
        else:
            support = set(adjacency[site.vertex]) & (set(active) - {step.router})
            require(support, "cut has no support in active territory")
            matches = [record for record in options if support & set(record[1])]
        require(len(matches) == 1, "site does not select a unique child interval")
        return matches[0]

    def resolve(active, site):
        active = frozenset(active)
        if active in terminals:
            return terminals[active]
        require(active in steps, "nonterminal territory has no router split")
        step = steps[active]
        anchor, child, _ = choose(active, site)
        if not child:
            require(anchor == mark, "empty interval is not the marked Q interval")
            return q_owner
        next_site = anchor if site in local_positions(step.router) else site
        return resolve(child, next_site)

    cut_owner = {
        cut: resolve(root, BASE.BASE.Position("cut", cut))
        for cut in range(cycle_count, len(adjacency))
    }
    private_owner = {
        (cycle, slot): resolve(root, BASE.BASE.Position("private", cycle, slot))
        for cycle in range(cycle_count)
        for slot in range(3 - len(adjacency[cycle]))
    }
    interval_owner = {}
    for step in plan.steps:
        owners = []
        for index, (anchor, child, _) in enumerate(records(step)):
            if child:
                owner = resolve(child, anchor)
            else:
                require(anchor == mark, "empty router interval does not carry Q")
                owner = q_owner
            interval_owner[(step.router, index)] = owner
            owners.append(owner)
        require(len(owners) == len(set(owners)), "router intervals coalesce after refinement")

    for cut, owner in cut_owner.items():
        retained = {cycle_owner[cycle] for cycle in adjacency[cut] if cycle in cycle_owner}
        require(len(retained) <= 1, "cut meets multiple terminal packets")
        if retained:
            require(retained == {owner}, "cut owner disagrees with retained packet")
        else:
            require(owner in set(interval_owner.values()), "deleted cut has no interval owner")
    mark_owner = resolve(root, mark)
    require(mark_owner in set(terminals.values()) | {q_owner}, "mark has no terminal owner")
    return FinalOwnership(
        tuple(sorted(cycle_owner.items())), tuple(sorted(cut_owner.items())),
        tuple(sorted(interval_owner.items())), tuple(sorted(private_owner.items())), mark_owner,
    )


def ownership_text(row, plan, ownership):
    def owner_text(owner):
        return f"{owner.kind}:{owner.index}"
    fields = [row.signature]
    fields.extend(f"C{key}={owner_text(value)}" for key, value in ownership.cycle_owners)
    fields.extend(f"X{key}={owner_text(value)}" for key, value in ownership.cut_owners)
    fields.extend(f"I{key[0]}.{key[1]}={owner_text(value)}" for key, value in ownership.interval_owners)
    fields.extend(f"V{key[0]}.{key[1]}={owner_text(value)}" for key, value in ownership.private_owners)
    fields.append(f"M={owner_text(ownership.mark_owner)}")
    fields.append(f"R={','.join(map(str, plan.routers))}")
    return "|".join(fields)


def classify_residual_geometry(row):
    adjacency = BASE.BASE.BASE.adjacency(row.tree)
    cuts = tuple(range(10, len(adjacency)))
    cycles = set(range(10))
    if len(cuts) == 1:
        hub = cuts[0]
        require(set(adjacency[hub]) == cycles, "bouquet cut does not meet all triangles")
        require(all(tuple(adjacency[cycle]) == (hub,) for cycle in cycles), "malformed bouquet")
        return "bouquet", None, hub, (), ()

    routers = [cycle for cycle in cycles if len(adjacency[cycle]) == len(cuts)]
    require(len(routers) == 1, "residual has no unique saturated router")
    router = routers[0]
    if len(cuts) == 2:
        hubs = [cut for cut in cuts if len(adjacency[cut]) == 9]
        require(len(hubs) == 1, "two-cut residual has no unique nine-triangle hub")
        hub = hubs[0]
        leaf_cut = next(cut for cut in cuts if cut != hub)
        require(len(adjacency[leaf_cut]) == 2 and router in adjacency[leaf_cut], "bad leaf cut")
        leaf = next(cycle for cycle in adjacency[leaf_cut] if cycle != router)
        require(tuple(adjacency[leaf]) == (leaf_cut,), "leaf triangle is not an incidence leaf")
        require(set(adjacency[hub]) == cycles - {leaf}, "two-cut hub neighborhood mismatch")
        return "two-cut", router, hub, (leaf,), (leaf_cut,)

    require(len(cuts) == 3, "unknown residual cut count")
    hubs = [cut for cut in cuts if len(adjacency[cut]) == 8]
    require(len(hubs) == 1, "three-cut residual has no unique eight-triangle hub")
    hub = hubs[0]
    leaves = []
    leaf_cuts = []
    for cut in cuts:
        if cut == hub:
            continue
        require(len(adjacency[cut]) == 2 and router in adjacency[cut], "bad three-cut leaf port")
        leaf = next(cycle for cycle in adjacency[cut] if cycle != router)
        require(tuple(adjacency[leaf]) == (cut,), "three-cut leaf is not an incidence leaf")
        leaves.append(leaf)
        leaf_cuts.append(cut)
    require(len(set(leaves)) == 2, "three-cut leaves are not distinct")
    require(set(adjacency[hub]) == cycles - set(leaves), "three-cut hub neighborhood mismatch")
    pairs = tuple(sorted(zip(leaves, leaf_cuts)))
    return "three-cut", router, hub, tuple(leaf for leaf, _ in pairs), tuple(cut for _, cut in pairs)


def make_residual_repair(row):
    template, router, hub, leaves, leaf_cuts = classify_residual_geometry(row)
    mark = row.positions[0]
    all_cycles = set(range(10))
    if template == "bouquet":
        owner = "A10Q"
        return ResidualRepair(template, "packing-one-A10Q", None, hub, (), (), (),
                              ((owner, tuple(range(10))),), ((hub, owner),), owner, owner,
                              10, 1, 0, True)

    if template == "two-cut":
        leaf = leaves[0]
        leaf_cut = leaf_cuts[0]
        hub_cycles = tuple(sorted(all_cycles - {router, leaf}))
        if mark.kind == "private" and mark.vertex == leaf or mark.kind == "cut" and mark.vertex == leaf_cut:
            return ResidualRepair(template, "TQ+A8", router, hub, leaves, (), (router,),
                                  (("TQ", (leaf,)), ("A8", hub_cycles)),
                                  ((hub, "A8"), (leaf_cut, "TQ")), "TQ", "TQ", 0, 0, 0, True)
        if mark.kind == "cut" and mark.vertex == hub or mark.kind == "private" and mark.vertex in hub_cycles:
            return ResidualRepair(template, "A8Q+T", router, hub, leaves, (), (router,),
                                  (("A8Q", hub_cycles), ("T", (leaf,))),
                                  ((hub, "A8Q"), (leaf_cut, "T")), "A8Q", "A8Q", 8, 1, 0, True)
        require(mark.kind == "private" and mark.vertex == router, "unknown two-cut mark orbit")
        retained = tuple(sorted(all_cycles - {leaf}))
        return ResidualRepair(template, "open-leaf+packing-one-A9Q", router, hub, leaves,
                              (leaf,), (), (("A9Q", retained), ("opened-tree", ())),
                              ((hub, "A9Q"), (leaf_cut, "A9Q")), "A9Q", "A9Q", 9, 1, 1, True)

    require(template == "three-cut", "unknown residual template")
    marked_leaf = next((leaf for leaf in leaves if mark.kind == "private" and mark.vertex == leaf), None)
    marked_cut_leaf = next((leaf for leaf, cut in zip(leaves, leaf_cuts)
                            if mark.kind == "cut" and mark.vertex == cut), None)
    q_leaf = marked_leaf if marked_leaf is not None else marked_cut_leaf
    hub_cycles = tuple(sorted(all_cycles - {router} - set(leaves)))
    if q_leaf is not None:
        other = next(leaf for leaf in leaves if leaf != q_leaf)
        cut_owner = tuple((cut, "TQ" if leaf == q_leaf else "T")
                          for leaf, cut in zip(leaves, leaf_cuts)) + ((hub, "A7"),)
        return ResidualRepair(template, "A7+TQ+T", router, hub, leaves, (), (router,),
                              (("A7", hub_cycles), ("TQ", (q_leaf,)), ("T", (other,))),
                              tuple(sorted(cut_owner)), "TQ", "TQ", 0, 0, 0, True)
    require(mark.kind == "cut" and mark.vertex == hub, "unknown three-cut mark orbit")
    retained = tuple(sorted(all_cycles - set(leaves)))
    cut_owner = tuple((cut, "A8Q") for cut in (hub,) + leaf_cuts)
    return ResidualRepair(template, "open-two-leaves+packing-one-A8Q", router, hub, leaves,
                          leaves, (), (("A8Q", retained), ("tree-1", ()), ("tree-2", ())),
                          tuple(sorted(cut_owner)), "A8Q", "A8Q", 8, 1, 2, True)


def verify_residual_repair(row, repair):
    template, router, hub, leaves, leaf_cuts = classify_residual_geometry(row)
    require((repair.template, repair.router, repair.hub, repair.leaves) ==
            (template, router, hub, leaves), "repair geometry fields changed")
    adjacency = BASE.BASE.BASE.adjacency(row.tree)
    mark = row.positions[0]
    packets = dict(repair.packet_cycles)
    require(len(packets) == len(repair.packet_cycles), "duplicate repair packet")
    require(repair.q_owner in packets and repair.mark_owner == repair.q_owner,
            "Q and marked connector do not have one common packet owner")
    retained = [cycle for cycles in packets.values() for cycle in cycles]
    require(Counter(retained) == Counter(set(range(10)) - set(repair.opened) - set(repair.destroyed)),
            "repair cycle ledger is not exact")
    require(set(repair.opened).isdisjoint(repair.destroyed), "cycle both opened and destroyed")
    cut_owner = dict(repair.cut_owners)
    require(len(cut_owner) == len(repair.cut_owners) and set(cut_owner) == set(range(10, len(adjacency))),
            "repair cut-owner ledger is not exact")
    require(set(cut_owner.values()) <= set(packets), "repair cut has no packet owner")
    if mark.kind == "cut":
        require(cut_owner[mark.vertex] == repair.mark_owner, "marked cut has wrong final owner")
    elif mark.vertex not in repair.opened and mark.vertex not in repair.destroyed:
        require(mark.vertex in packets[repair.mark_owner], "retained private mark has wrong owner")
    else:
        require(mark.vertex in repair.destroyed, "marked private connector was charged as opened tree")

    for opened in repair.opened:
        require(len(adjacency[opened]) == 1, "opened triangle is not a leaf")
        require(cut_owner[adjacency[opened][0]] == repair.q_owner,
                "opened leaf cut does not remain with cyclic Q packet")
        require(3 - len(adjacency[opened]) == 2, "opened leaf lacks a two-vertex private interval")
    if repair.terminal.startswith("packing-one-A10Q"):
        require(len(set(adjacency[hub]) & set(packets[repair.q_owner])) == 10, "A10Q not common-hub")
    if "packing-one-A9Q" in repair.terminal:
        require(set(packets[repair.q_owner]) == set(adjacency[hub]), "A9Q not common-hub")
    if repair.terminal == "A8Q+T":
        require(set(packets[repair.q_owner]) == set(adjacency[hub]) - {router}, "split A8Q not common-hub")
    if "packing-one-A8Q" in repair.terminal:
        require(set(packets[repair.q_owner]) == set(adjacency[hub]), "retained A8Q not common-hub")
    if repair.terminal == "TQ+A8":
        require(len(packets["TQ"]) == 1 and len(packets["A8"]) == 8, "TQ+A8 profile mismatch")
    if repair.terminal == "A7+TQ+T":
        require((len(packets["A7"]), len(packets["TQ"]), len(packets["T"])) == (7, 1, 1),
                "A7+TQ+T profile mismatch")
    require(repair.credit - repair.deficits - repair.tree_costs >= 0,
            "repair ledger cannot beat delta<1")
    require(repair.strict, "repair ledger lacks strict packet")


def repair_text(row, repair):
    return "|".join((row.signature, repair.template, repair.terminal,
                     f"R={repair.router}", f"H={repair.hub}", f"L={repair.leaves}",
                     f"O={repair.opened}", f"D={repair.destroyed}",
                     f"P={repair.packet_cycles}", f"X={repair.cut_owners}",
                     f"M={repair.mark_owner}", f"Q={repair.q_owner}",
                     f"ledger={repair.credit},{repair.deficits},{repair.tree_costs},{int(repair.strict)}"))


def verify_owner(row, plan):
    BASE.BASE.verify_interval_realization(row, plan)
    position = row.positions[0]
    removed = set(plan.routers)
    realized = {marked for step in plan.steps for marked, _ in step.owners}
    if position.kind == "private" and position.vertex in removed:
        require(position in realized, "private Q connector has no router interval")
    elif position.kind == "private":
        require(
            any(position.vertex in packet for packet in plan.packet_cycles),
            "private Q connector has no retained packet owner",
        )
    else:
        adjacency = BASE.BASE.BASE.adjacency(row.tree)
        require(
            position in realized
            or any(
                cycle in packet
                for packet in plan.packet_cycles
                for cycle in adjacency[position.vertex]
            ),
            "cut Q connector has no owner",
        )


def main():
    rows, incidence_count, placements = enumerate_rows()
    scores = Counter()
    routers = Counter()
    residuals = []
    owner_records = []
    for row in rows:
        plan = BASE.BASE.best_plan(row)
        scores[plan.credit] += 1
        routers[len(plan.routers)] += 1
        if plan.credit < 1:
            residuals.append(row)
        else:
            verify_owner(row, plan)
            ownership = materialize_final_owners(row, plan)
            owner_records.append(ownership_text(row, plan, ownership))

    row_digest = digest(row.signature for row in rows)
    residual_digest = digest(row.signature for row in residuals)
    owner_digest = digest(owner_records)
    repairs = tuple(make_residual_repair(row) for row in residuals)
    for row, repair in zip(residuals, repairs):
        verify_residual_repair(row, repair)
    repair_digest = digest(repair_text(row, repair) for row, repair in zip(residuals, repairs))
    cut_distribution = Counter(BASE.BASE.BASE.cut_count(row.tree) for row in residuals)

    print("ten-triangle incidence trees:", incidence_count)
    print("labelled interface placements before automorphisms:", placements)
    print("canonical marked one-interface rows:", len(rows))
    print("router accepted:", len(rows) - len(residuals))
    print("ordinary-router residuals:", len(residuals))
    print("credit distribution:", dict(sorted(scores.items())))
    print("router distribution:", dict(sorted(routers.items())))
    print("residual cut distribution:", dict(sorted(cut_distribution.items())))
    print("canonical-row sha256:", row_digest)
    print("canonical-residual sha256:", residual_digest)
    print("final-owner sha256:", owner_digest)
    print("repair types:", dict(sorted(Counter(repair.terminal for repair in repairs).items())))
    print("repair sha256:", repair_digest)
    for index, row in enumerate(residuals, 1):
        mark = row.positions[0]
        print(f"R{index}: cuts={BASE.BASE.BASE.cut_count(row.tree)} mark={mark} {row.signature}")

    require(incidence_count == 1037, "incidence count changed")
    require(placements == 21777, "placement count changed")
    require(len(rows) == 12099, "canonical marked count changed")
    require(
        scores == Counter({0: 10, 1: 15, 2: 26, 3: 161, 4: 1561, 5: 6190, 6: 4136}),
        "credit census changed",
    )
    require(routers == Counter({0: 10, 1: 7859, 2: 4192, 3: 38}), "router census changed")
    require(cut_distribution == Counter({1: 2, 2: 5, 3: 3}), "residual cuts changed")
    require(len(residuals) == 10, "residual total changed")
    require(row_digest == "8db6255acb0e663ea2d2c16ec4ffc0c329dae1cc8d7bb396eebd69aaa6b50402", "canonical row digest changed")
    require(residual_digest == "cb3daea744bf96c12f60b0a2028c4353c4b239a5cd36029cb75b7d16dff6d325", "canonical residual digest changed")
    require(owner_digest == "9600bb00f1f1fbf6e4cc74141fa2a4a27be9c781b785076492dff35021077479", "final-owner digest changed")
    require(Counter(repair.terminal for repair in repairs) == Counter({"packing-one-A10Q": 2, "TQ+A8": 2, "A8Q+T": 2, "open-leaf+packing-one-A9Q": 1, "A7+TQ+T": 2, "open-two-leaves+packing-one-A8Q": 1}), "repair type census changed")
    require(repair_digest == "5c0f91e0d8953425521030928b282e64f2e91be7140344613e30e67b236e7df3", "repair digest changed")
    print("exact endpoint closure: 12099 = 12089 + 10")


if __name__ == "__main__":
    main()
