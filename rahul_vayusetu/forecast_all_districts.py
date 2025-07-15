import pandas as pd
from prophet import Prophet
import os

df = pd.read_csv("weather_aqi_cleaned.csv", parse_dates=["timestamp"])
df["timestamp"] = df["timestamp"].dt.tz_localize(None)
df = df.dropna(subset=["pm25_smoothed"])

cities = df["city"].unique()
all_forecasts = []

for city in cities:
    city_df = df[df["city"] == city][["timestamp", "pm25_smoothed"]].copy()
    city_df = city_df.rename(columns={"timestamp": "ds", "pm25_smoothed": "y"})
    city_df = city_df.sort_values("ds")

    if len(city_df) < 2:
        print(f"❌ Skipping {city} — Not enough data")
        continue

    model = Prophet(daily_seasonality=True)
    model.fit(city_df)

    future = model.make_future_dataframe(periods=48, freq="H")
    forecast = model.predict(future)

    forecast["city"] = city
    all_forecasts.append(forecast[["ds", "city", "yhat", "yhat_lower", "yhat_upper"]])

# Merge and save
final_df = pd.concat(all_forecasts, ignore_index=True)
final_df.to_csv("forecast_all_districts.csv", index=False)
print("✅ All forecasts saved to forecast_all_districts.csv")
