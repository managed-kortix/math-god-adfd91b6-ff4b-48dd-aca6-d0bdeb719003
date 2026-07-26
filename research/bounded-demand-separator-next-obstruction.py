#!/usr/bin/env python3
"""Exact transition certificate for the rank-two bounded-demand obstruction."""

from dataclasses import dataclass


class CertificateError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise CertificateError(message)


@dataclass(frozen=True)
class State:
    p: int
    e: int
    c: int
    t: int
    pp: int


def standard_sequences():
    # T1 has only its hub port. T0 has hub, A, and B, so its standard split is
    # the forced three-singleton split. There can be no subsequent router.
    return {
        (): ("TTPP",),
        ("T0",): ("T", "E_A", "P_A", "E_B", "P_B"),
    }


def ledger(profiles):
    p = sum(profile.startswith("P_") for profile in profiles)
    e = sum(profile.startswith("E_") for profile in profiles)
    strict_triangular = int("T" in profiles)
    pp = int(any(profile == "PP" for profile in profiles))
    return State(p=p, e=e, c=0, t=strict_triangular, pp=pp)


def accepted(state):
    integer_acceptance = state.c >= state.e + 1
    pp_plus_strict = bool(state.pp and state.t)
    return integer_acceptance or pp_plus_strict


def main():
    sequences = standard_sequences()
    require(len(sequences) == 2, "standard sequence exhaustion changed")
    require(sequences[()] == ("TTPP",), "empty sequence profile changed")
    require(
        sequences[("T0",)] == ("T", "E_A", "P_A", "E_B", "P_B"),
        "forced split profile changed",
    )

    split_state = ledger(sequences[("T0",)])
    require(
        split_state == State(p=2, e=2, c=0, t=1, pp=0),
        "standard split ledger changed",
    )
    require(not accepted(split_state), "obstruction became accepting")

    coalesced_profiles = ("T", "PP")
    coalesced_state = State(p=0, e=0, c=0, t=1, pp=1)
    require(accepted(coalesced_state), "PP coalescence repair is not accepting")

    rank_one_profile = ("TPP",)
    require(rank_one_profile[0] == "TPP", "rank-one terminal changed")

    print("standard router sequences:", sequences)
    print("forced split state:", split_state)
    print("forced split accepted:", accepted(split_state))
    print("coalesced profiles:", coalesced_profiles)
    print("coalesced state accepted:", accepted(coalesced_state))
    print("rank-one base:", rank_one_profile)


if __name__ == "__main__":
    main()
