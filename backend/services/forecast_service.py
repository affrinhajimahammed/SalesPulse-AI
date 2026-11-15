from backend.forecasting import calculate_scenarios


def generate_forecast(opportunities):
    forecast = calculate_scenarios(opportunities)

    return {
        "status": "success",
        "forecast": forecast
    }