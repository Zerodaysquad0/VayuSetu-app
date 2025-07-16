import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_sms_alert(city: str, aqi: float, threshold: float):
    """
    Sends an SMS alert using Fast2SMS when AQI exceeds threshold.
    """

    api_key = os.getenv("FAST2SMS_API_KEY")
    to_phone = os.getenv("TO_PHONE")

    if not api_key or not to_phone:
        print("❌ ERROR: FAST2SMS_API_KEY or TO_PHONE missing in .env file")
        return

    message = (
        f"⚠️ ALERT from VayuSetu!\n"
        f"District: {city.title()}\n"
        f"PM2.5 Level: {aqi} µg/m³\n"
        f"Threshold: {threshold}\n"
        f"⚕️ Stay indoors. Avoid outdoor activities."
    )

    # ✅ Temporarily disabled SMS sending
    print(f"🔕 [SIMULATION] SMS alert would be sent to {to_phone}:")
    print(message)

    # Uncomment below to re-enable real SMS sending
    """
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": api_key
    }

    payload = {
        "sender_id": "FSTSMS",
        "message": message,
        "language": "english",
        "route": "q",
        "numbers": to_phone
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        if response.status_code == 200:
            print("✅ SMS alert sent successfully.")
        else:
            print(f"❌ Failed to send SMS. Status: {response.status_code} Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception occurred while sending SMS: {e}")
    """
