from datetime import datetime 
from typing import Optional 
from pydantic import BaseModel, Field 
 
 
class MenuTypeResponse(BaseModel): 
    id: int
    menutype: str
    desc: str
