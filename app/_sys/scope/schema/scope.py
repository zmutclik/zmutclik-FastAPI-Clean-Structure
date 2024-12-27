from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ScopeSchema(BaseModel):
    id: int = Field(None, description="ID")
    scope: str = Field(None, description="Scope name")
    desc: str = Field(None, description="description")
