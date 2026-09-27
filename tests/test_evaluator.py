import unittest
from reference_solution.evaluator import evaluate, normalize, score_case, token_f1

class EvaluatorTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalize("إِدارةُ  البَيانات"),"ادارة البيانات")
    def test_repeated_tokens_are_counted(self):
        self.assertAlmostEqual(token_f1("علم علم بيانات","علم بيانات"),0.8)
    def test_forbidden_claim_zeroes_score(self):
        case={"id":"x","reference":"القاهرة","required_concepts":["القاهرة"],"forbidden_claims":["الإسكندرية"]}
        self.assertEqual(score_case(case,"القاهرة وليست الإسكندرية")["score"],0.0)
    def test_missing_prediction_fails(self):
        cases=[{"id":"x","reference":"أ","required_concepts":[],"forbidden_claims":[]}]
        with self.assertRaisesRegex(ValueError,"missing predictions"): evaluate(cases,[])

if __name__=="__main__": unittest.main()
