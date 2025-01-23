from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CrossOriginSchema(BaseModel):
    id: int 
    link: str 
