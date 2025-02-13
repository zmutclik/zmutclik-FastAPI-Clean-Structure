from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time, datetime


class ClientSSOResponse(BaseModel):
    clientsso_id: str
    clientsso_secret: str
    nama: str
    ipaddress: str
    callback_uri: str
    disabled: bool
