from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: int = None
    roles: list[str] = []
    scopes: list[str] = []

    class Config:
        validate_assignment = True