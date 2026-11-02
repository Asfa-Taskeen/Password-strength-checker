import unittest

from password_checker.analyzer import analyze_password


class PasswordAnalyzerTests(unittest.TestCase):
    def test_empty_password_is_weak(self):
        report = analyze_password("")
        self.assertEqual(report.rating, "WEAK")
        self.assertEqual(report.score, 0)

    def test_common_password_is_weak(self):
        report = analyze_password("password")
        self.assertEqual(report.rating, "WEAK")
        self.assertEqual(report.score, 0)
        self.assertTrue(any("commonly used" in item for item in report.feedback))

    def test_long_diverse_password_scores_well(self):
        report = analyze_password("T7!mQ2#vL9@xR4$k")
        self.assertIn(report.rating, ("STRONG", "VERY STRONG"))
        self.assertGreaterEqual(report.score, 5)

    def test_repeated_characters_are_penalized(self):
        report = analyze_password("AAAAAAAAAAAAA1!")
        self.assertTrue(any("repeated" in item.lower() for item in report.feedback))

    def test_sequence_is_flagged(self):
        report = analyze_password("Abcd1234!Xyz")
        self.assertTrue(any("sequences" in item.lower() for item in report.feedback))

    def test_report_does_not_contain_password(self):
        secret = "Unique-Test-Password-928!"
        report = analyze_password(secret)
        rendered = repr(report)
        self.assertNotIn(secret, rendered)

    def test_non_string_input_is_rejected(self):
        with self.assertRaises(TypeError):
            analyze_password(None)


if __name__ == "__main__":
    unittest.main()
