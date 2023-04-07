from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, select, and_

from auth.models import User
from chats import models

from sqlalchemy.ext.asyncio import AsyncSession

from chats.schemas import MessageSendSchema

# Chat CRUD


async def create_chat(
        db: AsyncSession,
        from_c: int,
        to_c: int
) -> models.Chat:
    db_chat = models.Chat(
        from_id=from_c,
        to_id=to_c
    )
    db.add(db_chat)
    await db.commit()
    db.refresh(db_chat)
    return db_chat


async def get_chat(db: AsyncSession, chat_id: int):
    statement = select(models.Chat).filter(
        models.Chat.id == chat_id
    )
    result = await db.execute(statement)
    return result.scalars().first()


async def get_chats_by_users(
    db: AsyncSession,
    cur_user: User,
    to_user: User,
):
    statement = select(models.Chat).options(
        joinedload(models.Chat.from_user),
        joinedload(models.Chat.to_user)
    ).filter(or_(
        and_(
            models.Chat.from_user == cur_user,
            models.Chat.to_user == to_user,
        ),
        and_(
            models.Chat.from_user == to_user,
            models.Chat.to_user == cur_user,
        )
    ))
    result = await db.execute(statement)
    return result.scalars().all()

async def get_chats_by_user(
    db: AsyncSession,
    cur_user: User,
):
    statement = select(models.Chat).options(
        joinedload(models.Chat.from_user),
        joinedload(models.Chat.to_user)
    ).filter(or_(
            models.Chat.from_user == cur_user,
            models.Chat.to_user == cur_user,
    ))
    result = await db.execute(statement)
    return result.scalars().all()

# Message CRUD


async def create_user_message(
    db: Session,
    mess: MessageSendSchema,
    chat_id: int,
    user: User
):
    db_message = models.Message(
        **mess.dict(),
        chat_id=chat_id,
        from_user=user
    )
    db.add(db_message)
    await db.commit()
    db.refresh(db_message)
    return db_message


async def get_messages_by_chat_id(
        db: AsyncSession,
        chat_id
):
    statement = select(models.Message).options(
        joinedload(models.Message.from_user)
    ).filter(
        models.Message.chat_id == chat_id
    )
    result = await db.execute(statement)
    return result.scalars().all()
