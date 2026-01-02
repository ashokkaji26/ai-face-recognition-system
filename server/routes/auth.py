from fastapi import APIRouter, HTTPException
from models.user import UserCreate, UserLogin
from database import users_collection
from datetime import datetime, timezone

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
def signup(user: UserCreate):
    existing = users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = {
        "name": user.name,
        "email": user.email,
        "created_at": datetime.now(timezone.utc)
    }

    users_collection.insert_one(new_user)

    return {
        "success": True,
        "user": {
            "name": user.name,
            "email": user.email
        }
    }


@router.post("/login")
def login(user: UserLogin):
    existing = users_collection.find_one({"email": user.email})
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "success": True,
        "user": {
            "name": existing["name"],
            "email": existing["email"]
        }
    }