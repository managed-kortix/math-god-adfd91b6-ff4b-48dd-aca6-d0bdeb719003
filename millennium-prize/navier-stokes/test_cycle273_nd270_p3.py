#!/usr/bin/env python3
import json
from pathlib import Path
import unittest

from run_cycle273_nd270_p3 import (
    datum_state, execute, midpoint_step, preflight, verify_durable_integrity,
)

try:
    import numpy as np
    from scout_cycle265_3d_alignment import Galerkin3D
except ModuleNotFoundError:
    np = None
    Galerkin3D = None


ROOT = Path(__file__).parent


class Cycle273ND270P3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(
            (ROOT / "cycle273-nd270-p3-manifest.json").read_text(encoding="ascii")
        )
        cls.datum = json.loads(
            (ROOT / cls.manifest["singleton"]["file"]).read_text(encoding="ascii")
        )

    def test_initial_state_is_real_divergence_free_and_complete(self):
        if np is None:
            self.skipTest("numpy unavailable")
        solver = Galerkin3D(4)
        state = datum_state(solver, self.datum)
        defects = solver.defects(state)
        self.assertLess(defects["divergence"], 1e-15)
        self.assertLess(defects["reality"], 1e-15)
        self.assertEqual(np.count_nonzero(np.linalg.norm(state, axis=0)), 10)

    def test_midpoint_step_passes_frozen_residual_gate(self):
        if np is None:
            self.skipTest("numpy unavailable")
        solver = Galerkin3D(4)
        state = datum_state(solver, self.datum)
        _, diagnostics = midpoint_step(solver, state, 1 / 1048576, 1e-11, 40)
        self.assertLessEqual(diagnostics["residual_ratio"], 1e-11)
        self.assertLessEqual(diagnostics["iterations"], 40)
        self.assertTrue(np.isfinite(diagnostics["energy_identity_closure"]))
        self.assertTrue(np.isfinite(diagnostics["helicity_identity_closure"]))

    def test_preflight_fails_closed_on_frozen_digest_mismatch(self):
        result = preflight(self.manifest, ROOT)
        self.assertTrue(result["datum_digest_pass"])
        self.assertFalse(result["admission_certificate_digest_pass"])
        self.assertFalse(result["passed"])

    def test_frozen_analytic_cap_stops_before_trajectory(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "outcome.json"
            result = execute(ROOT / "cycle273-nd270-p3-manifest.json", output)
            self.assertEqual(result["status"], "BOUNDED_NEGATIVE_ANALYTIC_CAP")
            self.assertFalse(result["trajectory_generated"])
            self.assertFalse(result["full_pde_attempted"])
            self.assertTrue(result["durable_integrity"]["passed"])
            self.assertTrue(output.exists())

    def test_recovered_frozen_manifest_and_certificate_digests(self):
        amendment, manifest, integrity = verify_durable_integrity(
            ROOT / "cycle273-nd270-p3-manifest.json"
        )
        self.assertEqual(manifest["status"], "FROZEN_BEFORE_TRAJECTORY_COMPUTE")
        self.assertTrue(integrity["passed"])
        self.assertEqual(
            integrity["actual_sha256"]["cycle273-frozen-admission-certificate.json"],
            manifest["singleton"]["admission_certificate_sha256"],
        )
        self.assertFalse(amendment["semantics"]["compute_authorization_valid"])

    def test_digest_failure_precedes_analytic_status(self):
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            for name in (
                "cycle273-nd270-p3-manifest.json",
                "cycle273-nd270-p3-amendment.json",
                "cycle273-frozen-admission-certificate.json",
                "cycle-272-p3-example.json",
                "cycle-272-p3-certificate.json",
                "cycle-272-p3-finite-support-admission-audit.md",
                "cycle-265-genuine-3d-euler-pivot-architecture.md",
                "cycle-264-midpoint-tail-picard-interface.md",
                "cycle272-short-time-manifest.json",
            ):
                shutil.copyfile(ROOT / name, temporary / name)
            with (temporary / "cycle272-short-time-manifest.json").open("a", encoding="ascii") as stream:
                stream.write(" ")
            result = execute(
                temporary / "cycle273-nd270-p3-manifest.json",
                temporary / "outcome.json",
            )
            self.assertEqual(result["status"], "BOUNDED_NEGATIVE_PREFLIGHT_INTEGRITY_FAILURE")
            self.assertNotIn("analytic_precheck", result)


if __name__ == "__main__":
    unittest.main()
