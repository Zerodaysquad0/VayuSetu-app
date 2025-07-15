import requests
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

# Load API key from .env
load_dotenv()
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

# Load district info (name, lat, lon)
with open("bihar_districts.json", "r", encoding="utf-8") as f:
    districts = pd.read_json(f)

data_rows = []

# Loop through each district
for _, row in districts.iterrows():
    city = row["name"]
    lat = row["lat"]
    lon = row["lon"]

    try:
        # Fetch weather data
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}"
            f"&appid={OPENWEATHER_KEY}&units=metric"
        )
        weather_res = requests.get(weather_url)
        weather_data = weather_res.json()

        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]

        # Fetch air quality data (OpenAQ V3)
        aqi_url = (
            f"https://api.openaq.org/v3/latest?coordinates={lat},{lon}&parameter=pm25"
        )
        aqi_res = requests.get(aqi_url, headers={"X-API-Key": OPENWEATHER_KEY})
        aqi_data = aqi_res.json()

        pm25 = None
        if aqi_data.get("results"):
            pm25 = aqi_data["results"][0]["measurements"][0]["value"]

        # Append the collected data
        data_rows.append({
            "city": city,
            "latitude": lat,
            "longitude": lon,
            "temp_C": temp,
            "humidity_%": humidity,
            "pm2_5_µg/m3": pm25,
            "timestamp": pd.Timestamp.utcnow()
        })

    except Exception as e:
        print(f"❌ Error for {city}: {e}")

# Convert to DataFrame
df = pd.DataFrame(data_rows)

# Save or append to CSV
csv_path = "weather_and_aqi.csv"
if os.path.exists(csv_path):
    df.to_csv(csv_path, mode='a', header=False, index=False)
else:
    df.to_csv(csv_path, mode='w', header=True, index=False)

print(f"✅ Fetched data for {len(df)} cities and saved to {csv_path}")
