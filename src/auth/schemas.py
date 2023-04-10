from typing import List, Optional

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, validator

from auth.models import User


class UserRead(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        orm_mode = True
        

class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    
    
class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


class UserList(BaseModel):
    users: List[UserRead]
    
    # @validator('users', pre=True)
    # def parse_from_user(cls, value: User):
    #     return UserRead(
    #         id=value.id,
    #         email=value.email,
    #         username=value.username
    #     )