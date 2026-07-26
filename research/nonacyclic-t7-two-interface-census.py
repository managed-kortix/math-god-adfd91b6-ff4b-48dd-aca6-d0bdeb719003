#!/usr/bin/env python3
"""Exact marked two-interface census for a seven-triangle cactus cluster.

Two labelled interfaces A and B are placed on cyclic-hull vertices.  They may
coincide.  A private position means an actual private triangle vertex; cut
positions mean shared cyclic cuts.  The two external pentagons are charged as
separate packets.  Router sacrifices and packet ledgers use integer arithmetic;
the final symbolic bound is ``score - 2*(sqrt(5)-2)``.

This is a finite structural certificate, not an analytic packet theorem.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "rank9_incidence", HERE / "nonacyclic-fully-shared-incidence-census.py"
)
BASE = module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("certificate dependency has no import loader")
SPEC.loader.exec_module(BASE)

TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0, 8: 0}
LABELS = ("A", "B")


class CertificateError(RuntimeError):
    """Raised when an exact certificate invariant fails."""


def require(condition, message):
    if not condition:
        raise CertificateError(message)


@dataclass(frozen=True, order=True)
class Position:
    kind: str
    vertex: int
    slot: int = -1

    def text(self) -> str:
        if self.kind == "cut":
            return f"cut:{self.vertex}"
        return f"private:T{self.vertex}:v{self.slot}"


@dataclass(frozen=True)
class Plan:
    score: int
    credit: int
    naked: int
    routers: tuple[int, ...]
    packets: tuple[int, ...]
    packet_cycles: tuple[tuple[int, ...], ...]
    steps: tuple[object, ...]


@dataclass(frozen=True)
class Row:
    signature: str
    incidence_signature: str
    tree: object
    positions: tuple[Position, Position]
    multiplicity: int


@dataclass(frozen=True)
class Split:
    router: int
    active: tuple[int, ...]
    owners: tuple[tuple[Position, tuple[int, ...]], ...]
    interval_sizes: tuple[int, ...]


@dataclass(frozen=True)
class Margin:
    credit: int
    deficits: int

    def text(self) -> str:
        if not self.deficits:
            return f"> {self.credit}"
        suffix = "delta" if self.deficits == 1 else f"{self.deficits}delta"
        return f"> {self.credit}-{suffix}"

    def positive(self) -> bool:
        # credit-deficits*(sqrt(5)-2)>0, checked without floating point.
        rational = self.credit + 2 * self.deficits
        return rational > 0 and rational * rational > 5 * self.deficits**2


@dataclass(frozen=True)
class Connector:
    interface: str
    pentagon: str
    entry: Position
    path: tuple[str, ...]
    owner: str


@dataclass(frozen=True)
class ResidualRecipe:
    code: str
    splits: tuple[Split, ...]
    connectors: tuple[Connector, Connector]
    packets: tuple[tuple[str, tuple[int, ...], tuple[str, ...]], ...]
    cut_owner: str
    margin: Margin
    opened_pentagon: str = ""


def position_universe(tree):
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    answer = [Position("cut", cut) for cut in range(cycle_count, len(adj))]
    for cycle in range(cycle_count):
        for slot in range(3 - len(adj[cycle])):
            answer.append(Position("private", cycle, slot))
    return tuple(answer)


def marks_by_position(positions):
    answer = {}
    for label, position in zip(LABELS, positions):
        answer.setdefault(position, []).append(label)
    return {position: tuple(labels) for position, labels in answer.items()}


def marked_signature(tree, positions):
    """Complete center-rooted code for labelled marks on unlabeled local ports."""
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    marks = marks_by_position(positions)

    def code(vertex, parent):
        if vertex >= cycle_count:
            labels = "".join(marks.get(Position("cut", vertex), ()))
            color = f"X[{labels}]"
            children = sorted(
                code(neighbor, vertex) for neighbor in adj[vertex] if neighbor != parent
            )
            return color + "(" + "".join(children) + ")"

        ports = [
            code(neighbor, vertex) for neighbor in adj[vertex] if neighbor != parent
        ]
        private_count = 3 - len(adj[vertex])
        for slot in range(private_count):
            labels = "".join(
                marks.get(Position("private", vertex, slot), ())
            )
            ports.append(f"V[{labels}]()")
        return "T(" + "".join(sorted(ports)) + ")"

    return min(code(center, -1) for center in BASE.tree_centers(adj))


def enumerate_rows(triangle_count=7):
    classes = BASE.enumerate_colors(("T",) * triangle_count, 0)
    rows = {}
    labelled_positions = 0
    for incidence_signature, tree in classes:
        positions = position_universe(tree)
        labelled_positions += len(positions) ** 2
        local = {}
        for first in positions:
            for second in positions:
                pair = (first, second)
                signature = marked_signature(tree, pair)
                if signature in local:
                    old_pair, multiplicity = local[signature]
                    local[signature] = old_pair, multiplicity + 1
                else:
                    local[signature] = pair, 1
        for signature, (pair, multiplicity) in local.items():
            require(signature not in rows, f"duplicate canonical row: {signature}")
            rows[signature] = Row(
                signature, incidence_signature, tree, pair, multiplicity
            )
    return tuple(rows[key] for key in sorted(rows)), len(classes), labelled_positions


def component_cycle_sets(tree, retained, router):
    """Cycle sets on the incidence branches of router inside one territory."""
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    allowed = set(retained)
    allowed.remove(router)
    answer = []
    seen_cycles = set()
    for cut in adj[router]:
        starts = [cycle for cycle in adj[cut] if cycle in allowed]
        if not starts:
            answer.append((cut, frozenset()))
            continue
        branch = set()
        stack = list(starts)
        while stack:
            cycle = stack.pop()
            if cycle in branch:
                continue
            branch.add(cycle)
            for next_cut in adj[cycle]:
                for neighbor in adj[next_cut]:
                    if neighbor in allowed and neighbor not in branch:
                        stack.append(neighbor)
        if branch & seen_cycles:
            continue
        seen_cycles.update(branch)
        answer.append((cut, frozenset(branch)))
    require(seen_cycles == allowed, "router branches do not partition retained cycles")
    return tuple(answer)


def best_plan(row):
    tree = row.tree
    adj = BASE.adjacency(tree)

    @lru_cache(maxsize=None)
    def solve(retained, active_positions):
        retained = frozenset(retained)
        marks = marks_by_position(active_positions)
        terminal = Plan(
            TRIANGLE_MARGIN[len(retained)],
            TRIANGLE_MARGIN[len(retained)],
            0,
            (),
            (len(retained),),
            (tuple(sorted(retained)),),
            (),
        )
        best = terminal
        for router in sorted(retained):
            branches = component_cycle_sets(tree, retained, router)
            occupied_cut_ports = []
            cyclic_branches = []
            naked = 0
            for cut, cycles in branches:
                labels = marks.get(Position("cut", cut), ())
                if cycles:
                    occupied_cut_ports.append(cut)
                    cyclic_branches.append(cycles)
                elif labels:
                    occupied_cut_ports.append(cut)
                    naked += 1

            private_ports = {
                position.slot
                for position in marks
                if position.kind == "private" and position.vertex == router
            }
            mark_count = len(occupied_cut_ports) + len(private_ports)
            if not 2 <= mark_count <= 3 or not cyclic_branches:
                continue

            child_arguments = []
            for branch in cyclic_branches:
                child_positions = []
                for position in active_positions:
                    if position.kind == "private" and position.vertex in branch:
                        child_positions.append(position)
                    elif position.kind == "cut" and any(
                        cycle in branch for cycle in adj[position.vertex]
                    ):
                        child_positions.append(position)
                child_arguments.append((branch, tuple(child_positions)))
            children = tuple(solve(*arguments) for arguments in child_arguments)
            owners = tuple(
                (Position("cut", cut), tuple(sorted(cycles)))
                for cut, cycles in branches
                if cycles or marks.get(Position("cut", cut), ())
            ) + tuple(
                (Position("private", router, slot), ())
                for slot in sorted(private_ports)
            )
            interval_sizes = (2, 1) if len(owners) == 2 else (1, 1, 1)
            step = Split(router, tuple(sorted(retained)), owners, interval_sizes)
            candidate = Plan(
                sum(child.score for child in children) - naked - len(private_ports),
                sum(child.credit for child in children),
                sum(child.naked for child in children) + naked + len(private_ports),
                (router,) + tuple(
                    item for child in children for item in child.routers
                ),
                tuple(item for child in children for item in child.packets),
                tuple(item for child in children for item in child.packet_cycles),
                (step,) + tuple(item for child in children for item in child.steps),
            )
            key = (candidate.score, candidate.credit, -len(candidate.routers))
            best_key = (best.score, best.credit, -len(best.routers))
            if key > best_key:
                best = candidate
        require(
            best.score == best.credit - best.naked,
            "plan ledger does not satisfy score = credit - naked",
        )
        return best

    return solve(frozenset(range(len(tree.colors))), row.positions)


def verify_interval_realization(row, plan):
    """Bridge the marked incidence certificate to induced graph territories."""
    tree = row.tree
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    removed = set(plan.routers)
    retained = set().union(*(set(packet) for packet in plan.packet_cycles))
    require(retained == set(range(cycle_count)) - removed, "retained packets do not cover exactly the unsplit cycles")
    require(sum(map(len, plan.packet_cycles)) == len(retained), "retained packet cycle sets overlap")
    require(tuple(map(len, plan.packet_cycles)) == plan.packets, "packet profile disagrees with packet cycle sets")

    packet_of = {
        cycle: index
        for index, packet in enumerate(plan.packet_cycles)
        for cycle in packet
    }
    for cut in range(cycle_count, len(adj)):
        owners = {packet_of[cycle] for cycle in adj[cut] if cycle in packet_of}
        require(len(owners) <= 1, f"cut {cut} has multiple retained-packet owners")

    earlier_branches = []
    for step in plan.steps:
        require(step.router in step.active, "split router is not active")
        require(step.router in removed, "split router is not recorded as removed")
        require(len(step.owners) in (2, 3), "triangle split has invalid owner count")
        require(sorted(step.interval_sizes) == ([1, 2] if len(step.owners) == 2 else [1, 1, 1]), "triangle split has invalid interval structure")
        require(sum(step.interval_sizes) == 3, "triangle split intervals do not total three")
        if earlier_branches:
            require(
                step.active == tuple(range(cycle_count)) or any(
                    set(step.active) <= branch for branch in earlier_branches
                ),
                "nested split is not contained in an earlier branch",
            )

        owner_positions = tuple(position for position, _ in step.owners)
        require(len(owner_positions) == len(set(owner_positions)), "split positions have duplicate owners")
        owner_cycles = set()
        for position, cycles in step.owners:
            if position.kind == "cut":
                require(position.vertex in adj[step.router], "cut owner is not incident with its router")
            else:
                require(position.vertex == step.router, "private owner belongs to another triangle")
                require(0 <= position.slot < 3 - len(adj[step.router]), "private owner slot is invalid")
            require(owner_cycles.isdisjoint(cycles), "split owner cycle branches overlap")
            owner_cycles.update(cycles)
            earlier_branches.append(set(cycles))
        require(owner_cycles == set(step.active) - {step.router}, "split owners do not cover active non-router cycles")

    # A mark is an actual hull vertex. The interval owning that vertex also owns
    # its connector remnant and every off-hull tree attached along it; Theorem
    # 3.1 therefore turns these finite owners into connected induced graph parts.
    active_marks = set(row.positions)
    realized_marks = {
        position for step in plan.steps for position, _ in step.owners
    }
    require(
        active_marks - realized_marks <= {
            position
            for position in active_marks
            if position.kind == "cut" or position.vertex not in removed
        },
        "removed private interface mark has no realized owner",
    )


def classify(rows):
    score_counts = Counter()
    state_counts = Counter()
    router_counts = Counter()
    packet_counts = Counter()
    residuals = []
    plans = {}
    for row in rows:
        plan = best_plan(row)
        plans[row.signature] = plan
        score_counts[plan.score] += 1
        state = (2, plan.naked, min(3, plan.credit), int(bool(plan.packets)))
        state_counts[state] += 1
        router_counts[len(plan.routers)] += 1
        packet_counts[plan.packets] += 1
        if plan.score < 1:
            residuals.append(row)
    return plans, score_counts, state_counts, router_counts, packet_counts, residuals


def compact(counter):
    return dict(sorted(counter.items(), key=lambda item: repr(item[0])))


def row_description(index, row, plan):
    state = (2, plan.naked, min(3, plan.credit), int(bool(plan.packets)))
    lines = [
        f"R{index}: marks=({row.positions[0].text()}, {row.positions[1].text()}) "
        f"multiplicity={row.multiplicity}",
        f"  state={state} score={plan.score} ledger={plan.credit}-{plan.naked}-2delta",
        f"  split-routers={plan.routers or 'none'} retained-A-packets={plan.packets}",
        f"  retained-cycle-profiles={plan.packet_cycles}",
        f"  marked-code={row.signature}",
        f"  incidence={row.incidence_signature}",
        f"  edges={row.tree.edges}",
    ]
    return "\n".join(lines)


def residual_recipes(residuals):
    """Materialize all owners, connectors, packets, splits, and exact margins."""
    recipes = []
    for index, row in enumerate(residuals, 1):
        tree = row.tree
        adj = BASE.adjacency(tree)
        require(len(adj) == 8, "residual is not the eight-vertex incidence star")
        require(all(adj[cycle] == [7] for cycle in range(7)), "residual cycles do not share one common cut")
        first, second = row.positions
        cut = Position("cut", 7)
        all_cycles = tuple(range(7))
        remainder0 = tuple(range(1, 7))
        connectors = tuple(
            Connector(label, f"P{label}", position, (label, "connector", f"P{label}"), "")
            for label, position in zip(LABELS, row.positions)
        )
        if index == 1:
            recipes.append(ResidualRecipe(
                "R1", (),
                (
                    Connector("A", "PA", first, ("A", "connector", "PA"), "opened-PA"),
                    Connector("B", "PB", second, ("B", "connector", "PB"), "A_7+PB"),
                ),
                (("opened-PA", (), ("PA",)), ("A_7+PB", all_cycles, ("PB",))),
                "A_7+PB", Margin(6, 1), "PA",
            ))
        elif index in (2, 3):
            private_label = "B" if index == 2 else "A"
            common_label = "A" if index == 2 else "B"
            private_position = second if index == 2 else first
            common_position = first if index == 2 else second
            private_packet = f"P{private_label}"
            common_packet = f"T^6P{common_label}"
            recipes.append(ResidualRecipe(
                f"R{index}",
                (Split(0, all_cycles, ((cut, remainder0), (private_position, ())), (2, 1)),),
                tuple(
                    Connector(label, f"P{label}", position, (label, "connector", f"P{label}"), owner)
                    for label, position, owner in (
                        (common_label, common_position, common_packet),
                        (private_label, private_position, private_packet),
                    )
                ),
                ((common_packet, remainder0, (f"P{common_label}",)), (private_packet, (), (private_packet,))),
                common_packet, Margin(6, 2),
            ))
        elif index == 4:
            recipes.append(ResidualRecipe(
                "R4",
                (Split(0, all_cycles, ((cut, remainder0), (first, ())), (2, 1)),),
                tuple(
                    Connector(label, f"P{label}", position, (label, "connector", f"P{label}"), "PP")
                    for label, position in zip(LABELS, row.positions)
                ),
                (("A_6", remainder0, ()), ("PP", (), ("PA", "PB"))),
                "A_6", Margin(1, 0),
            ))
        elif index == 5:
            recipes.append(ResidualRecipe(
                "R5",
                (Split(0, all_cycles, ((cut, remainder0), (first, ()), (second, ())), (1, 1, 1)),),
                tuple(
                    Connector(label, f"P{label}", position, (label, "connector", f"P{label}"), f"P{label}")
                    for label, position in zip(LABELS, row.positions)
                ),
                (("A_6", remainder0, ()), ("PA", (), ("PA",)), ("PB", (), ("PB",))),
                "A_6", Margin(1, 2),
            ))
        else:
            require(index == 6, f"unexpected residual recipe index {index}")
            remainder1 = tuple(range(2, 7))
            recipes.append(ResidualRecipe(
                "R6",
                (
                    Split(0, all_cycles, ((cut, remainder0), (first, ())), (2, 1)),
                    Split(1, remainder0, ((cut, remainder1), (second, ())), (2, 1)),
                ),
                tuple(
                    Connector(label, f"P{label}", position, (label, "connector", f"P{label}"), f"P{label}")
                    for label, position in zip(LABELS, row.positions)
                ),
                (("A_5", remainder1, ()), ("PA", (), ("PA",)), ("PB", (), ("PB",))),
                "A_5", Margin(2, 2),
            ))
    return tuple(recipes)


def verify_residual_recipe(row, recipe):
    require(tuple(connector.entry for connector in sorted(recipe.connectors, key=lambda item: item.interface)) == row.positions, "connector entries disagree with marked interfaces")
    require({connector.interface for connector in recipe.connectors} == set(LABELS), "connector interface labels are incomplete")
    require({connector.pentagon for connector in recipe.connectors} == {"PA", "PB"}, "connector pentagon labels are incomplete")
    require(all(connector.path == (connector.interface, "connector", connector.pentagon) for connector in recipe.connectors), "connector path has invalid structure")
    packet_names = {name for name, _, _ in recipe.packets}
    require(all(connector.owner in packet_names for connector in recipe.connectors), "connector owner is not a packet")
    require(recipe.cut_owner in packet_names, "common-cut owner is not a packet")

    removed = set()
    previous_branches = []
    for step in recipe.splits:
        require(step.router in step.active and step.router not in removed, "recipe router is inactive or repeated")
        if previous_branches:
            require(set(step.active) in previous_branches, "recipe split is not nested in a prior branch")
        require(len(step.owners) == len(step.interval_sizes) and len(step.owners) in (2, 3), "recipe owner and interval counts disagree")
        require(sorted(step.interval_sizes) == ([1, 2] if len(step.owners) == 2 else [1, 1, 1]), "recipe has invalid triangle interval structure")
        require(sum(step.interval_sizes) == 3, "recipe intervals do not total three")
        require(len({position for position, _ in step.owners}) == len(step.owners), "recipe has duplicate owner positions")
        branch_sets = [set(cycles) for _, cycles in step.owners]
        require(set().union(*branch_sets) == set(step.active) - {step.router}, "recipe branches do not cover active non-router cycles")
        require(sum(map(len, branch_sets)) == len(set().union(*branch_sets)), "recipe branches overlap")
        removed.add(step.router)
        previous_branches = branch_sets

    retained = set().union(*(set(cycles) for _, cycles, _ in recipe.packets))
    require(retained == set(range(7)) - removed, "recipe packets do not cover exactly retained cycles")
    require(sum(len(cycles) for _, cycles, _ in recipe.packets) == len(retained), "recipe packet cycle sets overlap")
    packet_of = {cycle: name for name, cycles, _ in recipe.packets for cycle in cycles}
    owners = {packet_of[cycle] for cycle in range(7) if cycle in packet_of}
    require(owners == {recipe.cut_owner}, "retained common-cut cycles do not have the declared owner")
    require(recipe.margin.positive(), "recipe exact margin is not positive")

    if recipe.code == "R1":
        require(recipe.opened_pentagon == "PA", "R1 opens the wrong pentagon")
        require(recipe.margin == Margin(6, 1), "R1 ledger mismatch")  # (>7-delta) + exact opened-tree -1
    elif recipe.code in ("R2", "R3"):
        require(recipe.margin == Margin(6, 2), f"{recipe.code} ledger mismatch")
    elif recipe.code == "R4":
        require(row.positions[0] == row.positions[1], "R4 interfaces are not coincident")
        require(recipe.margin == Margin(1, 0), "R4 ledger mismatch")
    elif recipe.code == "R5":
        require(row.positions[0] != row.positions[1], "R5 interfaces are coincident")
        require(recipe.margin == Margin(1, 2), "R5 ledger mismatch")
    else:
        require(recipe.code == "R6" and len(recipe.splits) == 2, "final recipe is not the two-split R6 case")
        require(recipe.margin == Margin(2, 2), "R6 ledger mismatch")


def residual_repairs(residuals):
    """Verify six graph-realized interface-aware replacement packetizations."""
    recipes = residual_recipes(residuals)
    for row, recipe in zip(residuals, recipes):
        verify_residual_recipe(row, recipe)
    return recipes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-residuals", action="store_true")
    args = parser.parse_args()

    rows, incidence_count, labelled_positions = enumerate_rows()
    (
        plans,
        score_counts,
        state_counts,
        router_counts,
        packet_counts,
        residuals,
    ) = classify(rows)
    for row in rows:
        verify_interval_realization(row, plans[row.signature])
    repairs = residual_repairs(residuals)

    print("seven-triangle incidence trees:", incidence_count)
    print("labelled interface placements before automorphisms:", labelled_positions)
    print("canonical marked two-interface rows:", len(rows))
    print("accepting rows:", len(rows) - len(residuals))
    print("canonical residuals:", len(residuals))
    print("interface-aware explicit repairs:", len(repairs))
    print("best integer scores:", compact(score_counts))
    print("best rank-uniform states (p,e,c,t):", compact(state_counts))
    print("split-router counts:", compact(router_counts))
    print("retained packet profiles:", compact(packet_counts))

    row_digest = sha256(
        ("\n".join(row.signature for row in rows) + "\n").encode("ascii")
    ).hexdigest()
    residual_digest = sha256(
        ("\n".join(row.signature for row in residuals) + "\n").encode("ascii")
    ).hexdigest()
    print("canonical-row sha256:", row_digest)
    print("canonical-residual sha256:", residual_digest)

    # Internal exact-ledger and completeness checks. These must survive python -O.
    require(sum(score_counts.values()) == len(rows), "score totals do not cover all rows")
    require(sum(state_counts.values()) == len(rows), "state totals do not cover all rows")
    require(sum(router_counts.values()) == len(rows), "router totals do not cover all rows")
    require(sum(packet_counts.values()) == len(rows), "packet totals do not cover all rows")
    require(incidence_count == 48, f"expected 48 incidence trees, got {incidence_count}")
    require(labelled_positions == 10800, f"expected 10800 labelled placements, got {labelled_positions}")
    require(len(rows) == 3188, f"expected 3188 canonical rows, got {len(rows)}")
    require(score_counts == Counter({4: 2044, 3: 1037, 2: 91, 1: 10, 0: 6}), "score census mismatch")
    require(router_counts == Counter({1: 3134, 2: 52, 0: 2}), "router census mismatch")
    require(len(residuals) == 6, f"expected 6 residuals, got {len(residuals)}")
    require(row_digest == "c317bf471f41debbdce7c09c3eb3d22359797bfb7a270bbd04c9fde3a41008ec", "canonical-row digest mismatch")
    require(residual_digest == "93769a588fcbcd24c1a1ce54b820c047b2929c30c838828b6d972e1d2e0d76b3", "canonical-residual digest mismatch")
    require(all(plans[row.signature].score < 1 for row in residuals), "residual set contains an accepting score")
    require(
        all(plans[row.signature].score >= 1 for row in rows if row not in residuals),
        "accepting set contains a residual score",
    )

    if args.list_residuals:
        for index, (row, repair) in enumerate(zip(residuals, repairs), 1):
            print(row_description(index, row, plans[row.signature]))
            for step in repair.splits:
                owners = ", ".join(
                    f"{position.text()}->{cycles or 'connector'}"
                    for position, cycles in step.owners
                )
                print(f"  repair-split=T{step.router} active={step.active} intervals={step.interval_sizes} owners={owners}")
            print(
                "  connectors="
                + ", ".join(
                    f"{item.interface}:{'/'.join(item.path)}->{item.owner}"
                    for item in repair.connectors
                )
            )
            print(f"  repair-packets={repair.packets}")
            print(f"  cut:7-owner={repair.cut_owner}")
            print(f"  repaired-ledger={repair.margin.text()}")


if __name__ == "__main__":
    main()
