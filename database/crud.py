from sqlalchemy.orm import Session

from . import models
from api.schemas import schemas
from api.controllers.main import pwd_context


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


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Message).offset(skip).limit(limit).all()


def create_user_message(
    db: Session,
    mess: schemas.MessageSchema,
    user_id: int,
    chat_id: int
):
    db_item = models.Message(
        **mess.dict(),
        from_user_id=user_id,
        chat_id=chat_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
