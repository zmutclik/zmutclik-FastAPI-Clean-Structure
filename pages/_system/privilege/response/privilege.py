from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class PrivilegeResponse(BaseModel):
    id: int
    privilege: str
    desc: str