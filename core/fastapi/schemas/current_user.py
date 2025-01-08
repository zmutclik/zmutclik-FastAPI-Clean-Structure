from typing import Optional
from pydantic import BaseModel


class CurrentUser(BaseModel):
    username: str = None
    roles: list[str] = []
    scopes: list[str] = []
    channel: str = None
    client_id: Optional[str] = None
    session_id: Optional[str] = None

    class Config:
        validate_assignment = True
