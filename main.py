
import csv
import argparse
from collections import defaultdict
from pathlib import Path


def load_data(filename):
    records = []

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required = {"year", "category", "count"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must contain year, category and count.")

        for row in reader:
            year = int(row["year"])
            count = int(row["count"])
            category = row["category"].strip()

            if not 1900 <= year <= 2200:
                raise ValueError("Invalid year.")
            if count < 0 or not category:
                raise ValueError("Invalid count or category.")

            records.append({
                "year": year,
                "category": category,
                "count": count
            })

    if not records:
        raise ValueError("No records found.")

    return records


def analyze_data(records):
    yearly = defaultdict(int)
    categories = defaultdict(int)

    for item in records:
        yearly[item["year"]] += item["count"]
        categories[item["category"]] += item["count"]

    return yearly, categories


def generate_report(records):
    yearly, categories = analyze_data(records)

    print("\nCOMMUNITY SAFETY DATA EXPLORER")
    print("=" * 40)

    print("\nTOTAL COUNT:", sum(x["count"] for x in records))

    print("\nYEAR-WISE ANALYSIS")
    for year, count in sorted(yearly.items()):
        print(f"{year}: {count}")

    print("\nCATEGORY-WISE ANALYSIS")
    for category, count in sorted(
        categories.items(), key=lambda x: x[1], reverse=True
    ):
        print(f"{category}: {count}")

    print("\nNote: Counts are not population-adjusted rates.")
    print("Use only lawful, aggregate and appropriately licensed data.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="data/sample_incidents.csv"
    )
    parser.add_argument(
        "--output",
        default="reports/summary.txt"
    )
    args = parser.parse_args()

    try:
        records = load_data(args.input)
        generate_report(records)

        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)

        # Capture the report in a text file.
        yearly, categories = analyze_data(records)
        lines = ["COMMUNITY SAFETY DATA EXPLORER",
                 "=" * 40,
                 f"Total count: {sum(x['count'] for x in records)}",
                 "\nYEAR-WISE ANALYSIS"]

        lines.extend(
            f"{year}: {count}" for year, count in sorted(yearly.items())
        )
        lines.append("\nCATEGORY-WISE ANALYSIS")
        lines.extend(
            f"{name}: {count}"
            for name, count in sorted(
                categories.items(), key=lambda x: x[1], reverse=True
            )
        )
        output.write_text("\n".join(lines), encoding="utf-8")
        print(f"\nReport saved to {output}")

    except (OSError, ValueError) as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
