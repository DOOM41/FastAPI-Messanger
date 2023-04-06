from typing import Annotated

from fastapi import Depends
from ..controllers.main import get_db

from database.db import SessionLocal
from ..utils.utils import get_current_active_user

from ..schemas import schemas
from database import crud, models

from sqlalchemy.orm import Session


def create_chat(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    user_id,
    db: Session = Depends(get_db)
):
    chats = crud.get_chats_by_user(
        db=db,
        user=current_user
    )
    if chats:
        return {"res": 'existed'}
    chat = crud.create_chat(
        db,
        current_user.id,
        user_id
    )
    return chat


def get_own_chats(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    chats = crud.get_chats_by_user(
        db=db,
        user=current_user
    )
    return schemas.ChatList(
        chats=chats
    )


def send_message(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    message: schemas.MessageSchema,
    chat_id: int,
    db: Session = Depends(get_db)
):
    crud.create_user_message(
        db,
        message,
        chat_id,
        current_user
    )
    return {"res": 'sended'}


def get_messages(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    chat_id: int,
    db: Session = Depends(get_db)
):
    chat: models.Chat = crud.get_chat(db, chat_id)
    if current_user.id != chat.from_id and current_user.id != chat.to_id:
        return {'res': 'You are not in this chat'}
    messages = crud.get_messages_by_chat_id(db, chat_id)
    return schemas.MessageList(messages=messages)
