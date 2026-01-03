const API_BASE = "http://127.0.0.1:8000";

/* ================= ELEMENTS ================= */
const signupBtn = document.getElementById("signupBtn");
const loginBtn = document.getElementById("loginBtn");
const logoutBtn = document.getElementById("logoutBtn");

const nameInput = document.getElementById("nameInput");
const emailInput = document.getElementById("emailInput");

const authSection = document.getElementById("authSection");
const userEmail = document.getElementById("userEmail");

const dashboard = document.getElementById("dashboard");
const totalDaysEl = document.getElementById("totalDays");
const presentDaysEl = document.getElementById("presentDays");
const attendancePercentEl = document.getElementById("attendancePercent");
const calendarGrid = document.getElementById("calendarGrid");

const openCameraBtn = document.getElementById("openCameraBtn");
const uploadBtn = document.getElementById("uploadBtn");
const uploadInput = document.getElementById("uploadInput");

/* Webcam elements */
const cameraBox = document.getElementById("cameraBox");
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const captureBtn = document.getElementById("captureBtn");
const closeCameraBtn = document.getElementById("closeCameraBtn");
const countdownEl = document.getElementById("countdown");

let stream = null;

/* ================= UI HELPERS ================= */
const toast = document.getElementById("toast");
const loader = document.getElementById("loader");
const loaderText = document.getElementById("loaderText");

function showToast(message, type = "success") {
  toast.textContent = message;
  toast.className = `toast ${type}`;
  toast.classList.remove("hidden");

  setTimeout(() => {
    toast.classList.add("hidden");
  }, 3000);
}

function showLoader(text = "Processing...") {
  loaderText.textContent = text;
  loader.classList.remove("hidden");
}

function hideLoader() {
  loader.classList.add("hidden");
}

/* 🔥 HARD SAFETY: loader can NEVER stay forever */
window.addEventListener("load", hideLoader);
setTimeout(hideLoader, 8000);

/* ================= SESSION ================= */
window.addEventListener("DOMContentLoaded", () => {
  const savedUser = localStorage.getItem("ai_user");
  if (savedUser) {
    handleLogin(JSON.parse(savedUser));
  } else {
    hideLoader();
  }
});

/* ================= SIGNUP ================= */
signupBtn?.addEventListener("click", async () => {
  const name = nameInput.value.trim();
  const email = emailInput.value.trim();
  if (!name || !email) return alert("All fields required");

  const res = await fetch(`${API_BASE}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email })
  });

  const data = await res.json();
  if (data.success) handleLogin(data.user);
  else alert(data.message);
});

/* ================= LOGIN ================= */
loginBtn?.addEventListener("click", async () => {
  const email = emailInput.value.trim();
  if (!email) return alert("Email required");

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  });

  const data = await res.json();
  if (data.success) handleLogin(data.user);
  else alert(data.message);
});

/* ================= LOGOUT ================= */
logoutBtn?.addEventListener("click", () => {
  localStorage.removeItem("ai_user");
  location.reload();
});

/* ================= HANDLE LOGIN ================= */
function handleLogin(user) {
  localStorage.setItem("ai_user", JSON.stringify(user));

  authSection?.classList.add("hidden");
  dashboard?.classList.remove("hidden");

  userEmail.textContent = user.email;
  userEmail.classList.remove("hidden");
  logoutBtn.classList.remove("hidden");

  loadAttendanceDashboard(user.email);
}

/* ================= LOAD DASHBOARD ================= */
async function loadAttendanceDashboard(email) {
  showLoader("Loading attendance...");

  try {
    const res = await fetch(
      `${API_BASE}/attendance/history?email=${encodeURIComponent(email)}`
    );

    if (!res.ok) throw new Error("Failed to fetch attendance");

    const data = await res.json();
    if (!data.success) throw new Error("Invalid attendance data");

    setupCalendarControls(data.attendance);

  } catch (err) {
    console.error("Dashboard error:", err);
    showToast("Failed to load attendance", "error");
  } finally {
    hideLoader();
  }
}

/* ================= CALENDAR ================= */
function renderCalendar(attendanceDates, month, year) {
  calendarGrid.innerHTML = "";

  const daysInMonth = new Date(year, Number(month) + 1, 0).getDate();
  let presentCount = 0;

  for (let day = 1; day <= daysInMonth; day++) {
    const dateStr = `${year}-${String(Number(month) + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    const dayEl = document.createElement("div");

    dayEl.classList.add("calendar-day");
    dayEl.dataset.date = dateStr;

    if (attendanceDates.includes(dateStr)) {
      dayEl.classList.add("present");
      presentCount++;
    }

    calendarGrid.appendChild(dayEl);
  }

  totalDaysEl.textContent = daysInMonth;
  presentDaysEl.textContent = presentCount;
  attendancePercentEl.textContent =
    Math.round((presentCount / daysInMonth) * 100) + "%";
}

/* ================= CALENDAR CONTROLS ================= */
function setupCalendarControls(attendanceDates) {
  const monthSelect = document.getElementById("monthSelect");
  const yearSelect = document.getElementById("yearSelect");

  if (!monthSelect || !yearSelect) return;

  const today = new Date();
  const currentYear = today.getFullYear();

  monthSelect.innerHTML = "";
  yearSelect.innerHTML = "";

  const months = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
  ];

  months.forEach((m, i) => {
    const opt = document.createElement("option");
    opt.value = i;
    opt.textContent = m;
    monthSelect.appendChild(opt);
  });

  for (let y = currentYear; y >= currentYear - 4; y--) {
    const opt = document.createElement("option");
    opt.value = y;
    opt.textContent = y;
    yearSelect.appendChild(opt);
  }

  monthSelect.value = today.getMonth();
  yearSelect.value = currentYear;

  renderCalendar(attendanceDates, monthSelect.value, yearSelect.value);

  monthSelect.onchange = () =>
    renderCalendar(attendanceDates, monthSelect.value, yearSelect.value);

  yearSelect.onchange = () =>
    renderCalendar(attendanceDates, monthSelect.value, yearSelect.value);
}

/* ================= IMAGE UPLOAD ================= */
uploadBtn?.addEventListener("click", () => uploadInput.click());

uploadInput?.addEventListener("change", async () => {
  const file = uploadInput.files[0];
  if (!file) return;
  await markAttendance(file);
});

/* ================= WEBCAM ================= */
openCameraBtn?.addEventListener("click", async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    cameraBox.classList.remove("hidden");
  } catch {
    alert("Camera access denied");
  }
});

