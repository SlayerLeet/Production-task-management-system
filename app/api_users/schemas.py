from pydantic import BaseModel
from enum import Enum, auto

class UserRoles(Enum):
    USER = auto()
    OPERATOR = auto()
    LEAD = auto()
    
class UserAddSchema(BaseModel):
    username: str
    password: str
    
class UserSchema(UserAddSchema):
    id: int
    role: UserRoles = UserRoles.USER