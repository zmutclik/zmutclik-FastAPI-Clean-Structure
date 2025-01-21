from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class ScopeReponse(BaseModel):
    id: int
    scope: str
    desc: str
