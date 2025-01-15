from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class PrivilegeRequest(BaseModel):
    privilege: str
    desc: str
    menutype_id: int
    menus: list[int]
