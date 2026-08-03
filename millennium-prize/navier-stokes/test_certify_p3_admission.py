import pathlib
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class P3AdmissionCertificateTest(unittest.TestCase):
    def test_genuine_3d_example_is_certified_positive(self):
        completed = subprocess.run(
            ["uv", "run", "--with", "python-flint", "python",
             str(ROOT / "certify_p3_admission.py"), "--example",
             "--subdivisions", "2", "--precision", "96"],
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertIn('"proved_positive": true', completed.stdout)


if __name__ == "__main__":
    unittest.main()
