from typing import Optional
from pydantic import BaseModel


class CurrentUser(BaseModel):
    username: str = None
    roles: list[int] = []
    scopes: list[int] = []
    channel: str = None
    client_id: Optional[str] = None
    session_id: Optional[str] = None

    class Config:
        validate_assignment = True
