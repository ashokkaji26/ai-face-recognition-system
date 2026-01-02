from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    created_at: datetime = datetime.now(timezone.utc)


class UserLogin(BaseModel):
    email: EmailStr