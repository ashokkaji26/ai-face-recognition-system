# 🤖 AI Face Attendance System

A **production-ready AI-powered attendance system** that uses **face recognition** to automatically mark attendance.  
Built with **FastAPI, OpenCV, face-recognition (dlib)** on the backend and a **modern frontend hosted on GitHub Pages**.

> ⚠️ This project is deployed using **Docker** to handle heavy AI/ML dependencies and real-world cloud constraints.

---

## 🚀 Live Demo

- 🌐 **Frontend (GitHub Pages)**  
  👉 https://ashokkaji26.github.io/ai-face-recognition-system/

- 🧠 **Backend API (Railway)**  
  👉 https://ai-face-recognition-system-production.up.railway.app/

- 📘 **API Documentation (Swagger)**  
  👉 https://ai-face-recognition-system-production.up.railway.app/docs

---

## ✨ Key Features

- 🎯 **AI Face Recognition Attendance**
- 📸 Webcam & Image Upload Support
- 🧠 Automatic Face Registration
- 📊 Attendance History & Calendar View
- ☁️ Cloud Deployed (Docker + Railway)
- 🔐 Secure MongoDB Integration
- 🌐 Fully HTTPS (No Mixed Content Issues)

---

## 🧠 Tech Stack

### 🔹 Backend
- **FastAPI** – High-performance Python API
- **OpenCV** – Image processing
- **face-recognition (dlib)** – Face detection & encoding
- **MongoDB Atlas** – Cloud database
- **Docker** – Production deployment
- **Uvicorn** – ASGI server

### 🔹 Frontend
- **HTML, CSS, JavaScript**
- **GitHub Pages** – Static hosting

---

## 🏗️ Architecture Overview
Frontend (GitHub Pages - HTTPS)
|
|  HTTPS API Calls
↓
Backend (FastAPI + Docker - Railway)
|
↓
MongoDB Atlas (Cloud Database)

---

## 📸 How It Works

1️⃣ User signs up / logs in using email  
2️⃣ User uploads an image or uses webcam  
3️⃣ Face is detected & encoded using AI  
4️⃣ Attendance is marked automatically  
5️⃣ User can view attendance history & calendar  

---

## 🧪 API Endpoints (Sample)

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/auth/signup` | Register user |
| POST | `/auth/login` | Login user |
| POST | `/attendance/mark` | Mark attendance |
| GET | `/attendance/history` | Attendance history |
| POST | `/face/register-webcam` | Face registration |

👉 Full API available at `/docs`

---

## 🔐 Environment Variables

These are required for deployment:

```env
MONGO_URI=your_mongodb_atlas_uri
DB_NAME=ai_face_attendance

---

🐳 Why Docker?

This project uses Docker because:
	•	face-recognition depends on dlib, which is heavy
	•	Cloud platforms often fail without system-level dependencies
	•	Docker ensures consistent builds across environments
	•	This reflects real-world ML deployment practices

⸻

⚠️ Important Deployment Learnings:
	•	Fixed Mixed Content errors (HTTPS frontend → HTTPS backend)
	•	Proper CORS configuration for GitHub Pages
	•	Optimized memory usage for AI libraries
	•	Used Docker to avoid build failures on cloud platforms

---

📂 Project Structure:
ai-face-recognition-system/
│
├── server/
│   ├── main.py
│   ├── database.py
│   ├── routes/
│   ├── models/
│   └── requirements.txt
│
├── client/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── Dockerfile
├── README.md
└── .gitignore

---

🧑‍💻 Local Setup:
git clone https://github.com/ashokkaji26/ai-face-recognition-system.git
cd ai-face-recognition-system/server
pip install -r requirements.txt
uvicorn main:app --reload

---

🔮 Future Enhancements
	•	🛡️ Admin Analytics Dashboard
	•	📤 CSV Export
	•	🔁 Face Re-training
	•	🔐 JWT Authentication
	•	📈 Advanced Attendance Insights

---

👨‍💻 Author

Ashok Kaji
	•	GitHub: https://github.com/ashokkaji26
	•	LinkedIn: https://www.linkedin.com/in/ashokkaji26/

---

⭐ If you like this project

Give it a ⭐ on GitHub — it really helps!

---

Built with ❤️ using AI, Computer Vision & Real-World Engineering

