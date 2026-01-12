import unittest
from ledger.services import calc_summary, calc_category_expense


class TestServices(unittest.TestCase):
    def test_calc_summary(self):
        transactions = [
            {"type": "수입", "amount": 10000},
            {"type": "지출", "amount": 3000},
            {"type": "지출", "amount": 2000},
        ]
        income, expense, balance = calc_summary(transactions)
        self.assertEqual(income, 10000)
        self.assertEqual(expense, 5000)
        self.assertEqual(balance, 5000)

    def test_calc_category_expense(self):
        transactions = [
            {"type": "지출", "category": "식비", "amount": 8000},
            {"type": "지출", "category": "식비", "amount": 2000},
            {"type": "수입", "category": "급여", "amount": 1000000},
            {"type": "지출", "category": "교통", "amount": 1500},
        ]
        result = calc_category_expense(transactions)
        self.assertEqual(result["식비"], 10000)
        self.assertEqual(result["교통"], 1500)
        self.assertTrue("급여" not in result)  # 수입은 제외


if __name__ == "__main__":
    unittest.main()
