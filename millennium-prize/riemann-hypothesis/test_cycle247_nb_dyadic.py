#!/usr/bin/env python3

import json
import unittest
from fractions import Fraction

from verify_cycle247_nb_dyadic import (
    DEFAULT_CERTIFICATE,
    targets,
    verify_certificate,
)


class Cycle247NBDyadicTests(unittest.TestCase):
    def test_targets_are_complete(self):
        self.assertEqual(targets(1536), (3, 6, 12, 24, 48, 96, 192, 384, 768))

    def test_checked_in_certificate_and_threshold_crossing(self):
        certificate = json.loads(DEFAULT_CERTIFICATE.read_text())
        _, verdicts = verify_certificate(certificate)
        self.assertEqual(verdicts[:5], ("LT_3_OVER_4",) * 5)
        self.assertEqual(verdicts[5:], ("GT_3_OVER_4",) * 4)
        previous_upper = None
        for row in certificate["rows"]:
            lower = Fraction(row["ratio"]["lower"])
            upper = Fraction(row["ratio"]["upper"])
            self.assertLess(lower, upper)
            if previous_upper is not None:
                self.assertGreater(lower, previous_upper)
            previous_upper = upper


if __name__ == "__main__":
    unittest.main()
