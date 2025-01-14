from datetime import datetime 
from typing import Optional 
from pydantic import BaseModel, Field 
 
 
class MenuTypeSchema(BaseModel): 
    id: int = Field(None, description="ID") 
    menutype: str = Field(None, description="menutype name") 
    desc: str = Field(None, description="menutype description") 
