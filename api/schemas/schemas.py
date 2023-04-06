from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, validator


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


class MinUser(BaseModel):
    id: int
    email: str


class ChatSchema(BaseModel):
    id: int
    from_user: MinUser
    to_user: MinUser

    class Config:
        orm_mode = True

    @validator('from_user', 'to_user', pre=True)
    def parse_from_user(cls, value):
        return MinUser(id=value.id, email=value.email)


class ChatList(BaseModel):
    chats: List[ChatSchema]

class MessageSchema(BaseModel):
    content: str
    date: datetime = None

class MessageReadSchema(BaseModel):
    chat_id: int
    content: str
    date: datetime = None
    from_user: MinUser

    class Config:
        orm_mode = True

    @validator('from_user', pre=True)
    def parse_from_user(cls, value):
        return MinUser(id=value.id, email=value.email)


class MessageList(BaseModel):
    messages: List[MessageReadSchema]
