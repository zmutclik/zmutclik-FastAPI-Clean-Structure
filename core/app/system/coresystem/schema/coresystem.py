from datetime import datetime 
from typing import Optional 
from pydantic import BaseModel, Field 
 
 
class CoreSYSTEMSchema(BaseModel): 
    id: int = Field(None, description="ID") 
    coresystem: str = Field(None, description="coresystem") 
