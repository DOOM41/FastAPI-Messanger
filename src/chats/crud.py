from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, select

from auth.models import User
from chats import models

from sqlalchemy.ext.asyncio import AsyncSession


async def create_chat(
        db: AsyncSession, 
        from_c: User,
        to_c: User
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
    # await breakpoint()
    return await db(models.Chat).filter(
        models.Chat.id == chat_id
    ).first()


async def get_chats_by_user(
    db: AsyncSession,
    user: User,
    user_id: int = 0
):
    # breakpoint()
    statement = select(models.Chat).options(
        joinedload(models.Chat.from_user),
        joinedload(models.Chat.to_user)
    ).filter(or_(
        models.Chat.from_user == user,
        models.Chat.to_user == user,
    ))
    result = await db.execute(statement)
    return result.scalars().all()
