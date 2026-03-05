from pymongo import MongoClient
from datetime import datetime

# Local MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

# Create / Connect Database
db = client["women_safety_db"]

# Create / Connect Collection
alerts_collection = db["alerts"]


def save_alert_to_db(emotion, weapon, message, image_name):
    alert_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "emotion": emotion,
        "weapon_detected": weapon,
        "message": message,
        "screenshot": image_name
    }

    alerts_collection.insert_one(alert_data)
    print("✅ Alert saved to MongoDB successfully!")