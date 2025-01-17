from datetime import datetime 
from typing import Optional,Union,List
from pydantic import BaseModel, Field ,field_validator
 
class MenuResponse(BaseModel):
    id: str = Field(coerce_numbers_to_str=True)
    text: str
    segment: str
    tooltip: Optional[str] 
    href: str
    icon: str
    disabled: str
    
    
    @field_validator("disabled", mode="before")
    @classmethod
    def convert_bool_to_str(cls, v):
        if isinstance(v, bool):
            return str("0")  # Konversi otomatis
        return "1"
    
class MenusResponse(MenuResponse):
    children: List['MenusResponse'] = Field(default_factory=list)