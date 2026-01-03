from fastapi import APIRouter, HTTPException
from models.user import UserCreate, UserLogin
from database import users_collection
from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
def signup(user: UserCreate):
    # Normalize email
    email = user.email.strip().lower()

    existing = users_collection.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = {
        "name": user.name.strip(),
        "email": email,
        "created_at": datetime.now(timezone.utc)
    }

    try:
        users_collection.insert_one(new_user)
    except DuplicateKeyError:
        # Safety net for race condition
        raise HTTPException(status_code=400, detail="User already exists")

    return {
        "success": True,
        "user": {
            "name": new_user["name"],
            "email": new_user["email"]
        }
    }


@router.post("/login")
def login(user: UserLogin):
    email = user.email.strip().lower()

    existing = users_collection.find_one({"email": email})
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    # Defensive check (very rare but safe)
    if "name" not in existing or "email" not in existing:
        raise HTTPException(
            status_code=500,
            detail="User record is corrupted"
        )

    return {
        "success": True,
        "user": {
            "name": existing["name"],
            "email": existing["email"]
        }
    }