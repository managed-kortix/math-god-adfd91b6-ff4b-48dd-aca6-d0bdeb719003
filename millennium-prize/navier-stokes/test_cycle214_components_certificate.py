import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class ComponentsCertificateTest(unittest.TestCase):
    def test_published_certificate_replays(self):
        result = subprocess.run(
            ["python", str(ROOT / "validate_cycle214.py"),
             str(ROOT / "cycle214-components-certificate.json")],
            check=True, capture_output=True, text=True,
        )
        self.assertIn("PASS COMPONENTS Cycle 214", result.stdout)
        self.assertIn("NO FULL-PDE OR AMPLIFICATION CLAIM", result.stdout)

    def test_tampered_certificate_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = (ROOT / "cycle214-components-certificate.json").read_text(encoding="ascii")
            target = pathlib.Path(tmp) / "bad.json"
            target.write_text(source.replace('"mu": "1"', '"mu": "2"', 1), encoding="ascii")
            result = subprocess.run(
                ["python", str(ROOT / "validate_cycle214.py"), str(target)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FAIL CLOSED", result.stderr)


if __name__ == "__main__":
    unittest.main()
