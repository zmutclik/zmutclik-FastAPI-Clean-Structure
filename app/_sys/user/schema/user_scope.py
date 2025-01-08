from datetime import datetime

from pydantic import BaseModel, Field


class UserScopeSchema(BaseModel):
    id: int
    scope: str
    desc: str
