#!/usr/bin/env python3
"""Validate a saved Cycle 45 census against a fresh exact-runtime replay.

Default mode requires byte equality.  A focused run can instead validate that
every fresh interval is contained in its matching committed enclosure; this is
useful for a quick selected-scale reproduction without weakening the canonical
full-artifact check.
"""

import argparse
import json
from pathlib import Path
import tempfile

from flint import arb, ctx

from cycle45_dispersion_census import (
    DEFAULT_INTERVALS,
    DEFAULT_STARTS,
    SCRIPT_PATH,
    identity_error_ceiling,
    run,
)
from cycle45_runtime import ENVIRONMENT_MANIFEST_PATH, sha256_file

HERE = Path(__file__).resolve().parent
DEFAULT_ARTIFACT = HERE / "cycle45-dispersion-census-results.json"


class ArtifactValidationError(RuntimeError):
    pass


def canonical_bytes(payload):
    return (json.dumps(payload, indent=2) + "\n").encode("ascii")


def parse_finite_interval(text, label):
    try:
        value = arb(text)
    except Exception as exc:
        raise ArtifactValidationError(("invalid Arb interval", label, text)) from exc
    if not value.is_finite():
        raise ArtifactValidationError(("nonfinite Arb interval", label, text))
    return value


def interval_contains(container_text, contained_text, label):
    container = parse_finite_interval(container_text, f"{label}: committed")
    contained = parse_finite_interval(contained_text, f"{label}: fresh")
    if not container.contains(contained):
        raise ArtifactValidationError(
            ("fresh interval not contained in committed interval", label,
             container_text, contained_text)
        )


def validate_schema(payload):
    # Parsing and policy checks must occur at the artifact's declared working
    # precision, not at python-flint's process-global default precision.
    raw_bits = payload.get("arb_precision_bits")
    if not isinstance(raw_bits, int) or raw_bits < 128:
        raise ArtifactValidationError(("invalid Arb precision", raw_bits))
    ctx.prec = raw_bits
    required_top = {
        "scope", "anchor_commit", "arb_precision_bits", "runtime",
        "environment_manifest", "identity_error_policy", "theta", "starts",
        "intervals", "row_rule", "normalization", "verdict_policy", "rows",
    }
    if set(payload) != required_top:
        raise ArtifactValidationError(
            ("unexpected top-level schema", sorted(set(payload) - required_top),
             sorted(required_top - set(payload)))
        )
    if not payload["rows"]:
        raise ArtifactValidationError("artifact has no rows")
    bits = raw_bits
    policy = payload["identity_error_policy"]
    if policy.get("must_be_finite") is not True or \
            policy.get("must_contain_zero") is not True:
        raise ArtifactValidationError(("incoherent identity policy", policy))
    declared_ceiling = parse_finite_interval(
        policy.get("absolute_upper_bound_at_most", "nan"),
        "identity_error_policy.absolute_upper_bound_at_most",
    )
    expected_ceiling = identity_error_ceiling(bits)
    if not declared_ceiling.contains(expected_ceiling):
        raise ArtifactValidationError(
            ("identity policy ceiling disagrees with precision",
             declared_ceiling, expected_ceiling)
        )
    # The serialized policy uses 25 digits, so its radius legitimately exceeds
    # the exact 2^(-bits/2) ball.  Reject a vacuous serialization by requiring
    # its absolute uncertainty to be tiny relative to the declared ceiling.
    policy_error = abs(declared_ceiling - expected_ceiling).upper()
    if not policy_error <= expected_ceiling * arb("1e-20"):
        raise ArtifactValidationError(
            ("identity policy ceiling is too coarsely serialized",
             declared_ceiling, expected_ceiling)
        )

    interval_fields = {
        "D", "L3D", "Delta", "L2Delta", "LD_over_Delta", "beta2", "W2",
        "beta_signedW_cross", "signedW_offdiag", "recombination_error",
        "recombination_abs_error_upper_bound",
        "direct_identity_abs_error_upper_bound",
        "existing_probe_identity_abs_error_upper_bound",
    }
    upper_bound_fields = {
        "recombination_abs_error_upper_bound",
        "direct_identity_abs_error_upper_bound",
        "existing_probe_identity_abs_error_upper_bound",
    }
    for i, row in enumerate(payload["rows"]):
        if row.get("rank", 0) <= 0:
            raise ArtifactValidationError(("nonpositive row rank", i, row.get("rank")))
        parsed = {
            key: parse_finite_interval(row[key], f"rows[{i}].{key}")
            for key in interval_fields
        }
        if not parsed["Delta"] > 0:
            raise ArtifactValidationError(("Delta not certified positive", i))
        recombination = parsed["recombination_error"]
        if not recombination.contains(0) or not \
                abs(recombination).upper() <= expected_ceiling:
            raise ArtifactValidationError(
                ("invalid recombination identity enclosure", i,
                 row["recombination_error"])
            )
        for key in upper_bound_fields:
            value = parsed[key]
            if not value >= 0 or not value <= expected_ceiling:
                raise ArtifactValidationError(
                    ("invalid absolute error upper bound", i, key, row[key])
                )
        for j, packet in enumerate(row["ranges"]):
            for key in ("W2", "signed_energy", "signed_full_corr"):
                parse_finite_interval(packet[key], f"rows[{i}].ranges[{j}].{key}")


