# FastAPI
from typing import Any
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException,WebSocketException

# APPS
from chats.models import Chat
from chats import crud
from auth.models import User


async def check_user_in_chat(
        session: AsyncSession,
        current_user: User,
        chat_id: int
):
    chat: Chat = await crud.get_chat(session, chat_id)
    if not chat:
        raise HTTPException(
            status_code=400,
            detail={'res': 'Chat didnt existed'}
        )
    elif current_user.id != chat.from_id and current_user.id != chat.to_id:
        raise HTTPException(
            status_code=400,
            detail={'res': 'You are not in this chat'}
        )
    return


async def check_user_in_chat_ws(
    session: AsyncSession,
    current_user: User,
    chat_id: int
):
    chat: Chat = await crud.get_chat(session, chat_id)
    if current_user.id != chat.from_id and current_user.id != chat.to_id:
        raise WebSocketException(400, 'This user not in this chat')
    return True


async def check_chat_existed(
        chat: Chat,
        is_ws: bool = False
    ) -> Chat:
    if is_ws and not chat:
        raise WebSocketException(404,'Chat not found') 
    elif not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )
    return 