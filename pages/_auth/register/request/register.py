from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class RegisterRequest(BaseModel):
    username: str
    password: str
    password2: str
    email: EmailStr
    nohp: str
    full_name: str
