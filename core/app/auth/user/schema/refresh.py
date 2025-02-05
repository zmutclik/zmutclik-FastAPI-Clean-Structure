from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class RefreshTokenSchema(BaseModel):
    username: str
    client_id: str
    session_id: str
