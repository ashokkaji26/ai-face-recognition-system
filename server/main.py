from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import base64

app = FastAPI()

# =========================
# CORS (for frontend later)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Load Haar Cascade
# =========================
face_cascade = cv2.CascadeClassifier(
    "models/haarcascade_frontalface_default.xml"
)

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
# FACE DETECTION API (STEP 3.3)
# =========================
@app.post("/detect-face")
async def detect_face(file: UploadFile = File(...)):
    # Read image bytes
    image_bytes = await file.read()

    # Convert bytes to numpy array
    np_arr = np.frombuffer(image_bytes, np.uint8)

    # Decode image
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        return {"success": False, "message": "Invalid image"}

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

    # Draw bounding boxes
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
        return {"success": False, "message": "Failed to encode image"}

    image_base64 = base64.b64encode(buffer).decode("utf-8")

    return {
        "success": True,
        "faces_detected": len(face_list),
        "faces": face_list,
        "image_base64": image_base64
    }