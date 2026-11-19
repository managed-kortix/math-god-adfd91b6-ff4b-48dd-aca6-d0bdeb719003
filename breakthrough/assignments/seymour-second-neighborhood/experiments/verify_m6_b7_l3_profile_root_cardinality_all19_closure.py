#!/usr/bin/env python3
"""Compose the 18-profile ledger and position-14 refinement into all-19 closure."""

import argparse
from pathlib import Path

import check_m6_b7_l3_position14_terminal_refinement as terminal_cover
import m6_b7_l3_profile_root_cardinality as profiles
import verify_m6_b7_l3_position14_terminal_refinement_certificates as terminal
import verify_m6_b7_l3_profile_root_cardinality_except_position14_certificates as eighteen


def composition():
    campaign = profiles.load_profiles()
    eighteen_metadata, eighteen_rows = eighteen.load_ledger()
    terminal_metadata, terminal_rows = terminal.load_ledger()
    profile_positions = tuple(sorted({int(row["position"]) for row in eighteen_rows} | {14}))
    all_parents = {(accepted, cover) for profile in campaign for accepted, cover, _ in profile[7]}
    position14_parents = {(accepted, cover) for accepted, cover, _ in campaign[14][7]}
    leaves = terminal_cover.derive_cover()
    leaf_parents = {(accepted, cover) for _, _, _, _, members in leaves for accepted, cover, _ in members}
    assignments = {(accepted, cover, high_a) for _, _, _, high_a, members in leaves
                   for accepted, cover, _ in members}
    if profile_positions != tuple(range(19)) or len(campaign) != 19 or len(all_parents) != 5016 or \
            sum(len(profile[7]) for profile in campaign) != 32574:
        raise RuntimeError("19-profile/5016-parent campaign census changed")
    if position14_parents != leaf_parents or len(position14_parents) != 1269 or len(assignments) != 5076:
        raise RuntimeError("position-14 terminal refinement does not close its profile")
    if eighteen_metadata["parents"] != "5016" or terminal_metadata["parents"] != "1269" or \
            len(eighteen_rows) != 18 or len(terminal_rows) != 60:
        raise RuntimeError("component ledger scope changed")
    print("PASS closure=all19 profiles=19 disjoint=yes exhaustive=yes")
    print("PASS parents=5016 profile_parent_incidences=32574 position14_parents=1269 assignments=5076 leaves=60")
    print("PASS implication=entire-clean-B7-l3-parent-campaign-closed other-residual-groups=not-claimed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--no-replay", action="store_true")
    parser.add_argument("--representative", action="store_true")
    args = parser.parse_args()
    if not args.no_replay and args.checker is None:
        parser.error("fresh replay requires --checker")
    checker = args.checker.resolve(strict=True) if args.checker else None
    eighteen_metadata, eighteen_rows = eighteen.load_ledger()
    eighteen.verify_bindings(eighteen_metadata, checker)
    eighteen.artifact_paths(eighteen_rows)
    eighteen.verify_payloads(eighteen_rows, None if args.no_replay else checker)
    terminal_metadata, terminal_rows = terminal.load_ledger()
    terminal.verify_bindings(terminal_metadata, checker)
    terminal.artifact_paths(terminal_rows)
    selected = (0, 14, 29, 44, 59) if args.representative else None
    terminal.verify_payloads(terminal_rows, None if args.no_replay else checker, selected)
    composition()


if __name__ == "__main__":
    main()