closeCameraBtn?.addEventListener("click", stopCamera);

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }
  cameraBox.classList.add("hidden");
}

/* ================= COUNTDOWN ================= */
function startCountdown(callback) {
  let count = 3;
  countdownEl.textContent = count;
  countdownEl.classList.remove("hidden");

  const timer = setInterval(() => {
    count--;
    if (count === 0) {
      clearInterval(timer);
      countdownEl.classList.add("hidden");
      callback();
    } else {
      countdownEl.textContent = count;
    }
  }, 1000);
}

/* ================= CAPTURE ================= */
captureBtn?.addEventListener("click", () => {
  startCountdown(() => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {
      await smartWebcamAction(blob);
    }, "image/jpeg");
  });
});

/* ================= SMART WEBCAM ACTION ================= */
async function smartWebcamAction(imageBlob) {
  const result = await markAttendance(imageBlob, false);

  if (result === "NOT_REGISTERED") {
    const registered = await registerFaceWebcam(imageBlob);
    if (registered) {
      await markAttendance(imageBlob, true);
    }
  }

  stopCamera();
}

/* ================= MARK ATTENDANCE ================= */
async function markAttendance(imageBlob, showAlert = true) {
  showLoader("Marking attendance...");

  const user = JSON.parse(localStorage.getItem("ai_user"));
  if (!user) {
    hideLoader();
    return false;
  }

  const formData = new FormData();
  formData.append("email", user.email);
  formData.append("file", imageBlob);

  try {
    const res = await fetch(`${API_BASE}/attendance/mark`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (res.ok && data.success) {
      if (showAlert) showToast("Attendance marked successfully", "success");
      loadAttendanceDashboard(user.email);
      return true;
    }

    const errorMessage = data.message || data.detail;
    if (errorMessage === "User face not registered") {
      return "NOT_REGISTERED";
    }

    showToast(errorMessage || "Attendance failed", "error");
    return false;

  } catch (err) {
    console.error(err);
    showToast("Server error", "error");
    return false;
  } finally {
    hideLoader();
  }
}

/* ================= WEBCAM FACE REGISTRATION ================= */
async function registerFaceWebcam(imageBlob) {
  showLoader("Registering face...");

  const user = JSON.parse(localStorage.getItem("ai_user"));
  if (!user) {
    hideLoader();
    return false;
  }

  const formData = new FormData();
  formData.append("email", user.email);
  formData.append("file", imageBlob);

  try {
    const res = await fetch(`${API_BASE}/face/register-webcam`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (data.success) {
      showToast("Face registered successfully", "success");
      return true;
    }

    showToast(data.message || "Face registration failed", "error");
    return false;

  } catch {
    showToast("Server error during registration", "error");
    return false;
  } finally {
    hideLoader();
  }
}