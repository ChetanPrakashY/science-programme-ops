import datetime as dt
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pubtrack  # noqa: E402

ROW = dict(id="X", title="t", lead_author="a", type="paper", venue="v", deadline="2026-12-01",
           stage="technical", stage_since="2026-11-02", reviewer="r", customer_data="no", customer_consent="")


class Rules(unittest.TestCase):
    def test_clean_row(self):
        self.assertEqual(pubtrack.problems(ROW), [])

    def test_reviewer_required_from_technical_stage(self):
        self.assertIn("no technical reviewer named", pubtrack.problems({**ROW, "reviewer": ""}))

    def test_customer_data_needs_consent_before_approval(self):
        r = {**ROW, "stage": "approval", "customer_data": "yes", "customer_consent": "no"}
        self.assertIn("uses customer data but consent is not recorded", pubtrack.problems(r))

    def test_bad_stage_and_date(self):
        p = pubtrack.problems({**ROW, "stage": "techncal", "deadline": "01/12/2026"})
        self.assertTrue(any("unknown stage" in x for x in p) and any("deadline" in x for x in p))

    def test_workdays_skip_weekends(self):
        # Fri 6 Nov 2026 -> Mon 9 Nov 2026 is one working day
        self.assertEqual(pubtrack.workdays_between(dt.date(2026, 11, 6), dt.date(2026, 11, 9)), 1)


if __name__ == "__main__":
    unittest.main()
