from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass

class UserSchema(BaseModel):
    id: int = None
    username: Optional[str]
    password: str
    mail: Optional[str]

    class Config:
        orm_mode = True

class UserAuth(BaseModel):
    username: str
    password: str
    email: EmailStr


class MessageSchema(BaseModel):
    from_user: int
    to_user: int
    content: str
    date: datetime = None


class MessageList(BaseModel):
    users: list[MessageSchema]