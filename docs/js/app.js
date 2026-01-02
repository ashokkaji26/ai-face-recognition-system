const API_BASE = "http://127.0.0.1:8000";

const signupBtn = document.getElementById("signupBtn");
const loginBtn = document.getElementById("loginBtn");
const logoutBtn = document.getElementById("logoutBtn");

const nameInput = document.getElementById("nameInput");
const emailInput = document.getElementById("emailInput");

const authSection = document.getElementById("authSection");
const userEmail = document.getElementById("userEmail");

const savedUser = localStorage.getItem("ai_user");
if (savedUser) handleLogin(JSON.parse(savedUser));

signupBtn.addEventListener("click", async () => {
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

loginBtn.addEventListener("click", async () => {
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

logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("ai_user");
  location.reload();
});

function handleLogin(user) {
  localStorage.setItem("ai_user", JSON.stringify(user));
  authSection.classList.add("hidden");
  userEmail.textContent = user.email;
  userEmail.classList.remove("hidden");
  logoutBtn.classList.remove("hidden");
}