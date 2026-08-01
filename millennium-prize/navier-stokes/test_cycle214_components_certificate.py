import pathlib
import json
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class FullEnclosureCertificateTest(unittest.TestCase):
    def test_published_certificate_replays(self):
        result = subprocess.run(
            ["python", str(ROOT / "validate_cycle214.py"),
             str(ROOT / "cycle215-full-2d-enclosure-certificate.json")],
            check=True, capture_output=True, text=True,
        )
        self.assertIn("PASS FULL 2D PDE ENCLOSURE Cycle 215", result.stdout)
        self.assertIn("STRICT ENDPOINT L3 NEAR-DECAY CERTIFIED", result.stdout)

    def test_tampered_certificate_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = (ROOT / "cycle215-full-2d-enclosure-certificate.json").read_text(encoding="ascii")
            target = pathlib.Path(tmp) / "bad.json"
            target.write_text(source.replace('"mu": "1"', '"mu": "2"', 1), encoding="ascii")
            result = subprocess.run(
                ["python", str(ROOT / "validate_cycle214.py"), str(target)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FAIL CLOSED", result.stderr)

    def test_duplicate_json_key_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "duplicate.json"
            target.write_text('{"format":"a","format":"b"}', encoding="ascii")
            result = subprocess.run(
                ["python", str(ROOT / "validate_cycle214.py"), str(target)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate JSON key", result.stderr)

    def test_noncanonical_shell_key_fails_closed(self):
        source = json.loads(
            (ROOT / "cycle215-full-2d-enclosure-certificate.json").read_text(encoding="ascii")
        )
        shell_entry = source["slabs"][0]["shell_entry"]
        shell_entry["03"] = shell_entry.pop("3")
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "bad-shell-key.json"
            target.write_text(json.dumps(source), encoding="ascii")
            result = subprocess.run(
                ["python", str(ROOT / "validate_cycle214.py"), str(target)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("noncanonical shell key", result.stderr)

    def test_omitting_explicit_shells_from_norm_fails_closed(self):
        source = json.loads(
            (ROOT / "cycle215-full-2d-enclosure-certificate.json").read_text(encoding="ascii")
        )
        source["analytic_norm"]["tail_velocity_component"] = "0"
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "omitted-head.json"
            target.write_text(json.dumps(source), encoding="ascii")
            result = subprocess.run(
                ["python", str(ROOT / "validate_cycle214.py"), str(target)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("analytic norm mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main()
