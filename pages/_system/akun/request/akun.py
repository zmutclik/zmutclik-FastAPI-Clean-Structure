from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class AkunRequest(BaseModel):
    username: str
    email: EmailStr
    nohp: str
    full_name: str
    disabled: bool
    privileges: list[int]
    scopes: list[int]
