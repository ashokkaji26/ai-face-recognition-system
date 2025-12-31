from fastapi import FastAPI

app = FastAPI(title="AI Task Tracker Backend")

@app.get("/")
def root():
    return {"status": "Backend running successfully 🚀"}

@app.get("/health")
def health_check():
    return {"health": "OK"}