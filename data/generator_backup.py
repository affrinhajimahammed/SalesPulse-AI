
import random
from datetime import date, timedelta


REFERENCE_DATE = date(2026, 11, 15)


def generate_dataset(count=20, seed=20261022):
    rng = random.Random(seed)

    # 1. Territories
    territories = [
        {"territory_id": f"TER-{i:06d}", "name": name}
        for i, name in enumerate(
            ["Hyderabad", "Bengaluru", "Chennai"], start=1
        )
    ]

    # 2. Sales Representatives
    rep_names = ["Affrin", "Rahul", "Priya", "John"]
    sales_reps = []

    for i, name in enumerate(rep_names, start=1):
        territory = territories[(i - 1) % len(territories)]

        sales_reps.append({
            "rep_id": f"REP-{i:06d}",
            "name": name,
            "territory_id": territory["territory_id"]
        })

    # 3. Accounts
    accounts = []

    for i in range(1, 16):
        territory = rng.choice(territories)

        accounts.append({
            "account_id": f"ACC-{i:06d}",
            "company_name": f"Company {i}",
            "industry": rng.choice([
                "Technology", "Banking", "Healthcare", "Retail"
            ]),
            "territory_id": territory["territory_id"]
        })

    # 4. Sales Stages
    stages = [
        {"stage_id": "STAGE-001", "name": "Prospecting", "probability": 10},
        {"stage_id": "STAGE-002", "name": "Qualification", "probability": 25},
        {"stage_id": "STAGE-003", "name": "Proposal", "probability": 50},
        {"stage_id": "STAGE-004", "name": "Negotiation", "probability": 75},
        {"stage_id": "STAGE-005", "name": "Closed Won", "probability": 100},
        {"stage_id": "STAGE-006", "name": "Closed Lost", "probability": 0}
    ]

    stage_lookup = {s["name"]: s for s in stages}

    # 5. Opportunities and Stage History
    opportunities = []
    stage_history = []

    start_date = date(2025, 1, 1)
    total_days = (REFERENCE_DATE - start_date).days

    stage_paths = {
        "Prospecting": ["Prospecting"],
        "Qualification": ["Prospecting", "Qualification"],
        "Proposal": ["Prospecting", "Qualification", "Proposal"],
        "Negotiation": [
            "Prospecting", "Qualification", "Proposal", "Negotiation"
        ],
        "Closed Won": [
            "Prospecting", "Qualification", "Proposal",
            "Negotiation", "Closed Won"
        ],
        "Closed Lost": [
            "Prospecting", "Qualification", "Proposal",
            "Negotiation", "Closed Lost"
        ]
    }

    for i in range(1, count + 1):
        opportunity_id = f"OPP-2026-{i:06d}"

        created_date = start_date + timedelta(
            days=rng.randint(0, total_days)
        )

        days_open = (REFERENCE_DATE - created_date).days

        account = rng.choice(accounts)
        rep = rng.choice(sales_reps)

        territory = next(
            t for t in territories
            if t["territory_id"] == rep["territory_id"]
        )

        final_stage = rng.choices(
            list(stage_paths.keys()),
            weights=[15, 20, 20, 15, 20, 10],
            k=1
        )[0]

        path = stage_paths[final_stage]

        progress_days = rng.randint(0, days_open)

        for j, stage_name in enumerate(path):
            if len(path) == 1:
                change_days = 0
            else:
                change_days = round(
                    progress_days * j / (len(path) - 1)
                )

            changed_date = created_date + timedelta(days=change_days)

            stage_history.append({
                "id": f"STG-{opportunity_id}-{j + 1:03d}",
                "opportunity_id": opportunity_id,
                "old_stage": path[j - 1] if j > 0 else None,
                "new_stage": stage_name,
                "changed_date": changed_date.isoformat()
            })

        current_stage = stage_lookup[final_stage]

        opportunities.append({
            "id": opportunity_id,
            "name": f"Opportunity {i}",
            "account": account["company_name"],
            "account_id": account["account_id"],
            "sales_rep": rep["name"],
            "sales_rep_id": rep["rep_id"],
            "territory": territory["name"],
            "territory_id": territory["territory_id"],
            "amount": rng.randint(10000, 500000),
            "stage": final_stage,
            "stage_id": current_stage["stage_id"],
            "probability": current_stage["probability"],
            "days_open": days_open,
            "created_date": created_date.isoformat(),
            "expected_close_date": (
                created_date + timedelta(days=rng.randint(30, 180))
            ).isoformat(),
            "product": rng.choice([
                "Enterprise Software",
                "Cloud Services",
                "Analytics Platform"
            ]),
            "currency": "INR"
        })

    # 6. Activities
    activities = []
    activity_types = ["Call", "Email", "Meeting", "Demo"]

    for i, opportunity in enumerate(opportunities, start=1):
        created = date.fromisoformat(opportunity["created_date"])
        available_days = (REFERENCE_DATE - created).days

        for j in range(1, rng.randint(1, 5) + 1):
            activity_date = created + timedelta(
                days=rng.randint(0, available_days)
            )

            activities.append({
                "activity_id": f"ACT-{i:06d}-{j:03d}",
                "opportunity_id": opportunity["id"],
                "sales_rep_id": opportunity["sales_rep_id"],
                "activity_type": rng.choice(activity_types),
                "activity_date": activity_date.isoformat()
            })

    # 7. Quotas
    quotas = []

    quarters = [
        "2025Q1", "2025Q2", "2025Q3", "2025Q4",
        "2026Q1", "2026Q2", "2026Q3", "2026Q4"
    ]

    for rep in sales_reps:
        for quarter in quarters:
            quotas.append({
                "quota_id": f"QUOTA-{rep['rep_id']}-{quarter}",
                "sales_rep_id": rep["rep_id"],
                "period": quarter,
                "target_amount": rng.randint(500000, 1500000),
                "currency": "INR"
            })

    # 8. Historical Bookings
    historical_bookings = []

    for opportunity in opportunities:
        if opportunity["stage"] == "Closed Won":
            won_event = next(
                event for event in stage_history
                if event["opportunity_id"] == opportunity["id"]
                and event["new_stage"] == "Closed Won"
            )

            historical_bookings.append({
                "booking_id": f"BOOK-{opportunity['id']}",
                "opportunity_id": opportunity["id"],
                "booking_amount": opportunity["amount"],
                "booking_date": won_event["changed_date"],
                "status": "Booked",
                "currency": opportunity["currency"]
            })

    # 9. Forecast Snapshots
    forecast_snapshots = []

    snapshot_dates = [
        date(2025, 3, 31),
        date(2025, 6, 30),
        date(2025, 9, 30),
        date(2025, 12, 31),
        date(2026, 3, 31),
        date(2026, 6, 30),
        date(2026, 9, 30),
        REFERENCE_DATE
    ]

    for snapshot_date in snapshot_dates:
        pipeline = 0
        expected = 0
        opportunity_count = 0

        for opportunity in opportunities:
            created = date.fromisoformat(opportunity["created_date"])

            if created > snapshot_date:
                continue

            known_events = [
                event for event in stage_history
                if event["opportunity_id"] == opportunity["id"]
                and date.fromisoformat(event["changed_date"]) <= snapshot_date
            ]

            if not known_events:
                continue

            historical_stage = known_events[-1]["new_stage"]

            if historical_stage in ["Closed Won", "Closed Lost"]:
                continue

            probability = stage_lookup[historical_stage]["probability"]

            pipeline += opportunity["amount"]
            expected += opportunity["amount"] * probability / 100
            opportunity_count += 1

        forecast_snapshots.append({
            "snapshot_id": f"FCST-{snapshot_date.isoformat()}-001",
            "snapshot_date": snapshot_date.isoformat(),
            "pipeline_amount": round(pipeline, 2),
            "expected_revenue": round(expected, 2),
            "best_case": round(expected * 1.2, 2),
            "worst_case": round(expected * 0.8, 2),
            "opportunity_count": opportunity_count,
            "currency": "INR"
        })

    # 10. Data Validation
    validation_errors = []

    account_ids = {a["account_id"] for a in accounts}
    rep_ids = {r["rep_id"] for r in sales_reps}
    opportunity_ids = {o["id"] for o in opportunities}

    for opportunity in opportunities:
        if opportunity["account_id"] not in account_ids:
            validation_errors.append(
                f"Invalid account: {opportunity['id']}"
            )

        if opportunity["sales_rep_id"] not in rep_ids:
            validation_errors.append(
                f"Invalid sales rep: {opportunity['id']}"
            )

        if opportunity["amount"] < 0:
            validation_errors.append(
                f"Negative amount: {opportunity['id']}"
            )

        if not 0 <= opportunity["probability"] <= 100:
            validation_errors.append(
                f"Invalid probability: {opportunity['id']}"
            )

        if date.fromisoformat(opportunity["created_date"]) > REFERENCE_DATE:
            validation_errors.append(
                f"Future creation date: {opportunity['id']}"
            )

    for activity in activities:
        if activity["opportunity_id"] not in opportunity_ids:
            validation_errors.append(
                f"Invalid activity link: {activity['activity_id']}"
            )

    for quota in quotas:
        if quota["sales_rep_id"] not in rep_ids:
            validation_errors.append(
                f"Invalid quota link: {quota['quota_id']}"
            )

    won_opportunity_ids = {
        o["id"] for o in opportunities
        if o["stage"] == "Closed Won"
    }

    for booking in historical_bookings:
        if booking["opportunity_id"] not in won_opportunity_ids:
            validation_errors.append(
                f"Invalid booking: {booking['booking_id']}"
            )

    for event in stage_history:
        if event["opportunity_id"] not in opportunity_ids:
            validation_errors.append(
                f"Invalid stage history link: {event['id']}"
            )

    # 11. Return Complete Dataset
    return {
        "territories": territories,
        "sales_reps": sales_reps,
        "accounts": accounts,
        "stages": stages,
        "opportunities": opportunities,
        "stage_history": stage_history,
        "activities": activities,
        "quotas": quotas,
        "historical_bookings": historical_bookings,
        "forecast_snapshots": forecast_snapshots,
        "validation": {
            "status": "PASSED" if not validation_errors else "FAILED",
            "error_count": len(validation_errors),
            "errors": validation_errors
        }
    }


# Maintain compatibility with the existing Streamlit dashboard
def generate_opportunities(count=20, seed=20261022):
    return generate_dataset(count, seed)["opportunities"]
