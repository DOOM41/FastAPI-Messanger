from datetime import datetime
from typing import AsyncGenerator
from .db import (
    Base,
    engine,
    async_session_maker,
    Depends
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.dialects.sqlite import INTEGER
from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from sqlalchemy.orm import Mapped, mapped_column


SQLITE3_NAME = "./db.sqlite3"


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # def __init__(self, username, password, mail):
    #     self.username = username
    #     # password store with hash
    #     self.password = hashlib.md5(password.encode()).hexdigest()
    #     self.mail = mail

    # def __str__(self):
    #     return str(self.id) + ':' + self.username


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class Message(Base):
    """
    User Messages

    id : pk
    from_user_id : foreign key
    to_user_id : string
    content : string
    date : datetime.now
    """
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    from_user_id = Column('from_user_id', ForeignKey('user.id'))
    to_user_id = Column('to_user_id', ForeignKey('user.id'))
    content = Column('content', String(256))
    date = Column(
        'date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
    )

    def __init__(self, from_user_id: int, to_user_id: int, content: str, date: datetime = datetime.now()):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.content = content
        self.date = date

    def __str__(self):
        return str(self.id) + \
            ':user_id -> ' + str(self.user_id) + \
            ', content -> ' + self.content + \
            ', date -> ' + self.date.strftime('%Y%m%d - %H:%M:%S')
