from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class ScopeRequest(BaseModel):
    scope: str
    desc: str
