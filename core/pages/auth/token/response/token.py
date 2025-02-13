from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: str
    id_token: str
