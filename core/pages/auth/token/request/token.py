from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime
from typing import Optional


class TokenRequest(BaseModel):
    grant_type: str
    client_id: str
    client_secret: str
    code: Optional[str] = None
    refresh_token: Optional[str] = None
