from twilio.rest import Client
from pymongo import MongoClient
from datetime import datetime
import winsound

# -------------------------------
# TWILIO CONFIG (PUT YOUR OWN)
# -------------------------------
account_sid = "YOUR ACCOUNT SID"
auth_token = "YOUR AUTH TOKEN"
twilio_number = "YOUR TWILIO NUMBER"
receiver_number = "YOUR NUMBER"

client = Client(account_sid, auth_token)

# -------------------------------
# MONGODB CONNECTION
# -------------------------------
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["women_safety_db"]
collection = db["alerts"]


def trigger_emergency():
    try:
        # 1️⃣ Play Alert Sound
        winsound.Beep(2000, 1000)  # frequency, duration

        # 2️⃣ Send SMS
        message = client.messages.create(
            body="🚨 EMERGENCY ALERT! Immediate assistance required.",
            from_=twilio_number,
            to=receiver_number
        )

        # 3️⃣ Store in Database (Correct Structure)
        now = datetime.now()

        alert_data = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "emotion": "Manual Trigger",
            "weapon": "None",
            "message": "🚨 EMERGENCY ALERT! Immediate assistance required.",
            "screenshot": "None"
        }

        collection.insert_one(alert_data)

        return True

    except Exception as e:
        print("Emergency Error:", e)
        return False