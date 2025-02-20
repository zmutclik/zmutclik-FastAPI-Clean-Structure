from typing import Optional
from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class ForgetPasswordRequest(BaseModel):
    email: EmailStr
    client_id: str


class ForgetPasswordGantiRequest(BaseModel):
    email: EmailStr
    code: str
    password: str
    password2: str
