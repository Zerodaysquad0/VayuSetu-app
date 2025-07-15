import pandas as pd
import numpy as np

# Load raw data
try:
    df = pd.read_csv("weather_and_aqi.csv")
except FileNotFoundError:
    raise Exception("❌ 'weather_and_aqi.csv' not found. Run fetch_data.py first.")

# Parse and floor timestamps to the nearest hour
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.tz_convert("Asia/Kolkata").dt.floor("h")
df.set_index("timestamp", inplace=True)
df.sort_index(inplace=True)

# Clean each city individually
cleaned = []
for city, group in df.groupby("city"):
    group = group.sort_index()
    group_hourly = group.loc[~group.index.duplicated(keep="first")]

    # Rolling median to detect outliers
    group_hourly["pm25_median"] = group_hourly["pm2_5_µg/m3"].rolling(24, min_periods=1).median()

    # Cap PM2.5 values if extreme
    group_hourly["pm25_capped"] = np.where(
        group_hourly["pm2_5_µg/m3"] > 5 * group_hourly["pm25_median"],
        group_hourly["pm25_median"],
        group_hourly["pm2_5_µg/m3"]
    )

    # 6-hour smoothing
    group_hourly["pm25_smoothed"] = group_hourly["pm25_capped"].rolling(6, min_periods=1).mean()

    # Confidence score
    def get_confidence(val):
        if val <= 75: return "high"
        elif val <= 150: return "medium"
        else: return "low"

    group_hourly["confidence"] = group_hourly["pm25_smoothed"].apply(get_confidence)
    group_hourly["city"] = city
    cleaned.append(group_hourly)

# Merge all cities back
final_df = pd.concat(cleaned)
final_df = final_df[[
    "city", "latitude", "longitude", "temp_C", "humidity_%",
    "pm2_5_µg/m3", "pm25_capped", "pm25_smoothed", "confidence"
]]

# Save cleaned data
final_df.to_csv("weather_aqi_cleaned.csv")
print("✅ Cleaned data saved to 'weather_aqi_cleaned.csv'")
print(final_df.head())
