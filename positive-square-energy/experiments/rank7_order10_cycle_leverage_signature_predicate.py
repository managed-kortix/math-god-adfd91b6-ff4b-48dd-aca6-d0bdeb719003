#!/usr/bin/env python3
"""Exact algebraic replay of weighted-cycle signature winners at order ten."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "rank7_order10_expanded_weighted_family_scan.py"
SPEC = importlib.util.spec_from_file_location("rank7_order10_predicate_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load expanded weighted-cycle lane")
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

SOURCE_REPORT = HERE / "rank7_order10_expanded_weighted_family_scan.json"
SOURCE_STREAM = HERE / "rank7_order10_after_expanded_weighted_remainder.jsonl.xz"
WINNER_STREAM = HERE / "rank7_order10_expanded_weighted_family_owners.jsonl.xz"
OUTPUT = HERE / "rank7_order10_cycle_leverage_signature_predicate.json"
OWNERS = HERE / "rank7_order10_cycle_leverage_signature_predicate_owners.jsonl.xz"
REMAINDER = HERE / "rank7_order10_after_cycle_leverage_predicate_remainder.jsonl.xz"
SCHEMA = "rank-seven-order-ten-cycle-leverage-signature-predicate-v1"
F = Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def strict_json(path):
    raw = path.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    require(raw == base.weighted.canonical_bytes(payload),
            f"noncanonical JSON: {path.name}")
    return payload, hashlib.sha256(raw).hexdigest()


def signature_key(source, kernel, row):
    return base.encoded_signature(source, kernel, row)


def decode_parameters(payload):
    return tuple(F(*value) for value in payload[:3]) + (payload[3],)


def parameter_key(parameters):
    return tuple((value.numerator, value.denominator)
                 for value in parameters[:3]) + (parameters[3],)


def parameter_payload(key):
    return [list(value) for value in key[:3]] + [key[3]]


def load_signature_winners(source_report):
    expected = source_report["owner_stream"]
    digest = hashlib.sha256()
    winners = defaultdict(Counter)
    records = []
    physical = 0
    with lzma.open(WINNER_STREAM, "rb") as stream:
        for raw in stream:
            payload = json.loads(raw.decode("ascii"))
            require(raw == base.weighted.canonical_bytes(payload),
                    "noncanonical weighted owner")
            record, certificate, signature = payload
            require(certificate[1], "winner stream contains a rejection")
            key = json.dumps(signature, sort_keys=True, separators=(",", ":"))
            winners[key][parameter_key(decode_parameters(certificate[3]))] += 1
            records.append(payload)
            physical += record[4]
            digest.update(raw)
    require((len(records), physical, digest.hexdigest(),
             base.weighted.file_sha256(WINNER_STREAM)) ==
            (expected["record_total"], expected["physical_total"],
             expected["raw_sha256"], expected["artifact_sha256"]),
            "weighted winner stream authentication failed")
    ordered = {
        key: tuple(parameter for parameter, _ in sorted(
            counts.items(), key=lambda item: (-item[1], item[0])))
        for key, counts in winners.items()
    }
    return ordered, winners, records


def predicate(projector, kernel, row, winner_keys):
    """Return the first exact Phi<=6 witness, or the exact minimum Phi."""
    cut_core, cycle_cores, paths = base.components(projector, kernel["edges"], row)
    best = None
    for key in winner_keys:
        parameters = tuple(F(*value) for value in key[:3]) + (key[3],)
        cost, normalizer = base.gram_cost(
            cut_core, cycle_cores[parameters[3]], paths,
            kernel["degrees"], parameters)
        if cost is None:
            continue
        candidate = cost, key, normalizer
        if best is None or candidate < best:
            best = candidate
        if cost <= base.BUDGET:
            return True, candidate
    require(best is not None, "signature winners produced no finite predicate value")
    return False, best


def authenticated_remainder(source_info):
    digest = hashlib.sha256()
    total = physical = 0
    with lzma.open(SOURCE_STREAM, "rb") as stream:
        for raw in stream:
            record = json.loads(raw.decode("ascii"))
            require(raw == base.weighted.canonical_bytes(record),
                    "noncanonical predicate source row")
            digest.update(raw)
            total += 1
            physical += record[4]
            yield raw, record
    require((total, physical, digest.hexdigest(),
             base.weighted.file_sha256(SOURCE_STREAM)) ==
            (source_info["record_total"], source_info["physical_total"],
             source_info["raw_sha256"], source_info["artifact_sha256"]),
            "predicate source authentication failed")


def certificate(record, accepted, result):
    cost, key, normalizer = result
    return [record[0], accepted, base.weighted.pair(cost),
            parameter_payload(key), base.weighted.pair(normalizer)]


def scan(progress=False):
    source = base.load("rank7_order10_predicate_source", base.weighted.SOURCE)
    projector = base.load("rank7_order10_predicate_projector", base.weighted.PROJECTOR)
    kernels = source.kernel_dictionary()
    report, report_sha256 = strict_json(SOURCE_REPORT)
    source_info = report["updated_remainder_stream"]
    winners, winner_counts, prior_records = load_signature_winners(report)

    signature_totals = Counter()
    signature_owned = Counter()
    signature_physical = Counter()
    signature_owned_physical = Counter()
    winner_use = Counter()
    prior_replay = hashlib.sha256()
    for record, old_certificate, signature in prior_records:
        key = json.dumps(signature, sort_keys=True, separators=(",", ":"))
        kernel = kernels[record[2]]
        accepted, result = predicate(projector, kernel, tuple(record[3]), winners[key])
        require(accepted, "a persisted weighted owner fails its signature predicate")
        fresh = certificate(record, accepted, result)
        prior_replay.update(base.weighted.canonical_bytes(fresh))
        signature_totals[key] += 1
        signature_owned[key] += 1
        signature_physical[key] += record[4]
        signature_owned_physical[key] += record[4]

    new_owners = {}
    classification = hashlib.sha256()
    remainder_digest = hashlib.sha256()
    remainder_total = remainder_physical = 0
    scanned = targeted = 0
    owner_digest = hashlib.sha256()
    owner_physical = 0
    owner_tmp = OWNERS.with_name(OWNERS.name + ".tmp")
    remainder_tmp = REMAINDER.with_name(REMAINDER.name + ".tmp")
    with lzma.open(owner_tmp, "wb", format=lzma.FORMAT_XZ, preset=6) as owner_out, \
            lzma.open(remainder_tmp, "wb", format=lzma.FORMAT_XZ, preset=6) as remainder_out:
        for raw, record in authenticated_remainder(source_info):
            scanned += 1
            kernel = kernels[record[2]]
            key = signature_key(source, kernel, tuple(record[3]))
            if key not in winners:
                remainder_out.write(raw)
                remainder_digest.update(raw)
                remainder_total += 1
                remainder_physical += record[4]
                continue
            targeted += 1
            signature_totals[key] += 1
            signature_physical[key] += record[4]
            accepted, result = predicate(
                projector, kernel, tuple(record[3]), winners[key])
            fresh = certificate(record, accepted, result)
            classification.update(base.weighted.canonical_bytes(fresh))
            if accepted:
                payload = [record, fresh, json.loads(key)]
                encoded = base.weighted.canonical_bytes(payload)
                owner_out.write(encoded)
                owner_digest.update(encoded)
                new_owners[record[0]] = payload
                owner_physical += record[4]
                signature_owned[key] += 1
                signature_owned_physical[key] += record[4]
                winner_use[result[1]] += 1
            else:
                remainder_out.write(raw)
                remainder_digest.update(raw)
                remainder_total += 1
                remainder_physical += record[4]
            if progress and scanned % 500000 == 0:
                print(f"scanned={scanned} targeted={targeted} new={len(new_owners)}",
                      flush=True)
    owner_tmp.replace(OWNERS)
    remainder_tmp.replace(REMAINDER)
    require(remainder_total + len(new_owners) == source_info["record_total"],
            "predicate remainder partition failed")
    require(remainder_physical + owner_physical == source_info["physical_total"],
            "predicate physical partition failed")

    strata = []
    for key in sorted(winners, key=lambda item: (-signature_totals[item], item)):
        total = signature_totals[key]
        owned = signature_owned[key]
        strata.append({
            "signature": json.loads(key), "tested": total, "owned": owned,
            "failed": total - owned,
            "coverage": base.weighted.pair(F(owned, total)),
            "physical_total": signature_physical[key],
            "owned_physical_total": signature_owned_physical[key],
            "winner_parameters": [parameter_payload(row) for row in winners[key]],
            "historical_winner_counts": [
                {"parameter": parameter_payload(row), "count": winner_counts[key][row]}
                for row in winners[key]],
        })
    whole = [row for row in strata if row["failed"] == 0]
    result = {
        "schema": SCHEMA, "full_theorem": False,
        "scope": "exact full-remainder algebraic predicate scan induced by all 7,807 weighted-cycle owners",
        "source_report_sha256": report_sha256,
        "source_remainder": source_info,
        "theorem": {
            "projectors": "C=I-P with P the endpoint-incidence cut projector; R_e=P_ee and lambda_e=C_ee=1-R_e",
            "weighted_core": "K_q=A C diag(q_e) C A^T, where q_e is a listed nonnegative rational function of R_e, lambda_e, and L_e",
            "gram": "H=D(a A P A^T+b K_q)D; M=max(1,max_v H_vv); G=H/M+diag(1-diag(H)/M)",
            "predicate": "Phi=sum_e (1-t_e)/(L_e(1+t_e))<=6, t_e=(-1)^L_e H_uv/M",
            "sufficiency": "K_q and the cut core are Gram sums, diagonal completion is nonnegative, and Phi is the exact path-energy excess; hence the predicate certifies the canonical row and every same-parity lengthening",
            "signature_rule": "a signature is certified when every row satisfies Phi<=6 for at least one historical exact winner assigned to that signature; no parameter grid is searched",
        },
        "winner_source": {"path": WINNER_STREAM.name,
                          "owner_total": len(prior_records),
                          "signature_total": len(winners),
                          "parameter_total": len({row for rows in winners.values()
                                                  for row in rows}),
                          "exact_replay_sha256": prior_replay.hexdigest()},
        "scan": {"remainder_scanned": scanned, "predicate_targeted": targeted,
                 "new_owner_total": len(new_owners),
                 "new_owner_physical_total": owner_physical,
                 "combined_owner_total": len(prior_records) + len(new_owners),
                 "whole_signature_total": len(whole),
                 "whole_signature_owner_total": sum(row["owned"] for row in whole),
                 "winner_use": [
                     {"parameter": parameter_payload(row), "count": count}
                     for row, count in sorted(winner_use.items(),
                                              key=lambda item: (-item[1], item[0]))]},
        "strata": strata,
        "classification_stream_sha256": classification.hexdigest(),
        "owner_stream": {"path": OWNERS.name, "record_total": len(new_owners),
                         "physical_total": owner_physical,
                         "raw_sha256": owner_digest.hexdigest(),
                         "artifact_sha256": base.weighted.file_sha256(OWNERS)},
        "updated_remainder_stream": {
            "path": REMAINDER.name, "record_total": remainder_total,
            "physical_total": remainder_physical,
            "raw_sha256": remainder_digest.hexdigest(),
            "artifact_sha256": base.weighted.file_sha256(REMAINDER)},
        "claim_boundary": "only exact predicate owners are removed; failed and untargeted rows remain byte-for-byte",
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    report = scan(args.progress)
    raw = base.weighted.canonical_bytes(report)
    if args.audit:
        require(args.output.read_bytes() == raw, "predicate report does not reproduce")
    else:
        args.output.write_bytes(raw)
    print(f"scanned={report['scan']['remainder_scanned']} "
          f"targeted={report['scan']['predicate_targeted']} "
          f"new={report['scan']['new_owner_total']} "
          f"whole={report['scan']['whole_signature_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
