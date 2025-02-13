from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class ClientSSORequest(BaseModel):
    nama: str
    ipaddress: str
    callback_uri: str
    disabled: bool
