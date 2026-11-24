import unittest
from main import analyze_data, build_report


class TestCommunitySafety(unittest.TestCase):

    def setUp(self):
        self.records = [
            {"year": 2023, "category": "Theft", "count": 12},
            {"year": 2023, "category": "Fraud", "count": 7},
            {"year": 2024, "category": "Theft", "count": 15}
        ]

    def test_yearly_totals(self):
        yearly, categories = analyze_data(self.records)
        self.assertEqual(yearly[2023], 19)
        self.assertEqual(yearly[2024], 15)

    def test_category_totals(self):
        yearly, categories = analyze_data(self.records)
        self.assertEqual(categories["Theft"], 27)
        self.assertEqual(categories["Fraud"], 7)

    def test_report(self):
        report = build_report(self.records, "test.csv")
        self.assertIn("Total count across supplied rows: 34", report)


if __name__ == "__main__":
    unittest.main()
