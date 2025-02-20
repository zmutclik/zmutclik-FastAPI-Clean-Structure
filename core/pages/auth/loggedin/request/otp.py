from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime
from typing import Optional


class OtpRequest(BaseModel):
    email: EmailStr
    
class OtpLoginRequest(BaseModel):
    email: EmailStr
    code: int
    client_id: Optional[str] = None
