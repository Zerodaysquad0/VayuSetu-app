from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pandas as pd
import os

# ✅ Import your Indian SMS alert function
from alerts.sms_alert_india import send_sms_alert

app = FastAPI(
    title="VayuSetu Backend API",
    description="API to serve air quality forecasts and alerts for Indian districts",
    version="1.0.0"
)

# ✅ Load forecast data once at startup
DATA_PATH = os.getenv("FORECAST_CSV", "forecast_all_districts.csv")
try:
    df_forecast = pd.read_csv(DATA_PATH, parse_dates=["ds"])
    df_forecast["ds"] = df_forecast["ds"].dt.tz_localize(None)
except Exception:
    df_forecast = pd.DataFrame()

class ForecastResponse(BaseModel):
    ds: str
    yhat: float
    yhat_lower: float
    yhat_upper: float

@app.get("/", summary="API Health Check")
async def read_root():
    return {"status": "VayuSetu API up and running"}

@app.get("/forecast", response_model=list[ForecastResponse], summary="Get PM2.5 forecast for a district")
async def get_forecast(
    city: str = Query(..., description="Name of the district, e.g., Patna"),
    hours: int = Query(48, ge=1, le=168, description="Forecast horizon in hours")
):
    city_df = df_forecast[df_forecast["city"].str.lower() == city.lower()].copy()
    if city_df.empty:
        raise HTTPException(status_code=404, detail=f"No forecast for '{city}'")
    
    city_df = city_df.sort_values("ds").head(hours)

    return [
        ForecastResponse(
            ds=row["ds"].isoformat(),
            yhat=row["yhat"],
            yhat_lower=row["yhat_lower"],
            yhat_upper=row["yhat_upper"]
        )
        for _, row in city_df.iterrows()
    ]

@app.get("/alerts", summary="Check alert status for a district")
async def get_alert(
    city: str = Query(..., description="District name, e.g., Patna"),
    threshold: float = Query(100.0, description="PM2.5 threshold for alert")
):
    city_df = df_forecast[df_forecast["city"].str.lower() == city.lower()]
    if city_df.empty:
        raise HTTPException(status_code=404, detail="District not found")
    
    latest = city_df.sort_values("ds").iloc[-1]
    status = "OK"

    if latest.yhat > threshold:
        status = "ALERT"
        send_sms_alert(city.title(), latest.yhat, threshold)  # ✅ SMS sent here

    return {
        "city": city.title(),
        "pm25_forecast": latest.yhat,
        "threshold": threshold,
        "status": status
    }
