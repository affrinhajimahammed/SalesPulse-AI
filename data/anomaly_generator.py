
import csv
from pathlib import Path


def generate_anomalies():
    output_dir = Path("exports")
    output_dir.mkdir(exist_ok=True)

    anomalies = [
        {
            "anomaly_id": "ANM-000001",
            "opportunity_id": "OPP-2026-000001",
            "anomaly_type": "NEGATIVE_AMOUNT",
            "field": "amount",
            "invalid_value": -50000,
            "description": "Opportunity has a negative deal amount."
        },
        {
            "anomaly_id": "ANM-000002",
            "opportunity_id": "OPP-2026-000002",
            "anomaly_type": "INVALID_PROBABILITY",
            "field": "probability",
            "invalid_value": 150,
            "description": "Win probability exceeds 100 percent."
        },
        {
            "anomaly_id": "ANM-000003",
            "opportunity_id": "OPP-2026-000003",
            "anomaly_type": "CLOSE_DATE_BEFORE_CREATION",
            "field": "expected_close_date",
            "invalid_value": "2024-01-01",
            "description": "Expected close date is before opportunity creation."
        },
        {
            "anomaly_id": "ANM-000004",
            "opportunity_id": "OPP-2026-000004",
            "anomaly_type": "MISSING_ACCOUNT",
            "field": "account_id",
            "invalid_value": "ACC-999999",
            "description": "Opportunity references a nonexistent account."
        },
        {
            "anomaly_id": "ANM-000005",
            "opportunity_id": "OPP-2026-000005",
            "anomaly_type": "MIXED_CURRENCY",
            "field": "currency",
            "invalid_value": "USD",
            "description": "Currency differs from the baseline INR dataset."
        },
    ]

    labels = [
        {
            "anomaly_id": item["anomaly_id"],
            "opportunity_id": item["opportunity_id"],
            "label": 1,
            "is_anomaly": True,
            "anomaly_type": item["anomaly_type"]
        }
        for item in anomalies
    ]

    for filename, records in [
        ("anomalies.csv", anomalies),
        ("anomaly_labels.csv", labels)
    ]:
        with open(output_dir / filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)

    print("Anomaly dataset generated successfully!")
    print("Anomalies:", len(anomalies))
    print("Labels:", len(labels))
    print("Baseline dataset remains unchanged.")


if __name__ == "__main__":
    generate_anomalies()
