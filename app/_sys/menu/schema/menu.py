from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MenuSchema(BaseModel):
    id: int = Field(None, description="ID")
    text: str = Field(None, description="label text")
    segment: str = Field(None, description="segment func code")
    tooltip: str = Field(None, description="tooltip")
    href: str = Field(None, description="href link")
    icon: str = Field(None, description="icon menu")
    icon_color: str = Field(None, description="icon color menu")
    sort: int = Field(None, description="sort number")
    menutype_id: str = Field(None, description="menutype ID")
    parent_id: str = Field(None, description="parent ID")
    disabled: str = Field(None, description="disabled")
