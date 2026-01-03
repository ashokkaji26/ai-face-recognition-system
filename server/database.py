import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
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
try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000  # 5s timeout
    )

    # Force connection check
    client.admin.command("ping")

except ServerSelectionTimeoutError:
    raise RuntimeError("❌ Failed to connect to MongoDB (timeout)")

# =========================
# Database & Collections
# =========================
db = client["ai_face_attendance"]

users_collection = db["users"]
attendance_collection = db["attendance"]

# =========================
# Indexes (IMPORTANT)
# =========================
# Prevent duplicate attendance per day per user
attendance_collection.create_index(
    [("email", 1), ("date", 1)],
    unique=True
)

print("✅ Connected to MongoDB (ai_face_attendance)")