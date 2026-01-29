from pydantic import BaseModel, Field
from datetime import date
from dateutil.relativedelta import relativedelta
from enum import Enum


class Status(Enum):
    ACCEPTED = 0
    IN_PROGRESS = 1
    READY = 2
    
    
class Workshop(Enum):
    SEWING_WORKSHOP = 0
    METALWORKING_WORKSHOP = 1 


class TaskAddSchema(BaseModel):
    org_name: str
    task : str
    workshop : Workshop
    status : Status
    begin_date : date = Field(default_factory = lambda: date.today())
    dead_line : date = Field(default_factory = lambda: date.today() + relativedelta(months=1),ge=date.today())
    
    
class TaskSchema(TaskAddSchema):
    id : int
    
