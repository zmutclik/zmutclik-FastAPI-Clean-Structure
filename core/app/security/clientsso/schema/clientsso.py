from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ClientSSOSchema(BaseModel):
    clientsso_id: str
    clientsso_secret: str
    nama: str
    ipaddress: str
    callback_uri: str
    disabled: bool


class ClientSSOCodeSchema(BaseModel):
    clientsso_id: str
    client_id: str
    user_id: int
    code: str
