from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException
from datetime import datetime, timezone
import numpy as np
import face_recognition
from PIL import Image
import io
from pymongo.errors import DuplicateKeyError

from database import users_collection, attendance_collection

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

# Lower = stricter matching
MATCH_THRESHOLD = 0.45


# =========================
# MARK ATTENDANCE
# =========================
@router.post("/mark")
async def mark_attendance(
    email: str = Form(...),
    file: UploadFile = File(...)
):
    # 1️⃣ Fetch user
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if "face_embedding" not in user:
        raise HTTPException(status_code=400, detail="User face not registered")

    known_embedding = np.array(user["face_embedding"])

    # 2️⃣ Read image
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image file")

    try:
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = np.array(pil_image)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # 3️⃣ Detect face
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) != 1:
        return {
            "success": False,
            "message": "Image must contain exactly one face"
        }

    # 4️⃣ Encode face
    encodings = face_recognition.face_encodings(
        image,
        face_locations,
        model="small"
    )

    if not encodings:
        return {
            "success": False,
            "message": "Face encoding failed"
        }

    new_embedding = encodings[0]

    # 5️⃣ Compare embeddings
    distance = np.linalg.norm(known_embedding - new_embedding)
    if distance > MATCH_THRESHOLD:
        return {
            "success": False,
            "message": "Face does not match registered user",
            "distance": round(float(distance), 4)
        }

    # 6️⃣ Save attendance (DB-safe)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    try:
        attendance_collection.insert_one({
            "email": email,
            "date": today,
            "timestamp": datetime.now(timezone.utc),
            "status": "PRESENT"
        })
    except DuplicateKeyError:
        return {
            "success": False,
            "message": "Attendance already marked today"
        }

    return {
        "success": True,
        "message": "Attendance marked successfully",
        "distance": round(float(distance), 4)
    }


# =========================
# ATTENDANCE HISTORY
# =========================
@router.get("/history")
def attendance_history(email: str = Query(...)):
    records = attendance_collection.find(
        {"email": email},
        {"_id": 0, "date": 1}
    ).sort("date", 1)

    return {
        "success": True,
        "attendance": [r["date"] for r in records]
    }