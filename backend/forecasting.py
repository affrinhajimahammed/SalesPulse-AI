
from backend.validation import validate_opportunities


def calculate_weighted_pipeline(opportunities):
    validate_opportunities(opportunities)

    total = 0.0

    for opportunity in opportunities:
        amount = opportunity["amount"]
        probability = opportunity["probability"]
        total += amount * (probability / 100)

    return round(total, 2)


def calculate_scenarios(opportunities):
    validate_opportunities(opportunities)

    total_pipeline = sum(item["amount"] for item in opportunities)
    expected = calculate_weighted_pipeline(opportunities)

    return {
        "total_pipeline": round(total_pipeline, 2),
        "worst_case": round(expected * 0.8, 2),
        "expected_revenue": expected,
        "best_case": round(expected * 1.2, 2),
        "scenario_assumptions": {
            "worst_case_adjustment": -20,
            "best_case_adjustment": 20,
            "method": "Illustrative percentage adjustments, not calibrated confidence intervals"
        }
    }


def calculate_forecast_metrics(actual_values, predicted_values):
    if len(actual_values) != len(predicted_values):
        raise ValueError("Actual and predicted values must have equal lengths.")

    if not actual_values:
        raise ValueError("At least one actual and predicted value is required.")

    errors = []

    for actual, predicted in zip(actual_values, predicted_values):
        if actual < 0 or predicted < 0:
            raise ValueError("Forecast values cannot be negative.")

        errors.append(abs(actual - predicted))

    mae = sum(errors) / len(errors)
    total_actual = sum(actual_values)

    wape = (
        sum(errors) / total_actual * 100
        if total_actual != 0
        else None
    )

    return {
        "MAE": round(mae, 2),
        "WAPE_percentage": round(wape, 2) if wape is not None else None,
        "record_count": len(actual_values)
    }


def calculate_metrics_by_group(actual_values, predicted_values, groups):
    if not (len(actual_values) == len(predicted_values) == len(groups)):
        raise ValueError("Actuals, predictions and groups must have equal lengths.")

    grouped_data = {}

    for actual, predicted, group in zip(actual_values, predicted_values, groups):
        if group not in grouped_data:
            grouped_data[group] = {"actual": [], "predicted": []}

        grouped_data[group]["actual"].append(actual)
        grouped_data[group]["predicted"].append(predicted)

    results = {}

    for group, values in grouped_data.items():
        results[str(group)] = calculate_forecast_metrics(
            values["actual"],
            values["predicted"]
        )

    return results
