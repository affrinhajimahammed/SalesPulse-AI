
import pytest

from backend.forecasting import (
    calculate_scenarios,
    calculate_forecast_metrics,
    calculate_metrics_by_group
)


def test_valid_forecast():
    opportunities = [
        {"amount": 100000, "probability": 50},
        {"amount": 200000, "probability": 25}
    ]

    result = calculate_scenarios(opportunities)

    assert result["total_pipeline"] == 300000
    assert result["expected_revenue"] == 100000


def test_invalid_probability():
    opportunities = [
        {"amount": 100000, "probability": 150}
    ]

    with pytest.raises(ValueError):
        calculate_scenarios(opportunities)


def test_negative_amount():
    opportunities = [
        {"amount": -50000, "probability": 50}
    ]

    with pytest.raises(ValueError):
        calculate_scenarios(opportunities)


def test_forecast_metrics():
    actual = [100, 200]
    predicted = [90, 220]

    result = calculate_forecast_metrics(actual, predicted)

    assert result["MAE"] == 15
    assert result["WAPE_percentage"] == 10
    assert result["record_count"] == 2


def test_metrics_by_group():
    actual = [100, 200, 300]
    predicted = [90, 220, 270]
    groups = ["A", "A", "B"]

    result = calculate_metrics_by_group(actual, predicted, groups)

    assert result["A"]["MAE"] == 15
    assert result["B"]["MAE"] == 30


def test_metrics_length_mismatch():
    with pytest.raises(ValueError):
        calculate_forecast_metrics([100], [90, 80])


def test_metrics_empty_data():
    with pytest.raises(ValueError):
        calculate_forecast_metrics([], [])