def compare_overlap(committed, fresh):
    """Require metadata agreement and containment of every selected interval."""
    interval_fields = {
        "D", "L3D", "Delta", "L2Delta", "LD_over_Delta", "beta2", "W2",
        "beta_signedW_cross", "signedW_offdiag", "recombination_error",
        "recombination_abs_error_upper_bound",
        "direct_identity_abs_error_upper_bound",
        "existing_probe_identity_abs_error_upper_bound",
    }
    if committed["runtime"]["generator_sha256"] != sha256_file(SCRIPT_PATH):
        raise ArtifactValidationError("committed generator hash is stale")
    if committed["runtime"]["environment_manifest_sha256"] != sha256_file(
        ENVIRONMENT_MANIFEST_PATH
    ):
        raise ArtifactValidationError("committed environment-manifest hash is stale")
    if not set(fresh["starts"]).issubset(committed["starts"]):
        raise ArtifactValidationError("fresh starts are absent from artifact")
    if not all(interval in committed["intervals"]
               for interval in fresh["intervals"]):
        raise ArtifactValidationError("fresh intervals are absent from artifact")
    for key in set(committed) - {"rows", "starts", "intervals"}:
        if committed[key] != fresh[key]:
            raise ArtifactValidationError(("metadata differs", key,
                                           committed[key], fresh[key]))

    committed_rows = {
        (row["a"], tuple(row["I"])): row for row in committed["rows"]
    }
    for i, new in enumerate(fresh["rows"]):
        key_id = (new["a"], tuple(new["I"]))
        if key_id not in committed_rows:
            raise ArtifactValidationError(("fresh row absent from artifact", key_id))
        old = committed_rows[key_id]
        for key in set(old) - interval_fields - {"ranges"}:
            if old[key] != new[key]:
                raise ArtifactValidationError(("row metadata differs", i, key))
        for key in interval_fields:
            interval_contains(old[key], new[key], f"rows[{key_id}].{key}")
        if len(old["ranges"]) != len(new["ranges"]):
            raise ArtifactValidationError(("range counts differ", key_id))
        for j, (old_packet, new_packet) in enumerate(zip(old["ranges"], new["ranges"])):
            for key in ("lo", "hi"):
                if old_packet[key] != new_packet[key]:
                    raise ArtifactValidationError(("range metadata differs",
                                                   key_id, j, key))
            for key in ("W2", "signed_energy", "signed_full_corr"):
                interval_contains(old_packet[key], new_packet[key],
                                  f"rows[{key_id}].ranges[{j}].{key}")


def validate(artifact_path, starts, intervals, bits, mode):
    raw = artifact_path.read_bytes()
    try:
        committed = json.loads(raw)
    except Exception as exc:
        raise ArtifactValidationError("artifact is not valid JSON") from exc
    validate_schema(committed)
    fresh = run(starts=starts, intervals=intervals, bits=bits)
    fresh_raw = canonical_bytes(fresh)

    if mode == "byte-equal":
        if raw != fresh_raw:
            with tempfile.NamedTemporaryFile(
                prefix="cycle45-fresh-", suffix=".json", delete=False
            ) as handle:
                handle.write(fresh_raw)
                replay_path = handle.name
            raise ArtifactValidationError(
                ("artifact is not byte-identical to the fresh replay", replay_path)
            )
    else:
        compare_overlap(committed, fresh)
    return len(fresh["rows"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--starts", nargs="+", type=int, default=DEFAULT_STARTS)
    parser.add_argument("--intervals", nargs="+", default=DEFAULT_INTERVALS)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--mode", choices=("byte-equal", "overlap"),
                        default="byte-equal")
    args = parser.parse_args()
    count = validate(args.artifact, tuple(args.starts), tuple(args.intervals),
                     args.bits, args.mode)
    print(f"PASS: validated {count} rows ({args.mode})")


if __name__ == "__main__":
    main()
