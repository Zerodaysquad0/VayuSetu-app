import requests
import pandas as pd
import os
import json
from dotenv import load_dotenv

# 1. Load API keys from .env file
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_KEY")

if not OPENWEATHER_API_KEY:
    raise ValueError("❌ Missing OPENWEATHER_KEY in your .env file")

# 2. Load all districts of Bihar from JSON file
with open("bihar_districts.json", "r") as f:
    cities = json.load(f)

# 3. Fetch data for each city
records = []

for city in cities:
    name = city["name"]
    lat = city["lat"]
    lon = city["lon"]

    print(f"Fetching data for {name}...")

    try:
        # 3.1 Fetch weather
        weather_res = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "lat": lat,
                "lon": lon,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric"
            },
            timeout=10
        )
        weather_res.raise_for_status()
        weather = weather_res.json()

        temp = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]

        # 3.2 Fetch PM2.5 (air pollution)
        aqi_res = requests.get(
            "https://api.openweathermap.org/data/2.5/air_pollution",
            params={
                "lat": lat,
                "lon": lon,
                "appid": OPENWEATHER_API_KEY
            },
            timeout=10
        )
        aqi_res.raise_for_status()
        aqi = aqi_res.json()
        pm25 = aqi["list"][0]["components"]["pm2_5"]

        # 3.3 Save record
        records.append({
            "city": name,
            "latitude": lat,
            "longitude": lon,
            "temp_C": temp,
            "humidity_%": humidity,
            "pm2_5_µg/m3": pm25,
            "timestamp": pd.to_datetime("now", utc=True)
        })

    except Exception as e:
        print(f"⚠️ Error fetching data for {name}: {e}")

# 4. Save to CSV
df = pd.DataFrame(records)

if df.empty:
    print("⚠️ No data collected. Please check your API key or network.")
else:
    df.to_csv("weather_and_aqi.csv", index=False)
    print("✅ Data saved to weather_and_aqi.csv")
    print(df.head())
