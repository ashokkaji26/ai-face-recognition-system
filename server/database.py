import os
from pymongo import MongoClient
from dotenv import load_dotenv

# =========================
# Load environment variables
# =========================
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI not found in environment variables")

# =========================
# MongoDB Connection
# =========================
client = MongoClient(MONGO_URI)

# Database name
db = client["ai_face_attendance"]

# Collections
users_collection = db["users"]
attendance_collection = db["attendance"]

print("✅ Connected to MongoDB (ai_face_attendance)")