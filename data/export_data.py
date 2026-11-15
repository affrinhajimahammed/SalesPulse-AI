
import csv
import json
from pathlib import Path

from data.generator import generate_dataset


def export_dataset():
    print("Generating full hackathon dataset...")

    dataset = generate_dataset(count=20000)

    output_dir = Path("exports")
    output_dir.mkdir(exist_ok=True)

    # Export complete dataset as JSON
    json_path = output_dir / "salespulse_dataset.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(dataset, file, indent=4, default=str)

    # Export each entity as CSV
    for entity_name, records in dataset.items():

        if not isinstance(records, list) or not records:
            continue

        csv_path = output_dir / f"{entity_name}.csv"

        fieldnames = list(records[0].keys())

        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

    print("\nExport completed!")
    print("Sales representatives:", len(dataset["sales_reps"]))
    print("Accounts:", len(dataset["accounts"]))
    print("Opportunities:", len(dataset["opportunities"]))
    print("Stage history:", len(dataset["stage_history"]))
    print("Activities:", len(dataset["activities"]))
    print("Quotas:", len(dataset["quotas"]))
    print("Historical bookings:", len(dataset["historical_bookings"]))
    print("Forecast snapshots:", len(dataset["forecast_snapshots"]))
    print("Validation:", dataset["validation"])
    print("Output folder:", output_dir.resolve())


if __name__ == "__main__":
    export_dataset()
