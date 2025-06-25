from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    display_name: str
    company_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    company_name: Optional[str] = None
    phone_number: Optional[str] = None
    notification_preferences: Optional[dict] = None

class User(UserBase):
    id: str
    uid: str
    role: str = "user"  # user, admin
    phone_number: Optional[str] = None
    notification_preferences: dict = {
        "email": True,
        "whatsapp": False,
        "high_risk_only": False
    }
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str