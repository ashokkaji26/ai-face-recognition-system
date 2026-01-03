from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import face_recognition
from io import BytesIO
from database import users_collection

router = APIRouter(prefix="/face", tags=["Face"])


# =========================
# IMAGE UPLOAD REGISTRATION
# =========================
@router.post("/register")
async def register_face(
    email: str = Form(...),
    file: UploadFile = File(...)
):
    # 1️⃣ Read image bytes
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Empty image file uploaded"
        )

    image_stream = BytesIO(image_bytes)

    # 2️⃣ Load image safely
    try:
        image = face_recognition.load_image_file(image_stream)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file"
        )

    # 3️⃣ Detect faces
    face_locations = face_recognition.face_locations(image)

    if len(face_locations) == 0:
        return {
            "success": False,
            "message": "No face detected. Please upload a clear face image."
        }

    if len(face_locations) > 1:
        return {
            "success": False,
            "message": "Multiple faces detected. Upload only one face."
        }

    # 4️⃣ Generate embedding
    encodings = face_recognition.face_encodings(image, face_locations)
    if not encodings:
        raise HTTPException(
            status_code=400,
            detail="Face encoding failed"
        )

    face_encoding = encodings[0]

    # 5️⃣ Save embedding using EMAIL
    result = users_collection.update_one(
        {"email": email},
        {"$set": {"face_embedding": face_encoding.tolist()}}
    )

    if result.matched_count == 0:
        return {
            "success": False,
            "message": "User not found. Please sign up first."
        }

    return {
        "success": True,
        "message": "Face registered successfully"
    }


# =========================
# WEBCAM REGISTRATION
# =========================
@router.post("/register-webcam")
async def register_face_webcam(
    email: str = Form(...),
    file: UploadFile = File(...)
):
    # 1️⃣ Read image bytes
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Empty webcam image"
        )

    image_stream = BytesIO(image_bytes)

    # 2️⃣ Load image
    try:
        image = face_recognition.load_image_file(image_stream)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image data from webcam"
        )

    # 3️⃣ Detect faces
    face_locations = face_recognition.face_locations(image)

    if len(face_locations) == 0:
        return {
            "success": False,
            "message": "No face detected. Please try again."
        }

    if len(face_locations) > 1:
        return {
            "success": False,
            "message": "Multiple faces detected. Only one allowed."
        }

    # 4️⃣ Generate embedding
    encodings = face_recognition.face_encodings(image, face_locations)
    if not encodings:
        raise HTTPException(
            status_code=400,
            detail="Face encoding failed"
        )

    face_encoding = encodings[0]

    # 5️⃣ Save embedding
    result = users_collection.update_one(
        {"email": email},
        {"$set": {"face_embedding": face_encoding.tolist()}}
    )

    if result.matched_count == 0:
        return {
            "success": False,
            "message": "User not found"
        }

    return {
        "success": True,
        "message": "Face registered successfully using webcam"
    }