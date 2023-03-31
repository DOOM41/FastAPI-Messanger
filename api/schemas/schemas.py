from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    useremail: str | None = None


class MessageSchema(BaseModel):
    content: str
    date: datetime = None

    class Config:
        orm_mode = True


class MessageList(BaseModel):
    users: list[MessageSchema]
