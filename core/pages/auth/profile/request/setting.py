from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class SettingProfileRequest(BaseModel):
    full_name: str
    email: str
    nohp: str
