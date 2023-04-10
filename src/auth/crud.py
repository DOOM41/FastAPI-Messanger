from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User


async def get_user(db: AsyncSession, id: int):
    statement = select(User).filter(
        User.id == id
    )
    result = await db.execute(statement)
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    statement = select(User).offset(skip).limit(limit)
    result = await db.execute(statement)
    return result.scalars().all()