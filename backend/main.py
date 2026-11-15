
from fastapi import FastAPI, HTTPException

from backend.database import engine, Base
from backend import models

from backend.services.forecast_service import generate_forecast
from backend.services.risk_service import identify_risks
from backend.services.audit_service import (
    save_forecast_snapshot,
    get_forecast_history
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SalesPulse AI",
    description="Intelligent Sales Forecasting and Pipeline Risk Management",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SalesPulse AI",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/forecast")
def create_forecast(opportunities: list[dict]):
    try:
        return generate_forecast(opportunities)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/risks")
def detect_risks(opportunities: list[dict]):
    try:
        return {
            "status": "success",
            "risky_opportunities": identify_risks(opportunities)
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/forecast-history")
def save_forecast_history(opportunities: list[dict]):
    try:
        forecast_result = generate_forecast(opportunities)
        forecast = forecast_result["forecast"]

        return save_forecast_snapshot(forecast)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.get("/forecast-history")
def read_forecast_history():
    return {
        "status": "success",
        "history": get_forecast_history()
    }
