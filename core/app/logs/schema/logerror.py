from datetime import datetime
from typing import Optional, Union, List
from pydantic import BaseModel, Field, field_validator


class LogErrorSchema(BaseModel):
    error_type: Optional[str]
    error_message: Optional[str]
    error_traceback: Optional[str]
    file_name: Optional[str]
    line_number: Optional[str]
    function_name: Optional[str]
