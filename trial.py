import pandas as pd

df = pd.read_csv("weather_aqi_cleaned.csv")
patna = df[df["city"] == "Patna"]
print("Total rows:", len(patna))
print("Non-NaN smoothed:", patna["pm25_smoothed"].notna().sum())
print(patna[["timestamp", "pm25_smoothed"]])
