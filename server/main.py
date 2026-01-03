from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes.face import router as face_router
from routes.auth import router as auth_router
from routes.attendance import router as attendance_router

import cv2
import numpy as np
import base64
from pathlib import Path

app = FastAPI()

# =========================
# CORS (Frontend access)
# =========================
# ⚠️ For development only
# In production, replace "*" with frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# INCLUDE ROUTERS
# =========================
app.include_router(auth_router)
app.include_router(face_router)
app.include_router(attendance_router)

# =========================
# Load Haar Cascade safely
# =========================
BASE_DIR = Path(__file__).resolve().parent
cascade_path = BASE_DIR / "models" / "haarcascade_frontalface_default.xml"

face_cascade = cv2.CascadeClassifier(str(cascade_path))

if face_cascade.empty():
    raise RuntimeError("❌ Failed to load Haar Cascade")

print("✅ Haar Cascade loaded successfully")

# =========================
# Health Check
# =========================
@app.get("/")
def root():
    return {"message": "AI Face Recognition Backend is running 🚀"}

# =========================
# FACE DETECTION API
# =========================
@app.post("/detect-face")
async def detect_face(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file type")

    try:
        # Read image bytes
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Empty image file")

        # Convert bytes to numpy array
        np_arr = np.frombuffer(image_bytes, np.uint8)

        # Decode image
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        face_list = []

        for (x, y, w, h) in faces:
            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            face_list.append({
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h)
            })

        # Encode image to Base64
        success, buffer = cv2.imencode(".jpg", image)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to encode image")

        image_base64 = base64.b64encode(buffer).decode("utf-8")

        return {
            "success": True,
            "faces_detected": len(face_list),
            "faces": face_list,
            "image_base64": image_base64
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Face detection failed: {str(e)}"
        )