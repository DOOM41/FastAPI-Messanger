from datetime import datetime
from typing import List

from pydantic import BaseModel, validator

from auth.schemas import UserRead
from auth.models import User


class ChatSchema(BaseModel):
    id: int
    from_user: UserRead
    to_user: UserRead

    class Config:
        orm_mode = True

    @validator('from_user', 'to_user', pre=True)
    def parse_from_user(cls, value: User):
        return UserRead(
            id=value.id,
            email=value.email,
            username=value.username
        )


class ChatList(BaseModel):
    chats: List[ChatSchema]


class MessageSendSchema(BaseModel):
    content: str
    date: datetime = None

class MessageSenddSchema(BaseModel):
    content: str
    date: datetime = None
    from_user: int

class MessageReadSchema(BaseModel):
    chat_id: int
    content: str
    date: datetime = None
    from_user: UserRead

    class Config:
        orm_mode = True

    @validator('from_user', pre=True)
    def parse_from_user(cls, value: User):
        return UserRead(
            id=value.id,
            email=value.email,
            username=value.username
        )


class MessageList(BaseModel):
    messages: List[MessageReadSchema]
