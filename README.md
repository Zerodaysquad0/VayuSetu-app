
# 🌬️ VayuSetu - Air Quality Forecasting for Rural India

VayuSetu is a backend intelligence system designed to collect, clean, forecast, and serve PM2.5 air quality data along with weather insights — specifically aimed at aiding rural districts of India.

---

## 🔧 Tech Stack

| Purpose               | Tool/Library       |
|-----------------------|--------------------|
| AQI Data              | [OpenAQ API](https://docs.openaq.org/)
| Weather Data          | [OpenWeatherMap API](https://openweathermap.org/)
| Forecasting           | [Prophet by Meta](https://facebook.github.io/prophet/)
| API Framework         | [FastAPI](https://fastapi.tiangolo.com/)
| Scheduling (future)   | GitHub Actions (CRON)
| Deployment (future)   | Render / Railway

---

## 📁 Project Structure

```
RAHUL_WORK/
├── .env                        # API keys (OpenAQ, OpenWeatherMap)
├── requirements.txt            # All dependencies
├── rahul_vayusetu/             # All backend logic and data
│   ├── fetch_data.py           # Fetch PM2.5 & weather data
│   ├── clean_merge.py          # Clean & merge the datasets
│   ├── forecast_all_districts.py # Forecast PM2.5 per district using Prophet
│   ├── api_server.py           # FastAPI server with endpoints
│   ├── weather_and_aqi.csv     # Raw merged data
│   ├── weather_aqi_cleaned.csv # Cleaned hourly dataset
│   ├── forecast_all_districts.csv # Final forecast output for API
│   └── bihar_districts.json    # List of districts with lat/lon
```

---

## 🌐 API Endpoints (FastAPI)

> Hosted locally on: `http://127.0.0.1:8000`

### 🩺 Health Check

```
GET /
→ { "status": "VayuSetu API up and running" }
```

---

### 📊 Forecast Endpoint

```
GET /forecast?city=katihar&hours=72
```

Returns the next 72 hours of predicted PM2.5 for the given district.

#### Example Response:

```json
[
  {
    "ds": "2025-07-16T00:00:00",
    "yhat": 55.3,
    "yhat_lower": 50.1,
    "yhat_upper": 60.7
  }
]
```

---

### 🚨 Alerts Endpoint

```
GET /alerts?city=katihar&threshold=100
```

Returns alert if future PM2.5 forecast exceeds threshold.

#### Example:

```json
{
  "city": "Katihar",
  "pm25_forecast": 122.8,
  "threshold": 100,
  "status": "ALERT"
}
```

---

## 🛠️ How to Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/sahhhh11/VayuSetu-app.git
cd VayuSetu-app
```

### 2. Set up Virtual Environment (first time)

```bash
python -m venv venv
.env\Scriptsctivate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up `.env` File

Inside the root `RAHUL_WORK` folder:

```
OPENAQ_KEY=your_openaq_api_key
OPENWEATHER_KEY=your_openweather_key
```

### 5. Run Data Pipeline

```bash
cd rahul_vayusetu
python fetch_data.py
python clean_merge.py
python forecast_all_districts.py
```

### 6. Start FastAPI Server

```bash
uvicorn api_server:app --reload
```

Access docs at 👉 http://127.0.0.1:8000/docs

---

## 🎯 Future Features

- Hindi human-readable forecasts
- SMS alerts for rural areas
- Voice call warnings (Twilio/Exotel)
- Satellite aerosol data
- LSTM-based forecasting
- Mobile app integration
- CRON automation via GitHub Actions

---

## 👨‍💻 Author

**Rahul Kumar**  
Backend & Forecasting Developer  
💡 Focused on clean air for rural India 🇮🇳  
🔗 [LinkedIn](#) | [GitHub](https://github.com/sahhhh11)

---

## 🤝 Collaborators Welcome!

If you're working on frontend, mobile, or design — feel free to open PRs, suggestions, or forks!
