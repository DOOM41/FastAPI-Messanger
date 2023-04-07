from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Table, Column, Integer, String, TIMESTAMP, MetaData
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql.functions import current_timestamp
from auth.models import Base
from auth.models import User


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    from_id = Column('from_id', ForeignKey('user.id'))
    to_id = Column('to_id', ForeignKey('user.id'))

    from_user = relationship("User", foreign_keys=[from_id])
    to_user = relationship("User", foreign_keys=[to_id])


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    from_user_id = Column('from_user_id', ForeignKey('user.id'))
    chat_id = Column('chat_id', ForeignKey('chat.id'))
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

    def __init__(self, from_user: User, chat_id: int, content: str, date: datetime = datetime.now()):
        self.from_user = from_user
        self.chat_id = chat_id
        self.content = content
        self.date = date

    def __str__(self):
        return str(self.id) + \
            ':user_id -> ' + str(self.from_user_id) + \
            ', content -> ' + self.content + \
            ', date -> ' + self.date.strftime('%Y%m%d - %H:%M:%S')


