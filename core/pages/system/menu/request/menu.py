from datetime import datetime 
from typing import Optional,Union,List
from pydantic import BaseModel, Field 


class MenuRequest(BaseModel):
    text: str
    segment: str
    tooltip: Optional[str] = None
    href: str
    icon: str
    disabled: Optional[bool]=None
    sort: Optional[int] = None