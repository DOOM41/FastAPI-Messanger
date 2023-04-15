# FastAPI
from typing import Any
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException, WebSocketException

# APPS
from chats.models import Chat
from chats import crud
from auth.models import User


def check_user_in_chat(
    current_user: User,
    chat: Chat,
    is_ws: bool = False
) -> None:
    if is_ws and current_user.id != chat.from_id and current_user.id != chat.to_id:
        raise WebSocketException(400, {'res': 'You are not in this chat'})
    elif current_user.id != chat.from_id and current_user.id != chat.to_id:
        raise HTTPException(
            status_code=400,
            detail={'res': 'You are not in this chat'}
        )
    return


async def check_user_in_chat_ws(
    current_user: User,
    chat: Chat
):
    if current_user.id != chat.from_id and current_user.id != chat.to_id:
        raise WebSocketException(400, 'This user not in this chat')
    return True


def check_chat_existed(
    chat: Chat,
    is_ws: bool = False
) -> Chat:
    if is_ws and not chat:
        raise WebSocketException(404, 'Chat not found')
    elif not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )
    return
