from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: int = None
    role: str = None
    scopes: list[str] = []

    class Config:
        validate_assignment = True