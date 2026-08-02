import json
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class Cycle255CandidateScreenTest(unittest.TestCase):
    def compile(self, directory):
        binary = pathlib.Path(directory) / "cycle255-screen"
        subprocess.run(
            ["g++", "-O2", "-std=c++20", str(ROOT / "cycle255_candidate_screen.cpp"),
             "-lgmpxx", "-lgmp", "-o", str(binary)],
            check=True,
        )
        return binary

    def test_deterministic_checkpoint_and_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = self.compile(tmp)
            checkpoint = pathlib.Path(tmp) / "checkpoint.tsv"
            first = pathlib.Path(tmp) / "first.json"
            resumed = pathlib.Path(tmp) / "resumed.json"
            command = [
                str(binary), "--n", "16", "--steps-per-unit", "16",
                "--checkpoint", str(checkpoint), "--stop-after-feasible", "1",
            ]
            subprocess.run(command + ["--output", str(first)], check=True)
            first_data = json.loads(first.read_text(encoding="ascii"))
            self.assertEqual(first_data["status"], "FLOATING_GALERKIN_SCREEN_ONLY")
            self.assertFalse(first_data["pde_certificate"])
            self.assertFalse(first_data["complete"])
            self.assertEqual(first_data["feasible_members_screened"], 1)
            rows = checkpoint.read_text(encoding="ascii").splitlines()
            self.assertEqual(rows[0], "cycle255-floating-screen-checkpoint-v1")
            self.assertEqual(len(rows), 3)

            subprocess.run(command + ["--output", str(resumed)], check=True)
            resumed_data = json.loads(resumed.read_text(encoding="ascii"))
            self.assertEqual(resumed_data["feasible_members_screened"], 2)
            self.assertGreater(
                resumed_data["completed_enumeration_index"],
                first_data["completed_enumeration_index"],
            )
            self.assertEqual(len(checkpoint.read_text(encoding="ascii").splitlines()), 4)

    def test_fresh_runs_are_byte_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = self.compile(tmp)
            outputs = []
            checkpoints = []
            for run in range(2):
                output = pathlib.Path(tmp) / f"run-{run}.json"
                checkpoint = pathlib.Path(tmp) / f"run-{run}.tsv"
                subprocess.run(
                    [str(binary), "--n", "16", "--steps-per-unit", "16",
                     "--checkpoint", str(checkpoint), "--output", str(output),
                     "--stop-after-feasible", "2"],
                    check=True,
                )
                outputs.append(output.read_bytes())
                checkpoints.append(checkpoint.read_bytes())
            self.assertEqual(outputs[0], outputs[1])
            self.assertEqual(checkpoints[0], checkpoints[1])


if __name__ == "__main__":
    unittest.main()
