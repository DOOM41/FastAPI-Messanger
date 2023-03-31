from typing import Annotated

from fastapi import Depends

from database.db import SessionLocal
from ..utils.utils import get_current_user

from ..schemas import schemas
from database import crud


async def send_message(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    message: schemas.MessageSchema,
    chat_id: int
):
    mess = crud.create_user_message(
        SessionLocal(),
        message,
        current_user.id,
        chat_id
    )
    return {
        'result': "sended"
    }


async def get_message(first_id: int, second_id: int):
    
    return {}
