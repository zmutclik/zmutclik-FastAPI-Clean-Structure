from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class AkunResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    nohp: str
    full_name: str
    disabled: bool
