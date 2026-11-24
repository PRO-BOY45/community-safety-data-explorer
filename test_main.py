import unittest
import tempfile
import os
from unittest.mock import patch

from main import load_data, analyze_data, generate_report


class TestCommunitySafetyExplorer(unittest.TestCase):

    def setUp(self):
        self.records = [
            {"year": 2023, "category": "Theft", "count": 12},
            {"year": 2023, "category": "Fraud", "count": 7},
            {"year": 2024, "category": "Theft", "count": 15}
        ]

    def test_yearly_analysis(self):
        yearly, categories = analyze_data(self.records)

        self.assertEqual(yearly[2023], 19)
        self.assertEqual(yearly[2024], 15)

    def test_category_analysis(self):
        yearly, categories = analyze_data(self.records)

        self.assertEqual(categories["Theft"], 27)
        self.assertEqual(categories["Fraud"], 7)

    def test_total_count(self):
        total = sum(item["count"] for item in self.records)
        self.assertEqual(total, 34)

    def test_load_csv(self):
        csv_content = (
            "year,category,count\n"
            "2023,Theft,12\n"
            "2023,Fraud,7\n"
        )

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".csv",
            delete=False,
            encoding="utf-8",
            newline=""
        ) as file:
            file.write(csv_content)
            filename = file.name

        try:
            records = load_data(filename)
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]["count"], 12)
        finally:
            os.remove(filename)

    def test_report_output(self):
        with patch("builtins.print") as mock_print:
            generate_report(self.records)

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("COMMUNITY SAFETY DATA EXPLORER", printed_text)
        self.assertIn("TOTAL COUNT: 34", printed_text)


if __name__ == "__main__":
    unittest.main()

