from typing import Optional
from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: int = None
    roles: list[str] = []
    scopes: list[str] = []
    username: str = None
    channel: str = None
    client_id: Optional[str] = None
    session_id: Optional[str] = None

    class Config:
        validate_assignment = True
