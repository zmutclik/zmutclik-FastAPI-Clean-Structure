from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MenuSchema(BaseModel):
    id: int
    text: str
    segment: str
    tooltip: Optional[str] 
    href: str
    icon: str
    icon_color: str
    sort: int
    menutype_id: int
    parent_id: int
    disabled: bool


class MenuViewSchema(BaseModel):
    id: str = Field(coerce_numbers_to_str=True)
    text: str
    segment: str
    tooltip: Optional[str]
    href: str
    icon: str
    disabled: Optional[bool] 
    parent_id: str = Field(coerce_numbers_to_str=True)
