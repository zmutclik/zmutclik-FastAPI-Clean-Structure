from datetime import datetime 
from typing import Optional 
from pydantic import BaseModel, Field 
 
 
class MenuTypeRequest(BaseModel): 
    menutype: str
    desc: str
