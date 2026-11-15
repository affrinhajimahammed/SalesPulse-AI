
import random
from bisect import bisect_right
from datetime import date, timedelta

REFERENCE_DATE = date(2026, 11, 15)

TERRITORY_NAMES = ["Hyderabad", "Bengaluru", "Chennai"]

INDUSTRIES = [
    "Technology",
    "Banking",
    "Healthcare",
    "Retail",
    "Manufacturing",
    "Education",
]

PRODUCTS = [
    "Enterprise Software",
    "Cloud Services",
    "AI Solutions",
    "Analytics Platform",
]

STAGES = [
    {"stage_id": "STAGE-001", "name": "Prospecting", "probability": 10},
    {"stage_id": "STAGE-002", "name": "Qualification", "probability": 25},
    {"stage_id": "STAGE-003", "name": "Proposal", "probability": 50},
    {"stage_id": "STAGE-004", "name": "Negotiation", "probability": 75},
    {"stage_id": "STAGE-005", "name": "Closed Won", "probability": 100},
    {"stage_id": "STAGE-006", "name": "Closed Lost", "probability": 0},
]

STAGE_PROBABILITIES = {
    stage["name"]: stage["probability"] for stage in STAGES
}

STAGE_PATHS = {
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
        "Prospecting", "Qualification", "Closed Lost"
    ],
}


def quarter_dates():
    return [
        ("2025Q1", date(2025, 1, 1)),
        ("2025Q2", date(2025, 4, 1)),
        ("2025Q3", date(2025, 7, 1)),
        ("2025Q4", date(2025, 10, 1)),
        ("2026Q1", date(2026, 1, 1)),
        ("2026Q2", date(2026, 4, 1)),
        ("2026Q3", date(2026, 7, 1)),
        ("2026Q4", date(2026, 10, 1)),
    ]


