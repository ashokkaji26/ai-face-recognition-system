import cv2
import os

# -----------------------------
# Load Haar Cascade Model
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CASCADE_PATH = os.path.join(
    BASE_DIR, "models", "haarcascade_frontalface_default.xml"
)

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

if face_cascade.empty():
    raise RuntimeError("❌ Failed to load Haar Cascade model")

print("✅ Haar Cascade loaded successfully")


# -----------------------------
# Face Detection Function
# -----------------------------
def detect_faces(image_path):
    """
    Detect faces in an image and return bounding boxes
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError("Image not found")

    # Read image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Invalid image file")

    # Convert to grayscale (required for Haar)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    results = []
    for (x, y, w, h) in faces:
        results.append({
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h)
        })

    return results


# -----------------------------
# LOCAL TEST (TEMPORARY)
# -----------------------------
if __name__ == "__main__":
    test_image = "test.jpg"  # put a test image here
    try:
        detections = detect_faces(test_image)
        print("🟢 Faces detected:", detections)
    except Exception as e:
        print("🔴 Error:", e)