from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class OtpRequest(BaseModel):
    email: EmailStr
    
class OtpLoginRequest(BaseModel):
    email: EmailStr
    code: int
