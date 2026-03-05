from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["women_safety_auth"]
users_collection = db["users"]