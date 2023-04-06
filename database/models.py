from datetime import datetime
from .db import (
    Base,
    engine
)
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import Mapped, relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    from_id = Column('from_id', ForeignKey('users.id'))
    to_id = Column('to_id', ForeignKey('users.id'))

    from_user = relationship("User", foreign_keys=[from_id])
    to_user = relationship("User", foreign_keys=[to_id])


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    from_user_id = Column('from_user_id', ForeignKey('users.id'))
    chat_id = Column('chat_id', ForeignKey('chats.id'))
    content = Column('content', String(256))
    date = Column(
        'date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
    )
    
    from_user = relationship("User", foreign_keys=[from_user_id])
    chat = relationship("Chat")

    def __init__(self, from_user_id: int, chat_id: int, content: str, date: datetime = datetime.now()):
        self.from_user_id = from_user_id
        self.chat_id = chat_id
        self.content = content
        self.date = date

    def __str__(self):
        return str(self.id) + \
            ':user_id -> ' + str(self.user_id) + \
            ', content -> ' + self.content + \
            ', date -> ' + self.date.strftime('%Y%m%d - %H:%M:%S')


Base.metadata.create_all(bind=engine)
