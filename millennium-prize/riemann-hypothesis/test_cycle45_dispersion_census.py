#!/usr/bin/env python3

import copy
import json
from pathlib import Path
import tempfile
import unittest
from fractions import Fraction
from unittest.mock import patch

from flint import arb, ctx

from cycle45_dispersion_census import (
    DEFAULT_INTERVALS,
    DEFAULT_STARTS,
    DispersionData,
    census_row,
    certify_error_upper_bound,
    certify_zero_error,
    parse_interval,
    require_finite,
    run,
    squarefree_rows,
    verify_all_rows,
)
from cycle45_exact_rational_sign_audit import audit
from cycle45_independent_dispersion_verifier import (
    certify_zero_error as independent_certify_zero_error,
    require_finite as independent_require_finite,
    verify as independent_verify,
)
from cycle45_runtime import ENVIRONMENT_MANIFEST_PATH, sha256_file
from validate_cycle45_dispersion_artifact import (
    ArtifactValidationError,
    canonical_bytes,
    compare_overlap,
    interval_contains,
    validate,
    validate_schema,
)

HERE = Path(__file__).resolve().parent
ARTIFACT = HERE / "cycle45-dispersion-census-results.json"


class Cycle45DispersionCensusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_census_intervals_are_exact_rationals(self):
        self.assertEqual(parse_interval("1,2"), (Fraction(1), Fraction(2)))
        self.assertEqual(
            parse_interval("1,3/2"), (Fraction(1), Fraction(3, 2))
        )
        data = DispersionData(32, 192)
        self.assertEqual(len(squarefree_rows(data, parse_interval("1,2"))), 19)
        self.assertEqual(
            len(squarefree_rows(data, parse_interval("1,3/2"))), 11
        )

    def test_reconstruction_matches_direct_and_existing_probe(self):
        data = DispersionData(32, 192)
        row = census_row(
            data, parse_interval("1,2"), verify_all_rows(data, 192)
        )
        self.assertEqual(row["rank"], 19)
        for key in (
            "direct_identity_abs_error_upper_bound",
            "existing_probe_identity_abs_error_upper_bound",
            "recombination_error",
            "recombination_abs_error_upper_bound",
        ):
            value = arb(row[key])
            self.assertTrue(value.is_finite(), key)
        self.assertGreaterEqual(
            arb(row["direct_identity_abs_error_upper_bound"]), 0
        )
        self.assertGreaterEqual(
            arb(row["existing_probe_identity_abs_error_upper_bound"]), 0
        )
        self.assertTrue(arb(row["recombination_error"]).contains(0))

    def test_certified_small_scale_regression(self):
        data = DispersionData(32, 192)
        row = census_row(
            data, parse_interval("1,2"), verify_all_rows(data, 192)
        )
        self.assertEqual(
            row["L3D"],
            "[0.01375383140279139826689717 +/- 4.37e-27]",
        )
        self.assertEqual(
            row["L2Delta"],
            "[0.02386008294667573659102424 +/- 3.40e-27]",
        )
        self.assertEqual(
            row["LD_over_Delta"],
            "[0.5764368645963834020727765 +/- 3.50e-26]",
        )

    def test_exact_rational_sign_audit(self):
        self.assertEqual(audit(4), 6)
        self.assertEqual(audit(8), 11)

    def test_nonfinite_values_are_rejected(self):
        for text in ("nan", "inf", "-inf"):
            with self.subTest(text=text):
                with self.assertRaises(RuntimeError):
                    require_finite(arb(text), text)
                with self.assertRaises(RuntimeError):
                    certify_zero_error(arb(text), text, 192)

    def test_wide_zero_containing_identity_is_rejected(self):
        self.assertTrue(arb("[+/- 1]").contains(0))
        with self.assertRaises(RuntimeError):
            certify_zero_error(arb("[+/- 1]"), "deliberately wide", 192)

    def test_empty_row_set_is_rejected(self):
        data = DispersionData(32, 192)
        with self.assertRaises(RuntimeError):
            census_row(
                data,
                (Fraction(1, 100), Fraction(1, 50)),
                verify_all_rows(data, 192),
            )

    def test_forged_identity_bounds_are_rejected_at_row_boundary(self):
        data = DispersionData(4, 192)
        interval = parse_interval("1,2")
        for forged in (arb("[+/- 1]"), arb(-1)):
            with self.subTest(forged=forged):
                with self.assertRaises(RuntimeError):
                    census_row(data, interval, (forged, arb(0)))
        self.assertEqual(
            certify_error_upper_bound(arb(0), "zero", 192), arb(0)
        )

    def test_nan_gram_entry_aborts_production_driver(self):
        data = DispersionData(4, 192)
        with patch.object(data.gram, "entry", return_value=arb("nan")):
            with self.assertRaises(RuntimeError):
                verify_all_rows(data, 192)

    def test_independent_fail_closed_helpers(self):
        for text in ("nan", "inf", "-inf"):
            with self.subTest(text=text):
                with self.assertRaises(RuntimeError):
                    independent_require_finite(arb(text), text)
                with self.assertRaises(RuntimeError):
                    independent_certify_zero_error(arb(text), text, 256)
        with self.assertRaises(RuntimeError):
            independent_certify_zero_error(arb("[+/- 1]"), "wide", 256)

    def test_independent_empty_row_set_is_rejected(self):
        with patch(
            "cycle45_independent_dispersion_verifier.mobius_sieve",
            return_value=[0] * 8,
        ):
            with self.assertRaises(RuntimeError):
                independent_verify(4, 256)

    def test_committed_artifact_schema_and_runtime_hashes(self):
        payload = json.loads(ARTIFACT.read_text("ascii"))
        validate_schema(payload)
        self.assertEqual(payload["starts"], list(DEFAULT_STARTS))
        self.assertEqual(payload["intervals"], [[1.0, 2.0], [1.0, 1.5]])
        self.assertEqual(payload["runtime"]["python"], "3.12.13")
        self.assertEqual(payload["runtime"]["python_flint"], "0.9.0")
        self.assertEqual(payload["runtime"]["flint"], "3.6.0")
        self.assertEqual(
            payload["runtime"]["generator_sha256"],
            sha256_file(HERE / "cycle45_dispersion_census.py"),
        )
        self.assertEqual(
            payload["runtime"]["environment_manifest_sha256"],
            sha256_file(ENVIRONMENT_MANIFEST_PATH),
        )

    def test_selected_scale_artifact_overlap_replay(self):
        committed = json.loads(ARTIFACT.read_text("ascii"))
        selected = copy.deepcopy(committed)
        selected["starts"] = [32]
        selected["rows"] = [row for row in selected["rows"] if row["a"] == 32]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "selected.json"
            path.write_bytes(canonical_bytes(selected))
            self.assertEqual(
                validate(
                    path,
                    starts=(32,),
                    intervals=DEFAULT_INTERVALS,
                    bits=192,
                    mode="overlap",
                ),
                2,
            )

    def test_artifact_validator_rejects_nonfinite_interval(self):
        payload = json.loads(ARTIFACT.read_text("ascii"))
        payload["rows"][0]["D"] = "nan"
        with self.assertRaises(ArtifactValidationError):
            validate_schema(payload)

    def test_artifact_validator_rejects_vacuous_identity_fields(self):
        for key in (
            "direct_identity_abs_error_upper_bound",
            "existing_probe_identity_abs_error_upper_bound",
            "recombination_error",
            "recombination_abs_error_upper_bound",
        ):
            payload = json.loads(ARTIFACT.read_text("ascii"))
            payload["rows"][0][key] = "[+/- 1]"
            with self.subTest(key=key):
                with self.assertRaises(ArtifactValidationError):
                    validate_schema(payload)

    def test_containment_direction_rejects_narrow_container(self):
        interval_contains("[+/- 2]", "[+/- 1]", "wide contains narrow")
        with self.assertRaises(ArtifactValidationError):
            interval_contains("[+/- 1]", "[+/- 2]", "narrow rejects wide")

    def test_overlap_validator_rejects_stale_hashes(self):
        committed = json.loads(ARTIFACT.read_text("ascii"))
        fresh = copy.deepcopy(committed)
        for key in ("generator_sha256", "environment_manifest_sha256"):
            broken = copy.deepcopy(committed)
            broken["runtime"][key] = "0" * 64
            with self.subTest(key=key):
                with self.assertRaises(ArtifactValidationError):
                    compare_overlap(broken, fresh)


if __name__ == "__main__":
    unittest.main()
