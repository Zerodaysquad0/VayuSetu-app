import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Step 1: Load cleaned data
df = pd.read_csv("weather_aqi_cleaned.csv")

# Step 2: Choose a city to forecast (e.g., Patna)
city = "Patna"
city_df = df[df["city"] == city].copy()

# Step 3: Prepare data for Prophet (rename columns)
prophet_df = city_df[["timestamp", "pm25_smoothed"]].copy()
prophet_df = prophet_df.rename(columns={"timestamp": "ds", "pm25_smoothed": "y"})
prophet_df["ds"] = pd.to_datetime(prophet_df["ds"], utc=True)
prophet_df = prophet_df.sort_values("ds")

# Step 4: Validate data before training
if len(prophet_df.dropna()) < 2:
    raise ValueError(f"❌ Not enough usable PM2.5 data to forecast for {city}.")

# Step 5: Fit Prophet model
model = Prophet(daily_seasonality=True)
model.fit(prophet_df)

# Step 6: Create future dates
future = model.make_future_dataframe(periods=48, freq="H")  # Next 48 hours
forecast = model.predict(future)

# Step 7: Plot forecast
model.plot(forecast)
plt.title(f"PM2.5 Forecast for {city}")
plt.xlabel("Date")
plt.ylabel("PM2.5 (µg/m3)")
plt.tight_layout()
plt.show()

# Optional: Save forecast to CSV
forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(f"forecast_{city}.csv", index=False)
print(f"✅ Forecast saved to forecast_{city}.csv")
