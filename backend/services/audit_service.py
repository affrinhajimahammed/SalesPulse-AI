from datetime import datetime

from backend.database import SessionLocal
from backend.models import ForecastSnapshot


def save_forecast_snapshot(forecast, period="Current"):
    db = SessionLocal()

    try:
        snapshot = ForecastSnapshot(
            forecast_date=datetime.now(),
            period=period,
            total_pipeline=forecast["total_pipeline"],
            expected_revenue=forecast["expected_revenue"],
            best_case=forecast["best_case"],
            worst_case=forecast["worst_case"]
        )

        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)

        return {
            "status": "success",
            "snapshot_id": snapshot.id,
            "message": "Forecast saved successfully"
        }

    finally:
        db.close()


def get_forecast_history():
    db = SessionLocal()

    try:
        snapshots = db.query(ForecastSnapshot).order_by(
            ForecastSnapshot.forecast_date.desc()
        ).all()

        return [
            {
                "snapshot_id": item.id,
                "forecast_date": item.forecast_date.isoformat(),
                "period": item.period,
                "total_pipeline": item.total_pipeline,
                "expected_revenue": item.expected_revenue,
                "best_case": item.best_case,
                "worst_case": item.worst_case
            }
            for item in snapshots
        ]

    finally:
        db.close()