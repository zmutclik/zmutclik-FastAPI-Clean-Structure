from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
