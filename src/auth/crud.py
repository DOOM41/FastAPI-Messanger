from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User


async def get_user(db: AsyncSession, id: int):
    statement = select(User).filter(
        User.id == id
    )
    result = await db.execute(statement)
    return result.scalars().first()
