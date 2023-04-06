from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from . import models
from api.schemas import schemas
from api.controllers.main import pwd_context

# User


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Chats


def create_chat(db: Session, from_c: models.User, to_c: models.User):
    db_chat = models.Chat(
        from_id=from_c,
        to_id=to_c
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def get_chat(db: Session, chat_id: int):
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()


def get_chats_by_user(db: Session, user: models.User):
    return db.query(models.Chat).options(
        joinedload(models.Chat.from_user),
        joinedload(models.Chat.to_user)
    ).filter(or_(
        models.Chat.from_user == user,
        models.Chat.to_user == user,
    )).all()

# Messages


def create_user_message(
    db: Session,
    mess: schemas.MessageSchema,
    chat_id: int,
    user_id: int
):
    db_item = models.Message(
        **mess.dict(),
        chat_id=chat_id,
        from_user_id=user_id.id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_messages_by_chat_id(db: Session, chat_id):
    return db.query(models.Message)\
        .options(
            joinedload(models.Message.from_user)
    ).filter(
        models.Message.chat_id == chat_id
    ).all()