def generate_dataset(count=20, seed=20261022):
    rng = random.Random(seed)

    if count < 1:
        raise ValueError("Opportunity count must be at least 1.")

    # Scale master data for the full hackathon dataset.
    if count >= 20000:
        rep_count = 2000
        account_count = 2000
    else:
        rep_count = max(4, min(2000, count // 10))
        account_count = max(15, min(2000, count))

    # 1. Territories
    territories = [
        {
            "territory_id": f"TER-{i:06d}",
            "name": name,
        }
        for i, name in enumerate(TERRITORY_NAMES, start=1)
    ]

    # 2. Sales representatives
    sample_names = ["Affrin", "John", "Priya", "Rahul"]

    sales_reps = []
    for i in range(1, rep_count + 1):
        territory = territories[(i - 1) % len(territories)]

        name = (
            sample_names[i - 1]
            if i <= len(sample_names)
            else f"Sales Rep {i:04d}"
        )

        sales_reps.append({
            "rep_id": f"REP-{i:06d}",
            "name": name,
            "territory_id": territory["territory_id"],
        })

    # 3. Accounts
    accounts = []
    for i in range(1, account_count + 1):
        territory = territories[(i - 1) % len(territories)]

        accounts.append({
            "account_id": f"ACC-{i:06d}",
            "company_name": f"Company {i}",
            "industry": rng.choice(INDUSTRIES),
            "territory_id": territory["territory_id"],
        })

    account_lookup = {
        account["account_id"]: account for account in accounts
    }

    rep_lookup = {
        rep["rep_id"]: rep for rep in sales_reps
    }

    territory_lookup = {
        territory["territory_id"]: territory
        for territory in territories
    }

    # 4. Opportunities and related transactions
    opportunities = []
    stage_history = []
    activities = []
    historical_bookings = []

    events_by_opportunity = {}

    final_stage_options = [
        "Prospecting",
        "Qualification",
        "Proposal",
        "Negotiation",
        "Closed Won",
        "Closed Lost",
    ]

    final_stage_weights = [15, 20, 20, 15, 20, 10]

    for i in range(1, count + 1):
        opportunity_id = f"OPP-2026-{i:06d}"

        account = accounts[(i - 1) % len(accounts)]
        rep = sales_reps[(i - 1) % len(sales_reps)]
        territory = territory_lookup[rep["territory_id"]]

        created_date = REFERENCE_DATE - timedelta(
            days=rng.randint(1, 650)
        )

        expected_close_date = created_date + timedelta(
            days=rng.randint(30, 180)
        )

        amount = rng.randint(25000, 500000)

        final_stage = rng.choices(
            final_stage_options,
            weights=final_stage_weights,
            k=1,
        )[0]

        probability = STAGE_PROBABILITIES[final_stage]

        opportunity = {
            "id": opportunity_id,
            "name": f"Opportunity {i}",
            "account": account["company_name"],
            "account_id": account["account_id"],
            "sales_rep": rep["name"],
            "sales_rep_id": rep["rep_id"],
            "territory": territory["name"],
            "territory_id": territory["territory_id"],
            "amount": amount,
            "currency": "INR",
            "stage": final_stage,
            "stage_id": next(
                stage["stage_id"]
                for stage in STAGES
                if stage["name"] == final_stage
            ),
            "probability": probability,
            "created_date": created_date.isoformat(),
            "expected_close_date": expected_close_date.isoformat(),
            "days_open": (REFERENCE_DATE - created_date).days,
            "product": rng.choice(PRODUCTS),
        }

        opportunities.append(opportunity)

        # Generate chronological stage transitions.
        path = STAGE_PATHS[final_stage]
        event_dates = []

        available_days = (REFERENCE_DATE - created_date).days

        for stage_index, stage_name in enumerate(path):
            if len(path) == 1:
                event_date = created_date
            else:
                event_day = int(
                    available_days * stage_index / (len(path) - 1)
                )
                event_date = created_date + timedelta(days=event_day)

            event_dates.append(event_date)

            old_stage = (
                path[stage_index - 1]
                if stage_index > 0
                else ""
            )

            stage_history.append({
                "id": f"STG-{opportunity_id}-{stage_index + 1:03d}",
                "opportunity_id": opportunity_id,
                "old_stage": old_stage,
                "new_stage": stage_name,
                "changed_date": event_date.isoformat(),
            })

        events_by_opportunity[opportunity_id] = [
            (event_date, stage_name)
            for event_date, stage_name in zip(event_dates, path)
        ]

        # Generate sales activities.
        activity_count = rng.randint(1, 5)

        for activity_number in range(1, activity_count + 1):
            activity_date = created_date + timedelta(
                days=rng.randint(0, available_days)
            )

            activities.append({
                "activity_id": (
                    f"ACT-{opportunity_id}-{activity_number:03d}"
                ),
                "opportunity_id": opportunity_id,
                "sales_rep_id": rep["rep_id"],
                "activity_type": rng.choice([
                    "Call",
                    "Email",
                    "Meeting",
                    "Demo",
                    "Follow-up",
                ]),
                "activity_date": activity_date.isoformat(),
            })

        # Record bookings only for Closed Won opportunities.
        if final_stage == "Closed Won":
            booking_date = event_dates[-1]

            historical_bookings.append({
                "booking_id": f"BOOK-{i:06d}",
                "opportunity_id": opportunity_id,
                "booking_date": booking_date.isoformat(),
                "booking_amount": amount,
                "currency": "INR",
                "status": "Closed Won",
            })

    # 5. Quarterly quotas
    quotas = []

    for period, period_start in quarter_dates():
        for rep in sales_reps:
            quotas.append({
                "quota_id": (
                    f"QUOTA-{rep['rep_id']}-{period}"
                ),
                "sales_rep_id": rep["rep_id"],
                "period": period,
                "target_amount": rng.randint(500000, 2000000),
                "currency": "INR",
            })

    # 6. Forecast snapshots
    snapshot_dates = [
        date(2025, 3, 31),
        date(2025, 6, 30),
        date(2025, 9, 30),
        date(2025, 12, 31),
        date(2026, 3, 31),
        date(2026, 6, 30),
        date(2026, 9, 30),
        REFERENCE_DATE,
    ]

    forecast_snapshots = []

    for snapshot_number, snapshot_date in enumerate(
        snapshot_dates, start=1
    ):
        pipeline_amount = 0
        expected_revenue = 0
        opportunity_count = 0

        for opportunity in opportunities:
            opportunity_id = opportunity["id"]
            events = events_by_opportunity[opportunity_id]
            event_dates = [event[0] for event in events]

            event_index = bisect_right(
                event_dates, snapshot_date
            ) - 1

            if event_index < 0:
                continue

            snapshot_stage = events[event_index][1]

            if snapshot_stage in ("Closed Won", "Closed Lost"):
                continue

            amount = opportunity["amount"]
            probability = STAGE_PROBABILITIES[snapshot_stage]

            pipeline_amount += amount
            expected_revenue += amount * probability / 100
            opportunity_count += 1

        forecast_snapshots.append({
            "snapshot_id": (
                f"FCST-{snapshot_date.isoformat()}-{snapshot_number:03d}"
            ),
            "snapshot_date": snapshot_date.isoformat(),
            "opportunity_count": opportunity_count,
            "pipeline_amount": pipeline_amount,
            "expected_revenue": round(expected_revenue, 2),
            "best_case": round(expected_revenue * 1.2, 2),
            "worst_case": round(expected_revenue * 0.8, 2),
            "currency": "INR",
        })

    # 7. Selected data validation checks
    validation_errors = []

    valid_account_ids = set(account_lookup)
    valid_rep_ids = set(rep_lookup)
    valid_opportunity_ids = {
        opportunity["id"] for opportunity in opportunities
    }

    for opportunity in opportunities:
        if opportunity["account_id"] not in valid_account_ids:
            validation_errors.append(
                f"Invalid account: {opportunity['id']}"
            )

        if opportunity["sales_rep_id"] not in valid_rep_ids:
            validation_errors.append(
                f"Invalid representative: {opportunity['id']}"
            )

        if opportunity["amount"] < 0:
            validation_errors.append(
                f"Negative amount: {opportunity['id']}"
            )

        if not 0 <= opportunity["probability"] <= 100:
            validation_errors.append(
                f"Invalid probability: {opportunity['id']}"
            )

    for event in stage_history:
        if event["opportunity_id"] not in valid_opportunity_ids:
            validation_errors.append(
                f"Invalid stage history: {event['id']}"
            )

    for activity in activities:
        if activity["opportunity_id"] not in valid_opportunity_ids:
            validation_errors.append(
                f"Invalid activity: {activity['activity_id']}"
            )

        if activity["sales_rep_id"] not in valid_rep_ids:
            validation_errors.append(
                f"Invalid activity representative: "
                f"{activity['activity_id']}"
            )

    for booking in historical_bookings:
        if booking["opportunity_id"] not in valid_opportunity_ids:
            validation_errors.append(
                f"Invalid booking: {booking['booking_id']}"
            )

    for quota in quotas:
        if quota["sales_rep_id"] not in valid_rep_ids:
            validation_errors.append(
                f"Invalid quota: {quota['quota_id']}"
            )

    return {
        "territories": territories,
        "sales_reps": sales_reps,
        "accounts": accounts,
        "stages": STAGES,
        "opportunities": opportunities,
        "stage_history": stage_history,
        "activities": activities,
        "quotas": quotas,
        "historical_bookings": historical_bookings,
        "forecast_snapshots": forecast_snapshots,
        "validation": {
            "status": (
                "PASSED" if not validation_errors else "FAILED"
            ),
            "error_count": len(validation_errors),
            "errors": validation_errors,
        },
    }


# Keep the existing dashboard compatible.
def generate_opportunities(count=20, seed=20261022):
    dataset = generate_dataset(count=count, seed=seed)
    return dataset["opportunities"]
