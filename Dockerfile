FROM python:3.10-slim

# ---- System dependencies for dlib & face-recognition ----
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ---- Set working directory ----
WORKDIR /app

# ---- Install Python dependencies ----
COPY server/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---- Copy backend code ----
COPY server/ .

# ---- Expose port ----
EXPOSE 8000

# ---- Start FastAPI ----
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]