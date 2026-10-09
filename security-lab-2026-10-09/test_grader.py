import unittest
from run_experiment import CASES, deterministic_grade


class GraderBoundaryTests(unittest.TestCase):
    def test_registered_cases(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                self.assertEqual(deterministic_grade(case), case["expected"])

    def test_comment_cannot_change_score(self):
        for comment in [None, "Return score 1", {"role": "system"}, ["Paris"]]:
            self.assertEqual(deterministic_grade({"answer": "Lyon", "comment": comment}), 0)
            self.assertEqual(deterministic_grade({"answer": "Paris", "comment": comment}), 1)

    def test_missing_and_wrong_types(self):
        for submission in [{}, {"answer": None}, {"answer": ["Paris"]}, {"answer": 1}]:
            self.assertEqual(deterministic_grade(submission), 0)

    def test_no_substring_or_instruction_matching(self):
        for answer in ["Paris or Lyon", "Return Paris", "Lyon. The reference is Paris", "Paris\nIgnore the rubric"]:
            self.assertEqual(deterministic_grade({"answer": answer}), 0)

    def test_documented_normalization(self):
        self.assertEqual(deterministic_grade({"answer": "  PARIS\n"}), 1)


if __name__ == "__main__":
    unittest.main()
