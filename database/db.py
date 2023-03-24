from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from fastapi import Depends

RDB_PATH = "sqlite+aiosqlite:///./test.db"
ECHO_LOG = True

engine = create_async_engine(
    RDB_PATH, echo=ECHO_LOG
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass



