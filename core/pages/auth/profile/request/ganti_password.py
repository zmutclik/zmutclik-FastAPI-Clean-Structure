from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class GantiPasswordRequest(BaseModel):
    password_lama: str
    password_baru1: str
    password_baru2: str
