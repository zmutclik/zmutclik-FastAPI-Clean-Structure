from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CrossOriginSchema(BaseModel):
    id: int = Field(None, description="ID")
    link: str = Field(None, description="allowed link")
