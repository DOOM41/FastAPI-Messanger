from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from auth.models import User
from chats import models

from sqlalchemy.ext.asyncio import AsyncSession


async def create_chat(db: AsyncSession, from_c: User, to_c: User):
    db_chat = models.Chat(
        from_id=from_c,
        to_id=to_c
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def get_chat(db: AsyncSession, chat_id: int):
    return db.s(models.Chat).filter(models.Chat.id == chat_id).first()


def get_chats_by_user(db: Session, user: User):
    return db.query(models.Chat).options(
        joinedload(models.Chat.from_user),
        joinedload(models.Chat.to_user)
    ).filter(or_(
        models.Chat.from_user == user,
        models.Chat.to_user == user,
    )).all()